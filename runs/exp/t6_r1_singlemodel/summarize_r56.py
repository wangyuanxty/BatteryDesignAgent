"""Summarize R5 (D) energy/aging and R6 (E) full metrics."""
import json
from pathlib import Path

CELL = Path("cell")
for tag in ("D1", "D2"):
    e = json.loads((CELL / f"r5_{tag}_energy.json").read_text(encoding="utf-8"))
    ag = json.loads((CELL / f"r5_{tag}_aging_spme.json").read_text(encoding="utf-8"))
    print(f"== D{tag[1]} energy: ED={e['energy_density_wh_l']:.2f} mid={e['midpoint_voltage_v']:.4f} "
          f"cap={e['capacity_ah']:.4f} thick={e['thickness_m']} mass={e['mass_kg']:.5f}")
    print(f"   aging: SEI_end_nm={ag.get('sei_thickness_nm_end')}")
for tag in ("E1", "E2"):
    e = json.loads((CELL / f"r6_{tag}_energy.json").read_text(encoding="utf-8"))
    c4 = json.loads((CELL / f"r6_{tag}_4c_spme.json").read_text(encoding="utf-8"))
    ag = json.loads((CELL / f"r6_{tag}_aging_spme.json").read_text(encoding="utf-8"))
    ap = c4.get("anode_potential_v")
    apmin = min(ap) if ap else None
    vmax = max(c4.get("terminal_voltage_v") or c4.get("voltage_v") or []) if c4.get("terminal_voltage_v") or c4.get("voltage_v") else None
    t = c4.get("time_s") or c4.get("time")
    print(f"== E{tag[1]} energy: ED={e['energy_density_wh_l']:.2f} mid={e['midpoint_voltage_v']:.4f} "
          f"cap={e['capacity_ah']:.4f} thick={e['thickness_m']} mass={e['mass_kg']:.5f}")
    print(f"   4C: T_max_K={c4.get('T_max_K')} cap_ah={c4.get('capacity_ah')} Vmax={vmax} "
          f"anode_pot_min={apmin} plated={apmin is not None and apmin < 0} t_end={t[-1] if t else None}")
    print(f"   aging: SEI_end_nm={ag.get('sei_thickness_nm_end')}")
