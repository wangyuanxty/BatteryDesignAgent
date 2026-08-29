# Design FMEA (qualitative version, based on simulation signals)

> Qualitative S/O ratings are three-level (high/medium/low) based on simulation-signal magnitude vs threshold. Complete FMEA (process/supplier) is N/A (beyond pure-simulation boundary).

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Mitigation (implemented in design) |
|---|---|---|---|---|---|
| Negative electrode plating (fast charge) | 4C charge drives anode potential < 0 V (tight N/P + concentration polarization) | `anode_potential_v < 0` | High | Low | anode 108 µm (N/P 1.04), 1.5 µm anode particles, high-σ electrolyte → anode min +0.043 V (no plating) |
| Thermal runaway risk (temp rise exceeds limit) | 4C charge + 1C discharge reaction heat at 45 °C ambient | `T_max_K` vs 323.15 K | High | Low | active cooling h=400 W/m²·K → T_max 321.68 K |
| Insufficient capacity / energy density | thin electrodes / low active loading | 1C `capacity_ah` + `energy_density_wh_l` | Medium | Low | 6.372 Ah, 1260 Wh/L (≥ 950) |
| Voltage plateau too low | cathode OCV below 4.1 V | `midpoint_voltage_v` | Medium | Low | LNMO 4.7 V cathode → 4.131 V |
| Excessive SEI growth (cycle-life degradation) | 4.7 V cathode drives anode more negative, accelerating SEI | `sei_thickness_nm_end` | Medium | Low | artificial-SEI coating (SEI k 2e-15 m/s) → 193.6 nm (≤ 500 nm) |
| Positive electrode diffusion-limited fast charge | solid diffusivity 4e-15 m²/s (NMC value inherited) | 4C CC charge reaches ~27 % SOC | Medium | Medium | noted honestly; not resolvable within allowed levers (solid diffusivity excluded) |

## Conclusion

- Highest-risk items: thermal runaway risk and negative-electrode plating — both mitigated and verified (T_max 321.68 K, no plating).
- Remaining residual risk: positive-electrode diffusion limitation caps 4C CC charge depth (~27 % SOC); full FMEA (process/supplier) is **N/A (beyond pure-simulation boundary)**.
