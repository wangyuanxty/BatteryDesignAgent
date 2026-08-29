"""Mechanical retention derivation: lowT_retention = lowT_discharge.capacity_ah / 1C_discharge.capacity_ah.

Usage: derive.py <lowT_file> <rt_file> <out_file> [label]
Writes {lowT_retention, lowT_capacity_ah, rt_capacity_ah, lowT_source, rt_source, label}.
"""
import json
import sys

lowt_f, rt_f, out_f = sys.argv[1], sys.argv[2], sys.argv[3]
label = sys.argv[4] if len(sys.argv) > 4 else ""
lowt = json.load(open(lowt_f, encoding="utf-8"))
rt = json.load(open(rt_f, encoding="utf-8"))
cap_lowt = float(lowt["capacity_ah"])
cap_rt = float(rt["capacity_ah"])
out = {
    "lowT_retention": cap_lowt / cap_rt,
    "lowT_capacity_ah": cap_lowt,
    "rt_capacity_ah": cap_rt,
    "lowT_source": lowt_f,
    "rt_source": rt_f,
    "label": label,
}
json.dump(out, open(out_f, "w", encoding="utf-8"), indent=2)
print(json.dumps(out, indent=1))
