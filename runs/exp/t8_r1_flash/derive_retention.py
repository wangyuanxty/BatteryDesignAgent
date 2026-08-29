"""Mechanically derive 5C capacity retention from run-pyamm outputs.

retention = capacity_ah(5C) / capacity_ah(1C), same parameter set.
Writes {"capacity_retention_5c": r, "capacity_ah_1c": a, "capacity_ah_5c": b}.
"""
import json
import sys

f1c, f5c, out = sys.argv[1], sys.argv[2], sys.argv[3]
c1c = json.load(open(f1c, encoding="utf-8"))["capacity_ah"]
c5c = json.load(open(f5c, encoding="utf-8"))["capacity_ah"]
ret = c5c / c1c
json.dump(
    {"capacity_retention_5c": ret, "capacity_ah_1c": c1c, "capacity_ah_5c": c5c},
    open(out, "w", encoding="utf-8"),
    ensure_ascii=False,
)
print(f"1C={c1c:.4f} Ah  5C={c5c:.4f} Ah  retention={ret:.4f}")
