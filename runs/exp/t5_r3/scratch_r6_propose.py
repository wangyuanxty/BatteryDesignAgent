"""Round-6 propose entry: DFN verification of SPMe-passing finalists."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r3", "runs/exp")
append_entry(ws, {
    "action": "propose",
    "round": 6,
    "candidates": [
        "Y4 (max-margin, DFN-verify): params_y4.json full-order DFN re-run of 1C + 4C_45C",
        "Y3 (manufacturable-foils, DFN-verify): params_y3.json full-order DFN re-run of 1C + 4C_45C",
    ],
    "rationale": (
        "Funnel stage-3 rule: quick-screen ~s SPMe, then precise minute-scale DFN for passers. "
        "Rounds 4-5 SPMe: Y1-Y4 all pass all three criteria; Y4 best plating margin (+0.0171 V), "
        "Y3 supply-friendly foils (positive Al 8um, sep 9um, standard t+0.5/De6e-10 transport) "
        "with acceptable margin (+0.0095 V). "
        "Y1/Y2 not DFN-verified (Y1 SPMe margin only +0.0088 V, Y2 same cell at different h; "
        "policy-relevant finalists are Y4 and Y3)."
    ),
    "protocols": [
        "1C_discharge dfn -> calc-energy (contract ED)",
        "4C_charge_45C dfn --thermal lumped --plating (T_max_K, anode_potential_v)",
    ],
    "note": "4C current = 4 x nominal 5.044 Ah = 20.176 A on true ~5.0 Ah builds (honest true 4C)",
})