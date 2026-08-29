"""Derive retention_5c = capacity_5c / capacity_1c from DFN output files (mechanical).

Usage: python derive_retention.py <1c_json> <5c_json> <out_json>
Writes {candidate, capacity_1c_ah, capacity_5c_ah, retention_5c, formula}.
"""
import json
import sys

one_c = json.load(open(sys.argv[1], encoding="utf-8"))
five_c = json.load(open(sys.argv[2], encoding="utf-8"))
out = sys.argv[3]

cap1 = float(one_c["capacity_ah"])
cap5 = float(five_c["capacity_ah"])
ret = cap5 / cap1 if cap1 > 0 else 0.0

derived = {
    "candidate": out.split("\\")[-1].split("/")[-1].split("_derived")[0].replace("r1_", ""),
    "capacity_1c_ah": cap1,
    "capacity_5c_ah": cap5,
    "retention_5c": ret,
    "formula": "retention_5c = capacity_5c_ah / capacity_1c_ah (5C_discharge DFN vs same-params 1C_discharge DFN)",
    "sources": {"one_c": sys.argv[1], "five_c": sys.argv[2]},
}
with open(out, "w", encoding="utf-8") as f:
    json.dump(derived, f, indent=2)
print(f"{derived['candidate']}: 1C={cap1:.4f} Ah, 5C={cap5:.4f} Ah, retention_5c={ret:.4f}", flush=True)