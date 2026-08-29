"""Round-1 funnel entry (funnel_voting OFF ablation: mace only, no voting)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t2_r1_singlemodel", root="runs/exp")

entry = {
    "action": "funnel",
    "passed": 6,
    "rejected": 0,
    "detail": "funnel_voting OFF ablation: run-mlp(mace) only (chgnet/xtb not run, "
    "xtb HOMO line unavailable). Mace hard elimination lines applied: all six "
    "candidates converged and energy_ev <= 0.0 eV -> passed. No three-model "
    "voting, no ranking, no disputed concept.",
    "dispositions": [
        {"name": "FEC", "status": "passed",
         "reason": "mace converged, energy_ev -61.89 eV <= 0.0"},
        {"name": "VC", "status": "passed",
         "reason": "mace converged, energy_ev -53.34 eV <= 0.0"},
        {"name": "PS", "status": "passed",
         "reason": "mace converged, energy_ev -72.99 eV <= 0.0"},
        {"name": "EP", "status": "passed",
         "reason": "mace converged, energy_ev -95.98 eV <= 0.0"},
        {"name": "LiDFOB-anion", "status": "passed",
         "reason": "mace converged, energy_ev -63.40 eV <= 0.0 (anion screened "
         "as isolated species; cell-level benefit judged via parameter bridge)"},
        {"name": "LiDFP-anion", "status": "passed",
         "reason": "mace converged, energy_ev -29.25 eV <= 0.0 (anion screened "
         "as isolated species; cell-level benefit judged via parameter bridge)"},
    ],
}

append_entry(ws, entry)
print("funnel R1 written")
