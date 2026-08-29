"""Extract R2 (V1/V2/V3) result scalars from tool outputs for the missing R2 evaluate entries."""
import json

def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

for tag in ["v1", "v2", "v3"]:
    en = load(f"cell/r2_{tag}_energy.json")
    fc = load(f"cell/r2_{tag}_4c_dfn.json")
    a100 = load(f"cell/r2_{tag}_aging100_spme.json")
    min_v = min(fc["anode_potential_v"])
    charge_in = fc["capacity_ah"][-1] if isinstance(fc["capacity_ah"], list) else fc["capacity_ah"]
    print(f"[{tag}] ED={en['energy_density_wh_kg']:.2f} Wh/kg  cap={en['capacity_ah']:.4f} Ah  "
          f"4C min_anode={min_v:.4f} V  charge_in={charge_in:.4f} Ah  "
          f"SEI100={float(a100['sei_thickness_nm_end']):.2f} nm")
