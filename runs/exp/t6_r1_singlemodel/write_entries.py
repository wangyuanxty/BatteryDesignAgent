"""Write log.jsonl entry 0 (criteria), plan entry, and round-1 propose entry (t6_r1_singlemodel)."""
import json

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_singlemodel", "runs/exp")

LNMO_BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

entry0 = {
    "criteria": {
        "stage1": {
            # funnel_voting OFF (ablation, task text): run-mlp(mace) only; hard elimination lines.
            # mace lines: converged must be true; energy_ev <= 0.0 eV.
            # xtb HOMO line (max_homo_ev) unavailable: xtb not run under this ablation.
            "max_energy_ev": {"max": 0.0},
        },
        "stage2": {
            "energy_density_wh_l": {"min": 950.0},
            "midpoint_voltage_v": {"min": 4.1},
            "sei_thickness_nm_end": {"max": 500.0},
        },
        "stage3": {
            "T_max_K": {"max": 323.15},
            "plated": False,
        },
        "meta": {
            "case_id": "t6_r1_singlemodel",
            "task": "smartphone battery design: volumetric energy density >= 950 Wh/L; 4C fast charge (no lithium plating); max temperature <= 50 degC; anode SEI thickness <= 500 nm after 100 cycles; voltage plateau >= 4.1 V",
            "start_stage": 2,
            "start_stage_reason": "plateau >= 4.1 V exceeds NMC811-class ceiling (midpoint ~3.6 V): objective forces a material-level system decision (high-voltage LNMO system candidate) -> Stage 2",
            "base_params": "data/LNMO.json (Chen2020 base + LNMO 4.7 V-class positive overrides; negative/SEI/geometry/thermal inherited from Chen2020)",
            "real_compute": False,
            "ablation": {
                "funnel_voting": "OFF (task text): molecular screening = run-mlp(mace) only; hard elimination lines apply (mace converged/energy); xtb HOMO line unavailable; no three-model voting; no disputed concept",
                "exploration_force": "ON (default)",
                "ceiling_escalation": "ON (default)",
            },
            "freedoms": {
                "electrode_system": "adjustable (widest interpretation; task text silent)",
                "electrolyte_formulation": "adjustable (widest interpretation; t1_r1 lesson: silent text -> widest)",
                "electrode_modification": "adjustable (coating via SEI kinetic rate constant)",
                "cell_architecture": "adjustable (thickness/porosity/N-P/separator/current collector/particle size)",
                "thermal_management": "adjustable (Total heat transfer coefficient)",
            },
            "parse_notes": {
                "plateau_metric": "midpoint_voltage_v from calc-energy (voltage at discharge-time midpoint; plateau approximation)",
                "T_max_metric": "T_max_K from 4C_charge_45C protocol (4C charge after 1C discharge, 318.15 K ambient, lumped thermal)",
                "SEI_metric": "sei_thickness_nm_end from aging_1C_100cyc (100 cycles 1C CC, isothermal, SEI ec-reaction-limited)",
                "ED_metric": "energy_density_wh_l from calc-energy (contract: stack volume = sum of layer thickness x area, electrolyte excluded)",
                "plating_metric": "plated derived from anode_potential_v series min < 0 (4C_charge_45C --plating)",
            },
        },
    }
}

