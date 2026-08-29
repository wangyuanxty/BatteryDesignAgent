"""Write audit-ledger entry 0 (criteria + meta) for case t5_r2 — headless zero-interaction session.

Contract thresholds parsed verbatim from the task text:
  - energy density >= 500.94 Wh/kg  -> stage2 energy_density_wh_kg {"min": 500.94}
  - 4C fast charge, no lithium plating -> stage3 plated false (mechanical: anode_potential_v min < 0)
  - maximum temperature <= 60 C -> stage3 T_max_K {"max": 333.15}

Unspecified parameters -> protocol defaults, recorded:
  - start_stage 3 (no materials named in task text)
  - base Chen2020 (no electrode system named -> anchor-table default, recorded)
  - real_compute false | ablation switches all ON | all five degree-of-freedom categories adjustable
"""
import json

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

entry = {
    "criteria": {
        "stage1": {"max_energy_ev": 0.0, "max_homo_ev": -6.0},
        "stage2": {"energy_density_wh_kg": {"min": 500.94}},
        "stage3": {"T_max_K": {"max": 333.15}, "plated": False},
        "meta": {
            "task": "Design a battery for a next-generation flagship vehicle: energy density >= 500.94 Wh/kg, support 4C fast charge (no lithium plating), maximum temperature <= 60C",
            "headless": True,
            "threshold_parsing": {
                "energy_density_wh_kg": ">= 500.94 Wh/kg (contract caliber: calc-energy ED = discharge energy / electrode+collector+separator mass, electrolyte excluded by formula)",
                "plating": "4C fast charge without lithium plating -> stage3 plated=false (anode_potential_v series min < 0 V => plated, mechanically derived by log-evaluate)",
                "T_max": "maximum temperature <= 60 C -> T_max_K <= 333.15 K (60 C = 333.15 K), measured at 4C_charge_45C with coupled lumped thermal model",
            },
            "start_stage": 3,
            "start_stage_basis": "task text names no new materials/additives/electrode design; objective is metric-only -> starting-point rule maps to start_stage 3 (cell design); materials use system baseline until ceiling escalation is triggered",
            "base": "Chen2020",
            "base_basis": "task text names no electrode system -> anchor-table default Chen2020, recorded; to be re-verified by parameter dump at baseline characterization",
            "real_compute": False,
            "ablation": {"exploration_force": "on", "ceiling_escalation": "on", "funnel_voting": "on"},
            "ablation_basis": "all switches default ON (not declared in task text; benchmark run keeps the full protocol)",
            "freedoms": {
                "electrode_system": "adjustable",
                "electrolyte_formulation": "adjustable",
                "electrode_modification": "adjustable",
                "cell_architecture": "adjustable",
                "thermal_management": "adjustable",
            },
            "freedoms_basis": "zero-interaction execution: task text declares no degree-of-freedom locks -> all five categories take the widest interpretation per SKILL.md section 0 (t1_r1 lesson: narrow interpretation on undeclared freedoms produced a negative result)",
            "cad_model": "not requested (headless: no user available to clarify the optional structure-model deliverable)",
        },
    }
}

append_entry(ws, entry)
print("entry 0 written ->", ws.path / "log.jsonl")