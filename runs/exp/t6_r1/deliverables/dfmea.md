# Design FMEA (qualitative) — VBF-T6R1-DFMEA-01

Qualitative version, based on simulation signals. Ratings: S = severity (high/medium/low), O = occurrence (high/medium/low); basis = magnitude of simulated value vs threshold. RPN = simplified S×O matrix (qualitative caliber).

| # | Failure mode | Failure cause | Simulation signal (detectability basis) | S | O | RPN (qual.) | Design-side mitigation |
|---|---|---|---|---|---|---|---|
| 1 | Lithium plating at fast charge | end-of-charge anode surface saturation + electrolyte depletion gradients | anode_potential_v min = +10.96 mV at DFN (margin 11.0 mV); SPMe over-predicted margin — fidelity-sensitive signal | high | medium | high-medium | D_e 6.0e-10 m²/s low-viscosity electrolyte (transport fix, +30.3 mV vs default at DFN); N/P geometry 102.2 µm; r_neg 3.5 µm. Charge-protocol headroom recommended |
| 2 | Thermal limit exceedance at 4C/45 °C | ~6 W DFN heat generation with passive cooling | T_max = 321.42 K vs 323.15 K (margin 1.73 K) | high | low | medium | h = 400 W/m²K active cooling is a design requirement (h=10 fails: 328.9 K, h=200 fails at DFN: 323.80 K) |
| 3 | SEI overgrowth | EC solvent reduction at anode; growth diffusion-limited in EC through SEI | sei_thickness_nm_end = 385.3 nm vs 500 nm (margin 114.7 nm) | medium | low | low-medium | EC-lean electrolyte (2270.5 mol/m³) + EC diffusivity 1.0e-18 m²/s (L ∝ sqrt(c₀·D_ec)); real additive package must reproduce effective values |
| 4 | Electrolyte oxidative decomposition at 4.7 V | high-voltage window vs electrolyte HOMO level | Not simulated — true DFT endorsement skipped (real_compute=false) | high | unknown | — | LNMO 4.7 V window; recommend HOMO/IE-EA first-principles endorsement of final electrolyte before production |
| 5 | Midpoint/plateau sag under load | through-plane electrolyte depletion at ~70% depth | midpoint 4.1145 V vs 4.1 V (margin 14.5 mV); default-D_e DFN measured 4.0974 V (fail) | medium | low | low | D_e transport lever; separator 12 µm retained |
| 6 | Capacity shortfall | anode-limited utilization | 6.198 Ah simulated vs 4.5 Ah parameter-set nominal (no shortfall) | low | low | low | none |
| 7 | Cathode Mn dissolution / high-voltage fade (LNMO-specific) | Mn³⁺ disproportionation at high voltage | Not simulated — beyond model boundary | medium | unknown | — | literature-known LNMO risk; surface coating recommendation (design note, not simulated) |

**Conclusion:** highest-risk items are #1 (plating — margin 11 mV at DFN, fidelity-sensitive) and #2 (thermal — margin 1.73 K, requires active cooling h=400). Both mitigations are implemented in the shipped design. Items #4/#7 are unquantified (true-compute/experiment boundary) and are flagged for production-line follow-up. Complete FMEA including process/supplier failures: N/A (beyond pure simulation boundary).
