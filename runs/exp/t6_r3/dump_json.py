"""Dump all scalar keys of V27 final candidate outputs for deliverable generation."""
import json
import sys

files = {
    "1c": "runs/exp/t6_r3/cell/r10_V27_combo_1c.json",
    "energy": "runs/exp/t6_r3/cell/r10_V27_combo_energy.json",
    "4c": "runs/exp/t6_r3/cell/r10_V27_combo_4c.json",
    "aging": "runs/exp/t6_r3/cell/r10_V27_combo_aging.json",
}
for tag, path in files.items():
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        print(f"== {tag}: MISSING")
        continue
    print(f"== {tag}")
    for k, v in d.items():
        if isinstance(v, (int, float, str, bool)):
            print(f"  {k} = {v!r}")
        elif isinstance(v, list):
            print(f"  {k} = list[{len(v)}] first={v[0]!r} last={v[-1]!r}")
    print()
