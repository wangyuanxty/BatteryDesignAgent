import json
import pybamm

pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Electrode height [m]", "Electrode width [m]", "Nominal cell capacity [A.h]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]", "Separator thickness [m]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]", "Separator density [kg.m-3]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Positive electrode maximum concentration [mol.m-3]", "Negative electrode maximum concentration [mol.m-3]",
    "Positive electrode stoichiometry limits for reaction [0.0, 1.0]",
    "Negative electrode stoichiometry limits for reaction [0.0, 1.0]",
    "Electrolyte conductivity [S.m-1]", "Cation transference number", "Electrolyte diffusivity [m2.s-1]",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Upper voltage cut-off [V]", "Lower voltage cut-off [V]",
    "Positive electrode active material volume fraction", "Negative electrode active material volume fraction",
    "Positive electrode OCP entropic change [V.K-1]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "SEI kinetic rate constant [m.s-1]", "SEI reaction exchange current density [A.m-2]",
    "Positive electrode reaction rate constant [m.s-1]", "Negative electrode reaction rate constant [m.s-1]",
    "Positive electrode diffusivity [m2.s-1]", "Negative electrode diffusivity [m2.s-1]",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Cell cooling surface area [m2]", "Cell volume [m3]", "Total heat transfer coefficient [W.m-2.K-1]",
]
out = {}
for k in keys:
    try:
        v = pv[k]
        if isinstance(v, (int, float)):
            out[k] = float(v)
        elif isinstance(v, (list, tuple)):
            out[k] = [float(x) for x in v]
        else:
            out[k] = str(v)[:100]
    except Exception as e:
        out[k] = "ERR " + str(e)
print(json.dumps(out, indent=1))
