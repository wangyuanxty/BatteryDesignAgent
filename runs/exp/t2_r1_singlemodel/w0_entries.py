"""Write log.jsonl entry 0 (criteria + meta) and the Stage-1 plan entry.
Zero-interaction execution: thresholds parsed verbatim from the task text;
degrees of freedom not declared in the task text take the widest interpretation
(recorded in meta.freedoms). All log writes go through bda.store.append_entry.
"""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t2_r1_singlemodel", root="runs/exp")

entry0 = {
    "criteria": {
        # stage1 = molecular-level goals and elimination lines (pipeline Stage 2)
        "stage1": {
            # mace hard elimination lines (funnel_voting OFF: mace only; xtb HOMO
            # line unavailable because run-xtb is not executed in this ablation)
            "energy_ev": {"max": 0.0},
            "converged": True,
        },
        # stage2 = cell performance goals (pipeline Stage 3), thresholds verbatim
        # from the task text
        "stage2": {
            "energy_density_wh_kg": {"min": 327.18},
            # 100 cycles of 1C cycling (raw key of aging_1C_100cyc output)
            "sei_thickness_nm_end": {"max": 500},
            # 500 cycles of 1C cycling (aging --cycles 500 output key
            # sei_thickness_nm_end, mechanically renamed into a derived file
            # cell/derived_sei_500cyc.json so the two SEI thresholds are
            # judged against their own criteria keys; see meta.notes)
            "sei_thickness_nm_end_500cyc": {"max": 550},
            # -20 C discharge capacity retention vs 25 C 1C discharge,
            # mechanically derived: lowT capacity_ah / 25C capacity_ah * 100
            # (written to cell/derived_retention_lowT.json)
            "retention_lowT_pct": {"min": 90},
        },
        # stage3 = safety goals (pipeline Stage 4)
        "stage3": {
            # 4C fast charge without lithium plating: anode_potential_v must
            # never drop below 0 V (auto-derived by log-evaluate)
            "plated": False,
        },
        "meta": {
            "case": "t2_r1_singlemodel",
            "application": "grid energy storage",
            "real_compute": False,
            "start_stage": 2,
            "base_params": "Chen2020",
            "base_determination": "task text names no electrode system -> default "
            "Chen2020 per anchor table (discriminant verified: 93 keys, graphite "
            "LGM50 negative OCP, no SiOx keys, full thermal/geometry set, SEI "
            "kinetics present -> aging-capable; plating params absent -> runner "
            "injects standard defaults with trace)",
            "start_stage_reason": "task ablation note configures the molecular "
            "funnel (run-mlp mace only) -> molecular screening is in scope; "
            "objective metrics (SEI growth, 4C plating, -20 C retention) are "
            "electrolyte/material-scale levers -> start at Stage 2",
            "ablation": {
                "funnel_voting": "OFF (set by task text): molecular screening uses "
                "run-mlp(mace) only; chgnet/xtb not run; mace hard elimination "
                "lines (converged, energy_ev) apply; xtb HOMO line unavailable; "
                "no ranking, no disputed concept",
                "exploration_force": "ON (default; not mentioned in ablation)",
                "ceiling_escalation": "ON (default; not mentioned in ablation)",
            },
            "freedoms": {
                "electrode_system": "adjustable (task text silent -> widest "
                "interpretation; not exercised unless needed)",
                "electrolyte_formulation": "adjustable (task text silent -> widest "
                "interpretation, t1_r1 lesson)",
                "electrode_modification": "adjustable (task text silent -> widest "
                "interpretation)",
                "cell_architecture": "adjustable (task text silent -> widest "
                "interpretation)",
                "thermal_management": "adjustable (task text silent -> widest "
                "interpretation)",
            },
            "freedom_note": "zero-interaction execution: task text declares no "
            "degree-of-freedom restriction; widest interpretation recorded for "
            "audit traceability",
            "T_max_note": "task text sets no maximum-temperature red line; T_max_K "
            "is monitored and reported from 4C charge output but is not a "
            "pass/fail criterion",
            "notes": "derived metrics are mechanical transformations of tool "
            "outputs, written by python one-liners into cell/derived_*.json "
            "(each file documents source files, keys and formula); raw 500-cycle "
            "aging output is never passed to log-evaluate directly because its "
            "sei_thickness_nm_end key would be judged against the 100-cycle "
            "threshold",
        },
    }
}

