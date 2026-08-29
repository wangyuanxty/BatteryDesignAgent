# -*- coding: utf-8 -*-
"""Summarize R3 sim outputs (scratch)."""
import json
import os

d = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t8_r2\cell"
print("variant: 1C_Ah 5C_Ah retention ED_Wh/kg mass_g T_max_K plated anode_min_V")
for v in ["VE", "VF", "VG"]:
    try:
        c5 = json.load(open(d + "\\r3_" + v + "_5c_dfn.json", encoding="utf-8"))
        c1 = json.load(open(d + "\\r3_" + v + "_1c_dfn.json", encoding="utf-8"))
        en = json.load(open(d + "\\r3_" + v + "_energy.json", encoding="utf-8"))
    except OSError as e:
        print(v, "missing:", e)
        continue
    cap1, cap5 = c1["capacity_ah"], c5["capacity_ah"]
    ret = cap5 / cap1
    saf = None
    sp = d + "\\r3_" + v + "_safety.json"
    tmax = plated = anode_min = float("nan")
    if os.path.exists(sp):
        saf = json.load(open(sp, encoding="utf-8"))
        tmax = saf.get("t_max_k", saf.get("T_max_K", float("nan")))
        plated = saf.get("plated", "n/a")
        anode_min = saf.get("anode_potential_min_v", saf.get("anode_potential_v_min", float("nan")))
    print("%s: %.4f %.4f %.4f %.1f %.2f %s %s %s" % (
        v, cap1, cap5, ret, en["energy_density_wh_kg"], 1000 * en["mass_kg"],
        tmax if isinstance(tmax, (int, float)) else tmax, plated, anode_min))
    if saf:
        print("   safety keys:", sorted(saf.keys()))