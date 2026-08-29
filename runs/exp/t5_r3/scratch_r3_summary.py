"""Round-3 summary."""
import json

base = r"runs\exp\t5_r3\cell"
for v in ["w1", "w2", "w3", "w4"]:
    e = json.load(open(fr"{base}\r3_{v}_energy.json", encoding="utf-8"))
    s = json.load(open(fr"{base}\r3_{v}_4c_45c.json", encoding="utf-8"))
    ap = s.get("anode_potential_v", [0.0])
    t = s.get("time_s", [0.0])
    t_chg = [x for x in t if x > 3500]
    dur = (t_chg[-1] - t_chg[0]) if t_chg else 0.0
    print(
        f"{v}: ED={e['energy_density_wh_kg']:.1f} Wh/kg cap={e['capacity_ah']:.3f} Ah mass={e['mass_kg']*1000:.1f} g | "
        f"T_max={s.get('T_max_K'):.2f}K({s.get('T_max_K',0)-273.15:.1f}C) min_ap={min(ap):+.4f}V "
        f"4Ccap={s.get('capacity_ah'):.3f}Ah chg={dur:.0f}s n_neg={sum(1 for x in ap if x < 0)}"
    )