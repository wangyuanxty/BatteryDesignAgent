import json

# Read 500-cycle aging
with open("runs/exp/t2_r1_mimo/cell/r1_baseline_aging500.json") as f:
    d500 = json.load(f)
print(f"500-cycle aging: SEI thickness = {d500['sei_thickness_nm_end']:.1f} nm")
print(f"500-cycle final capacity = {d500['capacity_ah_per_cycle'][-1]:.4f} Ah")

# Read 100-cycle aging
with open("runs/exp/t2_r1_mimo/cell/r1_baseline_aging100.json") as f:
    d100 = json.load(f)
print(f"100-cycle aging: SEI thickness = {d100['sei_thickness_nm_end']:.1f} nm")
print(f"100-cycle final capacity = {d100['capacity_ah_per_cycle'][-1]:.4f} Ah")