plan_entry = {
    "action": "plan",
    "objective_breakdown": (
        "stage2: vol ED>=950 Wh/L (calc-energy energy_density_wh_l), plateau>=4.1 V (midpoint_voltage_v), "
        "SEI<=500 nm@100cyc (sei_thickness_nm_end); stage3: T_max<=323.15 K and plated=false under 4C_charge_45C "
        "(45 C ambient). Key trade-offs: (1) 1C capacity is protocol-capped at 4.5 Ah -> ED optimum is the minimum "
        "stack that still delivers 4.5 Ah; (2) T_max budget is only 5 K above 45 C ambient -> cooling coefficient is "
        "the primary thermal lever (default h=10 gives est. 40+ K rise at 18 A); (3) plateau>=4.1 V exceeds any "
        "NMC811-class system (midpoint ~3.6 V) -> high-voltage LNMO system required; (4) end-of-charge anode stoich "
        "is fixed ~0.90 by cycle closure -> plating mitigation via particle size/electrolyte/AM fraction, not thickness."
    ),
    "candidate_strategy": (
        "R1: propose systemLNMO (LNMO.json base) + electrolyte formulation HE (sigma 1.5 S/m, t+ 0.4) + anode coating "
        "(k_SEI x0.1) + 4 molecular film-forming additives (FEC/VC/LiDFOB/PS) through mace-only funnel (ablation); "
        "baseline characterization of LNMO as-is (1C spme + calc-energy + 4C lumped/plating spme + aging 100cyc spme). "
        "R2+: architecture variants (cathode 65-70 um [dead-c_max margin: baseline holds ~8.7 Ah >> 4.5], anode ~85-90 um "
        "[discharge drains 4.38 mAh/cm2 from anode starting at 90% stoich], sep 10 um, CC 10/8 um, AM fraction up, "
        "particles R_p 3 um / R_n 2.5 um) + electrolyte + coating + h=100-150. DFN for 4C plating on passers."
    ),
    "budget_allocation": (
        "R1: 1 sim set (4 runs) + mace funnel (4 molecules). R2: 3 architecture variants x (1C+energy+4C+aging). "
        "R3: thermal/SEI refinement 1-2 variants + DFN final verification. R4+: deliverables + render. ~15-20 runs total."
    ),
    "risk_and_fallback": (
        "Plating (highest risk): mitigate R_n/electrolyte/AM fraction; fallback Stage 3. T_max: h=100-150 + DCR reduction; "
        "if h needed >300 -> three-strike questioning (boundary check). SEI: Chen2020-scale ~449 nm marginal under 4.7 V "
        "window -> coating x0.1 kinetics. ED margin: target stack ~181-190 um at V_avg 4.15-4.2 V ~ 1000+ Wh/L (est). "
        "Plateau: anchor table midpoint 4.17 V -> margin; verify by sim."
    ),
    "detail": "design_plan.md",
}

propose_r1 = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "base": LNMO_BASE,
            "name": "systemLNMO",
            "role": "high-voltage LiNi0.5Mn1.5O4 spinel cathode system (4.7 V-class) to meet plateau >= 4.1 V; system candidate, skips molecular funnel, direct Stage 3 simulation",
        },
        {
            "struct": {
                "Electrolyte conductivity [S.m-1]": 1.5,
                "Cation transference number": 0.4,
            },
            "name": "HE-electrolyte",
            "role": "high-conductivity high-transference electrolyte formulation (sigma 1.5 S/m scalar, t+ 0.4; literature-based estimate) to cut DCR, reduce concentration polarization and anode surface-potential dip at 4C",
        },
        {
            "struct": {
                "SEI kinetic rate constant [m.s-1]": 1e-13,
            },
            "name": "Gr-ALD-coating",
            "role": "Al2O3 ALD-coated graphite anode suppressing SEI growth (k_SEI x0.1, estimate per library calibration 449->385 nm scale); inorganic coating skips molecular funnel (ML potentials unreliable on ionic solids), judged in Stage 3 aging",
        },
        {
            "smiles": "O=C1OC(F)CO1",
            "name": "FEC",
            "role": "fluoroethylene carbonate film-forming additive (SEI stabilization for high-voltage window)",
        },
        {
            "smiles": "O=C1OC=CO1",
            "name": "VC",
            "role": "vinylene carbonate film-forming additive (SEI stabilization)",
        },
        {
            "smiles": "O=C1C(=O)OB(F)(F)O1.[Li+]",
            "name": "LiDFOB",
            "role": "lithium difluoro(oxalato)borate film-forming salt additive (SEI quality)",
        },
        {
            "smiles": "O=S1(=O)CCCO1",
            "name": "PS",
            "role": "1,3-propane sultone film-forming additive (SEI stabilization)",
        },
    ],
    "llm_reason": (
        "Plateau >= 4.1 V is unreachable for NMC811-class systems (midpoint ~3.6 V) -> ceiling assessment concludes "
        "material-level escalation: adopt library LNMO 4.7 V-class parameter set (anchor: cell midpoint 4.17 V). "
        "4C fast charge at 18 A requires low anode surface-potential dip -> high-conductivity/high-t+ electrolyte and "
        "small anode particles. SEI <= 500 nm under 4.7 V window -> film-forming additive package (mace-only funnel, "
        "ablation) + Al2O3-coated graphite (k_SEI x0.1). Architecture follows in R2 per budget."
    ),
}

for entry in (entry0, plan_entry, propose_r1):
    append_entry(ws, entry)
print("wrote 3 entries to", ws.path / "log.jsonl")
