# Design Plan: Grid Energy Storage Battery

## Case ID: t2_r1_mimo

## 1. Objective Decomposition

**Primary targets (all must be met simultaneously):**

| # | Metric | Threshold | Decision Layer | Priority | Trade-off Direction |
|---|--------|-----------|----------------|----------|-------------------|
| M1 | Energy density | ≥ 327.18 Wh/kg | Stage 2 (cell) | HIGH | Thicker electrodes → higher ED but worse thermal/rate |
| M2 | 4C fast charge (no plating) | anode_potential_v ≥ 0 at all times | Stage 3 (safety) | HIGH | Higher rate → more plating risk; needs good transport |
| M3 | SEI thickness @100 cyc | ≤ 500 nm | Stage 2 (cell aging) | MEDIUM | Baseline Chen2020 SEI kinetics |
| M4 | Capacity retention @-20°C | ≥ 90% (vs 25°C) | Stage 2 (cell) | MEDIUM | Low-T retention limited by electrolyte transport |
| M5 | SEI thickness @500 cyc | ≤ 550 nm | Stage 2 (cell aging) | MEDIUM | Long cycling accumulation |

**Key trade-off expectations:**
- ED (M1) vs 4C plating (M2): Thick electrodes boost ED but increase transport resistance → plating risk at 4C. Must balance loading with rate capability.
- ED (M1) vs low-T retention (M4): Thick electrodes exacerbate low-T transport limitations.
- SEI growth (M3/M5): Chen2020 baseline SEI kinetics determine this; if unacceptable, need electrode modification (coating/additive).

## 2. Starting Point Determination

- **start_stage: 3** — Task specifies grid storage performance targets; no new materials/additives/electrode modifications requested
- **base_params: Chen2020** — NMC811/graphite system (default per §1.5 anchor table: no explicit system mentioned → default Chen2020)
- **Materials source: baseline** — all material properties from Chen2020 parameter set (literature values)
- **Degrees of freedom: WIDEST** — task text does not restrict any category → all five adjustable (electrode system locked to Chen2020; electrolyte formulation, electrode modification, cell architecture, thermal management all adjustable)

## 3. Candidate Strategy

**Round 1: Baseline characterization**
- Run Chen2020 baseline with default architecture
- Compute ED, aging (100cyc), low-T retention, 4C plating
- Establish which metrics are met/failing
- Perform opening ceiling assessment: estimate best-possible ED for Chen2020 system

**Round 2-4: Architecture exploration (2-4 variants per round)**
- Based on baseline diagnosis, propose targeted architecture variants:
  - Variant A: Thicker electrodes (higher loading → boost ED)
  - Variant B: Thinner electrodes with lower porosity (balance ED and transport)
  - Variant C: Optimal N/P ratio tuning (prevent plating)
  - Variant D: Smaller particle size (improve rate → help plating + low-T)
- Each variant simulated for 1C discharge + aging + low-T + 4C charge

**Round 5+: Iterative refinement**
- If ED insufficient: push electrode thickness higher
- If plating persists: increase electrolyte transport or reduce particle size
- If SEI too thick: consider electrode modification (coating)
- If low-T retention fails: consider electrolyte formulation change

**Budget allocation:** ~15 rounds total; ~5 for baseline + ceiling; ~10 for architecture iteration

## 4. Risk and Fallback Plan

| Risk | Likelihood | Mitigation | Fallback Route |
|------|-----------|------------|----------------|
| Chen2020 ED ceiling below 327 Wh/kg | MEDIUM | Ceiling assessment first | If ceiling < target → escalate to Stage 2 material design (system switch or electrolyte formulation) |
| Plating at 4C | MEDIUM | Reduce particle size, optimize N/P | Architecture adjustment (Stage 3) |
| Low-T retention < 90% | MEDIUM-HIGH | Chen2020 transport may be limiting | Electrolyte formulation (σ, D adjustments) — if locked, report negative |
| SEI > 500 nm @100 cyc | LOW-MEDIUM | Baseline SEI kinetics | Electrode modification (coating) — if needed, propose additive candidates |
| Three-strike on ED | MEDIUM | Escalation: question system boundary | If Chen2020 truly cannot reach 327 Wh/kg → system switch to higher-ED system |

**Three-strike questioning plan:**
1. Model/system: Is Chen2020 NMC811/graphite physically capable of 327 Wh/kg at practical parameters?
2. Task boundary: Are architecture degrees of freedom sufficient, or is electrolyte modification needed?
3. Metric: If 327 Wh/kg is unreachable with Chen2020, what is the actual ceiling?

## 5. References

- Chen2020 parameter set: NMC811/graphite teaching parameterization (base defaults for this task)
- SKILL.md §1.5 anchor table: deterministic system → parameter set mapping
- Domain experience: typical NMC811/graphite cells achieve 200-280 Wh/kg at cell level; >300 Wh/kg requires aggressive thin separator, low porosity, high loading
- Domain experience: 4C plating risk depends on Li⁺ diffusivity in graphite and electrolyte transport; smaller particles reduce plating risk
- Domain experience: EC/EMC-based electrolyte低温性能 is moderate; achieving >90% at -20°C requires good transport parameters

## 6. Ablation Switches

All ON (default):
- exploration_force: ON — propose 2-4 architecture variants per round
- ceiling_escalation: ON — proactive material-design escalation if ceiling assessment shows gap
- funnel_voting: ON — three-model heterogeneous voting (irrelevant at start_stage 3, relevant if escalated to Stage 2)
