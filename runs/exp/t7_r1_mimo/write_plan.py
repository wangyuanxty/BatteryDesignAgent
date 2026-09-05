"""Write plan entry to log.jsonl."""
import os, sys
os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
sys.path.insert(0, "D:/research/degradation_prognostics/Battery_Design_Agent")
from bda.store import append_entry, CaseWorkspace

ws = CaseWorkspace("t7_r1_mimo", "D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")

plan_entry = {
    "action": "plan",
    "objective_breakdown": "HEV battery: ED >= 327.18 Wh/kg (HIGH), 4C no plating (HIGH), SEI <= 550nm at 45C/100cyc (MEDIUM), nail 10W no TR (HIGH). Trade-offs: ED vs rate capability (thick electrode raises ED but increases plating risk); ED vs thermal safety (less thermal mass = more TR risk).",
    "candidate_strategy": "Round 1: baseline characterization + ceiling assessment. Rounds 2-4: architecture variants (thicker electrode, thinner separator, thinner CC, optimized porosity). Rounds 5-8: aging + safety screening of survivors. Rounds 9+: fine-tuning.",
    "budget_allocation": "1 round baseline + 3-4 architecture + 2-3 safety/aging + 0-2 fine-tuning = 6-10 total rounds",
    "risk_and_fallback": "Risk1: Chen2020 ED ceiling < 327.18 -> escalate to Stage 2. Risk2: 4C plating at high ED -> reduce thickness or smaller particles. Risk3: SEI > 550nm at 45C -> no material lever -> report negative. Risk4: nail TR -> reduce stored energy.",
    "detail": "design_plan.md"
}

append_entry(ws, plan_entry)
print("Plan entry written")
