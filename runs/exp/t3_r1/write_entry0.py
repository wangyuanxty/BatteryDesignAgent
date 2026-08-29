# Entry-0 / plan / funnel / round-1 propose writer (agent-built input writer; runs once).
# All log writes go through bda.store.append_entry per SKILL.md (no self-built appenders).
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")

TASK = ("Design a battery for power tools: nominal capacity >= 2 Ah, support 5C discharge "
        "(capacity retention >= 95%), support 4C fast charge (no lithium plating), maximum "
        "temperature <= 60C, power density >= 4000 W/kg.")

entry0 = {
    "criteria": {
        # stage1 = molecular-level goals / elimination lines: no molecular candidates in this
        # case (start_stage=3, materials use system baseline) -> empty by faithful parse.
        "stage1": {},
        "stage2": {
            "capacity_ah": {"min": 2.0},
            "retention_5c": {"min": 0.95},
            "power_density_w_kg": {"min": 4000.0},
        },
        "stage3": {
            "T_max_K": {"max": 333.15},  # 60 degC = 333.15 K (mechanical conversion)
            "plated": False,
        },
        "meta": {
            "case": "t3_r1 power-tool battery",
            "task_text": TASK,
            "start_stage": 3,
            "base": "Chen2020",
            "base_basis": ("task text names no electrode system -> anchor-table default Chen2020 "
                           "(NMC811/graphite baseline teaching parameterization); dump verified: no SiOx "
                           "keys (not OKane2022), SEI kinetic rate constant present, complete "
                           "thermal/geometry parameters present, nominal capacity 5.0 Ah"),
            "real_compute": False,
            "thermal": "lumped",
            "freedoms": {
                "electrode_system": "adjustable (default Chen2020; task text declares none -> widest interpretation)",
                "electrolyte_formulation": "adjustable (transport parameter overrides via parameter bridge)",
                "electrode_modification": "adjustable (SEI/cracking parameter overrides; not exercised unless needed)",
                "cell_architecture": "adjustable (thickness/porosity/N-P/separator/current collector/particle size)",
                "thermal_management": "adjustable (Total heat transfer coefficient [W.m-2.K-1])",
            },
            "measurement_notes": {
                "discharge_initial_state": ("Chen2020 initial state is discharged (positive electrode 27% "
                                            "lithiated, known artifact). 1C/5C discharge protocols run with "
                                            "initial concentrations overridden to fully-charged state "
                                            "(pos=63104, neg=994 mol/m3) to measure nominal capacity from "
                                            "100% SOC. Identical override for all candidates - a measurement "
                                            "precondition, not a design lever."),
                "T_max_K_scope": ("T_max criterion judged on the maximum of the lumped-thermal outputs of "
                                  "the 5C-discharge (25C ambient) and 4C-charge (45C ambient) protocols "
                                  "(mechanically derived, written to cell/*_derived.json)."),
                "retention_5c_definition": ("5C discharge capacity / 1C discharge capacity, same parameters, "
                                           "charged initial state (mechanically derived)."),
                "capacity_measure": ("capacity_ah from 1C DFN discharge (charged initial state); "
                                     "calc-energy contract formula for power density: "
                                     "V_OC^2/(4*DCR)/mass, mass = sum(layer thickness*(1-porosity)*density*area)."),
            },
        },
    }
}

plan = {
    "action": "plan",
    "objective_breakdown": (
        "Power-tool battery: capacity >=2 Ah (stage2), 5C retention >=95% (stage2), 4C fast charge "
        "plating-free (stage3), T_max <=60 C/333.15 K (stage3), power density >=4000 W/kg (stage2, "
        "calc-energy contract). Trade-off map: power density ~1/L^2 with electrode thickness while "
        "capacity ~L -> power-tool cell pushes thin while holding >=2 Ah; 5C retention aligned with "
        "thin+small-particles+high-kappa electrolyte; plating suppressed by N/P margin + small anode "
        "particles + fast electrolyte (aligned with rate capability, costs capacity); T_max binding "
        "case is 4C charge at 45 C ambient (only ~15 K headroom) -> DCR reduction + cooling h design."
    ),
    "candidate_strategy": (
        "Round 1 baseline characterization (Chen2020 defaults + artifact-documentation run). Round 2 "
        "single-lever architecture variants (thin electrodes / small particles / fast electrolyte / "
        "thin CC+separator / raised h). Rounds 3+ composites of passing levers, refinement on the "
        "binding metric. Ceiling assessment after rounds 1-2; transport-bound gap -> escalate to "
        "Stage 2 electrolyte formulation / system switch, not more tuning."
    ),
    "budget_allocation": (
        "~10 rounds; per candidate 1C DFN + 5C DFN + 4C-charge DFN (lumped+plating) + calc-energy + "
        "derived metrics + batch log-evaluate; SPMe only for quick screens."
    ),
    "risk_and_fallback": (
        "Power density 4000 W/kg aggressive for 5-Ah class -> three-strike questioning then honest "
        "negative result with reachability note. Plating -> N/P up, anode particles down, t+/kappa/D "
        "up. 5C retention <95% -> thinner electrodes/particles, kappa up. T_max >333.15 K -> h up, "
        "DCR down. Capacity <2 Ah -> stop thinning."
    ),
    "detail": "design_plan.md",
}

funnel_start3 = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "start_stage=3: no molecular screening in this case; materials use system baseline. "
        "Base determination: task text names no electrode system -> anchor-table default Chen2020 "
        "(NMC811/graphite). Dump verification: no SiOx keys (not OKane2022), SEI kinetic rate "
        "constant present, complete thermal/geometry parameters, nominal capacity 5.0 Ah. "
        "Props source marked: baseline (parameter set literature values)."
    ),
}

propose_r1 = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "struct": {},
            "name": "Baseline",
            "role": "baseline characterization of Chen2020 defaults (1C/5C discharge, 4C charge 45C+plating, calc-energy)",
        }
    ],
    "llm_reason": (
        "Round 1 anchors all gaps vs criteria on the unmodified Chen2020 system; discharged-initial-"
        "state artifact documented with an as-is 1C run alongside the charged-state measurements."
    ),
}

for entry in (entry0, plan, funnel_start3, propose_r1):
    append_entry(WS, entry)
print("wrote", len(Path(WS.path, "log.jsonl").read_text(encoding="utf-8").splitlines()), "lines to", WS.path / "log.jsonl")
