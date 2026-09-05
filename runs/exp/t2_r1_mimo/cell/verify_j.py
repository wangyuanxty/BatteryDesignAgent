import json

print("=== Variant J Full Results ===")

# 1C discharge + ED
with open("runs/exp/t2_r1_mimo/cell/r4_J_1c.json", encoding="utf-8") as f:
    d1c = json.load(f)
with open("runs/exp/t2_r1_mimo/cell/r4_J_energy.json", encoding="utf-8") as f:
    energy = json.load(f)
print(f"ED: {energy['energy_density_wh_kg']:.2f} Wh/kg (target: >= 327.18)")
print(f"1C capacity: {d1c['capacity_ah']:.4f} Ah")

# 4C plating
with open("runs/exp/t2_r1_mimo/cell/r4_J_4c.json", encoding="utf-8") as f:
    d4c = json.load(f)
ap = d4c["anode_potential_v"]
min_ap = min(ap)
plated = min_ap < 0
print(f"4C plating: {'YES (FAIL)' if plated else 'NO (PASS)'} (min V = {min_ap:.6f})")
print(f"4C T_max: {d4c['T_max_K']:.2f} K (target: <= 350)")

# Low-T
with open("runs/exp/t2_r1_mimo/cell/r4_J_lowT.json", encoding="utf-8") as f:
    dlt = json.load(f)
retention = dlt["capacity_ah"] / d1c["capacity_ah"] * 100
print(f"Low-T retention: {retention:.2f}% (target: >= 90%)")

# Aging 100
with open("runs/exp/t2_r1_mimo/cell/r4_J_aging100.json", encoding="utf-8") as f:
    d100 = json.load(f)
print(f"SEI @100 cyc: {d100['sei_thickness_nm_end']:.1f} nm (target: <= 500)")

# Aging 500
with open("runs/exp/t2_r1_mimo/cell/r4_J_aging500.json", encoding="utf-8") as f:
    d500 = json.load(f)
print(f"SEI @500 cyc: {d500['sei_thickness_nm_end']:.1f} nm (target: <= 550)")

print("\n=== CRITERIA CHECK ===")
checks = [
    ("ED >= 327.18", energy['energy_density_wh_kg'] >= 327.18, f"{energy['energy_density_wh_kg']:.2f}"),
    ("4C no plating", not plated, f"min_V={min_ap:.6f}"),
    ("T_max <= 350", d4c['T_max_K'] <= 350, f"{d4c['T_max_K']:.2f}"),
    ("Low-T >= 90%", retention >= 90, f"{retention:.2f}%"),
    ("SEI@100 <= 500", d100['sei_thickness_nm_end'] <= 500, f"{d100['sei_thickness_nm_end']:.1f} nm"),
    ("SEI@500 <= 550", d500['sei_thickness_nm_end'] <= 550, f"{d500['sei_thickness_nm_end']:.1f} nm"),
]
all_pass = True
for label, passed, value in checks:
    status = "PASS" if passed else "FAIL"
    if not passed: all_pass = False
    print(f"  [{status}] {label}: {value}")

print(f"\n{'ALL CRITERIA MET!' if all_pass else 'SOME CRITERIA FAILED'}")
