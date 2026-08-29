# -*- coding: utf-8 -*-
"""Probe Chen2020 keys needed for deliverables (scratch)."""
import json

import pybamm

pv = pybamm.ParameterValues("Chen2020")
ov = json.load(open(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t8_r2\cell\params_r3_VG.json", encoding="utf-8"))
pv.update(ov)
keys = [
    "Nominal cell capacity [A.h]", "Lower voltage cut-off [V]", "Upper voltage cut-off [V]",
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]", "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Typical electrolyte concentration [mol.m-3]", "Reference temperature [K]",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]", "Negative electrode diffusivity [m2.s-1]",
    "Initial concentration in electrolyte [mol.m-3]",
]
for k in keys:
    try:
        v = pv[k]
        if isinstance(v, (int, float)):
            print("%s = %s" % (k, v))
        else:
            print("%s = %s" % (k, str(v)[:60]))
    except Exception as e:
        print("%s -> MISSING (%s)" % (k, type(e).__name__))