# Battery Design Plan — t1_r1_luna

## Objective decomposition
- Gravimetric energy density: **≥392.61 Wh/kg** (cell-level contract-caliber metric).
- 4C fast charge: no lithium plating (mechanically, minimum anode surface potential ≥0 V).
- Maximum temperature: **≤60 °C = 333.15 K** during the 4C/45 °C safety protocol.
- Overcharge to 4.7 V: no thermal runaway trigger.

Energy density and thermal/rate safety are competing objectives: thinner/leaner inactive layers and high-voltage chemistry improve Wh/kg, while high transport, small particles, and cooling reduce polarization/heat. The 4.7 V requirement also favors a high-voltage cathode/system rather than relying only on a conventional NMC baseline.

## Starting interpretation and boundaries
No electrode system or material was named, so the deterministic default is Chen2020 for the baseline characterization. Starting layer is Stage 3 (architecture/system objective, no named new material); baseline material properties are marked baseline. Per zero-interaction rules, unspecified degrees of freedom take the widest interpretation: electrode system, electrolyte transport/formulation, electrode modification, architecture, and thermal management are adjustable. True compute defaults false. Structure model was not requested. All ablation switches remain ON.

## Candidate strategy
1. Characterize Chen2020 baseline with SPMe 1C discharge and contract-caliber `calc-energy`.
2. Test high-voltage LNMO parameter set as a system candidate because the task explicitly requires operation to 4.7 V and the anchor table identifies it as a 4.7-V-class system.
3. Test architecture/transport variants only where needed: thin current collectors/separator, reduced electrode thickness/porosity optimization, smaller particles, elevated electrolyte conductivity and cooling coefficient. Every variant is simulated and evaluated.
4. For the strongest candidate, run 4C charge at 45 °C with coupled lumped thermal/plating model, then overcharge and thermal-runaway ODE. If the first design fails, route failures to architecture/transport (temperature/plating) or system/material (energy-voltage ceiling) rather than blind reruns.

## Budget and risks
Use fast SPMe screening first; reserve DFN for promising designs and use the required safety protocols for the finalist. Main risks are: (a) conventional Chen2020 energy-density ceiling below the target, (b) 4C plating/temperature failure at 45 °C, and (c) high-voltage abuse triggering runaway. If the same cause fails three consecutive rounds, stop blind tuning and record a layered reachability question before pivoting or closing negative.

## Domain basis
- High-voltage cathode/system direction → protocol anchor table (LNMO JSON is identified as a 4.7-V-class system).
- Higher electrolyte transport, smaller particles, and stronger cooling reduce high-rate polarization/heat → domain experience (no precise source used for a conclusion-grade value).
- All conclusion-grade numeric values will be taken from BDA output artifacts; no true DFT/MD endorsement is requested.
