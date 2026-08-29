# Append closing entries: (1) endorse (skipped, real_compute false), (2) final (verdict + escalation).
import sys
sys.path.insert(0, r".claude/skills/virtual-battery-factory/scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1_noceiling", "runs")

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": ("real_compute: false (protocol default for this case) - true DFT/MD endorsement "
               "(run-orca / run-md) skipped; no fabricated first-principles values. Stage-5 "
               "endorsement is not applicable to this negative-result case: start_stage 3, "
               "electrode system locked, no material-design candidate entered the funnel; the "
               "selected design is architecture-level (Stage 3) and the honest verdict is "
               "infeasibility of two criteria in the admissible space, recorded in the final entry."),
    "candidates": [
        {"name": "L AnPorUp (best-effort cell design)",
         "note": ("best-in-sweep 4C plating margin -0.3868 V, lowest DCR 0.199 mOhm, ED 476.7, "
                  "SEI100 467.6, lowT 0.9944; SEI500 811.3 fails (best across sweep 771.4)")},
    ],
}
append_entry(ws, endorse)

final = {
    "action": "final",
    "verdict": "not achieved",
    "recommendation": (
        "Honest negative result within the admissible design space. Best-effort design L (AnPorUp): "
        "thin current collectors (Al 16->10 um, Cu 12->8 um) + anode porosity 0.25->0.35 on the "
        "Chen2020 NMC811/graphite baseline, nominal 4.9506 Ah (measured 1C). Passes 3/5 criteria "
        "with margin: ED 476.72 Wh/kg (>= 327.18), SEI100 467.6 nm (<= 500), lowT retention 0.9944 "
        "(>= 0.90), plus best-in-sweep 4C plating margin (-0.3868 V) and lowest DCR (0.199 mOhm). "
        "The two hard criteria - 4C no-plating (anode min >= 0 V) and SEI500 (<= 550 nm) - are "
        "infeasible: 14 designs / 10 lever axes / 4 rounds, best measured -0.3868 V and 771.4 nm. "
        "Design L is the honest deliverable; it must NOT be shipped as meeting the 4C/SEI500 spec."),
    "escalation": {
        "layer1_model_system": (
            "Is the failure a property of the system+protocol combination rather than the "
            "architecture? Yes. The 4C metric is pinned by (a) the test start state - the protocol "
            "first discharges the cell at 1C to v_min, leaving the anode deeply lithiated; (b) the "
            "SPMe surface response at ~195 A/m2; (c) the anode-internal electrolyte potential drop "
            "at the separator interface. The 4.2 V abort is a ~5 s transport event that no "
            "architecture lever moved by more than +0.052 V across 10 axes. SEI500 is pinned by the "
            "per-cycle 4.2 V charge-end depth (SEI ec-reaction-limited, isothermal 25 C aging). "
            "Conclusion: architecture-level tuning cannot meet either criterion on this system "
            "under this protocol."),
        "layer2_task_boundary": (
            "Are the locked freedoms genuinely out of scope? Yes - executed per entry 0: "
            "electrode_system locked (Chen2020 baseline; task text names no material system), "
            "electrode_modification locked, ceiling_escalation OFF (ablation note). The levers that "
            "would move the metrics - solid-phase diffusivity (protocol-excluded), SEI kinetics "
            "(electrode modification), charge cut-off (usage mode, excluded) - are outside the "
            "boundary. The one allowed adjacent lever, electrolyte transport formulation, was "
            "tested in BOTH directions (B transport-up worsened plating; K transport-down collapsed "
            "the cell). The boundary is unambiguous and was respected throughout."),
        "layer3_metric_relaxation": (
            "Is the objective reachable within the boundary at all? No - honest negative result. "
            "Best plating -0.3868 V vs >= 0 (gap 0.387 V; largest single-lever move 0.052 V; K's "
            "mechanical pass is a degenerate artifact - nominal collapse to 1.16 Ah makes '4C' "
            "45 A/m2 - and K fails ED at 238.2). Best SEI500 771.4 nm vs <= 550 (gap 221 nm; "
            "levers moved it only -6.5..+208 nm). Relaxation analysis (thresholds NOT relaxed): "
            "SEI500 <= 550 becomes reachable if the per-cycle charge depth is reduced ~28% (lower "
            "charge cut-off, excluded usage-mode lever) or SEI kinetics are slowed (locked "
            "electrode modification); plating >= 0 V becomes reachable only with a different "
            "material system or electrode modification (both locked) - no C-rate relaxation within "
            "the tested range reaches 0 V, and the metric is not monotone in current (D: 142 A/m2 "
            "-> -0.4067; J: 129 A/m2 -> -0.4455), so even a softer-rate test is not a guaranteed pass."),
    },
    "deliverables": ["design_spec", "bom", "datasheet", "calc", "dvpr", "dfmea",
                     "delivery_index", "report.html"],
    "real_compute": False,
}
append_entry(ws, final)
print("endorse + final entries appended")
