# Design FMEA (qualitative version) — VBF-T1R2-DFMEA-01

Qualitative version, based on simulation signals only (annotated per protocol). Ratings: S (severity) and O (occurrence) ∈ {High, Medium, Low}; basis = magnitude of the simulation value vs threshold. Simplified qualitative S×O matrix.

| # | Failure mode | Failure cause | Simulation signal (detectability basis) | S | O | Design-side mitigation (implemented in V4b) |
|---|---|---|---|---|---|---|
| 1 | Lithium plating on negative electrode during fast charge | Local anode polarization at high current (kinetic + transport limitation), low temperature | `cell/r4_v4b_4c_dfn.json:anode_potential_v` min +0.0215 V (margin thin — 21.5 mV above 0 V at 4C) | High | Low | N/P ≈ 1.35 (neg 96 µm); negative particle 1.5 µm (surface ×1.33); electrolyte bridge σ 1.8 S/m, D 6e-10, t⁺ 0.4 (`estimate`); negative porosity 0.32; cooling h = 60 keeps kinetics warm. Recommend: avoid 4C below 25 °C; anode-reference-electrode monitoring in production |
| 2 | Cell temperature exceeding 60 °C limit during fast charge | High-rate heat generation vs cooling capacity | 4C T_max 326.46 K vs limit 333.15 K (margin 6.69 K) | High | Low | h = 60 W/m²·K cold-plate-class cooling; thin collectors (8/6 µm) and separator (9 µm) shorten heat path; hA design-consistent in thermal-runaway coupling (0.3186 W/K) |
| 3 | Electrolyte oxidative decomposition under 4.7 V overcharge | 4.7 V exceeds EC/EMC solvent stability window | Overcharge sim T_max 299.43 K, run-tr triggered = false (proxy caliber, lumped model); molecular HOMO / IE−EA vs 4.7 V **not computed** (`real_compute: false`, endorse skipped honestly) | Medium | Medium | Charge cut-off redundancy in BMS; follow-up true-DFT endorsement of electrolyte against 4.7 V recommended before production; additive screening (Stage 2 funnel) as next design round |
| 4 | Incomplete fast charge (voltage-limited CC stop) | Polarization at 4C reaches 4.2 V before full SOC | CC acceptance 4.53 Ah = 79% of 1C capacity | Low | High | Documented as performance characteristic; CV step / higher-t⁺ electrolyte / thinner electrodes as future levers (logged in evaluate R4) |
| 5 | Capacity shortfall | Under-loading / impedance growth | 1C capacity 5.6997 Ah ≥ nominal 5.0 Ah | Medium | Low | Fine particles (2.0/1.5 µm) for kinetics; porosity headroom (0.36/0.32) for transport |
| 6 | SEI growth / cycle aging | Calendar + cycling SEI accumulation | Not simulated in this case (aging protocol available; set is aging-capable, SEI kinetic rate constant 1e-12 m/s) | Low | Medium | Follow-up aging run recommended; SEI-suppressing coating is an available Stage 2 lever |

## Conclusion

Highest-risk items: (1) plating margin is thin (+21.5 mV) — mitigated by design but the dominant residual risk under cold/aged conditions; (2) 4.7 V oxidative stability unverified at molecular level — flagged for true-DFT endorsement. Mitigations above are already implemented in the nominated design. Complete FMEA (process/supplier failure modes) is N/A (beyond pure simulation boundary).
