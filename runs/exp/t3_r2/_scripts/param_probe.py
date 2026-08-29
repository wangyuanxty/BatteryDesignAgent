"""Case t3_r2 anchor verification: dump key Chen2020 parameter values (read-only probe)."""
import json

import pybamm

pv = pybamm.ParameterValues("Chen2020")
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
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Positive electrode conductivity [S.m-1]",
    "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]",
    "Negative electrode diffusivity [m2.s-1]",
    "SEI kinetic rate constant [m.s-1]",
    "Initial inner SEI thickness [m]",
    "Initial outer SEI thickness [m]",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Ambient temperature [K]",
]
for k in keys:
    try:
        v = pv[k]
        print(json.dumps([k, v if isinstance(v, (int, float)) else str(v)], ensure_ascii=False))
    except KeyError:
        print(json.dumps([k, "MISSING"], ensure_ascii=False))
# stoichiometry probe: initial lithiation fraction of cathode
try:
    c0 = float(pv["Initial concentration in positive electrode [mol.m-3]"])
    cmax = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
    print(json.dumps(["cathode_initial_lithiation_fraction", round(c0 / cmax, 4)], ensure_ascii=False))
except KeyError:
    pass
try:
    c0n = float(pv["Initial concentration in negative electrode [mol.m-3]"])
    cmaxn = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
    print(json.dumps(["anode_initial_lithiation_fraction", round(c0n / cmaxn, 4)], ensure_ascii=False))
except KeyError:
    pass