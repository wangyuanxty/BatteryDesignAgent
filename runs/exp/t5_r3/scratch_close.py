"""Closing entries: endorse (honest skip) + final (achieved)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r3", "runs/exp")

append_entry(ws, {
    "action": "endorse",
    "skipped": True,
    "reason": "real_compute=false",
    "note": (
        "No true DFT/MD endorsement run (run-orca/run-md forbidden inside funnel; real_compute "
        "defaults false and was not enabled). Finalists endorsed at full-order DFN precision "
        "(model_used=DFN, no fallback) instead; no fabricated first-principles values."
    ),
})

append_entry(ws, {
    "action": "final",
    "recommendation": (
        "PRIMARY: Y4 (params_y4.json) — NMC811/graphite (Chen2020 base) pouch, 178.8 um stack: "
        "CC+ Al 6um / CC- Cu 5um / sep 7um / R_p 3um / R_n 3um, electrolyte sigma 5.0 S/m, "
        "t+ 0.6, D_e 9e-10 m2/s, h=26 W/m2K with 0.01062 m2 double-sided cooling. "
        "DFN-verified: ED 535.72 Wh/kg vs >=500.94, T_max 327.60 K vs <=333.15, "
        "min anode potential +0.0200 V (no plating) — r6_y4_energy_dfn.json + r6_y4_4c_dfn.json. "
        "4C CC charge window: 0->69% SOC (3.48 Ah) in 626 s at 20 A before 4.2 V cut-off "
        "(24x the baseline 26 s clamp); CV tail not simulated (current decays, plating risk "
        "monotonically decreases — domain reasoning, not simulated claim). "
        "ALTERNATE (supply-friendly): Y3 (Al 8um / sep 9um / standard transport t+0.5 D_e6e-10): "
        "ED 526.24 Wh/kg, T_max 329.38 K, min_ap +0.0162 V — DFN-verified pass, comfortable "
        "for foil supply whereas Y4's 5-6 um foils are aggressive."
    ),
    "verdict": "achieved",
    "no_escalation": (
        "No three-strike escalation triggered: per-round failure causes differed "
        "(r2 salt-transport limit -> r3/r4 thermal + honest-true-4C rebuild + r5 kinetic margin "
        "via warmth/anode-nanoparticles) — diagnosis-driven fallback, not blind retry. "
        "No Stage-2 material escalation needed: opening ceiling assessment conclusion held — "
        "architecture + transport formulation + thermal management suffice for all three "
        "contract criteria; proven by rounds 5-6 passes, not assumed."
    ),
    "self_check": (
        "7-failure-mode scan before closing: (1) no failure repackaged (W3 r3 mechanical pass "
        "later overturned by r4 honesty probes nominal6.5/6.0 — recorded in r4 batch notes); "
        "(2) every conclusion-grade value sourced to rN_*.json:key via mechanical log-evaluate; "
        "(3) no shortcut dependence (4C_45C + plating protocol — the harsh case — evaluated "
        "every round; 1C ED at 298.15 K per contract); (4) no bug-as-discovery (OKane2022 SiOx "
        "expectation discrepancy recorded as observation, not used); (5) entry-0 thresholds "
        "unmodified since written (contract intact); (6) units mechanical (333.15 K = 60 C; "
        "ED = calc-energy contract formula, electrolyte excluded); (7) no early lock-in "
        "(W3 pass overturned; Y1's thin +0.0088 V margin not promoted; DFN re-verification "
        "instead of assuming SPMe sufficiency)."
    ),
    "finalists": [
        {"name": "Y4", "params": "cell/params_y4.json", "ed_wh_kg": 535.72,
         "t_max_k": 327.60, "min_ap_v": 0.0200, "source": "cell/r6_y4_energy_dfn.json,cell/r6_y4_4c_dfn.json"},
        {"name": "Y3", "params": "cell/params_y3.json", "ed_wh_kg": 526.24,
         "t_max_k": 329.38, "min_ap_v": 0.0162, "source": "cell/r6_y3_energy_dfn.json,cell/r6_y3_4c_dfn.json"},
    ],
})