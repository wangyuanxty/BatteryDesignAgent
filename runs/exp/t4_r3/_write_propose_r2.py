"""t4_r3: write propose entry for round 2 (parameters listed up-front per SKILL bridge rule)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")

propose_r2 = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
            },
            "name": "V1_thin_pack",
            "role": "inactive-layer slimming: CCs 16/12->8/6 um, separator 12->8 um; pack 200.8->182.8 um targets vol-ED >= 880 at unchanged energy",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Negative electrode thickness [m]": 1.0e-4,
            },
            "name": "V2_thin_pack_NP125",
            "role": "V1 + negative thicker 85.2->100 um (N/P thickness ratio ~1.18): anode capacity buffer to lift 4C charge anode potential (plating gate)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Negative electrode thickness [m]": 1.0e-4,
                "Positive electrode thickness [m]": 8.5e-5,
            },
            "name": "V3_thin_pack_both",
            "role": "V2 + positive thicker 75.6->85 um: capacity headroom + polarization relief under fixed 5 A",
        },
        {
            "struct": {
                "Electrolyte conductivity [S.m-1]": 1.2,
                "Electrolyte diffusivity [m2.s-1]": 3.0e-10,
                "Cation transference number": 0.4,
            },
            "name": "V4_cold_elx",
            "role": "cold-temperature electrolyte formulation via transport bridge on baseline geometry: T-independent sigma=1.2 S/m, D=3e-10 m2/s, t+=0.4 (vs baseline t+=0.2594)",
        },
    ],
    "llm_reason": (
        "Round 2 splits the two failed metrics onto separable levers. vol-ED: measured baseline energy is "
        "time-capped at ~5 Ah drawn, so thinning inactive layers (V1) is the direct lever; N/P thickening "
        "(V2/V3) adds plating margin and uses part of the volume savings. Plating: baseline anode potential "
        "min -0.438 V at 4C/45C end-of-charge; levers tested independently are anode capacity buffer "
        "(V2/V3) and electrolyte transport (V4). Values listed before running. Sources: geometry values = "
        "architecture design (this run's own proposal); V4 transport values = domain-estimate formulation "
        "bridge (literature-order 1M LiPF6 EC/EMC sigma~1.0-1.2 S/m at 298K; t+=0.4, D=3e-10 as "
        "wide-temperature formulation direction) - marked ESTIMATE, not simulation output; T-independence "
        "of sigma/D is the crude model form of a wide-temperature electrolyte. All variants on Chen2020 "
        "(start_stage=3; no Stage-2 molecular work this round)."
    ),
}
append_entry(ws, propose_r2)
print("propose r2 written")