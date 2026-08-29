# -*- coding: utf-8 -*-
"""t7_r2: write log.jsonl entry 0 (criteria+meta), Stage-1 plan entry, funnel note.
Uses bda.store.append_entry exclusively (library API, canonical serialization)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t7_r2", "runs")

entry0 = {
    "criteria": {
        "stage1": {},
        "stage2": {
            "energy_density_wh_kg": {"min": 327.18},
            "sei_thickness_nm_end": {"max": 550},
        },
        "stage3": {
            "plated": False,
            "triggered": False,
        },
        "meta": {
            "case_id": "t7_r2",
            "task_text": ("Design a battery for a hybrid electric vehicle: energy density >= 327.18 Wh/kg, "
                          "4C fast charge without lithium plating, SEI <= 550 nm after 100 cycles at 45C, "
                          "nail penetration (10 W short-circuit heat generation) without triggering thermal runaway"),
            "real_compute": False,
            "ablation_switches": {"exploration_force": "on", "ceiling_escalation": "on", "funnel_voting": "on"},
            "freedoms": {
                "electrode_system": "adjustable",
                "electrolyte_formulation": "adjustable",
                "electrode_modification": "adjustable",
                "cell_architecture": "adjustable",
                "thermal_management": "adjustable",
            },
            "freedoms_basis": ("zero-interaction rule: no degree-of-freedom category declared in task text -> "
                               "widest interpretation for all five categories (t1_r1 lesson: undeclared electrolyte "
                               "adjustability must not default to locked)"),
            "start_stage": 3,
            "base_params": "Chen2020",
            "base_determination": ("task text names no electrode system -> anchor-table deterministic default Chen2020 "
                                   "(recorded). Dump verified before use: Chen2020 carries full thermal/geometry keys "
                                   "(Electrode height 0.065 m x width 1.58 m; CC 1.6e-5/1.2e-5 m; Separator 1.2e-5 m; "
                                   "Cell volume 2.42e-5 m3) and SEI kinetics (SEI kinetic rate constant 1e-12 m/s, "
                                   "SEI reaction exchange current density 1.5e-7 A/m2) -> aging-capable, no injected "
                                   "defaults needed. props source = baseline (literature parameterization)."),
            "protocol_anchor": {
                "energy_density": "calc-energy contract formula (ED = energy_wh / mass_kg; electrolyte excluded, annotated)",
                "fast_charge_4c": "run-pyamm --protocol 4C_charge_45C --thermal lumped --plating; plated = min(anode_potential_v) < 0 V (mechanical)",
                "aging_45c": "run-pyamm --protocol aging_1C_100cyc_45C; sei_thickness_nm_end (mechanical)",
                "nail": ("run-tr --q-nail 10 --mass-kg <calc-energy mass_kg>; triggered mechanical (dT/dt>1 K/s or "
                         "T>=573 K); hA = designed cooling h x Cell cooling surface area; near-adiabatic default "
                         "hA=0.05 W/K also recorded as unfavorable-condition check (paired boundary declaration)"),
            },
            "notes": ("No T_max red line, no capacity/voltage threshold, no 5C or low-T retention in task text -> "
                      "not criteria. No cell mass/dimension constraint declared. Nail at protocol defaults "
                      "t-init=298.15 K / t-amb=298.15 K / t-max=3600 s (task text sets only q=10 W)."),
        },
    }
}

plan_entry = {
    "action": "plan",
    "objective_breakdown": (
        "Four adjudicable metrics -> decision layers. (1) ED >= 327.18 Wh/kg [stage2, calc-energy contract formula, "
        "electrolyte excluded]: improved by cutting inactive mass (thinner current collectors/separator, lower porosity "
        "had to be balanced against transport). (2) SEI <= 550 nm after 100 x 1C cycles at 45 C [stage2, "
        "sei_thickness_nm_end]: controlled by anode SEI kinetics (coating bridge params). (3) 4C fast charge no plating "
        "[stage3, plated=false mechanical from anode_potential_v]: levers = anode design (N/P, particle size, porosity), "
        "electrolyte transport (sigma/t+), possibly SiOx system OCP shift. (4) Nail 10 W no thermal runaway "
        "[stage3, triggered=false mechanical run-tr]: levers = cell thermal mass, cooling h. Expected trade-offs: "
        "thicker electrodes/less inert material raise ED but worsen 4C rate capability (plating) - the central Pareto "
        "tension of this case; higher cooling h helps both 4C temperature and nail, no penalty to other metrics "
        "(HEV pack liquid cooling). T_max has no red line in task text -> not a criterion, still recorded."
    ),
    "candidate_strategy": (
        "R1: baseline Chen2020 full suite (1C DFN + calc-energy; 4C@45C lumped+plating DFN; aging_1C_100cyc_45C SPMe; "
        "nail run-tr q=10 W) + opening ceiling assessment: best-possible Chen2020 architecture vs 327.18 Wh/kg. "
        "If gap -> escalate to Stage 2 system candidate OKane2022 (NMC811/graphite+SiOx with cracking model, "
        "aging-capable; anchor table row for SiOx-containing negative) - system candidates skip the molecular funnel "
        "and are simulated at Stage 3/4. Subsequent rounds: 2-4 architecture/formulation variants per round "
        "(current collector/separator thinning, porosity, N/P, negative particle radius, electrolyte sigma/t+ bridge, "
        "SEI-coating bridge), each simulated 1-by-1 and judged by bda log-evaluate. Nail handling: cooling-h design "
        "via thermal-management freedom (HEV pack active liquid cooling h_eff=20 W/m2/K, domain estimate); "
        "hA = h x cooling area passed to run-tr; near-adiabatic default hA=0.05 W/K recorded alongside."
    ),
    "budget_allocation": (
        "R1 baseline + ceiling assessment (5-7 runs). R2: system switch or strongest architecture push (4-6 runs). "
        "R3-R6: targeted ED/plating/SEI trade-off tuning (2-4 variants each). R7+: safety settle + closing. "
        "Foreseen 8-12 rounds, ~40-60 simulation runs; every round evaluated via bda log-evaluate (batch mode)."
    ),
    "risk_and_fallback": (
        "Risk A: ED gap vs 327.18 -> ceiling assessment decides Stage-2 escalation (SiOx system) before architecture "
        "tuning. Risk B: 4C plating persists -> lever chain N/P up, negative particle radius down, electrolyte "
        "sigma/t+ up; same cause failing 3 consecutive rounds -> three-strike questioning (system assumption / task "
        "boundary / metric reachability) recorded in final escalation field. Risk C: SEI@45C overshoot -> coating "
        "bridge (SEI kinetic rate constant x0.1; measured magnitude reference on Chen2020-set: 449->385 nm at 25 C), "
        "compared vs baseline on the same system only. Risk D: nail TR at near-adiabatic hA -> cooling design lever, "
        "both conditions recorded (no favorable-only testing). Never relax thresholds (entry 0 is the contract); "
        "unreachable within boundary -> honest negative result with 'reachable if' note."
    ),
    "detail": "design_plan.md",
}

funnel_entry = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "start_stage=3: task text names no new materials/additives/electrolyte design, molecular funnel skipped; "
        "materials use system baseline. base=Chen2020 per anchor-table deterministic default (no electrode system in "
        "task text), dump-verified before use (negative density 1657 kg/m3, geometry + SEI kinetics keys all present). "
        "props source = baseline (literature parameterization)."
    ),
}

append_entry(ws, entry0)
append_entry(ws, plan_entry)
append_entry(ws, funnel_entry)
print("entry0 + plan + funnel written to", ws.path / "log.jsonl")