# Battery Design Plan — t1_r1_noforce (next-generation pure-electric-sedan cell)

Date: 2026-08-25 · Ablation: exploration_force OFF (free exploration) · real_compute=false · start_stage=3

## 1. Objective decomposition (thresholds verbatim from task text)

| Layer | Metric | Threshold | Protocol / tool |
|---|---|---|---|
| stage2 (cell performance) | gravimetric energy density | ≥ 392.61 Wh/kg | 1C discharge + `calc-energy` (contract stack-dry mass, electrolyte excluded) |
| stage3 (safety) | lithium plating @ 4C charge | none (`plated=false`) | `4C_charge_45C` lumped + plating, anode potential never < 0 V |
| stage3 (safety) | max cell temperature | ≤ 60 °C = 333.15 K | `4C_charge_45C` (45 °C ambient) `T_max_K` |
| stage3 (safety) | overcharge to 4.7 V | no thermal runaway (`triggered=false`) | `overcharge` (+0.5 V above cut-off) → `run-tr --sim` |

Expected multi-objective trade-offs:
- ED ↑ ⇔ thicker/low-porosity electrodes, thin collectors & separator ⇒ worsens 4C plating (long transport, high anode utilization) and raises T_max (more heat, less dissipation) — the central Pareto tension.
- Plating ↓ levers: smaller negative particle radius, higher electrolyte σ/t⁺, higher N/P, more porosity — all ED-costly or ED-neutral.
- T_max ↓ levers: cooling coefficient h ↑ (thermal DOF), lower cell resistance.
- Overcharge safety: mechanical judgment only (overcharge protocol + run-tr); a cool 4C design plus cathode-level headroom is the mitigation path.

## 2. Candidate strategy

- Base system: task text names no electrode system → anchor-table default **Chen2020** (NMC811/graphite baseline parameterization). Its 4.2 V upper cut-off + 0.5 V overcharge lands exactly on the 4.7 V spec.
- R1 baseline characterization: 1C discharge (SPMe screen → DFN precise), `calc-energy`, 4C_charge_45C (lumped+plating), overcharge + run-tr → gap to every criterion.
- Opening ceiling assessment (ceiling_escalation ON): probe the best-legal architecture+formulation on Chen2020 (ultra-thin collectors, thin separator, low-porosity thick electrodes, high-σ electrolyte, N/P 1.05, small particles, boosted cooling). If ceiling < 392.61 → **escalate to Stage 2 material design**: system switch to SiOx-bearing OKane2022 (higher anode capacity; cracking/aging model) or composition/additive candidates.
- Follow-up (exploration_force OFF — variants only at relevant moments): Pareto walk ED vs plating/T; every stage2-qualified candidate gets the full stage3 safety exam (4C + overcharge).

## 3. Budget allocation

- R1 baseline + R2 ceiling probe: 2 rounds.
- R3–R6: ED maximization (Chen2020, then escalated system if needed).
- R7–R9: safety fine-tuning (plating margin, T_max, overcharge margin).
- Closing: deliverables + render + verify-deliverables (no true compute, real_compute=false).

## 4. Risk and fallback plan

- ED unreachable in Chen2020 architecture space → escalate (Stage 2): SiOx system switch; LNMO high-voltage path excluded (its overcharge window would not match the 4.7 V spec); composition candidates as last resort.
- 4C plating on thick electrodes → negative particle radius ↓, electrolyte σ/t⁺ ↑, N/P ↑ (accept ED cost).
- T_max > 333.15 K → cooling h ↑ + resistance reduction.
- Chen2020 has no complete thermal/geometry/plating parameter set → run-pyamm injects defaults (traced via `injected_defaults`); safety judgments on Chen2020 are marked "approximate (default injection)" — a reason to prefer a full-parameter system for the final design if escalation occurs.
- Three-strike rule: 3 consecutive same-cause failures → question system/boundary/metric assumptions (plan-update entry + final escalation record), never a blind 4th retry.

## 5. References (domain basis; real sources only)

- NMC811/graphite baseline parameterization → C.-H. Chen, F. Brosa Planella, K. O'Regan, D. Gastol, W. D. Widanage, E. Kendrick, "Development of Experimental Techniques and Parameterization of a Physically Based Li-ion Battery Model", J. Electrochem. Soc. 167, 080534 (2020).
- SiOx anode raises cell energy → M. N. Obrovac, V. L. Chevrier, "Alloy Negative Electrodes for Li-Ion Batteries", Chem. Rev. 114, 11444 (2014).
- Fast-charge plating limits & mitigation (electrode loading, transport, particle size) → A. M. Colclasure et al., "Requirements for Enabling Extreme Fast Charging of High Energy Density Li-Ion Cells while Avoiding Lithium Plating", J. Electrochem. Soc. 166, A1412 (2019).
- Electrode areal-loading limits → K. G. Gallagher et al., "Optimizing Areal Capacities through Understanding the Limitations of Lithium-Ion Electrodes", J. Electrochem. Soc. 163, A138 (2016).
- SiOx cracking/aging model parameterization → S. E. J. O'Kane et al., "Lithium-ion battery degradation: how to model it", Phys. Chem. Chem. Phys. 24, 7909 (2022).
- Electrolyte transport (σ/t⁺) as plating lever → domain experience (no precise source).

## Revision history

- 2026-08-25: initial plan (entry 0 + plan entry).
