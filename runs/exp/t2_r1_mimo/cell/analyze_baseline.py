import json

# Check 1C discharge capacity for low-T ratio
with open("runs/exp/t2_r1_mimo/cell/r1_baseline_1c.json") as f:
    d1c = json.load(f)
with open("runs/exp/t2_r1_mimo/cell/r1_baseline_lowT.json") as f:
    dlt = json.load(f)

cap_1c = d1c["capacity_ah"]
cap_lt = dlt["capacity_ah"]
retention = cap_lt / cap_1c * 100
print(f"1C capacity: {cap_1c:.4f} Ah")
print(f"Low-T capacity: {cap_lt:.4f} Ah")
print(f"Retention: {retention:.2f}%")

# Check 4C charge details
with open("runs/exp/t2_r1_mimo/cell/r1_baseline_4c.json") as f:
    d4c = json.load(f)
print(f"\n4C charge: capacity_ah={d4c['capacity_ah']:.4f}, T_max={d4c['T_max_K']:.2f} K")
ap = d4c.get("anode_potential_v", [])
t = d4c.get("time_s", [])
print(f"4C time range: {min(t):.1f} to {max(t):.1f} s")
print(f"4C anode potential: min={min(ap):.4f} V, max={max(ap):.4f} V")
# Count negative anode potential points
neg_count = sum(1 for x in ap if x < 0)
print(f"Anode potential < 0: {neg_count}/{len(ap)} points ({neg_count/len(ap)*100:.1f}%)")

# Check first few anode potential values
print(f"First 10 anode potentials: {[f'{x:.4f}' for x in ap[:10]]}")
