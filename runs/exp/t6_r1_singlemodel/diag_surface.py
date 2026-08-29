"""Diagnose cathode/anode surface stoich during the E3 4C charge. Replicates runner model."""
import json
from pathlib import Path

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

c_max = 63104.0
t = sol["Time [s]"].entries
V = sol["Terminal voltage [V]"].entries
ap = sol["Negative electrode surface potential difference at separator interface [V]"].entries
import numpy as np


def arr(key):
    return np.asarray(sol[key].entries, dtype=float).reshape(-1)


c_avg = arr("Average positive particle concentration [mol.m-3]")
c_surf = arr("X-averaged positive particle surface concentration [mol.m-3]")
n_avg = arr("Average negative particle concentration [mol.m-3]")
n_surf = arr("X-averaged negative particle surface concentration [mol.m-3]")

# charge-phase start: the V minimum
i0 = int(min(range(len(V)), key=lambda i: V[i]))
print(f"discharge end t={t[i0]:.1f}s V={V[i0]:.4f}")
print(f"{'t_ch':>8} {'V':>7} {'anode_pot':>9} {'c_avg':>8} {'c_surf':>8} {'OCP_surf':>8} {'n_avg':>8} {'n_surf':>8} {'OCP_n_surf':>8}")
pts = [0, 30, 100, 300, 500, 700, 900, 1000, 1080, 1150, 1180, 1200, 1210, 1215, 1220, 1240]
for tch in pts:
    i = min(len(t) - 1, i0 + int(tch / (t[-1] - t[i0]) * (len(t) - 1 - i0)))
    # better: find the sample nearest to t[i0]+tch
    target = t[i0] + tch
    i = min(range(len(t)), key=lambda k: abs(t[k] - target))
    def tof(x):
        v = getattr(x, "value", x)
        return float(v)

    ocp_s = tof(lnmo_ocp(tof(c_surf[i] / c_max), 0))
    print(f"{tch:>8} {tof(V[i]):>7.4f} {tof(ap[i]):>9.4f} {tof(c_avg[i]/c_max):>8.4f} "
          f"{tof(c_surf[i]/c_max):>8.4f} {ocp_s:>8.4f} {tof(n_avg[i]/c_max):>8.4f} {tof(n_surf[i]/c_max):>8.4f}")

# OCP of negative at surface via the parameter function
try:
    import bda.simulators.lnmo_parameters as lp
    ocpn = None
except Exception:
    pass
print("negative c_max =", float(pv["Maximum concentration in negative electrode [mol.m-3]"]))
print("anode_pot at last samples:", ap[-3:])
print("V at last samples:", V[-3:])
