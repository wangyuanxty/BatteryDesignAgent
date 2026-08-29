"""Append round-3 propose entry (SEI-suppressing anode coating candidates)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")
entry = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "name": "ALD-coat-A",
            "role": "FastCharge-B geometry + anode ALD-Al2O3-type coating, SEI kinetic rate constant x0.01 (1e-14 m/s)",
            "struct": {
                "Negative particle radius [m]": 2.93e-06,
                "Electrolyte conductivity [S.m-1]": 2.5,
                "Electrolyte diffusivity [m2.s-1]": 1.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode porosity": 0.35,
                "Positive electrode porosity": 0.40,
                "SEI kinetic rate constant [m.s-1]": 1e-14,
            },
        },
        {
            "name": "ALD-coat-B",
            "role": "FastCharge-B geometry + ALD coating + LiF-rich inner SEI (fluorinated additive), k_sei x0.0001 (1e-16 m/s)",
            "struct": {
                "Negative particle radius [m]": 2.93e-06,
                "Electrolyte conductivity [S.m-1]": 2.5,
                "Electrolyte diffusivity [m2.s-1]": 1.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode porosity": 0.35,
                "Positive electrode porosity": 0.40,
                "SEI kinetic rate constant [m.s-1]": 1e-16,
            },
        },
        {
            "name": "ALD-coat-C",
            "role": "FastCharge-B geometry + thicker ALD coating + LiF-rich inner SEI, k_sei x0.00001 (1e-17 m/s)",
            "struct": {
                "Negative particle radius [m]": 2.93e-06,
                "Electrolyte conductivity [S.m-1]": 2.5,
                "Electrolyte diffusivity [m2.s-1]": 1.5e-09,
                "Cation transference number": 0.35,
                "Negative electrode porosity": 0.35,
                "Positive electrode porosity": 0.40,
                "SEI kinetic rate constant [m.s-1]": 1e-17,
            },
        },
    ],
    "llm_reason": (
        "R2 gap after plating fixed: sei_500cyc 826 nm (FastCharge-B) > 550. Cause = SEI growth kinetics -> "
        "electrode-modification (coating) lever, Stage 2 candidate class; inorganic ionic solid (ALD Al2O3-type) -> "
        "molecular funnel skipped per protocol, screened directly by Stage 3 aging. Parameters listed before running: "
        "SEI kinetic rate constant [m.s-1] 1e-14 / 1e-16 / 1e-17 (ESTIMATES spanning the plausible suppression range: "
        "protocol measured reference k x0.1 -> 449->385 nm @100cyc; log-growth extrapolation on V2 geometry suggests "
        "x1e-4..x1e-5 needed for <=550 nm @500cyc; magnitude beyond bare ALD literature (Jung 2010 Adv Mater 22:2172, "
        "3-7x retention improvement) justified by combined ALD + fluorinated-additive LiF-rich inner SEI — marked "
        "aggressive estimate). All other parameters = FastCharge-B (identical 1C/4C/lowT results by construction; "
        "k_sei does not enter those protocols). Measurement adjudicates."
    ),
}
append_entry(ws, entry)
print("propose R3 appended")
