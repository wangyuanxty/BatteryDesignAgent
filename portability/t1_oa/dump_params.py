import pybamm

keys = [
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Separator thickness [m]", "Positive electrode porosity",
    "Negative electrode porosity", "Separator porosity",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Electrode height [m]", "Electrode width [m]", "Nominal cell capacity [A.h]",
    "Upper voltage cut-off [V]", "Lower voltage cut-off [V]",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Electrolyte conductivity [S.m-1]", "Cation transference number",
    "Electrolyte diffusivity [m2.s-1]",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]", "Negative electrode diffusivity [m2.s-1]",
]

with open("param_dump.txt", "w", encoding="utf-8") as out:
    for base in ["Chen2020", "OKane2022", "ORegan2022"]:
        pv = pybamm.ParameterValues(base)
        out.write("=== " + base + " ===\n")
        for k in keys:
            try:
                out.write("  " + k + " = " + str(pv[k]) + "\n")
            except Exception:
                out.write("  " + k + " = MISSING\n")
print("done")
