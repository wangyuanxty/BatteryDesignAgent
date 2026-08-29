import json
from pathlib import Path

CELL = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_flash\cell")

# (derived_name, 1c_file, 5c_file, note) — retention_5c = cap5c/cap1c mechanically
items = [
    ("r0_base_derived.json", "r0_base_1c_dfn.json", "r0_base_5c_dfn.json",
     "baseline; retention from DFN 5C / DFN 1C"),
    ("r1_v1_derived.json", "r1_v1_1c_dfn.json", "r1_v1_5c_dfn.json",
     "V1; retention from DFN 5C / DFN 1C"),
    ("r1_v2_derived.json", "r1_v2_1c_dfn.json", "r1_v2_5c_dfn.json",
     "V2; retention from DFN 5C / DFN 1C"),
    ("r1_v3_derived.json", "r1_v3_1c_dfn.json", "r1_v3_5c_dfn.json",
     "V3; WARNING 5C model_used=SPMe(fallback) (DFN solver failed, auto-degraded); SPMe severely underestimates at 5C, retention not judgment-grade"),
]
for name, f1, f5, note in items:
    a = json.loads((CELL / f1).read_text(encoding="utf-8"))
    b = json.loads((CELL / f5).read_text(encoding="utf-8"))
    ret = b["capacity_ah"] / a["capacity_ah"]
    out = {
        "retention_5c": ret,
        "capacity_ah_1c": a["capacity_ah"],
        "capacity_ah_5c": b["capacity_ah"],
        "note": note + f"; retention = {b['capacity_ah']:.4f}/{a['capacity_ah']:.4f} = {ret:.4f}",
    }
    (CELL / name).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(name, "->", json.dumps(out))
