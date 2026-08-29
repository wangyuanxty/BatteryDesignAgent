"""Round-4 comparison entry: GridStore-D1 vs GridStore-Final (ALD-coat-B)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "comparison",
    "round": 4,
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
                "lowT_soak_retention_pct": 99.47,
            },
            "verdict": "pass (all five contracts; neg r 2.0um widens 4C margin to +0.091 V and lifts acceptance to 0.553 Ah vs ALD-coat-B; soak confirms true -20C retention) -> new front-runner",
        },
        {
            "name": "GridStore-Final",
            "metrics": {
                "energy_density_wh_kg": 446.556,
                "plated": False,
                "anode_potential_min_v": 0.076986,
                "c4_acceptance_ah": 0.537327,
                "sei_100cyc_nm": 8.434,
                "sei_500cyc_nm": 21.728,
                "lowT_retention_pct": 99.467,
                "lowT_soak_retention_pct": 99.46,
            },
            "verdict": "pass (identical design to ALD-coat-B by construction; R4 soak probe 5.00875 Ah -> 99.46% at true -20C) -> superseded by D1 on ED/acceptance/margin",
        },
    ],
    "conclusion": (
        "D1 strictly better than GridStore-Final (ED 449.5 vs 446.6, acceptance 0.553 vs 0.537 Ah, 4C margin "
        "+0.091 vs +0.077 V); GridStore-Final remains a verified fallback but is no longer the front-runner."
    ),
}
append_entry(ws, entry)
print("comparison R4 appended")
