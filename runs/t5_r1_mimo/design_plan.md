# Design Plan — t5_r1_mimo

## Revision history

- **Update after Round 1:** initial Chen2020 characterization showed the default baseline fell well short on energy density while 4C screening revealed lithium plating. Therefore Round 2 shifted to thicker-electrolyte-thinner-inert-mass candidates with stronger transport/cooling.
- **Update after Round 2:** Candidates C and D achieved the energy-density target and removed 4C plating, but both exceeded the 60 °C (333.15 K) thermal ceiling. Round 3 now focuses on thermal mitigation while preserving the high-energy candidate geometry.
- **Update after Round 3:** Candidate E remained slightly above the thermal ceiling, while Candidate E2 met all three targets (energy density, no plating, and maximum temperature). Candidate E2 is selected as the final recommended design for closing deliverables.


## Objective decomposition

Targets parsed from the task statement:

1. Gravimetric energy density ≥ 500.94 Wh/kg.
2. 4C fast charge without lithium plating.
3. Cell maximum temperature ≤ 60 °C (333.15 K) under thermal-coupled operation.

Primary multi-objective tension:

- Energy density favors thicker active layers, higher active-material fractions, lower inert mass, and benign transport assumptions.
- Fast-charge plating resistance and temperature control favor thinner electrodes, higher porosity, stronger electrolyte transport, higher cation transference, and more cooling headroom.
- The design should therefore be tuned as a Pareto problem, not as a single-metric optimization.

Decision-layer acceptance basis used by the protocol:

- `stage2` = discharge/energy deliverables.
- `stage3` = safety/abuse deliverables (4C charge thermal/plating).
- `stage1` left unspecified by the task text; will default to protocol molecular-level elimination lines only if a material-design path is needed.

## Starting-point determination

The task text states only performance targets and does **not** name an electrode system, electrolyte formulation, coating/dopant, architecture pack, or thermal boundary condition.

Per protocol:

- Electrode system not named → default to `Chen2020` and record the deterministic mapping reason.
- `start_stage: 3` is the correct default, because the objective as written does **not** specify new materials/additives/coatings.
- `real_compute: false` by default.

Important implication for this case:

- With `start_stage: 3`, no molecular screening is performed in the first instance; material properties are taken from the selected baseline parameter set.
- If the ceiling assessment later shows that the baseline system cannot reach 500.94 Wh/kg even with aggressive architecture/optimal formulation tuning, then the appropriate escalation path is cross-scale material design, not blind architectural iteration.

## Material system and mapping anchor

Selected baseline parameter set: `Chen2020`.

Deterministic mapping basis:

- Task text has no explicit electrode system.
- Protocol rule: no explicit system stated → default to `Chen2020` with an explicit record.

Operational consequence:

- Architecture exploration is the primary first-round lever.
- Electrolyte transport (`D_e`, `sigma_e`, `t_+`) and thermal coefficient `h` are unlockable via the widest boundary default in this case, because the task text does not lock them.

## Degree-of-freedom boundary (parsed from task text + headless defaults)

1. Electrode system  
   - Adjustable: yes.  
   - First-round choice: locked to `Chen2020` as the baseline system for initial architecture characterization.  
   - Escalation rule: if baseline architecture+formulation space still cannot reach the target, propose alternate systems/additives at Stage 2.

2. Electrolyte formulation  
   - Adjustable: yes.  
   - Interpretation: widest allowed by task text, because no constraint was stated.  
   - Parameters eligible for override: `Electrolyte diffusivity [m2.s-1]`, `Electrolyte conductivity [S.m-1]`, `Cation transference number`.

3. Electrode modification  
   - Adjustable: yes, if needed in later rounds.  
   - First-round priority: lower than architecture and transport, because no coating/dopant was named.

4. Cell architecture  
   - Adjustable: yes.  
   - Explicitly explorable parameters: electrode thicknesses, porosities, N/P ratio, separator thickness and porosity, current collector thicknesses, particle radii.

5. Thermal management  
   - Adjustable: yes.  
   - Parameter eligible for override: `Total heat transfer coefficient`.

Baseline-default interpretation for parameters not overridden in a round:

- Electrolyte uses default transport parameters unless explicitly overridden.
- Architecture uses baseline thickness/porosity/particle-size defaults unless explicitly overridden.
- Thermal management uses baseline `h` unless explicitly overridden.

## Ablation switches

Defaults used for this headless case, unless overridden later:

- `exploration_force`: ON  
- `ceiling_escalation`: ON  
- `funnel_voting`: ON

These states are recorded because the task text declares no ablation mode.

## Candidate strategy

### Round 1 plan

1. Run baseline `Chen2020` 1C discharge to establish the anchor operating point (`capacity_ah`, `energy_density_wh_kg`).
2. Use `calc-energy` to compute contract-grade gravimetric energy density and supporting mass/thickness metrics.
3. Run at least two architecture variants in the same round:
   - Variant A: thinner electrodes / higher rate-friendly transport path.
   - Variant B: thinner current collectors / higher active-material fraction.
4. Begin coarse thermal/plating assessment on the baseline system if architecture looks promising.

### Fallback routing (applied after each evaluation)

- If ED is too low but 4C safety looks favorable → return to Stage 3 and push architecture toward higher energy density.
- If ED looks feasible but 4C plating occurs → return to Stage 3 and improve transport/thermal boundary conditions (porosity, particle size, electrolyte transport, `h`).
- If architecture + formulation space is exhausted and ED ceiling remains below target → escalate to Stage 2 material design / system switching.

## Budget allocation (conceptual, not a hard round cap)

- First 3 rounds: baseline and coarse architecture exploration.
- Next 2–3 rounds: coupled 4C safety screening and temperature/plating mitigation.
- Additional rounds if needed: transport-tuned Pareto iterations or material escalation.

## Risk and fallback plan

1. **Primary risk:** ED infeasibility under `Chen2020` defaults.  
   - First response: aggressive but physically plausible architecture tuning plus transport improvement.
   - If still infeasible: escalate into material/system design (Stage 2).

2. **Primary fast-charge risk:** lithium plating.  
   - First response: increase porosity, reduce particle radius, and improve electrolyte transport parameters.
   - If ED too low afterward: re-balance ED vs rate capability.

3. **Primary thermal risk:** failure to stay ≤ 333.15 K during 4C charge.  
   - First response: transport/diffusivity improvements and increased `h`.
   - Risk: excessive thermal improvements may be unrealistic if not supported by plausible formulation/system changes.

4. **Logging risk:** headless mode may incorrectly restrict allowed design levers if freedom boundaries are set too narrowly.  
   - Mitigation: this plan adopts the widest allowed interpretation for unspecified degrees of freedom.

## References (domain basis for strategy)

- `Chen2020` parameter set usage → base-parameter anchor table in VBF protocol (`SKILL.md` §1.5).
- Architecture/transport/mitigation mapping → VBF protocol and CLI-command reference in `.claude/skills/virtual-battery-factory`.
- Widest interpretation of unspecified freedoms → VBF headless-execution rule and lessons recorded in protocol.
- Plating/treatment of safety metrics → VBF protocol Stage 4 and evaluation guidance.
- Practical direction only: high-energy dense cells typically require either electrode thinning, inert-mass reduction, improved electrolyte transport, or higher-voltage/high-capacity active materials.
