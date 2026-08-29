"""Write Round 5 propose entry + params file."""
import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t7_r1_noforce", "D:/research/degradation_prognostics/Battery_Design_Agent/runs")
struct = {
    "Positive current collector thickness [m]": 1.0e-05,
    "Negative current collector thickness [m]": 6.0e-06,
    "Separator thickness [m]": 1.0e-05,
    "Electrolyte conductivity [S.m-1]": 2.5,
    "Electrolyte diffusivity [m2.s-1]": 5.0e-10,
    "Cation transference number": 0.5,
    "Total heat transfer coefficient [W.m-2.K-1]": 100.0,
    "Negative particle radius [m]": 4.0e-06,
    "Negative electrode thickness [m]": 8.52e-05,
    "SEI kinetic rate constant [m.s-1]": 7.5e-13,
}
propose = {
    "action": "propose",
    "round": 5,
    "candidates": [
        {
            "struct": struct,
            "name": "h100 + r4.0 Anode + Coating, neg 85.2um",
            "role": "revert negative thickness to 85.2 um (SEI driver -7.4 nm/um empirical) while keeping r=4.0 um (plating-margin driver ~-17 mV/um) and the Al2O3 coating (k x0.75)",
        }
    ],
    "llm_reason": (
        "R4 diagnosis from PyBaMM Yang2017 ec-reaction-limited source + R2/R3/R4 empirical decomposition: "
        "(1) at 45C the SEI is solvent-diffusion-limited (L*k/D_ec ~1e9 >> 1 at 500 nm), so k-coating effect is "
        "~-18 nm only; (2) negative thickness drives SEI +~7 nm/um (R2->R3: +50 nm from +6.8 um; R3->R4: +22 nm "
        "from +3 um, each offset by coating -18 nm) - so thinner negative is the strongest sanctioned SEI lever; "
        "(3) particle radius is ~SEI-neutral (surface-area effect offset by lower 1C polarization -> higher anode "
        "potential in aging) but dominates 4C plating margin (~-17 mV/um; R2->R3 +20.6 mV split: +32 mV radius, "
        "-3 mV thickness). => revert negative to 85.2 um + keep r=4.0 um + coating: expected SEI ~480 nm "
        "(margin ~70 nm) and anode ~+24 mV (margin), ED up (lighter cell). Empirical model uncertain - full "
        "five-sim verification. Nail coupling: hA=0.531 W/K, t_init = candidate 4C T_max_K, mass = candidate mass."
    ),
}
append_entry(ws, propose)
(ws.path / "cell" / "params_r5_slim.json").write_text(json.dumps(struct, indent=2), encoding="utf-8")
print("propose R5 appended; params_r5_slim.json written")
