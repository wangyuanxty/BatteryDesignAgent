import json

for v in ["B", "D"]:
    with open(f"runs/exp/t2_r1_mimo/cell/r2_{v}_aging100.json") as f:
        d100 = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r2_{v}_aging500.json") as f:
        d500 = json.load(f)
    print(f"Variant {v}:")
    print(f"  SEI @100 cyc: {d100['sei_thickness_nm_end']:.1f} nm (threshold: 500)")
    print(f"  SEI @500 cyc: {d500['sei_thickness_nm_end']:.1f} nm (threshold: 550)")
    print(f"  Cap @100 cyc end: {d100['capacity_ah_per_cycle'][-1]:.4f} Ah")
    print(f"  Cap @500 cyc end: {d500['capacity_ah_per_cycle'][-1]:.4f} Ah")
    print()
