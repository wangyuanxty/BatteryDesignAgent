# -*- coding: utf-8 -*-
"""Summarize R2 sim outputs (scratch)."""
import json
import os

d = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t8_r2\cell"
for v in ["VA", "VB", "VC", "VD"]:
    try:
        c5 = json.load(open(d + "\\r2_" + v + "_5c_dfn.json", encoding="utf-8"))
    except OSError:
        print(v, "5C missing")
        continue
    cap5 = c5["capacity_ah"]
    c1 = json.load(open(d + "\\r2_" + v + "_1c_dfn.json", encoding="utf-8"))["capacity_ah"]
    ret = cap5 / c1
    enp = d + "\\r2_" + v + "_energy.json"
    if os.path.exists(enp):
        en = json.load(open(enp, encoding="utf-8"))
        print("%s: 1C=%.3fAh 5C=%.3fAh retention=%.3f ED=%.1f Wh/kg mass=%.1f g" % (
            v, c1, cap5, ret, en["energy_density_wh_kg"], 1000 * en["mass_kg"]))
    else:
        print("%s: 1C=%.3fAh 5C=%.3fAh retention=%.3f (energy pending)" % (v, c1, cap5, ret))