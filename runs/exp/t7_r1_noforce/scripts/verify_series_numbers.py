"""Verify series-derived numbers quoted in deliverables."""
import json
from pathlib import Path

ws = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_noforce")
d = json.loads((ws / "cell/r5_slim_4c45.json").read_text(encoding="utf-8-sig"))
print("4c45 series keys:", [k for k, v in d.items() if isinstance(v, list)])
for k, v in d.items():
    if isinstance(v, list) and v and isinstance(v[0], (int, float)):
        print(f"  {k}: len={len(v)} first={v[0]:.6g} last={v[-1]:.6g} min={min(v):.6g} max={max(v):.6g}")
        if "anode_potential" in k or "Voltage" in k or "Current" in k:
            print(f"    -> head: {[round(x, 4) for x in v[:5]]}")
            print(f"    -> tail: {[round(x, 4) for x in v[-5:]]}")

n = json.loads((ws / "validation/r5_slim_nail.json").read_text(encoding="utf-8-sig"))
print("\nnail series keys:", [k for k, v in n.items() if isinstance(v, list)])
for k, v in n.items():
    if isinstance(v, list) and v and isinstance(v[0], (int, float)):
        print(f"  {k}: len={len(v)} first={v[0]:.6g} last={v[-1]:.6g} min={min(v):.6g} max={max(v):.6g}")

# aging trajectory (capacity climb artifact, quoted in dvpr)
a = json.loads((ws / "cell/r5_slim_aging45.json").read_text(encoding="utf-8-sig"))
print("\naging45 series keys:", [k for k, v in a.items() if isinstance(v, list)])
for k, v in a.items():
    if isinstance(v, list) and v and isinstance(v[0], (int, float)):
        print(f"  {k}: len={len(v)} first={v[0]:.6g} last={v[-1]:.6g} min={min(v):.6g} max={max(v):.6g}")
