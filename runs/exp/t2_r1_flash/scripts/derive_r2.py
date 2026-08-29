"""Mechanically derive round-2 metrics from tool outputs (formula documented in each file's note)."""
import json
from pathlib import Path

CELL = Path(__file__).resolve().parent.parent / "cell"


def load(name):
    return json.loads((CELL / name).read_text(encoding="utf-8"))


# FC-A
fca_lowt, fca_1c, fca_ag500 = load("r2_fca_lowt.json"), load("r2_fca_1c_dfn.json"), load("r2_fca_aging500.json")
fca_derived = {
    "sei_500cyc_nm": fca_ag500["sei_thickness_nm_end"],
    "lowT_retention": round(fca_lowt["capacity_ah"] / fca_1c["capacity_ah"], 6),
    "note": "sei_500cyc_nm = r2_fca_aging500.json:sei_thickness_nm_end; lowT_retention = r2_fca_lowt.json:capacity_ah / r2_fca_1c_dfn.json:capacity_ah",
}
(CELL / "r2_fca_derived.json").write_text(json.dumps(fca_derived, ensure_ascii=False, indent=2), encoding="utf-8")

# SEI-a / SEI-b (500-cycle scans on FC-B basis)
seia = load("r2_seia_aging500.json")
seib = load("r2_seib_aging500.json")
for name, j in (("r2_seia_derived", seia), ("r2_seib_derived", seib)):
    out = {"sei_500cyc_nm": j["sei_thickness_nm_end"],
           "note": f"sei_500cyc_nm = {name}_aging500.json:sei_thickness_nm_end (500-cycle scan)"}
    (CELL / f"{name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

# FC-C
fcc_lowt, fcc_1c, fcc_ag500 = load("r2_fcc_lowt.json"), load("r2_fcc_1c_dfn.json"), load("r2_fcc_aging500.json")
fcc_derived = {
    "sei_500cyc_nm": fcc_ag500["sei_thickness_nm_end"],
    "lowT_retention": round(fcc_lowt["capacity_ah"] / fcc_1c["capacity_ah"], 6),
    "note": "sei_500cyc_nm = r2_fcc_aging500.json:sei_thickness_nm_end; lowT_retention = r2_fcc_lowt.json:capacity_ah / r2_fcc_1c_dfn.json:capacity_ah",
}
(CELL / "r2_fcc_derived.json").write_text(json.dumps(fcc_derived, ensure_ascii=False, indent=2), encoding="utf-8")

print("FC-A:  sei_500cyc_nm =", fca_derived["sei_500cyc_nm"], " lowT_retention =", fca_derived["lowT_retention"])
print("SEI-a: sei_500cyc_nm =", seia["sei_thickness_nm_end"])
print("SEI-b: sei_500cyc_nm =", seib["sei_thickness_nm_end"])
print("FC-C:  sei_500cyc_nm =", fcc_derived["sei_500cyc_nm"], " lowT_retention =", fcc_derived["lowT_retention"])
