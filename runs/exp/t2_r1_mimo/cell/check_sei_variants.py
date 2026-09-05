import json

print("=== SEI@500 Results for M/N/O ===")
for v in ["M", "N", "O"]:
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_aging500.json", encoding="utf-8") as f:
        d = json.load(f)
    sei = d["sei_thickness_nm_end"]
    passed = sei <= 550
    print(f"  Variant {v}: SEI = {sei:.1f} nm {'PASS' if passed else 'FAIL'} (target: <= 550)")

# Also run 1C + 4C for the best SEI variant to confirm other criteria
# Check which passed
for v in ["M", "N", "O"]:
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_aging500.json", encoding="utf-8") as f:
        d = json.load(f)
    if d["sei_thickness_nm_end"] <= 550:
        print(f"\nVariant {v} passes SEI@500! Running full verification...")
        break
