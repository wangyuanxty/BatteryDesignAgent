# Battery Design Plan — t4_r1_luna

## Objective decomposition
- Cell-level gravimetric energy density: **>=327.18 Wh/kg**.
- Cell-level volumetric energy density: **>=880 Wh/L**.
- Low-temperature performance: **1C discharge capacity retention at -20 °C >=95%**, mechanically defined as lowT capacity divided by 25 °C 1C capacity.
- No safety threshold was supplied, so no 4C/thermal acceptance criterion is registered; safety screening remains a diagnostic where run.

## Starting point and boundary
No electrode system or material invention was specified. Per protocol, start at Stage 3 with baseline Chen2020. Unspecified freedoms take the widest interpretation: electrode system, electrolyte transport/formulation, electrode modification, architecture, and thermal management are adjustable. The first pass prioritizes architecture and transport parameters, while preserving the Chen2020 electrochemical model.

## Candidate strategy
1. Characterize Chen2020 baseline at 25 °C and -20 °C; compute contract-caliber gravimetric and volumetric energy density.
2. Explore a small set of architecture variants (thinner current collectors/separator, adjusted porosity, smaller particles) and a low-temperature transport variant. Each candidate is simulated independently and evaluated against the pre-registered thresholds.
3. If low-temperature retention remains the bottleneck after three informed variants, pivot toward electrolyte conductivity/diffusivity and transference-number adjustments; if energy density is the bottleneck, use mass/volume-efficient architecture while checking capacity.

## Budget and risks
Use proxy SPMe first, with DFN only for promising low-temperature candidates if needed. The principal risk is that the Chen2020 transport parameterization cannot sustain 95% retention at -20 °C; architecture changes may improve polarization but can trade energy density. Do not relax thresholds or redefine retention. A three-strike recurrence of the same failure triggers explicit model, boundary, and metric-assumption questioning before closing.

## Domain basis
- Lower separator/current-collector mass and optimized porosity generally improve practical energy density: domain experience (no precise source).
- Higher electrolyte transport and smaller particles reduce concentration/solid diffusion polarization at low temperature: domain experience (no precise source).
- Contract-caliber values will be taken only from bda simulation outputs and mechanically derived calc-energy outputs.
