import pybamm

for base in ["Chen2020"]:
    print("=" * 20, base)
    pv = pybamm.ParameterValues(base)
    keys = [
        "Nominal cell capacity [A.h]",
        "Electrode height [m]",
        "Electrode width [m]",
        "Positive electrode thickness [m]",
        "Negative electrode thickness [m]",
        "Separator thickness [m]",
        "Positive electrode porosity",
        "Negative electrode porosity",
        "Separator porosity",
        "Positive electrode density [kg.m-3]",
        "Negative electrode density [kg.m-3]",
        "Separator density [kg.m-3]",
        "Positive current collector thickness [m]",
        "Negative current collector thickness [m]",
        "Positive current collector density [kg.m-3]",
        "Negative current collector density [kg.m-3]",
        "Upper voltage cut-off [V]",
        "Lower voltage cut-off [V]",
        "SEI kinetic rate constant [m.s-1]",
        "Positive particle radius [m]",
        "Negative particle radius [m]",
        "Electrolyte conductivity [S.m-1]",
        "Electrolyte diffusivity [m2.s-1]",
        "Cation transference number",
        "Cell volume [m3]",
        "Cell cooling surface area [m2]",
        "Total heat transfer coefficient [W.m-2.K-1]",
    ]
    for key in keys:
        try:
            print(f"  {key!r}: {pv[key]}")
        except KeyError:
            print(f"  {key!r}: MISSING")

# OKane2022 discrimination anchor check (for potential escalation)
print("=" * 20, "OKane2022 check")
pv = pybamm.ParameterValues("OKane2022")
for key in [
    "Negative electrode active material volume fraction",
    "Negative electrode specific capacity [A.h.kg-1]",
    "Negative electrode conductivity [S.m-1]",
    "Nominal cell capacity [A.h]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "SEI kinetic rate constant [m.s-1]",
    "SEI reaction exchange current density [A.m-2]",
    "Positive electrode cracking rate",
    "Negative electrode cracking rate",
    "Upper voltage cut-off [V]",
    "Cell volume [m3]",
    "Total heat transfer coefficient [W.m-2.K-1]",
]:
    try:
        print(f"  {key!r}: {pv[key]}")
    except KeyError:
        print(f"  {key!r}: MISSING")