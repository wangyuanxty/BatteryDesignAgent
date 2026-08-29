import json
from pathlib import Path

CELL = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t3_r1_flash\cell")

items = [
    ("r2_v4_derived.json", "r2_v4_1c_dfn.json", "r2_v4_5c_dfn.json", "V4; retention from DFN 5C / DFN 1C"),
    ("r2_v5_derived.json", "r2_v5_1c_dfn.json", "r2_v5_5c_dfn.json", "V5; retention from DFN 5C / DFN 1C"),
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
