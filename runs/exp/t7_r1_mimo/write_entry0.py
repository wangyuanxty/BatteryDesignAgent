"""Write log.jsonl entry 0 for t7_r1_mimo case."""
import json, sys, os
os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
sys.path.insert(0, "D:/research/degradation_prognostics/Battery_Design_Agent")
from bda.store import append_entry, CaseWorkspace

ws = CaseWorkspace("t7_r1_mimo", "D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")

entry_0 = {
    "criteria": {
        "stage1": {
            "note": "No molecular-level constraints in task; starting at Stage 3 (cell design) with Chen2020 baseline parameters"
        },
        "stage2": {
            "energy_density_wh_kg": {"min": 327.18},
            "sei_thickness_nm": {"max": 550},
            "sei_note": "SEI <= 550 nm after 100 cycles at 45C (aging_1C_100cyc_45C protocol)"
        },
        "stage3": {
            "plated": False,
            "nail_penetration_triggered": False,
            "nail_heat_w": 10,
            "nail_note": "Nail penetration: 10 W short-circuit heat generation must not trigger thermal runaway"
        },
        "meta": {
            "real_compute": False,
            "base_params": "Chen2020",
            "system": "NMC811/graphite (default Chen2020 baseline teaching parameterization)",
            "electrolyte": "EC/EMC + LiPF6 (default)",
            "start_stage": 3,
            "ablation": {
                "exploration_force": True,
                "ceiling_escalation": True,
                "funnel_voting": True
            },
            "cooling_h": 10,
            "cell_type": "pouch (default Chen2020 geometry)"
        },
        "freedoms": {
            "electrode_system": {"status": "locked", "value": "Chen2020", "reason": "no system specified in task; default Chen2020"},
            "electrolyte": {"status": "locked", "value": "baseline transport parameters", "reason": "no electrolyte formulation specified; default EC/EMC+LiPF6 transport"},
            "electrode_modification": {"status": "locked", "value": "none", "reason": "no coating/doping specified in task"},
            "cell_architecture": {"status": "adjustable", "value": "thickness/porosity/N-P/separator/current-collector/particle-size", "reason": "HEV design optimization; task demands high ED + safety which requires architecture tuning"},
            "thermal_management": {"status": "locked", "value": "h=10 W/m2K", "reason": "no cooling specified; default h=10"}
        }
    }
}

append_entry(ws, entry_0)
print("Entry 0 written successfully")
