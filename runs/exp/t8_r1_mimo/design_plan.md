# Design Plan: t8_r1_mimo — Long-Endurance Drone Battery

## Case ID
t8_r1_mimo

## Objective
Design a battery for a long-endurance drone with:
- **Energy density**: ≥ 446.18 Wh/kg (gravimetric)
- **5C discharge capacity retention**: ≥ 90% (5C capacity / 1C capacity)
- **Cell mass**: ≤ 40 g

## 1. Objective Decomposition

### Primary metric: Energy Density (≥ 446.18 Wh/kg)
- This is an **extremely aggressive** target. Commercial NMC811/graphite cells achieve ~250-300 Wh/kg at cell level.
- Theoretical NMC811/Graphite: ~260 Wh/kg; NMC811/SiOx-graphite: ~300 Wh/kg
- To approach 446 Wh/kg, possible directions:
  - LNMO/graphite (4.7V cathode: higher voltage → higher ED despite heavier spinel structure)
  - NMC811 with Si-rich anode (higher capacity anode)
  - Ultra-thin current collectors + thin separator (reduce inactive mass)
  - Possible lithium metal anode (highest theoretical ED but dendrite risk)
- **Expected trade-off**: higher ED ↔ lower rate capability; thinner electrodes ↔ higher power density risk

### Secondary metric: 5C Rate Retention (≥ 90%)
- 5C retention of 90% requires good electrolyte transport (σ, D_e) and moderate electrode thickness
- Thin electrodes (<100 µm) favor rate capability but sacrifice loading
- **Trade-off**: thick electrode for ED vs thin electrode for rate capability

### Tertiary metric: Cell Mass (≤ 40 g)
- A 40g cell limit constrains electrode area × thickness × density
- Mass = Σ(layer thickness × (1−porosity) × density × area)
- Small cells inherently have higher surface-to-volume ratio → better heat dissipation

### Multi-objective Pareto expectation:
- **ED vs 5C retention**: thicker electrode raises ED but worsens rate performance
- **ED vs mass**: can use high loading thin cell design to achieve both

## 2. Candidate Strategy

### Round 1: Baseline characterization
- Run Chen2020 baseline at 1C and 5C discharge
- Determine theoretical ceiling of this system
- Assess gap to 446.18 Wh/kg

### Round 2+: Ceiling-driven material escalation
- If baseline ceiling < 446 Wh/kg (expected), escalate to material design:
  - **System A**: LNMO/graphite (high-voltage cathode, 4.7V → higher ED potential)
  - **System B**: NMC811/SiOx-graphite (OKane2022, higher-capacity anode)
  - **Architecture push**: ultra-thin current collectors (6 µm Cu, 12 µm Al), thin separator (12 µm), high porosity (0.35), optimized particle size
- If ceiling assessment shows material gap → propose electrolyte transport enhancements

### Material escalation strategy:
- **Electrolyte conductivity boost**: override σ_e → improve 5C retention
- **Thin electrode architecture**: reduce mass while maintaining loading
- **High-voltage cathode**: LNMO at 4.7V maximizes specific energy
- **Si-rich anode**: SiOx/silicon composite for higher capacity

## 3. Budget Allocation (30 rounds total)
- Round 1-3: Baseline characterization + ceiling assessment (1C, 5C, calc-energy)
- Round 4-8: Architecture optimization (thickness, porosity, N/P, CC thickness)
- Round 9-15: Material system exploration (LNMO, SiOx, electrolyte transport)
- Round 16-25: Fine-tuning + optimization (best system, iterated architecture)
- Round 26-30: Safety assessment + closing

## 4. Risk and Fallback Plan

### Risk 1: ED unreachable with Chen2020
- **Likelihood**: HIGH — Chen2020 is a teaching parameterization, max ~280 Wh/kg
- **Fallback**: Switch to OKane2022 (SiOx anode) or LNMO system (if available); explore architecture mass reduction

### Risk 2: 5C retention < 90%
- **Likelihood**: MEDIUM — depends on electrode thickness and electrolyte transport
- **Fallback**: Reduce electrode thickness, boost electrolyte conductivity via parameter bridge

### Risk 3: Material system unavailable in parameter library
- **Likelihood**: MEDIUM — may not have all candidate systems in the library
- **Fallback**: Use available systems; document limitation honestly

### Risk 4: Mass constraint conflict with ED target
- **Likelihood**: LOW — 40g is generous for small cells
- **Fallback**: Reduce electrode area, use thinner electrodes

## 5. References (domain basis)
- NMC811/graphite cell-level ED ~250-300 Wh/kg → domain experience (no precise source)
- LNMO cathode operating at 4.7V, specific energy ~150-200 mAh/g → domain knowledge
- SiOx anode capacity ~1500 mAh/g (vs graphite 372 mAh/g) → domain knowledge
- Thin current collector (6µm Cu) reduces inactive mass by ~50% vs standard 10µm → domain knowledge
- 5C retention depends on electrode thickness (Thikhampornchai 2021-like observation) → domain experience
- OKane2022 parameter set has SiOx in negative electrode → anchor table verification
