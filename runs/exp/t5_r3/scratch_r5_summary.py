"""Round-5 summary."""
import json

base = r"runs\exp\t5_r3\cell"
for v in ["y1", "y2", "y3", "y4"]:
    s = json.load(open(fr"{base}\r5_{v}_4c_45c.json", encoding="utf-8"))
    ap = s.get("anode_potential_v", [0.0])
    t, volt = s.get("time_s", []), s.get("voltage_v", [])
    jumps = [i for i in range(1, len(volt)) if volt[i] - volt[i - 1] > 0.05]
    i0 = jumps[-1] if jumps else 0
    dur = t[-1] - t[i0] if i0 else 0.0
    print(
        f"{v}: T_max={s.get('T_max_K'):.2f}K({s.get('T_max_K',0)-273.15:.1f}C) "
        f"min_ap={min(ap):+.4f}V chg={dur:.0f}s chgAh={dur*4/3600:.2f} "
        f"n_neg={sum(1 for x in ap if x < 0)} cap={s.get('capacity_ah'):.3f}Ah"
    )