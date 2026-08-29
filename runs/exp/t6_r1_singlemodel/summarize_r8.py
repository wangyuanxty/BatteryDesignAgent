"""Summarize R8 E5/E6 metrics for the evaluate notes."""
import json
from pathlib import Path

CELL = Path("cell")
for tag in ("E5", "E6"):
    try:
        e = json.loads((CELL / f"r8_{tag}_energy.json").read_text(encoding="utf-8"))
        c4 = json.loads((CELL / f"r8_{tag}_4c_spme.json").read_text(encoding="utf-8"))
        ag = json.loads((CELL / f"r8_{tag}_aging_spme.json").read_text(encoding="utf-8"))
        ap = c4.get("anode_potential_v")
        plated = bool(ap) and min(ap) < 0
        dur_s = (c4.get("capacity_ah") or 0) * 3600 / 4.0
        print(f"== {tag}: ED={e['energy_density_wh_l']:.2f} mid={e['midpoint_voltage_v']:.4f} "
              f"cap={e['capacity_ah']:.4f} thick={e['thickness_m']}")
        print(f"   4C: T={c4.get('T_max_K'):.3f} cap_ah={c4.get('capacity_ah'):.4f} -> dur {dur_s:.1f} s "
              f"anode_min={min(ap) if ap else None} plated={plated}")
        print(f"   aging SEI={ag.get('sei_thickness_nm_end'):.2f}")
    except Exception as ex:
        print(f"== {tag}: ERROR {ex}")
