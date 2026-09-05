import json
with open("runs/exp/t2_r1_mimo/cell/r1_baseline_4c.json") as f:
    d = json.load(f)
if "anode_potential_v" in d:
    ap = d["anode_potential_v"]
    print(f"anode_potential_v: len={len(ap)}, min={min(ap):.6f}, max={max(ap):.6f}")
    if min(ap) < 0:
        print("PLATING DETECTED")
    else:
        print("No plating")
else:
    print("No anode_potential_v key found")
    print("Keys:", list(d.keys()))
print(f"capacity_ah: {d.get('capacity_ah', 'N/A')}")
print(f"T_max_K: {d.get('T_max_K', 'N/A')}")
