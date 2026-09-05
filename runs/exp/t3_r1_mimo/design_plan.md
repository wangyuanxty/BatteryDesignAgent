# Design Plan — t3_r1_mimo: Power Tool Battery

## Case ID
t3_r1_mimo

## Objective Decomposition
- **Nominal capacity ≥ 2 Ah**: requires appropriate electrode area and thickness; Chen2020 baseline is ~1.1 Ah → need ~2× area or thicker electrodes
- **5C discharge capacity retention ≥ 95%**: 5C_capacity / 1C_capacity ≥ 0.95; this is demanding — most NMC/graphite cells at 5C show 75-90% retention; needs high electrolyte conductivity, low DCR, small particle size
- **4C fast charge without lithium plating**: anode_potential_v ≥ 0 V at all times during 4C charge at 45°C; needs good electrolyte transport (σ, D, t⁺), adequate N/P ratio, thin electrodes
- **Maximum temperature ≤ 60°C (333.15 K)**: T_max during 4C charge with thermal coupling; requires adequate cooling (h parameter)
- **Power density ≥ 4000 W/kg**: achievable with Chen2020-type cells (~3800 W/kg baseline), needs moderate DCR reduction

## Multi-Objective Trade-off Expectations
- **5C retention vs capacity**: thicker electrodes → higher capacity but worse rate capability → 5C retention drops
- **4C plating vs capacity**: higher N/P ratio → better plating resistance but lower capacity
- **Temperature vs power**: higher current → more Joule heating → T_max rises; cooling helps but adds mass
- **Power density vs capacity**: high power needs low resistance → thinner electrodes → lower capacity

**Key Pareto**: ED vs T_max: thicker electrode raises capacity but worsens heat dissipation. The target 2Ah + 95% 5C retention + no plating is physically tight — electrode thickness and porosity must be carefully balanced.

## Candidate Strategy

### Round 1: Baseline Characterization
- Run Chen2020 baseline: 1C discharge → capacity, 5C discharge → capacity (retention), 4C charge → plating check
- Compute energy density, power density via calc-energy
- **Ceiling assessment**: estimate best achievable 5C retention and capacity under Chen2020 transport parameters
- If 5C retention < 95% at baseline → escalate to material design (electrolyte transport improvement)

### Round 2-4: Architecture Optimization (if needed)
- **Architecture A**: Thinner positive electrode (reduce thickness → better rate, lower capacity)
- **Architecture B**: Higher porosity (better transport, lower volumetric capacity)
- **Architecture C**: Smaller particle size (shorter diffusion path → better rate)
- **Architecture D**: Combined (thin + high porosity + small particle)

### Round 5-8: Material Design (if ceiling exceeded)
- Electrolyte transport improvement: higher σ, higher t⁺ → better 5C retention and plating resistance
- Coating/dopant: SEI suppression for cycle life
- Electrode modification for cracking suppression under high-rate cycling

## Budget Allocation
- Rounds 1-2: Baseline characterization + ceiling assessment (~20% budget)
- Rounds 3-5: Architecture optimization (~40% budget)
- Rounds 6-8: Material design / electrolyte improvement (~30% budget)
- Rounds 9+: Fine-tuning + safety verification (~10% budget)

## Risk and Fallback Plan
1. **Risk: 5C retention impossible with Chen2020 transport parameters** → Fallback: switch to ORegan2022 (different parameterization) or invent high-σ electrolyte
2. **Risk: 2 Ah capacity requires large electrode area → high resistance → poor rate** → Fallback: optimize porosity and thickness combination
3. **Risk: 4C plating at borderline conditions** → Fallback: increase N/P ratio, improve t⁺
4. **Risk: T_max exceeds 60°C under 4C charge** → Fallback: increase cooling h parameter

## References (Domain Basis)
- Chen2020 parameter set: standard teaching parameterization for NMC811/graphite, provides baseline transport parameters
- High-rate battery design: power tool batteries typically use 18650/21700 format with high-power electrode design (thin, high porosity)
- Electrolyte conductivity literature: σ > 10 mS/cm typical for EC/EMC+LiPF6 at 25°C; t⁺ ~0.3-0.4
- Plating resistance: anode potential > 0V requires adequate D × σ × t⁺ product (transport limitation)
- Domain experience (no precise source): 5C retention > 95% typically requires electrode thickness < 50 μm and porosity > 30%
