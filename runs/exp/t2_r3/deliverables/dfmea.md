# Design FMEA (qualitative, simulation-signal based) — combo-v5-final (VBF Case t2_r3)

> Qualitative calibre: severity/occurrence = high/medium/low based on magnitude of the simulation value vs threshold; RPN = simplified S×O matrix (qualitative). No numbers from memory.

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Mitigation (design-side, implemented / recommended) |
|---|---|---|---|---|---|
| Negative electrode plating during 4C fast charge | anode potential dips below 0 V vs Li/Li⁺ (transport- or kinetics-limited surface) | anode potential min +0.0443 V (DFN) / +0.0403 V (SPMe) — PASS but only ~40–44 mV margin | high | medium (thin margin) | implemented: fine negative particles (2.0 µm), neg. porosity 0.40, σ/D/t⁺ overrides. Recommend: retain/expand margin in pilot electrode design (physical validation of the transport assumptions) |
| Thermal excursion during fast charge | 4C at 45 °C ambient, ohmic+entropic heating | T_max 347.70 K = 74.5 °C, ΔT +29.5 K; no contract threshold exists | medium | medium | recorded, not asserted; recommend thermal-management sizing study + physical measurement before deployment |
| Electrolyte oxidative decomposition at high voltage | EC-based electrolyte vs 4.2 V window | NOT quantified — true-compute (HOMO/LUMO vs window) endorsement skipped (real_compute=false, recorded in endorse entry) | high | medium (unquantified) | mitigation: adhere to 2.5–4.2 V window; recommend DFT HOMO check + linear-sweep validation before pilot |
| Insufficient discharge capacity | geometry/material underperformance | 1C capacity 5.0648 Ah vs 5.0 Ah nominal; ED 447.1 Wh/kg vs 327.18 | low | low | none needed (margins ample) |
| Excessive anode SEI growth (contract failure mode) | solvent reduction on graphite | SEI 276.2 nm @100 cyc (≤500), 393.0 nm @500 cyc (≤550) — margin 157 nm | medium | low | implemented: SEI k ×0.2 + partial molar volume ×0.5 (denser film bridge, rounds 5–6) |
| Aging capacity fade (flagged observation) | unresolved: aging-protocol charge/discharge capacity declines steeply (0.331→0.012 Ah over 500 cyc) | capacity trajectory in `r6_combo-v5-final_aging500_spme.json`; NOT a contract metric; mechanism not resolved this session | medium | medium | recommend physical aging validation; do not quote trajectory as cycle-life data |

## Conclusion

Highest-risk items: (1) plating margin thinness (+0.044 V at DFN) despite pass — keep transport overrides or re-verify; (2) electrolyte oxidative stability unquantified (DFT skipped) — recommend true-compute endorsement before pilot; (3) aging capacity-trajectory artifact unresolved. Design-side mitigations for the contract failure modes (plating, SEI) are implemented in the parameter set. Complete FMEA incl. process/supplier failures: N/A (beyond pure simulation boundary).
