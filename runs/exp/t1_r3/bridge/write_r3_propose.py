# -*- coding: utf-8 -*-
"""t1_r3 — R3 propose entry."""
import sys

from bda.store import CaseWorkspace, append_entry


def main() -> int:
    ws = CaseWorkspace("exp/t1_r3")
    append_entry(ws, {
        "action": "propose",
        "round": 3,
        "candidates": [
            {
                "struct": {
                    "Electrolyte conductivity [S.m-1]": 1.6,
                    "Electrolyte diffusivity [m2.s-1]": 5.0e-10,
                    "Cation transference number": 0.5,
                    "Negative electrode porosity": 0.42,
                    "Positive electrode porosity": 0.45,
                    "Separator thickness [m]": 8e-6,
                    "Separator porosity": 0.6,
                    "Negative electrode thickness [m]": 110e-6,
                    "Positive particle radius [m]": 1.5e-6,
                    "Negative particle radius [m]": 1.5e-6,
                    "Total heat transfer coefficient [W.m-2.K-1]": 100.0,
                },
                "name": "V5_fastcharge_plus",
                "role": "acceptance push: sigma 1.6/t+ 0.5/D 5e-10 (advanced electrolyte, literature-consistent "
                        "45C values), porosity up, sep 8um+0.6, N/P 1.29 via 110um negative (higher anode OCP "
                        "-> more 4.2V budget + plating margin), 1.5um particles, liquid cooling h=100",
            },
            {
                "struct": {
                    "Positive electrode thickness [m]": 55e-6,
                    "Negative electrode thickness [m]": 80e-6,
                    "Nominal cell capacity [A.h]": 3.6,
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
                "name": "V6_thin_fastcharge",
                "role": "thin electrodes (pos 55um, neg 80um, nominal 3.6Ah rescaled, N/P 1.29) + V5 pack: "
                        "shorter diffusion path, lower 4C current, true 4C of a smaller cell",
            },
            {
                "struct": {
                    "Electrolyte conductivity [S.m-1]": 1.4,
                    "Electrolyte diffusivity [m2.s-1]": 4.2e-10,
                    "Cation transference number": 0.4,
                    "Negative electrode porosity": 0.4,
                    "Positive electrode porosity": 0.42,
                    "Separator thickness [m]": 9e-6,
                    "Negative electrode thickness [m]": 110e-6,
                    "Total heat transfer coefficient [W.m-2.K-1]": 80.0,
                },
                "name": "V7_np_only",
                "role": "N/P isolation: V1 transport pack + 110um negative only — quantifies the N/P lever "
                        "on 4C acceptance and anode margin",
            },
        ],
        "llm_reason": (
            "R2: transport pack cleared plating (V1 +0.005V) and T_max (327.8K) but 4C acceptance only "
            "0.4-0.7Ah — terminal voltage hits the 4.2V cap almost immediately, i.e. overpotential budget "
            "still too thin for a genuine 4C fast charge. R3 pushes acceptance: stronger electrolyte "
            "(sigma 1.6, t+ 0.5, D 5e-10 — advanced-formulation values, marked literature/estimate), "
            "N/P 1.29 (thicker negative raises anode OCP at fixed SOC -> both voltage budget and plating margin), "
            "1.5um particles (2x surface vs V3), thinner separator. V6 adds positive thinning (55um) with "
            "nominal capacity rescaled so 4C stays a true 4C. V7 isolates the N/P lever. "
            "Cooling h=100 (liquid-cooled pack). All keys verified present in Chen2020."
        ),
    })
    print("R3 propose entry appended")
    return 0


if __name__ == "__main__":
    sys.exit(main())
