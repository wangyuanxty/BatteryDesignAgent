"""Write Stage 1 plan entry to log.jsonl."""
import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t7_r1_noforce", "D:/research/degradation_prognostics/Battery_Design_Agent/runs")
entry = {
    "action": "plan",
    "objective_breakdown": (
        "HEV cell, four contract metrics: ED>=327.18 Wh/kg (stage2, calc-energy caliber, electrolyte excluded); "
        "4C charge at 45C without plating (stage3, min(anode_potential_v)>=0 V); "
        "SEI<=550 nm after 100 cycles at 45C (stage2, aging_1C_100cyc_45C sei_thickness_nm_end); "
        "nail 10 W without thermal runaway (stage3, run-tr triggered=false, t_init=T_max_K of 4C charge, mass from calc-energy). "
        "T_max_K recorded but unjudged (no task-text red line). "
        "Trade-off expectation: ED vs 4C plating (thicker electrodes raise ED but worsen transport); "
        "nail vs mass (small cell ~43 g -> mcp~39 J/K, 10 W nail is significant)."
    ),
    "candidate_strategy": (
        "R1: baseline Chen2020 characterization (all protocols) + Ceiling Probe A (Cu 6um/Al 10um CC, sep 10um, "
        "high-transport electrolyte sigma~2x/t+ 0.5/D~2x, all bridge values domain estimates) to bound the best-possible "
        "Chen2020-system ED and 4C margin. Opening ceiling assessment after R1: if ceiling<327.18 -> escalate to Stage 2 "
        "system switch (OKane2022 SiOx, aging-capable). R2+: targeted fixes per failing metric via symptom-to-scale "
        "mapping (SEI->coating/electrode modification; plating->N/P, particle radius, porosity, transport; nail->hA/thermal; "
        "ED->mass reduction then system switch). exploration_force OFF: variants only when a metric demands them."
    ),
    "budget_allocation": (
        "R1: baseline (1C spme+dfn, calc-energy, 4C@45C dfn+plating, aging45C, run-tr) + ceiling probe (1C dfn, calc-energy, "
        "4C@45C dfn+plating, run-tr) ~9 sims. R2-R5: 1-3 sims per targeted round. Closing: endorse-skip (real_compute=false), "
        "final, render, deliverables. No round cap: iterate until achieved or turn budget exhausted."
    ),
    "risk_and_fallback": (
        "ED low -> mass reduction then Stage 2 system switch; plating -> dfn verification, particle/N-P/transport levers; "
        "SEI>550 -> SEI kinetic rate constant reduction (coating, same-system comparison); nail triggered -> hA/thermal levers "
        "then boundary questioning. Three-strike rule with layer-by-layer assumption questioning recorded in final escalation field. "
        "Chen2020 first-cycle capacity known-low (initial state discharged) - not compared."
    ),
    "detail": "design_plan.md",
}
append_entry(ws, entry)
print("plan entry appended; total entries:", len((ws.path / "log.jsonl").read_text(encoding="utf-8").strip().splitlines()))
