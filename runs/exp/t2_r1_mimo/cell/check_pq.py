import json

print("=== SEI@500 for P/Q ===")
for v in ["P", "Q"]:
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_aging500.json", encoding="utf-8") as f:
        d = json.load(f)
    sei = d["sei_thickness_nm_end"]
    passed = sei <= 550
    print(f"  Variant {v}: SEI = {sei:.1f} nm {'PASS' if passed else 'FAIL'}")
