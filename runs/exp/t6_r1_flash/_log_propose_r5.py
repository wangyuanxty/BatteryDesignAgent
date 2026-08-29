import sys
from pathlib import Path

sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace(Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_flash"))

entry = {
    "action": "propose",
    "round": 5,
    "candidates": [
        {
            "name": "finA130",
            "role": "integrated final: archThin (sep 8um, CC 8/6um) + superTrans electrolyte (t+0.7, sigma 2.0, D 6e-10) + negative electrode 130um (N/P ~1.5) + h=60 - N/P sweep lower bound",
            "struct": {"Separator thickness [m]": 8e-6, "Positive current collector thickness [m]": 8e-6, "Negative current collector thickness [m]": 6e-6, "Cation transference number": 0.7, "Electrolyte conductivity [S.m-1]": 2.0, "Electrolyte diffusivity [m2.s-1]": 6e-10, "Negative electrode thickness [m]": 1.3e-4, "Total heat transfer coefficient [W.m-2.K-1]": 60},
            "props_source": "architecture = design choice; transport = estimate; thermal = estimate (vapor chamber stack)",
        },
        {
            "name": "finB140",
            "role": "N/P sweep mid: L_neg 140um",
            "struct": {"Separator thickness [m]": 8e-6, "Positive current collector thickness [m]": 8e-6, "Negative current collector thickness [m]": 6e-6, "Cation transference number": 0.7, "Electrolyte conductivity [S.m-1]": 2.0, "Electrolyte diffusivity [m2.s-1]": 6e-10, "Negative electrode thickness [m]": 1.4e-4, "Total heat transfer coefficient [W.m-2.K-1]": 60},
            "props_source": "architecture = design choice; transport = estimate",
        },
        {
            "name": "finC150",
            "role": "N/P sweep upper (diagnostic-verified M4 pass at +0.075 V): L_neg 150um; also carries 1C discharge for calc-energy",
            "struct": {"Separator thickness [m]": 8e-6, "Positive current collector thickness [m]": 8e-6, "Negative current collector thickness [m]": 6e-6, "Cation transference number": 0.7, "Electrolyte conductivity [S.m-1]": 2.0, "Electrolyte diffusivity [m2.s-1]": 6e-10, "Negative electrode thickness [m]": 1.5e-4, "Total heat transfer coefficient [W.m-2.K-1]": 60},
            "props_source": "architecture = design choice; transport = estimate",
        },
        {
            "name": "finSEI",
            "role": "SEI margin: EC diffusivity x0.3 (6e-19) on final architecture - target 470-480 nm (<500 with margin)",
            "struct": {"Separator thickness [m]": 8e-6, "Positive current collector thickness [m]": 8e-6, "Negative current collector thickness [m]": 6e-6, "Cation transference number": 0.7, "Electrolyte conductivity [S.m-1]": 2.0, "Electrolyte diffusivity [m2.s-1]": 6e-10, "Negative electrode thickness [m]": 1.5e-4, "EC diffusivity [m2.s-1]": 6e-19},
            "props_source": "estimate: LiF-rich artificial SEI coating blocks EC permeation",
        },
    ],
}

append_entry(ws, entry)
print("propose round 5 appended")
