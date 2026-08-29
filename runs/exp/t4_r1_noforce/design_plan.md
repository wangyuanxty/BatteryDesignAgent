# Design Plan — t4_r1_noforce: Extreme-Cold Battery (≥95% −20 °C retention, ≥327.18 Wh/kg, ≥880 Wh/L)

## 1. Objective decomposition

| Decision layer | Metric | Threshold | Protocol / source |
|---|---|---|---|
| stage2 (cell) | lowT_retention | ≥ 0.95 | lowT_discharge.capacity_ah ÷ 1C_discharge.capacity_ah (same params/mode, mechanical) |
| stage2 (cell) | energy_density_wh_kg | ≥ 327.18 | calc-energy (1C DFN discharge; electrolyte excluded, contract caliber) |
| stage2 (cell) | energy_density_wh_l | ≥ 880 | calc-energy (energy / Σ layer thickness × area) |
| stage3 (safety) | T_max_K (4C charge @45 °C, lumped) | ≤ 333.15 (60 °C) | 4C_charge_45C + run-tr if abuse needed (protocol default; task silent on safety) |
| stage3 (safety) | plated | false | anode_potential_v min ≥ 0 V in 4C_charge_45C |

**Expected trade-off direction**: ED/ED_vol vs low-T retention is the central Pareto tension. Thick, low-porosity electrodes raise energy density but lengthen ionic/solid diffusion paths and raise local current density — both punished harder at −20 °C (slower kinetics/diffusion). Conversely, high-porosity/thin electrodes help low-T but dilute ED. Safety (4C plating) opposes thin anodes and low anode porosity. Design freedom: all five DOF categories adjustable (widest interpretation, recorded in entry 0).

**First-order size-up (from parameter dump)**: Chen2020 stack mass ≈ 0.423 kg/m², thickness 200.8 µm, area 0.1027 m², 5 Ah nominal. If 1C delivers ≈5 Ah at ≈3.7 V avg → ED ≈ 425 Wh/kg, ED_vol ≈ 897 Wh/L — i.e., the ED/volumetric targets likely pass at baseline with margin; the binding constraint is expected to be −20 °C retention. Margin can be spent on transport-friendly architecture (thinner CC, smaller particles, electrolyte boost).

**Parameter-set note (measured)**: Chen2020's "Electrolyte conductivity [S.m-1]" function is temperature-independent (0.949 S/m at 298 K and 253 K) while OKane2022's scales by Arrhenius (0.949 → 0.280 S/m at 253 K). Chen2020 at −20 °C therefore represents an optimistic electrolyte-transport limit; low-T losses come from reaction kinetics (j0 Arrhenius) and solid diffusion. This asymmetry is a parameter-set property, to be annotated honestly in evaluations. Overriding σ via the parameter bridge replaces the value (constant override) — for Chen2020 the override sets a flat value; for OKane2022 the reference value scales with T.

## 2. Candidate strategy

- **Round 1 — baseline characterization (Chen2020)**: 1C discharge SPMe→DFN, lowT discharge SPMe→DFN, 4C charge 45 °C lumped+plating (SPMe screen), calc-energy, mechanical retention. Plus **opening ceiling assessment**: best-possible architecture+formulation of the existing NMC811/graphite system (thin CC 8/6 µm, thin separator, porosity 0.25/0.20, boosted σ/D/t⁺, small particles) vs the objective. If ED ceiling < 327.18 → escalate to material design (system switch OKane2022 NMC811/SiOx — SiOx anode raises capacity per anode mass, the standard high-ED path).
- **Rounds 2+ — fallback-routed levers**, applied at the scale the failure lives:
  - *Retention gap* (Stage-3, formulation/architecture levers): electrolyte σ ×2–3, D ×2–3, t⁺ ↑ (low-T-optimized electrolyte formulation — parameter bridge); particle radius ↓ (more reactive area, lower local current density, shorter solid diffusion); electrode thinning only if needed (costs ED).
  - *ED/volumetric gap* (Stage-3, architecture levers): reduce CC thickness (16/12 → 8/6 µm — Cu dominates mass), reduce porosity, separator thinning; thicker electrodes only after retention secured.
  - *Plating risk at 4C* (Stage-4): thicker anode / N/P ↑, porosity ↑ if triggered.
- Every evaluated round also passes the 4C safety exam (same cell model, independent dimension).

## 3. Budget allocation

~12 rounds: R1 baseline+ceiling (1 round) → retention levers (3–4 rounds) → ED/volumetric fine-tune (2–3 rounds) → joint tuning to margin (2–3 rounds) → safety confirmation + DFN finals (1–2 rounds). System-switch round (OKane2022) inserted on ceiling-escalation trigger, which also re-baselines retention (its electrolyte has real T-dependence — expected to *lower* low-T retention; transport boost then applied there).

## 4. Risk and fallback plan

1. **Retention may be kinetics-limited, not transport-limited** (j0 Ea dominates at −20 °C). Transport-only boosts would plateau below 95 %. Fallback: particle radius reduction (surface area ↑) — the architecture-side kinetics lever — plus electrolyte boosts jointly. Verify first (R2) before spending rounds on transport alone.
2. **Chen2020 T-independent electrolyte may inflate retention unrealistically** — if Chen2020 passes retention trivially, still annotate the parameter-set artifact; consider re-validating the final design on OKane2022 (real Arrhenius electrolyte) as a robustness check so the delivered design is not an artifact of one parameter set.
3. **ED_vol may be the binding ED metric**: volume includes porosity, so low-porosity architecture is the volumetric lever (same direction as mass ED — no conflict).
4. **DFN stiffness at 253 K**: auto-degrades to SPMe (runner); if SPMe fallback occurs, annotate and prefer SPMe-consistent comparisons.
5. **Three-strike rule**: if the same failure cause repeats 3 rounds → stop blind tuning, question system/boundary/metric assumptions layer by layer (recorded in final `escalation`), change direction or close as negative result honestly.

## 5. References (domain basis, real sources only)

- NMC811/graphite(+SiOx) cell parameterization and multi-scale parameter estimation → Chen et al., J. Electrochem. Soc. 167 (2020) 080534 ("Chen2020" set; PyBaMM); O'Kane et al., Phys. Chem. Chem. Phys. 24 (2022) 7909 ("OKane2022" set; SiOx anode, aging/plating parameters).
- Electrolyte conductivity composition dependence → Capiglia et al., J. Power Sources 81–82 (1999) 859 (function `electrolyte_conductivity_Capiglia1999` in PyBaMM).
- Electrolyte diffusivity/transference (LiPF6-EC-EMC) → Nyman et al., Electrochim. Acta 53 (2008) 6356 (function `electrolyte_diffusivity_Nyman2008` in PyBaMM).
- Direction: SiOx anode raises cell-level ED via higher specific capacity at given N/P → high-Si anode literature (domain experience; e.g., NMC811/SiOx 5 Ah cells reaching ~250 Wh/kg packaged, per the Chen 2020 cell paper's application notes).
- Direction: smaller active particles + higher-conductivity low-T electrolyte improve −20 °C rate capability; charge-transfer activation energy dominates low-T polarization → domain experience (no precise source).
- Direction: thin Cu/Al collectors and low porosity raise both gravimetric and volumetric ED → domain experience (no precise source).

## Revision history

- v1 (2026-08-25): initial plan, R1 baseline + ceiling assessment pending.
