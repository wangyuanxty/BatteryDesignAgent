"""Round-5 propose entry (t5_r2): decouple plating margin from cell temperature.

Parameter list BEFORE running (units + sources):
  - Cation transference number 0.45->0.60 (high-t+ electrolyte upper regime; Diederichsen et al.,
    ACS Energy Lett. 2, 2563 (2017) measures t+ up to ~0.6-0.7; marked ESTIMATE)
  - Electrolyte diffusivity [m2.s-1] 3.5e-10->5.0e-10 (advanced electrolyte estimate; marked ESTIMATE)
  - Negative particle radius [m] re-added 3.0e-6 (R3 measured +41 mV plating margin at h=10)
  - Negative electrode porosity 0.45 / Positive 0.43 (R4 measured: +0.05 neg porosity = +13.7 mV
    at h=50; anode-electrolyte transport is the plating dial)
  - C: Negative electrode thickness [m] +10% (1.2184e-4; N/P buffer, anode OCP floor)
  - Total heat transfer coefficient [W.m-2.K-1] = 60 (A/B/C) / 100 (D) - design choices in the
    thermal-management freedom (liquid cooling classes; domain experience, no precise source)

Reasoning: R4 showed cooling alone re-plates the cell (sluggish kinetics at lower T); the fix is to
raise the plating MARGIN at cool-cell temperatures via anode-side transport so strong cooling
(h 60-100) can bring T_max under 333.15 while anode potential stays positive.
"""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

append_entry(ws, {
    "action": "propose",
    "round": 5,
    "candidates": [
        {"name": "e5_A", "role": "t+ 0.6 + D 5e-10 + neg particle 3um + h 60 on e2 platform - transport-first plating margin at cooled cell"},
        {"name": "e5_B", "role": "e5_A + neg porosity 0.45 / pos por 0.43 (anode ionic network + mass cut); h 60"},
        {"name": "e5_C", "role": "e5_B + negative thickness +10% (N/P buffer, OCP floor); h 60"},
        {"name": "e5_D", "role": "e5_B + h 100 (immersion-class cooling bracket)"},
    ],
    "llm_reason": (
        "R4 evidence: T_max vs ap_min anti-correlated through cell temperature under h-sweep "
        "(h10: T367/ap+0.0138; h80: T334/ap-0.0285) - no h alone satisfies both. Root cause: "
        "cool-cell kinetics. Correction: raise plating margin at low T via anode-electrolyte "
        "transport (t+/D/porosity/particle + N/P arm), then re-cool. All measured as full triads."
    ),
})
print("propose round 5 appended")