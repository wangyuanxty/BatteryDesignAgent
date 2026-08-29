import pybamm
pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode active material volume fraction", "Negative electrode active material volume fraction",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Separator density [kg.m-3]", "Separator Bruggeman coefficient (electrolyte)",
    "Positive electrode Bruggeman coefficient (electrolyte)", "Negative electrode Bruggeman coefficient (electrolyte)",
    "Maximum concentration in positive electrode [mol.m-3]", "Maximum concentration in negative electrode [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]", "Initial concentration in negative electrode [mol.m-3]",
    "Lower voltage cut-off [V]", "Upper voltage cut-off [V]",
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode specific heat capacity [J.kg-1.K-1]", "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
]
for k in keys:
    try:
        print(f"{k} = {pv[k]}")
    except Exception as e:
        print(f"{k} = MISSING ({type(e).__name__})")
print("num series:", pv.get("Number of cells connected in series to make a battery"))
print("num parallel:", pv.get("Number of electrodes connected in parallel to make a cell"))
