"""Round-6 propose entry (t5_r2): finalist consolidation - thermal margin on the two passing platforms.

Parameter changes vs round-5 B/C (units): only Total heat transfer coefficient 60 -> 70 (f1/f2) or
80 (f3). Design choice (thermal-management freedom; liquid-cooling classes).
"""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

append_entry(ws, {
    "action": "propose",
    "round": 6,
    "candidates": [
        {"name": "f1_h70_B", "role": "e5_B platform + h 70: consolidate T margin (est ~1.5-2 K) at channel-cooling class"},
        {"name": "f2_h70_C", "role": "e5_C platform (max-ED, N/P buffered) + h 70: consolidate T margin keeping ED ~660"},
        {"name": "f3_h80_C", "role": "e5_C platform + h 80: stronger T margin arm"},
    ],
    "llm_reason": (
        "R5 gave three all-pass candidates but B/C hold only ~0.4 K T margin - too thin to close on. "
        "Finalist selection rule: keep transport/architecture gains, add cooling margin so the "
        "safety pass is robust; measure the h=70/80 consolidation arms, then DFN-verify the winner."
    ),
})
print("propose round 6 appended")