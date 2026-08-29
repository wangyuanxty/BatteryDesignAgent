# -*- coding: utf-8 -*-
"""Diagnose what limits 5C discharge for the V_D params (which plateaued at retention 0.722). Scratch."""
import json

import numpy as np
import pybamm

d = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t8_r2\cell"
pv = pybamm.ParameterValues("Chen2020")
pv.update(json.load(open(d + r"\params_r2_VD.json", encoding="utf-8")))

exp = pybamm.Experiment(["Discharge at 5C until 2.5 V"])
model = pybamm.lithium_ion.DFN(options={"thermal": "lumped"})
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()
t = sol["Time [s]"].entries
print("t_end =", round(float(t[-1]), 1), "capacity =", round(float(sol.cycles[-1]["Discharge capacity [A.h]"].entries[-1]), 3))

eta_pos = sol["X-averaged positive electrode reaction overpotential [V]"].entries
eta_neg = sol["X-averaged negative electrode reaction overpotential [V]"].entries
print("eta_pos 0/end: %.3f / %.3f" % (eta_pos[0], eta_pos[-1]))
print("eta_neg 0/end: %.3f / %.3f" % (eta_neg[0], eta_neg[-1]))

c_e = sol["Electrolyte concentration [mol.m-3]"].entries
if c_e.ndim == 3:
    c_e = c_e[:, :, -1]
print("c_e spatial t=end: min=%.0f max=%.0f  (n=%d)" % (np.min(c_e), np.max(c_e), c_e.shape[0]))
flat_ce = np.asarray(c_e).reshape(-1)
print("c_e first 15 nodes (neg side):", [round(float(x)) for x in flat_ce[:15]])
print("c_e last 15 nodes (pos side):", [round(float(x)) for x in flat_ce[-15:]])

c_s_n = sol["Negative particle concentration [mol.m-3]"].entries
c_s_p = sol["Positive particle concentration [mol.m-3]"].entries
c_n_max = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
c_p_max = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
if c_s_n.ndim == 3:
    c_s_n = c_s_n[:, :, -1]
    c_s_p = c_s_p[:, :, -1]
print("neg particle rel_cmax range t=end: %.3f - %.3f" % (np.min(c_s_n) / c_n_max, np.max(c_s_n) / c_n_max))
print("pos particle rel_cmax range t=end: %.3f - %.3f" % (np.min(c_s_p) / c_p_max, np.max(c_s_p) / c_p_max))
print("pos particle D_s =", pv["Positive electrode diffusivity [m2.s-1]"])
print("pos particle R =", pv["Positive particle radius [m]"], " tau_diff ~ R^2/D =",
      (float(pv["Positive particle radius [m]"])**2) / float(pv["Positive electrode diffusivity [m2.s-1]"]) if not callable(pv["Positive electrode diffusivity [m2.s-1]"]) else "func")