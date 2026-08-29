# t5_r3 Design Plan — Next-Generation Flagship Vehicle Battery

Case: `t5_r3` | Date: 2026-08-26 | Mode: zero-interaction (headless), task text is the only input.

## 1. Objective decomposition (decision-layer criteria, pre-registered in log.jsonl entry 0)

| Layer | Metric | Threshold | Tool output key |
|---|---|---|---|
| stage2 (cell performance) | Gravimetric energy density | **≥ 500.94 Wh/kg** | `calc-energy:energy_density_wh_kg` |
| stage3 (safety) | 4C fast charge, no lithium plating | `plated == false` | `run-pyamm 4C_charge_45C:anode_potential_v` (min ≥ 0 V) |
| stage3 (safety) | Maximum temperature | **≤ 60 °C = 333.15 K** | `run-pyamm 4C_charge_45C:T_max_K` |

Multi-objective trade-off expectation (the central design tension of this task):
- **ED ↑** wants thick electrodes (dilute collector/separator overhead mass), thin collectors, thin separator, low/moderate porosity (contract formula: mass = Σ thickness×(1−ε)×density×area, electrolyte excluded).
- **No plating at 4C** wants the opposite *direction* on electrode thickness: 4C areal current density scales with areal capacity (loading), so thick electrodes push the negative surface potential toward 0 V → Lithium plating. Mitigation levers: smaller negative particle radius, higher electrolyte conductivity/transference number, higher N/P, SiOx-type higher-potential anodes.
- **T_max ≤ 333.15 K** with 45 °C (318.15 K) protocol ambient leaves only ~15 K headroom; 4C ohmic heating (I²R) is the driver. Lever: cooling coefficient h (thermal management is adjustable).

## 2. Candidate strategy

- **Round 1 (baseline)**: Chen2020 NMC811/graphite as-is — 1C discharge SPMe + `calc-energy` + 4C charge 45 °C (lumped thermal + plating). Establishes the anchor numbers for all three metrics + opening ceiling assessment (below).
- **Rounds 2–5 (architecture ladder, 2–4 candidates/round per exploration_force)**:
  - *Mass overhead reduction* (pure ED win, small plating impact): current collectors down-gauged (Al 16→8 µm, Cu 12→6 µm; both manufacturable: 4–5 µm electrodeposited Cu foil on flagship programs), separator 12→9 µm.
  - *Dilution*: positive electrode 75.6→100 µm, negative 85.2→112 µm (N/P maintained ≈ 1.32 in areal-capacity terms), porosity kept as complement to active fraction (physical consistency: ε + ε_am + binder ≈ 1 — never "free" porosity inflation).
  - *Plating mitigation*: negative particle radius 5.86→3 µm (higher exchange area), electrolyte conductivity override (scalar, e.g. 2× the room-temperature Nyman2008 value via the parameter bridge), cation transference number 0.2594→0.4 (formulation-adjustable).
  - *Thermal*: `Total heat transfer coefficient` 10→30–50 W/m²/K (liquid-cooled flagship thermal system, honest design choice).
- **Round 6+ material escalation (ceiling_escalation, if ED or plating fails in architecture space)**: system switch candidates — OKane2022 (NMC811 || graphite+SiOx, capacity-rich anode with cracking model) or LNMO 4.7 V-class (voltage-driven ED); scrutineered one-by-one via the same 1C/4C evaluation chain.
- **Closing**: DFN check on finalists, deliverables, honest verdict.

## 3. Budget allocation

- Rounds 1–5: architecture exploration (SPMe, seconds-scale; DFN only for shortlisted candidates — proxy-first).
- Rounds 6–9: safety fine-tuning (plating/T_max) and, if required, Stage 2 molecular candidates (three-model funnel; screening only).
- Rounds 10–11: closing — endorse (real_compute=false → skip recorded honestly), deliverables, render, verify-deliverables.

## 4. Risk and fallback plan

- **Risk 1 — ED ceiling**: if architecture space cannot reach 500.94 Wh/kg (see ceiling estimate below), escalate to material design (Stage 2 or system switch) per `ceiling_escalation`; do NOT relax thresholds.
- **Risk 2 — plating at 4C**: expected to be the binding constraint with thick electrodes. Fallback = same-scale (Stage 3) parameter corrections: smaller negative particles, higher σ/t⁺, thinner areal loading, higher N/P. If the ghost remains, three-strike questioning of the system assumption → Si-containing anode (OKane2022).
- **Risk 3 — T_max**: only 15 K of headroom above protocol ambient; h escalation + conductivity (reduced ohmic heat) are the expected corrections; abuse scenarios (overcharge/nail) are *not* part of this task's named criteria, so 4C T_max is the operative check.
- **Known artifact to watch**: Chen2020 initial state is a discharged (low-SOC) relaxation state — first discharge capacity may be low; do not silently re-interpret; quantify with the 4C protocol's own pre-discharge if needed and record honestly.

## 5. Opening ceiling assessment (computed live in round 1, DOMAIN estimate here)

- Contract ED anatomy for Chen2020 (area 0.1027 m², I₁C = 5 A): baseline mass ≈ 43 g → +35% of mass is Cu/Al current collectors (Cu alone ≈ 11 g). Thin-collector + thick-electrode architecture can plausibly lift ED from ~400 Wh/kg-class toward ~500 Wh/kg per contract formula (mass dilution). The true ceiling: mass floor = electrode active mass (cannot go below chemical content) + inevitable separator → estimated **520–550 Wh/kg** architecture ceiling assuming transport limits allow 100–112 µm pairs and 6 µm Cu foil → 500.94 is *likely reachable in architecture space*, with plating the governing constraint. This estimate is directional, to be overturned by simulation in round 1.

## 6. References (domain basis; honesty-constrained)

- SiOx anode raises capacity and shifts anode plateau to higher potential (plating margin) → commercial high-SiO anode reviews / OKane2022 parameterization (domain experience, no precise source).
- Thin Cu foil (4–6 µm) enables pack/ED gains but raises handling cost → industry battery foil reports (domain experience).
- High-conductivity, high-transference electrolytes mitigate rate-induced plating → transport-parameter literature (domain experience).
- Liquid-cooling heat-transfer coefficients 30–60 W/m²/K for prismatic/pouch EV cells → thermal management literature (domain experience).
- Contract formula and protocol rules → this skill's SKILL.md and references/cli-commands.md.

## Audit trail note

All conclusion-grade numbers below come from tool outputs (`cell/*.json`), recorded via `bda log-evaluate`; this document is updated only on material direction changes (plan-update entries).