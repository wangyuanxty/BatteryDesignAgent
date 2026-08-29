"""Scratch: diff parameter sets Chen2020 vs OKane2022 vs ORegan2022 (key-level)."""
import pybamm

sets = {}
for name in ["Chen2020", "OKane2022", "ORegan2022"]:
    pv = pybamm.ParameterValues(name)
    sets[name] = set(pv.keys())
    for k in pv.keys():
        if any(s in k.lower() for s in ("silicon", "siox", "graphite", "cracking", "loss")):
            v = pv[k]
            try:
                vs = f"{float(v):.4g}"
            except (TypeError, ValueError):
                vs = f"<{type(v).__name__}>"
            print(f"{name} | {k} = {vs}")

print()
print("OKane2022 - Chen2020:", sorted(sets["OKane2022"] - sets["Chen2020"]))
print()
print("Chen2020 - OKane2022:", sorted(sets["Chen2020"] - sets["OKane2022"]))
print()
print("ORegan2022 extra vs Chen2020:", sorted(sets["ORegan2022"] - sets["Chen2020"])[:40])
