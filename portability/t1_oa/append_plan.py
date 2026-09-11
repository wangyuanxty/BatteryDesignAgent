import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t1_oa", "runs/portability")
plan = {
    "action": "plan",
    "objective_breakdown": "ED>=392.61 Wh/kg (stage2) ; 4C no plating + T_max<=333.15K + overcharge 4.7V no thermal runaway (stage3). Three-way Pareto tension: ED vs T_max vs plating; ED is the binding constraint (NMC/graphite practical cell ~250-300 Wh/kg).",
    "candidate_strategy": "R1 baseline+ceiling: Chen2020 (deterministic default) + OKane2022 (SiOx) + LNMO (4.7V) characterization; then escalate to Stage 2 material design if ceiling short of 392.61 (expected); architecture (thickness/porosity/N-P/separator/CC/particle) + electrolyte transport (sigma/t+/D) as primary knobs; safety fine-tune via thin electrodes + high-conductivity electrolyte + high-voltage cathode.",
    "budget_allocation": "baseline+ceiling 2 rounds; system/material 2-4; architecture+electrolyte 5-8; safety fine-tune 3-5; total ~12-15 rounds",
    "risk_and_fallback": "ED unreachable -> escalate SiOx/LNMO or honest negative with 'what needed'; plating -> thinner electrode/higher sigma+t+/smaller particle/higher N-P; T_max -> raise cooling h; overcharge runaway -> high-voltage cathode (LNMO 4.7V near-normal cutoff)",
    "detail": "design_plan.md"
}
append_entry(ws, plan)
print("plan appended")
