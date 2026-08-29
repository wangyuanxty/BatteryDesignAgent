# Battery Design Plan — t7_r1_luna

## Objective decomposition
- Cell gravimetric energy density: at least 327.18 Wh/kg.
- 4C charging at 45 °C: no lithium plating (minimum anode surface potential must remain non-negative).
- High-temperature durability: SEI thickness no greater than 550 nm after 100 cycles at 45 °C.
- Nail-penetration abuse: 10 W short-circuit heat source must not trigger thermal runaway.

## Starting point and candidate strategy
The task does not name a new material or electrode chemistry, so execution starts at cell-scale architecture (Stage 3) using the deterministic default Chen2020 parameter set. The initial round characterizes the baseline, then tests 2–4 architecture variants spanning thinner active layers, improved transport/porosity, smaller particles, and stronger cooling. If the opening ceiling or repeated failure indicates a material/transport bottleneck, escalate to Stage 2 candidates rather than continuing blind architecture tuning.

## Budget and risk plan
Use fast SPMe for initial screening, DFN for rate-sensitive confirmation, and run the required 45 °C aging and abuse protocols. Energy density and plating are expected to trade off against electrode thickness and thermal rise. A failed metric is routed to its causal scale: capacity/temperature to architecture and plating/transport limitation to material/electrolyte design. Three consecutive failures from the same cause trigger assumption questioning before any further trial.

## Domain basis
- Smaller particles and higher electrolyte transport generally reduce concentration polarization and plating risk: domain electrochemical experience (no precise source supplied).
- Thinner current collectors/separators and higher active-material fraction generally improve gravimetric energy density but can worsen thermal management: domain electrochemical experience (no precise source supplied).
- SEI growth is sensitive to temperature and kinetic rate; high-temperature aging must be measured on the same parameter set: protocol-defined model behavior.
- Nail safety is assessed mechanically with the coupled thermal runaway ODE, not inferred from nominal chemistry: protocol-defined verification.
