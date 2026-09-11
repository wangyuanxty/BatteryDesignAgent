"""Post-batch-3 log entry: funnel round 3."""
from bda import store

ws = store.CaseWorkspace("t9_r4", root="runs/exp")

funnel3 = {
    "action": "funnel",
    "round": 3,
    "passed": 1,
    "rejected": 13,
    "disputed": 0,
    "detail": (
        "AlB55 (LiAl0.5B0.5O2) 4.6413 V clears the window (margin 41 mV) - the first candidate past 4.6 V in 42 "
        "screened. Non-monotonic in B content: sharp 50:50 peak (nearest neighbors AlB82 4.464, BAl73 4.226, "
        "AlB95 4.488, BGa55 4.504). The peak comes from the delithiated x=0.3 state being ~1.5 eV off the "
        "B-content trend - flagged as a sensitivity risk; the charging-potential profile is the co-gate. "
        "Pure LiBO2 4.253 is NOT higher than LiAlO2 4.598 - the ionic-radius trend does not extrapolate to B; "
        "the pass is a mixing effect."
    ),
    "dispositions": [
        {"name": "LiBO2", "status": "rejected", "reason": "4.253 V < 4.6 (pure B below LiAlO2 - radius trend breaks at B)"},
        {"name": "AlB55", "status": "passed", "reason": "4.6413 V >= 4.6 - advances to the charging-potential gate"},
        {"name": "AlB73", "status": "rejected", "reason": "4.429 V < 4.6"},
        {"name": "AlB91", "status": "rejected", "reason": "4.443 V < 4.6"},
        {"name": "BAl73", "status": "rejected", "reason": "4.226 V < 4.6"},
        {"name": "BAl91", "status": "rejected", "reason": "4.304 V < 4.6"},
        {"name": "AlB82", "status": "rejected", "reason": "4.464 V < 4.6"},
        {"name": "AlB64", "status": "rejected", "reason": "4.280 V < 4.6"},
        {"name": "AlB95", "status": "rejected", "reason": "4.488 V < 4.6"},
        {"name": "GaAl55", "status": "rejected", "reason": "4.494 V < 4.6"},
        {"name": "AlSc55", "status": "rejected", "reason": "4.298 V < 4.6"},
        {"name": "BGa55", "status": "rejected", "reason": "4.504 V < 4.6"},
        {"name": "BSc55", "status": "rejected", "reason": "4.115 V < 4.6"},
        {"name": "GaAl91", "status": "rejected", "reason": "4.454 V < 4.6"},
    ],
}
store.append_entry(ws, funnel3)
print("funnel3 appended")
