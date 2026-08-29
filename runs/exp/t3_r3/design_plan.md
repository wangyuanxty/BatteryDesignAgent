# Design Plan — t3: Power-Tool Battery (t3_r3)

Date: 2026-08-26 · CaseWorkspace: `runs/exp/t3_r3` · start_stage: 3 (cell design; no new-material objective) · real_compute: false

## 1. Objective decomposition (criteria contract, logged in log.jsonl entry 0)

| Metric | Threshold | Decision layer | Measurement |
|---|---|---|---|
| Nominal capacity | ≥ 2.0 Ah | stage2 | `1C_discharge` output `capacity_ah` |
| 5C discharge retention | ≥ 95 % | stage2 | 5C capacity ÷ same-parameter 1C capacity (mechanical) |
| Power density | ≥ 4000 W/kg | stage2 | `calc-energy` `power_density_w_kg` = V_OC²/(4·DCR)/mass |
| 4C fast charge plating | none | stage3 | `4C_charge_45C` `anode_potential_v` min ≥ 0 V |
| Max temperature | ≤ 60 °C (= 333.15 K) | stage3 | max of `T_max_K` over 5C discharge / 4C charge (lumped thermal) |

**Expected trade-offs (directional expectations to verify by simulation):**
- *Capacity ↔ 5C retention / power density:* thinner electrodes cut ionic±kinetic overpotential (retention ↑, DCR ↓, W/kg ↑) but cut 1C capacity → 5C retention, power density and ≥2 Ah must be held simultaneously. Chen2020 baseline: 5 Ah, 75.6/85.2 µm, ε=0.335/0.25 — expect retention ≪ 95 % at 5C in baseline; fix with thin/high-porosity/small-particle electrodes.
- *Power density ↔ mass:* collectors+separator are mass floor; thinned electrodes lower both DCR and mass (net gain), but over-thinning re-raises collector share and can drop capacity under 2 Ah.
- *4C plating ↔ N/P and negative kinetics:* smaller negative particles + higher electrolyte σ/t⁺ + moderate N/P suppress the anode-surface overpotential dip below 0 V; 45 °C ambient helps kinetics, hurts T_max.
- *T_max ↔ power design:* lower resistance (same levers as retention) cuts heat; cooling h is a separate thermal-management lever (contract default 10 W/m²/K, adjustable by widest interpretation).

## 2. Starting point and system mapping

- Task text names **no electrode system and no new material/additive/electrolyte-design objective** → per §0 rule: `start_stage: 3`.
- Per §1.5 anchor table, "no explicit electrode system → default Chen2020 with record": **Chen2020** (NMC811/graphite, aging+thermal-capable). Discriminant anchors verified in `dump_base.py`: nominal 5.0 Ah; positive 75.6 µm / ε 0.335 / ρ 3262 / r_p 5.22 µm; negative 85.2 µm / ε 0.25 / ρ 1657 / r_p 5.86 µm; t⁺ 0.2594; c_e0 1000 mol/m³; h=10; v-cuts 2.5–4.2 V (NMC811/graphite signature).
- All ablation switches ON (exploration_force / ceiling_escalation / funnel_voting); all five degree-of-freedom categories adjustable (widest interpretation, §0 zero-interaction rule).

## 3. Candidate strategy

- **Round 1 — baseline characterization (ceiling anchor):** Chen2020 with zero overrides; 1C discharge (SPMe quick-screen, DFN reference), 5C discharge (DFN, mandated for high rate), 4C charge 45 °C (lumped+plating), `calc-energy`. Result = entry-chemistry/architecture ceiling evidence for the gap assessment (written into the funnel log, §1 Stage 3 opening ceiling assessment).
- **Opening ceiling assessment:** best-architecture estimate of the NMC811/graphite system under thin electrodes/optimal porosity/small particles/transport-boosted electrolyte vs the five thresholds. Expected verdict (to confirm by simulation): 5C-retention≥95 % and ≥2 Ah are jointly reachable at reduced thickness (areal-capacity budget ≈ 2 Ah at ~35–50 µm positive depending on ε); power density levers scale as (κ·ε^1.5)/(L²(1−ε)ρ) → thin+porous helps strongly; plating responds to negative-side design. If assessment shows ceiling < objective (e.g. plating unreachable at 4C in the NMC811/Gr system), escalate to Stage 2: electrolyte transport formulation first (σ/t⁺/D), system switch (OKane2022 SiOx or LNMO.json 4.7-V class — the V² term directly boosts power density) only if architecture+formulation is exhausted.
- **Rounds 2+ — architecture exploration (exploration_force: 2–4 variants/round)** in the direction of decreasing DCR·mass product while holding capacity ≥ 2 Ah and N/P ≈ baseline parity: (a) electrode thinning + porosity raise (capacity-guarded), (b) particle-size reduction (positive & negative; T1 evidence: small particles measurably help high rate), (c) electrolyte transport overrides (σ ↑ 1.3 S/m class per high-conductivity formulation literature, t⁺ ↑ 0.4 class per LiFSI-rich/low-solvating designs — values as literature-sourced overrides, marked as such), (d) collector/separator slimming and cooling-h raise for T_max.
- **Plating fix order** (only if R1 shows plating): negative thin + small negative particles + N/P tune → electrolyte σ/t⁺ → system escalation. Symptom→scale routing: potential-window/transport → material scale; capacity/temperature/retention → architecture scale.

