"""Agent-built scratch: write log.jsonl entry 0 (criteria+meta) and plan entry (Stage 1)."""
import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_flash", "runs/exp")

entry0 = {
    "criteria": {
        "stage1": {
            "max_energy_ev": {"max": 0.0},
            "max_homo_ev": {"max": -6.0}
        },
        "stage2": {
            "energy_density_wh_l": {"min": 950},
            "midpoint_voltage_v": {"min": 4.1},
            "sei_thickness_nm_end": {"max": 500}
        },
        "stage3": {
            "T_max_K": {"max": 323.15},
            "plated": False
        },
        "meta": {
            "case": "t6_r1_flash",
            "objective": "Design a battery for a smartphone: volumetric energy density >= 950 Wh/L, 4C fast charge (no lithium plating), maximum temperature <= 50 C, anode SEI thickness <= 500 nm after 100 cycles, voltage plateau >= 4.1 V",
            "real_compute": False,
            "start_stage": 2,
            "base_params": "LNMO.json (4.7 V-class high-voltage spinel; Chen2020 base + LNMO overlay per anchor table; --base path)",
            "system_mapping_basis": "task implies high-voltage cathode via plateau >= 4.1 V (NMC811 cell midpoint 3.61 V < 4.1 V ceiling); LNMO anchor: discharge midpoint 4.17 V",
            "aging_protocol": "aging_1C_100cyc (100 cycles 1C 25C; SEI ec-reaction-limited, isothermal)",
            "safety_protocol": "4C_charge_45C (4C charge, 45C ambient) + --thermal lumped --plating",
            "voltage_plateau_key": "midpoint_voltage_v (calc-energy plateau approximation, mechanical)",
            "freedoms": {
                "electrode_system": "adjustable - system switch to LNMO high-voltage cathode (no lock in task text)",
                "electrolyte_formulation": "adjustable - transport overrides sigma/t+/D allowed (no lock; widest interpretation)",
                "electrode_modification": "adjustable - coating/doping allowed (no lock)",
                "cell_architecture": "adjustable - thickness/porosity/N-P/separator/CC/particle size (no lock)",
                "thermal_management": "adjustable - cooling coefficient h (no lock)"
            }
        }
    }
}

plan_entry = {
    "action": "plan",
    "objective_breakdown": "M1 volumetric ED >= 950 Wh/L (stage2 energy_density_wh_l); M2 plateau >= 4.1 V (stage2 midpoint_voltage_v); M3 SEI <= 500 nm after 100 cycles (stage2 sei_thickness_nm_end); M4 no plating at 4C (stage3 plated=false); M5 T_max <= 50C (stage3 T_max_K <= 323.15 K, 4C_charge_45C lumped). Trade-off: ED (thick electrode, high voltage) vs fast-charge heat/plating (thin, low-resistance); plateau vs polarization from thickening.",
    "candidate_strategy": "R1 baseline/ceiling: LNMO system candidate (1C+calc-energy, aging, 4C safety) + Chen2020 reference 1C+calc-energy proving NMC811 plateau unreachable. R2 architecture variants (thickness up, porosity down, thin sep/CC, small anode particle). R3 electrolyte sigma/t+/D + cooling h on best architecture. R4 DFN precision. Fallback: SEI coating kinetics bridge or funnel additives only if M3/M4 binding; three-strike questioning if 4C protocol-scale issue.",
    "budget_allocation": "flash: R1 ~6 runs (SPMe), R2 ~6 runs, R3 ~5 runs, R4 ~4 DFN runs; close with deliverables+render+verify. Target <= 5 rounds.",
    "risk_and_fallback": "950 Wh/L tight (baseline LNMO est ~800s Wh/L; thickest sane variant must reach); plateau may drop below 4.1 V when thickening (polarization) - fallback thin + high-sigma electrolyte; 4C at fixed 18 A on ~0.5 Ah model is extreme - measure, question boundary at three-strike; SEI inherited Chen2020 kinetics ~449 nm < 500 nm expected.",
    "detail": "design_plan.md"
}

append_entry(ws, entry0)
append_entry(ws, plan_entry)
print("entry 0 + plan written to", ws.path / "log.jsonl")
