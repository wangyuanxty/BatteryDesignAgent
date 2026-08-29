# -*- coding: utf-8 -*-
"""Generate R2 variant params files (mechanical, capacity-preserving) and propose entry."""
import json

import pybamm
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t8_r2", "runs/exp")
cell = ws.path / "cell"

pv = pybamm.ParameterValues("Chen2020")
H0 = float(pv["Electrode height [m]"])
W0 = float(pv["Electrode width [m]"])
A0 = H0 * W0
Lp0 = float(pv["Positive electrode thickness [m]"])
Ln0 = float(pv["Negative electrode thickness [m]"])
AMVFp0 = float(pv["Positive electrode active material volume fraction"])

TPORT = {  # high-transport electrolyte formulation (all values: literature-bounded estimates)
    "Electrolyte diffusivity [m2.s-1]": 4.0e-10,
    "Cation transference number": 0.36,
    "Electrolyte conductivity [S.m-1]": 1.2,
}

VARIANTS = {}


def mk(name, struct):
    VARIANTS[name] = struct


# V_A: transport only, geometry = baseline
mk("VA", {"name": "V_A transport", "struct": dict(TPORT)})

# V_B: transport + positive porosity reservoir (binder 5%: eps 0.40 + AMVF 0.55),
#      Lp enlarged to preserve positive capacity
lv_b = Lp0 * AMVFp0 / 0.55
mk("VB", {"name": "V_B reservoir", "struct": dict(
    TPORT,
    **{
        "Positive electrode porosity": 0.40,
        "Positive electrode active material volume fraction": 0.55,
        "Positive electrode thickness [m]": lv_b,
    },
)})

# V_C: transport + thinner electrodes, area scaled up to preserve cell capacity (5 Ah)
fp = 60.0e-6 / Lp0
wp = W0 / fp
mk("VC", {"name": "V_C thin-loading", "struct": dict(
    TPORT,
    **{
        "Positive electrode thickness [m]": 60.0e-6,
        "Negative electrode thickness [m]": Ln0 * 60.0e-6 / Lp0,
        "Electrode width [m]": wp,
    },
)})

# V_D: V_C + thin separator + thin collectors
mk("VD", {"name": "V_D thin+inactive", "struct": dict(
    TPORT,
    **{
        "Positive electrode thickness [m]": 60.0e-6,
        "Negative electrode thickness [m]": Ln0 * 60.0e-6 / Lp0,
        "Electrode width [m]": wp,
        "Separator thickness [m]": 9.0e-6,
        "Positive current collector thickness [m]": 8.0e-6,
        "Negative current collector thickness [m]": 6.0e-6,
    },
)})

for key, v in VARIANTS.items():
    path = cell / f"params_r2_{key}.json"
    path.write_text(json.dumps(v["struct"], ensure_ascii=False, indent=2), encoding="utf-8")
    print(key, "->", path.name)

propose = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "name": "V_A transport",
            "role": "electrolyte formulation: D=4.0e-10 m2/s (const), t+=0.36 (Valoen&Reimers 2005 JES 152 A882), sigma=1.2 S/m (Nyman2008-class blend; estimate) - isolate the formulation gain on 5C salt-depletion",
            "struct": VARIANTS["VA"]["struct"],
        },
        {
            "name": "V_B reservoir",
            "role": "V_A + positive porosity 0.40 (AMVF 0.55, 5% binder), positive thickness 91.4 um to preserve capacity - larger electrolyte reservoir where depletion occurs",
            "struct": VARIANTS["VB"]["struct"],
        },
        {
            "name": "V_C thin-loading",
            "role": "V_A + positive 60 um / negative 67.6 um, width 1.58->1.99 m so capacity stays 5 Ah - lower areal loading reduces 5C areal current density",
            "struct": VARIANTS["VC"]["struct"],
        },
        {
            "name": "V_D thin+inactive",
            "role": "V_C + separator 9 um + collectors 8/6 um - transport + inactive-mass trim preview of the full design direction",
            "struct": VARIANTS["VD"]["struct"],
        },
    ],
    "llm_reason": "R1 diagnosis: 5C failure = positive-electrode electrolyte salt depletion (c_e->0 within ~62 s, +0.81 V positive activation overpotential); ED gap 45.4 Wh/kg and 4C-charge plating share the same transport root cause. R2 explores the three mass-neutral-to-ED levers (D/t+/sigma, porosity reservoir, loading reduction via area trade) one axis each plus a combined package; all variants capacity-preserving (Qnom 5 Ah) so 5C current is comparable. Values: t+ 0.36 literature (Valoen & Reimers); D/sigma high-transport-blend estimates (bounded by Nyman2008/Valoen measurements) - marked estimate, not simulation output.",
}

append_entry(ws, propose)
# also write params-notes for the record
notes = {
    "round": 2,
    "method": "all variants share Nominal cell capacity 5 Ah; V_B/V_C geometry chosen so positive-electrode capacity (cmax*AMVF*L*A) is preserved vs baseline",
    "area_va_vb_m2": round(A0, 6),
    "area_vc_vd_m2": round(H0 * wp, 6),
    "sources": "t+=0.36 Valoen&Reimers JES 152 A882 (2005); D=4.0e-10 const = high-transport blend estimate (Nyman2008 peak 4.1e-10 dilute); sigma=1.2 S/m = blend estimate (Nyman2008/Valoen ~1.0-1.1 at 1M)",
}
cell.joinpath("params_r2_notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
print("propose R2 written;", len(VARIANTS), "variants")