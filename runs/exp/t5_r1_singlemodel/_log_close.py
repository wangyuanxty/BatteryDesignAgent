import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
ws = CaseWorkspace("exp/t5_r1_singlemodel", "runs")

endorse_entry = {
    "action": "endorse",
    "candidates": [
        {"name": "VC", "smiles": "O=C1OC=CO1",
         "endorsement": {"skipped": True, "reason": "meta.real_compute=false: true-compute endorsement (run-orca/run-md) not executed per protocol"}},
        {"name": "FEC", "smiles": "FC1COC(=O)O1",
         "endorsement": {"skipped": True, "reason": "meta.real_compute=false: true-compute endorsement (run-orca/run-md) not executed per protocol"}},
        {"name": "DTD", "smiles": "O=S1(=O)OCCO1",
         "endorsement": {"skipped": True, "reason": "meta.real_compute=false: true-compute endorsement (run-orca/run-md) not executed per protocol"}},
    ],
    "note": "real_compute=false: closing skips run-orca/run-md true-compute endorsement; skip recorded honestly, no DFT/MD values fabricated. Additives remain qualitative formulation recommendations (mace screening passed only, funnel_voting OFF).",
}

final_entry = {
    "action": "final",
    "verdict": "achieved",
    "recommendation": (
        "Final design archN_robust (base OKane2022 + overrides in candidates/r4_archN_params.json): "
        "ED 533.18 Wh/kg DFN 1C (threshold 500.94, margin +32.2); 4C fast charge at 45C ambient DFN: "
        "T_max 330.50 K (threshold 333.15 K, margin 2.65 K), anode potential min +0.0215 V -> plated=false. "
        "All three entry-0 criteria achieved; SPMe cross-check ED 531.85 Wh/kg (+0.25% vs DFN). "
        "Qualitative formulation recommendation: VC/FEC/DTD electrolyte additives (mace funnel passed, "
        "funnel_voting OFF; no cell-level additive simulation exists in this library). "
        "True-compute endorsement skipped (real_compute=false)."
    ),
}

for e in (endorse_entry, final_entry):
    append_entry(ws, e)
print("endorse + final entries written")
