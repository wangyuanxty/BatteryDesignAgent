"""Dump top-level key structure of the four V12 output files + a 1C DFN T-max check."""
import json

for name, path in [
    ("1c_dfn", "runs/exp/t3_r3/cell/r5_v12_1c_dfn.json"),
    ("5c_dfn", "runs/exp/t3_r3/cell/r5_v12_5c_dfn.json"),
    ("4c_dfn", "runs/exp/t3_r3/cell/r5_v12_4c_dfn.json"),
    ("derived", "runs/exp/t3_r3/cell/r5_v12_derived.json"),
]:
    d = json.load(open(path, encoding="utf-8"))
    print("==", name, "==")
    for k, v in d.items():
        if isinstance(v, list):
            print(f"  {k}: list[{len(v)}] first={v[0] if v else None} min={min(v) if v and isinstance(v[0], (int, float)) else 'n/a'}")
        elif isinstance(v, dict):
            print(f"  {k}: dict keys={list(v.keys())[:8]}")
        else:
            print(f"  {k}: {v}")