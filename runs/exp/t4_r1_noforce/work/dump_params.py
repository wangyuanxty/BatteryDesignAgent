"""Dump key parameters of Chen2020 / OKane2022 (evaluating function-typed keys at T=298.15K/253.15K, c_e=1000 mol/m3)."""
import json
import pybamm

scalar_keys = [
    "Cation transference number",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Separator thickness [m]", "Positive electrode porosity", "Negative electrode porosity",
    "Separator porosity", "Positive particle radius [m]", "Negative particle radius [m]",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Electrode height [m]", "Electrode width [m]", "Nominal cell capacity [A.h]",
    "Lower voltage cut-off [V]", "Upper voltage cut-off [V]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]", "Negative electrode diffusivity [m2.s-1]",
    "Positive electrode surface area per unit volume [m-1]",
    "Negative electrode surface area per unit volume [m-1]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
]
func_keys = ["Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]"]

report = {}
for base in ["Chen2020", "OKane2022"]:
    pv = pybamm.ParameterValues(base)
    d = {}
    for k in scalar_keys:
        d[k] = float(pv[k]) if k in pv else "MISSING"
    for k in func_keys:
        f = pv.get(k)
        if callable(f):
            v298 = f(1000.0, 298.15)
            v253 = f(1000.0, 253.15)
            d[k] = {
                "type": "function",
                "at_298K_c1000": float(getattr(v298, "evaluate", lambda: v298)()),
                "at_253K_c1000": float(getattr(v253, "evaluate", lambda: v253)()),
            }
        else:
            d[k] = float(f) if f is not None else "MISSING"
    report[base] = d

print(json.dumps(report, indent=1))
