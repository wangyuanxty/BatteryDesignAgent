"""Post-batch-3 log entry: propose round 4 (charging-potential gate)."""
from bda import store

ws = store.CaseWorkspace("t9_r4", root="runs/exp")

propose4 = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {"name": "AlB55", "role": "round-3 window pass (4.6413 V) - charging-potential gate: incremental voltage profile over the delithiation window"},
        {"name": "LiAlO2", "role": "round-2 anchor (4.598 V) - profile documentation of the d0 O-redox line's top-end"},
    ],
    "llm_reason": (
        "The stage-1 window has two co-gates: avg >= 4.6 V (AlB55 passes at 4.6413, margin 41 mV) and the "
        "charging potential <= 4.8 V (anodic limit of the fixed EC/EMC + LiPF6 electrolyte). For d0 O-redox, the "
        "top-of-charge incremental potential can exceed the average: comp/profile_voltage.py re-relaxes x = 1.0 "
        "and 0.9..0.3 (nested seeded subsets of the same removal order) and reports charging_potential_v = "
        "incremental V(0.4 -> 0.3), the last charge step into the top-of-charge state, plus max_incremental_v. "
        "LiAlO2 is profiled as the d0-line anchor. The profile also supplies the CHGNet-relaxed cell density "
        "required by the mapped-cell parameter set."
    ),
}
store.append_entry(ws, propose4)
print("propose4 appended")
