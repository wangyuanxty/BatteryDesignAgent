import sys
from pathlib import Path

sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace(Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_flash"))

# Design update: DFN verification (task 5) forced thermal redesign h 120 -> 300
design_update = {
    "action": "plan",
    "update": True,
    "reason": "DFN precision verification (task 5) of final design: DFN 1C calc confirms M1 1171.7 Wh/L / M2 4.1446 V (pass); DFN 4C at h=120 shows T_max 326.12 K (lumped-SPM 321.86 underestimated peak by 4.3 K) -> M5 fails at DFN. Thermal redesign: h sweep at DFN: h=200 -> 323.83 fail, h=250 -> 323.05 pass (0.10 K margin), h=300 -> 322.50 pass (0.65 K margin). Final spec: h=300 W/m2K (vapor chamber + graphite + aluminum frame). DFN M4: anode min -0.0192 V (h300) - still plated, consistent with the protocol-boundary conclusion (SPM -0.2623 V). DFN aging: runner caps DFN aging at 1 cycle (27.4 nm vs SPM cycle-1 ~29 nm - consistent); SPM 100-cycle 292.2 nm stands as M3 evidence.",
    "candidate_strategy": "Final design unchanged except thermal: h 120 -> 300 W/m2K (verified margin at DFN). All other parameters as finN-2e19.",
    "budget_allocation": "DFN verification complete. Moving to closing: deliverables, render, verify-deliverables.",
}

# DFN verification evidence entry
verify = {
    "action": "verify",
    "round": 5,
    "name": "finN-2e19 DFN precision verification (task 5)",
    "model": "DFN",
    "results": {
        "M1 energy_density_wh_l": {"value": 1171.71, "threshold_min": 950, "verdict": "pass", "source": "cell/r5_finN_dfn_1c_calc.json"},
        "M2 midpoint_voltage_v": {"value": 4.1446, "threshold_min": 4.1, "verdict": "pass", "source": "cell/r5_finN_dfn_1c_calc.json"},
        "M3 sei_thickness_nm_end": {"value": 27.4, "note": "DFN aging capped at 1 cycle by runner; SPM 100-cycle = 292.2 nm is the M3 evidence", "source": "cell/r5_finN_dfn_aging.json"},
        "M4 plated": {"value": True, "threshold": False, "verdict": "fail", "source": "cell/r5_finN_dfn_h300_4c.json (anode min -0.0192 V; real charge 6.68 Ah)"},
        "M5 T_max_K_h300": {"value": 322.50, "threshold_max": 323.15, "verdict": "pass", "source": "cell/r5_finN_dfn_h300_4c.json"},
        "M5 T_max_K_h250": {"value": 323.05, "threshold_max": 323.15, "verdict": "pass", "source": "cell/r5_finN_dfn_h250_4c.json"},
        "M5 T_max_K_h200": {"value": 323.83, "threshold_max": 323.15, "verdict": "fail", "source": "cell/r5_finN_dfn_h200_4c.json"},
        "M5 T_max_K_h120": {"value": 326.12, "threshold_max": 323.15, "verdict": "fail", "source": "cell/r5_finN_dfn_4c.json"},
    },
    "spm_vs_dfn": {
        "ED_wh_l": {"spm": 1172.1, "dfn": 1171.7},
        "midV_v": {"spm": 4.2475, "dfn": 4.1446},
        "capacity_ah": {"spm": 6.347, "dfn": 6.324},
        "charge_4C_ah": {"spm": 6.97, "dfn": 6.68},
        "anode_min_V": {"spm": -0.2623, "dfn": -0.0192},
        "T_max_K_h120": {"spm": 321.86, "dfn": 326.12},
    },
}

append_entry(ws, design_update)
append_entry(ws, verify)
print("design update + DFN verify appended")
