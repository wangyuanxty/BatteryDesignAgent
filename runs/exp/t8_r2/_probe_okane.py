# -*- coding: utf-8 -*-
"""Probe OKane2022 key parameters (escalation candidate) — scratch."""
import pybamm

pv = pybamm.ParameterValues("OKane2022")
keys = [
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]", "Separator thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]", "Separator density [kg.m-3]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Nominal cell capacity [A.h]",
    "Positive electrode active material volume fraction", "Negative electrode active material volume fraction",
    "Upper voltage cut-off [V]", "Lower voltage cut-off [V]",
    "Cation transference number", "Initial concentration in electrolyte [mol.m-3]",
    "Cell cooling surface area [m2]",
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
# particle radius naming
import re
for k in pv.keys():
    if "radius" in k.lower() and ("positive" in k.lower() or "negative" in k.lower()):
        print("RADIUS-KEY:", k, "=", pv[k])
for k in sorted(pv.keys()):
    if "silicon" in k.lower() or "siox" in k.lower():
        print("SIOX-KEY:", k, "=", pv[k])
    if "sei kinetic" in k.lower():
        print("SEI-KEY:", k, "=", pv[k])