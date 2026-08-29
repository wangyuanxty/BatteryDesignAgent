"""Probe Chen2020 parameter-set keys needed for deliverables."""
import json
import pybamm

pv = pybamm.ParameterValues("Chen2020")
with open(r"runs/exp/t8_r3/cell/params_r4_V13_porousanode.json", encoding="utf-8") as f:
    ov = json.load(f)
pv.update(ov, check_already_exists=False)

keys = [
    "Nominal cell capacity [A.h]", "Lower voltage cut-off [V]", "Upper voltage cut-off [V]",
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Separator thickness [m]",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Ambient temperature [K]", "Cell cooling surface area [m2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
]
for k in keys:
    try:
        print(f"{k} = {pv[k]}")
    except KeyError:
        print(f"{k} = MISSING")
# any capacity-density style keys?
for k in sorted(pv.keys()):
    if "capacit" in k.lower():
        print("CAPKEY:", k, "=", pv[k])