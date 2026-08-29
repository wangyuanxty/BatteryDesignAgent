# -*- coding: utf-8 -*-
"""Mechanically derive retention_5c = cap(5C dfn)/cap(1C dfn, same params) -> derived JSON for log-evaluate."""
import json
import sys

ROOT = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t8_r2"

jobs = [
    ("r1_base_1c_dfn.json", "r1_base_5c_dfn.json", "r1_base_retention.json"),
]

for fn1c, fn5c, out in jobs:
    d1 = json.load(open(ROOT + r"\cell\\" + fn1c, encoding="utf-8"))
    d5 = json.load(open(ROOT + r"\cell\\" + fn5c, encoding="utf-8"))
    c1 = d1["capacity_ah"]
    c5 = d5["capacity_ah"]
    ret = c5 / c1
    rec = {
        "retention_5c": ret,
        "capacity_ah_1c": c1,
        "capacity_ah_5c": c5,
        "note": "retention_5c = capacity_ah_5c / capacity_ah_1c (same-parameter DFN runs; mechanical division)",
    }
    with open(ROOT + r"\cell\\" + out, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    print(f"{out}: retention_5c = {ret:.4f} (5C {c5:.3f} Ah / 1C {c1:.3f} Ah)")

# also inspect safety file
d = json.load(open(ROOT + r"\cell\r1_base_safety.json", encoding="utf-8"))
print("safety:", {k: d[k] for k in d if k in ("model_used", "capacity_ah", "T_max_K")})
ap = d["anode_potential_v"]
print(f"anode_potential_v min = {min(ap):.4f} V -> plated={min(ap) < 0}")
print(f"anode_potential_v t=0/end = {ap[0]:.4f} / {ap[-1]:.4f}")