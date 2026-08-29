from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")

ceiling = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "Opening ceiling assessment (Stage 3 architecture+formulation space, no molecular screening in "
        "this case). Levers assessed: electrode thickness (V2: 40/52 um), particle radius (V1: 2.0/2.5 um), "
        "electrolyte transport (V3: kappa 1.5 S/m, D 2.5e-10, t+ 0.35), porosity (V4: 0.42/0.35), cooling "
        "(V5: h 30), combined (V6). Single levers fail: best single retention 0.589 (V2), best single T_max "
        "340.0 K (V2), plating near-miss -0.0117 V (V2). Combined V6 MEETS ALL CRITERIA: capacity 3.078 Ah, "
        "retention_5c 0.978, T_max 324.9 K, anode min +0.0143 V (plating-free), power density 38.8 kW/kg, "
        "ED 380 Wh/kg. Conclusion: the architecture+formulation ceiling of the Chen2020 system is ABOVE the "
        "task objective -> no Stage-2 material-design escalation needed; proceed to round-3 refinement "
        "(fixed-point Q_nom, plating margin, cooling/electrolyte relaxation)."
    ),
}

append_entry(WS, ceiling)
print("ceiling assessment appended")
