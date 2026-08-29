"""Read isolation 4C results."""
import json

base = r"runs\exp\t5_r3\cell"
for tag in ["isoA", "isoB", "isoC", "isoD", "okanebase"]:
    s = json.load(open(fr"{base}\r2_{tag}_4c_45c.json", encoding="utf-8"))
    ap = s.get("anode_potential_v", [0.0])
    t = s.get("time_s", [0.0])
    # charge segment: after the 1C pre-discharge; detect as t > 3500
    t_chg = [x for x in t if x > 3500]
    dur_chg = (t_chg[-1] - t_chg[0]) if t_chg else 0.0
    print(
        f"{tag:10s} T_max={s.get('T_max_K'):.2f}K min_ap={min(ap):+.4f}V "
        f"4Ccap={s.get('capacity_ah'):.4f}Ah charge_dur~{dur_chg:.0f}s n_neg={sum(1 for x in ap if x < 0)}"
    )