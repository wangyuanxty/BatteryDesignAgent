import pybamm, json
pv = pybamm.ParameterValues("Chen2020")
keys = ["Positive electrode active material volume fraction",
        "Negative electrode active material volume fraction",
        "Negative electrode density [kg.m-3]",
        "Positive electrode density [kg.m-3]",
        "Separator density [kg.m-3]",
        "Maximum concentration in negative electrode [mol.m-3]",
        "Positive electrode maximum concentration [mol.m-3]",
        "Negative electrode OCP stoich limits",
        "Positive electrode OCP stoich limits",
        "Negative electrode stoichiometry limits for reaction [0.0, 1.0]",
        "Positive electrode stoichiometry limits for reaction [0.0, 1.0]",
        "Separator porosity",
        "Negative electrode porosity",
        "Positive electrode porosity",
        "Negative electrode thickness [m]",
        "Positive electrode thickness [m]",
        "Separator thickness [m]",
        "Electrolyte density [kg.m-3]",
        "Positive particle radius [m]",
        "Negative particle radius [m]"]
out = {}
for k in keys:
    try:
        v = pv[k]
        out[k] = v
        if hasattr(v, "value"):
            out[k] = v.value
    except KeyError:
        out[k] = "<missing>"
print(json.dumps(out, indent=1, default=str))
