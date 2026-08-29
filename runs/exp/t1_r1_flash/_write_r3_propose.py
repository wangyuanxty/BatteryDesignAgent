# Round-3 propose entry (agent-built input script)
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t1_r1_flash", root="runs")

propose = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
                "Electrolyte conductivity [S.m-1]": 2.19,
                "Electrolyte diffusivity [m2.s-1]": 4.08e-10,
                "Cation transference number": 0.4,
            },
            "name": "ArchA-h150-F1",
            "role": "high-transport electrolyte formulation (sigma x1.5 at 45C, D x1.5, t+ 0.259->0.4): shrink anode electrolyte-phase overpotential -> raise anode potential above 0 V at 4C",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
                "Electrolyte conductivity [S.m-1]": 2.92,
                "Electrolyte diffusivity [m2.s-1]": 5.45e-10,
                "Cation transference number": 0.4,
            },
            "name": "ArchA-h150-F2",
            "role": "aggressive high-transport electrolyte (sigma x2.0, D x2.0, t+ 0.4): upper-bound probe of transport fix",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
                "Negative particle radius [m]": 3.0e-6,
            },
            "name": "ArchA-h150-P1",
            "role": "particle-size lever: negative particle 5.86->3 um (higher surface area, shorter solid diffusion path, lower local current density)",
        },
    ],
    "llm_reason": "R2: cooling fixed T_max (326.6/327.7 K) but exposed plating (-0.077/-0.107 V). Cause lives in anode transport, not architecture: at ~54 C cell temperature the anode cannot sustain 4C without surface-potential inversion. Fall back to the electrolyte formulation DOF (t1_r1 lesson: sigma_e is the root-cause lever): sigma/D x1.5-2.0 and t+ 0.4 are literature-informed estimates for high-conductivity/single-ion-like formulations (LiFSI-based / dilute or anion-trapping electrolytes; values marked estimate, not simulation output). P1 isolates the particle-size lever as an alternative route.",
}
append_entry(ws, propose)
print("propose R3 written")
