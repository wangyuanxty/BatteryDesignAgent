"""Derive sei_thickness_nm_500cyc from an aging(--cycles 500) output alone (aging-only candidates).

Entry-0 meta formula: sei_thickness_nm_500cyc = mechanical copy (rename) of
sei_thickness_nm_end from aging_1C_100cyc --cycles 500 output.
Usage: python _derive_sei500.py <aging500_file> <sei500_out> [label]
"""
import json
import sys

def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

aging500, out_sei = sys.argv[1:3]
label = sys.argv[3] if len(sys.argv) > 3 else "r"

sei500 = float(load(aging500)["sei_thickness_nm_end"])
entry = {
    "sei_thickness_nm_500cyc": round(sei500, 4),
    "formula": "mechanical copy (rename) of sei_thickness_nm_end from aging_1C_100cyc --cycles 500",
    "source": aging500.replace("\\", "/").split("/")[-1],
}
with open(out_sei, "w", encoding="utf-8") as f:
    json.dump(entry, f, indent=2)
print(f"[{label}] sei_thickness_nm_500cyc = {sei500:.2f}")
