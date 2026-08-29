# -*- coding: utf-8 -*-
"""Derive R3 retention files + write r3 batch evaluate file."""
import json
from pathlib import Path

cell = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t8_r2\cell")

for v in ["VE", "VF", "VG"]:
    d1 = json.load(open(cell / ("r3_" + v + "_1c_dfn.json"), encoding="utf-8"))
    d5 = json.load(open(cell / ("r3_" + v + "_5c_dfn.json"), encoding="utf-8"))
    c1, c5 = d1["capacity_ah"], d5["capacity_ah"]
    rec = {
        "retention_5c": c5 / c1,
        "capacity_ah_1c": c1,
        "capacity_ah_5c": c5,
        "note": "retention_5c = capacity_ah_5c / capacity_ah_1c (same-parameter DFN runs; mechanical division)",
    }
    (cell / ("r3_" + v + "_retention.json")).write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(v, "retention =", round(rec["retention_5c"], 4))

batch = []
for v in ["VE", "VF", "VG"]:
    batch.append({
        "candidate": "V_" + v,
        "round": 3,
        "outputs": [
            "cell/r3_" + v + "_1c_dfn.json",
            "cell/r3_" + v + "_5c_dfn.json",
            "cell/r3_" + v + "_energy.json",
            "cell/r3_" + v + "_retention.json",
            "cell/r3_" + v + "_safety.json",
        ],
        "note": "R3: both levers (particle radius shrink 5.22/5.86->3.0/3.5 um, area-preserving loading cuts; V_G adds t+ 0.40 / D 4.2e-10 margin). Full suite incl. 4C-charge 45C thermal+plating exam. anode_potential_v min > 0 => no plating by mechanical derivation.",
    })

(cell / "r3_batch.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
print("r3_batch.json written with", len(batch), "candidates")