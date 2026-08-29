# Design FMEA (qualitative version, simulation-signal based) — t8_r3 (VBF-T8R3-DFMEA-01)

Qualitative ratings derived from simulation signal magnitudes vs thresholds; complete process/supplier FMEA is N/A (beyond pure simulation boundary).

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Negative electrode plating (fast charge) | low-T anode kinetics loss at high cooling | anode_potential_v min +17.7 mV at 4C/45 °C (V13) — margin over 0 V | high | low | negative porosity 0.30 + 2.5 µm graphite + h=60 design point; V7-type cooling-only designs rejected (−10 mV) |
| Thermal runaway risk (temperature rise) | excessive heat during charge abuse | T_max 326.53 K vs 333.15 K limit; run-tr triggered=false on overcharge coupling | high | low | forced-air h≥60 W/m²K pack cooling mandated in design |
| Electrolyte oxidative decomposition | voltage window excess | window 4.2 V top (parameter set); no final DFT endorsement run (real_compute=false) — signal NOT verified at molecular level | medium | low | voltage window kept at parameter-set limit; DFT endorsement would be the next verification step |
| Insufficient capacity / energy | active-loading below requirement at mass cap | ED 497.5 vs 446.18 Wh/kg (51 Wh/kg margin); retention 98.66% vs 90% | medium | low | V13 loading/porosity selection; V6/V11 show 500–536 Wh/kg headroom if needed |
| Thick-anode plating liability (documented negative result) | through-anode electrolyte polarization at 4C | V9/V11 (neg 100 µm) anode −26.5/−10.8 mV vs +7.3 mV at 85.2 µm | medium | low (avoided) | negative thickness kept at 85.2 µm — design rule recorded |


**Conclusion**: no high-risk items remain at the selected design point; the highest-severity modes (plating, thermal) both show positive margins (+17.7 mV, −6.6 K); complete FMEA including process/supplier failures: N/A (beyond pure simulation boundary).
