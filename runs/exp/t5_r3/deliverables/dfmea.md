# Design FMEA (Qualitative) — VBF-T5R3-DFMEA-01

**Case**: t5_r3 · **Design**: Y4 (primary) · **Caveat**: qualitative version based on simulation risk signals only; severity/occurrence rated high/medium/low from the magnitude of the simulated value vs thresholds. Complete FMEA (process/supplier failures) is N/A (beyond pure simulation boundary).

| # | Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|---|
| 1 | Lithium plating on negative electrode during 4C fast charge | Salt-concentration transport limit at high rate (root-caused in round 2: baseline plated severely, min_ap −0.438 V) | `r6_y4_4c_dfn.json:anode_potential_v` min **+0.0200 V** — positive, but margin is the thinnest of the three criteria | High | Low (no plating point in simulated CC window; margin thin at cut-off) | Transport upgrade (σ 5.0 S/m, t⁺ 0.6, D_e 9e-10), 3 µm anode particles, mild warmth (h=26 W/m²K) engineered in; CV tail untested — physical validation recommended |
| 2 | Thermal overrun / temperature overshoot during fast charge | Heat generation at 4C exceeds cooling capacity | `T_max_K` **327.60 K vs 333.15 K** — 5.6 K margin | High | Low | Double-sided cooling 0.01062 m² + h tuning; margin relies on cooling-area assumption — validate in physical cell |
| 3 | Electrolyte oxidative decomposition | High cathode potential vs electrolyte HOMO | Not computed — true DFT endorsement skipped (`real_compute=false`, endorsed honestly) | Medium | Unknown (honest) | Baseline EC/LiPF6-class chemistry at standard 4.2 V window (NMC811); no claim made without first-principles signal |
| 4 | Insufficient capacity / energy shortfall | Coating/geometry inadequacy | 1C `capacity_ah` 5.0442 vs nominal 5.0; ED 535.72 vs 500.94 | Low | Low | DFN-verified; ED margin 7% |
| 5 | Manufacturing-induced performance drift | 5–6 µm metal foils handling; ±tolerance effect on warmth-dependent plating margin (~6.6 mV/K sensitivity measured in round 5) | No direct signal (thermal-kinetic coupling measured: rounds 4–5 h-series) | Medium | Medium | Y3 (Al 8 µm / sep 9 µm) provided as supply-friendly alternate; DVPR flags foil handling |
| 6 | CV-tail plating at high SOC | Current taper regime not simulated in 4C protocol | Indirect: anode potential at 4.2 V cut-off (+0.0200 V, worst point of CC window); risk monotonic with current (domain reasoning) | High | Low | Physical 4C + CV charge test with reference electrode listed in DVPR |

## Conclusion

Highest-risk items: plating margin at CC cut-off (#1) and the cooling-assumption dependence of the thermal margin (#2). Both are design-engineered (transport + thermal + kinetic margins at DFN precision) but the *margins* — not direction — remain simulation-grade; physical validation items are named in the DVPR. Full process/supplier FMEA: **N/A (beyond pure simulation boundary)**.