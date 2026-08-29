"""Dump Chen2020 parameter values relevant to this case (anchor verification + architecture levers)."""
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
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator porosity",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Positive current collector conductivity [S.m-1]",
    "Negative current collector conductivity [S.m-1]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Cell cooling surface area [m2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell volume [m3]",
    "SEI kinetic rate constant [m.s-1]",
    "SEI reaction exchange current density [A.m-2]",
    "Initial inner SEI thickness [m]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode OCP [V]",
]
out = {}
for k in keys:
    try:
        v = pv[k]
        if callable(v):
            out[k] = f"<function {getattr(v, '__name__', '?')}>"
        else:
            out[k] = v
    except KeyError:
        out[k] = "<MISSING>"

# also check for plating params presence
plating_keys = [k for k in pv.keys() if "plating" in k.lower() or "plated" in k.lower()]
out["plating_param_keys"] = plating_keys
with open(r"runs\exp\t6_r1_noceiling\cell\chen2020_dump.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, default=str)
print("dumped", len(out), "keys")
