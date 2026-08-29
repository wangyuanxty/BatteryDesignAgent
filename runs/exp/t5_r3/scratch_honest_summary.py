"""Read honest-4C probes."""
import json

base = r"runs\exp\t5_r3\cell"
for n in ["65", "60"]:
    s = json.load(open(fr"{base}\r3_honest{n}_4c_45c.json", encoding="utf-8"))
    ap = s.get("anode_potential_v", [0.0])
    print(
        f"honest{n}: T_max={s.get('T_max_K'):.2f}K({s.get('T_max_K',0)-273.15:.1f}C) "
        f"min_ap={min(ap):+.4f}V 4Ccap={s.get('capacity_ah'):.3f}Ah n_neg={sum(1 for x in ap if x < 0)}"
    )