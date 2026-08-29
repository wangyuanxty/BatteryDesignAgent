from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")

entry = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {"struct": {"Negative electrode thickness [m]": 5.8e-5},
         "name": "V7_NPMargin",
         "role": "V6 + anode 52->58 um (widen plating margin from the thin +14 mV of V6; Q_nom 2.94, cathode-limited estimate)"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 15.0},
         "name": "V8_Cooling15",
         "role": "V6 + cooling h 30->15 W/m2/K (relax toward light forced-air cooling realistic for power tools; Q_nom 3.08 fixed point)"},
        {"struct": {"Electrolyte conductivity [S.m-1]": 1.2, "Electrolyte diffusivity [m2.s-1]": 2.0e-10,
                    "Cation transference number": 0.3},
         "name": "V9_ModerateElectrolyte",
         "role": "V6 + electrolyte kappa 1.5->1.2 S/m, D 2.5->2.0e-10, t+ 0.35->0.30 (closer to realistic LiPF6-with-additive formulation; Q_nom 3.08)"},
        {"struct": {"Positive electrode porosity": 0.335, "Negative electrode porosity": 0.25},
         "name": "V10_NoPorosityBoost",
         "role": "V6 with porosity rolled back to baseline 0.335/0.25 (check whether the porosity boost is needed; Q_nom 3.02)"},
        {"struct": {},
         "name": "V11_FixedPointCombo",
         "role": "V6 combo with Q_nom corrected to the measured fixed point 3.08 Ah (true 5C = 15.4 A / 4C = 12.3 A reference design)"},
    ],
    "llm_reason": (
        "V6 passes all criteria but with three soft spots: Q_nom 2.62 understated C-rates by ~15% "
        "(measured 1C = 3.078 Ah), the plating margin was only +14 mV, and h=30 plus the aggressive "
        "electrolyte constants are the least defensible levers. Round 3 refines: V11 re-tests the combo "
        "at the fixed-point nominal; V7 widens the plating margin via N/P; V8 relaxes cooling; V9 uses "
        "moderate electrolyte transport; V10 checks whether the porosity boost can be dropped."
    ),
}

append_entry(WS, entry)
print("propose round 3 appended")
