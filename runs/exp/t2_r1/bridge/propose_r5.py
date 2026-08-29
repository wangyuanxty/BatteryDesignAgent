"""Append round-5 propose entry (D2: positive particle radius for deeper 4C acceptance)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "propose",
    "round": 5,
    "candidates": [
        {
            "name": "GridStore-D2",
            "role": "4C-acceptance probe: D1 + r_pos 5.22->2.5 um (cathode surface kinetics: 4C charge is cathode-surface-OCP-limited; smaller positive particles lower surface overpotential, deeper charge before 4.2 V cut)",
            "struct": {
                "Negative particle radius [m]": 2.0e-06,
                "Positive particle radius [m]": 2.5e-06,
                "Electrolyte conductivity [S.m-1]": 3.0,
                "Electrolyte diffusivity [m2.s-1]": 2.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode porosity": 0.35,
                "Positive electrode porosity": 0.40,
                "SEI kinetic rate constant [m.s-1]": 1e-16,
            },
        },
    ],
    "llm_reason": (
        "R4 D1 result: plating-free (min +0.0909 V) but 4C acceptance only 0.553 Ah (11% SOC) — charge terminates "
        "on the 4.2 V cut while bulk SOC is low -> cathode SURFACE OCP limits (r_pos 5.22 um untouched so far). "
        "Positive particle radius [m] 2.5e-6 (architecture; cathode surface area x2 lowers local surface stoich "
        "excursion at 4C — domain experience, no precise source). Adoption rule: D2 adopted only if plated=false "
        "and 4C acceptance improves materially; else final = GridStore-D1."
    ),
}
append_entry(ws, entry)
print("propose R5 appended")
