# Design Plan — VBF Case t2_r1_flash

**Task (verbatim)**: Design a battery for grid energy storage: energy density ≥ 327.18 Wh/kg, support 4C fast charge (no lithium plating), anode SEI thickness ≤ 500 nm after 100 cycles of 1C cycling, discharge capacity retention ≥ 90% at -20°C, SEI ≤ 550 nm after 500 cycles.

**Case meta**: headless (zero-interaction) run; base = Chen2020 (task named no electrode system → deterministic default, record in entry 0); start_stage = 3 (no material design requested in task text; escalate into Stage 2 only if the opening ceiling assessment shows a material-property bottleneck); real_compute = false; all five degree-of-freedom categories adjustable (widest interpretation, recorded in entry 0 meta.freedoms); T_max red line = 333.15 K (60 °C) documented default.

---

## 1. Objective decomposition (layered, with priorities and trade-off expectations)

| # | Metric (layer) | Threshold (contract) | Risk | Trade-off |
|---|---|---|---|---|
| 1 | `energy_density_wh_kg` (stage2) | ≥ 327.18 | Low–medium | Thick electrodes/thin CC raise ED but worsen polarization → hurts 4C & −20 °C |
| 2 | `sei_thickness_nm_end` @100 cyc (stage2) | ≤ 500 nm | Low (baseline ≈ 449 nm per signal-scale reference) | — |
| 3 | `sei_500cyc_nm` @500 cyc (stage2) | ≤ 550 nm | Medium–high (sublinear growth at 500 cyc likely exceeds 550 with baseline kinetics) | SEI suppression (coating/additive bridge) |
| 4 | `lowT_retention` @−20 °C, 1C (stage2) | ≥ 0.90 | **High (hardest)** — baseline Li-ion typically 0.4–0.8 at −20 °C | High-transport electrolyte + small particles + thin electrodes |
| 5 | `plated` @4C charge 45 °C (stage3) | false | Medium–high | Small negative particles, high σ, N/P margin, cooling |
| 6 | `T_max_K` @4C charge 45 °C (stage3) | ≤ 333.15 K | Medium | Cooling h lever (thermal management) |

Priority: all six must pass. Risk order (highest first): lowT retention → 4C plating → 500-cycle SEI → ED → T_max → 100-cycle SEI.

Key trade-off axis: **ED vs rate/low-T** — thicker electrodes raise ED but raise polarization; the final design must find a compromise (moderate thickening + transport/particle levers for rate metrics).

## 2. Candidate strategy

- **Round 1 — baseline characterization (Chen2020, untouched)**: 1C discharge (DFN), calc-energy, aging 100 cyc, aging 500 cyc, lowT discharge, 4C charge (lumped + plating). Establishes the gap per metric and feeds the opening ceiling assessment.
- **Opening ceiling assessment** (during R1 evaluation): estimate the best-possible architecture+formulation of the NMC811/graphite system (thin CC 6/10 µm, optimal porosities, high-transport electrolyte) for ED, 4C, and −20 °C. If lowT/4C ceilings fall short → **escalate into Stage 2** (electrolyte formulation candidates / additive design). If ED ceiling is sufficient (expected: NMC811/graphite can reach >350 Wh/kg with aggressive architecture) → stay in architecture space.
- **Round 2 — targeted levers by gap**:
  - ED gap → architecture: thicker positive (75.6 → ~95–110 µm), thinner CCs (Al 16 → 8–10 µm; Cu 12 → 6 µm), N/P retune.
  - lowT + 4C gaps → electrolyte formulation overrides (σ/D/t⁺ for a low-T high-conductivity formulation; literature-order values, marked `estimate`) + negative particle radius ↓ (5.86 → ~3–4 µm) + separator porosity ↑.
  - SEI@500 gap → electrode modification bridge: `SEI kinetic rate constant` ↓ (×0.1 order, coating-suppression bridge) and/or `SEI reaction exchange current density` ↓; compare on same system (Chen2020).
  - T_max gap → `Total heat transfer coefficient` ↑ (10 → 20–40 W/m²K).
- **Round 3 — combined best design**: full verification battery (all 6 sims) on the best combination.
- **Round 4+ — final safety re-verify + closing**.

## 3. Budget allocation (flash run, target ≤ ~22 sims)

- R1 baseline: 6 sims. R2: ~8 sims (2–3 architecture variants + 1–2 electrolyte variants + SEI variant, each on the protocols that matter for its gap). R3 combined: 6 sims. R4 final: 1–2 sims. Reserve ~4 sims for fallback iterations. If 3 consecutive rounds fail on the same cause → three-strike questioning + plan update (no 4th blind try).

## 4. Risk and fallback plan (symptom → scale routing)

- **lowT_retention < 0.90**: hardest metric. Ladder: (1) electrolyte transport overrides with aggressive-but-realistic values (σ(−20 °C) ~8–12 mS/cm class, LiFSI-based/ester-containing formulations — literature order-of-magnitude, marked estimate); (2) negative particle ↓ + thinner electrodes + separator porosity ↑; (3) if still failing → three-strike: question metric reachability within boundary; if genuinely unreachable, honestly record negative result with the "if X relaxed to Y" note. No threshold relaxation.
- **plated = true @4C**: negative particle ↓, σ ↑, t⁺ ↑, N/P margin ↑, cooling ↑. Root cause = anode surface potential < 0 V (transport + architecture).
- **sei_500cyc_nm > 550**: SEI kinetics reduction (coating bridge: Al2O3-class coating or FEC-class additive; organic additive → molecular funnel at Stage 2, inorganic coating → direct Stage 3 aging). If additive route taken, funnel screening applies (three-model voting, HOMO elimination line).
- **energy_density < 327.18**: thicker electrode + thin CC + porosity optimization; ceiling assessment bounds reachability.
- **T_max > 333.15**: cooling h ↑ (thermal management lever).
- **Fallback routing rule**: material-property gap → Stage 2; architecture/parameter gap → Stage 3. Escalation (cell → material) only when gap attribution says the existing system's property ceiling is the bottleneck.

## 5. References (domain basis; all real, none fabricated)

| Direction | Source |
|---|---|
| Thick electrodes / thin current collectors raise gravimetric ED | Kuang, Chen, Kirsch, Hu, "Thick Electrode Batteries: Design, Fabrication, and Performance", Advanced Energy Materials 9, 1803857 (2019) — direction only |
| High-energy NMC811/graphite cell parameterization (baseline) | Chen et al., "Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models", J. Electrochem. Soc. 167, 080534 (2020) — the Chen2020 base set itself |
| Li plating during fast charge ↔ negative surface potential < 0 V | O'Kane et al., Li-plating modelling parameter set (OKane2022, PyBaMM), J. Electrochem. Soc. (2022) — direction only |
| Ester co-solvents / high-LiFSI electrolytes raise low-temperature conductivity and fast-charge capability | Dahn group ester-based electrolyte studies (Logan et al.) — domain experience, no precise citation; direction only |
| −20 °C retention of conventional Li-ion typically 0.4–0.8 | Domain experience (no precise source) |
| SEI growth suppression via coatings (Al2O3-class) and film-forming additives (FEC-class) | Domain experience (no precise source); bridging via SEI kinetic rate constant / SEI reaction exchange current density per protocol parameter bridge |

## 6. Deliverables at close

design_spec.md, bom.xlsx, datasheet.md, calc.xlsx, dvpr.md, dfmea.md, delivery_index.md (+ PDF releases), report.html via `bda render`, `verify-deliverables` check, endorse/final entries (endorse records real_compute=false skip honestly).
