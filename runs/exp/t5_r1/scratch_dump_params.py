"""Scratch (agent-built input helper, not a bda output artifact): dump key parameters
of candidate base parameter sets for anchor verification and Stage-1 planning."""
import json
import pybamm

KEYS = [
    "Nominal cell capacity [A.h]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Separator thickness [m]",
    "Separator porosity",
    "Separator density [kg.m-3]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Upper voltage cut-off [V]",
    "Lower voltage cut-off [V]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "SEI kinetic rate constant [m.s-1]",
    "SEI reaction exchange current density [A.m-2]",
    "Positive electrode cracking rate",
    "Negative electrode cracking rate",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode conductivity [S.m-1]",
    "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]",
    "Negative electrode diffusivity [m2.s-1]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
]

def dump(name):
    try:
        pv = pybamm.ParameterValues(name)
    except Exception as e:
        print(f"### {name}: UNAVAILABLE ({e})")
        return
    out = {}
    for k in KEYS:
        if k in pv:
            v = pv[k]
            try:
                out[k] = float(v)
            except (TypeError, ValueError):
                out[k] = f"<{type(v).__name__}>"
    print(f"### {name}")
    print(json.dumps(out, indent=1, default=str))
    # discriminant check: silicon-related keys
    si = [k for k in pv.keys() if "ilicon" in k or "SiOx" in k or "SiO" in k]
    print(f"--- {name} silicon-ish keys: {si[:10]}")
    print(f"--- {name} total key count: {len(pv.keys())}")

for b in ["Chen2020", "OKane2022", "ORegan2022", "Prada2013"]:
    dump(b)

# LNMO custom set
from pathlib import Path
lnmo = Path("D:/research/degradation_prognostics/Battery_Design_Agent/.claude/skills/virtual-battery-factory/scripts/bda/simulators/data/LNMO.json")
print("### LNMO.json exists:", lnmo.exists())
if lnmo.exists():
    data = json.loads(lnmo.read_text(encoding="utf-8"))
    print(json.dumps({k: (str(v)[:80]) for k, v in data.items()}, indent=1))
