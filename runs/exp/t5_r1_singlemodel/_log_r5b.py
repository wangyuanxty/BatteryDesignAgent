import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
ws = CaseWorkspace("exp/t5_r1_singlemodel", "runs")

funnel_entry = {
    "action": "funnel",
    "round": 5,
    "stage": 2,
    "model": "mace",
    "voting": "off",
    "dispositions": [
        {"name": "VC", "smiles": "O=C1OC=CO1", "energy_ev": -53.3376, "converged": True, "status": "passed"},
        {"name": "FEC", "smiles": "FC1COC(=O)O1", "energy_ev": -61.8898, "converged": True, "status": "passed"},
        {"name": "DTD", "smiles": "O=S1(=O)OCCO1", "energy_ev": -62.8207, "converged": True, "status": "passed"},
    ],
    "note": (
        "funnel_voting OFF ablation: run-mlp(mace) ONLY (chgnet/xtb not executed). Hard elimination lines "
        "applied: converged=true for all three and energy_ev <= 0.0 eV for all three -> all pass. "
        "No ranking, no disputed concept (single-model ablation semantics). Cell-level additive effect is not "
        "simulatable in this library (no additive bridge parameter) -> recorded honestly as qualitative "
        "formulation recommendation, not a criteria metric. Outputs: validation/r5_molecules_mace.json"
    ),
}
append_entry(ws, funnel_entry)
print("R5 funnel entry written")
