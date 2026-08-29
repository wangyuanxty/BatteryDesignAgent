"""Append round-4 propose entry (final verification + 4C-acceptance probe)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {
            "name": "GridStore-D1",
            "role": "4C-acceptance probe: ALD-coat-B + r_neg 2.0 um + sigma_e 3.0 S/m + D_e 2.5e-9 m2/s (deeper 4C charge attempt; rejected if plating returns)",
            "struct": {
                "Negative particle radius [m]": 2.0e-06,
                "Electrolyte conductivity [S.m-1]": 3.0,
                "Electrolyte diffusivity [m2.s-1]": 2.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode porosity": 0.35,
                "Positive electrode porosity": 0.40,
                "SEI kinetic rate constant [m.s-1]": 1e-16,
            },
        },
        {
            "name": "GridStore-Final",
            "role": "final design verification = ALD-coat-B (FastCharge-B + k_sei 1e-16), plus true -20C soak evidence",
            "struct": {
                "Negative particle radius [m]": 2.93e-06,
                "Electrolyte conductivity [S.m-1]": 2.5,
                "Electrolyte diffusivity [m2.s-1]": 1.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode porosity": 0.35,
                "Positive electrode porosity": 0.40,
                "SEI kinetic rate constant [m.s-1]": 1e-16,
            },
        },
    ],
    "llm_reason": (
        "R3 closed the SEI contracts (ALD-coat-B recommended). R4: (1) GridStore-D1 probes whether stronger transport "
        "(r_neg 2.0 um, sigma 3.0 S/m, D 2.5e-9 — ESTIMATES as in R2) deepens 4C charge acceptance beyond 0.537 Ah "
        "without re-introducing plating (min must stay >0 V); (2) GridStore-Final = ALD-coat-B with true -20C soak "
        "probe (Initial temperature 253.15 K) as robustness evidence. Adoption rule: D1 adopted only if plated=false "
        "and all other contracts hold; otherwise final = GridStore-Final."
    ),
}
append_entry(ws, entry)
print("propose R4 appended")
