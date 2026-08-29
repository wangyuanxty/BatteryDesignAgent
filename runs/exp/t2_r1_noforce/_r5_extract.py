"""Extract R5 result scalars from tool outputs (F1 full battery, F2/S1 aging-only)."""
import json

def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

for tag in ["f1"]:
    en = load(f"cell/r5_{tag}_energy.json")
    fc = load(f"cell/r5_{tag}_4c_dfn.json")
    a100 = load(f"cell/r5_{tag}_aging100_spme.json")
    a500 = load(f"cell/r5_{tag}_aging500_spme.json")
    min_v = min(fc["anode_potential_v"])
    charge_in = fc["capacity_ah"][-1] if isinstance(fc["capacity_ah"], list) else fc["capacity_ah"]
    lowt = load(f"cell/r5_{tag}_lowT_spme.json")
    print(f"[{tag}] ED={en['energy_density_wh_kg']:.2f} Wh/kg  cap={en['capacity_ah']:.4f} Ah  "
          f"cap_lowT={lowt['capacity_ah']:.4f} Ah  "
          f"4C min_anode={min_v:.4f} V  charge_in={charge_in:.4f} Ah  "
          f"SEI100={float(a100['sei_thickness_nm_end']):.2f} nm  SEI500={float(a500['sei_thickness_nm_end']):.2f} nm")
for tag in ["f2", "s1"]:
    a100 = load(f"cell/r5_{tag}_aging100_spme.json")
    a500 = load(f"cell/r5_{tag}_aging500_spme.json")
    print(f"[{tag}] SEI100={float(a100['sei_thickness_nm_end']):.2f} nm  SEI500={float(a500['sei_thickness_nm_end']):.2f} nm")
