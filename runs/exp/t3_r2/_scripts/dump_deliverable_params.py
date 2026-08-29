"""Dump Chen2020 parameters needed for closing deliverables (datasheet/BOM/calc/N-P)."""
import pybamm

pv = pybamm.ParameterValues("Chen2020")
KEYS = [
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Separator thickness [m]",
    "Separator porosity",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Initial concentration in electrolyte [mol.m-3]",
    "Cation transference number",
]
for k in KEYS:
    v = pv.get(k)
    print(f"{k} = {v}")
aliases = [
    "Positive electrode active material volume fraction",
]
# Report any function-type values verbatim
print("---function params of interest---")
for k in ("Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]"):
    print(k, "->", pv.get(k))