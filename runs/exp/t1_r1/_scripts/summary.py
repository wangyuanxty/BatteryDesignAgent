"""Summarize scalar keys + anode potential min of given output JSONs."""
import json
import sys

for path in sys.argv[1:]:
    d = json.load(open(path, encoding="utf-8"))
    out = {}
    for k, v in d.items():
        if isinstance(v, (int, float, bool)):
            out[k] = v
    if "anode_potential_v" in d:
        out["anode_potential_min_v"] = min(d["anode_potential_v"])
    print(path)
    print(json.dumps(out, ensure_ascii=False))
    print()
