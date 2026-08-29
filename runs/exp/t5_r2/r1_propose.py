"""Round-1 propose + start_stage-3 funnel note (t5_r2)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

# --- propose (round 1: system baseline characterization) ---
append_entry(ws, {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "name": "baseline_Chen2020",
            "role": "system baseline characterization: NMC811/graphite LGM50-class, no parameter overrides; anchors the ceiling assessment and the reference arm for later comparisons",
        }
    ],
    "llm_reason": (
        "start_stage 3: task text names no materials -> materials use the system baseline. "
        "Base = Chen2020 (anchor-table default; no electrode system named in task text, recorded "
        "in entry-0 meta.base_basis). No parameter overrides this round - pure baseline. "
        "Purpose: measured ED / 4C plating / T_max anchors + layer-mass decomposition for the "
        "opening ceiling assessment."
    ),
})

# --- funnel (start_stage 3 note: base determination recorded) ---
append_entry(ws, {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "start_stage=3: this case starts at Stage 3 (cell design); molecular funnel not run "
        "this round. Base parameter set: Chen2020. Matching basis: task text names no electrode "
        "system -> anchor-table default ('no explicit electrode system -> Chen2020'), verified by "
        "parameter dump: positive OCP nmc_LGM50_ocp_Chen2020, pos max conc 63104 mol/m3 (NMC811-"
        "class), negative OCP graphite_LGM50 (graphite, max conc 33133), aging-capable SEI params "
        "present. Material properties source: baseline (literature parameterization)."
    ),
})
print("propose(round 1) + funnel entry appended")