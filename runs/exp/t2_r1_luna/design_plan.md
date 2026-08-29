# Battery Design Plan

## Objective decomposition
- Cell-level energy density: ≥327.18 Wh/kg.
- 4C fast charge: no lithium plating (negative-electrode potential must remain ≥0 V).
- Durability: anode SEI thickness ≤500 nm after 100 cycles and ≤550 nm after 500 cycles at 1C.
- Low-temperature performance: discharge capacity retention at −20 °C ≥90% of the 25 °C reference.
- No explicit electrode/material system is supplied; use the deterministic Chen2020 baseline and treat architecture, transport formulation, electrode modification, and thermal management as adjustable within the widest task interpretation.

## Candidate strategy
Start at cell design (pipeline Stage 3), because the task does not name a new material. Characterize the Chen2020 baseline, then test architecture/transport variants targeting fast-charge plating, low-temperature transport, mass-specific energy, and SEI growth. Use the same parameter set for aging comparisons. If the baseline cannot approach the energy-density ceiling, escalate to material/system design rather than silently relaxing the target.

## Budget and evaluation
Run a baseline plus 2–4 architecture/formulation variants per round. For each candidate run 1C discharge, low-temperature discharge, 4C charge at 45 °C with lumped thermal/plating, and 100-/500-cycle aging. Compute energy density mechanically from the discharge output. Evaluate every candidate through `bda log-evaluate`; retain failures and route them to the scale of the diagnosed cause.

## Risks and fallback
Likely risks are Chen2020's mass/geometry ceiling, low-temperature electrolyte transport, and SEI growth under long cycling. Architecture failures trigger Stage 3 parameter changes (thinner layers, smaller particles, transport overrides, cooling). SEI-specific failures trigger same-system SEI/coating parameter changes; a material ceiling triggers Stage 2 escalation. Three repeated failures of the same cause trigger explicit system, boundary, and metric questioning before closure.

## Domain basis
- Higher electrolyte conductivity and cation transference reduce concentration polarization and plating risk (domain experience; no precise source asserted).
- Smaller active-particle radius shortens diffusion paths and improves high-rate/low-temperature kinetics (domain experience; no precise source asserted).
- Lower SEI kinetic rate is a direct proxy for film-forming/coating suppression in the simulator's aging model (protocol-calibrated model lever).
