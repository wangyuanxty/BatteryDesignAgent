# Design Plan — t6_r1_noceiling: Smartphone Cell

Case: smartphone battery, volumetric energy density ≥ 950 Wh/L, 4C fast charge without lithium plating, T_max ≤ 50 °C, anode SEI ≤ 500 nm after 100 cycles, voltage plateau ≥ 4.1 V.
Ablation: `ceiling_escalation` OFF — no proactive material-design escalation; only materials/systems named in the task text (none named → default system Chen2020, NMC811/graphite); design happens inside the cell/architecture formulation space.

## 1. Objective decomposition (decision thresholds + expected trade-offs)

| Metric | Threshold (entry 0) | Scale of the lever | Expected difficulty |
|---|---|---|---|
| Volumetric ED | `energy_density_wh_l ≥ 950` (calc-energy contract caliber: discharge energy ÷ stack volume; electrolyte/casing excluded by tool definition) | Stage 3 architecture | Medium-hard: dead-layer thinning + loading of capacity-limiting negative electrode |
| Voltage plateau | `midpoint_voltage_v ≥ 4.1` (tool definition: voltage at discharge-time midpoint) | Stage 2 material (cathode OCP) | **Infeasible in-scope**: NMC811/graphite midpoint ≈ 3.6–3.7 V; architecture moves it only by tens of mV (IR). 4.1 V requires a 4.7 V-class cathode (LNMO-class) — a system switch, forbidden by the ablation boundary |
| Fast charge | `plated = false` at 4C charge, 45 °C ambient (`anode_potential_v` min < 0 → plated, mechanical) | Stage 3 architecture (negative particle size, porosity, N/P, thickness) + Stage 4 check | Hard at high ED (trade-off direction: dense/thick negatives plate earlier) |
| Max temperature | `T_max_K ≤ 323.15` (50 °C) during 4C/45 °C | Stage 3 thermal management (cooling h 10→25 W/m²K) | Depends on 4C heat generation; ΔT allowance is only 5 K above the 45 °C ambient |
| SEI after 100 cycles | `sei_thickness_nm_end ≤ 500` (aging_1C_100cyc, isothermal) | Stage 3 aging (SEI kinetics baseline) | Expected pass: Chen2020 baseline final SEI ≈ 449 nm (skill reference calibration); watch dense designs |

**Multi-objective trade-off expectations**
- ED ↑ needs compaction (thinner separator/CC, higher active fraction with lower porosity, thicker capacity-limiting negative). All three worsen or stress 4C fast charge (longer/thinner electrolyte paths, higher local current density) → ED ↔ plating Pareto.
- 4C at 45 °C generates strong ohmic + reversible heat; with h = 10 W/m²K the lumped thermal may exceed 323.15 K → cooling h is a free-ish lever (smartphone graphite-spreader cooling, up to ~25 W/m²K, recorded).
- Plateau vs everything: fixed by cathode OCP — independent of architecture; expected to fail on every candidate; this is the flagged material gap (ceiling_escalation OFF → cannot close it; three-strike questioning will document the boundary).

## 2. Candidate strategy

- **R1 — baseline + first ED variants** (exploration_force: ≥2 variants/round): baseline characterization of Chen2020; then (A) dead-layer thinning (separator 12→9 μm, CC 16/12→10/8 μm); (B) A + active-fraction ↑ with porosity ↓ (pos 0.665→0.70/0.335→0.30, neg 0.75→0.80/0.25→0.20, nominal 5.6 Ah); (C) A + negative thicken 85.2→110 μm (capacity-limiting electrode, nominal 6.4 Ah). Screen: 1C discharge (SPMe) + calc-energy.
- **R2 — 4C safety pass**: on baseline + best-ED variants, 4C_charge_45C (DFN, lumped, plating). Refine against plating: negative particle radius ↓, negative porosity ↑ (recover), N/P management. Refine against T_max: cooling h ↑.
- **R3 — aging pass**: aging_1C_100cyc on ≤3 finalists; check `sei_thickness_nm_end ≤ 500`.
- **R4+ — refinement rounds** until ED ≥ 950 with safety pass, or budget exhaustion. Plateau expected to fail every round (same cause) → three-strike questioning at round ≥4, documented in `final.escalation`.

