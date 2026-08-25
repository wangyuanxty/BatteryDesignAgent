"""Inspect key parameters of available parameter sets (helper, not a deliverable)."""
import sys
import pybamm

sets = sys.argv[1:] or ["Chen2020", "ORegan2022", "OKane2022"]
keys = [
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator thickness [m]",
    "Separator porosity",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Nominal cell capacity [A.h]",
    "Upper voltage cut-off [V]",
    "Lower voltage cut-off [V]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Initial concentration in electrolyte [mol.m-3]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Positive electrode OCP [V]",
    "Negative electrode OCP [V]",
    "Electrolyte diffusivity [m2.s-1]",
    "Electrolyte conductivity [S.m-1]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Negative electrode exchange-current density [A.m-2]",
    "Positive electrode exchange-current density [A.m-2]",
    "SEI kinetic rate constant [m.s-1]",
]
for s in sets:
    print("=" * 30, s, "=" * 30)
    pv = pybamm.ParameterValues(s)
    for k in keys:
        try:
            v = pv[k]
            if callable(v):
                print(f"{k} = <function>")
            else:
                print(f"{k} = {v}")
        except Exception as e:
            print(f"{k} = MISSING ({type(e).__name__})")
    print()
