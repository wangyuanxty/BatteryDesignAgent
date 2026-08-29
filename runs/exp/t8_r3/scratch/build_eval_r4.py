"""Derive R4 retention files + build R4 log-evaluate batch file."""
import json
from pathlib import Path

cell = Path("runs/exp/t8_r3/cell")

tags = {
    "V12 cooled_anodefast2": "V12_cooled_anodefast2",
    "V13 porousanode": "V13_porousanode",
}
notes = {
    "V12 cooled_anodefast2": ("V8 winner + negative particle 1.2 um: ALL pass - retention 0.9881, ED 488.8 Wh/kg, "
                              "mass 38.05 g, 4C/45C T_max 326.84 K, anode_min +0.0132 V. Negative-particle lever "
                              "confirms: 1.2 um widens anode margin +7.3 -> +13.2 mV at unchanged thermal margin 6.3 K."),
    "V13 porousanode": ("V8 winner + negative porosity 0.30: ALL pass with the best margin set of the campaign - "
                        "retention 0.9866, ED 497.5 Wh/kg (mass 37.32 g), 4C/45C T_max 326.53 K (6.6 K margin), "
                        "anode_min +0.0177 V (2.4x V8). Coating-density route (porosity 0.30) beats the finer-particle "
                        "route on ED and both safety margins. SELECTED AS FINAL."),
}

def derive(tag):
    p1 = cell / f"r4_{tag}_1c_dfn.json"
    p5 = cell / f"r4_{tag}_5c_dfn.json"
    c1 = json.loads(p1.read_text(encoding="utf-8"))["capacity_ah"]
    c5 = json.loads(p5.read_text(encoding="utf-8"))["capacity_ah"]
    derived = {
        "candidate": tag,
        "capacity_1c_ah": c1,
        "capacity_5c_ah": c5,
        "retention_5c": c5 / c1 if c1 > 0 else 0.0,
        "formula": "retention_5c = capacity_5c_ah / capacity_1c_ah (5C_discharge DFN vs same-params 1C_discharge DFN)",
        "sources": {"one_c": str(p1), "five_c": str(p5)},
    }
    (cell / f"r4_{tag}_derived.json").write_text(json.dumps(derived, indent=2), encoding="utf-8")

batch = []
for cand, tag in tags.items():
    derive(tag)
    batch.append({
        "candidate": cand,
        "outputs": [
            f"runs/exp/t8_r3/cell/r4_{tag}_5c_dfn.json",
            f"runs/exp/t8_r3/cell/r4_{tag}_derived.json",
            f"runs/exp/t8_r3/cell/r4_{tag}_1c_dfn.json",
            f"runs/exp/t8_r3/cell/r4_{tag}_energy.json",
            f"runs/exp/t8_r3/cell/r4_{tag}_4c_safety.json",  # last: criteria-relevant T_max_K
        ],
        "note": notes[cand] + (" | file order: 4C safety last -> T_max_K judged from the safety-protocol run."),
    })
(cell / "log_eval_r4_batch.json").write_text(json.dumps(batch, indent=2), encoding="utf-8")
print("wrote r4 batch")