import pybamm

keys = [
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Positive electrode conductivity [S.m-1]",
    "Negative electrode conductivity [S.m-1]",
    "Positive current collector conductivity [S.m-1]",
    "Negative current collector conductivity [S.m-1]",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Positive current collector specific heat capacity [J.kg-1.K-1]",
    "Negative current collector specific heat capacity [J.kg-1.K-1]",
    "Positive electrode OCP entropic change [V.K-1]",
    "Negative electrode OCP entropic change [V.K-1]",
    "Negative electrode density [kg.m-3]",
    "Negative electrode active material volume fraction",
    "Negative electrode maximum concentration [mol.m-3]",
    "Positive electrode maximum concentration [mol.m-3]",
    "Negative electrode stoichiometry limits",
    "Positive electrode stoichiometry limits",
]

with open("param_dump2.txt", "w", encoding="utf-8") as out:
    for base in ["Chen2020", "OKane2022"]:
        pv = pybamm.ParameterValues(base)
        out.write("=== " + base + " ===\n")
        for k in keys:
            try:
                out.write("  " + k + " = " + str(pv[k]) + "\n")
            except Exception as e:
                out.write("  " + k + " = MISSING (" + str(e)[:80] + ")\n")
print("done")
