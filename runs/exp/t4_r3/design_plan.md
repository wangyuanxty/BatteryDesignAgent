# Design Plan — runs/exp/t4_r3: Extreme-Cold Equipment Battery (Chen2020)

Case: t4_r3. Date: 2026-08-26. Mode: zero-interaction (headless); plan is executed without human confirmation; every conclusion-grade number must come from tool output.

## 1. Objective decomposition (contract, verbatim from task text)

| Metric | Threshold | Decision layer | Judged by |
|---|---|---|---|
| 1C discharge capacity retention at −20 °C | ≥ 95 % | stage2 | 100 × cap(lowT_discharge 1C @253.15 K) ÷ cap(1C_discharge @298.15 K), same params, mechanical derivation written to `bridge/` for `bda log-evaluate` |
| Gravimetric energy density | ≥ 327.18 Wh/kg | stage2 | `bda calc-energy` contract caliber (electrolyte excluded, annotated) |
| Volumetric energy density | ≥ 880 Wh/L | stage2 | `bda calc-energy` (`energy_density_wh_l`, contract caliber volume = Σ layer thickness × area) |
| Max cell temperature (4C charge @45 °C) | ≤ 333.15 K (default red line, task silent) | stage3 | `run-pyamm 4C_charge_45C --thermal lumped` → `T_max_K` |
| Lithium plating (4C charge @45 °C) | none (`plated = false`) | stage3 | `anode_potential_v` min < 0 V → plated (mechanical) |

**Trade-off expectation (multi-objective):** low-T retention ↔ energy density is the central Pareto conflict.
−20 °C kills electrolyte transport (σ, D_Li fall toward zero; t⁺ 0.2594 baseline). Raising retention wants *thin electrodes / high porosity / small particles / high-conductivity electrolyte* — all of which sacrifice mass- and volume-energy density. The density targets (327.18 Wh/kg *and* 880 Wh/L simultaneously) instead want *thick, dense, low-porosity electrodes*. So the design search must first secure retention headroom, then re-add density among passers — not the reverse.
Secondary conflict: thicker electrodes raise 4C-charge heat (T_max) — but the task imposes no fast-charge requirement, so Stage 4 is a default gate, likely satisfiable at 10 W/m²/K baseline cooling.

## 2. Candidate strategy

