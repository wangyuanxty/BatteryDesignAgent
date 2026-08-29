# Round-5 propose entry (agent-built input script)
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t1_r1_flash", root="runs")

propose = {
    "action": "propose",
    "round": 5,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
                "Electrolyte conductivity [S.m-1]": 4.38,
                "Electrolyte diffusivity [m2.s-1]": 1.09e-9,
                "Cation transference number": 0.6,
            },
            "name": "ArchA-h150-F4",
            "role": "single-ion-like high-transport formulation: sigma 4.38 S/m (x3), D x4, t+ 0.6; final nudge to clear the -2.3 mV gap (values estimate)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Electrolyte diffusivity [m2.s-1]": 1.2e-9,
                "Cation transference number": 0.65,
            },
            "name": "ArchA-h150-F4b",
            "role": "margin variant of F4 (sigma 5.0, D x4.4, t+ 0.65): target anode min >= +10 mV",
        },
    ],
    "llm_reason": "R4 narrowed the failure to -2.3 mV with the transport ceiling (F3: sigma x3/D x3/t+ 0.5); N/P levers rejected (deeper charge into surface saturation). The concentration-polarization term scales ~(1-t+)/t+ and D^-1: t+ 0.5->0.6 and D x3->x4 should add ~5-15 mV. F4/F4b are single-ion-like liquid formulations (literature-informed estimates; single-ion polymer/anion-trapping concepts report t+ 0.6-0.9, low-viscosity high-D solvents ~1e-9 m2/s). Winner gets the full confirmation suite.",
}
append_entry(ws, propose)
print("propose R5 written")
