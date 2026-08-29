"""Dump anchor parameters for the chosen base set (workspace-internal helper, t3_r3)."""
import json
import sys

import pybamm

KEYS = [
    "Nominal cell capacity [A.h]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator thickness [m]",
    "Separator porosity",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Positive current collector conductivity [S.m-1]",
    "Negative current collector conductivity [S.m-1]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Initial concentration in electrolyte [mol.m-3]",
]

pv = pybamm.ParameterValues(sys.argv[1] if len(sys.argv) > 1 else "Chen2020")
out = {}
for k in KEYS:
    try:
        v = pv[k]
        out[k] = float(v) if not isinstance(v, (str, bytes)) else str(v)
    except Exception as e:
        out[k] = f"MISSING: {e}"

# also report typical capacity-relevant specifics
try:
    out["_max_pos_stoich"] = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
except Exception:
    pass
try:
    out["_max_neg_stoich"] = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
except Exception:
    pass

print(json.dumps(out, indent=1))