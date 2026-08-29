"""t4_r3 §1.5 anchor verification: dump key Chen2020 parameters (discriminant anchor +
geometry/transport/electrolyte keys needed for ceiling assessment). Read-only.

Writes workspace param_dump_chosen.json (agent-built input artifact, not a command --out file).
"""
import json

import pybamm

from bda.store import CaseWorkspace

ws = CaseWorkspace("exp/t4_r3", root="runs")

pv = pybamm.ParameterValues("Chen2020")

keys = [
    # Discriminant anchor (NMC811/graphite, no SiOx — OKane2022 would show SiOx keys)
    "Positive electrode conductivity [S.m-1]",
    "Negative electrode conductivity [S.m-1]",
    # Geometry / architecture
    "Electrode height [m]",
    "Electrode width [m]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator porosity",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Nominal cell capacity [A.h]",
    "Cell volume [m3]",
    "Cell cooling surface area [m2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Initial concentration in electrolyte [mol.m-3]",
    "Cation transference number",
    "Negative electrode OCP [V]",
    "_max_n_stoich",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "SEI kinetic rate constant [m.s-1]",
]

dump = {}
for k in keys:
    if k in pv:
        v = pv[k]
        if isinstance(v, (int, float)):
            dump[k] = {"value": v}
        elif callable(v):
            dump[k] = {"callable": True, "repr": repr(v)[:800]}
        else:
            dump[k] = {"repr": repr(v)[:800]}
    else:
        dump[k] = {"missing": True}

# pybamm sets have items() and also print_parameters-ish API; pick a few extras
extras = [
    ("_sig_function", None),
]

out = ws.path / "param_dump_chosen.json"
out.write_text(json.dumps(dump, indent=2, ensure_ascii=False), encoding="utf-8")
print("wrote", out)
for k, v in dump.items():
    if "value" in v:
        print(f"{k} = {v['value']}")
    elif "callable" in v:
        print(f"{k} = <callable> {v['repr'][:110]}")
    elif "missing" in v:
        print(f"{k} = MISSING")
    else:
        print(f"{k} = {v['repr'][:110]}")