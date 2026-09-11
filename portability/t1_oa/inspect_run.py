import json
import sys

for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    ap = d.get("anode_potential_v")
    mn = min(ap) if ap else None
    plated = (mn < 0) if mn is not None else None
    print(f)
    print("  T_max_K =", d.get("T_max_K"))
    print("  anode_min_V =", mn)
    print("  plated =", plated)
    print("  capacity_ah =", d.get("capacity_ah"))
    print("  model =", d.get("model_used"))
    print("  injected_defaults =", sorted(d.get("injected_defaults", {}).keys()))
