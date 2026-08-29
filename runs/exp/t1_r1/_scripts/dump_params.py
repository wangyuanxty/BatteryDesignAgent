"""Dump key parameters of candidate PyBaMM parameter sets for anchor verification."""
import json
import pybamm

SETS = ["Chen2020", "OKane2022", "ORegan2022"]
PATTERNS = [
    "current collector thickness", "electrode height", "electrode width",
    "separator thickness", "separator porosity", "particle radius",
    "upper voltage", "lower voltage", "nominal cell capacity",
    "electrode thickness", "porosity", "total heat transfer",
    "electrolyte conductivity", "cation transference", "electrolyte diffusivity",
    "density", "maximum concentration", "initial concentration",
    "sei kinetic", "cracking rate", "initial temperature",
    "active material volume fraction", "stoichiometry limits",
    "molar mass", "specific heat", "thermal conductivity", "heat of reaction",
]

for name in SETS:
    try:
        pv = pybamm.ParameterValues(name)
    except Exception as e:
        print(f"== {name}: FAILED {e}")
        continue
    keys = [k for k in pv.keys()
            if any(s in k.lower() for s in PATTERNS)]
    out = {k: str(pv[k]) for k in keys}
    print(f"== {name} ({len(out)} keys) ==")
    print(json.dumps(out, indent=1, ensure_ascii=False))
    print()
