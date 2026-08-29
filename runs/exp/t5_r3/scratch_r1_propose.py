"""t5_r3 round-1 propose (baseline candidate) via append_entry."""
from bda.store import CaseWorkspace, append_entry
ws = CaseWorkspace("t5_r3", "runs/exp")
propose = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "struct": {},
            "name": "Chen2020 baseline",
            "role": "opening baseline characterization: 1C discharge + contract ED + 4C/45C plating/thermal audit",
        }
    ],
    "llm_reason": (
        "start_stage=3 with system baseline Chen2020 (no electrode system named in task text -> anchor-table default). "
        "Baseline establishes all three criteria anchor values and feeds the opening ceiling assessment."
    ),
}
append_entry(ws, propose)
print("round-1 propose appended")