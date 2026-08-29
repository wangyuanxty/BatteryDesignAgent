"""Append plan entry to log.jsonl."""
import sys

sys.path.insert(0, r".claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t8_r3", root="runs", create=False)

entry = {
    "action": "plan",
    "objective_breakdown": (
        "stage2: ED>=446.18 Wh/kg (contract 1C energy / stack mass); retention_5c>=0.9 "
        "(5C DFN cap / same-params 1C DFN cap); mass_kg<=0.04. stage3: T_max_K<=333.15 at 4C/45C charge, plated=false. "
        "Trade-off: ED vs 5C retention Pareto (thicker electrodes raise energy-per-40g but hurt 5C); "
        "mass budget reallocation (thin Cu/Al/sep -> more active mass); Chen2020 default stack ~43.5 g > 40 g so mass reduction is mandatory; "
        "446.18 Wh/kg at 40 g <=> >=17.85 Wh <=> ~4.82 Ah at 3.7 V midpoint."
    ),
    "candidate_strategy": (
        "R1: C0 baseline characterization (full metric set) + V1 mass-fit (thin collectors/sep, full area, <=40 g) "
        "+ V2 active-boost (V1 + thicker electrodes) + V3 rate-margin (V1 + smaller negative particle radius). "
        "Follow-up per fallback routing: rate short -> stage3 transport/kinetic fixes; "
        "ED short at 40 g -> stage2 system escalation (LNMO high-voltage candidate); thermal -> cooling h."
    ),
    "budget_allocation": (
        "R1-3 architecture frontier (mass fit, thickness sweep), ~4 sims+calc per candidate (1C SPMe->DFN, calc-energy, 5C DFN, 4C charge); "
        "R4-6 fine-tune winning branch (particle size / electrolyte transport / porosity / cooling); R7+ escalation/closing."
    ),
    "risk_and_fallback": (
        "A: 1C capacity <4.82 Ah -> stage2 system escalation (LNMO midpoint ~4.17 V, or OKane2022 SiOx). "
        "B: 5C retention <90% -> neg particle radius down -> electrolyte sigma up -> thickness down; three-strike questioning. "
        "C: T_max breach -> cooling h up (thermal-management freedom). D: solver/parameter errors -> read verbatim, fix, rerun."
    ),
    "detail": "design_plan.md",
}
append_entry(ws, entry)
print("plan entry appended")