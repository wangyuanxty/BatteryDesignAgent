"""t9_r4 log setup: entry 0 criteria + plan + propose/funnel for rounds 1-3."""
from bda import store

ws = store.CaseWorkspace("t9_r4", root="runs/exp")

# --- Entry 0: criteria pre-registration (verbatim task thresholds) ---
entry0 = {
    "criteria": {
        "stage1": {
            "avg_voltage_v": {"min": 4.6},
            "charging_potential_v": {"max": 4.8},
        },
        "stage2": {
            "energy_density_wh_kg": {"min": 327.18},
        },
        "stage3": {
            "plated": False,
            "triggered": False,
            "sei_thickness_nm_end": {"max": 500.0},
        },
        "meta": {
            "case": "t9_r4",
            "task": "Grid-storage cell cathode on the Chen2020 NMC811/graphite profile; the cathode composition is the only free variable",
            "criteria_key_alignment": "stage1 key 'avg_voltage_v' matches the run-comp output field name (the task's 'computed average voltage'); threshold value 4.6 unchanged from the task text; 'charging_potential_v' matches the profile-script output field",
            "freedoms": "cathode composition only; electrolyte (EC/EMC + LiPF6), cell architecture (Chen2020 geometry), thermal management, and SEI kinetics are fixed",
            "mapping_rule": "constant OCP = computed average voltage; capacity = 0.9 x computed capacity; SEI kinetics = Chen2020 baseline k0",
            "ed_active_report": "ED_active = V x C x 0.9 (report value)",
            "catalogue_exclusion": "candidate must not be one of the 115 documented materials in runs/exp/known_set_comp/known_set_v3.json",
            "hull_exclusion": "computed point (V, C, stab) must lie outside the convex hull of the 102 known points (comp_envelope_check.py adjudication)",
            "family_constraint": "only six supported structure families (layered LiMO2, olivine LiMPO4, spinel LiM2O4, tavorite LiM(PO4)F, tavorite LiM(SO4)F, NASICON Li3M2(PO4)3); others unsupported (hard boundary)",
            "true_voltage_guard": "the 4.6 V window must hold beyond the screening proxy: experimental value, own QE computation (run-qe), or literature-consistent evidence; computed-only from an overestimate-prone family is not evidence",
            "charging_potential_source": "computed incremental potential into the top-of-charge state (x: 0.4 -> 0.3, same CHGNet machinery, profile script) + cell upper voltage cut-off 4.8 V",
            "protocol_note": "constant-OCP plateau discharge in the fixed cell is anode-limited (~5.1 Ah, LNMO.json precedent behavior); this is the fixed-cell discharge signature, labeled honestly",
            "start_stage": 2,
            "real_compute": True,
        },
    }
}
store.append_entry(ws, entry0)

