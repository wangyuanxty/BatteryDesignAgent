import sys
from pathlib import Path

sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace(Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_flash"))

plan_update = {
    "action": "plan",
    "update": True,
    "reason": "three-strike (Rounds 3-5, 15+ configurations, same root cause): M4 'no lithium plating at 4C charge to 4.7 V cutoff' is structurally unpassable for the LNMO system with a real charge. Mechanism (finM/finN diagnostics): the charge is anode-capacity-limited (anode surface saturates sto_surf=1.0 at ~7-7.4 Ah, before the cathode empties), and at the 4.7 V cutoff anode_potential = U_pos(sto_surf)+eta_pos-4.7-phi_e(sep) ~ +0.02-0.20 V < 0 by construction because the LNMO OCP ceiling (4.706 V) equals the charge cutoff (4.7 V). Anode-side levers cancel (U_neg/eta_neg/stoich do not enter ap at the cutoff); cathode kinetics lever ineffective (mass-transfer-limited, eta_pos 0.015 V); electrolyte phi_e(sep) measured +0.196 V (11x ohmic estimate) would require sigma ~100 S/m (physically impossible for liquid electrolytes) to lift ap>=0; larger anodes just shift the termination to the protocol cutoff with the same negative ap. The only mechanically-passing configurations are degenerate 0-0.003 Ah charge legs (0.1-0.6 s) - vacuous passes rejected as protocol-gaming, not design claims.",
    "candidate_strategy": "Accept M4 as a protocol-level feasibility boundary (LNMO 4.7 V ceiling == cutoff interaction), documented honestly. Final design = best M1/M2/M3/M5 point: finN architecture (L_neg 120 um, eps_neg 0.65, sigma 20 S/m, t+ 0.9, D 1e-9, r_pos 2.0 um, r_neg 3 um, sep 8 um, CC 8/6 um, h 120 W/m2K) + EC diffusivity 2e-19 (LiF-rich SEI): M1 1172.1 Wh/L, M2 4.2475 V, M3 292.2 nm, M5 321.86 K, real 4C charge 6.97 Ah (M4 fail -0.2623 V, recorded as the boundary demonstration).",
    "budget_allocation": "Round 5 closed. Remaining budget -> DFN precision verification of the final design (task 5) + deliverables/render/verify (task 6).",
}

design = {
    "action": "design",
    "name": "finN-2e19",
    "round": 5,
    "role": "FINAL DESIGN (smartphone pouch, LNMO 4.7 V-class / graphite)",
    "struct": {"Separator thickness [m]": 8e-6, "Positive current collector thickness [m]": 8e-6, "Negative current collector thickness [m]": 6e-6, "Cation transference number": 0.9, "Electrolyte conductivity [S.m-1]": 20.0, "Electrolyte diffusivity [m2.s-1]": 1e-9, "Negative electrode thickness [m]": 1.2e-4, "Negative electrode active material volume fraction": 0.65, "Positive particle radius [m]": 2.0e-6, "Negative particle radius [m]": 3e-6, "EC diffusivity [m2.s-1]": 2e-19, "Total heat transfer coefficient [W.m-2.K-1]": 120},
    "evidence": {
        "M1 energy_density_wh_l": {"value": 1172.1, "threshold_min": 950, "verdict": "pass", "source": "cell/r5_finN_1c_calc.json"},
        "M2 midpoint_voltage_v": {"value": 4.2475, "threshold_min": 4.1, "verdict": "pass", "source": "cell/r5_finN_1c_calc.json"},
        "M3 sei_thickness_nm_end": {"value": 292.2, "threshold_max": 500, "verdict": "pass", "source": "cell/r5_finN2e19_aging.json"},
        "M4 plated": {"value": True, "threshold": False, "verdict": "fail", "source": "cell/r5_finN_4c.json (anode min -0.2623 V; real charge 6.97 Ah)", "boundary_note": "structurally unpassable with real charge - LNMO OCP ceiling 4.706 V == 4.7 V cutoff; see plan update"},
        "M5 T_max_K": {"value": 321.86, "threshold_max": 323.15, "verdict": "pass", "source": "cell/r5_finN_4c.json"},
        "capacity_ah_1c": {"value": 6.347, "source": "cell/r5_finN_1c_calc.json"},
        "charge_4C_ah": {"value": 6.97, "source": "cell/r5_finN_4c.json (1393 s @ 18 A)"},
    },
    "props_source": "architecture = design choice; electrolyte transport (sigma 20, t+ 0.9) = high-transference high-conductivity additive electrolyte estimate (domain experience, no precise source); eps_neg 0.65 = dense calendered graphite (aggressive but realizable); D_ec 2e-19 = LiF-rich SEI coating estimate (EC permeation block); h 120 = smartphone vapor-chamber + frame cooling estimate",
}

append_entry(ws, plan_update)
append_entry(ws, design)
print("plan update + final design appended")
