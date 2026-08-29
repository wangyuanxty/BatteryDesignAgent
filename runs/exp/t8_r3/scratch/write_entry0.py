"""Write log.jsonl entry 0 (criteria + meta) for t8_r3. Run from repo root."""
import json
import sys

sys.path.insert(0, r".claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t8_r3", root="runs", create=True)

entry = {
    "criteria": {
        "stage1": {
            "max_energy_ev": 0.0,   # mace relaxation energy elimination line (protocol default)
            "max_homo_ev": -6.0,    # xtb HOMO elimination line (protocol default)
        },
        "stage2": {
            "energy_density_wh_kg": {"min": 446.18},  # task text verbatim: >= 446.18 Wh/kg
            "retention_5c": {"min": 0.9},             # task text: 5C discharge >= 90% capacity retention
            "mass_kg": {"max": 0.04},                 # task text: cell mass <= 40 g (0.04 kg, mechanical conversion)
        },
        "stage3": {
            "T_max_K": {"max": 333.15},  # 4C/45C charge max temperature; protocol default 60 C red line (task text unspecified)
            "plated": False,             # no lithium plating at 4C charge 45 C
        },
        "meta": {
            "case": "t8_r3",
            "task_text": "Design a battery for a long-endurance drone: energy density >= 446.18 Wh/kg, 5C discharge with >= 90% capacity retention, cell mass <= 40 g",
            "start_stage": 3,
            "start_stage_reason": "objective names no new materials/additives/electrolyte design -> per protocol start at Stage 3 (cell design); materials use system baseline",
            "base_params": "Chen2020",
            "base_reason": "task text names no electrode system -> deterministic default Chen2020 (anchor table: NMC811/graphite teaching parameterization). Discriminant verified by parameter dump: pure-graphite negative, pos density 3262 / neg density 1657, nominal 5 Ah, area 0.065x1.58 m.",
            "real_compute": False,
            "ablation_switches": {
                "exploration_force": "ON",
                "ceiling_escalation": "ON",
                "funnel_voting": "ON",
            },
            "freedoms": {
                "electrode_system": "adjustable (base parameter set switch allowed; widest interpretation)",
                "electrolyte_formulation": "adjustable (sigma/t+/D transport overrides allowed)",
                "electrode_modification": "adjustable (coating/doping allowed)",
                "cell_architecture": "adjustable (thickness/porosity/N-P/separator/current collector/particle size/cell geometry)",
                "thermal_management": "adjustable (total heat transfer coefficient)"},
            "freedoms_basis": "zero-interaction execution: task text declares no degree-of-freedom locks -> all five categories widest interpretation, recorded in audit (t1_r1 lesson)",
            "metric_definitions": {
                "energy_density_wh_kg": "calc-energy contract formula: ED = integral(V*I_1C dt)/3600 / mass_kg; mass = layers (pos/neg active with porosity factor + pos/neg current collectors + separator, electrolyte excluded) x electrode area; source calc-energy output",
                "retention_5c": "5C capacity / same-parameter 1C capacity (5C_discharge DFN vs 1C_discharge DFN), mechanically computed, recorded to derived JSON for log-evaluate",
                "mass_kg": "calc-energy output mass_kg (stack mass incl. collectors, excl. electrolyte/casing)",
                "T_max_K": "run-pyamm 4C_charge_45C protocol, thermal=lumped, max volume-averaged cell temperature",
                "plated": "auto-derived: min(anode_potential_v) < 0 V at 4C charge 45C",
            },
            "protocols": {
                "rate": "5C_discharge --mode dfn (SPMe underestimates at 5C)",
                "safety": "4C_charge_45C --thermal lumped --plating",
                "aging": "not required: criteria contain no cycle-life threshold; aging protocol skipped unless coating/doping candidates appear (recorded)",
            },
            "stage3_note": "T_max_K threshold 333.15 K is a protocol default applied because task text does not specify a temperature red line (zero-interaction: defaults for unspecified parameters); plated=false is the standard fast-charge safety requirement",
        },
    }
}

append_entry(ws, entry)
print("entry 0 written to", ws.path / "log.jsonl")
print(json.dumps(entry, ensure_ascii=False, indent=2))