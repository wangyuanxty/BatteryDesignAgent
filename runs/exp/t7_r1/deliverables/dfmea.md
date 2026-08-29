# Design FMEA (Qualitative, Simulation-Signal Based) — Case t7_r1

Document: VBF-T7R1-DFMEA-01 · Prepared 2026-08-25 · Signature: Prepared ______ / Reviewed ______ / Approved ______

Qualitative version based on simulation signals (S/O three-level: High/Medium/Low; magnitude = deviation of simulated value from threshold). Complete FMEA including process/supplier failures: N/A (beyond pure-simulation boundary).

| # | Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design mitigation |
|---|---|---|---|---|---|---|
| 1 | Lithium plating on negative electrode during 4C fast charge | Transport/solid-diffusion polarization at high rate (large graphite particles, low porosity, low electrolyte transport) | anode_potential_v min: baseline −0.1918 V (plates) → design +0.0476 V; isolation data: porosity dominant lever (−0.134 → −0.0419 V), h=200 worsened (−0.131 V) | High (Li metal → short-circuit/TR hazard) | Low (margin +0.048 V at 4C/45 °C with 1.5 µm graphite, porosity 0.36, σ 2.5 S/m, t⁺ 0.55) | Keep porosity ≥ 0.36 and particle radius ≤ 1.5 µm; electrolyte transport overrides as specced; do not fast-charge below 0 °C (not simulated); re-verify after any material change |
| 2 | Thermal runaway from nail penetration | Internal short with 10 W heat source exceeding local heat rejection | run-tr triggered flag: baseline triggered 322.2 s (contract h=10) → design not triggered, T_max 336.32 K; sensitivity: h=30 triggers at 666 s, h=40 passes 348.69 K | High | Low (design h = 50 W/(m²·K), 25 % above the 40 floor) | Cooling spec h ≥ 40 W/(m²·K) on 0.00531 m² surface as a hard floor; monitor thermal-interface degradation in pack integration |
| 3 | Cell overheating during 4C fast charge | Ohmic + polarization heating at 45 °C ambient | T_max_K = 330.13 K (56.98 °C) at 45 °C ambient (h = 50) | Medium | Low | No T_max threshold adjudicated in task; 330 K is far below SEI runaway-onset regimes; keep h = 50 |
| 4 | Electrolyte oxidative decomposition at high voltage | HOMO level of solvent vs cathode potential window (4.2 V upper cut-off) | No molecular data (Stage 2 not entered; start_stage = 3; real_compute = false) | Medium | Not assessed (honest gap — no proxy/DFT run) | Upper cut-off kept at parameter-set 4.2 V; first-principles endorsement skipped per real_compute=false — flagged for future work |
| 5 | Insufficient capacity / energy density | Cathode loading or utilization below requirement | ED 483.25 Wh/kg vs 327.18 threshold (48 % margin); capacity 6.032 Ah; ceiling probe showed ED non-binding | Low | Low | Margin documented in DVPR item 2 |
| 6 | Excessive SEI growth at 45 °C | High-temperature side reactions (ec reaction limited) | sei_thickness_nm_end 465.47 nm vs 550 nm (15 % margin) | Medium | Low | SEI kinetic rate at set value 1e-12 m/s; margin monitored; per-cycle capacity artifact labeled (not interpreted as real capacity) |
| 7 | Cooling degradation below design floor | Aging/damage of thermal interface lowering h | Sensitivity sweep: h=30 → TR at 666 s; h=25 → TR at 518.4 s | High | Medium (interface aging plausible in pack) | Design h = 50 with floor 40 (25 % margin); DVPR 6a is the evidence basis; pack-level verification required |

## Conclusion

Highest-risk items: #1 plating (mitigated: +0.048 V margin) and #2/#7 nail-TR/cooling degradation (mitigated: h = 50 vs floor ≈ 40). All mitigations are implemented in the current design (V11-final) and backed by simulation evidence; items #4 (molecular stability) remains an honest unassessed gap due to real_compute = false.
