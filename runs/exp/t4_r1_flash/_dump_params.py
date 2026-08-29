import pybamm, sys

base = sys.argv[1] if len(sys.argv) > 1 else "Chen2020"
pv = pybamm.ParameterValues(base)
keys = sorted(pv.keys())
print("TOTAL KEYS:", len(keys), "for", base)

pats = [
    "lectrolyte", "transference", "electrode thickness", "porosity", "separator",
    "current collector", "particle radius", "SEI", "reaction rate",
    "exchange-current", "activation energy", "voltage cut-off",
    "Nominal cell capacity", "heat transfer", "Cell volume", "Cell cooling",
    "density", "specific heat", "electrode height", "electrode width",
    "initial concentration", "cracking",
]
for p in pats:
    hits = [k for k in keys if p.lower() in k.lower()]
    print(f"--- pattern '{p}': {len(hits)}")
    for h in hits:
        v = pv[h]
        vt = type(v).__name__
        try:
            vs = f"{float(v):.4g}"
        except Exception:
            vs = str(v)[:90]
        print(f"    {h} = [{vt}] {vs}")
