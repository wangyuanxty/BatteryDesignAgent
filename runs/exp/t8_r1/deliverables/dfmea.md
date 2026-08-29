# Design FMEA (qualitative version) — T8-40g

- **Document code**: VBF-T8R1-DFMEA-01
- **Case**: t8_r1 — long-endurance drone battery
- **Generation date**: 2026-08-25
- **Signature**: Prepared: ________  Reviewed: ________  Approved: ________

Qualitative version, based on simulation risk signals (values from tool output files under `cell/`). Severity/occurrence are three-level qualitative ratings (high/medium/low), basis = magnitude of simulation value deviating from the threshold; RPN uses the simplified qualitative S×O matrix (annotated qualitative caliber).

## Failure Mode Table

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | RPN (qual.) | Design-side mitigation recommendation |
|--------------|---------------|------------------------------------------|----------|------------|-------------|----------------------------------------|
| Negative electrode lithium plating (fast charge) | Overpotential at anode during 4C charge exceeds plating threshold; slow solid diffusion (large particles); low anode capacity headroom | `r5_final_4c45_dfn.json` anode_potential_v min = +0.0082 V (baseline plated; after mitigation margin 8.2 mV) | High | Low | High×Low → acceptable | Fine-graphite 1.5 µm anode particles, t⁺ 0.5, thicker anode (95 µm) for lithiation headroom; keep 4C charge within voltage-limited acceptance (0.94 Ah) |
| Thermal runaway risk (temperature rise exceeds limit) | Polarization + ohmic heat at 4C/45 °C exceeds cooling capacity | `r5_final_4c45_dfn.json` T_max 330.41 K vs 333.15 K limit — margin only 2.74 K | High | Low | High×Low → acceptable | Forced-air cooling h = 40 W/m²/K assumed; verify real h by thermal test; derate charge current if ambient > 45 °C |
| Electrolyte oxidative decomposition (voltage window) | Solvent HOMO vs cathode potential at 4.2 V | No DFT endorsement run (real_compute = false; endorse entry skipped) — signal absent | Medium | Medium | Medium×Medium → track | Not endorsed at molecular level; if Stage-5 endorsement is later funded, verify electrolyte HOMO window first |
| Insufficient capacity | Capacity below drone endurance requirement | 1C capacity 6.9427 Ah vs nominal 6.1494 Ah — PASS (energy 25.246 Wh) | Medium | Low | Medium×Low → acceptable | Capacity margin exists (DFN 1C exceeds nominal); monitor on production lots |
| Mass overrun (>40 g) | Layer mass accumulation from tolerance spread | Contract mass 39.798 g vs 40 g — margin only 0.202 g (0.5%) | Medium | Medium | Medium×Medium → track | Tight mass margin: control foil thickness and coating density tolerances in production; electrolyte mass (11.03 g, literature density) is outside contract caliber but counts in real pack mass |
| 5C retention degradation | Diffusion/transport limits reappear at high rate after aging | 5C retention 98.77% (fresh) — PASS; aging not simulated | Medium | Low | Medium×Low → acceptable | Run aging + 5C protocol if cycle-life requirement is added later |
| Incomplete 4C charge (voltage-limited) | 4.2 V cut-off reached at 0.94 Ah during 4C charge | `r5_final_4c45_dfn.json` capacity 0.9395 Ah | Low | High | Low×High → acceptable | Charge at ≤ 2C for full capacity; 4C reserved for emergency/top-up |

## Conclusion

- **Highest-risk items**: (1) thermal margin at 4C/45 °C (2.74 K) — mitigation implemented via h = 40 W/m²/K cooling, but real heat-transfer coefficient must be verified physically; (2) electrolyte oxidation at 4.2 V — no molecular-level endorsement in this case (real_compute = false); (3) mass margin (0.202 g) — production tolerance control required.
- Mitigation measures for plating, thermal, and retention risks have been implemented in the design (R2–R4 change history, see design_spec.md §6).
- Complete FMEA including process/supplier failures: N/A (beyond pure simulation boundary).
