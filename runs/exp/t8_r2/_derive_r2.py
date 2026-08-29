# -*- coding: utf-8 -*-
"""Derive R2 retention files + write ceiling-assessment funnel entry + R2 batch evaluate inputs."""
import json

from bda.store import CaseWorkspace, append_entry

ROOT = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t8_r2"
ws = CaseWorkspace("t8_r2", "runs/exp")
cell = ws.path / "cell"

derived = {}
for v in ["VA", "VB", "VC", "VD"]:
    d1 = json.load(open(cell / f"r2_{v}_1c_dfn.json", encoding="utf-8"))
    d5 = json.load(open(cell / f"r2_{v}_5c_dfn.json", encoding="utf-8"))
    c1, c5 = d1["capacity_ah"], d5["capacity_ah"]
    rec = {
        "retention_5c": c5 / c1,
        "capacity_ah_1c": c1,
        "capacity_ah_5c": c5,
        "note": "retention_5c = capacity_ah_5c / capacity_ah_1c (same-parameter DFN runs; mechanical division)",
    }
    (cell / f"r2_{v}_retention.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    derived[v] = rec
    print(v, "retention =", round(rec["retention_5c"], 4))

# Ceiling assessment (Stage-3 opening, now quantitative)
ceiling = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "ceiling_assessment": {
        "levers_assessed": [
            "current collectors 16/12 -> 8/6 um", "separator 12 -> 9 um",
            "positive porosity 0.335 -> 0.40 (AMVF 0.55, 5% binder)", "electrode thickness 75.6/85.2 -> 60/67.6 um (area-scaled, capacity-preserving)",
            "electrolyte D 4.0e-10 m2/s, t+ 0.36, sigma 1.2 S/m (formulation)",
        ],
        "findings": {
            "ed_ceiling_nmc811_graphite_envelope": "467.0 Wh/kg measured (V_D, not yet individually ED-optimized) > objective 446.18 -> ED is inside the existing-chemistry envelope; no material escalation needed for ED",
            "retention_response": "0.087 (baseline) -> 0.676 (V_A transport only) -> 0.722 plateau (V_B/V_C/V_D); electrolyte salt depletion resolved (c_e positive side 0 -> 355 mol/m3 at 5C), limiter moved to positive solid-phase surface depletion (pos particle stoich 0.312 at separator face at t=515 s; tau_diff~6812 s >> 720 s)",
            "mass_response": "43.5 g baseline -> 37.7 g (V_D) <= 40 g cap satisfied via collector/separator trim",
        },
        "escalation_decision": "ceiling_escalation assessed NOT fired: objective within architecture+formulation reach; retention binding limit = positive solid-diffusion surface depletion addressed via allowed microstructure lever (particle radius) in R3, not an excluded-lever dead end",
        "data_sources": ["cell/r2_VD_energy.json", "cell/r2_VA_energy.json", "_diag_vd.py run (scratch diagnostics of r2_VD 5C state)"],
    },
    "detail": "Stage-3 opening ceiling assessment; system switch to OKane2022 evaluated and discounted (identical cell geometry/densities to Chen2020 -> negligible ED lever at this fidelity)",
}
append_entry(ws, ceiling)
print("ceiling assessment written")