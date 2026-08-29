import json
import pybamm

pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Nominal cell capacity [A.h]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator porosity",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive electrode conductivity [S.m-1]",
    "Negative electrode conductivity [S.m-1]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Cell cooling surface area [m2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "SEI kinetic rate constant [m.s-1]",
]
out = {}
for k in keys:
    try:
        v = pv[k]
    except KeyError:
        out[k] = "<MISSING>"
        continue
    if callable(v):
        try:
            v = float(v(0.5))
        except Exception:
            v = "<function>"
    out[k] = v
print(json.dumps(out, indent=1, default=str))
