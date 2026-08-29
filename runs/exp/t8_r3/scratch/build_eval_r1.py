"""Derive retention files for round-1 candidates + build log-evaluate batch file."""
import json
from pathlib import Path

cell = Path("runs/exp/t8_r3/cell")

def derive(name, outname):
    p1 = cell / f"r1_{name}_1c_dfn.json"
    p5 = cell / f"r1_{name}_5c_dfn.json"
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
    out = cell / f"r1_{outname}_derived.json"
    out.write_text(json.dumps(derived, indent=2), encoding="utf-8")
    print(f"{name}: retention_5c={derived['retention_5c']:.4f}")

for name in ["C0", "V1", "V2", "V3"]:
    derive(name, name)

notes = {
    "C0 baseline": "baseline characterization (Chen2020 defaults): mass 43.45 g exceeds 40 g cap; ED 400.8 Wh/kg below 446.18; 5C retention 8.7%; 4C/45C T_max 354.3 K > 333.15 K and anode potential dips to -0.19 V (plated). All targets fail at baseline; anchors the design gap.",
    "V1 massfit": "thin collectors/separator fix mass (38.05 g <= 40 g) and ED (457.9 Wh/kg >= 446.18) -> stage2 mass/ED pass; 5C retention 9.1% (far below 0.9); 4C/45C T_max 355.6 K > 333.15 K and plated -> stage3 fail. Rate bottleneck diagnosed positive-electrode particle surface saturation (scratch/diag_physics.py).",
    "V2 activeboost": "thicker electrodes raise 1C energy (18.61 Wh, ED 466.7 Wh/kg, mass 39.87 g) but 5C retention drops to 8.4% -> thicker electrodes worsen the diagnosed cathode-surface saturation under fixed current, consistent with diagnosis.",
    "V3 ratemargin": "negative-only particle downsize (5.86->4.0 um) moves retention 8.7->9.7%: negative side was not the 5C bottleneck (cathode is); targeting positive particle size next round.",
}

batch = []
tags = {"C0 baseline": "C0", "V1 massfit": "V1", "V2 activeboost": "V2", "V3 ratemargin": "V3"}
for name, note in notes.items():
    tag = tags[name]
    batch.append({
        "candidate": name,
        "outputs": [
            f"runs/exp/t8_r3/cell/r1_{tag}_5c_dfn.json",
            f"runs/exp/t8_r3/cell/r1_{tag}_derived.json",
            f"runs/exp/t8_r3/cell/r1_{tag}_4c_safety.json",
            f"runs/exp/t8_r3/cell/r1_{tag}_1c_dfn.json",
            f"runs/exp/t8_r3/cell/r1_{tag}_energy.json",
        ],
        "note": note,
    })

out = cell / "log_eval_r1_batch.json"
out.write_text(json.dumps(batch, indent=2), encoding="utf-8")
print("wrote", out)