# Design Plan — Case t4_r1_mimo
## Extreme-Cold Battery: -20°C Retention ≥ 95%, ED ≥ 327.18 Wh/kg, VED ≥ 880 Wh/L

**Date**: 2026-08-30  
**System**: NMC811 / Graphite (Chen2020 parameterization)  
**Start stage**: 3 (cell design; materials use baseline defaults)

---

## 1. Objective Decomposition

| Metric | Threshold | Priority | Trade-off direction |
|--------|-----------|----------|---------------------|
| 1C capacity retention @ -20°C | ≥ 95% | **Critical** (task's defining requirement) | Higher EC content → better ED but worse low-T conductivity |
| Gravimetric ED | ≥ 327.18 Wh/kg | High | Thicker electrodes → higher loading → higher ED but worse rate/low-T |
| Volumetric ED | ≥ 880 Wh/L | High | Lower porosity → higher VED but worse transport |

### Multi-objective trade-off expectation
- **ED vs low-T retention**: Primary tension. High ED requires thick, dense electrodes. Low-T retention requires efficient Li⁺ transport. The compromise is high loading + optimized electrolyte transport.
- **Gravimetric vs volumetric ED**: These can be jointly optimized by reducing porosity (reduces volume more than mass since electrolyte is excluded from mass but not volume). However, too-low porosity kills transport, worsening low-T performance.

## 2. Candidate Strategy

### Round 1: Baseline characterization
- Run 1C discharge (25°C) → calc-energy for ED/VED
- Run lowT_discharge (-20°C) → get retention %
- **Ceiling assessment**: Can Chen2020 baseline reach 327.18 Wh/kg? If not → need electrolyte/transport optimization.

### Round 2-3: Architecture variants (high-energy targets)
Based on baseline gap:
- **Variant A**: Increase electrode thickness (+20%), reduce porosity (neg: 0.25→0.20, pos: 0.30→0.25)
- **Variant B**: Thinner current collectors, optimal separator
- **Variant C**: Extreme loading (thick electrodes + thin separator + thin CC)

### Round 4-5: Electrolyte formulation for cold performance
Key insight: EC freezes at -29°C (mp) but becomes highly viscous at -20°C. 
Solvent reformulation:
- **Candidate F1**: Reduce EC fraction (30→15 wt%), increase DMC/LMC for lower viscosity
- **Candidate F2**: Fluoroethylene carbonate (FEC) co-solvent replacement — wider liquid range
- **Candidate F3**: Ethyl acetate (EA) co-solvent — very low viscosity, good Li⁺ transport at -20°C

Transport parameter overrides (estimate based on domain knowledge):
- F1: σ↑ 40% at -20°C, D↑ 30%, t+ unchanged
- F2: σ↑ 25% at -20°C, D↑ 20%, t+ unchanged  
- F3: σ↑ 60% at -20°C, D↑ 45%, t+ slightly reduced

### Round 6+: Combined optimization
Best architecture + best electrolyte → verify all three metrics simultaneously.

## 3. Budget Allocation

| Phase | Rounds | Purpose |
|-------|--------|---------|
| Baseline characterization | 1 | Establish starting point |
| Architecture exploration | 2-4 | Push ED/VED to target |
| Electrolyte optimization | 5-7 | Achieve low-T retention |
| Combined verification | 8-9 | Final validation |
| Safety assessment | 10 | Stage 4 check |
| **Total** | **~10** | |

## 4. Risk and Fallback Plan

### Risk 1: ED ceiling too low (Chen2020 baseline)
- **Check**: Run calc-energy on baseline
- **If below target**: The parameter set's electrode loading and particle size limit ED. Adjusting thickness/porosity is the primary lever.
- **Fallback**: Increase electrode thickness progressively until solver stability limits

### Risk 2: Low-T retention unreachable at high ED
- **The fundamental tension**: Thick electrodes + low porosity = high ED but poor low-T kinetics
- **Fallback route (per protocol)**: Architecture issue → Stage 3 (adjust porosity upward, accepting some ED loss)
- **Escalation**: If no architecture works → electrolyte formulation is the lever (higher σ at -20°C)

### Risk 3: Three-strike scenario
- If same failure cause persists 3 rounds → stop blind tuning, question assumptions
- Likely 3-strike point: "Is 327.18 Wh/kg reachable with Chen2020 system at -20°C ≥95%?"
- Question layers: (1) system parameter bounds (2) task boundary (electrolyte freedom) (3) metric physicality

## 5. References (Domain Basis)

- NMC811/graphite baseline ED ~250-300 Wh/kg → Chen2020 parameterization (literature baseline)
- EC freezing point -29°C → causes dramatic conductivity drop at -20°C → electrolyte design literature (domain experience)
- Low-viscosity co-solvents (DMC, EA, fluorinated ethers) improve low-T transport → well-established in battery literature (domain experience)
- Increasing electrode thickness increases areal capacity → fundamental battery design principle
- Reducing porosity increases volumetric energy density → standard trade-off in cell design

## 6. Decision Log

| Decision | Rationale | Date |
|----------|-----------|------|
| start_stage = 3 | No new materials/additives specified; optimization of existing system | 2026-08-30 |
| base_params = Chen2020 | No explicit electrode system → default per protocol | 2026-08-30 |
| real_compute = false | Default (headless session) | 2026-08-30 |
| Electrolyte unlocked | Extreme-cold task implies electrolyte reformulation is necessary | 2026-08-30 |
