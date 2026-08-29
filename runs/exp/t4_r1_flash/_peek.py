"""Print key scalars from run-pyamm / calc-energy / derived JSONs (UTF-8 safe)."""
import json, sys

for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    print(f"=== {f}")
    for k, v in d.items():
        if isinstance(v, (list, dict)):
            if k == "anode_potential_v":
                print(f"  {k}: len={len(v)}, min={min(v):.4f}, max={max(v):.4f}")
            elif k == "injected_defaults":
                print(f"  {k}: {v}")
            else:
                print(f"  {k}: <{type(v).__name__} len={len(v)}>")
        else:
            print(f"  {k}: {v}")
