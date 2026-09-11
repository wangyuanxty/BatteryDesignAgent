import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("portability/t6_oa", "runs")

# Round 2: architecture variants targeting the three failures
propose2 = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
            },
            "name": "LNMO-S1 thin-cell",
            "role": "smartphone thin collectors/separator + thicker anode (N/P~1.04) to fix plating and boost volumetric ED",
        },
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "SEI kinetic rate constant [m.s-1]": 5e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 40,
            },
            "name": "LNMO-S2 thin-cell+coating+cooling",
            "role": "S1 + artificial-SEI coating (SEI k 5e-15, estimate) + cooling h=40 to fix SEI and T_max",
        },
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "SEI kinetic rate constant [m.s-1]": 5e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 40,
                "Negative particle radius [m]": 3e-6,
                "Electrolyte conductivity [S.m-1]": 1.8,
                "Cation transference number": 0.4,
            },
            "name": "LNMO-S3 +anode-kinetics",
            "role": "S2 + smaller anode particles + high-conductivity electrolyte to probe transport effect on plating/SEI",
        },
    ],
    "llm_reason": (
        "Baseline failures: plating (N/P~1.0), T_max 328.9K, SEI 753nm. "
        "Diagnosis: (1) plating from anode capacity ~equal to positive -> thicken anode + thin collectors/separator to raise N/P without losing volume; "
        "(2) T_max from 1C-discharge reaction heat at 45C -> raise cooling h; "
        "(3) SEI from LNMO 4.7V driving anode more negative -> artificial-SEI coating (SEI k reduction). "
        "S1 isolates geometry; S2 adds coating+cooling; S3 probes whether transport changes help."
    ),
}

# Round 3: refine coating strength + cooling sweep + N/P margin
propose3 = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "SEI kinetic rate constant [m.s-1]": 2e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 60,
            },
            "name": "LNMO-S4 stronger-coating+cooling",
            "role": "stronger artificial-SEI coating (k 2e-15) + cooling h=60",
        },
        {
            "struct": {
                "Negative electrode thickness [m]": 112e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "SEI kinetic rate constant [m.s-1]": 2e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 60,
            },
            "name": "LNMO-S5 +N/P-margin",
            "role": "S4 + thicker anode (112um, N/P~1.08) for extra plating margin",
        },
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "SEI kinetic rate constant [m.s-1]": 2e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 80,
            },
            "name": "LNMO-S6 cooling-80",
            "role": "S4 + cooling h=80 to bring T_max under 323.15K",
        },
        {
            "struct": {
                "Negative electrode thickness [m]": 108e-6,
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 7e-6,
                "SEI kinetic rate constant [m.s-1]": 2e-15,
                "Total heat transfer coefficient [W.m-2.K-1]": 100,
            },
            "name": "LNMO-S7 cooling-100",
            "role": "S4 + cooling h=100 for comfortable T_max margin",
        },
    ],
    "llm_reason": (
        "Round2: plating fixed by geometry (S2 anode_min +0.028V), SEI marginal (492.6nm), T_max still 324.9K. "
        "Round3 refinements: (1) stronger coating k=2e-15 to widen SEI margin; "
        "(2) sweep cooling h=60/80/100 to bring T_max below 323.15K; "
        "(3) one variant with thicker anode (112um) to check N/P margin benefit."
    ),
}

append_entry(ws, propose2)
append_entry(ws, propose3)
print("propose R2+R3 written")
