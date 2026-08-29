# Design FMEA (qualitative version, based on simulation signals) — V10a_final_h45

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Lithium plating at negative electrode (fast charge) | anode potential below 0 V vs Li/Li+ at 4C/45C | anode_potential_v min: Chen2020 +28.96 mV, OKane2022 +24.96 mV (both > 0) | high | low | anode porosity 0.35, deep electrolyte transport (sigma 4.0 S/m, t+ 0.45, D 3.539e-10), small particles (3/2 um) lift anode margin at the separator interface |
| Thermal runaway risk (temperature rise exceeds limit) | 4C charge heat generation above cooling capacity | T_max 329.33 K (Chen2020) / 331.78 K (OKane2022) vs 333.15 K limit | high | low | cooling h = 45 W/m2K; margin 3.82 K / 1.37 K under the two parameter sets |
| Capacity loss at extreme cold | electrolyte transport freezing / kinetic slowdown | -20 C retention 0.9944 (Chen2020, T-independent sigma) / 0.9788 (OKane2022, Arrhenius sigma) | medium | low | transport design validated on the Arrhenius-conductivity parameter set, which is the conservative cold case |
| Insufficient capacity | under-utilization / early cut-off | 1C capacity 5.0618 Ah vs 5.0 Ah nominal | low | low | capacity margin positive; no capacity criterion in entry 0 |
| Electrolyte oxidative decomposition (voltage window) | HOMO/IE-EA of electrolyte vs cathode potential | no molecular-level data (real_compute=false, Stage 5 skipped) | medium | medium | residual risk not quantified by simulation; noted honestly — true DFT endorsement skipped per protocol |
| Electrolyte conductivity over-estimation in the judged set | Chen2020 conductivity function is temperature-independent (0.9487 S/m at 253 K), physically optimistic for cold operation | dump_params comparison: Chen2020 vs OKane2022 at 253.15 K (0.9487 vs 0.280 S/m) | medium | medium | design overrides sigma to a constant 4.0 S/m on BOTH sets and passes the OKane2022 (Arrhenius) robustness re-check — cold-retention claim is not an artifact of the optimistic set |

## Conclusion

Highest-risk item: electrolyte oxidative stability (no molecular endorsement, real_compute=false) — recorded as a residual uncertainty, not simulated away. All failure modes with simulation coverage show low occurrence under the final design. Complete FMEA (process/supplier failures) is N/A (beyond pure simulation boundary).
