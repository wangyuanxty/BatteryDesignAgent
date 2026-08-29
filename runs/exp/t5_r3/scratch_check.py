"""Scratch env/case check for t5_r3 (agent-built input, not a simulation artifact)."""
import pybamm

print("pybamm", pybamm.__version__)
pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Separator density [kg.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Negative electrode active material volume fraction",
    "Nominal cell capacity [A.h]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Cell cooling surface area [m2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Electrolyte conductivity [S.m-1]",
    "Cation transference number",
    "Negative electrode OCP [V]",
]
for k in keys:
    v = pv.get(k) if k in pv.keys() else "<MISSING>"
    print(k, "=", repr(v)[:110])