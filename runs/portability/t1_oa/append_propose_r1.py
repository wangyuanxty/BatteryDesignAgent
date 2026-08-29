import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t1_oa", "runs/portability")

propose = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "struct": {
                "Electrolyte conductivity [S.m-1]": 2.0,
                "Cation transference number": 0.5,
            },
            "name": "V1-high-conductivity-electrolyte",
            "role": "raise electrolyte conductivity 1.1->2.0 S/m (advanced LiFSI/carbonate) and transference number 0.26->0.5 to cut ohmic+concentration polarization, lifting anode potential above 0 V at 4C",
        },
        {
            "struct": {
                "Electrolyte conductivity [S.m-1]": 2.0,
                "Cation transference number": 0.5,
                "Negative particle radius [m]": 3.0e-6,
                "Positive particle radius [m]": 3.0e-6,
            },
            "name": "V2-transport-plus-nano-particles",
            "role": "V1 plus smaller active particles (5.86->3.0 um neg / 5.22->3.0 um pos) to relieve solid-diffusion polarization during 4C charge",
        },
        {
            "struct": {
                "Electrolyte conductivity [S.m-1]": 2.5,
                "Cation transference number": 0.6,
                "Electrolyte diffusivity [m2.s-1]": 2.0e-10,
                "Negative particle radius [m]": 2.0e-6,
            },
            "name": "V3-max-transport",
            "role": "aggressive transport: conductivity 2.5 S/m, t+=0.6, electrolyte diffusivity 2e-10 m2/s (vs ~3e-10 baseline function), negative particle 2.0 um",
        },
    ],
    "llm_reason": "Chen2020 baseline: ED 400.29 Wh/kg >= 392.61 (pass), T_max 332.35K <= 333.15 (pass, thin margin), overcharge triggered=false (pass), but 4C plating fails (anode min -0.438 V). Plating fix via electrolyte transport (conductivity/t+/diffusivity) and particle radius does NOT add mass -> ED preserved; higher conductivity also cuts ohmic heat -> T_max margin widens. OKane2022 (SiOx) has no plating but T_max 368K (35K over); fixable but larger lift. Choose Chen2020 as base.",
}

append_entry(ws, propose)
print("propose round 1 appended")
