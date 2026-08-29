import json

base = r"runs\exp\t4_r1_flash\cell"
a = json.load(open(base + r"\final_b7_1c_dfn.json", encoding="utf-8"))
b = json.load(open(base + r"\final_b7_lowt_dfn.json", encoding="utf-8"))
r = b["capacity_ah"] / a["capacity_ah"]
out = {
    "low_temperature_retention": r,
    "capacity_1c_ah": a["capacity_ah"],
    "capacity_lowt_ah": b["capacity_ah"],
    "ref_source": "final_b7_1c_dfn.json",
    "lowt_source": "final_b7_lowt_dfn.json",
    "derived_by": "mechanical ratio, DFN",
}
with open(base + r"\final_b7_retention_dfn.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(out, indent=2))
print(json.dumps(out, indent=1))
