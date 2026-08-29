"""Dump Chen2020 parameter values needed for design_spec / bom / calc."""
import pybamm

pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Lower voltage cut-off [V]", "Upper voltage cut-off [V]", "Nominal cell capacity [A.h]",
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]", "Separator thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]", "Separator density [kg.m-3]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode conductive additive volume fraction",
    "Positive electrode binder volume fraction",
    "Negative electrode conductive additive volume fraction",
    "Negative electrode binder volume fraction",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Initial concentration in electrolyte [mol.m-3]",
    "Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]", "Cation transference number",
    "SEI kinetic rate constant [m.s-1]", "Initial inner SEI thickness [m]",
    "SEI reaction exchange current density [A.m-2]", "Inner SEI reaction proportion",
    "Outer SEI solvent diffusivity [m2.s-1]", "SEI open-circuit potential [V]",
    "Total heat transfer coefficient [W.m-2.K-1]", "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]", "Negative electrode diffusivity [m2.s-1]",
]
for k in keys:
    try:
        v = pv[k]
        print(f"{k} = {v}")
    except KeyError:
        print(f"{k} = <NOT IN SET>")
