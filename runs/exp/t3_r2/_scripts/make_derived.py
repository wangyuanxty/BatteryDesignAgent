"""Derive decision metrics for log-evaluate (mechanical, per SKILL Stage 3 rate rule).

Usage: python make_derived.py <1c_dfn.json> <5c_dfn.json> <out.json>
Writes: capacity_retention_5c = 5C capacity / 1C capacity (same params, SKILL rule);
        t_max_5c_k = T_max_K of the 5C discharge output (task T_max<=60C covers the 5C scenario).
"""
import json
import sys

one = json.loads(open(sys.argv[1], encoding="utf-8").read())
five = json.loads(open(sys.argv[2], encoding="utf-8").read())
caps = [d["capacity_ah"] for d in (one, five)]
if not caps[0]:
    raise SystemExit("1C capacity is 0; cannot derive retention")
retention = round(five["capacity_ah"] / one["capacity_ah"], 4)
out = {
    "capacity_retention_5c": retention,
    "t_max_5c_k": round(float(five["T_max_K"]), 4),
    "derivation": (
        f"capacity_retention_5c = 5C capacity {caps[1]:.4f} Ah / 1C capacity {caps[0]:.4f} Ah "
        f"(same parameter set, SKILL Stage 3 rate-scenario rule); "
        f"t_max_5c_k = T_max_K of the 5C discharge run (25 C ambient, lumped thermal)"
    ),
}
open(sys.argv[3], "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2))
print(out)