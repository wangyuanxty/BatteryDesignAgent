import json, sys
sys.path.insert(0, ".")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t2_r1_mimo", "runs/exp/t2_r1_mimo")

# Rewrite entry 0 with corrected criteria
entry0 = {
    "criteria": {
        "stage1": {},
        "stage2": {
            "energy_density_wh_kg": {"min": 327.18},
            "sei_thickness_nm_end_100cyc": {"max": 500},
            "sei_thickness_nm_end_500cyc": {"max": 550},
            "capacity_retention_lowT_pct": {"min": 90.0}
        },
        "stage3": {"plated": False, "T_max_K": {"max": 350}},
        "meta": {
            "real_compute": False,
            "base_params": "Chen2020",
            "start_stage": 3,
            "ablation": {"exploration_force": True, "ceiling_escalation": True, "funnel_voting": True}
        }
    },
    "action": "entry0",
    "task": "Grid energy storage battery design",
    "objectives": ["ED >= 327.18 Wh/kg", "4C fast charge no plating", "SEI <= 500 nm @100 cyc", "capacity retention >= 90% @-20C", "SEI <= 550 nm @500 cyc"]
}

# Clear and rewrite log.jsonl
with open("runs/exp/t2_r1_mimo/log.jsonl", "w", encoding="utf-8") as f:
    f.write(json.dumps(entry0, ensure_ascii=False) + "\n")

# Re-add plan entry
plan = {
    "action": "plan",
    "objective_breakdown": "ED>=327.18 is achievable (baseline=400). Critical failures: 4C plating (anode_potential_v min=-0.439V) and SEI@500 (778nm>550nm). Low-T retention (99.4%) and SEI@100 (449nm) already pass.",
    "candidate_strategy": "R1 baseline done. R2: thin-electrode variants to reduce plating. R3-R5: iterate on thickness/NP/particle size. If still failing: consider electrolyte transport modification.",
    "budget_allocation": "~15 rounds: 1 baseline, 10 architecture, 4 safety/aging",
    "risk_and_fallback": "Chen2020 may have high SEI growth rate (material limitation). If architecture alone cannot fix SEI@500, escalate to electrode modification.",
    "detail": "design_plan.md"
}
append_entry(ws, plan)

# Round 1 propose
propose = {
    "action": "propose",
    "round": 1,
    "candidates": [{"name": "Chen2020 baseline", "role": "NMC811/graphite baseline characterization"}],
    "llm_reason": "Baseline characterization: establish which metrics pass/fail. ED=400 (pass), Low-T=99.4% (pass), SEI@100=449nm (pass), 4C plating=yes (FAIL), SEI@500=778nm (FAIL)."
}
append_entry(ws, propose)

# Round 1 evaluate (manually constructed with all metrics)
eval_entry = {
    "action": "evaluate",
    "round": 1,
    "metrics": {
        "energy_density_wh_kg": 400.29,
        "capacity_retention_lowT_pct": 99.43,
        "sei_thickness_nm_end_100cyc": 449.1,
        "sei_thickness_nm_end_500cyc": 777.9,
        "plated": True,
        "T_max_K": 332.35
    },
    "verdict": "fail",
    "evidence": [
        {"metric": "energy_density_wh_kg", "value": 400.29, "threshold": {"min": 327.18}, "verdict": "pass", "source": "cell/r1_baseline_energy.json:energy_density_wh_kg"},
        {"metric": "capacity_retention_lowT_pct", "value": 99.43, "threshold": {"min": 90.0}, "verdict": "pass", "source": "computed: 4.9196/4.9478*100"},
        {"metric": "sei_thickness_nm_end_100cyc", "value": 449.1, "threshold": {"max": 500}, "verdict": "pass", "source": "cell/r1_baseline_aging100.json:sei_thickness_nm_end"},
        {"metric": "sei_thickness_nm_end_500cyc", "value": 777.9, "threshold": {"max": 550}, "verdict": "fail", "source": "cell/r1_baseline_aging500.json:sei_thickness_nm_end"},
        {"metric": "plated", "value": True, "threshold": False, "verdict": "fail", "source": "cell/r1_baseline_4c.json:anode_potential_v (min=-0.439V<0 derived)"},
        {"metric": "T_max_K", "value": 332.35, "threshold": {"max": 350}, "verdict": "pass", "source": "cell/r1_baseline_4c.json:T_max_K"}
    ],
    "note": "Baseline passes ED/LowT/SEI@100 but fails 4C plating and SEI@500.",
    "candidate": "Chen2020 baseline"
}
append_entry(ws, eval_entry)

print("All R1 entries written correctly")
