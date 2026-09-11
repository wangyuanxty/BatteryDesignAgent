import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("portability/t6_oa", "runs")

plan = {
    "action": "plan",
    "objective_breakdown": (
        "stage2(cell): volumetric ED>=950 Wh/L, midpoint plateau>=4.1V, SEI<=500nm/100cyc; "
        "stage3(safety): T_max<=323.15K(50C) at 4C charge@45C, plated=false. "
        "Trade-off: volumetric ED vs fast-charge safety (T_max/plating) are in tension; "
        "thicker electrodes raise ED but worsen heat/plating; high-voltage LNMO raises ED per Ah "
        "but generates more heat per coulomb at 4C."
    ),
    "candidate_strategy": (
        "System: LNMO high-voltage spinel cathode (4.7V class, midpoint~4.17V) - forced by plateau>=4.1V "
        "(NMC811 ~3.6V cannot meet). Round1 baseline characterization (1C discharge->ED/plateau; "
        "4C charge@45C+plating->T_max/plating; aging 100x1C->SEI). Round2+ architecture exploration "
        "(2-4 variants/round: electrode thickness, collector/separator thinning, porosity, active fraction, "
        "anode particle radius, electrolyte conductivity, cooling h)."
    ),
    "budget_allocation": "R1 baseline; R2-7 architecture/material exploration (SPMe screen -> DFN passers); R8-12 safety+SEI fine-tuning; reserve fallback rounds.",
    "risk_and_fallback": (
        "RiskA: T_max<=323.15K very tight (+5K over 45C ambient) -> raise h, lower DCR. "
        "RiskB: ED>=950 Wh/L may exceed architecture ceiling -> thin collectors/separator, thick electrodes, high active fraction; else honest negative. "
        "RiskC: graphite plating at 4C -> smaller anode particles, higher electrolyte conductivity, reduced anode thickness. "
        "RiskD: SEI>500nm -> SEI-suppressing coating. Fallback routes: ED->Stage3 arch; plating/T_max->Stage3 arch + Stage2 transport; SEI->Stage2 coating."
    ),
    "detail": "design_plan.md",
}

append_entry(ws, plan)
print("plan entry written")
