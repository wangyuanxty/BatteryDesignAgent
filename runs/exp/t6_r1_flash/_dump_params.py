"""Scratch: dump key parameter values from Chen2020 base + LNMO overlay (what the runner actually uses)."""
import json
import pybamm
from pathlib import Path
from bda.simulators.lnmo_parameters import lnmo_ocp

extra = json.loads(Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json").read_text(encoding="utf-8"))
for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
    if isinstance(extra.get(key), str):
        extra[key] = lnmo_ocp
pv = pybamm.ParameterValues("Chen2020")
pv.update(extra, check_already_exists=False)

keys = [
    "Nominal cell capacity [A.h]",
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Positive electrode maximum concentration [mol.m-3]",
    "Negative electrode maximum concentration [mol.m-3]",
    "Positive electrode stoichiometry limits for reaction [0.0, 1.0]",
    "Negative electrode stoichiometry limits for reaction [0.0, 1.0]",
    "Cation transference number",
    "Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]",
    "SEI kinetic rate constant [m.s-1]",
    "SEI reaction exchange current density [A.m-2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]", "Cell volume [m3]",
    "Initial SEI thickness [m]",
    "Negative electrode reaction rate constant [m.s-1]",
    "Positive electrode reaction rate constant [m.s-1]",
    "Negative particle diffusivity [m2.s-1]", "Positive particle diffusivity [m2.s-1]",
    "Lower voltage cut-off [V]", "Upper voltage cut-off [V]",
]
for k in keys:
    try:
        v = pv[k]
        if callable(v):
            v = "<function>"
        print(f"{k} = {v}")
    except KeyError:
        print(f"{k} = MISSING")
