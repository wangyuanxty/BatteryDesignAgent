"""Write plan update entry."""
import os, sys
os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
sys.path.insert(0, "D:/research/degradation_prognostics/Battery_Design_Agent")
from bda.store import append_entry, CaseWorkspace

ws = CaseWorkspace("t7_r1_mimo", "D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")

update_entry = {
    "action": "plan",
    "update": True,
    "reason": "ceiling_escalation triggered: baseline ED=400 Wh/kg exceeds target (327.18), so no material escalation needed. Primary failure is 4C plating. Architecture exploration converged: V_K (45% porosity, 8um separator, 3um particles) achieves anode_min=+0.0047V (no plating) with ED=419 Wh/kg. Proceeding to aging + nail safety validation for V_K.",
    "candidate_strategy": "V_K_extreme_transport selected as Top-1 candidate: positive/negative porosity=0.45, separator thickness=8um/porosity=0.65, particle radius=3um. Running aging 45C and nail penetration to complete evaluation.",
    "budget_allocation": "Rounds 1-2: architecture exploration (completed, V_K identified). Rounds 3-4: V_K aging + nail safety (in progress). Expected completion in 2-3 more rounds.",
    "risk_and_fallback": "V_K high porosity (0.45) reduces active material fraction — need to verify aging/SI behavior. If nail TR triggers on V_K → explore even thinner electrodes or different separator."
}

append_entry(ws, update_entry)
print("Plan update written")
