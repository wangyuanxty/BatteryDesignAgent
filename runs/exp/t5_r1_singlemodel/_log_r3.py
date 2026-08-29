import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
ws = CaseWorkspace("exp/t5_r1_singlemodel", "runs")

comparison_entry = {
    "action": "evaluate",
    "round": 2,
    "comparison": [
        {"name": "archD_combine", "metrics": {"energy_density_wh_kg": 484.9, "T_max_K": 334.73, "plated": False}, "verdict": "fail"},
        {"name": "archE_posPoro", "metrics": {"energy_density_wh_kg": 528.1, "T_max_K": 335.20, "plated": False}, "verdict": "fail"},
        {"name": "archF_npTrim", "metrics": {"energy_density_wh_kg": 460.6, "T_max_K": 334.64, "plated": False}, "verdict": "fail"},
        {"name": "archG_cool60", "metrics": {"energy_density_wh_kg": 484.7, "T_max_K": 329.89, "plated": True}, "verdict": "fail"},
    ],
    "note": "R2 comparison: archE is the first ED passer (528.1 Wh/kg, +27.2 margin) and passes plating; Tmax is the only unmet criterion (335.20 vs 333.15, 2.05 K over at h=40). archF proves negative electrode binds capacity (N/P trim rejected). archG proves h=60 overcools -> plating (cooling vs plating trade-off).",
}

propose_entry = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 1e-5,
                "Positive electrode porosity": 0.40,
                "Negative electrode porosity": 0.22,
                "Electrolyte conductivity [S.m-1]": 3.5,
                "Electrolyte diffusivity [m2.s-1]": 1.2e-9,
                "Cation transference number": 0.55,
                "Positive particle radius [m]": 2.6e-6,
                "Negative particle radius [m]": 2.9e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archH_transport",
            "role": "archE + stronger electrolyte bridge (sigma 3.5 S/m, D 1.2e-9, t+ 0.55): less ohmic heat (Tmax down) and better anode margin, zero mass cost",
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
                "Total heat transfer coefficient [W.m-2.K-1]": 50.0,
            },
            "name": "archI_h50",
            "role": "archE + cooling h=50: thermal middle ground between h=40 (335.20 K, no plating) and h=60 (329.89 K, plating)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 1e-5,
                "Positive electrode porosity": 0.40,
                "Negative electrode porosity": 0.22,
                "Negative electrode thickness [m]": 8.9e-5,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 7.5e-10,
                "Cation transference number": 0.45,
                "Positive particle radius [m]": 2.6e-6,
                "Negative particle radius [m]": 2.9e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archJ_npUp",
            "role": "archE + negative thickness +4.5% (N/P 1.19): neg is capacity-binding -> more neg active = more Ah and higher anode potential at charge end (plating margin), +0.5 g mass cost",
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
                "Positive particle radius [m]": 2.0e-6,
                "Negative particle radius [m]": 2.2e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archK_particles",
            "role": "archE + particle radii 2.0/2.2 um: faster solid-phase kinetics -> less activation/kinetic heat and less negative surface dip",
        },
    ],
    "llm_reason": (
        "archE passes ED with 27 Wh/kg margin; Tmax (335.20 vs 333.15) is the only unmet criterion and the plating "
        "margin (+0.0021 V) is too thin. R3 probes four orthogonal safety levers on top of archE: stronger transport "
        "bridge (archH, sigma 3.5/D 1.2e-9/t+ 0.55 - formulation estimates), intermediate cooling (archI h=50 - "
        "the h=40/60 endpoints bracket the target), N/P up (archJ - neg binds capacity, so more neg adds Ah and "
        "lifts anode potential), smaller particles (archK). Winners combine in R4."
    ),
}

for e in (comparison_entry, propose_entry):
    append_entry(ws, e)
print("comparison R2 + propose R3 written")
