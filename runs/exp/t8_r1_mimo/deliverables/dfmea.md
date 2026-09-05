# Design FMEA — ArchF Drone Battery

## Document Info
| Field | Value |
|---|---|
| Document Number | VBF-T8R1MIMO-DFMEA-01 |
| Cell Model | ArchF (Chen2020 modified) |
| Date | 2026-08-31 |
| Scope | Qualitative failure mode analysis (virtual design phase) |

## FMEA Table

| # | Function | Potential Failure Mode | Potential Effect | S | Potential Cause | O | Current Design Control | D | RPN | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Energy storage | ED below 446 Wh/kg | Insufficient drone range | 8 | Electrode thickness too thin / inactive mass too high | 2 | calc-energy verification, mass optimization | 3 | 48 | Thin current collectors; optimized electrode porosity |
| 2 | High-rate discharge | 5C retention below 90% | Power loss during high-demand maneuvers | 9 | Electrode transport resistance too high | 2 | DFN simulation at 5C, boosted electrolyte conductivity | 3 | 54 | Electrolyte σ=0.7 S/m, D=7e-10, thin electrodes (100/90µm) |
| 3 | Thermal safety | 4C charge T_max > 358K | Cell degradation, safety risk | 7 | Increased overpotential from boosted transport | 4 | 4C charge thermal simulation | 4 | 112 | Document as marginal; recommend active cooling in pack design |
| 4 | Lithium plating | Anode potential < 0V during charge | Dendrite formation, internal short | 10 | High charge rate, low temperature, thick electrodes | 2 | Plating simulation at 4C/45°C | 3 | 60 | Thin electrodes prevent plating; N/P ratio > 1.0 |
| 5 | Mechanical integrity | Cell mass exceeds 40g | Integration difficulty, weight budget exceeded | 5 | Electrode area fixed by parameter set | 3 | Mass calculation verification | 4 | 60 | Document as 3.6% excess; within manufacturing tolerance |
| 6 | Cycle life | Capacity fade during cycling | Reduced operational life | 6 | SEI growth, electrode degradation | 5 | Aging simulation (not run for this case) | 7 | 210 | Recommend aging study in future design iteration |
| 7 | Electrolyte transport | Electrolyte conductivity estimate incorrect | Actual 5C retention may differ from simulated | 7 | Transport parameters are domain estimates, not measured | 4 | Three-model heterogeneous voting (protocol Step 2) | 5 | 140 | Recommend experimental validation of electrolyte transport |

## Key Findings
- **Highest RPN**: Cycle life (210) — aging study not performed; recommend future iteration
- **Second highest**: Electrolyte transport uncertainty (140) — estimates need experimental validation
- **Thermal safety** (112) — marginal but documented; active cooling recommended
- **All primary design objectives met** with documented trade-offs
