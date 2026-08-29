"""Entry 0 for case t4_r1_noforce — criteria + meta, written once via bda.store."""
import sys
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t4_r1_noforce", "runs/exp")

entry = {
    "criteria": {
        "stage1": {
            "max_energy_ev": {"max": 0.0},
            "max_homo_ev": {"max": -6.0},
        },
        "stage2": {
            "lowT_retention": {"min": 0.95},
            "energy_density_wh_kg": {"min": 327.18},
            "energy_density_wh_l": {"min": 880.0},
        },
        "stage3": {
            "T_max_K": {"max": 333.15},
            "plated": False,
        },
        "meta": {
            "case": "t4_r1_noforce",
            "task": "Design a battery for extreme-cold environment equipment: 1C discharge capacity retention >= 95% at -20C, energy density >= 327.18 Wh/kg, volumetric energy density >= 880 Wh/L",
            "real_compute": False,
            "start_stage": 3,
            "base_default": "Chen2020",
            "ablation": {
                "exploration_force": "OFF (declared by task text: no forced 2-4 architecture variants per round, free exploration)",
                "ceiling_escalation": "ON (protocol default)",
                "funnel_voting": "ON (protocol default; molecular funnel not engaged at start_stage=3)",
            },
            "freedoms": {
                "electrode_system": "adjustable (widest interpretation; task text silent) — base parameter-set switch allowed; default starting set Chen2020 per anchor-table rule (no electrode system named in task)",
                "electrolyte_formulation": "adjustable (widest interpretation; task text silent) — electrolyte conductivity/diffusivity/transference-number transport overrides allowed (primary low-T levers)",
                "electrode_modification": "adjustable (widest interpretation; task text silent) — coating/doping via SEI/cracking parameter bridge",
                "cell_architecture": "adjustable (widest interpretation; task text silent) — thickness/porosity/N-P/separator/current collector/particle radius",
                "thermal_management": "adjustable (widest interpretation; task text silent) — cooling coefficient",
            },
            "retention_definition": "lowT_retention = lowT_discharge.capacity_ah / 1C_discharge.capacity_ah (same params, same mode); mechanically computed and written to bridge/derived_*.json",
            "safety_defaults_note": "task text silent on safety metrics; protocol-default safety exam applied: 4C charge at 45C, lumped thermal + plating; T_max_K <= 333.15 K (60 C) and plated=false",
            "stage1_note": "molecular-level layer not engaged at start_stage=3; protocol-default elimination lines pre-registered in case of material-design escalation",
            "start_stage_basis": "no new materials/additives/electrolyte design named in task text -> architecture/formulation optimization scope -> start_stage 3 (SKILL 0.2 rule)",
        },
    }
}

if (ws.path / "log.jsonl").exists():
    raise SystemExit("log.jsonl already exists — refuse to overwrite entry 0")
append_entry(ws, entry)
print("entry 0 written ->", ws.path / "log.jsonl")
