"""t4_r3: propose entry round 5 — OKane2022 platform: thin pack + cooling + particle radii."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")

propose_r5 = {
    "action": "propose",
    "round": 5,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
            },
            "name": "V10_ok_thin",
            "role": "OKane2022 + thin pack (CC 16/12->8/6 um, sep 12->8 um): vol-ED 854.8->~930 Wh/L; dose the side effects (T_max, plating margin, retention)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40,
            },
            "name": "V11_ok_thin_h40",
            "role": "V10 + cooling h 10->40 W/m2/K (cold-plate grade): pull 4C@45C T_max 368.3->~331 K",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 60,
                "Negative particle radius [m]": 3.0e-6,
                "Positive particle radius [m]": 3.5e-6,
            },
            "name": "V12_ok_thin_h60_Rshrink",
            "role": "V11 + stronger cooling h=60 + particle shrink (neg 3.0/pos 3.5 um): recover plating margin lost to lower T via diffusion relief",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 40,
                "Negative particle radius [m]": 2.5e-6,
                "Positive particle radius [m]": 3.0e-6,
            },
            "name": "V13_ok_thin_h40_Rshrink",
            "role": "V11 + particle shrink (neg 2.5/pos 3.0 um): plating margin at moderate cooling",
        },
    ],
    "llm_reason": (
        "Round 4 verdict: OKane2022 (V9) is the platform — retention 95.57% under real Arrhenius cold "
        "physics, ED_kg 405.7 pass, plating pass (+0.0092 V razor-thin); gaps: vol-ED 854.8 (<880) and "
        "T_max 368.33 K (>>333.15). OKane2022 geometry dump shows the exact Chen2020 pack (200.8 um), so "
        "the thin-pack slimming transfers: 854.8 x 200.8/182.8 ~ 939 Wh/L. T_max: delta-T 50.2 K at h=10, "
        "A=0.00531 m2 -> h=40 projects T_max~330.7 K (cold-plate-grade thermal management is realistic "
        "for extreme-cold equipment with active BTMS). Known coupling: more cooling -> colder charge -> "
        "slower kinetics -> plating margin shrinks, so V12/V13 pair cooling with negative/positive "
        "particle shrink (dumped radii 5.86/5.22 -> 2.5-3.0/3.0-3.5 um; R^2 diffusion-time scaling). "
        "All values listed before running; sources: architecture/thermal design values (this proposal); "
        "particle-size scaling domain experience. All on OKane2022."
    ),
}
append_entry(ws, propose_r5)
print("propose r5 written")