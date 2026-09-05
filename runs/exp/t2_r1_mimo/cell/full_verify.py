import json, subprocess, os

os.chdir("D:\\research\\degradation_prognostics\\Battery_Design_Agent")

for v in ["P", "Q"]:
    name_map = {"P": "P_ultra_low_sei", "Q": "Q_very_low_sei"}
    name = name_map.get(v, f"{v}_variant")
    print(f"\n=== Full verification: Variant {v} ===")

    # 1C discharge
    cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "run-pyamm",
           "--params", f"runs/exp/t2_r1_mimo/cell/params_{name}.json",
           "--base", "Chen2020", "--protocol", "1C_discharge", "--mode", "spme",
           "--out", f"runs/exp/t2_r1_mimo/cell/r5_{v}_1c.json"]
    subprocess.run(cmd, capture_output=True)

    # Calc energy
    cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "calc-energy",
           "--sim", f"runs/exp/t2_r1_mimo/cell/r5_{v}_1c.json",
           "--params", f"runs/exp/t2_r1_mimo/cell/params_{name}.json",
           "--base", "Chen2020",
           "--out", f"runs/exp/t2_r1_mimo/cell/r5_{v}_energy.json"]
    subprocess.run(cmd, capture_output=True)

    # 4C charge
    cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "run-pyamm",
           "--params", f"runs/exp/t2_r1_mimo/cell/params_{name}.json",
           "--base", "Chen2020", "--protocol", "4C_charge_45C", "--mode", "spme",
           "--thermal", "lumped", "--plating",
           "--out", f"runs/exp/t2_r1_mimo/cell/r5_{v}_4c.json"]
    subprocess.run(cmd, capture_output=True)

    # Low-T
    cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "run-pyamm",
           "--params", f"runs/exp/t2_r1_mimo/cell/params_{name}.json",
           "--base", "Chen2020", "--protocol", "lowT_discharge", "--mode", "spme",
           "--out", f"runs/exp/t2_r1_mimo/cell/r5_{v}_lowT.json"]
    subprocess.run(cmd, capture_output=True)

    # Aging 100
    cmd = [".venv\\Scripts\\python.exe", "-m", "bda", "run-pyamm",
           "--params", f"runs/exp/t2_r1_mimo/cell/params_{name}.json",
           "--base", "Chen2020", "--protocol", "aging_1C_100cyc", "--mode", "spme",
           "--out", f"runs/exp/t2_r1_mimo/cell/r5_{v}_aging100.json"]
    subprocess.run(cmd, capture_output=True)

    # Now read all results
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_energy.json", encoding="utf-8") as f:
        energy = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_4c.json", encoding="utf-8") as f:
        d4c = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_lowT.json", encoding="utf-8") as f:
        dlt = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_1c.json", encoding="utf-8") as f:
        d1c = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_aging100.json", encoding="utf-8") as f:
        d100 = json.load(f)
    with open(f"runs/exp/t2_r1_mimo/cell/r5_{v}_aging500.json", encoding="utf-8") as f:
        d500 = json.load(f)

    ap = d4c["anode_potential_v"]
    min_ap = min(ap)
    plated = min_ap < 0
    retention = dlt["capacity_ah"] / d1c["capacity_ah"] * 100

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

    print(f"  >>> {'ALL CRITERIA MET!' if all_pass else 'SOME CRITERIA FAILED'}")
