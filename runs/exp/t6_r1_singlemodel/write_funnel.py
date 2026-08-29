"""Write funnel entry (round 1, mace-only ablation)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_singlemodel", "runs/exp")
entry = {
    "action": "funnel",
    "passed": 3,
    "rejected": 1,
    "detail": (
        "funnel_voting OFF (ablation): run-mlp(mace) only; hard elimination lines applied "
        "(converged must be true; energy_ev <= 0.0 eV). xtb not run -> HOMO line unavailable; "
        "no three-model voting; no disputed concept. 4 candidates: FEC/VC/PS pass; LiDFOB "
        "eliminated (mace converged=false, fmax 0.264 after 50 BFGS steps)."
    ),
    "dispositions": [
        {"name": "FEC", "status": "passed", "reason": "mace converged=true, energy -61.890 eV <= 0"},
        {"name": "VC", "status": "passed", "reason": "mace converged=true, energy -53.338 eV <= 0"},
        {"name": "LiDFOB", "status": "rejected", "reason": "mace converged=false (BFGS fmax 0.264 > 0.05 at 50 steps); hard elimination line"},
        {"name": "PS", "status": "passed", "reason": "mace converged=true, energy -72.993 eV <= 0"},
    ],
}
append_entry(ws, entry)
print("funnel entry written")
