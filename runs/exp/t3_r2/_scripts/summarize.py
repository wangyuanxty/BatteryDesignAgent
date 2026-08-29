"""Summarize run-pyamm output scalars + key series stats (avoids dumping huge arrays into context)."""
import json
import sys

for path in sys.argv[1:]:
    d = json.loads(open(path, encoding="utf-8").read())
    scalars = {k: v for k, v in d.items() if isinstance(v, (int, float, bool))}
    extra = {}
    if "anode_potential_v" in d:
        a = d["anode_potential_v"]
        extra["anode_potential_min_v"] = round(min(a), 5)
        extra["anode_potential_start_v"] = round(a[0], 5)
        extra["anode_potential_end_v"] = round(a[-1], 5)
    print(json.dumps({"file": path, "model_used": d.get("model_used"), "scalars": scalars, **extra}, ensure_ascii=False))