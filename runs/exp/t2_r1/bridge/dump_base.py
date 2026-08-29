"""Dump Chen2020 parameter-set keys relevant to t2_r1 design levers (read-only)."""
import json
import pybamm

pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Nominal cell capacity [A.h]",
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Separator thickness [m]", "Separator porosity", "Separator density [kg.m-3]",
    "Upper voltage cut-off [V]", "Lower voltage cut-off [V]",
    "SEI kinetic rate constant [m.s-1]", "SEI reaction exchange current density [A.m-2]",
    "Initial inner SEI thickness [m]", "Inner SEI reaction proportion",
    "SEI solvent diffusivity [m2.s-1]", "Outer SEI solvent diffusivity [m2.s-1]",
    "Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode OCP [V]", "Negative electrode OCP [V]",
    "Positive electrode OCP entropic change [V.K-1]",
    "Negative electrode OCP entropic change [V.K-1]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Cell volume [m3]", "Cell cooling surface area [m2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
]

def fmt(v):
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    return f"<{type(v).__name__}> {repr(v)[:120]}"

out = {}
for k in keys:
    if k in pv:
        out[k] = fmt(pv[k])
    else:
        out[k] = "<MISSING>"

missing = [k for k in keys if k not in pv]
print(json.dumps(out, indent=2, ensure_ascii=False))
print("MISSING:", missing)
