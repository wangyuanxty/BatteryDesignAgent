# Battery Design Plan — t3_r1_luna

## Objective decomposition
- Nominal capacity: >=2 Ah (cell-level capacity).
- 5C discharge retention: >=95%, evaluated as 5C capacity divided by same-parameter 1C capacity.
- 4C fast charge: no lithium plating, mechanically determined from minimum anode surface potential >=0 V.
- Maximum temperature: <=60 °C = 333.15 K, evaluated with coupled lumped thermal model.
- Power density: >=4000 W/kg from the contract `calc-energy` calculation.

The rate and thermal constraints are expected to trade off: thinner electrodes, smaller particles, higher electrolyte transport, and stronger cooling improve rate/heat performance but can reduce areal capacity. Capacity is the hard feasibility constraint alongside power density.

## Candidate strategy
Start at cell scale using the deterministic default Chen2020 parameter set because no electrode system was specified. Establish a baseline, then explore architecture variants (reduced electrode thickness, smaller particles, adjusted porosity/current collectors) and a high-transport electrolyte formulation. Each candidate is evaluated with 1C, 5C DFN, and coupled 4C/45C plating simulations; `calc-energy` supplies power density.

## Budget and fallback
Use a compact baseline plus 2–4 architecture/transport variants per round. If capacity is low, restore thickness/active loading while using particle and transport changes to preserve rate. If power density is low, prioritize mass reduction and DCR reduction. If temperature or plating fails, prioritize smaller particles, higher electrolyte conductivity/transference, thinner separator/current collectors, and cooling coefficient. Three repeated failures with the same cause trigger assumption questioning rather than blind retry. True DFT/MD is disabled by default.

## Domain basis and risks
- High transport and small particles reduce concentration polarization and plating risk — domain experience (no precise source).
- Thin current collectors and separators reduce inactive mass and improve gravimetric power — domain experience (no precise source).
- Higher porosity improves transport but lowers volumetric active material — domain experience (no precise source).
- The contract power-density and energy-density values are tool-derived and electrolyte-excluded; this limitation is carried into the verification report.
