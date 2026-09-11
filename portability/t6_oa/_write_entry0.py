import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("portability/t6_oa", "runs")

entry0 = {
    "criteria": {
        "stage1": {
            "max_energy_ev": {"max": 0.0},
            "max_homo_ev": {"max": -6.0},
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
            "real_compute": False,
            "start_stage": 2,
            "base": ".claude/skills/virtual-battery-factory/scripts/bda/simulators/data/LNMO.json",
            "system": "LNMO high-voltage spinel cathode / graphite (Chen2020 base + LNMO.json positive-electrode override)",
            "freedoms": {
                "electrode_system": "adjustable (LNMO high-voltage cathode required for plateau>=4.1V)",
                "electrolyte_formulation": "adjustable",
                "electrode_modification": "adjustable",
                "cell_architecture": "adjustable",
                "thermal_management": "adjustable",
            },
            "ablation": {
                "exploration_force": "ON",
                "ceiling_escalation": "ON",
                "funnel_voting": "ON",
            },
        },
    }
}

append_entry(ws, entry0)
print("entry0 written:", json.dumps(entry0, ensure_ascii=False))
