"""Mechanically derive R1 metrics from tool outputs (formula documented in each file's note)."""
import json
from pathlib import Path

CELL = Path(__file__).resolve().parent.parent / "cell"

lowt = json.loads((CELL / "r1_base_lowt.json").read_text(encoding="utf-8"))
onec = json.loads((CELL / "r1_base_1c_dfn.json").read_text(encoding="utf-8"))
aging500 = json.loads((CELL / "r1_base_aging500.json").read_text(encoding="utf-8"))

retention = lowt["capacity_ah"] / onec["capacity_ah"]
derived_lowt = {
    "lowT_retention": round(retention, 6),
    "note": "lowT_retention = r1_base_lowt.json:capacity_ah / r1_base_1c_dfn.json:capacity_ah (mechanical derivation, formula documented)",
    "capacity_ah_lowT": lowt["capacity_ah"],
    "capacity_ah_25C": onec["capacity_ah"],
}
(CELL / "r1_derived_lowt.json").write_text(json.dumps(derived_lowt, ensure_ascii=False, indent=2), encoding="utf-8")

derived_sei500 = {
    "sei_500cyc_nm": aging500["sei_thickness_nm_end"],
    "note": "sei_500cyc_nm = r1_base_aging500.json:sei_thickness_nm_end (500-cycle run, key renamed for criteria layer)",
}
(CELL / "r1_derived_sei500.json").write_text(json.dumps(derived_sei500, ensure_ascii=False, indent=2), encoding="utf-8")

print("lowT_retention =", retention)
print("sei_500cyc_nm =", aging500["sei_thickness_nm_end"])
