"""Diagnose the electrolyte salt profile across the E3 4C charge."""
import json
from pathlib import Path

import numpy as np
import pybamm

from bda.simulators.pybamm_runner import PLATING_PARAM_DEFAULTS, THERMAL_PARAM_DEFAULTS
from bda.simulators.lnmo_parameters import lnmo_ocp

CELL = Path("cell")
BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

params = json.loads((CELL / "r7_E3_params.json").read_text(encoding="utf-8"))
extra = json.loads(Path(BASE).read_text(encoding="utf-8"))
for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
    if isinstance(extra.get(key), str):
        extra[key] = lnmo_ocp
pv = pybamm.ParameterValues("Chen2020")
pv.update(extra, check_already_exists=False)
pv.update(params)
pv.update({"Ambient temperature [K]": 318.15}, check_already_exists=False)
pv.update(PLATING_PARAM_DEFAULTS, check_already_exists=False)
for name, value in THERMAL_PARAM_DEFAULTS.items():
    if name not in pv:
        pv.update({name: value}, check_already_exists=False)

options = {"thermal": "lumped", "lithium plating": "irreversible"}
model = pybamm.lithium_ion.SPMe(options=options)
v_min = float(pv["Lower voltage cut-off [V]"])
v_max = float(pv["Upper voltage cut-off [V]"])
exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V", "Charge at 4C until 4.7 V"])
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()

t = sol["Time [s]"].entries
V = sol["Terminal voltage [V]"].entries
i0 = int(min(range(len(V)), key=lambda i: V[i]))
c_e = sol["Electrolyte concentration [mol.m-3]"]
ce_entries = np.asarray(c_e.entries, dtype=float)  # (x_nodes, t)
n_x, n_t = ce_entries.shape
print("c_e entries shape:", ce_entries.shape)
print(f"{'t_ch':>7}", "  ".join(f"node{j:>2}" for j in range(min(n_x, 12))))
for tch in (0, 100, 300, 700, 1000, 1150, 1200, 1215, 1225):
    target = t[i0] + tch
    i = min(range(len(t)), key=lambda k: abs(t[k] - target))
    row = ce_entries[:, i]
    print(f"{tch:>7}  min={row.min():7.0f}  max={row.max():7.0f}  "
          + "  ".join(f"{v:6.0f}" for v in row[:min(n_x, 12)]))
