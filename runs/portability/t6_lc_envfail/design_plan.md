# Design Plan — Smartphone Battery (case t6_lc)

## 0. Task (verbatim thresholds)
- Volumetric energy density ≥ 950 Wh/L
- 4C fast charge with no lithium plating (anode surface potential never < 0 V)
- Maximum temperature ≤ 50 °C (323.15 K) during 4C fast charge
- Anode SEI thickness ≤ 500 nm after 100 cycles (1C/1C aging)
- Voltage plateau ≥ 4.1 V (discharge midpoint voltage)

## 1. Objective decomposition (decision layers)
| Metric | Threshold | Decision layer | Priority | Expected trade-off |
|---|---|---|---|---|
| Voltage plateau | ≥ 4.1 V (midpoint_voltage_v) | stage2 (cell) | hard gate | Forces high-voltage cathode (LNMO 4.7 V class; NMC811 ≈3.6 V fails) |
| Volumetric ED | ≥ 950 Wh/L | stage2 (cell) | hard gate | Favors thick/dense electrodes → conflicts with 4C plating & heat |
| SEI thickness @100cyc | ≤ 500 nm | stage2 (cell, aging) | hard gate | Favors SEI-suppressing coating/electrolyte |
| Max temperature @4C | ≤ 50 °C (323.15 K) | stage3 (safety) | hard gate | Favors thin electrodes, high cooling h |
| Lithium plating @4C | plated = false | stage3 (safety) | hard gate | Favors thin electrodes, high-σ electrolyte, small particles |

**Central Pareto tension**: volumetric ED (thick, dense, low-porosity electrodes) vs 4C plating/heat (thin electrodes, low loading). Strategy: maximize ED on the LNMO high-voltage platform, then fight plating/heat with transport/thermal levers rather than electrode thickness alone.

## 2. Starting-point determination
- Task names **no** new material/additive/electrolyte and no electrode system → `start_stage = 3` (cell design).
- Deterministic base: **Chen2020** (task text has no explicit electrode system), recorded in log entry 0.
- Opening ceiling assessment (ceiling_escalation ON) will be executed at baseline characterization: Chen2020 (NMC811/graphite) discharge midpoint ≈ 3.6 V < 4.1 V ⇒ voltage-plateau requirement is **unreachable in architecture space** ⇒ escalate to **Stage-2 System candidate** `LNMO.json` (4.7 V-class spinel, cell midpoint ≈ 4.17 V; anchor: LNMO.json `Upper voltage cut-off [V]` = 4.7, `Positive electrode OCP` = lnmo_ocp 4.7 V-class).

## 3. Candidate strategy (first round)
1. **Baseline characterization (Chen2020)**: 1C discharge (SPMe→DFN) + `calc-energy` → measure actual plateau/ED/DCR; confirms the NMC811 plateau gap (expected fail on ≥4.1 V) and provides the ceiling-assessment evidence.
2. **System switch candidate**: `{"base": "<path>/LNMO.json", "name": "systemLNMO", "role": "4.7 V-class high-voltage cathode to meet plateau ≥ 4.1 V"}` (System candidate: skips molecular funnel, direct Stage-3 simulation).
3. **Architecture variants (exploration_force ON, 2–4/round)** on the LNMO system tuned for the ED-vs-plating Pareto: electrode thickness / porosity / N-P ratio / separator thickness-porosity / particle radius.
4. **Electrolyte formulation** (high-σ / high-t⁺ transport overrides) to suppress plating at 4C.
5. **SEI suppression** (if SEI > 500 nm appears): electrode-modification candidate (SEI kinetic rate constant ↓) compared on the same system.

## 4. Budget allocation
- R1 baseline + ceiling assessment: 1 round.
- R2–R6: LNMO system bring-up + architecture exploration (ED/plateau).
- R7–R10: 4C safety fine-tuning (plating + T_max) + SEI aging.
- R11+: fallback/adjudication; Stage-5 true compute **skipped** (`real_compute = false`).

## 5. Risk & fallback plan
- **Plateau**: if LNMO midpoint < 4.1 V → no architecture fix possible → escalate to other high-voltage cathode parameter set; if none → honest negative result on plateau.
- **ED 950 Wh/L**: very aggressive for LNMO (lower volumetric capacity than NMC); fallback = raise active-material volume fraction / thin current collectors / thin separator (all architecture). If still short → honest negative result with "closest achievable ED" recorded.
- **4C plating / T_max**: fallback = thinner electrodes, higher electrolyte conductivity, smaller particle radius, higher cooling h. If plating persists at all feasible architecture → boundary questioning (three-strike rule).
- **SEI 500 nm**: fallback = SEI-kinetics suppression (coating) on the **same** LNMO/Chen2020 system; cross-system SEI comparison is invalid.

## 6. References (domain basis)
- High-voltage spinel cathode raises plateau to 4.7 V class and cell midpoint ≈4.17 V → bda anchor table `LNMO high-voltage cathode / spinel (4.7 V)` (skill `references/` + `scripts/bda/simulators/data/LNMO.json`).
- High-conductivity / high-transference electrolyte mitigates Li plating under fast charge → transport-parameter literature (domain experience, no precise source).
- SEI kinetic rate constant reduction lowers 100-cycle SEI thickness → SEI growth model in Chen2020/OKane2022 parameterizations (skill Stage-3 aging protocol; measured signal-scale: Chen2020 SEI kinetics ×0.1 → 449→385 nm).
- Smaller particle radius improves high-rate capability → OKane2022/Chen2020 particle-size keys (domain experience).

## Revision history
- 2026-08-26 v1: initial plan (headless, zero-interaction).
