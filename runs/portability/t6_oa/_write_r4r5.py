import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("portability/t6_oa", "runs")

# Round 4: DFN verification of the SPMe winner (LNMO-S7 / V7)
propose4 = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "SEI kinetic rate constant [m.s-1]": 2e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 100,
            },
            "name": "LNMO-S7 DFN-verification",
            "role": "re-run the SPMe winner (S7) under DFN to verify fast-charge safety at higher fidelity",
        },
    ],
    "llm_reason": (
        "SPMe screen showed S7 passes all 5 criteria (T_max 322.71K, anode +0.0298). "
        "Protocol requires DFN for passers. DFN resolves concentration gradients SPMe smooths over, "
        "so fast-charge (4C) polarization is expected to be larger."
    ),
}

# Round 5: DFN fast-charge re-optimization
propose5 = {
    "action": "propose",
    "round": 5,
    "candidates": [
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "Negative particle radius [m]": 1.5e-6,
                "Electrolyte conductivity [S.m-1]": 1.8,
                "Cation transference number": 0.4,
                "SEI kinetic rate constant [m.s-1]": 2e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 150,
            },
            "name": "LNMO-DFN-D1 transport",
            "role": "smaller anode particles (1.5um, faster solid diffusion) + high-conductivity electrolyte (1.8 S/m) to cut 4C anode/electrolyte polarization; cooling h=150",
        },
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "Negative particle radius [m]": 1.5e-6,
                "Electrolyte conductivity [S.m-1]": 1.8,
                "Cation transference number": 0.4,
                "SEI kinetic rate constant [m.s-1]": 2e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 300,
            },
            "name": "LNMO-DFN-D10 cooling-300",
            "role": "D1 electrochemistry (plating-safe, anode +0.043) + cooling h=300 to bring T_max under 323.15K",
        },
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "Negative particle radius [m]": 1.5e-6,
                "Electrolyte conductivity [S.m-1]": 1.8,
                "Cation transference number": 0.4,
                "SEI kinetic rate constant [m.s-1]": 2e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 400,
            },
            "name": "LNMO-DFN-D11 cooling-400",
            "role": "D1 electrochemistry + cooling h=400 for comfortable T_max margin (final candidate)",
        },
    ],
    "llm_reason": (
        "DFN shows S7 plates (anode -0.020V) and T_max 330.7K: 4C concentration polarization is larger in DFN. "
        "Diagnosis: anode solid-diffusion (D=3.3e-14, R=5.86um -> tau~1040s >> charge time) and electrolyte concentration "
        "polarization drive anode negative; 1C-discharge + 4C-charge reaction heat drives T_max. "
        "Fixes: (1) smaller anode particles 1.5um (tau~68s) + high-conductivity electrolyte 1.8 S/m to cut polarization; "
        "(2) note: speeding the positive electrode (reducing positive particle radius) enables deeper charge and re-triggers "
        "plating, so the positive is kept at baseline 5.22um (charge reaches ~27% SOC at 4C CC, limited by positive kinetics); "
        "(3) cooling h sweep 150/300/400 for T_max."
    ),
}

append_entry(ws, propose4)
append_entry(ws, propose5)
print("propose R4+R5 written")
