# Battery Design Plan — t5_r1_luna

## Objective decomposition
- Cell gravimetric energy density: **≥500.94 Wh/kg** (contract metric; calculated by `calc-energy`).
- 4C fast charge: no lithium plating, determined from minimum simulated anode potential ≥0 V.
- Maximum temperature: **≤60 °C = 333.15 K**, determined from coupled lumped-thermal output.
- Priority: satisfy all three simultaneously; energy density and fast-charge thermal margin are expected to trade off against electrode loading and transport.

## Starting point and boundary
The task names no new material or electrode system, so execution starts at cell design (pipeline Stage 3) using the deterministic default Chen2020 teaching parameter set. Unspecified degrees of freedom receive the widest interpretation: architecture, electrolyte transport, electrode modification, electrode-system switching, and cooling are considered adjustable candidates, while excluded levers remain excluded by protocol. True DFT/MD is disabled by default.

## Candidate strategy
1. Characterize the Chen2020 baseline at 1C and under 4C/45°C coupled thermal-plating conditions.
2. Assess the opening energy-density ceiling. Explore 2–4 architecture variants per round, prioritizing thinner inactive layers, higher practical active loading, smaller particles, and improved electrolyte transport/cooling where valid.
3. If the existing-system ceiling is below 500.94 Wh/kg, escalate to a system/material candidate rather than blindly tuning architecture. Every candidate receives a real cell simulation and mechanical evaluation.
4. Continue targeted fallback by failure cause: architecture/thermal failures return to Stage 3; material/system ceiling failures escalate to Stage 2. Stop only on achievement or a documented three-strike/budget conclusion.

## Budget and risk plan
Allocate the initial rounds to baseline plus architecture variants, then reserve later rounds for the strongest energy/thermal compromise and (if required) a system switch. Main risks are that the Chen2020 parameterization cannot reach 500.94 Wh/kg under the contract mass definition, and that 4C charging produces plating or excessive heat. Do not relax thresholds or substitute unverified estimates. Record all solver or parameter failures verbatim and use only output-file values in conclusions.

## Domain basis
- Higher electrode loading and reduced inactive mass generally raise gravimetric energy density, but increase ionic/thermal polarization and plating risk — domain experience (no precise source).
- Smaller active particles and improved electrolyte transport reduce diffusion polarization and can improve fast-charge margin — domain experience (no precise source).
- Coupled thermal simulation is required because 4C heat generation and cooling determine the temperature constraint — protocol requirement.
