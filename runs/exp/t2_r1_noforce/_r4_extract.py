"""Extract R4 (V7/V8) result scalars from tool outputs and write derived SEI-500 files.

Derived metric formula (entry-0 meta): sei_thickness_nm_500cyc = mechanical copy (rename)
of sei_thickness_nm_end from aging_1C_100cyc --cycles 500 output.
"""
import json

def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

def derive_sei500(aging500_path, out_path):
    d = load(aging500_path)
    sei500 = float(d["sei_thickness_nm_end"])
    entry = {
        "sei_thickness_nm_500cyc": round(sei500, 4),
        "formula": "mechanical copy (rename) of sei_thickness_nm_end from aging_1C_100cyc --cycles 500",
        "source": aging500_path.replace("\\", "/").split("/")[-1],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2)
    return sei500

for tag in ["v7", "v8"]:
    en = load(f"cell/r4_{tag}_energy.json")
    fc = load(f"cell/r4_{tag}_4c_dfn.json")
    a100 = load(f"cell/r4_{tag}_aging100_spme.json")
    a500 = load(f"cell/r4_{tag}_aging500_spme.json")
    min_v = min(fc["anode_potential_v"])
    charge_in = fc["capacity_ah"][-1] if isinstance(fc["capacity_ah"], list) else fc["capacity_ah"]
    sei100 = float(a100["sei_thickness_nm_end"])
    sei500 = derive_sei500(f"cell/r4_{tag}_aging500_spme.json", f"derived/r4_{tag}_sei500.json")
    print(f"[{tag}] ED={en['energy_density_wh_kg']:.2f} Wh/kg  cap={en['capacity_ah']:.4f} Ah  "
          f"4C min_anode={min_v:.4f} V  charge_in={charge_in:.4f} Ah  "
          f"SEI100={sei100:.2f} nm  SEI500={sei500:.2f} nm")
print("derived files written: derived/r4_v7_sei500.json, derived/r4_v8_sei500.json")
