"""t4_r3: dump OKane2022 geometry/thermal/particle keys (design of round-5 architecture)."""
import json

import pybamm

from bda.store import CaseWorkspace

ws = CaseWorkspace("exp/t4_r3", root="runs")
pv = pybamm.ParameterValues("OKane2022")

keys = [
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
    "Cell cooling surface area [m2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Cation transference number",
    "Initial temperature [K]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
]

dump = {}
for k in keys:
    if k in pv:
        v = pv[k]
        if isinstance(v, (int, float)):
            dump[k] = v
            print(f"{k} = {v}")
        elif callable(v):
            dump[k] = repr(v)[:200]
            print(f"{k} = <callable> {dump[k]}")
        else:
            dump[k] = repr(v)[:200]
            print(f"{k} = {dump[k]}")
    else:
        dump[k] = "MISSING"
        print(f"{k} = MISSING")

(ws.path / "param_dump_okane.json").write_text(json.dumps(dump, indent=2, ensure_ascii=False), encoding="utf-8")