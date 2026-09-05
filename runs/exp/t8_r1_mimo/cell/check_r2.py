import json

files = {
    'OK2022_1C': 'runs/exp/t8_r1_mimo/cell/r2_okane2022_1c.json',
    'OK2022_5C': 'runs/exp/t8_r1_mimo/cell/r2_okane2022_5c.json',
    'Chen_B_1C': 'runs/exp/t8_r1_mimo/cell/r2_chen2020_archB_1c.json',
    'Chen_B_5C': 'runs/exp/t8_r1_mimo/cell/r2_chen2020_archB_5c.json',
    'Chen_C_1C': 'runs/exp/t8_r1_mimo/cell/r2_chen2020_archC_1c.json',
    'Chen_C_5C': 'runs/exp/t8_r1_mimo/cell/r2_chen2020_archC_5c.json',
}
for name, path in files.items():
    d = json.load(open(path))
    cap = d["capacity_ah"]
    tmax = d.get("T_max_K", "N/A")
    model = d["model_used"]
    print(f"{name}: cap={cap:.4f} Ah, T_max={tmax}, model={model}")
