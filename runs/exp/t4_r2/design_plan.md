# Stage 1 — Overall Design Plan
## Case t4_r2: extreme-cold battery (−20 °C equipment)

**Task (verbatim)**: Design a battery for extreme-cold environment equipment: 1C discharge capacity retention >= 95% at -20C, energy density >= 327.18 Wh/kg, volumetric energy density >= 880 Wh/L.

**Case parameters (parsed, zero-interaction; entry 0 is the contract)**
- System: none named → anchor-table default Chen2020 (LCO/graphite teaching parameterization), recorded.
- start_stage: 3 (no new materials named → architecture/formulation space; electrolyte transport overrides via parameter bridge).
- Freedoms: all five categories adjustable (widest interpretation, recorded in entry 0 meta).
- real_compute: false; ablation switches: all ON.

## 1. Objective decomposition (decision layers per entry 0)

| # | Metric | Threshold | Layer | Physical drivers | Trade-off direction |
|---|---|---|---|---|---|
| 1 | retention_1c_m20c | ≥ 0.95 | stage2 (cell) | electrolyte σ/D at 253.15 K (Arrhenius ≈ −80% vs 298 K bare), solid diffusion τ = R²/Ds, areal current density (electrode thickness), porosity, particle radius | conflicts with W3 (thick/dense) |
| 2 | energy_density_wh_kg | ≥ 327.18 (contract caliber, layers-only, 25 °C 1C) | stage2 | cathode capacity & OCP, anode capacity, separator/collector mass fraction | mildly conflicts with W1 (thinner electrodes add overhead) |
| 3 | energy_density_wh_l | ≥ 880.0 (contract caliber, layers-only) | stage2 | stack thickness budget: electrodes vs separator+collector overhead, porosity | strongly conflicts with W1 (thick dense electrodes maximize Wh/L) |
| 4 | T_max_K | ≤ 333.15 (default, task silent) | stage3 (4C/45 °C) | heat generation, cooling h | mostly independent |
| 5 | plated | false (default) | stage3 (4C/45 °C) | anode kinetics vs Li⁰ potential | conflicts with thin-anode high-ED designs (N/P) |

Expected binding constraint order: **W3 ≈ W1 >> W2**. W3/W1 ratio implies stack mean density ≈ 2.69 g/cm³ (327.18/880 = 0.3718 L/kg), i.e. a compact, cathode-dominated stack — the design must maximize cold transport *within* a dense stack.

## 2. Candidate strategy

- **R1 baseline**: full profile of Chen2020 defaults (1C discharge + calc-energy + lowT discharge + retention + 4C/45C safety), funnel log carries the mandatory base-determination statement (default reason + discriminant dump). **Opening ceiling assessment** in this round: estimate the best-possible Chen2020-set architecture+formulation (thin separator/collectors, optimal porosity, small particles, high-transport electrolyte overrides) against the three stage2 targets; quantify the gap.
- **R2 in-set tuning (if ceiling plausible)**: Chen2020 architecture/formulation variants — particle radius ↓, electrode thickness ↓/↑ sweep, separator thinner, porosity tuned, electrolyte σ/D/t⁺ overrides (low-T-optimized formulation proxy, marked `estimate`).
- **Likely escalation (ceiling_escalation ON)**: LCO/graphite stack ceiling is lower than NMC811/SiOx for W3 (rough order-of-magnitude: LCO ≈ 730–800 Wh/L layers-only at 4–5 mAh/cm² vs NMC811/SiOx ≈ 830–900). If R1/R2 show a material gap → **Stage 2 escalation: system switch to OKane2022** (NMC811/graphite+SiOx, cracking model; anchor-table match) + bridging overrides. Formulation/solvent candidates enter Stage 3 directly per protocol (no molecular funnel); organic additive molecules would go through the three-model funnel (funnel_voting ON).
- **Rounds 3–8**: OKane2022 architecture/electrolyte sweep, 2–4 variants per round (exploration_force ON): thickness/porosity/N-P/separator/collector/particle-size + transport overrides; challenge both cold retention and W3.
- **Rounds 9–10**: DFN precision confirmation on passers (SPMe screens first), Stage 4 safety on finalists (4C/45 °C lumped + plating), select recommendation.
- **Closing**: 7 deliverables + PDF releases, endorse (real_compute=false → recorded skip), final entry, render, verify-deliverables.

## 3. Budget allocation

