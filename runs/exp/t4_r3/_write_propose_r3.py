"""t4_r3: propose entry round 3 — particle-radius lever for the plating gate."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")

propose_r3 = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Negative particle radius [m]": 3.5e-6,
            },
            "name": "V5_thin_pack_Rneg35",
            "role": "V1 geometry + negative particle radius 5.86->3.5 um: cut graphite solid-diffusion time (R^2/D) by 2.8x to lift 4C end-of-charge anode potential (plating gate)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Negative particle radius [m]": 3.0e-6,
                "Positive particle radius [m]": 3.5e-6,
            },
            "name": "V6_thin_pack_Rneg30_Rpos35",
            "role": "V5 + positive particle radius 5.22->3.5 um: relieve positive diffusion overpotential at 4C too",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Negative particle radius [m]": 2.5e-6,
                "Positive particle radius [m]": 3.0e-6,
            },
            "name": "V7_thin_pack_Rneg25_Rpos30",
            "role": "aggressive particle shrink (neg 2.5 um / pos 3.0 um): maximize 4C plating margin",
        },
    ],
    "llm_reason": (
        "Round 2 diagnosis: V2/V3 (thicker negative) made anode potential WORSE (-0.493/-0.444 vs baseline "
        "-0.438 V) and V4 transport (-0.440 V) barely moved it -> the 4C end-of-charge plating signature is "
        "dominated by solid-phase diffusion in the graphite particles (Chen2020 has temperature-independent "
        "constant D_s), not electrolyte transport and not N/P buffer. Symptom-to-scale mapping: particle "
        "size is the architecture lever at the diffusion scale. V1 geometry (vol-ED 927.3 Wh/L already "
        "passes) is kept as the base; particle radii are the only new d.o.f. Values listed before running; "
        "sources: architecture design values (this run's proposal); particle-size - diffusion-time scaling "
        "is standard electrode-design physics (domain experience). All variants Chen2020, start_stage=3."
    ),
}
append_entry(ws, propose_r3)
print("propose r3 written")