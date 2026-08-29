# Design Plan — t5_r1_singlemodel (Next-Generation Flagship Vehicle Battery)

Case ID: t5_r1 (workspace `runs/exp/t5_r1_singlemodel`)
Ablation: **funnel_voting OFF** (molecular screening = run-mlp(mace) only; hard elimination lines apply; no three-model voting / no disputed concept). exploration_force ON, ceiling_escalation ON, real_compute = false.

## 1. Objective decomposition (parsed from task text, thresholds verbatim)

| Decision layer | Metric | Threshold | Tool source |
|---|---|---|---|
| stage1 (molecular) | mace relaxation energy_ev | ≤ 0.0 eV, converged=true (hard elimination; HOMO line unavailable — xtb not run under funnel_voting OFF) | run-mlp(mace) |
| stage2 (cell) | energy density | ≥ 500.94 Wh/kg | calc-energy (contract formula) |
| stage3 (safety) | lithium plating at 4C charge (45 °C) | plated = false (anode_potential_v ≥ 0 V at all times) | run-pyamm 4C_charge_45C --plating |
| stage3 (safety) | maximum cell temperature | ≤ 60 °C = 333.15 K | run-pyamm 4C_charge_45C T_max_K (thermal lumped) |

Multi-objective trade-off map:
- **ED vs 4C plating**: thick/high-loading electrodes raise ED but worsen rate capability and plating margin.
- **ED vs T_max**: mass cuts (thin collectors/separator) raise ED but reduce lateral heat spreading; low porosity raises active fraction but adds ohmic heat.
- **T_max vs plating**: both relieved by electrolyte transport (σ/D/t⁺) and particle size; cooling h is a pure T_max lever with zero ED cost (thermal-management DOF).
- Expected Pareto: push ED via mass cuts + material upgrades; hold safety via electrolyte formulation + particle size + cooling h.

## 2. Candidate strategy

1. **Round 1 — baseline + system probe (Stage 3 start)**: task text names no explicit electrode system → anchor-table default Chen2020 (NMC811/graphite). Characterize baseline (1C discharge SPMe→DFN, calc-energy, 4C_charge_45C safety). In parallel, propose system candidate OKane2022 (same NMC811/graphite geometry in this library build, but native plating/stripping + cracking + SEI-on-cracks parameters — the better 4C-plating judgment vehicle) and two architecture probes: (a) ED-max probe — thin current collectors + thin separator + porosity cuts; (b) 4C-safety probe — high-transport electrolyte bridge + small particles + raised cooling h.
2. **Opening ceiling assessment (after round 1)**: estimate NMC811/graphite ED ceiling in this virtual geometry (aggressive mass cut + transport) vs 500.94 Wh/kg. Gap → **ceiling_escalation (ON) into Stage 2 material design**: high-voltage LNMO system (4.7 V OCP, own parameter set `data/LNMO.json`), electrode-composition candidates via run-comp (CHGNet, CUDA env) for higher-capacity/higher-voltage cathodes, electrolyte additive molecules via run-mlp(mace)-only funnel.
3. **Stage 3/4 iteration**: 2–4 architecture variants per round (exploration_force ON): thickness/porosity/N/P, separator, current collectors, particle size; safety exam (4C_charge_45C + plating) on every candidate; evaluation via `bda log-evaluate` (mechanical verdict).
4. **Final material integration**: best material property set (bridge: σ/D/t⁺, particle size, voltage/capacity params) + best architecture, then DFN-precision confirmation of all three criteria.

## 3. Budget allocation

- Rounds 1–2: baseline + ceiling assessment + system selection (4–6 sims/round).
- Rounds 3–6: ED push — material escalation (run-comp batch, ~1 GPU-hour) + architecture mass cuts.
- Rounds 7–10: safety fine-tuning — 4C plating margin and T_max via formulation bridge + cooling.
- Round 11+: DFN confirmation, deliverables, render, verify-deliverables.
- Simulation budget discipline: SPMe screens (seconds), DFN for passers and all 4C safety judgments; calc-energy on every discharge candidate.

## 4. Risk and fallback plan

| Risk | Fallback (symptom → scale) |
|---|---|
| A. ED < 500.94 even after architecture push | ceiling gap → Stage 2 escalation: LNMO high-voltage system; run-comp composition candidates (high-Ni / Li-rich cathodes) → self-built parameter set (constant-OCP approximation); electrolyte excluded from mass already (contract formula) |
| B. 4C plating (anode potential < 0 V) | architecture + electrolyte transport (Stage 3 + bridge): raise σ/D/t⁺ (formulation), halve particle radii, thin electrodes, raise N/P; OKane2022 native plating model for judgment |
| C. T_max > 333.15 K | cooling h escalation (thermal-management DOF, default 10 → 25–60), σ↑ (ohmic heat ↓), particle size ↓ (kinetic heat ↓) |
| D. Chen2020 plating params are injected defaults | prefer OKane2022 (native plating) for final safety judgments; annotate source honestly |
| E. Three strikes on same failure cause | question model/system (is NMC811/graphite reachable?), task boundary (all five DOF categories already widest), metric (record "reachable if X relaxed to Y") → direction change or honest negative result |

## 5. References (domain basis; real sources only)

- NMC811/graphite baseline parameterization and SEI/cracking physics: Chen et al., J. Electrochem. Soc. 167, 080534 (2020); O'Kane et al., J. Electrochem. Soc. 169, 090501 (2022) — the Chen2020/OKane2022 PyBaMM parameter sets.
- Simulation framework: Sulzer et al., J. Open Res. Softw. 9, 14 (2021) (PyBaMM).
- High-energy cathode directions (high-Ni/Li-rich) and high-voltage spinel: Nitta et al., Materials Today 18, 252 (2015); Manthiram et al., Energy Environ. Sci. 7, 1339 (2014) (LNMO perspective).
- Fast-charge plating mitigation via electrolyte transport and particle size: domain experience (no precise source); consistent with OKane2022 plating-exchange-current parameterization.
- Thin-collector/thin-separator mass-reduction ED levers: industry practice, domain experience (no precise source).

## Revision history
- v1 (2026-08-25): initial plan.
