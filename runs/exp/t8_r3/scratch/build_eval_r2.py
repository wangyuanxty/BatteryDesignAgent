"""Derive R2 retention files + build R2 log-evaluate batch file."""
import json
from pathlib import Path

cell = Path("runs/exp/t8_r3/cell")

notes = {
    "V4": ("V4 ratemax", "positive particle 1.5 um + negative 2.5 um + high-transport electrolyte on V1 mass base: 5C retention jumps 8.7% -> 98.0% (diagnosis hit: cathode surface saturation cured), ED 485.3 Wh/kg, mass 38.05 g pass; 4C/45C T_max 352.5 K > 333.15 K fails thermal; anode_min +0.0126 V no plating (thin margin)."),
    "V5": ("V5 thickcathode", "V4 + pos 90 um: retention 98.0% confirmed; ED 454.1 pass, mass 39.4 g pass; T_max 354.0 K fails; anode +0.0149 V no plating."),
    "V6": ("V6 thickboth", "V4 + both electrodes scaled: best ED so far (500.9 Wh/kg) with retention 98.1% and mass 39.5 g; T_max 356.4 K fails; anode +0.0027 V very thin positive margin."),
    "V7": ("V7 ratemax+cooling", "V4 + h=60 W/m2K: T_max 328.5 K passes thermal; but colder cell slows kinetics -> anode_min -0.0102 V -> plated=true fails; retention 97.7%, ED 484.4, mass pass. Thermal-plating trade-off exposed: need anode margin at low T."),
}

def derive(name):
    p1 = cell / f"r2_{name}_1c_dfn.json"
    p5 = cell / f"r2_{name}_5c_dfn.json"
    c1 = json.loads(p1.read_text(encoding="utf-8"))["capacity_ah"]
    c5 = json.loads(p5.read_text(encoding="utf-8"))["capacity_ah"]
    derived = {
        "candidate": name,
        "capacity_1c_ah": c1,
        "capacity_5c_ah": c5,
        "retention_5c": c5 / c1 if c1 > 0 else 0.0,
        "formula": "retention_5c = capacity_5c_ah / capacity_1c_ah (5C_discharge DFN vs same-params 1C_discharge DFN)",
        "sources": {"one_c": str(p1), "five_c": str(p5)},
    }
    (cell / f"r2_{name}_derived.json").write_text(json.dumps(derived, indent=2), encoding="utf-8")

for name in ["V4", "V5", "V6", "V7"]:
    derive(name)

batch = []
for name, (cand, note) in notes.items():
    batch.append({
        "candidate": cand,
        "outputs": [
            f"runs/exp/t8_r3/cell/r2_{name}_5c_dfn.json",
            f"runs/exp/t8_r3/cell/r2_{name}_derived.json",
            f"runs/exp/t8_r3/cell/r2_{name}_4c_safety.json",
            f"runs/exp/t8_r3/cell/r2_{name}_1c_dfn.json",
            f"runs/exp/t8_r3/cell/r2_{name}_energy.json",
        ],
        "note": note,
    })
(cell / "log_eval_r2_batch.json").write_text(json.dumps(batch, indent=2), encoding="utf-8")
print("wrote r2 batch")