# --- Plan entry (Stage 1) ---
plan = {
    "action": "plan",
    "objective_breakdown": (
        "stage1 (molecular): computed avg voltage >= 4.6 V (run-comp CHGNet); charging potential <= 4.8 V "
        "(anodic limit of fixed electrolyte, computed incremental profile); outside documented catalogue (115) and "
        "outside known hull (102 points); supported family only. stage2 (cell): ED >= 327.18 Wh/kg on 1C discharge "
        "(calc-energy contract convention) under the fixed mapping rule (constant OCP = V_avg, capacity = 0.9xC, "
        "SEI = Chen2020 k0); report ED_active = VxCx0.9. stage3 (safety/aging): no plating at 4C/45C, no "
        "thermal-runaway trigger, SEI <= 500 nm after 100x1C. Guard: true voltage >= 4.6 beyond the proxy."
    ),
    "candidate_strategy": (
        "Measured this session: baseline ED = 400.29 Wh/kg (tool) and family capacity bounds show only the "
        "layered LiMO2 family can clear ED 327.18 under the 0.9-capacity rule (non-layered ceiling ~322 Wh/kg "
        "even at V=4.8/C=128; LiNiPO4 at true 5.1 V gives ~317). So the candidate must be layered with computed "
        "V in [4.6, 4.8]. Round 1 probed TM-redox layered (Cu/Fe/Ni/Co/Mn/V): band 2.56-3.99 V - insufficient. "
        "Round 2 probed Cr mixes + d0/d10 O-redox layered: LiAlO2 4.598 V (2 mV short), LiGaO2 4.479, LiZnO2 "
        "4.492, LiScO2 4.298 - the d0/d10 line sits at the window edge; smaller d0 cation -> higher V "
        "(Al > Ga > Sc by ionic radius). Round 3 refines the B-Al d0 system (B3+ is the smallest d0 cation)."
    ),
    "budget_allocation": (
        "run-comp: 3 batches x 14 (done/queued) + profile script (8 states x finalists). "
        "run-pyamm/calc-energy/run-tr: ~10 runs. run-qe: finalist only, attempt within budget."
    ),
    "risk_and_fallback": (
        "R1: layered band provably below 4.6 -> contract infeasible (non-layered ED-infeasible by the capacity "
        "bounds) -> honest negative result with layer-by-layer questioning. R2: charging potential > 4.8 -> "
        "compositional adjustment or next candidate. R3: mapped-cell ED < 327.18 -> recheck mapping first. "
        "R4: 4C plating or TR -> verify nominal-capacity scaling; fixed architecture limits levers. "
        "R5: run-qe too slow -> recorded honestly; guard rests on literature-consistency evidence."
    ),
    "detail": "design_plan.md",
}
store.append_entry(ws, plan)

# --- Round 1: TM-redox layered sweep ---
propose1 = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {"name": "LiCuO2", "role": "Cu3+/2+ layered oxide, literature ~4.5-4.8 V class"},
        {"name": "LiFeO2", "role": "Fe3+/4+ layered, high-voltage d5 endpoint"},
        {"name": "CuNi55", "role": "Cu/Ni 50:50 layered mix"},
        {"name": "CuMn55", "role": "Cu/Mn 50:50 layered mix"},
        {"name": "CuFe55", "role": "Cu/Fe 50:50 layered mix"},
        {"name": "CuCo55", "role": "Cu/Co 50:50 layered mix"},
        {"name": "NiFe55", "role": "Ni/Fe 50:50 layered mix"},
        {"name": "CoFe55", "role": "Co/Fe 50:50 layered mix"},
        {"name": "FeMn55", "role": "Fe/Mn 50:50 layered mix"},
        {"name": "LiVO2", "role": "V3+/4+ layered control"},
        {"name": "CuAl91", "role": "Cu-rich with Al stabilizer"},
        {"name": "CuZr91", "role": "Cu-rich with Zr dopant"},
        {"name": "CuMn73", "role": "Cu-rich Mn mix"},
        {"name": "CuNi82", "role": "Cu-rich Ni mix"},
    ],
    "llm_reason": (
        "ED feasibility analysis (baseline ED measured 400.29 Wh/kg + family capacity bounds 0.9xCxM_am) shows "
        "only the layered family can clear 327.18 Wh/kg; the known layered band tops at 4.029 V (NiMnMA), so the "
        "window [4.6, 4.8] is empty in the hull. Round 1 maps the TM-redox layered voltage envelope: Cu (4.5-4.8 V "
        "class experimentally) and Fe (highest known layered computed 3.94) as the primary hypotheses, Ni/Co/Mn/V "
        "as controls."
    ),
}
store.append_entry(ws, propose1)

