# Design Plan — t2_r2: Grid-Energy-Storage Battery

Case: grid energy storage cell. Base system: Chen2020 (NMC811 / graphite) — task text
names no electrode system, so the deterministic anchor table selects Chen2020 (aging-capable).
start_stage = 3 (task names no new materials/additives → no Stage 2 molecular funnel unless
ceiling assessment escalates). All five degree-of-freedom categories adjustable (widest).

## 1. Objective decomposition (entry-0 contract, verbatim thresholds)

| # | Metric | Layer | Threshold | Protocol / tool |
|---|---|---|---|---|
| 1 | energy density | stage2 | ≥ 327.18 Wh/kg | 1C_discharge + calc-energy (contract formula) |
| 2 | SEI thickness @100 cyc (1C) | stage2 | ≤ 500 nm | aging_1C_100cyc |
| 3 | SEI thickness @500 cyc (1C) | stage2 | ≤ 550 nm | aging_1C_100cyc --cycles 500 |
| 4 | capacity retention @ −20 °C | stage2 | ≥ 90 % | lowT_discharge ÷ 1C_discharge (mechanical) |
| 5 | no lithium plating at 4C | stage3 | plated = false | 4C_charge_45C, lumped thermal, plating on |

Expected trade-off directions (design tension map):

- **ED ↔ 4C plating**: thicker electrodes raise ED but raise areal current density at 4C
  (plating risk ↑). Mitigators inside architecture space: high negative porosity, small
  negative particle radius, high-conductivity electrolyte, N/P margin.
- **ED ↔ SEI thickness**: thicker electrodes raise per-area cycle depth → more SEI growth
  per cycle; thinner electrodes lower it but erode ED. SEI lever independent of geometry:
  anion-film suppression via `SEI kinetic rate constant [m.s-1]` (coating/additive bridge).
- **−20 °C retention ↔ ED**: low-T capacity is transport/kinetics-limited; mitigation
  (thin cathode, high porosity, small particles, boosted electrolyte σ/D) mostly does NOT
  conflict with ED except porosity and thickness. Expect −20 °C to be the binding metric
  on the default Chen2020 transport set.

## 2. Candidate strategy

- **Round 1 — baseline characterization + ceiling probes**: run all five protocols on the
  stock Chen2020 set; compute ED via calc-energy. In parallel, probe the *ceiling* of the
  architecture space: one "max-ED" probe (thick cathode, low porosity, thin CC/separator)
  and one "fast-charge/low-T" probe (thin electrodes, high porosity, boosted electrolyte
  σ). Verdict of ceiling assessment → whether 327.18 Wh/kg + 90 % @−20 °C is reachable
  inside architecture+formulation space, or material design (Stage 2 escalation) is needed.
- **Round 2+ — architecture sweep** (exploration_force ON: 2–4 variants/round):
  electrode thickness ladder, porosity ladder, separator/CC thinning, particle-size
  reduction, electrolyte σ/t⁺/D overrides (formulation bridge), N/P revision.
- **Round N — targeted fixes** per fallback diagnosis:
  SEI@500 over → coating bridge on `SEI kinetic rate constant [m.s-1]`;
  plating at 4C → transport + anode geometry; low-T shortfall → electrolyte formulation.
- **Finalists re-verify with DFN** (1C discharge, 4C charge; aging stays SPMe per protocol).

## 3. Budget allocation

- Rounds 1–2: baseline + ceiling probes (cheap, spme-scale).
- Rounds 3–7: architecture/formulation iteration (2–4 variants each).
- Rounds 8–9: finalist DFN re-verification + coating fine-tune if SEI target marginal.
- Aging runs: SPMe 100 cyc ≈ 3 s, 500 cyc ≈ 15 s → SEI rescreening affordable every round
  for shortlisted variants only (not for wide sweeps).
- 4C charge with plating: SPMe quick-screen; DFN only for finalists.

## 4. Risk & fallback plan

| Risk | Early signal | Fallback / escalation path |
|---|---|---|
| −20 °C retention ≪ 90 % with baseline transport | lowT capacity ≤ 70 % of 25 °C | electrolyte-formulation bridge (σ/t⁺/D overrides, low-T optimized solvent direction, literature-anchored values, marked estimate if not literature-exact) — allowed DOF, no Stage-2 trip |
| 327.18 Wh/kg unreachable with plating-safe geometry | ED ceiling probe below target | re-balance thickness/porosity; if truly capped → three-strike questioning → system switch candidate (e.g. OKane2022 SiOx anode) via ceiling_escalation |
| SEI@500 > 550 nm | aging 500 trend above 550 | reduce `SEI kinetic rate constant [m.s-1]` (coating bridge, direction: ALD alumina / artificial-SEI coatings); magnitude calibrated to the protocol's measured Chen2020 reference (0.1× k → 449→385 nm @100 cyc per SKILL signal-scale note) |
| 4C plating persists | anode_potential_v min < 0 | thin negative electrode, ↑ negative porosity, ↓ negative particle radius, ↑ σ electrolyte, then re-check ED |

**Three-strike policy**: same failure cause for 3 consecutive rounds → layer-by-layer
questioning (system / task-boundary / metric assumptions) recorded in `final` escalation field;
no blind 4th retry.

## 5. Domain basis (direction → source; no fabricated citations)

- SiOx/NMC fast-charge cell parameterization & 6C fast-charge design rules →
  O'Kane et al., "Lithium-ion battery degradation: how to diagnose..." / PyBaMM OKane2022
  fast-charge parameter set (real; shipped inside PyBaMM).
- Thin-electrode / high-porosity fast-charge; SEI-limited aging → domain experience
  (no precise source).
- Low-temperature electrolyte (VC/EC/EMC limits, high-conductivity co-solvents, e.g.
  ester/ether blends) → domain experience (no precise source).
- SEI-suppressing coatings (Al2O3 ALD, artificial SEI) on graphite → domain experience
  (no precise source).

## 6. Revision history

- v1 (2026-08-26): initial plan; round-1 baseline + ceiling probes defined.
- v2 (2026-08-26, R3→R4 direction update): 4C plating resolved by anode-side rate
  optimization (neg porosity 0.42, neg particle radius 2.5 µm, σ=2.5 S·m⁻¹ const /
  D=4e-10 / t⁺=0.35, open separator) rather than thickness alone; SEI@500 required
  ≥3-decade SEI-kinetics suppression via the coating bridge — k=1e-14 insufficient
  (578 nm @500), k=2e-15 selected (330.1 nm @500, 99.9 nm @100). No system switch
  or Stage-2 material escalation needed; architecture+formulation space sufficed.
  Budget reallocated: rounds 4–5 spent on coating fine-tune + finalist DFN
  re-verification, not on further ED laddering (ED ceiling probe R1 already
  established 521.7 Wh/kg reachable — final 522.45).