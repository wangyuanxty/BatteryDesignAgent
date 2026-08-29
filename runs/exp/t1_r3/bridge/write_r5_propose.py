# -*- coding: utf-8 -*-
"""t1_r3 — R5 propose entry: nominal-capacity correction on V9 finalist."""
import sys

from bda.store import CaseWorkspace, append_entry


def main() -> int:
    ws = CaseWorkspace("exp/t1_r3")
    append_entry(ws, {
        "action": "propose",
        "round": 5,
        "candidates": [
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
                    "Nominal cell capacity [A.h]": 5.085,
                },
                "name": "V11_final",
                "role": "V9 finalist with nominal capacity corrected to measured 1C capacity (5.085 Ah). "
                        "4C protocol current = 4x5.085 = 20.34 A = true 4C of the cell's measured capacity. "
                        "R4 acceptance re-read: reported capacity_ah is C-rate-normalized duration; "
                        "true Ah = reported x nominal. V9 charged 4.65 Ah = 91.4% of 5.085 Ah at 20 A "
                        "(3.93C true) in 14.0 min with anode +0.0424 V margin and T_max 321.0 K. "
                        "V11 re-runs the 4C protocol at the corrected true-4C current to confirm no plating.",
            },
        ],
        "llm_reason": (
            "R4 all three variants pass stage3 (plated=false, T_max<333.15K) and stage2 ED (556-615 Wh/kg "
            "vs 392.61). Units diagnosis of the acceptance 'plateau': the runner's charge capacity_ah is "
            "duration x C_rate/3600 (C-rate-normalized duration); the experiment current is C_rate x "
            "Nominal cell capacity. True accepted Ah = reported x nominal. V8: 1.204x2.6 = 3.13 Ah = 93.6% "
            "of its 3.345 Ah measured 1C capacity; V9: 0.929x5 = 4.65 Ah = 91.4% of 5.085 Ah; "
            "V10: 1.217x3.3 = 4.02 Ah = 95.7% of 4.199 Ah. The earlier '~32-46% SOC' reading compared "
            "C-h units against nominal Ah — wrong. V9 is the honest best: its nominal (5 Ah) already "
            "equals measured capacity within 1.7%, so the 4C protocol ran at 3.93C true. V11 closes the "
            "last 1.7% by setting nominal = measured 5.085 Ah so the 4C current (20.34 A) is true 4C. "
            "No excluded levers touched (nominal capacity is an allowed scaling label; all other keys "
            "unchanged from V9)."
        ),
    })
    print("R5 propose entry appended")
    return 0


if __name__ == "__main__":
    sys.exit(main())
