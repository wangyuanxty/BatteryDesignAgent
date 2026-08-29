"""Round-3 entries: plan update (assumption overturned) + propose (final design)."""
import json
from pathlib import Path

CASE = Path("runs/exp/t2_r1_singlemodel")
LOG = CASE / "log.jsonl"

plan_update = {
    "action": "plan",
    "update": True,
    "reason": (
        "key assumption overturned by simulation: SPMe is unreliable for the "
        "thick-anode geometries needed for 4C plating control - at neg 250 um the "
        "SPMe electrolyte-concentration profile becomes unphysical during 1C "
        "(c_e +2990 -> -36 mol/m3 at the cathode, negative concentration) which "
        "zeroes the cathode exchange-current density and collapses the voltage; "
        "the SPMe 4C 'pass' (ap_min +0.15) was an artifact of the same pathology. "
        "DFN is adopted as the reliable mode for all design-relevant runs."
    ),
    "candidate_strategy": (
        "DFN 4C lever scan on the thick-anode base (neg 250 um / pos 100 um / "
        "radii 3.5/3.0 um): constant negative exchange-current density 2.0 A/m2 "
        "is the decisive fix - 4C charge-phase anode potential stays +0.24..+0.29 V "
        "(min +0.112 over the full cycle, in the discharge phase), 5.57 Ah charged "
        "at 4C. Non-monotonic sensitivity (i0=20 A/m2 fails at -0.26 V; i0=2 is the "
        "optimum), thickness alone insufficient at any tested value (150/200/225/"
        "250/300 um all plate without the kinetics fix). SEI500 fix: ec-reaction-"
        "limited growth (Yang2017) is diffusion-limited at L>100 nm "
        "(L*k_exp/D_ec >> 1, D_ec=2e-18), j_sei ~ F*c0*D_ec/L, so L ~ sqrt(D_ec): "
        "V1's k-only pack gave just -5.4% (measured 736 nm); the lever is EC "
        "diffusivity D_ec 2e-18 -> 1e-18 (film permeability of the additive-"
        "derived denser SEI; explicit film-property extension of the SEI-"
        "suppression bridge, honest estimate) - predicts ~550 nm at 500 cycles."
    ),
    "budget_allocation": (
        "R3: one combined final design in DFN across all protocols (1C, lowT, "
        "4C45, conservative 25C-start 4C, aging 100/500) + Stage 4 safety "
        "(overcharge + thermal-runaway screen on the final design)."
    ),
}

propose = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "name": "R3_finaldesign",
            "role": (
                "DFN-validated combined design: architecture neg 250 um / pos 100 um "
                "/ radii 3.5/3.0 um (4C reaction-zone crowding control via areal flux "
                "reduction), constant negative exchange-current density 2.0 A/m2 "
                "(interfacial kinetics bridge from LiDFOB/LiDFP additive pack; "
                "D-scan optimum), SEI pack k 1e-12->3e-13 + SEI i0 1.5e-7->7.5e-8 "
                "(FEC/PS/LiDFOB film), EC diffusivity 2e-18->1e-18 m2/s (denser "
                "additive-derived SEI, lower solvent permeation - diffusion-limited "
                "growth regime, film-property extension of the SEI-suppression "
                "bridge, recorded as estimate)"
            ),
            "struct": {
                "Negative electrode thickness [m]": 2.5e-4,
                "Positive electrode thickness [m]": 1.0e-4,
                "Positive particle radius [m]": 3.0e-6,
                "Negative particle radius [m]": 3.5e-6,
                "Negative electrode exchange-current density [A.m-2]": 2.0,
                "SEI kinetic rate constant [m.s-1]": 3e-13,
                "SEI reaction exchange current density [A.m-2]": 7.5e-8,
                "EC diffusivity [m2.s-1]": 1.0e-18,
            },
        }
    ],
    "llm_reason": (
        "R2 partial fixes evaluated: V1 SEI pack insufficient alone (SEI500 736>550, "
        "growth is D_ec-diffusion-limited not k-limited); V2 kinetics alone marginal "
        "(SPMe -0.419); V3 thick electrodes worsen SPMe 4C (-0.523). Diagnostics: "
        "SPMe c_e profile unphysical for thick anodes (negative concentration at the "
        "cathode -> i0_pos collapse -> voltage cliff); DFN adopted. DFN scan: "
        "anode thickness alone never passes (150 um -0.399, 200 um -0.355, 250 um "
        "-0.284, 300 um -0.238); the winning lever is constant neg i0 = 2.0 A/m2 on "
        "the 250 um base: full-cycle ap min +0.112 V, 4C charge-phase ap +0.244.."
        "+0.287 V, 5.57 Ah charged at 4C before the 4.2 V cut. Conservative 25C-start "
        "4C cross-check also passes (ap min +0.111 V). R3 measured: 1C 6.956 Ah, "
        "ED 358.0 Wh/kg (>327.18, +30.8 margin), lowT 6.927 Ah (retention 99.6% >90%). "
        "Aging 100/500 (DFN) with the full pack is the remaining criterion; SEI500 "
        "prediction ~550 nm from the D_ec scaling (baseline 778)."
    ),
}

with LOG.open("a", encoding="utf-8") as f:
    f.write(json.dumps(plan_update, ensure_ascii=False) + "\n")
    f.write(json.dumps(propose, ensure_ascii=False) + "\n")
print("appended plan-update + R3 propose")