funnel1 = {
    "action": "funnel",
    "round": 1,
    "passed": 0,
    "rejected": 14,
    "disputed": 0,
    "detail": "All 14 below the 4.6 V window (band 2.56-3.99 V); best LiNi0.5Fe0.5O2 3.990, LiFeO2 3.943; Cu layered computes 3.5-3.8 (CHGNet prices Cu layered low).",
    "dispositions": [
        {"name": "LiCuO2", "status": "rejected", "reason": "3.707 V < 4.6"},
        {"name": "LiFeO2", "status": "rejected", "reason": "3.943 V < 4.6"},
        {"name": "CuNi55", "status": "rejected", "reason": "3.750 V < 4.6"},
        {"name": "CuMn55", "status": "rejected", "reason": "3.512 V < 4.6"},
        {"name": "CuFe55", "status": "rejected", "reason": "3.807 V < 4.6"},
        {"name": "CuCo55", "status": "rejected", "reason": "3.492 V < 4.6"},
        {"name": "NiFe55", "status": "rejected", "reason": "3.990 V < 4.6 (round max)"},
        {"name": "CoFe55", "status": "rejected", "reason": "3.682 V < 4.6"},
        {"name": "FeMn55", "status": "rejected", "reason": "3.342 V < 4.6"},
        {"name": "LiVO2", "status": "rejected", "reason": "2.564 V < 4.6"},
        {"name": "CuAl91", "status": "rejected", "reason": "3.693 V < 4.6"},
        {"name": "CuZr91", "status": "rejected", "reason": "3.722 V < 4.6"},
        {"name": "CuMn73", "status": "rejected", "reason": "3.615 V < 4.6"},
        {"name": "CuNi82", "status": "rejected", "reason": "3.670 V < 4.6"},
    ],
}
store.append_entry(ws, funnel1)

# --- Round 2: Cr mixes + d0/d10 O-redox layered ---
propose2 = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {"name": "LiScO2", "role": "d0 Sc3+ layered (O-redox on delithiation)"},
        {"name": "LiAlO2", "role": "d0 Al3+ layered (O-redox), lightest d0 cation"},
        {"name": "LiGaO2", "role": "d10 Ga3+ layered (O-redox)"},
        {"name": "LiZnO2", "role": "d10 Zn2+ layered (charge-unbalanced reference)"},
        {"name": "FeNi73", "role": "Fe-rich Ni mix, band-edge probe"},
        {"name": "FeNi37", "role": "Ni-rich Fe mix, band-edge probe"},
        {"name": "CrFe55", "role": "Cr/Fe mix (Cr tops known non-layered families)"},
        {"name": "CrNi55", "role": "Cr/Ni mix"},
        {"name": "CrCo55", "role": "Cr/Co mix"},
        {"name": "FeCo91", "role": "Fe-rich Co-doped"},
        {"name": "NiFe91", "role": "Ni-rich Fe-doped"},
        {"name": "FeNi91", "role": "Fe-rich Ni-doped"},
        {"name": "ZnNi55", "role": "Zn/Ni mix (d10 + redox)"},
        {"name": "ScFe55", "role": "Sc/Fe mix (d0 + redox)"},
    ],
    "llm_reason": (
        "Round 1: the TM-redox layered band caps at ~4.0 V (NiFe55 3.99; known LiNiO2 3.89) - no 3d redox reaches "
        "4.6. New hypothesis: d0/d10 cations (Sc/Al/Ga/Zn) cannot oxidize, so delithiation forces O oxidation - "
        "the Li2MnO3-class O-redox mechanism whose real-world activation plateau sits at 4.4-4.7 V. Also probe the "
        "Fe/Ni band edges and Cr mixes (Cr tops the known spinel/NASICON bands) for completeness of the envelope "
        "documentation."
    ),
}
store.append_entry(ws, propose2)

