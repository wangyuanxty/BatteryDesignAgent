"""Print scalar keys of round-1 outputs."""
import json
from pathlib import Path

ws = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_noforce")
files = [
    "cell/r1_base_1c_dfn.json",
    "cell/r1_base_energy.json",
    "cell/r1_base_4c45.json",
    "cell/r1_base_aging45.json",
    "cell/r1_probeA_1c_dfn.json",
    "cell/r1_probeA_energy.json",
    "cell/r1_probeA_4c45.json",
]
for f in files:
    d = json.loads((ws / f).read_text(encoding="utf-8-sig"))
    scalars = {k: round(v, 6) if isinstance(v, float) else v for k, v in d.items() if isinstance(v, (int, float, bool))}
    series = {k: f"list[{len(v)}] min={min(v):.5g} max={max(v):.5g}" for k, v in d.items() if isinstance(v, list) and v and isinstance(v[0], (int, float))}
    print(f"--- {f} ---")
    print("  scalars:", json.dumps(scalars, ensure_ascii=False))
    print("  series :", json.dumps(series, ensure_ascii=False))
