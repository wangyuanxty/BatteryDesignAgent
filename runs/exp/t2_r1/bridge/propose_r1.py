"""Append round-1 propose entry (baseline characterization)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "name": "Baseline Chen2020",
            "role": "system baseline characterization: NMC811/graphite grid-storage cell with Chen2020 default architecture/transport/SEI parameters (no overrides)",
            "struct": {},
        }
    ],
    "llm_reason": (
        "Round 1 is baseline characterization per Stage-1 plan: full protocol sweep "
        "(1C SPMe+DFN, calc-energy, lowT, aging 100/500, 4C charge 45C with plating) establishes "
        "the measured gap vector before any design lever is pulled; all subsequent variants "
        "are compared against these numbers on the same system."
    ),
}
append_entry(ws, entry)
print("propose R1 appended")
