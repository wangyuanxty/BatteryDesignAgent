import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
ws = CaseWorkspace("exp/t5_r1_singlemodel", "runs")

comparison_entry = {
    "action": "evaluate",
    "round": 1,
    "comparison": [
        {"name": "baseline_Chen2020", "metrics": {"energy_density_wh_kg": 400.8, "T_max_K": 354.29, "plated": True}, "verdict": "fail"},
        {"name": "sys_OKane2022", "metrics": {"energy_density_wh_kg": 405.6, "T_max_K": 367.42, "plated": False}, "verdict": "fail"},
        {"name": "archA_EDmax", "metrics": {"energy_density_wh_kg": 468.9, "T_max_K": 370.36, "plated": False}, "verdict": "fail"},
        {"name": "archB_4Csafe", "metrics": {"energy_density_wh_kg": 417.6, "T_max_K": 334.22, "plated": False}, "verdict": "fail"},
        {"name": "archC_thin", "metrics": {"energy_density_wh_kg": 377.6, "T_max_K": 362.47, "plated": False}, "verdict": "fail"},
    ],
    "note": "R1 cross-candidate comparison: mechanical values taken from the per-candidate evaluate entries above (same output files). All five fail overall; archA wins ED (468.9), archB wins safety (Tmax 334.22, no plating).",
}

ceiling_entry = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "detail": (
        "Opening ceiling assessment (R1 data, NMC811/graphite on OKane2022 base). Levers assessed: "
        "(1) CC/separator thinning + porosity cut (archA): mass 43.45->37.50 g, ED 400.8/405.6->468.9, capacity "
        "unchanged (4.972 Ah) -> cell sits exactly where material limit and 2.5 V cut-off coincide; "
        "(2) electrode thinning (archC): -15% thickness -> -15.7% capacity -> material-limited, rejected; "
        "(3) transport bridge sigma 2.2 S/m / D 7.5e-10 / t+ 0.45 + halved particles (archB): energy "
        "17.63->18.15 Wh (+3%), Tmax 334.22 K at h=40. Estimated architecture ceiling: mass floor ~33.5 g IF "
        "positive-porosity rebalance (pos 0.28->0.40) and N/P trim (neg thickness -8%) do not cost capacity "
        "(which electrode binds at 2.5 V is unresolved - probed in R2); energy ceiling ~18.3 Wh -> ED ceiling "
        "~545 Wh/kg, above the 500.94 target. Fallback: if capacity drops with pos-mass trim -> architecture "
        "ceiling ~490 -> gap attributed to material properties -> Stage 2 escalation (high-capacity cathode "
        "composition via run-comp / LNMO 4.7 V system). Gap to objective from archA: +32.0 Wh/kg needed."
    ),
}

propose_entry = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 1e-5,
                "Positive electrode porosity": 0.28,
                "Negative electrode porosity": 0.22,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 7.5e-10,
                "Cation transference number": 0.45,
                "Positive particle radius [m]": 2.6e-6,
                "Negative particle radius [m]": 2.9e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archD_combine",
            "role": "combine R1 winners: archA mass cuts + archB transport/particles/cooling on OKane2022",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 1e-5,
                "Positive electrode porosity": 0.40,
                "Negative electrode porosity": 0.22,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 7.5e-10,
                "Cation transference number": 0.45,
                "Positive particle radius [m]": 2.6e-6,
                "Negative particle radius [m]": 2.9e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archE_posPoro",
            "role": "archD + positive porosity 0.28->0.40 (pos active mass -17%, -3.0 g): tests whether positive electrode has capacity slack at 2.5 V cut-off",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 1e-5,
                "Positive electrode porosity": 0.28,
                "Negative electrode porosity": 0.22,
                "Negative electrode thickness [m]": 7.84e-5,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 7.5e-10,
                "Cation transference number": 0.45,
                "Positive particle radius [m]": 2.6e-6,
                "Negative particle radius [m]": 2.9e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archF_npTrim",
            "role": "archD + negative thickness -8% (N/P 1.14->1.05): tests negative capacity slack; frees 0.9 g if capacity holds",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 1e-5,
                "Positive electrode porosity": 0.28,
                "Negative electrode porosity": 0.22,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 7.5e-10,
                "Cation transference number": 0.45,
                "Positive particle radius [m]": 2.6e-6,
                "Negative particle radius [m]": 2.9e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 60.0,
            },
            "name": "archG_cool60",
            "role": "archD + cooling h 40->60: Tmax margin probe (watch plating margin vs temperature trade-off)",
        },
    ],
    "llm_reason": (
        "R1 shows mass cuts (archA) and transport bridge (archB) are the two effective levers; R2 combines them "
        "(archD) and attributes remaining ED gap by orthogonal probes: pos porosity up (archE, tests positive "
        "slack), N/P trim (archF, tests negative slack), h=60 (archG, Tmax margin). All transport/electrolyte "
        "values remain domain estimates (marked estimate). If archE/archF capacity holds -> architecture ceiling "
        ">= ~500; if not -> Stage 2 material escalation next round (ceiling_escalation ON)."
    ),
}

for e in (comparison_entry, ceiling_entry, propose_entry):
    append_entry(ws, e)
print("comparison + ceiling + propose(round 2) written")