funnel2 = {
    "action": "funnel",
    "round": 2,
    "passed": 0,
    "rejected": 13,
    "disputed": 1,
    "detail": "d0/d10 O-redox line lands at the window edge: LiAlO2 4.598 V (2 mV short of 4.6, disputed as refinement anchor), LiZnO2 4.492, LiGaO2 4.479, LiScO2 4.298; all redox mixes 3.55-4.0. Smaller d0 cation -> higher V (Al > Ga > Sc).",
    "dispositions": [
        {"name": "LiScO2", "status": "rejected", "reason": "4.298 V < 4.6"},
        {"name": "LiAlO2", "status": "disputed", "reason": "4.598 V, 2 mV below window - refinement anchor (B doping direction)"},
        {"name": "LiGaO2", "status": "rejected", "reason": "4.479 V < 4.6"},
        {"name": "LiZnO2", "status": "rejected", "reason": "4.492 V < 4.6 (and Zn2+ charge-unbalanced on the M site)"},
        {"name": "FeNi73", "status": "rejected", "reason": "3.964 V < 4.6"},
        {"name": "FeNi37", "status": "rejected", "reason": "3.925 V < 4.6"},
        {"name": "CrFe55", "status": "rejected", "reason": "3.747 V < 4.6"},
        {"name": "CrNi55", "status": "rejected", "reason": "3.786 V < 4.6"},
        {"name": "CrCo55", "status": "rejected", "reason": "3.554 V < 4.6"},
        {"name": "FeCo91", "status": "rejected", "reason": "3.841 V < 4.6"},
        {"name": "NiFe91", "status": "rejected", "reason": "3.959 V < 4.6"},
        {"name": "FeNi91", "status": "rejected", "reason": "3.958 V < 4.6"},
        {"name": "ZnNi55", "status": "rejected", "reason": "4.247 V < 4.6"},
        {"name": "ScFe55", "status": "rejected", "reason": "3.999 V < 4.6"},
    ],
}
store.append_entry(ws, funnel2)

# --- Plan update: direction change to the d0 O-redox line ---
plan_update = {
    "action": "plan-update",
    "objective_breakdown": (
        "Direction change after round 2: the TM-redox layered band (2.5-4.0 V) cannot reach 4.6; the d0/d10 "
        "O-redox layered line (4.25-4.60 V) sits at the window edge with a clean ionic-radius trend "
        "(Al 4.598 > Zn 4.492 > Ga 4.479 > Sc 4.298). Round 3 probes the smallest d0 cation, B3+, via LiBO2 and "
        "the B-Al line, seeking >= 4.60 V. Charging-potential check (<= 4.8 V at the top-of-charge state) is the "
        "co-gating criterion for this chemistry."
    ),
    "candidate_strategy": "LiBO2 + B-Al gradient mixes + Ga/Sc controls (all charge-balanced M3+ d0/d10).",
    "budget_allocation": "batch 3 (14 candidates) + profile script on finalists; remaining budget unchanged.",
    "risk_and_fallback": (
        "If the B-Al line caps below 4.6: the layered family envelope is then documented at 2.5-4.6 V and the "
        "window is infeasible within the six supported families -> honest negative result with escalation "
        "questioning. If a candidate passes 4.6: immediately check the charging potential profile (<= 4.8 V) "
        "before any cell work."
    ),
    "detail": "design_plan.md",
}
store.append_entry(ws, plan_update)

# --- Round 3: B-Al d0 system ---
propose3 = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {"name": "LiBO2", "role": "smallest d0 cation B3+, O-redox layered"},
        {"name": "AlB55", "role": "Al/B 50:50"},
        {"name": "AlB73", "role": "Al-rich B-doped"},
        {"name": "AlB91", "role": "Al-rich B-doped (near LiAlO2)"},
        {"name": "BAl73", "role": "B-rich Al-doped"},
        {"name": "BAl91", "role": "B-rich Al-doped (near LiBO2)"},
        {"name": "AlB82", "role": "Al/B 80:20"},
        {"name": "AlB64", "role": "Al/B 60:40"},
        {"name": "AlB95", "role": "Al-rich B-doped (finest step)"},
        {"name": "GaAl55", "role": "Ga/Al control (expect ~4.54)"},
        {"name": "AlSc55", "role": "Al/Sc control (expect ~4.45)"},
        {"name": "BGa55", "role": "B/Ga mix"},
        {"name": "BSc55", "role": "B/Sc mix"},
        {"name": "GaAl91", "role": "Ga-rich Al-doped control"},
    ],
    "llm_reason": (
        "Round 2 funnel: LiAlO2 4.598 V is 2 mV under the window; the d0 line ranks by ionic radius "
        "(Al 0.535 A > Ga 0.62 > Sc 0.745 in V). B3+ (0.27 A) is the smallest, lightest d0 cation and is "
        "unexplored - LiBO2 and the B-Al gradient are the natural refinement; all compositions charge-balanced "
        "(M3+). Ga/Sc mixes serve as mixing-rule controls."
    ),
}
store.append_entry(ws, propose3)

print("log setup done")
