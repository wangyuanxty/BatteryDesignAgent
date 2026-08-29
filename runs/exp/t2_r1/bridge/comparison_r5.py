"""Round-5 comparison entry: GridStore-D2 vs GridStore-D1."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "comparison",
    "round": 5,
    "comparison": [
        {
            "name": "GridStore-D1",
            "metrics": {
                "energy_density_wh_kg": 449.485,
                "plated": False,
                "anode_potential_min_v": 0.090931,
                "c4_acceptance_ah": 0.552542,
                "sei_100cyc_nm": 7.876,
                "sei_500cyc_nm": 19.083,
                "lowT_retention_pct": 99.474,
            },
            "verdict": "pass (all five contracts)",
        },
        {
            "name": "GridStore-D2",
            "metrics": {
                "energy_density_wh_kg": 458.133,
                "plated": False,
                "anode_potential_min_v": 0.048448,
                "c4_acceptance_ah": 0.828370,
                "sei_100cyc_nm": 9.082,
                "sei_500cyc_nm": 25.325,
                "lowT_retention_pct": 99.572,
                "lowT_soak_retention_pct": 99.57,
            },
            "verdict": "pass (all five contracts) -> front-runner",
        },
    ],
    "conclusion": (
        "D2 (D1 + pos r 2.5um) delivers +50% 4C acceptance (0.553 -> 0.828 Ah) and ED 458.1 vs 449.5 Wh/kg; "
        "4C margin narrows to +0.0484 V (still mechanically plating-free); SEI 9.1/25.3 nm well inside limits; "
        "aging trajectory flat. D2 strictly better on acceptance/ED -> front-runner. Margin robustness probed in R6."
    ),
}
append_entry(ws, entry)
print("comparison R5 appended")
