"""Diagnose LNMO aging protocol behavior: per-step termination, capacities, SEI."""
import json
from pathlib import Path

import pybamm

from bda.simulators.lnmo_parameters import lnmo_ocp

BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"
extra = json.loads(Path(BASE).read_text(encoding="utf-8"))
for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
    if isinstance(extra.get(key), str):
        extra[key] = lnmo_ocp
pv = pybamm.ParameterValues("Chen2020")
pv.update(extra, check_already_exists=False)

v_min = float(pv["Lower voltage cut-off [V]"])
v_max = float(pv["Upper voltage cut-off [V]"])
print("v_min", v_min, "v_max", v_max)

exp = pybamm.Experiment(
    [("Discharge at 1C until 2.5 V", "Charge at 1C until 4.7 V")] * 2
)
model = pybamm.lithium_ion.SPMe(options={"SEI": "ec reaction limited", "thermal": "isothermal"})
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()
print("n cycles:", len(sol.cycles))
for i, cyc in enumerate(sol.cycles):
    t = cyc["Time [s]"].entries
    V = cyc["Terminal voltage [V]"].entries
    Q = cyc["Discharge capacity [A.h]"].entries
    try:
        qc = cyc["Charge capacity [A.h]"].entries
    except Exception:
        qc = None
    print(f"--- cycle {i+1}: t {t[0]:.1f} -> {t[-1]:.1f} s, steps {len(cyc.steps)}")
    print(f"    V start {V[0]:.4f} end {V[-1]:.4f}  min {V.min():.4f} max {V.max():.4f}")
    print(f"    Discharge capacity entries: {[f'{q:.4f}' for q in Q[-6:]]} (last={Q[-1]:.4f})")
    if qc is not None:
        print(f"    Charge capacity entries: {[f'{q:.4f}' for q in qc[-6:]]} (last={qc[-1]:.4f})")
    for j, st in enumerate(cyc.steps):
        print(f"    step {j}: {st}")
sei = sol.cycles[-1]["Negative SEI thickness [m]"].entries
print("SEI end max (nm):", float(sei.max()) * 1e9)
