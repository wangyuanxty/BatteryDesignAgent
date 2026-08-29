"""Derive R3 retention files + build R3 log-evaluate batch file (correct file order)."""
import json
from pathlib import Path

cell = Path("runs/exp/t8_r3/cell")

tags = {
    "V8 cooled_anodefast": "V8_cooled_anodefast",
    "V9 cooled_thickneg": "V9_cooled_thickneg",
    "V10 midcool_anodefast": "V10_midcool_anodefast",
    "V11 cooled_bigmargin": "V11_cooled_bigmargin",
}
notes = {
    "V8 cooled_anodefast": ("h=60 W/m2K + negative particle 1.5 um on V4 base: ALL criteria pass - retention 0.9862, "
                            "ED 487.8 Wh/kg, mass 38.05 g, 4C/45C T_max 327.27 K (<333.15), anode_min +0.0073 V no plating. "
                            "Margins: thermal 5.9 K, anode 7.3 mV (thin). Negative-particle downsizing restored the anode "
                            "kinetic margin at the cooled operating point (V7 -> V8: -10.2 mV -> +7.3 mV)."),
    "V9 cooled_thickneg": ("h=60 + negative electrode 100 um (N/P up ~17%) at neg particle 2.5 um: ED jumps to 532.9 Wh/kg "
                           "and retention 0.9746 fine, T_max 329.12 K pass, but anode_min -0.0265 V -> plated FAIL. "
                           "Capacity-margin route alone does not hold the anode positive at the cold end; "
                           "electrolyte polarization through the thicker negative dominates."),
    "V10 midcool_anodefast": ("h=40 + negative particle 1.5 um: ALL criteria pass - retention 0.9869, ED 487.9 Wh/kg, "
                              "mass 38.05 g, 4C/45C T_max 331.09 K (<333.15, thin 2.1 K margin), anode_min +0.0107 V "
                              "no plating (best anode margin of the round). Trade-off curve mapped: h=40 warms the cell "
                              "enough to widen anode margin but thermal margin compresses."),
    "V11 cooled_bigmargin": ("h=60 + negative 1.5 um + negative 100 um: best ED 536.5 Wh/kg, retention 0.9826, "
                             "T_max 328.02 K pass, but anode_min -0.0108 V -> plated FAIL. Thick-negative polarization "
                             "again overrides the particle-size gain (V8 +7.3 mV -> V11 -10.8 mV at same h=60). "
                             "Anode thickness is a plating liability at 4C/45C in this system, not an asset."),
}

def derive(tag):
    p1 = cell / f"r3_{tag}_1c_dfn.json"
    p5 = cell / f"r3_{tag}_5c_dfn.json"
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
    (cell / f"r3_{tag}_derived.json").write_text(json.dumps(derived, indent=2), encoding="utf-8")

batch = []
for cand, tag in tags.items():
    derive(tag)
    batch.append({
        "candidate": cand,
        "outputs": [
            f"runs/exp/t8_r3/cell/r3_{tag}_5c_dfn.json",
            f"runs/exp/t8_r3/cell/r3_{tag}_derived.json",
            f"runs/exp/t8_r3/cell/r3_{tag}_1c_dfn.json",
            f"runs/exp/t8_r3/cell/r3_{tag}_energy.json",
            f"runs/exp/t8_r3/cell/r3_{tag}_4c_safety.json",  # last: criteria-relevant T_max_K (last-wins extractor)
        ],
        "note": notes[cand] + (" | file order: 4C safety last so T_max_K is judged from the safety-protocol run; "
                              "capacity_ah scalar therefore shows the 4C protocol capacity."),
    })
(cell / "log_eval_r3_batch.json").write_text(json.dumps(batch, indent=2), encoding="utf-8")
print("wrote r3 batch")