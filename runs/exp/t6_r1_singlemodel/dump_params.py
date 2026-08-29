"""Dump design-relevant parameter values for Chen2020 base and LNMO-overridden set."""
import json
from pathlib import Path

import pybamm

KEYS = [
    "Nominal cell capacity [A.h]",
    "Upper voltage cut-off [V]",
    "Lower voltage cut-off [V]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Separator porosity",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode maximum concentration [mol.m-3]",
    "Negative electrode maximum concentration [mol.m-3]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Positive electrode molar mass [kg.mol-1]",
    "Negative electrode molar mass [kg.mol-1]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode conductivity [S.m-1]",
    "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]",
    "Negative electrode diffusivity [m2.s-1]",
    "Positive electrode reaction rate constant [m.s-1]",
    "Negative electrode reaction rate constant [m.s-1]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "SEI kinetic rate constant [m.s-1]",
    "SEI reaction exchange current density [A.m-2]",
    "Initial inner SEI thickness [m]",
    "Initial outer SEI thickness [m]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Positive current collector specific heat capacity [J.kg-1.K-1]",
    "Negative current collector specific heat capacity [J.kg-1.K-1]",
    "Ambient temperature [K]",
]


def build_set(base: str):
    if base.endswith(".json"):
        from bda.simulators.lnmo_parameters import lnmo_ocp
        extra = json.loads(Path(base).read_text(encoding="utf-8"))
        for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
            if isinstance(extra.get(key), str):
                extra[key] = lnmo_ocp
        pv = pybamm.ParameterValues("Chen2020")
        pv.update(extra, check_already_exists=False)
    else:
        pv = pybamm.ParameterValues(base)
    return pv


for base in ["Chen2020", r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"]:
    pv = build_set(base)
    print("=" * 90)
    print("BASE:", base)
    for k in KEYS:
        try:
            v = pv[k]
            if callable(v):
                v = "<function>"
            print(f"  {k} = {v}")
        except KeyError:
            print(f"  {k} = <MISSING>")
