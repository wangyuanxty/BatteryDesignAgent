import json
from pathlib import Path
import sys

sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace(Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_flash"))

entry = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {
            "name": "seiDEC50",
            "role": "electrode modification coating (artificial SEI / Al2O3+LiF interphase): EC diffusivity through SEI x0.5 (2e-18 -> 1e-18) - r3 root cause: growth is EC-diffusion-limited (L/D_ec*k_exp >> 1 at ~700 nm), final thickness ~ sqrt(D_ec)",
            "struct": {"EC diffusivity [m2.s-1]": 1e-18},
            "props_source": "estimate: LiF-rich interphase blocks EC permeation (domain experience, no precise source)",
        },
        {
            "name": "seiDEC40",
            "role": "coating stronger: EC diffusivity x0.4 (8e-19) - margin version for 500 nm target",
            "struct": {"EC diffusivity [m2.s-1]": 8e-19},
            "props_source": "estimate: same coating, stronger effect",
        },
        {
            "name": "tplus70",
            "role": "electrolyte formulation: cation transference number 0.26 -> 0.7 (single-ion-like): diffusion potential ~ (1-t+) drops 0.74->0.3, lifts anode surface potential at 4C cutoff - isolate t+ lever on plating",
            "struct": {"Cation transference number": 0.7},
            "props_source": "estimate: single-ion conductor / immobilized-anion formulation (domain experience; LiFSI-PEO class)",
        },
        {
            "name": "superTrans",
            "role": "electrolyte max transport (t+0.7, sigma 2.0 S/m, D 6e-10) + thermal h=60: combined M4+M5 signal in one run",
            "struct": {
                "Cation transference number": 0.7,
                "Electrolyte conductivity [S.m-1]": 2.0,
                "Electrolyte diffusivity [m2.s-1]": 6e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 60,
            },
            "props_source": "estimate: high-t+ + high-sigma + high-D formulation",
        },
    ],
}

append_entry(ws, entry)
print("propose round 4 appended")
