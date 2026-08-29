"""Read probeA aging scalar + injected_defaults of 4C outputs + cooling surface area presence."""
import json
from pathlib import Path

ws = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_noforce")
d = json.loads((ws / "cell/r1_probeA_aging45.json").read_text(encoding="utf-8-sig"))
print("probeA aging sei_thickness_nm_end:", d["sei_thickness_nm_end"])
print("probeA aging caps first/last/min/max:", d["capacity_ah_per_cycle"][0], d["capacity_ah_per_cycle"][-1],
      min(d["capacity_ah_per_cycle"]), max(d["capacity_ah_per_cycle"]))
d2 = json.loads((ws / "cell/r1_base_aging45.json").read_text(encoding="utf-8-sig"))
print("baseline aging caps first/last/min/max:", d2["capacity_ah_per_cycle"][0], d2["capacity_ah_per_cycle"][-1],
      min(d2["capacity_ah_per_cycle"]), max(d2["capacity_ah_per_cycle"]))
for f in ("cell/r1_base_4c45.json", "cell/r1_probeA_4c45.json"):
    d3 = json.loads((ws / f).read_text(encoding="utf-8-sig"))
    print(f, "injected_defaults:", json.dumps(d3.get("injected_defaults", {}), ensure_ascii=False))
