# -*- coding: utf-8 -*-
"""t1_r3 — R4 propose entry."""
import sys

from bda.store import CaseWorkspace, append_entry


def main() -> int:
    ws = CaseWorkspace("exp/t1_r3")
    append_entry(ws, {
        "action": "propose",
        "round": 4,
        "candidates": [
            {
                "struct": {
                    "Positive electrode thickness [m]": 40e-6,
                    "Negative electrode thickness [m]": 60e-6,
                    "Nominal cell capacity [A.h]": 2.6,
                    "Positive current collector thickness [m]": 10e-6,
                    "Negative current collector thickness [m]": 6e-6,
                    "Electrolyte conductivity [S.m-1]": 1.6,
                    "Electrolyte diffusivity [m2.s-1]": 5.0e-10,
                    "Cation transference number": 0.5,
                    "Negative electrode porosity": 0.42,
                    "Positive electrode porosity": 0.45,
                    "Separator thickness [m]": 8e-6,
                    "Separator porosity": 0.6,
                    "Positive particle radius [m]": 1.5e-6,
                    "Negative particle radius [m]": 1.5e-6,
                    "Total heat transfer coefficient [W.m-2.K-1]": 100.0,
                },
                "name": "V8_ultrathin",
                "role": "ultrathin 40/60um electrodes (nominal 2.6Ah rescaled, N/P 1.33), thin CCs 10/6um "
                        "to hold ED — diffusion path halved, 4C current down to 10.4A",
            },
            {
                "struct": {
                    "Positive current collector thickness [m]": 10e-6,
                    "Negative current collector thickness [m]": 6e-6,
                    "Electrolyte conductivity [S.m-1]": 1.8,
                    "Electrolyte diffusivity [m2.s-1]": 6.0e-10,
                    "Cation transference number": 0.55,
                    "Negative electrode porosity": 0.42,
                    "Positive electrode porosity": 0.45,
                    "Separator thickness [m]": 8e-6,
                    "Separator porosity": 0.6,
                    "Positive particle radius [m]": 0.8e-6,
                    "Negative particle radius [m]": 0.8e-6,
                    "Total heat transfer coefficient [W.m-2.K-1]": 120.0,
                },
                "name": "V9_nano_aggressive",
                "role": "full 5Ah geometry + aggressive kinetics/transport: 0.8um particles (2x surface vs 1.5um), "
                        "sigma 1.8 / t+ 0.55 / D 6e-10 (advanced electrolyte, literature/estimate), thin CCs, h=120",
            },
            {
                "struct": {
                    "Positive electrode thickness [m]": 50e-6,
                    "Negative electrode thickness [m]": 72e-6,
                    "Nominal cell capacity [A.h]": 3.3,
                    "Positive current collector thickness [m]": 10e-6,
                    "Negative current collector thickness [m]": 6e-6,
                    "Electrolyte conductivity [S.m-1]": 1.8,
                    "Electrolyte diffusivity [m2.s-1]": 5.5e-10,
                    "Cation transference number": 0.5,
                    "Negative electrode porosity": 0.42,
                    "Positive electrode porosity": 0.45,
                    "Separator thickness [m]": 8e-6,
                    "Separator porosity": 0.6,
                    "Positive particle radius [m]": 1.0e-6,
                    "Negative particle radius [m]": 1.0e-6,
                    "Total heat transfer coefficient [W.m-2.K-1]": 100.0,
                },
                "name": "V10_hybrid",
                "role": "middle path: 50/72um (nominal 3.3Ah, N/P 1.25), 1.0um particles, sigma 1.8/t+ 0.5/D 5.5e-10, "
                        "thin CCs, h=100 — balances capacity retention vs 4C acceptance",
            },
        ],
        "llm_reason": (
            "R3: plating cleared with margin (V5/V6 +0.025/+0.033V) and T_max 320-322K, but 4C acceptance stuck "
            "at ~1.1-1.2Ah — terminal voltage still caps at ~32% SOC, so residual polarization ~0.5V at 4C "
            "must come down. Diagnosis from R2/R3: kinetics slow (i0 ~5.4/0.8 A/m2 measured from Chen2020 "
            "exchange-current functions at 45C) + electrolyte concentration polarization; V7 showed N/P up "
            "hurts via diffusion path. R4 attacks both: V8 cuts the diffusion path and current (ultrathin, "
            "true-4C rescaled), V9 maximizes surface/transport at full 5Ah, V10 the compromise. "
            "CCs thinned 16/12->10/6um so ED stays well above 392.61 despite lower capacity. "
            "All keys verified present in Chen2020."
        ),
    })
    print("R4 propose entry appended")
    return 0


if __name__ == "__main__":
    sys.exit(main())
