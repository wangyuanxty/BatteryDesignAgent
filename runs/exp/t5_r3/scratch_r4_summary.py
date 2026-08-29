"""Round-4 summary + charge-duration detail."""
import json

base = r"runs\exp\t5_r3\cell"
for v in ["x1", "x2", "x3", "x4"]:
    e = json.load(open(fr"{base}\r4_{v}_energy.json", encoding="utf-8"))
    s = json.load(open(fr"{base}\r4_{v}_4c_45c.json", encoding="utf-8"))
    ap = s.get("anode_potential_v", [0.0])
    t, volt = s.get("time_s", []), s.get("voltage_v", [])
    # charge begins at the last voltage up-jump (terminal voltage recovering past ~3.0 after 2.5V cut)
    jumps = [i for i in range(1, len(volt)) if volt[i] - volt[i - 1] > 0.05]
    i0 = jumps[-1] if jumps else 0
    dur = t[-1] - t[i0] if i0 else 0.0
    cap_chg = dur * 4 / 3600.0
    print(
        f"{v}: ED={e['energy_density_wh_kg']:.1f} Wh/kg cap={e['capacity_ah']:.3f} Ah mass={e['mass_kg']*1000:.1f} g | "
        f"T_max={s.get('T_max_K'):.2f}K({s.get('T_max_K',0)-273.15:.1f}C) min_ap={min(ap):+.4f}V "
        f"chg={dur:.0f}s chgAh={cap_chg:.2f} n_neg={sum(1 for x in ap if x < 0)}"
    )