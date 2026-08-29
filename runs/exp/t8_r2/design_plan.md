# Design Plan — Long-Endurance Drone Battery (Case t8_r2)

## Objective (verbatim from task text)

| Metric | Threshold | Source of truth |
|---|---|---|
| Gravitimetric energy density | ≥ 446.18 Wh/kg | `calc-energy` contract-caliber (discharge energy / layer-stack mass, electrolyte excluded — procedure-defined, not chosen) |
| 5C discharge capacity retention | ≥ 90% | capacity_ah(5C discharge, DFN) ÷ capacity_ah(1C discharge, same parameters) — mechanical division, recorded to a derived JSON for evaluation |
| Cell mass | ≤ 40 g (= 0.04 kg) | `calc-energy` `mass_kg` (layer stack × electrode area) |

## Objective decomposition and trade-offs

1. **ED ≥ 446.18 Wh/kg — binding metric.** ED is a stack-composition ratio: increase active/inactive mass ratio (thinner current collectors, thinner separator, higher electrode density/lower porosity) and raise mean discharge voltage. Chen2020 baseline stack (75.6 µm NMC811 / 85.2 µm graphite, 12 µm separator, 16/12 µm collectors, area 0.1027 m²) is estimated at ≈ 400–415 Wh/kg contract-caliber (≈ 43.5 g mass) → expected gap ≈ 30–45 Wh/kg.
2. **5C retention ≥ 90% — binding metric, opposite lever direction.** Rate capability wants small particles, moderate electrode thickness, high electrolyte transport (σ, D, t⁺). Electrode thickening for ED worsens 5C retention → **Pareto pair (ED × retention)**; prefer mass-neutral transport levers (electrolyte σ/D/t⁺, particle-size routing) over thickness extremes.
3. **Mass ≤ 40 g — geometric lever.** ED and 5C retention are area-independent ratios; mass is area-proportional. Baseline ≈ 43.5 g → reduce electrode area (width 1.58 m → ≈ 1.4 m) or trim inactive mass. No capacity target in the task, so area is a free lever.
4. **Stage 4 safety exam (protocol default):** 4C charge at 45 °C, lumped thermal + plating module — `plated` must be false. Thin anodes raise plating risk → guard with N/P and negative particle size.

## Candidate strategy

- **R1 — baseline characterization (Chen2020, no overrides):** 1C discharge (SPMe screen → DFN), `calc-energy`, 5C discharge DFN, 4C-charge-45 °C safety DFN. Establishes measured gap and the Stage-3 opening **ceiling assessment** (best-case architecture + high-transport electrolyte envelope vs 446.18).
- **R2–R4 — architecture + formulation variants (2–4/round):** thin collectors (16/12 → 10/8 → 6/4 µm), thin separator (12 → 9 → 8 µm), porosity trim (pos 0.335 → 0.30, neg 0.25 → 0.26), thickness rebalance (pos 76 → 85–95 µm, neg 85 → N/P-tuned), particle trim (pos 5.22 → 3.5 µm, neg 5.86 → 4.0 µm), electrolyte σ ≈ 1.2–1.3 S/m, D ≈ 2.6–2.9e-10 m²/s, t⁺ = 0.35 (high-transport LiPF₆-carbonate formulation direction; literature values, marked as such — not simulation output).
- **Ceiling escalation (ON):** if the R1 ceiling assessment shows 446.18 unreachable in the NMC811/graphite envelope → escalate to Stage 2 material design: system candidate **OKane2022 (graphite+SiOx** — higher anode capacity, lower anode mass fraction **)**; only then inpatient molecule/coating work.
- **Every round:** best/selected variants re-verified at 5C and the 4C safety exam; mass checked via `calc-energy` on the same params.

## Budget allocation

- R1: 4 simulations (SPMe screen + 3 DFN). R2–R6: ≈ 4 variants × 4 sims ≈ 16. Possible system-switch rounds: +2. Total target ≤ 8 rounds / ≈ 30 simulations, all second-to-minute scale.
- `real_compute: false` → Stage 5 true-DFT/MD endorsement skipped; `endorse` entry records the skip honestly. No fabricated first-principles numbers.

## Risk and fallback plan

- **Risk 1 — ED ceiling of NMC811/graphite:** if aggressive architecture+formulation tops out below 446.18 → escalate Stage 2 (SiOx system, then cathode composition via `run-comp`); if the material envelope still falls short → three-strike questioning (system / boundary / metric) → honest negative result with the "reachable if relaxed to X" note. Never relax the threshold itself.
- **Risk 2 — 5C retention < 90%:** diagnose transport limitation (electrolyte σ/D/t⁺ vs solid-state diffusion in particles) → formulation overrides first (mass-neutral), then particle/porosity/thickness; no solid-phase diffusivity masquerading (excluded lever).
- **Risk 3 — plating at 4C charge:** raise transport, trim negative particle radius, tune N/P; mechanical `plated` judgment only (anode_potential_v min < 0).
- **Risk 4 — mass > 40 g at final stack:** reduce electrode area (ratio metrics invariant) and re-run `calc-energy` for the mass evidence.
- **Fallback routing:** architecture/parameter symptoms → Stage 3 levers; potential-window/material-limit symptoms → Stage 2. Three consecutive failures of the same cause → stop blind tuning, question assumptions layer-by-layer, direction change or honest negative close.

## References (direction → source, no fabrication)

- Alloy/SiOx anodes raise anode capacity and cell ED → Obrovac & Chevrier, *Chem. Rev.* 114 (2014) 11444–11502.
- Baseline NMC811/graphite parameterization → Chen et al., *J. Electrochem. Soc.* 167 (2020) 080534 (PyBaMM Chen2020).
- Carbonate-electrolyte transport ceiling (σ, D, t⁺ of LiPF₆ blends) → Valøen & Reimers, *J. Electrochem. Soc.* 152 (2005) A882; Nyman et al., *Electrochim. Acta* 53 (2008) 6356–6365.
- Next-generation drone-cell ED directions (Li-metal / high-capacity anodes) → Lin, Liu & Cui, *Nat. Nanotechnol.* 12 (2017) 194–206; drone-cell roadmaps → domain experience (no precise source).
- SiOx-containing NMC cell parameterization → OKane2022 published parameter set (PyBaMM; J. Electrochem. Soc. / PCCP publication — exact citation to be fixed before any paper use).