plan_entry = {
    "action": "plan",
    "objective_breakdown": (
        "Grid energy storage cell, NMC811/graphite (Chen2020 default, no system "
        "named in task text). Four quantified metrics: (1) ED >= 327.18 Wh/kg "
        "contract caliber (calc-energy, electrolyte/casing excluded) — mass "
        "levers: current collectors, separator, porosity; capacity side depends "
        "on the parameter set's achievable discharge window, measured first. "
        "(2) 4C fast charge without plating — anode surface potential must stay "
        ">= 0 V; levers: electrolyte conductivity, negative porosity/particle "
        "size/N-P ratio; 45 C ambient already helps kinetics. (3) SEI <= 500 nm "
        "@100 cyc and <= 550 nm @500 cyc — binding constraint expected to be the "
        "500-cycle line (SEI reaction-limited growth scales roughly with sqrt "
        "of cycle count); lever: SEI kinetic rate constant / SEI exchange "
        "current density via film-forming additive bridge. (4) -20 C 1C "
        "retention >= 90% vs 25 C — hardest metric, levers: electrolyte "
        "conductivity (low-T formulation bridge), electrode thickness/porosity; "
        "expected trade-off ED vs low-T rate capability (Pareto). T_max is "
        "monitored, not a criterion (task text sets no red line)."
    ),
    "candidate_strategy": (
        "Round 1: Stage-2 molecular funnel (mace only per ablation) on six "
        "electrolyte additives targeting the three failure modes — FEC, VC, PS "
        "(SEI film formers), ethyl propionate EP (low-T conductivity co-"
        "solvent), LiDFOB anion, LiDFP anion (low-T interfacial film formers) "
        "— plus baseline characterization: 1C discharge (SPMe then DFN), "
        "calc-energy, aging 100 cyc, aging 500 cyc, lowT discharge, 4C charge "
        "45 C with plating. Round 2+: bridge passers into PyBaMM parameters "
        "(FEC/VC/PS -> SEI kinetic rate constant x0.3 literature estimate; "
        "EP/LiDFP -> electrolyte conductivity override marked estimate; "
        "LiDFOB -> SEI exchange current density) and simulate 2-4 architecture "
        "variants per round (exploration_force ON): thin collectors/thin "
        "separator (ED), negative porosity + particle size (plating), positive "
        "thickness/porosity (low T). Refine jointly, verify final design at "
        "Stage 4 with coupled thermal, then close."
    ),
    "budget_allocation": (
        "R1 funnel + baseline (6 protocols, ~8 runs), R2 additive-bridge "
        "variants + first architecture set (4-6 runs), R3 refinement toward "
        "joint optimum (3-5 runs), R4 Stage-4 safety on final design + closing. "
        "No round cap: iterate until achieved or session budget exhausted; "
        "aging 500 cyc runs only on shortlisted candidates (~3 s/100 cycles "
        "scale, keep to <= 3 runs)."
    ),
    "risk_and_fallback": (
        "Risk 1 (SEI 500 cyc): if x0.3 kinetics still > 550 nm at 500 cyc, "
        "strengthen to x0.1 or cut SEI reaction exchange current density; if "
        "the model structure makes 550 unreachable, three-strike questioning "
        "and honest negative result. Risk 2 (lowT >= 90%): conductivity "
        "override flattens Arrhenius T-dependence (approximation, marked); "
        "combine with thinner positive electrode / higher porosity; ED trade-"
        "off monitored. Risk 3 (4C plating): escalate negative-electrode "
        "architecture (porosity, particle size, N/P) before considering "
        "electrolyte overrides. Risk 4 (ED): if baseline window gives low "
        "capacity, raise capacity via electrode design within allowed levers "
        "(initial concentrations are excluded as design levers — baseline "
        "comparability). Fallback routing: transport/plating failures -> "
        "Stage 3 architecture or electrolyte bridge; stability failures -> "
        "Stage 2 substitution; three strikes -> escalation questioning in "
        "final entry."
    ),
    "detail": "design_plan.md",
}

append_entry(ws, entry0)
append_entry(ws, plan_entry)
print("entry 0 + plan written to", ws.path / "log.jsonl")