- Stage 3 exploration ≈ 60% of rounds (baseline + ceiling + ≤8 variant rounds); Stage 4 safety ≈ 20%; closing/deliverables ≈ 20%. DFN only for passers. SPMe screens ≈ seconds, DFN ≈ minutes — full loop affordable.
- Per-round pattern: propose → run 1C+lowT(+4C for complete criteria coverage) → calc-energy → mechanical retention derivation → batch log-evaluate (one entry per candidate).

## 4. Risk and fallback plan

- **R1 (cold retention vs W3 irreconcilable)**: if ≥ 3 consecutive rounds fail on the same cause → three-strike questioning (system assumption / task-boundary assumption / metric assumption) written layer-by-layer into the final `escalation` field; if truly unreachable, close as an honest negative result stating the reachable frontier ("relax X to Y" per protocol).
- **R2 (LCO ceiling gap)**: answered by the R1 ceiling assessment — escalation to OKane2022 (not architecture thrashing).
- **R3 (electrolyte overrides are estimates)**: parameter-bridge values for σ/D/t⁺ marked `estimate`, never masqueraded as measured; validated directionally in-cell (cold retention responds).
- **R4 (Chen2020 lacks full thermal/geometry set)**: run-pyamm injects defaults with trace (`injected_defaults`); T_max reliability marked approximate in evaluate notes.
- **R5 (SPMe underestimates cold transport? / plating)**: DFN double-check on finalists; plating key auto-derived from anode_potential_v.
- **R6 (simulation artifact)**: any non-monotonic capacity behavior labeled honestly; no beautification.

## 5. References (domain basis — real sources only)

- LCO/graphite baseline parameterization (Chen2020): C.-H. Chen, F. Brosa Planella, K. O'Regan, D. Gastol, W. D. Widanage, E. Kendrick, *J. Electrochem. Soc.* 167, 080534 (2020).
- NMC811/graphite+SiOx + degradation parameterization (OKane2022): S. E. J. O'Kane et al., *Phys. Chem. Chem. Phys.* 24, 7909 (2022).
- Low-temperature electrolyte formulations: low-EC / ester co-solvent electrolytes raise conductivity at −20 °C → M. C. Smart, B. V. Ratnakumar, *J. Electrochem. Soc.* 149, A361 (2002); transport-limited capacity loss at low T → domain experience (no precise source).
- Particle-size dependence of low-T rate capability (τ = R²/Ds) → domain experience (no precise source); small-particle advantage also measured in-platform precedent (T1 +14.6 contribution note in protocol).
- High-energy NMC811 cells: commercial 350 Wh/kg / ~750 Wh/L plateau → industry reports (domain experience).

## Revision history
- v1 (2026-08-26, round 0): initial plan per above.
- v2 (2026-08-26, after R1): ceiling assessment — W3 solvable in-set via compression (B1 893.12 Wh/L ≥ 880); **ceiling_escalation to OKane2022 NOT triggered**; Chen2020 base retained for the session. Warm-start artifact found in lowT protocol → cold-soak procedure (`Initial temperature [K]`=253.15) recorded; re-nominalization procedure adopted for C-rate honesty.
- v3 (2026-08-26, after R3): SPMe plating indicator at 4C declared unreliable (discharge-leg/over-prediction artifacts) → **all plating/T_max verdicts moved to DFN**. DFN mechanism: end-of-charge separator-interface salt depletion (r_neg lever neutral-to-worse; margin monotone but insufficient). Strike 1 recorded (geometry-only attack, R2+R3).
- v4 (2026-08-26, after R4): escalation layer 1 — lever class switched to electrolyte transport (σ 1.4→1.6, D 2.6e-10→3.2e-10, t+ 0.5→0.6, formulation estimates, T-independent scalars) + cooling h 40→80. Transport moved ap_min by +0.185 V and T_max by −14.8 K; thick-stack (27 A areal) family shed.
- v5 (2026-08-26, after R5): **finalist E3 selected** — compressed stack (por 0.28/0.28, sep 8 µm, cc 12/8 µm, r 3.5/3 µm) + high-transport blended-single-ion electrolyte (σ 1.6 S/m, D 3.2e-10, t+ 0.6) + anode porosity headroom 0.28 + h=80 liquid cooling. All five criteria pass at DFN verdict grade; two independent DFN 4C runs identical. Budget consumed: rounds 1–5 in Stage 3 (plan allowed ≤8 variant rounds after baseline), Stage 4 on finalist per plan line 30.