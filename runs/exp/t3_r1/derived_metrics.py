# Mechanically derived metrics for log-evaluate (agent-built input writer).
# retention_5c = 5C discharge capacity / 1C discharge capacity (same parameters)
# T_max_K      = max of lumped-thermal T_max over the 5C-discharge and 4C-charge protocols
# Usage: python derived_metrics.py <1C.json> <5C.json> <4C.json> <out.json>
import json
import sys


def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)


def main():
    j1c, j5c, j4c, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    d1, d5, d4 = load(j1c), load(j5c), load(j4c)
    caps = {"1C": float(d1["capacity_ah"]), "5C": float(d5["capacity_ah"])}
    tmax = {}
    for tag, d in (("1C", d1), ("5C", d5), ("4C_charge", d4)):
        if "T_max_K" in d:
            tmax[tag] = float(d["T_max_K"])
    derived = {
        "retention_5c": round(caps["5C"] / caps["1C"], 6),
        "T_max_K": round(max(tmax.values()), 4),
        "_derivation": {
            "retention_5c": f"capacity_ah(5C)={caps['5C']} / capacity_ah(1C)={caps['1C']}",
            "T_max_K": f"max over protocols = {tmax} (5C discharge 25C amb, 4C charge 45C amb)",
        },
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(derived, f, indent=2)
    print("derived ->", out, derived)


if __name__ == "__main__":
    main()
