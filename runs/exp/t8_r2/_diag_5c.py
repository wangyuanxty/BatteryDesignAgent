# -*- coding: utf-8 -*-
"""Diagnostic v2: overpotential split + spatial electrolyte profile at 5C. Scratch analysis only."""
import pybamm
import numpy as np

pv = pybamm.ParameterValues("Chen2020")
exp = pybamm.Experiment(["Discharge at 5C until 2.5 V"])
model = pybamm.lithium_ion.DFN(options={"thermal": "lumped"})
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()
t = sol["Time [s]"].entries

eta_pos = sol["X-averaged positive electrode reaction overpotential [V]"].entries
eta_neg = sol["X-averaged negative electrode reaction overpotential [V]"].entries
phi_e = sol["X-averaged electrolyte potential [V]"].entries
V = sol["Terminal voltage [V]"].entries
print("t_end =", t[-1])
print(f"V(0)={V[0]:.3f}  V(end)={V[-1]:.3f}")
print(f"eta_pos 0/end: {eta_pos[0]:+.3f} / {eta_pos[-1]:+.3f}")
print(f"eta_neg 0/end: {eta_neg[0]:+.3f} / {eta_neg[-1]:+.3f}")
print(f"phi_e 0/end: {phi_e[0]:+.3f} / {phi_e[-1]:+.3f}")

c_e = sol["Electrolyte concentration [mol.m-3]"].entries
if c_e.ndim == 3:
    c_e = c_e[:, :, -1]
print("c_e shape (spatial x time):", c_e.shape)
n = c_e.shape[0]
print("c_e spatial at t=end:", [round(float(c_e[i, -1])) for i in range(n)])
print("c_e spatial at t=0.5*t_end:", [round(float(c_e[i, int(len(t)*0.5)])) for i in range(n)])

c_s_n = sol["Negative particle concentration [mol.m-3]"].entries
c_n_max = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
c_s_p = sol["Positive particle concentration [mol.m-3]"].entries
c_p_max = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
if c_s_n.ndim == 3:
    c_s_n = c_s_n[:, :, -1]
    c_s_p = c_s_p[:, :, -1]
print("neg particle conc rel_cmax range t=end:", round(float(np.min(c_s_n))/c_n_max, 3), "-", round(float(np.max(c_s_n))/c_n_max, 3))
print("pos particle conc rel_cmax range t=end:", round(float(np.min(c_s_p))/c_p_max, 3), "-", round(float(np.max(c_s_p))/c_p_max, 3))

# what does the OCV do along the way? take open-circuit via model-less approach: use stoich x-avgs
sto_n = sol["X-averaged negative electrode stoichiometry"].entries
sto_p = sol["X-averaged positive electrode stoichiometry"].entries
print("stoich neg 0/end:", round(float(sto_n[0]), 4), round(float(sto_n[-1]), 4))
print("stoich pos 0/end:", round(float(sto_p[0]), 4), round(float(sto_p[-1]), 4))