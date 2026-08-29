"""Append round-2 candidate comparison table (supplementary display record; verdicts from log-evaluate)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "comparison",
    "round": 2,
    "comparison": [
        {
            "name": "FastCharge-A",
            "metrics": {
                "energy_density_wh_kg": 414.403,
                "plated": False,
                "anode_pot_min_v": 0.06568,
                "charge_4c_ah": 0.5208,
                "sei_100cyc_nm": 495.117,
                "sei_500cyc_nm": 820.391,
                "lowT_retention_pct": 99.465,
                "lowT_soak_retention_pct": 99.462,
            },
            "verdict": "fail (sei_500cyc only)",
        },
        {
            "name": "FastCharge-B",
            "metrics": {
                "energy_density_wh_kg": 446.556,
                "plated": False,
                "anode_pot_min_v": 0.07699,
                "charge_4c_ah": 0.5373,
                "sei_100cyc_nm": 499.488,
                "sei_500cyc_nm": 826.450,
                "lowT_retention_pct": 99.467,
                "lowT_soak_retention_pct": 99.461,
            },
            "verdict": "fail (sei_500cyc only); best ED + best plating margin -> chosen base geometry for R3 coating variants",
        },
        {
            "name": "FastCharge-C",
            "metrics": {
                "energy_density_wh_kg": 441.929,
                "plated": False,
                "anode_pot_min_v": 0.05593,
                "charge_4c_ah": 0.6182,
                "sei_100cyc_nm": 582.442,
                "sei_500cyc_nm": 940.226,
                "lowT_retention_pct": 99.996,
                "lowT_soak_retention_pct": 99.996,
            },
            "verdict": "fail (sei_100cyc + sei_500cyc); N/P boost rejected — thicker negative worsens SEI and plating cleared without it",
        },
    ],
}
append_entry(ws, entry)
print("comparison R2 appended")
