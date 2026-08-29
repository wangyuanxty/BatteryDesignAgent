import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("portability/t1_lc", "runs")

task = ("Design a battery for a next-generation pure electric sedan: "
        "energy density \u2265 392.61 Wh/kg, support 4C fast charge "
        "(no lithium plating), maximum temperature \u2264 60\u00b0C, "
        "overcharge to 4.7 V without triggering thermal runaway.")

entry = {
    "criteria": {
        "stage1": {
            "max_energy_ev": 0.0,
            "max_homo_ev": -6.0
        },
        "stage2": {
            "energy_density_wh_kg": {"min": 392.61}
        },
        "stage3": {
            "T_max_K": {"max": 333.15},
            "plated": False,
            "triggered": False
        },
        "meta": {
            "real_compute": False,
            "ablation": {
                "exploration_force": True,
                "ceiling_escalation": True,
                "funnel_voting": True
            },
            "start_stage": 3,
            "base_params": "Chen2020",
            "freedoms": {
                "electrode_system": "adjustable",
                "electrolyte_formulation": "adjustable",
                "electrode_modification": "adjustable",
                "cell_architecture": "adjustable",
                "thermal_management": "adjustable"
            },
            "freedoms_note": ("headless zero-interaction: no degrees of freedom declared in task text; "
                              "widest interpretation applied and recorded (t1_r1 lesson)"),
            "task": task
        }
    }
}

append_entry(ws, entry)
print("entry 0 written to", ws.path / "log.jsonl")
