"""Rebuild round-1 and round-2 log-evaluate batch files with corrected file order.

Extractor is last-wins over the file list (bda/audit.py extract_metrics); T_max_K must
therefore be judged from the LAST file carrying it. The criteria-relevant thermal state
is the 4C/45C safety protocol run -> 4c_safety.json goes LAST. Side effect (documented in
notes): the record's capacity_ah scalar becomes the safety-protocol capacity; the design
capacity_ah lives in the 1C/derived files which are listed earlier.
"""
import json
from pathlib import Path

cell = Path("runs/exp/t8_r3/cell")
CORR = ("(corrected re-evaluation, supersedes earlier same-round entry of this candidate: "
        "T_max_K is now sourced from the 4C/45C safety-protocol output file per the thermal "
        "criterion intent; the earlier entry accidentally judged T_max from the 1C file because "
        "the extractor is last-wins over the listed files. capacity_ah scalar in metrics is the "
        "4C-safety protocol capacity; design capacities are the *_1c_dfn/capacity_1c_ah interface. "
        "plated is derived from the most complete anode_potential_v time series.)")

def batch(order_names):
    out = []
    for cand, note, tag in order_names:
        out.append({
            "candidate": cand,
            "outputs": [
                f"runs/exp/t8_r3/cell/r{tag[0]}_{tag[1]}_5c_dfn.json",
                f"runs/exp/t8_r3/cell/r{tag[0]}_{tag[1]}_derived.json",
                f"runs/exp/t8_r3/cell/r{tag[0]}_{tag[1]}_1c_dfn.json",
                f"runs/exp/t8_r3/cell/r{tag[0]}_{tag[1]}_energy.json",
                f"runs/exp/t8_r3/cell/r{tag[0]}_{tag[1]}_4c_safety.json",
            ],
            "note": CORR + " " + note,
        })
    return out

r1_notes = {
    "C0 baseline": "baseline characterization (Chen2020 defaults): mass 43.45 g exceeds 40 g cap; ED 400.8 Wh/kg below 446.18; 5C retention 8.7%; 4C/45C T_max 354.3 K > 333.15 K and anode potential dips to -0.19 V (plated). All targets fail at baseline.",
    "V1 massfit": "thin collectors/separator fix mass (38.05 g) and ED (457.9 Wh/kg); 5C retention 9.1% (far below 0.9); 4C T_max 355.6 K and plated. Rate bottleneck diagnosed as positive-particle surface saturation (scratch/diag_physics.py).",
    "V2 activeboost": "thicker electrodes raise 1C energy (18.61 Wh, ED 466.7 Wh/kg, mass 39.87 g) but 5C retention drops to 8.4%: thicker electrodes worsen cathode-surface saturation at fixed current, matching diagnosis.",
    "V3 ratemargin": "negative-only particle downsize (5.86->4.0 um) moves retention 8.7->9.7%: negative side was not the 5C bottleneck (cathode is); positive particle size targeted next round.",
}
r2_notes = {
    "V4 ratemax": "positive particle 1.5 um + negative 2.5 um + high-transport electrolyte on V1 mass base: 5C retention jumps 8.7% -> 98.0% (diagnosis hit: cathode surface saturation cured), ED 485.3 Wh/kg, mass 38.05 g pass; 4C/45C T_max 352.5 K > 333.15 K fails thermal; anode_min +0.0126 V no plating (thin margin).",
    "V5 thickcathode": "V4 + pos 90 um: retention 98.0% confirmed; ED 454.1 pass, mass 39.4 g pass; T_max 354.0 K fails; anode +0.0149 V no plating.",
    "V6 thickboth": "V4 + both electrodes scaled: best ED so far (500.9 Wh/kg) with retention 98.1% and mass 39.5 g; T_max 356.4 K fails; anode +0.0027 V very thin positive margin.",
    "V7 ratemax+cooling": "V4 + h=60 W/m2K: T_max 328.5 K passes thermal; colder cell slows kinetics -> anode_min -0.0102 V -> plated=true fails; retention 97.7%, ED 484.4, mass 38.05 g pass. Thermal-plating trade-off exposed: anode margin must be rebuilt at low T.",
}

def tagmap(notes, rnd):
    tags = {}
    for full in notes:
        key = full.split(" ")[0]
        tags[full] = (rnd, key)
    return tags

t1 = tagmap(r1_notes, 1)
t2 = tagmap(r2_notes, 2)

b1 = batch([(n, r1_notes[n], t1[n]) for n in r1_notes])
b2 = batch([(n, r2_notes[n], t2[n]) for n in r2_notes])

(cell / "log_eval_r1_batch.json").write_text(json.dumps(b1, indent=2), encoding="utf-8")
(cell / "log_eval_r2_batch.json").write_text(json.dumps(b2, indent=2), encoding="utf-8")
print("wrote corrected r1/r2 batch files")