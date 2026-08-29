"""t5_r3 round-4 propose via append_entry."""
from bda.store import CaseWorkspace, append_entry
ws = CaseWorkspace("t5_r3", "runs/exp")
propose = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 6e-06,
                "Negative current collector thickness [m]": 5e-06,
                "Separator thickness [m]": 7e-06,
                "Positive particle radius [m]": 3e-06,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Cation transference number": 0.5,
                "Electrolyte diffusivity [m2.s-1]": 6e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 50.0,
                "Cell cooling surface area [m2]": 0.01062,
            },
            "name": "X1 honest5Ah+full-mit",
            "role": "TRUE-4C cell: baseline electrode thickness (actual ~5Ah = real 4C at 20A) + aggressive foils + cathode 3um + transport + h50 + double-sided cooling",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 6e-06,
                "Negative current collector thickness [m]": 5e-06,
                "Separator thickness [m]": 7e-06,
                "Positive particle radius [m]": 3e-06,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Cation transference number": 0.5,
                "Electrolyte diffusivity [m2.s-1]": 6e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 40.0,
                "Cell cooling surface area [m2]": 0.01062,
            },
            "name": "X2 X1+h40",
            "role": "cooling sensitivity probe: h=40 instead of 50",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 5e-06,
                "Separator thickness [m]": 9e-06,
                "Positive particle radius [m]": 3e-06,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Cation transference number": 0.5,
                "Electrolyte diffusivity [m2.s-1]": 6e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 50.0,
                "Cell cooling surface area [m2]": 0.01062,
            },
            "name": "X3 manufacturability-relaxed",
            "role": "Al 8um (standard foil) + separator 9um: check ED still >= 500.94 with easier supply base",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 5e-06,
                "Separator thickness [m]": 9e-06,
                "Positive particle radius [m]": 3e-06,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Cation transference number": 0.5,
                "Electrolyte diffusivity [m2.s-1]": 6e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 60.0,
                "Cell cooling surface area [m2]": 0.01062,
            },
            "name": "X4 X3+h60",
            "role": "manufacturability-relaxed + stronger cooling (h=60) for T_max headroom",
        },
    ],
    "llm_reason": (
        "Honesty probe of W3: raising nominal capacity to 6.5 (matching built 6.55Ah -> true 4C=26A) breaks both "
        "safe margins (min_ap -0.0230V plated, T_max 340.33K). W3's pass leaned on the 5-Ah nameplate "
        "understating a 6.5-Ah build -> the 20A '4C' was really 3.1C. REBUILD HONEST: electrodes back to "
        "baseline thickness (actual capacity ~5.0Ah -> true 4C at 20A), ED recovered via aggressive foils "
        "(Al 6um, Cu 5um) and separator 7um. T_max strategy: h=40-60 plus DOUBLE-SIDED cooling (cooling area "
        "0.00531->0.01062 m2 = both pouch faces on cold plates, real EV pack practice). Cathode particle 3um "
        "expands charge-transfer area x1.74 -> lower 4C polarization -> less heat + later cut-off. Formulation "
        "envelope fixed at the isoC-proven sigma=5/t+=0.5/De=6e-10 (round-3 W2 showed weaker transport loses "
        "plating). Thicker-foil variants X3/X4 probe the ED-vs-manufacturability trade. All values parameters "
        "come from tool outputs; transport/cooling values are flagged estimates with industry basis."
    ),
}
append_entry(ws, propose)
print("round-4 propose appended")