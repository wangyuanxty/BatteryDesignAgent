# -*- coding: utf-8 -*-
"""t8_r2 log initialization: entry 0 (criteria+meta), plan, funnel(start_stage=3), propose R1."""
import sys
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t8_r2", "runs/exp")
assert ws.path.exists(), ws.path

entry0 = {
    "criteria": {
        "stage1": {
            # molecular-level elimination lines (protocol defaults; used if/when Stage 2 material screen runs)
            "max_energy_ev": {"max": 0.0},
            "max_homo_ev": {"max": -6.0},
        },
        "stage2": {
            "energy_density_wh_kg": {"min": 446.18},
            "retention_5c": {"min": 0.9},
            "mass_kg": {"max": 0.04},
        },
        "stage3": {
            "plated": False,
        },
        "meta": {
            "task": "Design a battery for a long-endurance drone: energy density >= 446.18 Wh/kg, 5C discharge with >= 90% capacity retention, cell mass <= 40 g",
            "task_parsed": {
                "energy_density_wh_kg": {"min": 446.18, "definition": "calc-energy contract-caliber (V*I_1C integral / layer-stack mass, electrolyte excluded)"},
                "retention_5c": {"min": 0.9, "definition": "capacity_ah(5C_discharge dfn) / capacity_ah(1C_discharge, same params), mechanically derived to derived JSON"},
                "mass_kg": {"max": 0.04, "definition": "calc-energy mass_kg (layer stack x electrode area); 40 g = 0.04 kg"},
            },
            "start_stage": 3,
            "start_stage_basis": "task text names no materials/additives/electrolyte design -> start at Stage 3 cell design (SKILL Sec.0 rule 2); ceiling_escalation ON may proactively escalate to Stage 2",
            "base_params_initial": "Chen2020",
            "base_basis": "no electrode system named in task -> anchor-table default Chen2020 (SKILL Sec.1.5); discriminant verified by parameter dump: NMC811 positive (AMVF 0.665, density 3262 kg/m3), pure-graphite negative (density 1657 kg/m3, no SiOx keys)",
            "real_compute": False,
            "ablation": {
                "exploration_force": "ON (default; task names no ablation)",
                "ceiling_escalation": "ON (default; task names no ablation)",
                "funnel_voting": "ON (default; task names no ablation)",
            },
            "freedoms": {
                "electrode_system": "adjustable (widest interpretation; task names no system)",
                "electrolyte_formulation": "adjustable (widest interpretation; sigma/t+/D transport overrides via parameter bridge)",
                "electrode_modification": "adjustable (widest interpretation)",
                "cell_architecture": "adjustable (widest interpretation; includes electrode height/width area to satisfy the mass cap, thickness/porosity/N-P/separator/collectors/particle size)",
                "thermal_management": "adjustable (widest interpretation; cooling coefficient and cooling surface area)",
            },
            "stage3_scope": "Stage-4 safety exam = 4C charge at 45 C, lumped thermal + plating module (protocol default); task has no overcharge/nail/thermal-runaway objective",
            "notes": "zero-interaction (headless) execution: thresholds parsed verbatim from task text, no clarification; exclusions honored: solid-phase conductivity/diffusivity, initial lithiation, initial SEI, charge cut-off are not design levers",
        },
    }
}

plan = {
    "action": "plan",
    "objective_breakdown": "ED>=446.18 Wh/kg (calc-energy contract caliber) binds stack composition (active/inactive mass ratio + mean voltage); retention_5c>=0.9 binds rate capability (particles/thickness/electrolyte transport) - the two form a Pareto pair (thick electrodes raise ED, hurt 5C); mass<=40 g is area-scalar while ED/retention are area-independent ratios -> area is the free mass lever (baseline stack ~43.5 g at 0.1027 m2; no capacity target in task)",
    "candidate_strategy": "R1 baseline characterization (Chen2020, no overrides; 1C SPMe->DFN, calc-energy, 5C DFN, 4C-charge-45C safety DFN) + opening ceiling assessment; R2-R4 architecture+formulation variants (thin collectors/separator, porosity trim, thickness rebalance, particle trim, high-transport electrolyte sigma/D/t+); if ceiling assessment shows 446.18 unreachable in NMC811/graphite envelope -> escalate Stage 2 (OKane2022 graphite+SiOx system, then cathode composition); best variant re-verified at 5C + 4C safety exam each round",
    "budget_allocation": "R1: 4 sims; R2-R6: ~4 variants x 4 sims = ~16; up to +2 rounds for system switch; total <=8 rounds / ~30 sims, all second-to-minute scale; real_compute=false -> Stage 5 true-compute endorsement skipped and recorded",
    "risk_and_fallback": "R1 ED ceiling of NMC811/graphite -> Stage 2 escalation (SiOx anode / cathode composition) -> if still short, three-strike questioning and honest negative close with 'reachable if relaxed to X' note (never relax threshold); R2 5C retention short -> mass-neutral transport levers first, then particles/porosity/thickness; R3 plating at 4C charge -> transport + negative particle trim + N/P tune; R4 mass>40g -> reduce electrode area then re-run calc-energy; fallback routing by symptom scale (architecture->Stage 3, material limit->Stage 2)",
    "detail": "design_plan.md",
}

funnel_start = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "detail": "start_stage=3: no molecular screen in this case; materials use system baseline parameters. Base determined by anchor table (SKILL Sec.1.5): task text names no electrode system -> default Chen2020; verified by parameter-set dump (NMC811 AMVF 0.665 / density 3262, pure graphite density 1657, no SiOx). Props source = baseline (published literature parameterization, Chen et al. JES 167 (2020) 080534). Ceiling assessment to follow after R1 baseline measurement.",
}

propose1 = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "name": "Baseline Chen2020",
            "role": "baseline characterization: 1C discharge (SPMe screen then DFN), calc-energy, 5C discharge DFN, 4C-charge-45C lumped-thermal + plating DFN; no parameter overrides",
            "struct": {},
        }
    ],
    "llm_reason": "Measure the untouched Chen2020 envelope first: contract ED gap to 446.18, 5C retention, 43.5 g baseline mass vs 40 g cap, and the 4C-charge plating state; the measured gap calibrates whether architecture/formulation levers alone can close it or material escalation (SiOx) is required - informed fallback routing per protocol.",
}

if ws.path.joinpath("log.jsonl").exists():
    print("log.jsonl already exists - refusing to re-init", file=sys.stderr)
    sys.exit(1)

append_entry(ws, entry0)
append_entry(ws, plan)
append_entry(ws, funnel_start)
append_entry(ws, propose1)
print("wrote entry0 + plan + funnel + propose R1 to", ws.path / "log.jsonl")