"""t4_r3: propose entry round 7 — DFN confirmation of V17 + plating-margin variant V18."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")

propose_r7 = {
    "action": "propose",
    "round": 7,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 60,
                "Negative particle radius [m]": 2.0e-6,
                "Positive particle radius [m]": 2.5e-6,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 6.0e-10,
                "Cation transference number": 0.5,
            },
            "name": "V17_ok_h60_elx_plus_DFN",
            "role": "DFN-mode confirmation of the V17 SPMe passer (same params, --mode dfn): precise 1C/lowT/4C45 re-computation against entry-0 criteria",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 50,
                "Negative particle radius [m]": 2.0e-6,
                "Positive particle radius [m]": 2.5e-6,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 6.0e-10,
                "Cation transference number": 0.5,
            },
            "name": "V18_ok_h50_elx_plus_DFN",
            "role": "plating-margin variant: h lowered 60->50 W/m2/K (uses V17's 4.4 K T_max headroom to warm the 4C charge ~3-4 K) while keeping transport/radii; DFN mode",
        },
    ],
    "llm_reason": (
        "Round 6: V17 SPMe passes all five checked criteria (retention 97.91, ED_kg 514.3, ED_L 976.0, "
        "T_max 328.73, no plating +0.0063 V). Thin margins demand DFN precision (protocol rule: SPMe "
        "proxy screens, DFN confirms passers). V18 is a margin-engineering variant inside the criteria "
        "box: SPMe heat balance projects T_max ~332 K at h=50 (still <333.15), and warmer 4C charge "
        "should widen the anode-potential margin. No parameter outside the sanctioned DoF is touched; "
        "V17/V18 params differ only in the cooling coefficient."
    ),
}
append_entry(ws, propose_r7)
print("propose r7 written")