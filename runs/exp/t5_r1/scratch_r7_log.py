# -*- coding: utf-8 -*-
"""Append three-strike plan update + R7 proposal to log.jsonl."""
import sys
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t5_r1", root="runs")

plan_update = {
    "action": "plan",
    "update": True,
    "reason": (
        "Three-strike rule triggered: R4, R5, R6 all failed with the same single cause "
        "(anode surface potential at separator interface < 0 V during 4C charge), each round "
        "with transport levers (D_e, t+, sigma, eps_neg, sep) moving the gap -0.30 -> -0.016 V "
        "but saturating. Questioning conclusion from time-series localization: the minimum occurs "
        "at the END of the charge segment (final sample, monotonic slide from +0.188 V) - i.e. "
        "end-of-charge solid-phase diffusion overpotential at the anode particles, not a mid-charge "
        "electrolyte-depletion transient. With R_neg = 5.86 um and Ds = 3.3e-14 m2/s, diffusion "
        "time R^2/Ds ~ 1040 s vs ~800 s charge segment: the particle SURFACE concentration runs "
        "ahead of the bulk, U(c_surf) collapses toward 0 V, and residual kinetic + ohmic "
        "overpotentials push the surface potential below zero."
    ),
    "candidate_strategy": (
        "Pivot within Stage 3 to the untried solid-phase lever: negative particle radius reduction "
        "(2.0-3.5 um, high-power small-grain synthetic graphite class; smaller particles = shorter "
        "diffusion path + larger surface area -> lower diffusion and kinetic overpotentials). "
        "Platform stays R6D (aggressive electrolyte transport + slim cathode + N/P 1.40 + h 60). "
        "If R7 closes plating in both systems, proceed to final confirmation."
    ),
    "budget_allocation": (
        "R7: 4 candidates x 2 systems = 8 DFN runs. ED margin is huge (630 vs 500.94 target, "
        ">= 129 Wh/kg slack) so no ED risk from this lever; T_max expected to improve slightly "
        "(less polarization heat)."
    ),
}
append_entry(ws, plan_update)

propose = {
    "action": "propose",
    "round": 7,
    "candidates": [
        {
            "name": "R7A negR3.5um",
            "role": "R6D platform + Negative particle radius 5.86 -> 3.5 um (moderate step; diffusion time ~380 s < charge 800 s)",
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Positive electrode thickness [m]": 7.56e-05,
                "Negative electrode thickness [m]": 0.0001058,
                "Positive particle radius [m]": 2.61e-06,
                "Negative particle radius [m]": 3.5e-06,
                "Electrolyte conductivity [S.m-1]": 2.0,
                "Electrolyte diffusivity [m2.s-1]": 4.5e-10,
                "Cation transference number": 0.45,
                "Total heat transfer coefficient [W.m-2.K-1]": 60.0,
                "Negative electrode porosity": 0.45,
                "Separator thickness [m]": 8e-06,
                "Separator porosity": 0.55,
            },
        },
        {
            "name": "R7B negR2.61um",
            "role": "R6D + Negative particle radius 2.61 um (match cathode; diffusion time ~210 s, surface tracks bulk through 800 s charge)",
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Positive electrode thickness [m]": 7.56e-05,
                "Negative electrode thickness [m]": 0.0001058,
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
        },
        {
            "name": "R7C negR2.0um",
            "role": "R6D + Negative particle radius 2.0 um (aggressive ultrafine-graphite step; diffusion time ~120 s)",
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Positive electrode thickness [m]": 7.56e-05,
                "Negative electrode thickness [m]": 0.0001058,
                "Positive particle radius [m]": 2.61e-06,
                "Negative particle radius [m]": 2.0e-06,
                "Electrolyte conductivity [S.m-1]": 2.0,
                "Electrolyte diffusivity [m2.s-1]": 4.5e-10,
                "Cation transference number": 0.45,
                "Total heat transfer coefficient [W.m-2.K-1]": 60.0,
                "Negative electrode porosity": 0.45,
                "Separator thickness [m]": 8e-06,
                "Separator porosity": 0.55,
            },
        },
        {
            "name": "R7D negR2.61+sep6",
            "role": "R7B + separator 6 um (thin production-class separator; residual electrolyte ohmic term)",
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Positive electrode thickness [m]": 7.56e-05,
                "Negative electrode thickness [m]": 0.0001058,
                "Positive particle radius [m]": 2.61e-06,
                "Negative particle radius [m]": 2.61e-06,
                "Electrolyte conductivity [S.m-1]": 2.0,
                "Electrolyte diffusivity [m2.s-1]": 4.5e-10,
                "Cation transference number": 0.45,
                "Total heat transfer coefficient [W.m-2.K-1]": 60.0,
                "Negative electrode porosity": 0.45,
                "Separator thickness [m]": 6e-06,
                "Separator porosity": 0.55,
            },
        },
    ],
    "llm_reason": (
        "Three-strike questioning (R4-R6): dip localized at END of charge -> solid-phase diffusion "
        "bottleneck at anode particles (R=5.86um, Ds=3.3e-14 -> tau~1040s > 800s charge). "
        "R7 sweeps the untried negative-particle-radius lever (3.5/2.61/2.0 um; physically "
        "grounded: high-power small-grain graphite, also reduces cracking strain in OKane2022 "
        "direction) plus a separator-6um combo. Dual judgment both systems."
    ),
}
append_entry(ws, propose)
print("plan update + R7 propose appended")
