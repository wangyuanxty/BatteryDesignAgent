"""Mechanically derive bridge JSONs for criteria keys not present in raw outputs.

- sei_100cyc_nm / sei_500cyc_nm : verbatim copy of aging output sei_thickness_nm_end
  (the raw key carries two cycle-count contracts in the task; flat criteria needs one
  key per threshold).
- lowT_retention_pct : 100 x capacity_ah(lowT) / capacity_ah(1C same params).

Usage: python make_bridge.py <prefix> <aging100.json> <aging500.json> <lowT.json> <oneC.json> <outdir>
"""
import json
import sys

prefix, a100, a500, lowT, oneC, outdir = sys.argv[1:7]

def load(p):
    return json.load(open(p, encoding="utf-8-sig"))

d100 = load(a100)["sei_thickness_nm_end"]
d500 = load(a500)["sei_thickness_nm_end"]
c_lowT = load(lowT)["capacity_ah"]
c_1c = load(oneC)["capacity_ah"]
ret = 100.0 * c_lowT / c_1c

b100 = {
    "sei_100cyc_nm": d100,
    "source": "sei_thickness_nm_end (verbatim copy, nm)",
    "source_file": a100,
    "formula": "copy",
}
b500 = {
    "sei_500cyc_nm": d500,
    "source": "sei_thickness_nm_end (verbatim copy, nm)",
    "source_file": a500,
    "formula": "copy",
}
bret = {
    "lowT_retention_pct": ret,
    "capacity_ah_lowT_253K": c_lowT,
    "capacity_ah_25C_1C": c_1c,
    "formula": "100 x capacity_ah(lowT_discharge 253.15K) / capacity_ah(1C_discharge 298.15K), same params",
    "source_files": [lowT, oneC],
}
with open(f"{outdir}/{prefix}_sei100.json", "w", encoding="utf-8") as f:
    json.dump(b100, f, ensure_ascii=False, indent=2)
with open(f"{outdir}/{prefix}_sei500.json", "w", encoding="utf-8") as f:
    json.dump(b500, f, ensure_ascii=False, indent=2)
with open(f"{outdir}/{prefix}_lowT_ret.json", "w", encoding="utf-8") as f:
    json.dump(bret, f, ensure_ascii=False, indent=2)
print(f"{prefix}: sei100={d100:.3f} nm, sei500={d500:.3f} nm, lowT_ret={ret:.4f}% ({c_lowT:.5f}/{c_1c:.5f} Ah)")