- **Round 1 — baseline characterization (Chen2020, empty params):** 1C discharge (25 °C), lowT discharge (−20 °C), 4C charge @45 °C (lumped + plating), `calc-energy`. Establishes: baseline retention, baseline ED/vol-ED, DCR, T_max. Also the **opening ceiling assessment** data (below).
- **Opening ceiling assessment (with ceiling_escalation ON):** with contract formula and dumped Chen2020 geometry (pos 75.6 µm / neg 85.2 µm / sep 12 µm / CCs 16+12 µm; packing densities 3262/1657 kg/m³; porosities 0.335/0.25), the *mass* budget is already favorable (active fraction ≈ 64 % of layer mass). Best-possible architecture (thicker electrodes, thin separator/CC, optimal porosity) plus max-transport electrolyte is estimated against the 327.18/880 targets **after measuring baseline energy** (energy depends on the simulated discharge from the set's initial state, so the ceiling is anchored to measured energy, not nominal 5 Ah). If the density ceiling turns out below target → **proactively escalate to Stage 2** (system switch / additive design), per `ceiling_escalation`.
- **Round 2+ — retention first:** each round proposes 2–4 architecture/formulation variants (exploration_force ON), one per run-pyamm call, covering:
  - *Electrolyte formulation* (σ, D, t⁺ overrides via parameter bridge — the "cold-electrolyte formulation" design path; values from literature/domain estimates marked `estimate`; a scalar σ makes conductivity temperature-independent, which is the crude-but-real lever this model exposes),
  - *Architecture*: thinner electrodes (ionic path), higher porosity, smaller particle radii (solid path), separator thinning (density + transport), N/P control.
- **Once retention ≥ 95 % secured:** shift variants toward density recovery (thicker electrodes / lower porosity) while holding retention; passers get DFN-mode confirmation.
- **Escalation route** (if Architecture×Formulation plateaus below 95 %): Stage 2 molecular additive design (low-T electrolyte additives identified by molecular funnel) — only if the plateau is materially below target and ceiling analysis shows transport is the binding constraint.
- All candidates are compared against baseline in the same round via `bda log-evaluate` (batch mode, one entry per candidate).

## 3. Budget allocation

- Round 1 (baseline, 4 sims + calc-energy + derived retention): fixed.
- Rounds 2–6: formulation + architecture screening, 2–4 SPMe variants/round (≈ 12 variants).
- Rounds 7–9: density recovery + refinement, DFN confirmation of finalists.
- Round 10+: safety confirmation (DFN 4C), `final` entry, deliverables (design_spec, BOM, datasheet, calc, DVPR, DFMEA, delivery_index), `verify-deliverables`.
- Total ≈ 20–30 simulation calls (SPMe seconds-scale; DFN tens of seconds). `real_compute = false` → no true DFT/MD; `endorse` records the skip honestly.

## 4. Risk and fallback plan

- **R1: baseline retention catastrophically low (< 50 %)** — expected; validates the transport-first strategy. Low retention is the *known* behavior of generic electrolytes at −20 °C; the model's T-dependence lives mostly in electrolyte transport → formulation overrides are the highest-leverage move.
- **R2: retention plateaus < 95 % despite aggressive transport + architecture** → three-strike questioning (recorded in `final.escalation` if triggered): ① model/system assumption — is 95 % retention at −20 °C/1C physically reachable within Chen2020's fixed kinetic params (T-independent k, D_s)? If the model has no T-dependence outside the electrolyte, the retention ceiling is set by whatever T-dependence remains + OCP shifts, and the residual gap may be unreachable *in this model*; ② task boundary assumption — electrolyte formulation is within scope (widest interpretation recorded in entry 0); electrode system switch is also in scope; ③ metric assumption — unreachable → honest negative result with "reachable if X relaxed" statement; never threshold relaxation.
- **R3: ED/vol-ED fail while retention passes** → density recovery variants (thicker/denser electrodes, thin separator/CC); if the measured energy ceiling (best architecture) sits below 327.18 Wh/kg or 880 Wh/L → escalate to Stage 2 (system/cathode switch), per ceiling assessment.
- **R4: safety gate fails (plating/T_max)** → thicker electrodes are self-correcting levers for plating (more negative capacity buffer), cooling `h` raise is in-scope for T_max.
- **Simulation-failure handling:** SPMe solver errors → adjust protocol legality (per bda error message), DFN fallback is automatic; failures recorded verbatim, never swallowed.

## 5. References (domain basis — direction → source; no fabrication)

- Low-T electrolyte transport collapse & cold-electrolyte formulation levers (σ/t⁺/D as dominant −20 °C knobs) → domain experience (no precise source); direction consistent with charged-capacity loss attribution in PyBaMM Chen2020-family models.
- Thin electrodes / small particles raise cold-cranking power; thick low-porosity electrodes raise gravimetric+volumetric ED → standard Li-ion cell-design trade-off literature (e.g., battery manufacturing cell-design handbooks); domain experience.
- −20 °C 1C retention ≥ 95 % requires specialized low-T electrolytes (esters/FEC-rich/dual-salt) in real cells → industry low-temperature electrolyte reviews; precise sources not on hand → **domain experience (no precise source)**.
- Parameter bridge mapping (σ/t⁺/D → PyBaMM keys) → this skill's SKILL.md §1.5/§Parameter-bridge table (in-repo reference, real).
- Chen2020 parameter set identity → Chen et al. 2020, "Development of Experimental Techniques …" (PyBaMM distributed parameterization — in-repo library reference, real); discriminant anchor verified by dump (graphite OCP, no SiOx keys).

*Revision history: initial plan 2026-08-26 (this file). Plan updates are appended as plan-update entries in log.jsonl per protocol.*