# -*- coding: utf-8 -*-
"""t1_r3 — append the Stage 1 plan entry to log.jsonl (protocol-mandated path)."""
import sys

from bda.store import CaseWorkspace, append_entry

ENTRY = {
    "action": "plan",
    "objective_breakdown": (
        "ED>=392.61 Wh/kg (contract calc-energy, electrolyte excluded) | 4C fast charge plated=false "
        "(anode potential >=0 V) | T_max_K<=333.15 K on 4C and overcharge cell-thermal outputs | "
        "overcharge 4.7 V (NMC811 4.2+0.5 V) triggered=false (run-tr). Expected trade-off: ED vs 4C plating "
        "(thick electrodes raise ED but worsen plating); T_max is expected to be resolvable via cooling h "
        "(liquid cooling, sedan standard) without touching ED."
    ),
    "candidate_strategy": (
        "R1 baseline Chen2020 (default: task names no electrode system; anchor verified by parameter dump) "
        "with 1C/calc-energy/4C-plating/overcharge+run-tr + opening ceiling assessment. "
        "R2-R5: 2-4 variants/round — plating: neg particle radius 5.86->3 um, electrode thinning, N/P up, "
        "electrolyte sigma 1.0->1.4 S/m & t+ raise (bridge table); ED: Cu CC 12->6-8 um, Al CC 16->10 um, "
        "separator 12->9 um, porosity up (pos 0.335->0.40, neg 0.25->0.33); T_max: h 10->50-100 W/m2K. "
        "Escalation path: OKane2022 (SiOx negative, native plating params) system switch if architecture "
        "space saturates (ceiling_escalation ON). R6-R8 safety pass on finalists (overcharge DFN + run-tr)."
    ),
    "budget_allocation": (
        "R1 baseline+ceiling; R2-R5 fast-charge/ED exploration (~3 candidates/round); "
        "R6-R8 overcharge/TR safety pass + finalist confirmation; R9 closing "
        "(endorse skip real_compute=false, final, render, deliverables, verify-deliverables)."
    ),
    "risk_and_fallback": (
        "4C plating persistent after 3 rounds -> escalate to electrolyte formulation -> OKane2022 SiOx switch "
        "-> three-strike questioning (system/boundary/metric) recorded in final.escalation. "
        "ED below 392.61 after thinning -> CC/separator/porosity mass levers then re-tune thickness on the "
        "ED-vs-plating Pareto front. Overcharge T_max>333.15 K -> h raise + polarization cuts; "
        "triggered persists -> honest negative on safety axis or system switch (LNMO shifts overcharge target "
        "to 5.2 V, deviation from verbatim 4.7 V recorded if used). DFN failure -> SPMe fallback (runner)."
    ),
    "detail": "design_plan.md",
}


def main() -> int:
    ws = CaseWorkspace("exp/t1_r3")
    append_entry(ws, ENTRY)
    print("plan entry appended")
    return 0


if __name__ == "__main__":
    sys.exit(main())
