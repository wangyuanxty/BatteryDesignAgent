# -*- coding: utf-8 -*-
"""t4_r2: mechanical N/P derivation from the solved DFN (E3 params).
N/P = usable negative capacity density / usable positive capacity density
    = (cmax_neg*span_neg*F/3600*t_neg) / (cmax_pos*span_pos*F/3600*t_pos)
where span_i = |x_avg_i(t_end) - x_avg_i(t_0)| during a full 1C discharge
(same experiment as run-pyamm, DFN, E3 params). Pure model output.
"""
import json
import os
import pybamm

HERE = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t4_r2"
pset = pybamm.ParameterValues("Chen2020")
pset.update(json.load(open(os.path.join(HERE, "cell", "params_E3.json"), encoding="utf-8")))

v_min = float(pset["Lower voltage cut-off [V]"])
sim = pybamm.Simulation(
    pybamm.lithium_ion.DFN(options={}),
    experiment=pybamm.Experiment([f"Discharge at 0.1C until {v_min} V"]),
    parameter_values=pset,
)
sol = sim.solve()
print("(C/10 discharge endpoint stoichiometries ~ equilibrium material windows)")
xn = sol["Negative electrode stoichiometry"].entries
xp = sol["Positive electrode stoichiometry"].entries
Qn = float(pset["Maximum concentration in negative electrode [mol.m-3]"])
Qp = float(pset["Maximum concentration in positive electrode [mol.m-3]"])
t_neg = float(pset["Negative electrode thickness [m]"])
t_pos = float(pset["Positive electrode thickness [m]"])
F = 96485.33212

span_neg = abs(float(xn[-1] - xn[0]))
span_pos = abs(float(xp[-1] - xp[0]))
cap_neg = Qn * span_neg * F / 3600.0 * t_neg   # Ah/m2
cap_pos = Qp * span_pos * F / 3600.0 * t_pos   # Ah/m2
area = float(pset["Electrode height [m]"]) * float(pset["Electrode width [m]"])

print(f"x_neg: {float(xn[0]):.4f} -> {float(xn[-1]):.4f} (span {span_neg:.4f})")
print(f"x_pos: {float(xp[0]):.4f} -> {float(xp[-1]):.4f} (span {span_pos:.4f})")
print(f"neg usable capacity density = {cap_neg:.3f} Ah/m2  -> {cap_neg*area:.3f} Ah on 0.1027 m2")
print(f"pos usable capacity density = {cap_pos:.3f} Ah/m2  -> {cap_pos*area:.3f} Ah on 0.1027 m2")
print(f"N/P (usable) = {cap_neg/cap_pos:.4f}")
print(f"terminal voltage drift sanity: {float(sol['Terminal voltage [V]'].entries[-1]):.4f} V vs cutoff {v_min}")