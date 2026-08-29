# Round-6 propose entry (agent-built input script)
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t1_r1_flash", root="runs")

propose = {
    "action": "propose",
    "round": 6,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 120.0,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Electrolyte diffusivity [m2.s-1]": 1.2e-9,
                "Cation transference number": 0.65,
            },
            "name": "F4b-h120",
            "role": "cooling-robustness probe: final electrolyte package at softer cooling h=120 (more manufacturable liquid-cooling spec); confirm T_max/plating margins still hold",
        },
    ],
    "llm_reason": "R5 F4b passed all 4C criteria (anode min +0.0114 V, T_max 323.4 K). Round 6 confirms robustness of the cooling spec: at h=120 the cell runs ~2 K hotter (better kinetics -> plating margin increases) while T_max stays well under 333.15 K. Simultaneously records the full-suite confirmation of F4b (ED/overcharge-TR/4C) in one evaluate entry with all outputs.",
}
append_entry(ws, propose)
print("propose R6 written")
