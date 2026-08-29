"""Append round-3 candidate comparison table."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "comparison",
    "round": 3,
    "comparison": [
        {
            "name": "ALD-coat-A",
            "metrics": {
                "k_sei_m_s": 1e-14,
                "sei_100cyc_nm": 201.681,
                "sei_500cyc_nm": 500.364,
                "energy_density_wh_kg": 446.556,
                "plated": False,
                "lowT_retention_pct": 99.467,
            },
            "verdict": "pass (SEI@500 margin 9.0% thin)",
        },
        {
            "name": "ALD-coat-B",
            "metrics": {
                "k_sei_m_s": 1e-16,
                "sei_100cyc_nm": 8.434,
                "sei_500cyc_nm": 21.728,
                "energy_density_wh_kg": 446.556,
                "plated": False,
                "lowT_retention_pct": 99.467,
            },
            "verdict": "pass (all five contracts, robust margins, clean aging trajectory) -> recommended final design",
        },
        {
            "name": "ALD-coat-C",
            "metrics": {
                "k_sei_m_s": 1e-17,
                "sei_100cyc_nm": 5.342,
                "sei_500cyc_nm": 6.704,
                "energy_density_wh_kg": 446.556,
                "plated": False,
                "lowT_retention_pct": 99.467,
            },
            "verdict": "pass (more aggressive k, no added benefit over B)",
        },
    ],
}
append_entry(ws, entry)
print("comparison R3 appended")
