import json
import re

d = json.load(open(r"runs/exp/known_set_comp/known_set_v3.json", encoding="utf-8"))
# membership layer: find the list under whichever key the script uses
mem = None
for k in ("membership", "formulas", "known_formulas", "catalogue"):
    if k in d:
        mem = d[k]
        break
if mem is None:
    # fall back to inspecting top-level keys
    print("top-level keys:", sorted(d.keys()))
    raise SystemExit(0)
if isinstance(mem, list) and mem and isinstance(mem[0], dict):
    keys = set(m["formula"] for m in mem if "formula" in m)
elif isinstance(mem, dict):
    keys = set(mem.keys())
else:
    keys = set(mem)
print("membership key used:", type(mem).__name__, "count:", len(keys))
for f in ("LiNi0.75Mg0.25PO4F", "LiNi0.875Mg0.125PO4F"):
    print(f, "->", "IN MEMBERSHIP (REJECT)" if f in keys else "not in membership (layer A0 pass)")
norm = {re.sub(r"\s+", "", k).lower() for k in keys}
for f in ("LiNi0.75Mg0.25PO4F", "LiNi0.875Mg0.125PO4F"):
    print("normalized:", f, "->", "HIT" if f.lower() in norm else "clean")
