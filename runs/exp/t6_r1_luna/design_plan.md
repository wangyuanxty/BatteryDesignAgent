# Battery Design Plan

## Objective decomposition
Design a smartphone cell with volumetric energy density ≥950 Wh/L, 4C charge without lithium plating, maximum temperature ≤50 °C (323.15 K), 100-cycle SEI thickness ≤500 nm, and voltage plateau ≥4.1 V. Volumetric energy density and voltage plateau are primary coupled objectives; higher electrode loading can raise energy per volume but increases polarization and fast-charge heating. Safety and SEI are hard constraints.

## Starting point and candidate strategy
No electrode system or material/additive was specified, so the deterministic baseline is Chen2020 (default teaching parameterization) and execution starts at Stage 3 using baseline material properties. First characterize baseline 1C discharge, calculate contract energy density, run 100-cycle aging, and run coupled 4C/45 °C plating safety. Then test architecture variants (thinner separator/current collectors and reduced particle radii) while retaining the same baseline system. Because the requested 4.1 V plateau and 950 Wh/L are unusually demanding for the unspecified Chen2020 baseline, any failure is attributed first to system/material ceiling rather than silently relaxing thresholds.

## Budget and fallback
Use a baseline plus two architecture variants in the first round. If energy density or plateau fails, the cause is material/system-level and the plan would escalate to a high-voltage system candidate in a subsequent round; if temperature or plating fails while cell metrics pass, route back to architecture/transport tuning. If the same cause fails three consecutive rounds, stop blind tuning and document model, boundary, and metric assumptions.

## Risks and references
- High-voltage plateau direction → LNMO high-voltage cathode parameterization documented in the Virtual Battery Factory anchor table (domain protocol reference).
- Fast-charge plating risk → smaller particles and improved electrolyte transport are expected to reduce concentration polarization (domain experience; no precise source).
- SEI growth → lower SEI kinetic rate/coating is a recognized mitigation direction (domain experience; no precise source).

True DFT/MD endorsement is disabled by default (`real_compute=false`); no conclusion-grade first-principles values will be fabricated.
