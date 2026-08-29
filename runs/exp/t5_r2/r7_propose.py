"""Round-7 propose entry (t5_r2): finalist verification at DFN precision."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

append_entry(ws, {
    "action": "propose",
    "round": 7,
    "candidates": [
        {"name": "final_f2_h70_C", "role": "selected finalist (e5_C platform: x1.3 thickness, N/P-buffered 121.84um negative, porosity 0.43/0.45, t+ 0.6, D 5e-10, particle 3um, h 70) - verification pass: 1C discharge at DFN precision for the contract ED, 4C safety re-confirmed"},
    ],
    "llm_reason": (
        "R6 f2_h70_C passed all criteria at spme-grade 1C; finalist deserves DFN-grade contract "
        "numbers before closing (protocol: spme quick-screen, dfn precision for passers). "
        "No parameter changes vs p_r6_f2 - verification only."
    ),
})
print("propose round 7 appended")