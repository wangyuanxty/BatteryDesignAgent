"""t4_r3 Stage 1: write plan entry + start-at-stage-3 funnel/baseline record into log.jsonl."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")

plan = {
    "action": "plan",
    "objective_breakdown": (
        "stage2: -20C 1C retention >= 95% (mechanical = 100 x cap(253.15K 1C)/cap(298.15K 1C)); "
        "ED >= 327.18 Wh/kg and vol-ED >= 880 Wh/L (calc-energy contract caliber, electrolyte excluded); "
        "stage3: T_max <= 333.15 K (4C@45C, task-silent default red line), plated=false. "
        "Multi-objective trade-off: low-T retention wants thin/high-porosity/small-particle/high-transport; "
        "the two density targets want thick/dense/low-porosity -> retention headroom first, then density recovery."
    ),
    "candidate_strategy": (
        "R1 baseline Chen2020 (empty params: 1C, lowT, 4C45+lumped+plating, calc-energy) feeding the opening "
        "ceiling assessment; R2+ transport-first formulation overrides (sigma/D/t+ via parameter bridge) plus "
        "architecture variants (thickness/porosity/particle radii/separator) 2-4 per round; density recovery "
        "after retention secured; DFN confirmation for finalists; escalate to Stage 2 only if density ceiling "
        "or retention plateau demands material design (ceiling_escalation ON)."
    ),
    "budget_allocation": (
        "R1 baseline fixed (4 sims + calc-energy); R2-6 formulation+architecture screening (SPMe, 2-4/round); "
        "R7-9 density recovery + DFN confirmations; R10+ safety gate, final entry, deliverables. "
        "real_compute=false -> endorse records skip, no true DFT/MD."
    ),
    "risk_and_fallback": (
        "Retention plateaus <95% -> three-strike questioning (T-dependence of Chen2020 lives mostly in electrolyte "
        "transport; residual gap possibly model-limited -> honest negative result with 'reachable if' statement); "
        "ED failures -> density recovery variants then ceiling_escalation to Stage 2; safety failures -> "
        "thickness buffer / cooling h; solver errors recorded verbatim, SPMe<->DFN fallback automatic."
    ),
    "detail": "design_plan.md",
}
append_entry(ws, plan)
print("plan entry written")

funnel_note = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "start_stage=3: this case starts at Stage 3 cell design; materials use system baseline "
        "(source: baseline/literature-values embedded in the chosen parameter set, not a funnel screening). "
        "Base determination (SKILL 1.5 anchor table): task text names no electrode system -> default Chen2020; "
        "discriminant anchor verified by parameter dump param_dump_chosen.json — negative OCP = "
        "graphite_LGM50_ocp_Chen2020 (pure graphite, no SiOx keys -> Chen2020, not OKane2022), positive max "
        "concentration 63104 mol/m3 (NMC811), nominal 5 Ah, laptop geometry. Established before any run."
    ),
}
append_entry(ws, funnel_note)
print("funnel (stage-3-start) entry written")

print("log.jsonl tail:")
for line in (ws.path / "log.jsonl").read_text(encoding="utf-8").splitlines():
    print(line[:160])