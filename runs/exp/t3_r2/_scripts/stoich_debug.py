"""Debug: print raw values of candidate concentration/stoichiometry variables."""
import json

import pybamm

params = json.loads(
    open(r"runs/exp/t3_r2/cell/r2_p1_params_final.json", encoding="utf-8-sig").read()
)
pv = pybamm.ParameterValues("Chen2020")
pv.update(params)
v_min = float(pv["Lower voltage cut-off [V]"])

exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V"])
model = pybamm.lithium_ion.DFN(options={"thermal": "lumped"})
sol = pybamm.Simulation(model, experiment=exp, parameter_values=pv).solve()
cyc = sol.cycles[-1]

for name in [
    "Average positive particle concentration [mol.m-3]",
    "X-averaged positive particle concentration [mol.m-3]",
    "Positive electrode stoichiometry",
    "Average positive particle stoichiometry",
    "X-averaged positive particle stoichiometry",
    "Average negative particle concentration [mol.m-3]",
    "Negative electrode stoichiometry",
    "Average negative particle stoichiometry",
]:
    try:
        arr = cyc[name].entries
        print(name, "first5:", [round(float(v), 4) for v in arr[:5]],
              "last5:", [round(float(v), 4) for v in arr[-5:]])
    except Exception as e:
        print(name, "ERR", e)