from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")

entry = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {"struct": {"Positive particle radius [m]": 2.0e-6, "Negative particle radius [m]": 2.5e-6},
         "name": "V1_SmallParticles",
         "role": "particle radius 5.22/5.86 um -> 2.0/2.5 um (diffusion time ~r^2/D_s and charge-transfer area)"},
        {"struct": {"Positive electrode thickness [m]": 4.0e-5, "Negative electrode thickness [m]": 5.2e-5},
         "name": "V2_ThinElectrodes",
         "role": "electrode thickness 75.6/85.2 um -> 40/52 um (ionic path and areal load down; N/P raised toward plating margin)"},
        {"struct": {"Electrolyte conductivity [S.m-1]": 1.5, "Electrolyte diffusivity [m2.s-1]": 2.5e-10,
                    "Cation transference number": 0.35},
         "name": "V3_FastElectrolyte",
         "role": "electrolyte transport boost vs Nyman2008 baseline kappa=0.949 S/m, D=1.77e-10, t+=0.259 (advanced formulation, estimate)"},
        {"struct": {"Positive electrode porosity": 0.42, "Negative electrode porosity": 0.35},
         "name": "V4_HighPorosity",
         "role": "porosity 0.335/0.25 -> 0.42/0.35 (ionic transport up at the cost of active-material loading)"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 30.0},
         "name": "V5_ActiveCooling",
         "role": "cooling h 10 -> 30 W/m2/K (forced-air class thermal management)"},
        {"struct": {"Positive electrode thickness [m]": 4.0e-5, "Negative electrode thickness [m]": 5.2e-5,
                    "Positive particle radius [m]": 2.0e-6, "Negative particle radius [m]": 2.5e-6,
                    "Positive electrode porosity": 0.42, "Negative electrode porosity": 0.35,
                    "Electrolyte conductivity [S.m-1]": 1.5, "Electrolyte diffusivity [m2.s-1]": 2.5e-10,
                    "Cation transference number": 0.35,
                    "Total heat transfer coefficient [W.m-2.K-1]": 30.0},
         "name": "V6_ComboCeiling",
         "role": "all levers combined: opening ceiling assessment of the architecture+formulation space"},
    ],
    "llm_reason": (
        "Round-1 diagnosis: 5C retention 0.087, plating at 4C, T_max 354.3 K are all transport/architecture-"
        "scale (thick energy-cell electrodes, slow electrolyte, natural-convection cooling). Round 2 isolates "
        "one lever per candidate for attribution; V6 probes the combined ceiling. Nominal capacity per "
        "candidate set to its design value (anode-limited scaling of the measured 4.947 Ah baseline: "
        "Q_nom = 4.947 x (L_neg/85.2um) x (amf_neg/0.75)) so C-rate currents match the designed cell: "
        "V1/V3/V5 = 4.95 Ah, V2 = 3.02 Ah, V4 = 4.29 Ah, V6 = 2.62 Ah (self-consistency verified by the "
        "1C run itself). Electrolyte override constants calibrated from Nyman2008 evaluation (kappa=0.9487 "
        "S/m, D=1.769e-10 m2/s at 1M); 1.5 S/m / 2.5e-10 / t+=0.35 marked as advanced-formulation "
        "literature estimates (domain experience, no precise source)."
    ),
}

append_entry(WS, entry)
print("propose round 2 appended")
