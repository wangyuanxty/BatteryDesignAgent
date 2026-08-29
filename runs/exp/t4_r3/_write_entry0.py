"""t4_r3 entry-0 writer: writes criteria+meta as log.jsonl entry 0 via bda.store.append_entry.

Agent-built input file (allowed); log write goes through the bda store API (no self-built JSON writer).
Workspace: runs/exp/t4_r3 (CaseWorkspace resolves relative to repo root, cwd-independent).
"""
import json

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")

entry0 = {
    "criteria": {
        "stage1": {
            # Stage-2 funnel elimination lines (pre-registered per protocol; unused unless
            # ceiling_escalation pulls the case into Stage 2 material design).
            "max_energy_ev": {"max": 0.0},
            "max_homo_ev": {"max": -6.0},
        },
        "stage2": {
            # Cell performance contract — numbers verbatim from the task text.
            "lowT_retention_1C_pct": {"min": 95},
            "energy_density_wh_kg": {"min": 327.18},
            "energy_density_wh_l": {"min": 880},
        },
        "stage3": {
            "T_max_K": {"max": 333.15},
            "plated": False,
        },
        "meta": {
            "task_text": (
                "Design a battery for extreme-cold environment equipment: 1C discharge "
                "capacity retention >= 95% at -20C, energy density >= 327.18 Wh/kg, "
                "volumetric energy density >= 880 Wh/L."
            ),
            "start_stage": 3,
            "start_stage_reason": (
                "task names no new materials/additives/electrode design, only cell-level "
                "performance targets (SKILL §0.2 rule) -> start at Stage 3 cell design; "
                "materials use system baseline parameters"
            ),
            "base_params": "Chen2020",
            "base_params_reason": (
                "task text names no electrode system -> anchor-table deterministic default "
                "Chen2020 (SKILL §1.5); discriminant anchor verified by parameter dump before use"
            ),
            "real_compute": False,
            "ablation": {
                "exploration_force": "ON",
                "ceiling_escalation": "ON",
                "funnel_voting": "ON",
                "note": "all defaults; task text silent on ablation",
            },
            "freedoms": {
                "electrode_system": "adjustable (base parameter-set switch allowed)",
                "electrolyte_formulation": "adjustable (Electrolyte conductivity/diffusivity [S.m-1]/[m2.s-1], Cation transference number)",
                "electrode_modification": "adjustable (SEI kinetic rate constant/reaction exchange current density, cracking rate)",
                "cell_architecture": "adjustable (electrode thickness/porosity/N-P, separator, current collectors, particle radii)",
                "thermal_management": "adjustable (Total heat transfer coefficient)",
            },
            "freedom_basis": (
                "zero-interaction session: degrees of freedom not declared in task text take "
                "the widest interpretation, recorded here (t1_r1 lesson)"
            ),
            "defaults_used": {
                "T_max_K_redline": "333.15 K (= 60 C); task text silent -> protocol default recorded",
                "abuse_scenarios": "not requested by task text -> overcharge/nail skipped",
                "structure_model": "not requested -> no 3D structure model deliverable",
                "aging": "not requested -> no cycle-life criterion",
            },
            "lowT_retention_definition": (
                "mechanical: 100 * capacity_ah(lowT_discharge, 1C, 253.15 K) / "
                "capacity_ah(1C_discharge, 298.15 K) with identical params "
                "(pybamm_runner PROTOCOLS comment); derived JSON written to bridge/ and "
                "passed to bda log-evaluate as an output file"
            ),
            "energy_density_scope": (
                "contract caliber (bda calc-energy): electrolyte excluded from mass and "
                "volume, annotated in output (electrolyte_included: false)"
            ),
        },
    }
}

append_entry(ws, entry0)
print("entry 0 written to", ws.path / "log.jsonl")
print(json.dumps(entry0, ensure_ascii=False, indent=2)[:600], "...")