"""Print a compact summary of the given output JSONs (read-only)."""
import json
import sys

for path in sys.argv[1:]:
    d = json.load(open(path, encoding="utf-8-sig"))
    print("=" * 10, path)
    for k, v in d.items():
        if isinstance(v, (int, float, bool)):
            print(f"  {k} = {v}")
        elif isinstance(v, list) and k in ("anode_potential_v",):
            print(f"  {k}: len={len(v)} min={min(v):.5g} max={max(v):.5g}")
        elif isinstance(v, list) and k in ("capacity_ah_per_cycle",):
            print(f"  {k}: len={len(v)} first={v[0]:.4g} last={v[-1]:.4g} min={min(v):.4g} max={max(v):.4g}")
        elif isinstance(v, dict):
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)[:200]}")
        elif isinstance(v, list) and k not in ("time_s", "voltage_v", "cycle_numbers"):
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)[:200]}")
