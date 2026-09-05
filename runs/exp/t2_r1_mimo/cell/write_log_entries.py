import json, sys
sys.path.insert(0, ".")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t2_r1_mimo", "runs/exp/t2_r1_mimo")

# Round 1 propose (baseline characterization)
propose = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {"name": "Chen2020 baseline", "role": "NMC811/graphite baseline characterization", "params": "params_baseline.json (empty overrides)"}
    ],
    "llm_reason": "Round 1 is baseline characterization of Chen2020 system. Runs 1C discharge, 100/500-cycle aging, lowT discharge, and 4C charge to establish which metrics pass/fail and identify optimization targets."
}
append_entry(ws, propose)

print("Round 1 propose entry written")
