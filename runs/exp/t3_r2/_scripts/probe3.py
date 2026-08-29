"""Probe 3: is Chen2020's native initial state already the fully-charged state?

Computes initial OCV (U_pos - U_neg at initial stoichiometries) and runs a quick SPMe 1C
discharge with NATIVE parameters to measure delivered capacity.
"""
import json

import pybamm

pv = pybamm.ParameterValues("Chen2020")
model = pybamm.lithium_ion.SPMe()
sim = pybamm.Simulation(model, parameter_values=pv)
# evaluate OCV at initial state without solving
u_pos = pv["Positive electrode OCP [V]"]
u_neg = pv["Negative electrode OCP [V]"]
x0 = float(pv["Initial concentration in positive electrode [mol.m-3]"]) / float(
    pv["Maximum concentration in positive electrode [mol.m-3]"]
)
y0 = float(pv["Initial concentration in negative electrode [mol.m-3]"]) / float(
    pv["Maximum concentration in negative electrode [mol.m-3]"]
)
ocv = float(u_pos(x0)) - float(u_neg(y0))
print(json.dumps({"x0": round(x0, 4), "y0": round(y0, 4), "initial_OCV_V": round(ocv, 4)}))
exp = pybamm.Experiment(["Discharge at 1C until 2.5 V"])
sol = pybamm.Simulation(model, experiment=exp, parameter_values=pv).solve()
print(
    json.dumps(
        {
            "cap_ah": round(float(sol.cycles[-1]["Discharge capacity [A.h]"].entries[-1]), 4),
            "V_start": round(float(sol["Terminal voltage [V]"].entries[0]), 4),
        }
    )
)