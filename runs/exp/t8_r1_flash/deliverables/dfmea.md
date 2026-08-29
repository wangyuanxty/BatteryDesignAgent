# Design FMEA (qualitative) — VBF-T8R1FLASH-DFMEA-01

**Qualitative version based on simulation risk signals** (not a full process/supplier FMEA). | **Date**: 2026-08-25

| Failure mode | Cause | Simulation signal | S | O | Design-side mitigation (implemented) |
|---|---|---|---|---|---|
| Negative electrode lithium plating (fast charge) | anode polarization at 4C, limited negative headroom | min anode potential 0.0247 V (>0 → no plating signal; V1/V2 showed negative/edge signals) | High | Low | nano particles, high-transport electrolyte (t⁺=0.50 est.), thinner electrodes, separator porosity 0.55 |
| Thermal runaway risk (temperature rise beyond limit) | 4C charge heat generation vs h=10 cooling | 4C T_max 331.98 K vs 333.15 (margin 1.2 K; V3/V5 exceeded) | High | Low | transport upgrade + larger pouch cooling area 0.0075 m² (V5 control shows +2.8 K without it) |
| Electrolyte oxidative decomposition | voltage window vs HOMO/IE-EA | Not computed (no molecular funnel; real_compute=false) | Medium | Medium | upper cutoff 4.2 V conservative; LNMO 4.7 V system rejected (lower ED path) |
| Insufficient capacity / energy | loading too low, rate losses | 1C 3.45 Ah, ED 473.0 Wh/kg vs targets | Medium | Low | thickness/Pareto scan V1–V5; final balances ED vs 5C vs T_max |
| Overcharge thermal runaway | charge beyond 4.2 V | 0.5C to 4.7 V: T_max 300.57 K, triggered=false | High | Low | BMS cutoff required (beyond cell design) |

**Conclusion**: Highest-risk item = 4C fast-charge thermal (margin 1.2 K); mitigation implemented via transport + cooling-area levers; plating risk mitigated. Complete FMEA including process/supplier failures: N/A (beyond pure-simulation boundary).
