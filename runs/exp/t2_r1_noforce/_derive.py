"""Mechanical derivation of criteria metrics from tool outputs (entry-0 meta formulas).

- lowT_retention_pct = 100 x capacity_ah(lowT_discharge) / capacity_ah(1C_discharge, same design params)
- sei_thickness_nm_500cyc = mechanical copy of aging(--cycles 500) output key sei_thickness_nm_end
  (renamed with cycle-count suffix so 100-cyc and 500-cyc contracts use distinct criteria keys)

Usage: python _derive.py <lowT_file> <ref_1C_file> <aging500_file> <retention_out> <sei500_out> [label]
"""
import json
import sys

def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

lowt, ref, aging500, out_ret, out_sei = sys.argv[1:6]
label = sys.argv[6] if len(sys.argv) > 6 else "r"

d_lowt, d_ref, d_a500 = load(lowt), load(ref), load(aging500)
cap_lowt = float(d_lowt["capacity_ah"])
cap_ref = float(d_ref["capacity_ah"])
ret_pct = 100.0 * cap_lowt / cap_ref
sei500 = float(d_a500["sei_thickness_nm_end"])

ret_entry = {
    "lowT_retention_pct": round(ret_pct, 4),
    "formula": "100 * capacity_ah(lowT_discharge, 253.15K ambient, Initial temperature 253.15K) / capacity_ah(1C_discharge, 298.15K)",
    "cap_lowT_ah": cap_lowt,
    "cap_25C_ah": cap_ref,
    "sources": [lowt.split("/")[-1], ref.split("/")[-1]],
}
sei_entry = {
    "sei_thickness_nm_500cyc": round(sei500, 4),
    "formula": "mechanical copy (rename) of sei_thickness_nm_end from aging_1C_100cyc --cycles 500",
    "source": aging500.split("/")[-1],
}
with open(out_ret, "w", encoding="utf-8") as f:
    json.dump(ret_entry, f, indent=2)
with open(out_sei, "w", encoding="utf-8") as f:
    json.dump(sei_entry, f, indent=2)
print(f"[{label}] lowT_retention_pct = {ret_pct:.2f} (cap_lowT={cap_lowt:.4f}, cap_25C={cap_ref:.4f})")
print(f"[{label}] sei_thickness_nm_500cyc = {sei500:.2f}")
