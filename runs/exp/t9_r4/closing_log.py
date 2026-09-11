"""Closing log entry: funnel round 4 (appended BEFORE the round-4 evaluate)."""
from bda import store

ws = store.CaseWorkspace("t9_r4", root="runs/exp")

funnel4 = {
    "action": "funnel",
    "round": 4,
    "passed": 0,
    "rejected": 2,
    "disputed": 0,
    "detail": (
        "Charging-potential gate DECISIVE FAILURE: AlB55 charging_potential_v = 7.410 V (incremental V(0.4 -> 0.3) "
        "into the top-of-charge state) - 2.6 V above the 4.8 V anodic limit of the fixed EC/EMC + LiPF6 electrolyte. "
        "The round-3 window pass (avg 4.641 V) was bought with a pathological x=0.3 endpoint: E(0.3) sits ~9 eV off "
        "its composition neighbors and the final Li removal costs 7.4 V. The sharp 50:50 peak was this artifact's "
        "signature, not a designable chemistry. The mechanism is fatal for the whole d0/d10 O-redox layered line "
        "(any avg >= 4.6 in that family comes from the same diseased endpoint). LiAlO2 (4.598 V) fails the window "
        "regardless. No candidate survives both stage-1 co-gates."
    ),
    "dispositions": [
        {"name": "AlB55", "status": "rejected", "reason": "charging_potential_v 7.410 V > 4.8 V - incompatible with the fixed electrolyte; the window pass was the artifact signature"},
        {"name": "LiAlO2", "status": "rejected", "reason": "avg 4.598 V < 4.6 (and the d0-line mechanism is condemned by the AlB55 gate)"},
    ],
}
store.append_entry(ws, funnel4)
print("funnel4 appended")

