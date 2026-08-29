"""Extra keys: concentration/max-concentration/electrolyte formulation + energy metrics."""
import json
import pybamm
import sys

sys.stdout.reconfigure(encoding="utf-8")

base = "Chen2020"
overrides = json.load(open(r"runs\exp\t4_r1_flash\_params_b7.json", encoding="utf-8"))
pv = pybamm.ParameterValues(base)
pv.update(overrides)

for pat in ["concentration", "Electrolyte", "voltage", "entropy", "OCP"]:
    hits = sorted(k for k in pv.keys() if pat.lower() in k.lower())
    print(f"--- '{pat}': {len(hits)} keys")
    for h in hits:
        v = pv[h]
        if callable(v):
            print(f"    {h} = <function>")
        else:
            try:
                print(f"    {h} = {float(v):.8g}")
            except Exception:
                print(f"    {h} = {str(v)[:80]}")

print()
e = json.load(open(r"runs\exp\t4_r1_flash\cell\final_b7_energy_dfn.json", encoding="utf-8"))
print("=== final_b7_energy_dfn.json full ===")
print(json.dumps(e, indent=1)[:1600])
