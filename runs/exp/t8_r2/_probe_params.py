import pybamm

pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]", "Separator thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]", "Separator density [kg.m-3]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Nominal cell capacity [A.h]",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Cation transference number",
    "Upper voltage cut-off [V]", "Lower voltage cut-off [V]",
    "Electrolyte diffusivity [m2.s-1]", "Electrolyte conductivity [S.m-1]",
    "Positive electrode active material volume fraction", "Negative electrode active material volume fraction",
    "Initial concentration in electrolyte [mol.m-3]",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "SEI kinetic rate constant [m.s-1]",
    "Cell cooling surface area [m2]", "Total heat transfer coefficient [W.m-2.K-1]", "Cell volume [m3]",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Positive electrode thermal conductivity [W.m-1.K-1]",
]
for k in keys:
    try:
        v = pv[k]
        s = str(v)
        if len(s) > 100:
            s = s[:100] + "..."
        print(f"{k} = {s}")
    except KeyError:
        print(f"{k} = <MISSING>")