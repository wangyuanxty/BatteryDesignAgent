"""Summarize simulation outputs: prints scalar keys + key series stats for a list of files."""
import json
import sys
from pathlib import Path

for f in sys.argv[1:]:
    p = Path(f)
    j = json.loads(p.read_text(encoding="utf-8"))
    print(f"=== {p.name} ===")
    for k, v in j.items():
        if isinstance(v, list):
            if v and isinstance(v[0], (int, float)):
                print(f"  {k}: len={len(v)} first={v[0]:.4g} last={v[-1]:.4g} min={min(v):.4g} max={max(v):.4g}")
            else:
                print(f"  {k}: len={len(v)}")
        elif isinstance(v, dict):
            print(f"  {k}: dict keys={list(v.keys())[:8]}")
        else:
            print(f"  {k} = {v}")
