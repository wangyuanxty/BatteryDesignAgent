"""Read R3 candidate scalars."""
import json
from pathlib import Path

ws = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_noforce")
for f in ("cell/r3_anode_1c_dfn.json", "cell/r3_anode_4c45.json", "cell/r3_anode_aging45.json"):
    d = json.loads((ws / f).read_text(encoding="utf-8-sig"))
    scalars = {k: round(v, 6) if isinstance(v, float) else v for k, v in d.items() if isinstance(v, (int, float, bool))}
    series = {k: f"list[{len(v)}] min={min(v):.5g} max={max(v):.5g}" for k, v in d.items() if isinstance(v, list) and v and isinstance(v[0], (int, float))}
    print(f"--- {f} ---")
    print("  scalars:", json.dumps(scalars, ensure_ascii=False))
    print("  series :", json.dumps(series, ensure_ascii=False))
