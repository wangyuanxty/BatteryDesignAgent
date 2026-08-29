"""Scratch: print summary of bda output JSONs (agent-built helper)."""
import json
import sys

LONG_KEYS = ("voltage_v", "time_s", "anode_potential_v", "cycle_numbers", "capacity_ah_per_cycle", "T_series_K", "t_series_s")

for name in sys.argv[1:]:
    d = json.load(open(name, encoding="utf-8-sig"))
    print(f"=== {name} ===")
    for k, v in d.items():
        if k in LONG_KEYS and isinstance(v, list) and v:
            print(f"  {k}: list len={len(v)} first={v[0]:.6g} last={v[-1]:.6g}")
            if k in ("voltage_v", "anode_potential_v", "T_series_K"):
                print(f"    min={min(v):.6g} max={max(v):.6g}")
        elif isinstance(v, float):
            print(f"  {k}: {v:.6g}")
        else:
            print(f"  {k}: {v}")
    print()
