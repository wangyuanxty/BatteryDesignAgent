"""Summarize round-2 metrics for A1-A4."""
import json
from pathlib import Path

CELL = Path("cell")
names = [("A1_anode_rebalance", "A1"), ("A2_plus_electrolyte", "A2"),
         ("A3_plus_nanoparticles", "A3"), ("A4_plus_coating_cooling", "A4")]
for n, s in names:
    e = json.loads((CELL / f"r2_{s}_energy.json").read_text(encoding="utf-8"))
    c4 = json.loads((CELL / f"r2_{s}_4c_spme.json").read_text(encoding="utf-8"))
    ag = json.loads((CELL / f"r2_{s}_aging_spme.json").read_text(encoding="utf-8"))
    ap = c4.get("anode_potential_v")
    apmin = min(ap) if ap else None
    print(f"== {n}")
    print(f"  ED_wh_l       = {e['energy_density_wh_l']:.2f}")
    print(f"  midpoint_v    = {e['midpoint_voltage_v']:.4f}")
    print(f"  capacity_ah   = {e['capacity_ah']:.4f}   thickness_m = {e['thickness_m']}")
    print(f"  mass_kg       = {e['mass_kg']:.5f}")
    print(f"  4C: T_max_K   = {c4.get('T_max_K')}  cap_ah = {c4.get('capacity_ah')}")
    print(f"  4C: anode_pot min = {apmin}  (plated = {apmin is not None and apmin < 0})")
    print(f"  4C: keys = {sorted(c4.keys())}")
    print(f"  aging: SEI_end_nm = {ag.get('sei_thickness_nm_end')}")
