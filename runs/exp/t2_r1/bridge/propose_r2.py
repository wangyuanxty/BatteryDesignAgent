"""Append round-2 propose entry (plating-mitigation architecture/transport variants)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "name": "FastCharge-A",
            "role": "4C plating mitigation: halved negative particle radius + high-transport low-T-dependence electrolyte formulation (constant sigma/D/t+)",
            "struct": {
                "Negative particle radius [m]": 2.93e-06,
                "Electrolyte conductivity [S.m-1]": 2.5,
                "Electrolyte diffusivity [m2.s-1]": 1.5e-09,
                "Cation transference number": 0.35,
            },
        },
        {
            "name": "FastCharge-B",
            "role": "A + higher porosity (pos 0.40 / neg 0.35) lowering tortuosity at 4C",
            "struct": {
                "Negative particle radius [m]": 2.93e-06,
                "Electrolyte conductivity [S.m-1]": 2.5,
                "Electrolyte diffusivity [m2.s-1]": 1.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode porosity": 0.35,
                "Positive electrode porosity": 0.40,
            },
        },
        {
            "name": "FastCharge-C",
            "role": "A + N/P boost (negative thickness 85.2->110 um, N/P ~0.95->1.23) anti-plating capacity buffer at end of charge",
            "struct": {
                "Negative particle radius [m]": 2.93e-06,
                "Electrolyte conductivity [S.m-1]": 2.5,
                "Electrolyte diffusivity [m2.s-1]": 1.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode thickness [m]": 1.1e-04,
            },
        },
    ],
    "llm_reason": (
        "R1 gap: 4C plated (anode potential min -0.192 V) and charge acceptance only 0.176 Ah before 4.2 V cut "
        "-> cell-scale polarization cause -> Stage 3 architecture/transport levers. Parameters listed before running "
        "(name/unit/source): Negative particle radius [m] 5.86->2.93 um (architecture; x2 surface area, protocol "
        "measured reference small-particle plating-resistance contribution); Electrolyte conductivity [S.m-1] 2.5 "
        "constant (literature-informed ESTIMATE: concentrated LiFSI/carbonate blends 1.5-2.5 S/m; constant override "
        "removes Arrhenius T-dependence = also the lowT lever); Electrolyte diffusivity [m2.s-1] 1.5e-9 constant "
        "(optimistic ESTIMATE, same formulation); Cation transference number 0.35 (ESTIMATE, concentrated electrolytes "
        "0.3-0.5); Negative/Positive electrode porosity 0.35/0.40 (architecture, tortuosity); Negative electrode "
        "thickness [m] 1.1e-4 (N/P 0.95->1.23, anti-plating buffer, ED cost ~+8% negative mass). All else baseline. "
        "SEI kinetics untouched this round (progressive attribution: SEI@500 fix is the R3 coating lever). "
        "True -20C soak probes (Initial temperature 253.15 K) run alongside for severity check, not part of criteria."
    ),
}
append_entry(ws, entry)
print("propose R2 appended")
