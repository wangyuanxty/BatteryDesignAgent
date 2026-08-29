# Stage-1 log writes for VBF case t1_r1_flash (agent-built input script)
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t1_r1_flash", root="runs")

entry0 = {
    "criteria": {
        "stage1": {
            "max_energy_ev": 0.0,
            "max_homo_ev": -6.0,
        },
        "stage2": {
            "energy_density_wh_kg": {"min": 392.61},
        },
        "stage3": {
            "T_max_K": {"max": 333.15},  # 60 C + 273.15
            "plated": False,
            "triggered": False,
        },
        "meta": {
            "task": "Design a battery for a next-generation pure electric sedan: energy density >= 392.61 Wh/kg, support 4C fast charge (no lithium plating), maximum temperature <= 60 C, overcharge to 4.7 V without triggering thermal runaway.",
            "real_compute": False,
            "start_stage": 3,
            "base_params": "OKane2022",
            "freedoms": {
                "electrode_system": "adjustable (task silent -> widest interpretation); baseline OKane2022 (NMC811/graphite+SiOx) chosen: complete thermal/geometry params (honest T_max), SEI+cracking models, 4.2 V cutoff -> overcharge +0.5 V = task 4.7 V; system switches allowed",
                "electrolyte_formulation": "adjustable (Electrolyte conductivity/diffusivity, Cation transference number overrides)",
                "electrode_modification": "adjustable (SEI kinetic rate constant / SEI reaction exchange current density / cracking rate)",
                "cell_architecture": "adjustable (thickness/porosity/N-P/separator/current collector/particle size)",
                "thermal_management": "adjustable (Total heat transfer coefficient h)",
            },
        },
    }
}
append_entry(ws, entry0)

plan = {
    "action": "plan",
    "objective_breakdown": "4 criteria in 2 decision layers: stage2 energy_density_wh_kg >= 392.61 (architecture levers); stage3 plated=false at 4C/45C (anode_potential_v min >= 0), T_max_K <= 333.15 at 4C/45C (only 15 K rise budget; cooling h + DCR), triggered=false on overcharge to 4.7 V (run-tr mechanical, cell mass from calc-energy). Trade-off: thicker electrodes raise ED but worsen 4C overpotential (plating) and heat; cooling h and electrolyte transport help 4C/T_max at zero ED cost.",
    "candidate_strategy": "R1: baseline OKane2022 full suite (1C DFN + calc-energy; 4C charge lumped+plating; overcharge+run-tr) + 2 ED probes (Arch-A thin collectors, Arch-B thick positive + thin collectors). R2 routed by failing metric: ED -> thickness/porosity; plating -> sigma/t+/particle radius/N-P; T_max -> cooling h; TR -> mass/chemistry. R3 full confirmation on final candidate.",
    "budget_allocation": "R1 ~7 sims; R2 ~4-6; R3 ~4; total ~15-17 cell sims; 0 true compute (real_compute=false); Stage 2 escalation only if architecture ceiling < ED target after R1.",
    "risk_and_fallback": "ED<392.61 likely on stock OKane2022 -> thin collectors+thickness; ceiling assessment after R1, escalate to Stage 2 if unreachable. Plating at end of charge -> transport/particle/N-P levers. T_max with h=10 default: hA=0.053 W/K so DT>>15 K expected -> cooling h primary lever. Overcharge TR judged mechanically. Three-strike -> question assumptions layer-by-layer in final.escalation.",
    "detail": "design_plan.md",
}
append_entry(ws, plan)
print("entry0 + plan written to", ws.path / "log.jsonl")
