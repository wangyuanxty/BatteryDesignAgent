"""Read key values from finalist cell outputs (t10_r4)."""
import json
import io

base = "runs/exp/t10_r4/cell/"
for f, keys in [
    ("aging_finalist.json", ["sei_thickness_nm_end", "model_used"]),
    ("finalist_energy.json", ["energy_density_wh_kg", "energy_density_wh_l", "mass_kg", "capacity_ah", "energy_wh"]),
    ("finalist_4c45.json", ["T_max_K", "model_used"]),
    ("finalist_tr.json", ["triggered", "T_max_K", "dTdt_max_K_s", "trigger_time_s"]),
]:
    d = json.load(io.open(base + f, encoding="utf-8"))
    print(f, {k: d.get(k) for k in keys})

d4 = json.load(io.open(base + "finalist_4c45.json", encoding="utf-8"))
ap = d4.get("anode_potential_v")
print("anode_potential_v: min=%.5f max=%.5f n=%d" % (min(ap), max(ap), len(ap)))

d1 = json.load(io.open(base + "finalist_1c_spme.json", encoding="utf-8"))
print("1c:", d1.get("capacity_ah"), d1.get("model_used"))

da = json.load(io.open(base + "aging_finalist.json", encoding="utf-8"))
caps = da.get("capacity_ah_per_cycle")
print("aging last cap: %.4f (n=%d)" % (caps[-1], len(caps)))
