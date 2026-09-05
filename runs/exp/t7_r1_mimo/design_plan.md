# Design Plan: HEV Battery (t7_r1_mimo)

**Case ID**: t7_r1_mimo  
**Date**: 2026-08-31  
**Base Parameter Set**: Chen2020 (NMC811/graphite, baseline teaching parameterization)

---

## 1. Objective Decomposition

### Primary Metrics & Thresholds

| Metric | Threshold | Priority | Trade-off Direction |
|--------|-----------|----------|-------------------|
| Energy density | ≥ 327.18 Wh/kg | HIGH | Thicker electrodes → higher ED but worse thermal dissipation and rate capability |
| 4C fast charge (no plating) | anode_potential_v ≥ 0 V at all times during 4C charge at 45°C | HIGH | Higher porosity/thinner electrode → better rate → less plating risk, but lowers ED |
| SEI thickness after 100 cyc @ 45°C | ≤ 550 nm | MEDIUM | Thinner coating → less ED penalty, but thicker SEI; high-T aging accelerates SEI growth |
| Nail penetration (10 W) | No thermal runaway (triggered = false) | HIGH | Higher thermal mass → safer but heavier (lower ED) |

### Multi-Objective Trade-off Analysis

**ED vs Rate Capability (4C plating)**: Chen2020 baseline is a teaching parameterization — moderate electrode thickness. The target ED of 327.18 Wh/kg is achievable for NMC811/graphite if electrodes are moderately thick. However, thicker electrodes reduce Li⁺ transport and increase plating risk at 4C. **Strategy**: start with baseline characterization, then explore moderate thickness increases with compensating porosity/separator adjustments.

**ED vs SEI at 45°C**: High-temperature aging accelerates SEI growth. Chen2020 has an SEI kinetic model (ec reaction limited). Without additives/coating, the 550 nm limit after 100 cycles at 45°C should be checked early. If the baseline SEI exceeds 550 nm, the only lever within locked material freedom is reducing electrode thickness (which hurts ED).

**ED vs Nail Safety**: 10 W nail heat is modest — the key is thermal mass (m×Cp). Heavier cells absorb more heat. If nail safety fails, reducing electrode thickness (less stored energy) or increasing separator thickness helps, but both hurt ED.

**Critical risk**: ED ≥ 327.18 Wh/kg may be at the ceiling of Chen2020 architecture space. If ceiling assessment shows the existing system cannot reach 327.18 Wh/kg with any architecture, we must escalate to Stage 2 material design (ceiling_escalation ON).

---

## 2. Candidate Strategy

### Round 1: Baseline Characterization
- Run 1C discharge (SPMe) → voltage curve, capacity
- Run calc-energy → baseline ED
- Ceiling assessment: what is the theoretical max ED under optimal architecture?
- **Decision point**: if baseline ED is close to 327.18 (within ~15%), continue with architecture tuning. If far (gap > 20%), consider ceiling escalation.

### Round 2-4: Architecture Exploration (exploration_force ON)
- 2-4 architecture variants per round, systematically exploring:
  - **Variant B**: Thicker positive electrode (increase ED, risk: plating at 4C)
  - **Variant C**: Thinner separator (reduces inactive mass → higher ED, risk: thermal safety)
  - **Variant D**: Thinner current collectors (reduces inactive mass → higher ED)
  - **Variant E**: Optimized porosity (balance transport vs active material fraction)
- Each variant simulated for 1C discharge + calc-energy → ED check
- Candidates that pass ED threshold proceed to aging and safety checks

### Round 5-8: Aging + Safety Screening
- Run 100-cycle aging at 45°C for ED-passing candidates
- Run 4C charge at 45°C with plating + thermal model
- Run nail penetration thermal runaway test
- Select Top candidate(s) that pass all criteria

### Round 9+: Fine-tuning (if needed)
- If all candidates fail one metric, diagnose failure cause
- Fallback routing: architecture issue → adjust params; material issue → escalate to Stage 2

---

## 3. Budget Allocation

| Phase | Rounds | Purpose |
|-------|--------|---------|
| Baseline characterization | 1 | Anchor performance of Chen2020 default |
| Architecture exploration | 3-4 | Screen 6-10 architecture variants |
| Aging + safety screening | 2-3 | Evaluate surviving candidates |
| Fine-tuning | 0-2 | Fix marginal failures |
| **Total** | **6-10** | |

---

## 4. Risk and Fallback Plan

### Risk 1: Chen2020 baseline ED too low
- **Probability**: Medium — Chen2020 is a teaching parameterization, not optimized for high ED
- **Mitigation**: Ceiling assessment in Round 1; if gap too large → escalate to Stage 2 (material design)
- **Fallback trigger**: If 3 consecutive architecture variants fail ED → question system assumption

### Risk 2: 4C plating at high ED
- **Probability**: High — thicker electrodes increase plating risk
- **Mitigation**: High porosity + thin separator + high transport electrolyte parameters
- **Fallback**: If plating persists → reduce electrode thickness (ED trade-off) or add architecture with smaller particles

### Risk 3: SEI exceeds 550 nm at 45°C
- **Probability**: Medium — 45°C accelerates SEI; no additives in locked material scope
- **Mitigation**: Run aging first; if exceeds threshold → the only lever is reducing electrode thickness
- **Fallback**: If SEI > 550 nm for all candidates → honestly report negative result (material modification needed)

### Risk 4: Nail penetration triggers thermal runaway
- **Probability**: Low — 10 W is modest; Chen2020 cell thermal mass may be sufficient
- **Mitigation**: Run thermal runaway ODE with correct mass
- **Fallback**: If triggered → reduce stored energy (thinner electrodes) or increase thermal mass

---

## 5. References (Domain Basis)

- Chen2020 parameterization: PyBaMM teaching example, NMC811/graphite, based on Chen et al. (2020) data-driven model → PyBaMM documentation
- SEI growth at elevated temperature: standard organic SEI model in PyBaMM, ec reaction limited kinetics → protocol SKILL.md Section 1, Stage 3
- Plating criterion: anode surface potential < 0 V vs Li/Li⁺ → standard plating module in PyBaMM
- Nail penetration thermal runaway: three-side-reaction ODE (SEI decomposition / negative-electrolyte / positive-electrolyte) → run-tr protocol
- Domain experience: NMC811/graphite cells can achieve 250-350 Wh/kg at cell level depending on electrode loading and packaging; 327.18 Wh/kg is in the upper range of achievable with Chen2020 parameters

---

## Plan Status

**Created**: 2026-08-31  
**Status**: Active  
**Next action**: Baseline characterization (Round 1)
