"""Dump Chen2020 parameter set values for the keys needed by the t9_r4 cell mapping."""
import json

import pybamm

pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Nominal cell capacity [A.h]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode maximum concentration [mol.m-3]",
    "Negative electrode maximum concentration [mol.m-3]",
    "Positive electrode molar mass [kg.mol-1]",
    "Positive electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]",
    "Positive electrode reaction rate constant [m.s-1]",
    "Positive electrode number of electrons transferred",
    "Lower voltage cut-off [V]", "Upper voltage cut-off [V]",
    "SEI kinetic rate constant [m.s-1]",
    "Positive electrode OCP [V]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Positive electrode surface area to volume ratio [m-1]",
    "Negative electrode surface area to volume ratio [m-1]",
    "Cell cooling surface area [m2]", "Cell volume [m3]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Electrolyte conductivity [S.m-1]", "Cation transference number",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Positive electrode exchange-current density [A.m-2]",
    "Negative electrode exchange-current density [A.m-2]",
    "SEI reaction exchange current density [A.m-2]",
]
out = {}
for k in keys:
    if k in pv:
        v = pv[k]
        if callable(v):
            try:
                out[k] = f"callable({v(0.5) if 'OCP' in k else '?'})"
            except Exception:
                out[k] = "callable(?)"
        else:
            out[k] = float(v) if isinstance(v, (int, float)) else v
    else:
        out[k] = "MISSING"
print(json.dumps(out, indent=2, default=str))
