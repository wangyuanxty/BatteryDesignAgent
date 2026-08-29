"""t5_r3 summary reader for round-2 candidates."""
import json

base = r"runs\exp\t5_r3\cell"
for v in ["v1", "v2", "v3", "v4"]:
    e = json.load(open(fr"{base}\r2_{v}_energy.json", encoding="utf-8"))
    s = json.load(open(fr"{base}\r2_{v}_4c_45c.json", encoding="utf-8"))
    d1 = json.load(open(fr"{base}\r2_{v}_1c_spme.json", encoding="utf-8"))
    ap = s.get("anode_potential_v", [0.0])
    print(
        f"{v}: ED={e['energy_density_wh_kg']:.1f} Wh/kg cap={e['capacity_ah']:.3f} Ah "
        f"mass={e['mass_kg']*1000:.1f} g | "
        f"4C T_max={s.get('T_max_K'):.2f} K ({s.get('T_max_K', 0)-273.15:.1f} C) "
        f"min_ap={min(ap):+.3f} V 4C_cap={s.get('capacity_ah'):.3f} Ah "
        f"1C_Tmax={d1.get('T_max_K'):.1f} K"
    )