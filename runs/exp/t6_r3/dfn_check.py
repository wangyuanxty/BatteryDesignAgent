"""Print model_used + key metrics for DFN verification outputs.

Usage: python dfn_check.py [glob-pattern]   (default: cell/r9_*.json)
"""
import glob
import json
import sys

WS = "runs/exp/t6_r3/cell"
pat = sys.argv[1] if len(sys.argv) > 1 else "r9_*.json"
for f in sorted(glob.glob(f"{WS}/{pat}")):
    with open(f, encoding="utf-8") as fh:
        d = json.load(fh)
    mu = d.get("model_used", "?")
    out = [f.split("/")[-1], f"model={mu}"]
    for k in ("energy_density_wh_l", "midpoint_voltage_v", "T_max_K", "capacity_ah", "sei_thickness_nm_end"):
        if k in d:
            v = d[k]
            if k == "midpoint_voltage_v":
                out.append(f"{k}={v:.6f}")
            else:
                out.append(f"{k}={v:.4g}" if isinstance(v, (int, float)) else f"{k}={v}")
    if "anode_potential_v" in d:
        ap = d["anode_potential_v"]
        out.append(f"amin={min(ap):+.6f}")
    print(" | ".join(out))
