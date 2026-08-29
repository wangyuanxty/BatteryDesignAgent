"""Per-electrode stoichiometry readout for P1 1C discharge (calc-sheet N/P evidence).

Solves the same 1C DFN experiment as the candidate suite, then reads the
volume-averaged positive/negative electrode concentration at start/end of the
discharge step, converts to stoichiometry x (pos) / y (neg), and computes the
per-electrode consumed areal capacity with the model's own active-material
volume fractions. Identity check: both must equal the cell delivered areal
capacity (series current).
"""
import json

import numpy as np
import pybamm

params = json.loads(
    open(r"runs/exp/t3_r2/cell/r2_p1_params_final.json", encoding="utf-8-sig").read()
)
pv = pybamm.ParameterValues("Chen2020")
pv.update(params)
v_min = float(pv["Lower voltage cut-off [V]"])
area = 0.1027  # m2, Electrode height 0.065 x width 1.58

exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V"])
# matching the suite: nominal already inside params
model = pybamm.lithium_ion.DFN(options={"thermal": "lumped"})
sol = pybamm.Simulation(model, experiment=exp, parameter_values=pv).solve()

caps = sol.cycles[-1]["Discharge capacity [A.h]"].entries
cap_ah = float(caps[-1])
c_max_p = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
c_max_n = float(pv["Maximum concentration in negative electrode [mol.m-3]"])

# volume-averaged concentrations at the discharge step boundaries
pos_name = "Positive electrode stoichiometry"
neg_name = "Negative electrode stoichiometry"
c_pos = sol.cycles[-1][pos_name].entries
c_neg = sol.cycles[-1][neg_name].entries
if "stoichiometry" in pos_name:
    x0, x1 = float(c_pos[0]), float(c_pos[-1])
    y0, y1 = float(c_neg[0]), float(c_neg[-1])
else:
    x0, x1 = float(c_pos[0]) / c_max_p, float(c_pos[-1]) / c_max_p
    y0, y1 = float(c_neg[0]) / c_max_n, float(c_neg[-1]) / c_max_n

L_p, L_n = params["Positive electrode thickness [m]"], params["Negative electrode thickness [m]"]
eps_p = float(pv["Positive electrode active material volume fraction"])
eps_n = float(pv["Negative electrode active material volume fraction"])
F = 96485.0

# consumed areal capacity per electrode (Ah/m2)
pos_consumed = c_max_p * F * (x1 - x0) * L_p * eps_p / 3600.0
neg_consumed = c_max_n * F * (y0 - y1) * L_n * eps_n / 3600.0
cell_areal = cap_ah / area

out = {
    "discharge_capacity_ah": cap_ah,
    "x_start": round(float(x0), 4), "x_end": round(float(x1), 4),
    "y_start": round(float(y0), 4), "y_end": round(float(y1), 4),
    "pos_consumed_area_capacity_ah_m2": round(float(pos_consumed), 3),
    "neg_consumed_area_capacity_ah_m2": round(float(neg_consumed), 3),
    "cell_delivered_area_capacity_ah_m2": round(float(cell_areal), 3),
    "identity_pos_vs_cell": round(float(pos_consumed / cell_areal), 4),
    "identity_neg_vs_cell": round(float(neg_consumed / cell_areal), 4),
}
print(json.dumps(out, indent=2))
open(r"runs/exp/t3_r2/_logs/p1_stoich_probe.json", "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=2)
)