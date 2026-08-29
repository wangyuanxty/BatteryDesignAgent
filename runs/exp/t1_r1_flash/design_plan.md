# Design Plan — VBF t1_r1_flash (next-generation BEV sedan battery)

**Case**: Design a battery for a next-generation pure electric sedan.
**Task (verbatim)**: energy density ≥ 392.61 Wh/kg · support 4C fast charge (no lithium plating) ·
maximum temperature ≤ 60 °C · overcharge to 4.7 V without triggering thermal runaway.

## 1. Objective decomposition (decision layers)

| Metric | Layer | Threshold (contract) | Lever set (adjustable DOFs) |
|---|---|---|---|
| `energy_density_wh_kg` | stage2 | **min 392.61** | architecture (electrode thickness, porosity, N/P, separator, current collectors, particle size) |
| `plated` (4C charge, 45 °C) | stage3 | **false** (`anode_potential_v` min ≥ 0 V) | electrode thickness ↓, electrolyte σ/t⁺/D ↑, negative particle radius ↓, N/P |
| `T_max_K` (4C charge, 45 °C amb.) | stage3 | **max 333.15** (=60 °C; only 15 K rise budget) | cooling coefficient h, DCR (geometry), electrolyte transport |
| `triggered` (overcharge to 4.7 V) | stage3 | **false** | cell mass (mcp), chemistry, cooling (run-tr mechanical) |

**Trade-off expectation**: ED vs 4C/T_max — thicker electrodes raise ED but increase anode overpotential
(plating) and heat generation (T_max). Cooling h and electrolyte transport help 4C/T_max with **no ED cost**
→ exploit them first. Thin collectors raise ED with negligible electrochemical side effects.

## 2. System determination

Task text names no explicit electrode system → anchor-table default would be Chen2020, but Chen2020 lacks a
complete thermal/geometry parameter set (T_max would rely on injected defaults → approximate, violating the
honest-thermal requirement of the stage-3 criteria). Electrode-system DOF is undeclared in the task → widest
interpretation (adjustable). **Baseline = OKane2022** (NMC811/graphite+SiOx, LG-M50-class EV chemistry with
complete thermal/geometry params, SEI + cracking models): canonical next-gen BEV chemistry; upper cut-off
4.2 V → overcharge protocol (+0.5 V) lands exactly on the task's 4.7 V. Recorded deviation from table
default, rationale above.

## 3. Candidate strategy

- **R1**: baseline OKane2022 full characterization (1C DFN + calc-energy; 4C charge lumped+plating;
  overcharge + run-tr) + 2 architecture ED probes: **Arch-A** thin current collectors, **Arch-B** thick
  positive + thin collectors.
- **R2 (routing by R1 failures)**: ED short → thickness/porosity push; plating → σ/t⁺/particle radius,
  thin negative; T_max → cooling h (pack-level lever, no ED cost); TR → mass/chemistry check.
- **R3**: full confirmation suite on the final candidate.

## 4. Budget allocation

R1 ≈ 7 sims · R2 ≈ 4–6 sims · R3 ≈ 4 sims. Total ≈ 15–17 cell sims, 0 molecular sims unless escalation to
Stage 2 fires. `real_compute: false` → closing skips true DFT/MD with honest endorse entry.

## 5. Risk and fallback plan

- **ED < 392.61 on stock OKane2022**: likely (conservative EV cell) → thin collectors + thickness push;
  opening ceiling assessment after R1; if architecture ceiling < target → **escalate to Stage 2** (material
  design: high-voltage cathode / additive).
- **4C plating at end-of-charge (high SOC)**: likely marginal at 4C on stock chemistry → electrolyte
  transport overrides (σ/t⁺), negative particle size; N/P rebalance.
- **T_max with default h=10**: hA = 0.053 W/K ⇒ ΔT ≫ 15 K expected → cooling h is the primary T_max lever
  (thermal-management DOF adjustable); also DCR reduction.
- **Overcharge TR**: mechanically judged by run-tr; if triggered → increase mcp (cell size), reduce
  overcharge heat (lower DCR), or revisit chemistry; do not hand-wave.
- **Three-strike**: 3 consecutive rounds with same cause → question assumptions (system reachability / task
  boundary / metric reachability) and record layer-by-layer in `final.escalation`.

## 6. References (directional basis; honesty constraint)

- OKane2022 parameter set (PyBaMM): NMC811/graphite+SiOx EV chemistry, complete thermal/geometry — anchor.
- Next-gen BEV energy-density push (300→400+ Wh/kg cell): high-Ni cathodes + Si-containing anodes →
  domain experience (no precise source).
- Fast-charge plating mitigation (high-σ electrolytes, small particles, thin electrodes) →
  domain experience (plating-review literature, no precise source).
- Pack-level liquid cooling effective heat-transfer coefficient ≫ 10 W/m²K →
  domain experience (no precise source).
