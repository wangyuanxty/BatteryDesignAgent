# Design Plan — t6_r1: Smartphone Battery (≥950 Wh/L, 4C no-plating, ≤50°C, SEI ≤500 nm, plateau ≥4.1 V)

## 1. Objective decomposition (decision layers, thresholds verbatim from task)

| Layer | Metric | Threshold | Tool / output key |
|---|---|---|---|
| stage1 (molecular) | elimination lines (defaults; system candidates skip the funnel) | energy_ev ≤ 0.0 eV, HOMO ≤ −6.0 eV | run-mlp / run-xtb (not exercised unless molecular additives are proposed) |
| stage2 (cell) | volumetric energy density | ≥ 950 Wh/L | calc-energy `energy_density_wh_l` (contract formula, electrolyte excluded) |
| stage2 (cell) | voltage plateau | ≥ 4.1 V | calc-energy `midpoint_voltage_v` (discharge-time midpoint) |
| stage2 (cell) | anode SEI thickness after 100 cycles | ≤ 500 nm | run-pyamm `aging_1C_100cyc` `sei_thickness_nm_end` |
| stage3 (safety) | 4C fast charge, no lithium plating | plated = false | run-pyamm `4C_charge_45C --plating` (min `anode_potential_v` ≥ 0 V) |
| stage3 (safety) | maximum temperature | ≤ 50 °C = 323.15 K | run-pyamm `4C_charge_45C --thermal lumped` `T_max_K` |

Parsed under the skill's zero-interaction rule; recorded in log.jsonl entry 0 (contract, not post-hoc revisable).

## 2. Key determinations

- **Electrode system / base mapping**: task text names no system → anchor-table default **Chen2020** (recorded). The plateau ≥ 4.1 V metric is physically unreachable by NMC811-class cathodes (anchor: NMC811 cell midpoint 3.61 V) → deterministic switch to the high-voltage **LNMO library parameter set** (`scripts/bda/simulators/data/LNMO.json`, 4.7 V-class spinel; runner merges Chen2020 base + JSON overrides). Discriminant verified by numeric dump (lnmo_ocp bulk plateau ≈ 4.40–4.45 V).
  - *Honest caveat recorded in entry 0*: several LNMO.json keys use parameter names the installed pybamm 26.7.1 Chen2020 set does not read (max concentration, molar mass, stoich limits stay Chen2020 values). Effective behavior is judged from simulation output only.
- **start_stage = 2**: the objective requires a new material (high-voltage cathode) → Stage 2 with a **system candidate** (system candidates skip the molecular funnel and go directly to Stage 3 simulation).
- **Degrees of freedom** (not declared in task → widest interpretation, recorded in entry 0 `meta.freedoms`): electrode system, electrolyte formulation, electrode modification, cell architecture, thermal management — all **adjustable**. Excluded levers per protocol: solid-phase σ/D, initial lithiation, initial SEI thickness, charge cut-off voltage.
- **real_compute = false** (default): Stage 5 true-compute endorsement skipped, recorded honestly.
- **Aging**: 100 cycles (task text), isothermal SEI ec-reaction-limited protocol.

## 3. Candidate strategy

1. **R1 — baseline characterization (ceiling assessment)**: Chen2020 default 1C discharge (evidence: plateau infeasibility → material bottleneck) + **systemLNMO** 1C discharge; both SPMe, both calc-energy. Evaluation via `bda log-evaluate` (mechanical verdicts).
2. **R2–R6 — architecture optimization on LNMO** (2–4 variants/round, each a candidate):
   - anode thickening to restore N/P ≈ 1.1 (default geometry is anode-limited: usable ≈ 3.84 vs nominal 4.38 mAh/cm²);
   - separator 12 → 8 µm; current collectors 16/12 → 10/8 µm;
   - cathode thickness optimization (shifts the sto window into the higher-OCP region of the LNMO curve);
   - porosity reduction; negative particle radius for rate capability.
   - SPMe quick-screen → DFN for passers.
3. **R7 — aging**: `aging_1C_100cyc` on the best stack → `sei_thickness_nm_end` vs 500 nm (Chen2020-family measured reference ≈ 449 nm; coating lever `SEI kinetic rate constant [m.s-1]` in reserve).
4. **R8–R11 — Stage 4 safety**: `4C_charge_45C --thermal lumped --plating`.
   - plating → fallback Stage 3 (N/P ↑, negative particle radius ↓), then Stage 2 formulation (σ/t⁺ up);
   - T_max > 323.15 K → thermal management lever (`Total heat transfer coefficient` ↑), plus polarization reduction (electrolyte σ).
5. **R12+ — final confirmation**: winning stack at DFN (1C + 4C + aging), then closing (endorse-skip, final, render, deliverables).

## 4. Budget allocation

≈ 12–15 rounds. SPMe for screening (seconds); DFN for passers/final (minute-scale); aging ≈ seconds per 100 cycles; no true compute. Fallbacks consume from the same pool — architecture space gets ~5 rounds, safety gets ~4, buffer ~3.

## 5. Risk & fallback plan

| Risk | Trigger | Fallback / escalation |
|---|---|---|
| 950 Wh/L above LNMO/graphite stack ceiling | 3 consecutive architecture rounds without progress | escalate Stage 2 (electrolyte transport → higher voltage utilization); then three-strike questioning (system → boundary → metric reachability), honest negative result if unreachable |
| Plating at 4C | min(anode_potential_v) < 0 V | Stage 3: N/P ↑, negative particle radius ↓ → Stage 2: σ/t⁺ (literature values) |
| T_max > 323.15 K (only 5 K headroom at 45 °C ambient) | T_max_K > 323.15 | thermal h ↑ first; heat-gen ↓ (σ ↑, polarization ↓); if unreachable at plausible smartphone h → question operating-condition assumption, record honestly |
| midpoint < 4.1 V (thin margin vs ~4.17 anchor) | midpoint_voltage_v < 4.1 | polarization reduction (same levers as ED direction — keep low-porosity/thick electrodes in balance) |
| SEI > 500 nm | sei_thickness_nm_end > 500 | anode current-density ↓ (thicker anode), coating lever (SEI kinetic rate constant, estimate-marked) |

**Three-strike rule armed**: same-cause failure ×3 → stop blind tuning, question layer by layer (model/system → task boundary → metric reachability), record in `final.escalation`. No threshold relaxation; negative results reported honestly.

## 6. References (directional basis; no fabricated citations)

- High-voltage LNMO spinel OCP → `scripts/bda/simulators/data/LNMO.json` docstring (literature-calibrated: Markovsky/Duncan 4.7 V plateau) + skill anchor table.
- SEI ec-reaction-limited kinetics signal scale (449 nm / 100 cycles reference) → skill SKILL.md (measured reference).
- Extreme fast charge without plating (N/P, particle size, transport) → Colclasure et al., J. Electrochem. Soc. 166 (2019) A1412.
- Electrolyte transport values (σ ≈ 1.0–1.6 S/m LiPF6/LiFSI carbonate) → Valøen & Reimers, J. Electrochem. Soc. 152 (2005) A882 + domain experience.
- Ultra-thin separator / current collectors smartphone practice → domain experience (no precise source).
