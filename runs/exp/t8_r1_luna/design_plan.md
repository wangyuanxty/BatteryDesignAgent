# Battery Design Plan — t8_r1_luna

## Objective decomposition
- Primary gravimetric energy density: **≥446.18 Wh/kg** by contract-caliber `calc-energy` output.
- High-rate durability: **5C capacity retention ≥90%**, mechanically computed from same-parameter 5C and 1C discharge capacities.
- Packaging constraint: **cell mass ≤40 g (0.040 kg)**, evaluated from the same `calc-energy` mass definition.
- No explicit safety threshold was supplied; safety remains a verification dimension, with 4C/45°C thermal and plating checks recorded but not used to invent an acceptance threshold.

## Candidate strategy
The task names no electrode chemistry, so the deterministic default is Chen2020 and execution starts at cell scale (Stage 3). Because the objective is unusually high for the default teaching parameterization, first characterize a baseline, then explore 2–4 architecture variants per round: thinner current collectors/separator, reduced particle radii, porosity/thickness adjustments, and transport overrides where the parameter set accepts them. The 5C retention target is checked with DFN at 5C and a same-parameter 1C reference. If the opening ceiling shows the mass/energy target is unreachable by architecture alone, escalate to material/system alternatives only if a complete parameter chain is available.

## Budget allocation and fallback
- Round 1: baseline Chen2020 characterization and safety; establish mass/ED ceiling.
- Rounds 2–4: architecture/transport variants targeting mass reduction and high-rate retention; stop blind repetition after three same-cause failures.
- If failure is capacity/heat/rate transport, fall back to Stage 3 parameter/architecture changes. If the calculated ED ceiling is below 446.18 Wh/kg, question the system and boundary assumptions and record the negative result rather than relaxing the target.
- True DFT/MD is disabled (`real_compute=false`); closing endorsement records the skip honestly.

## Domain basis
- Thinner inactive layers and current collectors reduce gravimetric dead mass (domain engineering principle; no precise source used).
- Smaller particles and improved electrolyte transport reduce high-rate polarization and plating risk (domain experience; no precise source used).
- Energy density and rate retention trade off against electrode loading and thermal transport; all final numbers are simulation/tool outputs, not estimates.
