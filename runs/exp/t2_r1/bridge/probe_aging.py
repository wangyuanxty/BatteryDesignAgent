"""Read-only diagnostic: what do the aging protocol's per-cycle capacities measure?

Mirrors pybamm_runner._run_aging exactly (Chen2020 + D3 params, SPMe, SEI ec reaction
limited, isothermal, 1C CC steps between the set's voltage limits), then prints
current / voltage / SEI / stoich trajectories to pin down the per-cycle capacity
mechanics for an honest annotation.
"""
import json
from pathlib import Path

import pybamm

params = json.loads(Path("runs/exp/t2_r1/candidates/r6_d3_params.json").read_text(encoding="utf-8-sig"))
pv = pybamm.ParameterValues("Chen2020")
pv.update(params)

v_min = float(pv["Lower voltage cut-off [V]"])
v_max = float(pv["Upper voltage cut-off [V]"])
exp = pybamm.Experiment(
    [(
        f"Discharge at 1C until {v_min} V",
        f"Charge at 1C until {v_max} V",
    )] * 2
)
options = {"SEI": "ec reaction limited", "thermal": "isothermal"}
model = pybamm.lithium_ion.SPMe(options=options)
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()

def tryvar(c, name):
    try:
        e = c[name].entries
        return f"{name}: first={e[0]:.6g} mid={e[len(e)//2]:.6g} last={e[-1]:.6g}"
    except Exception as ex:
        return f"{name}: <n/a>"

for i, c in enumerate(sol.cycles):
    ct = c["Time [s]"].entries
    cv = c["Terminal voltage [V]"].entries
    ci = c["Current [A]"].entries
    dc = c["Discharge capacity [A.h]"].entries
    tp = c["Throughput capacity [A.h]"].entries
    print(f"=== cycle {i} (t {ct[0]:.1f} -> {ct[-1]:.1f} s) ===")
    idx = [0, len(ct)//4, len(ct)//2, 3*len(ct)//4, len(ct)-1]
    print("  t     :", " ".join(f"{ct[j]:9.1f}" for j in idx))
    print("  V     :", " ".join(f"{cv[j]:9.4f}" for j in idx))
    print("  I     :", " ".join(f"{ci[j]:9.4f}" for j in idx))
    print(f"  Discharge cap: n={len(dc)} first={dc[0]:.5f} last={dc[-1]:.5f} | Throughput last={tp[-1]:.5f} Ah")
    for name in ("Negative SEI thickness [m]",
                 "Average negative particle concentration [mol.m-3]",
                 "Average positive particle concentration [mol.m-3]",
                 "Negative electrode stoichiometry",
                 "Positive electrode stoichiometry"):
        print("  " + tryvar(c, name))