## 3. Budget allocation

- R1: 4 × (1C SPMe + calc-energy) ≈ 4 × ~15 s.
- R2: 4 × 4C DFN ≈ 4 × ~1–3 min. R3: ≤3 × aging SPMe ≈ ≤3 × ~1 min.
- R4–R6: targeted refinements (2–3 variants/round, screened SPMe, DFN for finals).
- Total ≈ 6 rounds. No true compute (`real_compute: false` — closing records the skip honestly).

## 4. Risk and fallback plan

| Risk | Watch-signal | Fallback (scale-correct routing) |
|---|---|---|
| Plateau ≥ 4.1 V unreachable | midpoint_voltage_v ≈ 3.6–3.7 on every candidate | Material gap (cathode OCP = Stage 2 property). Escalation forbidden (ceiling_escalation OFF, no system named in task). Three-strike → question boundary; final honestly notes "reachable only via high-voltage cathode system (e.g., LNMO-class, midpoint ≈ 4.17 V per anchor table) — excluded by ablation" |
| 4C plating | anode_potential_v < 0 in R2 | Stage 3: smaller negative particles, higher negative porosity, moderate N/P, avoid over-thick negative |
| T_max > 323.15 K | 4C T_max_K | Stage 3 thermal: h ↑ within 10–25; if still failing at h=25, record thermal ceiling honestly |
| SEI > 500 nm | aging final thickness | Stage 3: lower local current density (higher active fraction/thickness) or accept negative on this metric |
| ED < 950 after full architecture space | R4–R6 plateau of best ED | Record ceiling honestly (opening ceiling assessment without escalation); final notes which material lever would be needed (Si anode / higher cathode capacity) — outside ablation boundary |

## 5. References (directional basis; no fabricated sources)

- NMC811/graphite cell midpoint ≈ 3.61 V vs LNMO-class ≈ 4.17 V → virtual-battery-factory skill §1.5 anchor table (this skill's `references/`, bda `data/LNMO.json`).
- Chen2020 SEI kinetics signal scale (kinetic rate constant ×0.1 → 100-cycle SEI 449→385 nm) → virtual-battery-factory skill SKILL.md Stage 3 (measured reference).
- Contract energy-density formula and plateau/DCR definitions → bda `energy.py` (tool definition, same formula for all tasks).
- ED vs fast-charge trade-off, smartphone passive cooling h range (10–25 W/m²K), commercial NMC/graphite volumetric ED ~700–750 Wh/L → domain experience (no precise source).
- Smaller negative particles raise plating resistance at high rate (measured +14.6 contribution in prior protocol runs) → virtual-battery-factory skill SKILL.md Stage 3 (T1 reference).

## Revision history

- v1 (2026-08-25): initial plan (R1: baseline + 3 ED variants; R2: 4C safety; R3: aging; plateau flagged as material gap under ceiling_escalation OFF).
- v2 (2026-08-25, update: three-strike triggered after R4): stop blind architecture tuning. Three causes failed 3+ consecutive rounds — plateau (cathode OCP ceiling ≈ 4.0 V; best 3.998 V), T_max at 4C/45 °C (hA ≤ 0.133 W/K in-boundary; best 336.4 K at h=25), plating-free 4C at ED ≥ 950 (plating-free ED ceiling measured ≈ 770–840 Wh/L). Questioning recorded in log `final.escalation`; direction changed from architecture exploration to honest negative-result closing with Pareto documentation and per-metric relaxation mapping. Achieved in-boundary: ED ≥ 950 (B: 951.7, B-p: 964.4 Wh/L) and SEI ≤ 500 nm (404.6/417.7/449.1 nm).
