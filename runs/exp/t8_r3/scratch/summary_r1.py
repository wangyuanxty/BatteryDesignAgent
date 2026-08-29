"""Summarize round-1 outputs: scalar keys from all JSONs + derived retention."""
import json
import sys
from pathlib import Path

cell = Path("runs/exp/t8_r3/cell")

def scalars(p):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    out = {k: v for k, v in d.items() if isinstance(v, (int, float, bool))}
    if "anode_potential_v" in d and isinstance(d["anode_potential_v"], list) and d["anode_potential_v"]:
        out["anode_min_v"] = min(d["anode_potential_v"])
    return out

for name in ["C0", "V1", "V2", "V3"]:
    print("=" * 10, name)
    for kind in ["1c_dfn", "energy", "5c_dfn", "4c_safety"]:
        p = cell / f"r1_{name}_{kind}.json"
        if p.exists():
            print(f"  {kind}:", scalars(p))
    # retention derived
    p1 = cell / f"r1_{name}_1c_dfn.json"
    p5 = cell / f"r1_{name}_5c_dfn.json"
    if p1.exists() and p5.exists():
        c1 = json.loads(p1.read_text(encoding="utf-8"))["capacity_ah"]
        c5 = json.loads(p5.read_text(encoding="utf-8"))["capacity_ah"]
        print(f"  retention_5c = {c5}/{c1} = {c5/c1:.4f}")