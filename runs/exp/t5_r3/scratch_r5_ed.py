"""Round-5 ED check."""
import json

base = r"runs\exp\t5_r3\cell"
for v in ["y1", "y2", "y3", "y4"]:
    e = json.load(open(fr"{base}\r5_{v}_energy.json", encoding="utf-8"))
    s = json.load(open(fr"{base}\r5_{v}_4c_45c.json", encoding="utf-8"))
    ap = s.get("anode_potential_v", [0.0])
    print(
        f"{v}: ED={e['energy_density_wh_kg']:.1f} Wh/kg cap={e['capacity_ah']:.3f} Ah mass={e['mass_kg']*1000:.2f} g | "
        f"T_max={s.get('T_max_K'):.2f}K min_ap={min(ap):+.4f}V"
    )