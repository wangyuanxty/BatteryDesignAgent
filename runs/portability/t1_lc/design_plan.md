# Design Plan — t1_lc (Next-generation pure-electric sedan)

## 1. Objective decomposition (decision layers)

Parsed from task text (verbatim thresholds):

| Decision layer | Metric | Threshold | Scenario |
|---|---|---|---|
| stage2 (cell performance) | energy_density_wh_kg | ≥ 392.61 | 1C discharge, contract-caliber (electrolyte/casing excluded) |
| stage3 (safety) | plated | false | 4C charge @45°C |
| stage3 (safety) | T_max_K | ≤ 333.15 K (60°C) | 4C charge @45°C, lumped thermal |
| stage3 (safety) | triggered | false | overcharge to 4.7 V (NMC upper cut-off 4.2 V + 0.5 V) |

**Multi-objective trade-off expectations (directional):**
- ED vs 4C fast-charge: thicker/denser electrodes raise ED but worsen transport → higher risk of plating and higher T_max. Expected Pareto tension.
- ED vs T_max: thicker electrodes raise areal loading → higher internal heat generation per cell mass for a given rate; T_max is the binding constraint at 4C.
- Overcharge stability (4.7 V no TR): NMC811 cathode decomposition/oxygen release above ~4.5 V is the dominant TR driver → a high-voltage-stable cathode (LNMO) or cathode coating/additives may be needed; this conflicts with ED (LNMO has lower practical ED).

## 2. Candidate strategy

- **Round 1 — baseline characterization (Chen2020, default system since task names no electrode system).**
  Measure contract-caliber ED (1C discharge + calc-energy), 4C plating/T_max, and overcharge→TR. This establishes the gap and the ceiling.
- **Ceiling assessment** (executed during Round 1): estimate best-possible architecture (thin CC/separator, optimal porosity, high loading) and transport-formulation ceiling of Chen2020 against 392.61 Wh/kg. Objective exceeds ceiling → **escalate to Stage 2 material design** (system switch to OKane2022 NMC811/SiOx for higher ED, and/or electrolyte/cathode-stability additives for 4.7 V overcharge).
- **Follow-up directions (per fallback routing):**
  - ED shortfall → scale at which cause lives = material (switch to higher-capacity system OKane2022 SiOx) or architecture (thin collectors/separator, high loading, low porosity).
  - Plating at 4C → architecture/parameter (particle size down, porosity up, N/P, electrolyte transport σ/t⁺).
  - T_max > 60°C → thermal management (cooling h up) + transport.
  - Overcharge TR → material (cathode coating / electrolyte additive / LNMO system switch).

## 3. Budget allocation

- Round 1: baseline (4 simulations + calc-energy + TR). 
- Rounds 2–4: architecture + thermal exploration (2–4 variants/round per exploration_force).
- If ceiling shortfall: 1–2 rounds material/system switch (OKane2022, LNMO), then re-verify cell scale.
- Safety fine-tuning: 1–2 rounds (cooling h, particle size, coating parameter).
- Closing: endorse/render/deliverables.

## 4. Risk and fallback plan

- **Highest risk: 392.61 Wh/kg contract ED.** Chen2020 baseline likely ~400 Wh/kg (contract caliber, 5 Ah nominal / ~43 g active+CC+separator mass) — borderline. SiOx (OKane2022) raises capacity; thin collectors/separator raise ED further. If unreachable even with system switch, record negative result honestly.
- **Plating at 4C** is likely with thick high-ED electrodes; mitigate via particle size, porosity, N/P, electrolyte transport (σ/t⁺) overrides.
- **Overcharge 4.7 V TR**: NMC811 overcharge likely triggers TR → must test mechanically (run-tr). Mitigation = cathode stabilization (coating, LNMO switch) — note LNMO overcharge target becomes 5.2 V (its own cut-off +0.5 V), which does NOT satisfy the literal "4.7 V" term; record this ambiguity if used.
- Three-strike rule: same failure cause ×3 → question system/boundary/metric assumptions, update plan, continue with direction change or close as negative result.

## 5. References (direction → source)

- SiOx anode raises cell capacity/energy density → high-Si anode reviews (domain experience, no precise source).
- High-conductivity/high-transference electrolyte mitigates 4C plating → transport-parameter literature (domain experience).
- NMC overcharge oxygen-release is the TR trigger; 4.7 V stability needs cathode coating/high-voltage spinel → battery safety literature (domain experience).
- LNMO 4.7 V-class spinel cathode OCP → bda library data/LNMO.json (this skill's references).
