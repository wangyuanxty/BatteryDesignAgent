import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
ws = CaseWorkspace("exp/t5_r1_singlemodel", "runs")

comparison_entry = {
    "action": "evaluate",
    "round": 3,
    "comparison": [
        {"name": "archH_transport", "metrics": {"energy_density_wh_kg": 528.3, "T_max_K": 332.91, "plated": False}, "verdict": "pass"},
        {"name": "archI_h50", "metrics": {"energy_density_wh_kg": 526.3, "T_max_K": 332.30, "plated": True}, "verdict": "fail"},
        {"name": "archJ_npUp", "metrics": {"energy_density_wh_kg": 540.4, "T_max_K": 335.27, "plated": False}, "verdict": "fail"},
        {"name": "archK_particles", "metrics": {"energy_density_wh_kg": 531.2, "T_max_K": 334.14, "plated": False}, "verdict": "fail"},
    ],
    "note": "R3 comparison: archH is the FIRST all-criteria PASS (ED 528.3, Tmax 332.91, no plating +0.0155 V) - stronger electrolyte bridge (sigma 3.5/D 1.2e-9/t+ 0.55) at h=40 solves both safety criteria with zero mass cost. h=50 already overcools (archI plating). R4 widens the 0.24 K Tmax margin.",
}

propose_entry = {
    "action": "propose",
    "round": 4,
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
                "Total heat transfer coefficient [W.m-2.K-1]": 45.0,
            },
            "name": "archL_h45",
            "role": "archH + h=45: split the difference between h=40 (Tmax 332.91, no plating) and h=50 (332.30, plating) to widen Tmax margin without losing anode margin",
        },
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
                "Positive particle radius [m]": 2.0e-6,
                "Negative particle radius [m]": 2.2e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archM_smallP",
            "role": "archH + particles 2.0/2.2 um: kinetic boost on top of strong transport - less activation heat, more anode margin",
        },
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
                "Positive particle radius [m]": 2.0e-6,
                "Negative particle radius [m]": 2.2e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 45.0,
            },
            "name": "archN_robust",
            "role": "archH + small particles + h=45: robustness candidate - combined thermal and kinetic margin",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 1e-5,
                "Positive electrode porosity": 0.40,
                "Negative electrode porosity": 0.20,
                "Electrolyte conductivity [S.m-1]": 3.5,
                "Electrolyte diffusivity [m2.s-1]": 1.2e-9,
                "Cation transference number": 0.55,
                "Positive particle radius [m]": 2.6e-6,
                "Negative particle radius [m]": 2.9e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archO_negPoro",
            "role": "archH + negative porosity 0.22->0.20: negative binds capacity -> +2.6% neg active = more Ah and energy; ED robustness probe (0.35 g mass cost)",
        },
    ],
    "llm_reason": (
        "archH passes with Tmax margin of only 0.24 K; R4 widens margins without touching the winning structure. "
        "archL/archN test intermediate cooling (h=45 between the measured 40/50 endpoints); archM/archN test small "
        "particles on top of strong transport; archO banks ED margin via the capacity-binding negative electrode. "
        "All values tool-consistent with R1-R3; electrolyte values remain formulation estimates."
    ),
}

for e in (comparison_entry, propose_entry):
    append_entry(ws, e)
print("comparison R3 + propose R4 written")
