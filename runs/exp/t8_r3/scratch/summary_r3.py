"""Summarize round-3 outputs."""
import json
from pathlib import Path

cell = Path("runs/exp/t8_r3/cell")

def scalars(p):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    out = {k: v for k, v in d.items() if isinstance(v, (int, float, bool))}
    if isinstance(d.get("anode_potential_v"), list) and d["anode_potential_v"]:
        out["anode_min_v"] = min(d["anode_potential_v"])
    return out

tags = {"V8": "V8_cooled_anodefast", "V9": "V9_cooled_thickneg",
        "V10": "V10_midcool_anodefast", "V11": "V11_cooled_bigmargin"}
for name in ["V8", "V9", "V10", "V11"]:
    tag = tags[name]
    print("=" * 10, name)
    for kind in ["1c_dfn", "energy", "5c_dfn", "4c_safety"]:
        p = cell / f"r3_{tag}_{kind}.json"
        if p.exists():
            s = scalars(p)
            keep = {k: v for k, v in s.items() if k in (
                "capacity_ah", "T_max_K", "anode_min_v", "energy_wh", "mass_kg",
                "energy_density_wh_kg", "model_used")}
            print(f"  {kind}:", keep)
    p1 = cell / f"r3_{tag}_1c_dfn.json"
    p5 = cell / f"r3_{tag}_5c_dfn.json"
    if p1.exists() and p5.exists():
        c1 = json.loads(p1.read_text(encoding="utf-8"))["capacity_ah"]
        c5 = json.loads(p5.read_text(encoding="utf-8"))["capacity_ah"]
        print(f"  retention_5c = {c5/c1:.4f}")