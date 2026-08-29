# Round-4 propose entry (agent-built input script)
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t1_r1_flash", root="runs")

propose = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
                "Electrolyte conductivity [S.m-1]": 4.38,
                "Electrolyte diffusivity [m2.s-1]": 8.16e-10,
                "Cation transference number": 0.5,
            },
            "name": "ArchA-h150-F3",
            "role": "transport ceiling probe: sigma x3 (4.38 S/m at 45C-equivalent), D x3, t+ 0.5; upper bound of what advanced liquid electrolytes can deliver (values estimate)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
                "Negative electrode thickness [m]": 1.05e-4,
                "Electrolyte conductivity [S.m-1]": 2.19,
                "Electrolyte diffusivity [m2.s-1]": 4.08e-10,
                "Cation transference number": 0.4,
            },
            "name": "ArchA-h150-NP",
            "role": "N/P fix: negative 85.2->105 um (N/P ~1.35) lowers anode lithiation at 4.2 V -> higher anode OCP at end of charge; + F1 transport; ED cost ~462->~435 Wh/kg",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
                "Negative electrode thickness [m]": 1.15e-4,
                "Electrolyte conductivity [S.m-1]": 2.92,
                "Electrolyte diffusivity [m2.s-1]": 5.45e-10,
                "Cation transference number": 0.4,
            },
            "name": "ArchA-h150-NP2",
            "role": "stronger N/P (negative 115 um, ~1.48) + F2 transport; ED cost ~462->~418",
        },
    ],
    "llm_reason": "R3 showed transport fixes help monotonically (F2 anode min -0.029 V) but do not clear 0 V alone: the dip is dominated by end-of-charge anode surface saturation (charge stops at 4.2 V with only ~10% SOC delivered). Two-pronged round: (1) transport ceiling F3 tests whether pure formulation can reach 0 V; (2) N/P increase attacks the OCP term directly (same Li inventory over more negative capacity -> higher U_neg at EOC), combined with F1/F2 transport. ED margins stay >392.61 for both N/P candidates (est. 435 / 418).",
}
append_entry(ws, propose)
print("propose R4 written")
