"""Append round-6 propose entry (D3: plating-margin robustness probe)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "propose",
    "round": 6,
    "candidates": [
        {
            "name": "GridStore-D3",
            "role": "plating-margin robustness probe: D2 + negative porosity 0.35->0.40 (lower anode tortuosity -> more anode-surface potential headroom at 4C; adoption only if margin improves and other metrics hold)",
            "struct": {
                "Negative particle radius [m]": 2.0e-06,
                "Positive particle radius [m]": 2.5e-06,
                "Electrolyte conductivity [S.m-1]": 3.0,
                "Electrolyte diffusivity [m2.s-1]": 2.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode porosity": 0.40,
                "Positive electrode porosity": 0.40,
                "SEI kinetic rate constant [m.s-1]": 1e-16,
            },
        },
    ],
    "llm_reason": (
        "D2 passes all contracts but the 4C anode-potential margin is +0.0484 V — positive yet the thinnest in the "
        "family (D1 +0.0909). Negative electrode porosity [0.40] (architecture; lower tortuosity reduces anode-side "
        "concentration overpotential at 4C, domain experience) should widen the margin at small ED cost (~1%). "
        "Adoption rule: adopt only if anode potential min improves and 4C acceptance does not collapse; "
        "else final = GridStore-D2."
    ),
}
append_entry(ws, entry)
print("propose R6 appended")
