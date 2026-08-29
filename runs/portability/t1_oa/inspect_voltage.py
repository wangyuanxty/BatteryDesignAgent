import json
import sys

for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    v = d.get("voltage_v")
    if v:
        print(f, "max_voltage_V =", max(v), "min_voltage_V =", min(v))
    else:
        print(f, "no voltage_v")
