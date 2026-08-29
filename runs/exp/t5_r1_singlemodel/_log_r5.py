import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
ws = CaseWorkspace("exp/t5_r1_singlemodel", "runs")

comparison_entry = {
    "action": "evaluate",
    "round": 4,
    "comparison": [
        {"name": "archL_h45", "metrics": {"energy_density_wh_kg": 528.6, "T_max_K": 331.53, "plated": False}, "verdict": "pass"},
        {"name": "archM_smallP", "metrics": {"energy_density_wh_kg": 532.0, "T_max_K": 331.79, "plated": False}, "verdict": "pass"},
        {"name": "archN_robust", "metrics": {"energy_density_wh_kg": 531.8, "T_max_K": 330.50, "plated": False}, "verdict": "pass"},
        {"name": "archO_negPoro", "metrics": {"energy_density_wh_kg": 521.2, "T_max_K": 333.21, "plated": False}, "verdict": "fail"},
    ],
    "note": "R4 comparison: archL/archM/archN all pass; archN_robust selected as final design (best combined margins: ED +30.9 Wh/kg, Tmax 2.65 K under, anode +21.5 mV). archO fails Tmax by 0.06 K (333.21>333.15) - neg porosity 0.20 adds mass without energy gain, rejected.",
}

propose_entry = {
    "action": "propose",
    "round": 5,
    "candidates": [
        {
            "smiles": "O=C1OC=CO1",
            "name": "VC",
            "role": "vinylene carbonate - film-forming electrolyte additive: polymerizable SEI builder to stabilize graphite surface under 4C fast charge",
        },
        {
            "smiles": "FC1COC(=O)O1",
            "name": "FEC",
            "role": "fluoroethylene carbonate - film-forming additive: LiF-rich SEI, suppresses electrolyte reduction at high-rate charge (no-plating support)",
        },
        {
            "smiles": "O=S1(=O)OCCO1",
            "name": "DTD",
            "role": "ethylene sulfate - SEI sulfur-chemistry additive: lowers interfacial resistance, supports fast charge",
        },
        {
            "struct": "archN_robust params (DFN-precision confirmation, see candidates/r4_archN_params.json)",
            "name": "final_archN_DFNconf",
            "role": "final design DFN-precision confirmation: 1C discharge DFN + calc-energy + existing 4C DFN",
        },
    ],
    "llm_reason": (
        "Design criteria already met by archN_robust (R4). R5 serves two protocol duties: (1) exercise the "
        "molecular funnel under the funnel_voting OFF ablation - electrolyte additive candidates (VC/FEC/DTD, "
        "real commercial fast-charge additives) screened with run-mlp(mace) ONLY; hard elimination lines "
        "(converged=true, energy_ev<=0.0 eV) apply; run-xtb/run-mlp(chgnet) NOT executed; no ranking, no "
        "disputed concept. (2) Final DFN-precision confirmation of archN_robust (SPMe ED 531.8 -> DFN). "
        "Additive cell-level effect is not simulatable in this library (no additive bridge parameter) - "
        "recorded honestly as qualitative formulation recommendation, not a criteria metric."
    ),
}

for e in (comparison_entry, propose_entry):
    append_entry(ws, e)
print("comparison R4 + propose R5 written")