## 4. Budget allocation

- Round 1: 4 run-pyamm (1C SPMe + 1C DFN + 5C DFN + 4C lumped+plating) + 1 calc-energy + evaluate. Zero material-scale spend (start_stage 3).
- Exploration rounds: ≤ 4 rounds × 3 candidates × (1C SPMe + 5C DFN + 4C SPMe) + calc-energy; DFN reference re-run only for round finalists (proxy-first). ≈ 12–15 run-pyamm/round worst case.
- Closing: no true DFT/MD (real_compute=false → endorse records the skip honestly); deliverables + render.
- Stop rule: all five metrics pass, or budget/harness exhausted → honest `final` (negative result is a valid result).

## 5. Risk & fallback plan

| Risk | Symptom | Fallback (scale of cause) |
|---|---|---|
| 5C retention < 95 % | 5C/1C capacity ratio | Stage 3: thinner electrodes, ε ↑, particle ↓, electrolyte σ/t⁺ ↑ |
| Capacity < 2 Ah after thinning | 1C capacity_ah | Stage 3: re-thicken positive to areal-capacity floor; porosity/particle rebalance |
| Plating at 4C | anode_potential_v min < 0 | Stage 3 negative-side design → electrolyte formulation → Stage 2 system/escalation |
| T_max > 333.15 K | lumped T_max_K | Stage 3: resistance cut + cooling h raise (thermal-management DOF) |
| Power density < 4000 W/kg | calc-energy | Stage 3: DCR·mass product attack; verify against V² lever if system switch |
| Three identical-cause failures | 3 consecutive rounds | Three-strike questioning: (1) is the NMC811/Gr system reachable at 5C/4C under these bounds? (2) boundary: are electrolyte/cooling levers correctly inside scope (widest interpretation)? (3) metric feasibility; only then close as negative |

## 6. Domain references (real sources only; "domain experience" marks where precise source is not claimed)

- Chen, C.-H., Brosa Planella, F., O'Regan, K., Gastol, D., Widanage, W. D., Kendrick, E. (2020). Development of experimental techniques for parameterization of multi-scale lithium-ion battery models. *J. Electrochem. Soc.* 167, 080534. → Chen2020 parameter set used as `base`; initial discharged state (27 % lithiated cathode) explains low first-cycle capacity.
- O'Kane, S. E. J., et al. (2022). Lithium-ion battery degradation: how to diagnose it via multiscale modeling... *J. Electrochem. Soc.* 169, 060516. → plating/degradation modeling & the OKane2022-style plating parameter convention; system-switch fallback candidate.
- Gallagher, K. G., et al. (2016). Optimizing areal capacities through understanding the limitations of lithium-ion electrodes. *J. Electrochem. Soc.* 163, A138. → areal-capacity vs power trade-off basis for thinning strategy.
- Weiss, M., et al. (2021). Fast charging of lithium-ion batteries: a review of materials aspects. *Adv. Energy Mater.* 11, 2101126. → plating-suppression levers (negative particle size/N-P/electrolyte), 4C-charge directional basis.
- Newman, J., Tiedemann, W. (1975). Porous-electrode theory with battery applications. *AIChE J.* 21, 25. → the DCR·mass / areal-power scaling reasoning used in the ceiling assessment.
- High-conductivity/low-solvating electrolyte formulations raising effective σ and t⁺ (LiFSI-class): domain experience (no precise source); values used as explicitly literature-estimated overrides, not simulation output.
- LNMO 4.7-V-class spinel as high-voltage power-tool cathode direction: domain experience (no precise source); only activated if ceiling escalation is triggered and judged necessary.

## Revision history

- 2026-08-26 (v1): initial plan for t3_r3 (zero-interaction execution).