# -*- coding: utf-8 -*-
"""t1_r3 — R2 propose entry."""
import sys

from bda.store import CaseWorkspace, append_entry


def main() -> int:
    ws = CaseWorkspace("exp/t1_r3")
    append_entry(ws, {
        "action": "propose",
        "round": 2,
        "candidates": [
            {
                "struct": {
                    "Electrolyte conductivity [S.m-1]": 1.4,
                    "Electrolyte diffusivity [m2.s-1]": 4.2e-10,
                    "Cation transference number": 0.4,
                    "Negative electrode porosity": 0.4,
                    "Positive electrode porosity": 0.42,
                    "Separator thickness [m]": 9e-6,
                    "Total heat transfer coefficient [W.m-2.K-1]": 80.0,
                },
                "name": "V1_transport",
                "role": "transport upgrade: sigma 1.4 S/m (Nyman2008 @45C magnitude), D 4.2e-10, "
                        "t+ 0.40 (high-transference formulation, estimate), porosity up, separator 9 um, liquid cooling h=80",
            },
            {
                "struct": {
                    "Positive electrode thickness [m]": 60e-6,
                    "Negative electrode thickness [m]": 68e-6,
                    "Nominal cell capacity [A.h]": 3.97,
                    "Electrolyte conductivity [S.m-1]": 1.4,
                    "Electrolyte diffusivity [m2.s-1]": 4.2e-10,
                    "Cation transference number": 0.4,
                    "Negative electrode porosity": 0.4,
                    "Positive electrode porosity": 0.42,
                    "Separator thickness [m]": 9e-6,
                    "Total heat transfer coefficient [W.m-2.K-1]": 80.0,
                },
                "name": "V2_thin",
                "role": "electrodes thinned -21/-20% (diffusion path shortened, true 4C of a 3.97 Ah cell; "
                        "nominal capacity scaled to positive thickness, N/P unchanged) + V1 transport pack",
            },
            {
                "struct": {
                    "Positive particle radius [m]": 2.61e-6,
                    "Negative particle radius [m]": 2.93e-6,
                    "Electrolyte conductivity [S.m-1]": 1.4,
                    "Electrolyte diffusivity [m2.s-1]": 4.2e-10,
                    "Cation transference number": 0.4,
                    "Negative electrode porosity": 0.4,
                    "Positive electrode porosity": 0.42,
                    "Separator thickness [m]": 9e-6,
                    "Total heat transfer coefficient [W.m-2.K-1]": 80.0,
                },
                "name": "V3_particles",
                "role": "particle radii halved (kinetic overpotential down, plating margin up) + V1 transport pack",
            },
            {
                "struct": {
                    "Total heat transfer coefficient [W.m-2.K-1]": 80.0,
                },
                "name": "V4_cooling",
                "role": "thermal isolation: h 10->80 W/m2K (liquid cooling) only — separates T_max fix from plating fix",
            },
        ],
        "llm_reason": (
            "R1 baseline 4C leg: anode min -0.19 V (plated) and only 0.176 Ah accepted before 4.2 V cap -> "
            "salt-depletion/concentration-polarization dominated (negative porosity 0.25 tortuous path, t+ 0.26, "
            "Nyman conductivity). Four orthogonal probes: V1 transport-only, V2 geometry (thin electrodes, "
            "N/P preserved, nominal capacity rescaled so '4C' stays a true 4C), V3 kinetics (half particle radii), "
            "V4 cooling-only. All parameter keys verified present in Chen2020 (bridge/base_dump.json)."
        ),
    })
    print("R2 propose entry appended")
    return 0


if __name__ == "__main__":
    sys.exit(main())
