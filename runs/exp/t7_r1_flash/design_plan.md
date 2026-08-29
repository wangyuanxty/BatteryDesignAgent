# Design Plan — t7_r1_flash (HEV battery, four-objective contract)

Case: `runs/exp/t7_r1_flash` · start_stage 3 (cell scale) · base `Chen2020` (default, no electrode system named)
Goal (verbatim thresholds): ED ≥ 327.18 Wh/kg · 4C fast charge without Li plating · SEI ≤ 550 nm after 100 cycles @45 °C · nail (10 W short-circuit heat) without thermal runaway.

## 1. Objective decomposition (decision layers)

| # | Metric (output key) | Threshold | Layer | Protocol | Trade-off direction |
|---|---|---|---|---|---|
| 1 | `energy_density_wh_kg` | ≥ 327.18 | stage2 | 1C_discharge → calc-energy | thick/low-porosity electrodes raise ED but worsen 4C plating margin and 45°C SEI/thermal load |
| 2 | `plated` (from `anode_potential_v` min < 0) | false | stage3 | 4C_charge_45C --thermal lumped --plating | thin negative / small particles / high-σ electrolyte mitigate; conflicts with ED |
| 3 | `sei_thickness_nm_end` | ≤ 550 | stage2 | aging_1C_100cyc_45C | 45 °C accelerates SEI; coating (SEI kinetics ↓) is the strong lever |
| 4 | `triggered` | false | stage3 | run-tr --q-nail 10 --mass-kg (mcp=mass×900), t-init from 4C T_max_K | small cell = small mcp = fast nail heating; cooling hA is the dominant lever |

Priority: ED first (hardest), then nail (needs coherent cooling design), then plating, then SEI — but all four must pass on the **final integrated candidate** (no metric-independent winners).

## 2. Baseline expectation (Chen2020, from dumped parameters)

- Geometry: pos 75.6 µm/ε0.335, neg 85.2 µm/ε0.25, sep 12 µm/ε0.47, Al 16 µm, Cu 12 µm, area 0.1027 m², nominal 5 Ah.
- Estimated mass ≈ 0.043 kg (43 g class) → nail mcp ≈ 39 J/K; with default hA≈0.053 W/K a sustained 10 W nail heats ~0.26 K/s → side-reaction onset (~408 K est.) reached in minutes → **baseline expected to trigger**; cooling must be designed (hA ≥ ~0.9 W/K keeps nail steady-state below onset).
- Baseline 1C discharge starts from Chen2020's discharged initial state (cathode x≈0.27) — first-discharge capacity is a fraction of nominal; calc-energy measures this contract discharge. ED baseline expected ~240 Wh/kg class (estimate, will measure).
- SEI: k_SEI=1e-12 m/s, i0=1.5e-7 A/m². 25 °C 100cyc ≈ 449 nm (protocol reference); 45 °C will be higher (Arrhenius) — **likely > 550 nm; coating lever ×0.1 kinetics is the prepared countermeasure** (25 °C reference: 449→385 nm).
- 4C charge at 45 °C: 20 A on 0.103 m² ≈ 19 mA/cm² — moderate; baseline may or may not plate. Thicker electrodes will degrade the margin.

## 3. Candidate strategy

- **R1 (baseline characterization)**: Chen2020, no overrides — 1C (spme→dfn) + calc-energy; 4C_charge_45C (thermal lumped + plating); aging_1C_100cyc_45C; run-tr nail (10 W, mass-coupled, t-init = 4C T_max_K; plus t-init 298.15 standard check). Produces the gap vector.
- **R2 (architecture variants, 3)**: HE-1 (thicker electrodes, thin CC/sep), HE-2 (HE-1 + lower porosity), HP-1 (plating-mitigation: thin negative, small negative particle, high-σ electrolyte). Full battery: 1C+calc-energy, 4C, aging45.
- **R3+ (targeted)**: close whichever gaps remain:
  - ED short → loading push + (if architecture ceiling insufficient) escalate to Stage 2 material design: system switch (OKane2022 SiOx-family or LNMO high-voltage) — anchor-verified before switch.
  - SEI > 550 → electrode modification (SEI kinetic rate constant ×0.1, compare on same system).
  - Plating → electrolyte σ/t⁺ formulation override + negative particle/thickness.
  - Nail → thermal management h_total (W/m²K) with consistent run-tr hA = h×A_surface; verify 4C T_max stays sane.
- **Final round**: integrate the winning levers into one candidate; re-verify all four metrics; then Stage 4 nail on the final cell + close.

## 4. Budget allocation

Baseline R1 (4 sim classes) · architecture R2 (3 candidates × 4 sims, spme quick-screen, dfn for passers) · targeted R3–R5 (2–3 candidates/round) · integrated final + nail · Stage 5: real_compute=false → skip endorsement, honestly record. Estimated total: 8–14 rounds; simulation cost is seconds-to-minutes each.

## 5. Risk and fallback plan

- **ED hardest**: if architecture space cannot reach 327.18 (three-strike on ED), question in order: (a) system assumption — is Chen2020 the right base or does the task imply a higher-energy system (escalate to OKane2022 SiOx / LNMO); (b) boundary assumption — are excluded levers truly excluded (recorded); (c) metric assumption — only then consider honest negative. Escalation is preferred over negative: the task text's "battery for HEV" with no system named leaves the electrode system adjustable (widest interpretation).
- **Nail**: physics says cooling hA is decisive. If hA values needed exceed physical plausibility, question the 10 W-sustained reading of the scenario and the thermal-management boundary; design hA from cell geometry + HEV liquid-cooling practice (realistic hA ~0.5–1.5 W/K for a module-level pouch with active cooling).
- **SEI 45 °C**: if ×0.1 kinetics insufficient, add SEI exchange-current lever or combine with cycling-temperature design; comparison always on the same system (Chen2020 family).
- **Plating**: if architecture+electrolyte can't clear 4C, revisit N/P balance and negative particle size; particle-size lever measured +14.6 contribution in prior runs (skill reference).
- **Three-strike**: stop blind tuning, question three layers (system / boundary / metric), record in final escalation, then direction change or honest negative.

## 6. References (directional basis)

- Parameter set Chen2020 → C.-H. Chen, F.B. Planella, K. O'Regan, D. Gastol, W.D. Widanage, E. Kendrick, "Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models", J. Electrochem. Soc. 167 (2020) 080534.
- SiOx/high-capacity anode direction + cracking → S.E.J. O'Kane et al., "Lithium-ion battery degradation: what you need to know", Phys. Chem. Chem. Phys. 24 (2022) 7909 (OKane2022 parameter set basis).
- 4C fast charge / plating mitigation → S. Ahmed et al., "Enabling fast charging – A battery technology gap assessment", J. Power Sources 367 (2017) 250.
- SEI growth at elevated temperature (45 °C aging) → E. Prada et al., J. Electrochem. Soc. 160 (2013) A616 (aging model family).
- Thermal-runaway/nail three-side-reaction model → as implemented in bda run-tr (Kim et al. 2019 / Coman et al. 2016 Arrhenius kinetics; tool-cited).
- High-energy cell architecture (thin collectors/separator, high loading) trade-off vs rate → domain experience (no precise source).
- HEV battery thermal management (active cooling for fast charge) → domain experience (no precise source).
