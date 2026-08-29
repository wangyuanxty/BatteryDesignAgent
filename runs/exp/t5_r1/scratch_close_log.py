# -*- coding: utf-8 -*-
"""Closing entries: endorse (real_compute=false honest skip) + final (verdict achieved, escalation record)."""
import sys
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t5_r1", root="runs")

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": (
        "real_compute=false (protocol default; task did not request true DFT/MD endorsement). "
        "Stage 5 run-orca/run-qe/run-md true-compute endorsement is skipped honestly; no "
        "first-principles values are claimed. All conclusion-grade numbers in this case come "
        "from tool outputs: bda run-pyamm (DFN, Chen2020/OKane2022) + bda calc-energy + "
        "bda log-evaluate. Molecular-scale levers used here (electrolyte transport formulation "
        "sigma/D_e/t+, negative particle radius 2.61 um) were screened at the continuum "
        "parameter-bridge level only."
    ),
}
append_entry(ws, endorse)

final = {
    "action": "final",
    "verdict": "achieved",
    "recommendation": (
        "Winning design R7B (bridge/r7b_negR261.json), validated under BOTH Chen2020 and "
        "OKane2022 (dual judgment): NMC811/graphite(-SiOx) pouch cell, Al foil 8 um / Cu foil "
        "6 um, positive electrode 75.6 um, negative electrode 105.8 um (N/P 1.40), both particle "
        "radii 2.61 um, electrolyte sigma 2.0 S/m / D_e 4.5e-10 m2/s / t+ 0.45 (formulation "
        "overrides, aggressive upper-bound estimates), negative porosity 0.45, separator 8 um / "
        "porosity 0.55, total heat transfer coefficient h = 60 W/m2/K (immersion-class liquid "
        "cooling). Measured (DFN, tool outputs): Chen2020 -> ED 642.098 Wh/kg >= 500.94, "
        "T_max 326.829 K <= 333.15 K, anode surface potential min +0.01826 V (no plating); "
        "OKane2022 -> ED 641.118 Wh/kg, T_max 328.189 K, anode min +0.01798 V (no plating). "
        "4C protocol = 1C discharge to v_min then 20 A CC charge to v_max at 45 C ambient, "
        "per contract. Honest caveats: (1) charge-capacity key in 4C outputs is under-reported "
        "5x by a pybamm_runner library bug (t*C_rate/3600 missing the 5 Ah nominal factor); "
        "it does not affect the stage3 judgments (plated/T_max), physical charge acceptance "
        "~4.7-5.0 Ah computed separately; (2) electrolyte transport overrides are literature-"
        "upper-bound estimates (estimate-flagged in proposals), not measured formulations; "
        "(3) real_compute=false -> no first-principles endorsement (see endorse entry)."
    ),
    "escalation": {
        "rule": "three-strike",
        "strikes": [
            {"round": 4, "candidate": "R4D +neg porosity 0.35", "failed metric": "plated=true (anode min -0.04867/-0.04783 V, Chen/OKane)"},
            {"round": 5, "candidate": "R5D +diffusivity 4.5e-10", "failed metric": "plated=true (anode min -0.02388/-0.02046 V, Chen/OKane)"},
            {"round": 6, "candidate": "R6D +t+ 0.45", "failed metric": "plated=true (anode min -0.01904/-0.01594 V, Chen/OKane)"},
        ],
        "questions": [
            {
                "assumption": "model/system: is a plating-free 4C charge physically reachable for this NMC811/graphite(-SiOx) system?",
                "conclusion": (
                    "Yes. Transport-lever response was monotonic (gap -0.1299 V -> -0.0159 V over R4-R6) and "
                    "time-series localization showed the minimum at the END of the charge segment (final sample; "
                    "monotonic slide from +0.188 V) - an end-of-charge solid-phase diffusion overpotential at the "
                    "5.86 um anode particles (tau = R^2/Ds ~ 1040 s vs ~800 s charge). The solid-phase lever had "
                    "not been used; the system itself is reachable."
                ),
                "why continue/stop": "continue: direction change to negative particle radius (still Stage 3, same system).",
            },
            {
                "assumption": "task boundary: is negative particle size inside the declared degree-of-freedom boundary?",
                "conclusion": (
                    "Yes. Entry 0 meta.freedoms declares cell architecture adjustable and explicitly lists "
                    "particle size as the corresponding lever; no boundary violation, no task-text restriction "
                    "was overridden."
                ),
                "why continue/stop": "continue within the recorded boundary.",
            },
            {
                "assumption": "metric: is the objective physically reachable within the given boundary?",
                "conclusion": (
                    "Yes - R7 with negative particle radius 2.61 um achieves plated=false under both systems "
                    "with >= +18 mV margin (Chen +0.01826 V, OKane +0.01798 V), ED 642.1/641.1 Wh/kg, "
                    "T_max 326.8/328.2 K. No threshold relaxation: entry 0 contract untouched."
                ),
                "why continue/stop": "continue to achievement; close as achieved.",
            },
        ],
        "decision": "continue with direction change (executed in R7: negative particle radius 5.86 -> 2.61 um) - succeeded.",
    },
    "final_design": {
        "params": {
            "Positive current collector thickness [m]": 8e-06,
            "Negative current collector thickness [m]": 6e-06,
            "Positive electrode thickness [m]": 7.56e-05,
            "Negative electrode thickness [m]": 1.058e-04,
            "Positive particle radius [m]": 2.61e-06,
            "Negative particle radius [m]": 2.61e-06,
            "Electrolyte conductivity [S.m-1]": 2.0,
            "Electrolyte diffusivity [m2.s-1]": 4.5e-10,
            "Cation transference number": 0.45,
            "Total heat transfer coefficient [W.m-2.K-1]": 60.0,
            "Negative electrode porosity": 0.45,
            "Separator thickness [m]": 8e-06,
            "Separator porosity": 0.55,
        },
        "bridge": "bridge/r7b_negR261.json",
    },
    "dual_judgment": {
        "Chen2020": {
            "energy_density_wh_kg": 642.0982441223834,
            "T_max_K": 326.82900164098754,
            "anode_min_v": 0.01826,
            "plated": False,
            "sources": ["cell/r7b_chen_energy.json", "cell/r7b_chen_4c_dfn.json"],
        },
        "OKane2022": {
            "energy_density_wh_kg": 641.1175848865234,
            "T_max_K": 328.18866882740235,
            "anode_min_v": 0.01798,
            "plated": False,
            "sources": ["cell/r7b_okane_energy.json", "cell/r7b_okane_4c_dfn.json"],
        },
        "rule": "final design must pass 4C under both parameter systems (self-imposed conservative rule, recorded in plan).",
    },
    "known_tool_issues": (
        "pybamm_runner charge capacity_ah = t*C_rate/3600 misses the 5 Ah nominal-current factor "
        "(4C runs report ~0.9 Ah while physical charge acceptance is ~4.7-5.0 Ah); does not affect "
        "stage3 judgment (plated from anode_potential_v, T_max from lumped thermal). Recorded "
        "honestly in R5-R7 evaluate notes; do not cite 4C capacity_ah as a design metric."
    ),
}
append_entry(ws, final)
print("endorse + final appended")
