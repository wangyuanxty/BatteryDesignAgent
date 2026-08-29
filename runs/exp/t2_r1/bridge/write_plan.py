"""Append Stage-1 plan entry + start_stage=3 funnel entry to log.jsonl."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")

plan = {
    "action": "plan",
    "objective_breakdown": (
        "stage2: ED>=327.18 Wh/kg (calc-energy contract), SEI<=500 nm @100cyc & <=550 nm @500cyc "
        "(aging_1C_100cyc), lowT retention>=90% (lowT/1C capacity ratio, same params); "
        "stage3: plated=false at 4C charge 45C. Expected trade-offs: N/P up helps plating but costs ED; "
        "thin electrodes help lowT but cost ED; electrolyte transport sigma/D up helps plating+lowT at no ED cost "
        "(first-priority lever); SEI kinetics (coating) has no ED cost."
    ),
    "candidate_strategy": (
        "R1 baseline Chen2020 full sweep (1C SPMe/DFN+calc-energy, lowT, aging 100 & 500, 4C_charge_45C DFN lumped+plating) "
        "-> gap vector. Expected gaps: 4C plating (graphite), lowT retention<90% (Nyman2008 T-dependence), "
        "SEI@500>550 (baseline 100cyc ~449 nm reference). Lever ladder: plating -> r_neg down, sigma_e up, N/P up, porosity up; "
        "lowT -> sigma/D formulation overrides (weak T-dependence), porosity, particle radius, thin electrodes; "
        "SEI -> anode ALD-Al2O3-type coating k_sei down (+j_SEI branch); ED -> thin collectors/separator, thick electrodes, N/P rebalance; "
        "ED ceiling shortfall -> Stage 2 escalation (system switch, e.g. OKane2022 SiOx)."
    ),
    "budget_allocation": (
        "R1 baseline sweep; R2-4 architecture+transport variants; R5 SEI-kinetics variants; R6 final verification sweep; "
        "real_compute=false (no true DFT/MD)."
    ),
    "risk_and_fallback": (
        "lowT may hit model limits -> three-strike questioning (system/boundary/metric) recorded in final.escalation if hit; "
        "ED artifact (Chen2020 initial state cathode 27% lithiated) is systematic -> ceiling assessment decides "
        "Stage 2 escalation (system switch) vs architecture tuning; 4C plating if cell-scale levers insufficient -> "
        "Stage 2 escalation (electrolyte/system); failures read verbatim and recorded; every propose round gets a "
        "same-round log-evaluate; no threshold relaxation."
    ),
    "detail": "design_plan.md",
}

funnel = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "start_stage=3: molecular screening skipped; materials use system baseline. "
        "Base determination: task text names no electrode system -> anchor-table default Chen2020; "
        "discriminant verified by parameter dump before entry 0 (NMC811/graphite OCP functions "
        "nmc_LGM50_ocp_Chen2020 / graphite_LGM50_ocp_Chen2020; 'SEI kinetic rate constant [m.s-1]' present -> "
        "aging-capable). props source: baseline (literature parameter set, Chen2020 JES 167 080534)."
    ),
}

append_entry(ws, plan)
append_entry(ws, funnel)
print("plan + funnel entries appended")
