"""t5_r3 entry-0 writer: criteria + meta via bda.store.append_entry (protocol-mandated writer)."""
import sys
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r3", "runs/exp")

entry0 = {
    "criteria": {
        # Molecular-level elimination lines (protocol defaults, pre-registered in case Stage 2 opens).
        "stage1": {
            "max_energy_ev": {"max": 0.0},
            "max_homo_ev": {"max": -6.0},
        },
        # Cell performance goals (task text verbatim: energy density >= 500.94 Wh/kg).
        "stage2": {
            "energy_density_wh_kg": {"min": 500.94},
        },
        # Safety goals (task text verbatim: 4C fast charge with no lithium plating;
        # maximum temperature <= 60 C == 333.15 K, mechanically converted).
        "stage3": {
            "T_max_K": {"max": 333.15},
            "plated": False,
        },
        # Case-level parameters.
        "meta": {
            "task_text": "Design a battery for a next-generation flagship vehicle: energy density >= 500.94 Wh/kg, support 4C fast charge (no lithium plating), maximum temperature <= 60C",
            "zero_interaction": True,
            "start_stage": 3,
            "start_stage_reason": "task text names no new materials/additives/electrolyte design; "
                                "architecture/formulation-level objective -> start at Stage 3 (cell design); "
                                "materials use system baseline; ceiling_escalation ON may escalate to Stage 2",
            "base_params": "Chen2020",
            "base_params_reason": "task text names no electrode system -> default Chen2020 per anchor table (recorded default)",
            "real_compute": False,
            "ablation": {"exploration_force": "on", "ceiling_escalation": "on", "funnel_voting": "on"},
            "freedoms": {
                "electrode_system": "adjustable (widest interpretation: no lock declared in task text)",
                "electrolyte_formulation": "adjustable (sigma/t+ transport overrides via parameter bridge)",
                "electrode_modification": "adjustable (coating/dopant via SEI/cracking parameters)",
                "cell_architecture": "adjustable (thickness/porosity/N-P/separator/current collector/particle size)",
                "thermal_management": "adjustable (cooling coefficient h)",
            },
            "structure_model_requested": False,
        },
    }
}

if ws.path.joinpath("log.jsonl").exists():
    raise SystemExit("log.jsonl already exists - refusing to overwrite entry 0")
append_entry(ws, entry0)
print("entry 0 written:", ws.path / "log.jsonl")