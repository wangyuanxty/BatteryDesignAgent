"""Correct V9/V11 params: width mass-fit so calc-energy stack mass <= 40 g."""
import json
from pathlib import Path
import sys

sys.path.insert(0, r".claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

cell = Path("runs/exp/t8_r3/cell")
for name in ["V9_cooled_thickneg", "V11_cooled_bigmargin"]:
    p = cell / f"params_r3_{name}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["Electrode width [m]"] = 1.504  # mass-fit: expected calc-energy stack ~39.78 g (was 40.11 g at W=1.51)
    p.write_text(json.dumps(d, indent=2), encoding="utf-8")
    print("corrected", p.name)

ws = CaseWorkspace("exp/t8_r3", root="runs", create=False)
append_entry(ws, {
    "action": "note",
    "round": 3,
    "subject": "V9/V11 width mass-fit correction",
    "detail": (
        "Propose-round-3 entry was appended before the in-script stack-mass pre-check printed; the pre-check "
        "(same layer formula as calc-energy: active layers and separator with porosity factor, collectors "
        "without, electrolyte excluded) gave V9/V11 40.11 g at nominal width 1.51 m > 40 g cap. Correction: "
        "Electrode width [m] = 1.504 for V9 and V11 (mass-fit arithmetic, same lever as rounds 1-2), expected "
        "calc-energy mass ~39.78 g. All other fields of the round-3 propose entry unchanged. Params files "
        "cell/params_r3_V9_v*.json / V11 are the corrected executable artifacts."
    ),
})
print("correction note appended")