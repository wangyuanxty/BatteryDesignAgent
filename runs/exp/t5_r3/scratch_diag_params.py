"""Diagnostics for the 4C plating clamp (t5_r3 round-2 problem isolation)."""
import json
import pybamm

# 1) OKane2022 keys: does it differ from Chen2020 in anode kinetics / Si content?
pv = pybamm.ParameterValues("OKane2022")
print("== OKane2022 keys of interest ==")
keys = [
    "Negative electrode OCP [V]",
    "Negative electrode OCP entropic change [V.K-1]",
    "Negative electrode diffusivity [m2.s-1]",
    "Negative electrode conductivity [S.m-1]",
    "Negative electrode active material volume fraction",
    "Negative electrode porosity",
    "Negative particle radius [m]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Negative electrode cracking rate",
    "Negative electrode thickness [m]",
    "Positive electrode cracking rate",
    "SEI kinetic rate constant [m.s-1]",
    "Lithium plating transfer coefficient",
    "Exchange-current density for plating [A.m-2]",
    "Nominal cell capacity [A.h]",
    "Separator density [kg.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
]
for k in keys:
    v = pv.get(k) if k in pv.keys() else "<MISSING>"
    print(" ", k, "=", repr(v)[:90])
nnc = [k for k in pv.keys() if "ilicon" in k or "licon" in k]
print("Si-keys:", nnc[:10])
print("n params:", len(pv.keys()))

# 2) Chen2020 plating/kinetics constants
pv2 = pybamm.ParameterValues("Chen2020")
print("== Chen2020 anode kinetics ==")
for k in [
    "Negative electrode OCP [V]",
    "Negative electrode reaction rate",
    "Negative electrode exchange-current density [A.m-2]",
    "Negative electrode charge transfer coefficient",
    "Negative electrode diffusivity [m2.s-1]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
]:
    v = pv2.get(k) if k in pv2.keys() else "<MISSING>"
    print(" ", k, "=", repr(v)[:90])