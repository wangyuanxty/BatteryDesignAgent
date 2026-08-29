# Design FMEA — Qualitative Version (VBF-T5R1SINGLEMODEL-DFMEA-001)

> Case: t5_r1_singlemodel. Qualitative version, based on simulation signals; severity/occurrence are three-level ratings (high/medium/low) anchored to the magnitude of the simulated value vs threshold. RPN = simplified S×O qualitative matrix. Complete FMEA (process/supplier failures) is N/A beyond the pure-simulation boundary.

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Negative electrode lithium plating (4C fast charge) | anode potential < 0 V during high-rate charge | `anode_potential_v` min = +0.0215 V at 4C/45 °C — margin +21.5 mV (measured) | high (if occurred) | low | transport bridge σ 3.5 S·m⁻¹ / D 1.2×10⁻⁹ m²·s⁻¹ / t⁺ 0.55; 2.2 µm negative particles; h = 45 (avoid overcooling — measured h>45 pushes anode below 0 V, R3) |
| Thermal runaway risk (temperature over limit) | insufficient cooling / high-rate heat generation | T_max 330.50 K vs 333.15 K — margin 2.65 K (thinnest margin of the three criteria) | high (if occurred) | low | h = 45 W·m⁻²·K⁻¹ + thin layer stack (184.8 µm); margin thinner than plating margin — first thing to re-verify under tolerance spread |
| Electrolyte oxidative decomposition at high voltage | electrolyte HOMO vs cathode upper cut-off 4.2 V | **not verified in this case** — funnel_voting OFF ablation removed the xTB HOMO line; true-compute endorsement skipped (real_compute = false) | medium | medium | qualitative additive recommendation VC/FEC (mace-passed film formers); honest gap: HOMO line unmeasured — listed as top residual risk |
| Insufficient capacity / energy density | mass overshoot or porosity-slack assumption break | ED 533.18 Wh/kg vs 500.94 — margin +32.2; capacity is negative-limited (N/P ≈ 1.00 equilibrium caliber) | high (if occurred) | low | mass cuts (CC 8/6 µm, sep 10 µm) + positive porosity 0.40 on measured slack (R1: no capacity loss); production must re-optimize binder/additive split (not parameterized in base set) |
| Cell mass under-count | electrolyte excluded from contract mass caliber | contract mass 34.46 g vs 41.08 g with electrolyte (literature density) | low | — | disclosed in spec/datasheet; BOM carries both calibers |
| Anode oversize absent (N/P ≈ 1.00) | mass-first design removed conventional N/P > 1 headroom | negative electrode binds capacity (R2: −8% neg thickness → −7.9% capacity) | medium | low | plating suppression moved from oversize to kinetics (bridge + particles); margin +21.5 mV measured — re-verify under low-temperature/aging |

## Conclusion

Highest-risk items: (1) electrolyte oxidative stability unverified (no HOMO data under the funnel_voting OFF ablation; true-compute skipped) — recommend xTB HOMO screening + true-compute endorsement as follow-up; (2) N/P ≈ 1.00 negative-limited design — plating robustness relies on the kinetic bridge, validated only at the simulated fresh-cell condition. All mitigations listed above are implemented in the final design (archN_robust) or disclosed as limitations. Complete FMEA incl. process/supplier failures: N/A (beyond pure-simulation boundary).
