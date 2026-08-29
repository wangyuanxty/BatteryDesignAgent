"""Round-3 propose entry (t5_r2): 4 candidates attacking the 4C safety wall on the surviving ED platform.

All overridden parameters listed BEFORE running with units and sources:
  - Electrolyte conductivity [S.m-1] = 1.5 (from baseline Nyman2008 EC/EMC sigma(T) ~1.0-1.2 S/m at 298 K
    to advanced-liquid class ~1.2-1.6 S/m; source: literature (Nyman 2008; electrolyte engineering
    reviews), value chosen mid-range, marked ESTIMATE)
  - Cation transference number = 0.45 (baseline 0.2594 -> high-t+ electrolyte strategies reach
    0.4-0.65; source: Diederichsen et al., ACS Energy Lett. 2, 2563 (2017); marked ESTIMATE)
  - Electrolyte diffusivity [m2.s-1] = 3.5e-10 (baseline function ~2.7e-10 at 298 K; modest raise,
    marked ESTIMATE)
  - Negative electrode porosity 0.25->0.35, Positive electrode porosity 0.335->0.40 (design choices:
    lighter stack + better ionic network)
  - Negative particle radius [m] 5.86e-6->3.0e-6 (design choice: anode charge kinetics surface area)
  - Negative electrode thickness x1.15 on arch_C (N/P capacity buffer; with the 1.5-scale platform)
"""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

append_entry(ws, {
    "action": "propose",
    "round": 3,
    "candidates": [
        {"name": "B_elec", "role": "arch_B + electrolyte transport boost (sigma 1.5 S/m, t+ 0.45, D 3.5e-10; literature estimates) - cure 4C concentration/ohmic polarization that drives plating"},
        {"name": "B_elec_por", "role": "B_elec + porosity pos 0.40 / neg 0.35 - lighter stack (ED margin) and better ionic transport; watches 1C capacity delivery cliff"},
        {"name": "B_elec_particle", "role": "B_elec + negative particle radius 3.0 um - charge kinetics (activation overpotential) at 4C"},
        {"name": "C_elec_NP15", "role": "arch_C x1.5 platform + transport boost + negative thickness x1.15 (N/P buffer); ED-margin variant against plating"},
    ],
    "llm_reason": (
        "Round-2 established arch_B/arch_C pass ED (509.06/512.23) but plate at 4C with T_max up to "
        "369.9 K (evidence round-2 evaluate). Failure cause is transport-scale (electrolyte depletion "
        "at the anode during 4C charge) + activation/thermal -> solve at Stage 3 with the Stage-2 "
        "formulation bridge (transport overrides, literature-anchored estimates listed above) plus "
        "architecture dials (porosity, particle size, N/P). Thermal (cooling h) reserved for next "
        "round after transport effect is measured."
    ),
})
print("propose round 3 appended")