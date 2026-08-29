# -*- coding: utf-8 -*-
"""t1_r3 — R1 propose + funnel (start_stage 3 basis + opening ceiling assessment) entries."""
import sys

from bda.store import CaseWorkspace, append_entry


def main() -> int:
    ws = CaseWorkspace("exp/t1_r3")
    append_entry(ws, {
        "action": "propose",
        "round": 1,
        "candidates": [
            {"name": "baseline", "role": "Chen2020 baseline characterization (default base: task names no electrode system)"},
        ],
        "llm_reason": (
            "R1 = baseline characterization of the deterministic default Chen2020 (NMC811/graphite, "
            "anchor verified by parameter dump: neg density 1657 graphite, no SiOx, no plating/cracking params; "
            "cut-off 4.2 V → overcharge protocol target 4.2+0.5=4.7 V, verbatim task match). "
            "Run all four protocol legs (1C, 4C+plating, overcharge, run-tr) to establish the full mechanical picture."
        ),
    })
    append_entry(ws, {
        "action": "funnel",
        "passed": 0,
        "rejected": 0,
        "disputed": 0,
        "detail": (
            "start_stage=3: this case starts at Stage 3; materials use system baseline (props source=baseline). "
            "base=Chen2020, matching basis: task text names no electrode system → anchor-table deterministic "
            "default Chen2020; verified by parameter dump (bridge/base_dump.json): NMC811 OCP (nmc_LGM50_ocp_Chen2020), "
            "graphite negative (density 1657, no SiOx), upper cut-off 4.2 V, no plating/cracking keys, SEI params present. "
            "Opening ceiling assessment (R1 measured): ED baseline 400.75 Wh/kg >= 392.61 already; "
            "mass-side levers (CC 16+12→10+6 um, separator 12→9 um, porosity up) estimate ED ceiling ~540 Wh/kg → "
            "ED objective within existing-system ceiling, no Stage-2 material escalation needed yet. "
            "4C leg: T_max 354.3 K, anode potential min -0.19 V (plated), charge accepted 0.176 Ah — "
            "transport/kinetics-limited within the existing chemistry; fixable at Stage 3 "
            "(porosity/electrolyte sigma,t+,D/particle size/thickness/cooling h). Escalation to OKane2022 SiOx "
            "held as fallback if 3 consecutive Stage-3 rounds keep plating."
        ),
        "dispositions": [],
    })
    print("R1 propose + funnel entries appended")
    return 0


if __name__ == "__main__":
    sys.exit(main())
