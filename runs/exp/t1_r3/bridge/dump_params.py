# -*- coding: utf-8 -*-
"""t1_r3 parameter dump — verify the deterministic base-set anchor (§1.5) before first run.

Dumps the parameter keys that matter for the case (architecture / thermal / transport /
cut-offs / plating / aging) for Chen2020, OKane2022, and the LNMO composite
(Chen2020 + data/LNMO.json overrides). Written to bridge/base_dump.json (own workspace).
"""
import json
import sys
from pathlib import Path

import pybamm

from bda.simulators.lnmo_parameters import lnmo_ocp

KEYS = [
    "Nominal cell capacity [A.h]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Separator thickness [m]",
    "Separator porosity",
    "Separator density [kg.m-3]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode maximum concentration [mol.m-3]",
    "Negative electrode maximum concentration [mol.m-3]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Positive electrode OCP [V]",
    "Positive electrode OCP [V] (from stoich)",
    "SEI kinetic rate constant [m.s-1]",
    "Initial SEI thickness [m]",
    "Positive electrode cracking rate",
    "Negative electrode cracking rate",
    "Typical plated lithium concentration [mol.m-3]",
    "Exchange-current density for plating [A.m-2]",
    "Reference temperature [K]",
]


def dump_set(name: str, pv: pybamm.ParameterValues) -> dict:
    out = {}
    for k in KEYS:
        try:
            v = pv[k]
            if callable(v):
                out[k] = f"<function {getattr(v, '__name__', '?')}>"
            elif isinstance(v, (str, int, float, bool, list)):
                out[k] = v
            else:
                out[k] = str(v)
        except KeyError:
            out[k] = None
    return out


def main() -> int:
    result = {}

    pv_chen = pybamm.ParameterValues("Chen2020")
    result["Chen2020"] = dump_set("Chen2020", pv_chen)

    pv_okane = pybamm.ParameterValues("OKane2022")
    result["OKane2022"] = dump_set("OKane2022", pv_okane)

    lnmo_path = (
        Path(__file__).resolve().parents[4]
        / ".claude" / "skills" / "virtual-battery-factory"
        / "scripts" / "bda" / "simulators" / "data" / "LNMO.json"
    )
    extra = json.loads(lnmo_path.read_text(encoding="utf-8"))
    for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
        if isinstance(extra.get(key), str):
            extra[key] = lnmo_ocp
    pv_lnmo = pybamm.ParameterValues("Chen2020")
    pv_lnmo.update(extra, check_already_exists=False)
    result["LNMO_composite"] = dump_set("LNMO", pv_lnmo)

    out = Path(__file__).resolve().parent / "base_dump.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"written → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
