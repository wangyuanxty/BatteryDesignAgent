import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
ws = CaseWorkspace("exp/t5_r1_singlemodel", "runs")

plan_entry = {
    "action": "plan",
    "objective_breakdown": (
        "ED >= 500.94 Wh/kg (stage2; calc-energy contract formula = discharge energy / sum of layer masses, "
        "electrolyte excluded from mass). 4C fast charge at 45 C: plated=false (anode_potential_v >= 0 V at all "
        "times; stage3) and T_max <= 60 C = 333.15 K (stage3; 4C_charge_45C protocol, thermal lumped). "
        "Multi-objective Pareto: thick/high-loading electrodes raise ED but hurt 4C rate capability; mass cuts "
        "(thin current collectors/separator, electrode thinning) raise ED but concentrate heat and raise current "
        "density; electrolyte transport (sigma/D/t+) and particle size relieve both plating and T_max; cooling h "
        "is a pure T_max lever with zero ED cost (thermal-management DOF)."
    ),
    "candidate_strategy": (
        "R1 (Stage 3 start): Chen2020 baseline (anchor-table default - task text names no explicit electrode "
        "system) + OKane2022 system candidate (native plating/stripping/cracking parameters) + 3 architecture "
        "probes on OKane2022: archA ED-max (CC 8/6 um, separator 10 um, porosities 0.28/0.22), archB 4C-safety "
        "(sigma 2.2 S/m, D 7.5e-10 m2/s, t+ 0.45, particle radii halved, cooling h 10->40), archC mass-cut "
        "(electrode thickness -15%). Opening ceiling assessment after R1: if NMC811/graphite ED ceiling "
        "< 500.94 -> Stage 2 escalation (LNMO 4.7 V system, run-comp high-capacity cathode compositions, "
        "mace-only funnel molecules per funnel_voting OFF). Subsequent rounds: 2-4 architecture variants per "
        "round (exploration_force ON), per-candidate safety exam, combine round winners."
    ),
    "budget_allocation": (
        "R1-2: baseline + ceiling assessment + system selection; R3-6: ED push (material escalation + mass "
        "cuts); R7-10: 4C plating / T_max fine-tuning; R11+: DFN confirmation, deliverables, render, "
        "verify-deliverables. SPMe screens (seconds), DFN for passers and all 4C safety judgments; calc-energy "
        "on every discharge candidate."
    ),
    "risk_and_fallback": (
        "A. ED ceiling < 500.94 in architecture space -> Stage 2 escalation (LNMO system switch / run-comp "
        "compositions / formulation bridge). B. 4C plating -> transport bridge (sigma/D/t+), small particles, "
        "thin electrodes, N/P ratio; use OKane2022 native plating model for judgments. C. T_max > 333.15 K -> "
        "cooling h escalation (10 -> 40+) and DCR reduction. D. Chen2020 has no native plating parameters "
        "(standard defaults injected at runtime) -> prefer OKane2022 for final safety judgment. E. Three strikes "
        "on the same failure cause -> question model/system, task boundary, and metric assumptions; honest "
        "negative result with relaxation note."
    ),
    "detail": "design_plan.md",
}

funnel_entry = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "detail": (
        "start_stage=3 (starting-point rule: task text names no new materials/additives/electrolyte design -> "
        "cell-design stage; materials use system baseline). Base determination: task text names no explicit "
        "electrode system -> anchor-table deterministic default Chen2020 (NMC811/graphite). Verified by parameter-"
        "set dump: negative OCP = graphite_LGM50_ocp_Chen2020, positive OCP = nmc_LGM50_ocp_Chen2020, Nominal "
        "cell capacity 5 Ah, complete thermal/geometry parameter set (no injections needed). Note: OKane2022 in "
        "this PyBaMM build shares the same NMC811/graphite geometry (negative electrode density 1657 kg/m3, no "
        "SiOx secondary phase - the anchor-table SiOx discriminant is absent in this build; recorded honestly); "
        "OKane2022 adds native plating/stripping + cracking + SEI-on-cracks parameters. Props source: baseline "
        "(literature parameterization). No molecular candidates this round; funnel_voting OFF -> run-mlp(mace) "
        "only if molecules are proposed in later rounds."
    ),
}

propose_entry = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "base": "Chen2020",
            "name": "baseline_Chen2020",
            "role": "anchor-table default system baseline (NMC811/graphite); 1C discharge + calc-energy + 4C safety characterization",
        },
        {
            "base": "OKane2022",
            "name": "sys_OKane2022",
            "role": "system switch candidate: same NMC811/graphite geometry but native plating/stripping/cracking parameters - better 4C plating judgment vehicle",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 1e-5,
                "Positive electrode porosity": 0.28,
                "Negative electrode porosity": 0.22,
            },
            "name": "archA_EDmax",
            "role": "ED-max probe on OKane2022: thin CC (Al 8um/Cu 6um) + thin separator (10um) + porosity cut -> mass reduction + active fraction up",
        },
        {
            "struct": {
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 7.5e-10,
                "Cation transference number": 0.45,
                "Positive particle radius [m]": 2.6e-6,
                "Negative particle radius [m]": 2.9e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
            },
            "name": "archB_4Csafe",
            "role": "4C-safety probe on OKane2022: high-transport electrolyte bridge + halved particle radii + strong cooling h=40",
        },
        {
            "struct": {
                "Positive electrode thickness [m]": 6.4e-5,
                "Negative electrode thickness [m]": 7.2e-5,
            },
            "name": "archC_thin",
            "role": "mass-cut probe on OKane2022: electrode thickness -15% (capacity risk vs mass gain at fixed 5 A)",
        },
    ],
    "llm_reason": (
        "No explicit system in task text -> Chen2020 default baseline per anchor table (recorded). OKane2022 "
        "proposed as system candidate: native plating model makes the 4C plating judgment model-consistent. "
        "archA probes the ED-max direction (thin CC/separator + porosity cut); archB probes the safety floor "
        "(transport bridge + kinetics + cooling); archC probes electrode thinning as pure mass cut. Electrolyte "
        "values are domain estimates (marked estimate): sigma 2.2 S/m ~2x Nyman2008 room-T value, D 7.5e-10 "
        "m2/s ~2x baseline, t+ 0.45 from 0.2594 - plausible advanced-formulation targets, not simulation "
        "output. Particle radii halved (5.22->2.6 um pos, 5.86->2.9 um neg). h 10->40 W/m2/K = aggressive "
        "liquid cooling (thermal-management DOF)."
    ),
}

for e in (plan_entry, funnel_entry, propose_entry):
    append_entry(ws, e)
print("plan + funnel + propose(round 1) written to", ws.path / "log.jsonl")
