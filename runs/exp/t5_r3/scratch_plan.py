"""t5_r3 plan-entry writer via bda.store.append_entry."""
from bda.store import CaseWorkspace, append_entry
ws = CaseWorkspace("t5_r3", "runs/exp")
plan = {
    "action": "plan",
    "objective_breakdown": (
        "stage2: energy_density_wh_kg >= 500.94 (calc-energy contract); "
        "stage3: 4C fast charge without lithium plating (anode_potential_v min >= 0 V -> plated=false) "
        "and T_max_K <= 333.15 (60 C). Trade-off: ED wants thick electrodes/thin collectors/mass dilution; "
        "4C plating wants low areal current density (thin electrodes), small negative particles, "
        "high electrolyte conductivity; T_max has only 15 K headroom above the 318.15 K protocol ambient."
    ),
    "candidate_strategy": (
        "Round1 baseline Chen2020 (1C + calc-energy + 4C/45C/plating). "
        "Rounds2-5 architecture ladder: thin collectors (Al 16->8um, Cu 12->6um), "
        "separator 12->9um, thicker electrodes (pos 75.6->100um, neg 85.2->112um, N/P kept), "
        "negative particle radius 5.86->3um, electrolyte sigma/t+ overrides, cooling h 10->30-50. "
        "Round6+ material escalation if ceiling unmet: OKane2022 (graphite+SiOx) or LNMO 4.7V system switch."
    ),
    "budget_allocation": (
        "Rounds1-5 architecture (SPMe proxy-first, DFN only for shortlist); "
        "Rounds6-9 safety fine-tuning + Stage2 material escalation if required; "
        "Rounds10-11 closing (endorse skip honest, deliverables, render, verify)."
    ),
    "risk_and_fallback": (
        "R1 ED ceiling: escalate via ceiling_escalation -> Stage2/system switch, never relax thresholds. "
        "R2 plating: same-scale corrections (particle size, sigma/t+, loading, N/P); ghost -> system assumption "
        "questioned -> SiOx anode. R3 T_max: h escalation + conductivity; 4C T_max is the operative check "
        "(abuse not in task criteria). Known artifact: Chen2020 initial state discharged -> first discharge "
        "capacity may be low; recorded honestly."
    ),
    "detail": "design_plan.md",
}
append_entry(ws, plan)
print("plan entry appended")