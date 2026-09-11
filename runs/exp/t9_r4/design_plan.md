# t9_r4 — Design Plan (Stage 1)

Grid-storage cell on the Chen2020 NMC811/graphite profile. Cathode composition is the free
variable; electrolyte (EC/EMC + LiPF6) and cell architecture are frozen. Headless contract,
t9_r4, 2026-09-10.

## Objective decomposition

| Layer | Criterion | Threshold (verbatim) | Tool / source |
|---|---|---|---|
| stage1 (molecular) | computed average voltage | >= 4.6 V | run-comp (CHGNet) |
| stage1 | charging potential | <= 4.8 V (anodic limit of fixed electrolyte) | computed profile (same CHGNet machinery) + literature plateau |
| stage1 | outside documented catalogue | not one of the 115 documented materials | comp_envelope_check.py --formula |
| stage1 | outside known-set hull | point outside convex hull of the 102 points (V,C,stab) | comp_envelope_check.py --point |
| stage1 | supported family | one of the six frameworks (strict dispatch) | run-comp |
| stage2 (cell) | energy density at 1C discharge | >= 327.18 Wh/kg (calc-energy, contract convention) | run-pyamm 1C + calc-energy |
| stage2 | ED_active | report V x C x 0.9 | mechanical from run-comp |
| stage3 (safety/aging) | no Li plating at 4C charge 45 C | anode_potential_v stays > 0 | run-pyamm 4C_charge_45C --plating |
| stage3 | no thermal-runaway trigger at 4C/45C | triggered == false | run-tr from the 4C output |
| stage3 | SEI after 100 x 1C cycles | <= 500 nm | run-pyamm aging_1C_100cyc |
| guard | true voltage >= 4.6 beyond the proxy | experimental / own QE / literature-consistent | run-qe (attempt) + literature |

Cell mapping (fixed rule): constant OCP = computed average voltage; capacity = 0.9 x computed
capacity; SEI kinetics = Chen2020 baseline k0 (a cathode composition does not change SEI).

## Decisive feasibility analysis (this drives the candidate strategy)

1. **Baseline measured this session**: Chen2020 1C discharge 4.948 Ah, 17.39 Wh, mass
   0.04345 kg -> **ED = 400.29 Wh/kg** (calc-energy). Midpoint 3.935 V.
2. **ED for a mapped candidate** ≈ V_avg x C_cell / M_total with M_total ≈ 0.0435 kg and
   C_cell = 0.9 x C_comp x M_am (M_am ≈ 5.16e-6 x ρ_am).
3. **Family capacity bounds** (C_comp = 0.7 Li x F/3.6 / MW, the tool's definition):
   layered LiMO2: 180-224 mAh/g (3d TM MW 45-65); olivine: <= 128 (Sc, no redox; Ti 125.3);
   spinel: <= 113; tavorite sulfate/phosphate: <= 111; NASICON: <= 46.
4. **Non-layered families are ED-infeasible**: even the best case (olivine, C=128, V=4.8)
   gives ED ≈ 4.8 x 0.9 x 128 x 0.0253 / 0.04345 ≈ 322 < 327.18; realistic high-voltage
   olivines (C≈117) give ≈ 294; spinels (C≈103) ≈ 259; tavorites ≈ 250; NASICON ≈ 115.
   -> **The candidate must be a layered LiMO2** (C_comp >= ~180), where ED at V=4.6-4.8 is
   ≈ 445-465 Wh/kg, clearing 327.18 with >= 35 % margin.
5. **Layered voltage gap**: the known set's layered band tops at 4.029 V (NiMnMA). The
   [4.6, 4.8] x [180, 200] region of (V, C, stab) is empty in the 102-point hull -> a
   layered candidate landing there is expected outside the hull (adjudicated mechanically).
6. **Chemistry for a 4.6-4.8 V layered oxide**: Cu3+/Cu2+ layered oxides (LiCuO2-class)
   delithiate at ~4.5-4.8 V vs Li/Li+ (documented family: Li2CuO2/LiCuO2/NaCuO2 studies,
   Arai et al., Solid State Ionics 1998 — Cu-based layered oxides as high-voltage cathodes;
   the exact citation to be verified in the closing report). Fe3+/Fe4+ layered (LiFeO2)
   sits lower (~4.0-4.5 V). Ni-rich layered computes <= ~3.9-4.0 (measured in the known
   set) — insufficient. Cu is also light enough to keep C_comp ≈ 183 (MW 102.5).
7. **Charging potential**: computed as the incremental potential into the top-of-charge
   state (x: 0.4 -> 0.3) with the same CHGNet machinery (workspace profile script);
   the cell's upper voltage cut-off is set to 4.8 V (the declared limit).
8. **True-voltage guard**: primary = run-qe (own QE, Li-metal reference, same voltage
   definition) if budget allows; secondary = literature-consistent evidence (4.5-4.8 V
   Cu-oxide cathodes documented). A computed-only claim would not pass; the layered family
   is not an overestimate-prone family (NMC811 self-calibration 3.802 vs 3.8 V).
9. **Safety/aging expectations**: SEI kinetics baseline (untouched) -> 100-cycle SEI is the
   Chen2020 baseline behavior (measured signal-scale ~449 nm < 500 nm; to be confirmed with
   the mapped cell). 4C current = 4 x nominal capacity; nominal ≈ 4.17 Ah (layered Cu) vs
   5.0 Ah baseline -> lower C-rate stress than the baseline at the same 4C multiplier.
   Thermal: constant OCP -> zero entropic heat; lumped thermal, h = 10 (contract default).
   TR trigger checked mechanically via run-tr.

## Candidate strategy

- Round 1 (in flight): 14 layered candidates — LiCuO2, LiFeO2, Cu/M/Ni/Co/Fe 50:50 mixes,
  Cu0.9Al0.1, Cu0.9Zr0.1, Cu0.75Mn0.25, Cu0.8Ni0.2, LiVO2. Goal: find the family/element
  that pushes CHGNet layered voltage into [4.6, 4.8].
- Round 2: refine around the winner (dopants/stabilizers, margin on V and on C), screen
  enough neighbors to bracket the [4.6, 4.8] band; envelope-check all finalists.
- Round 3: charging-potential profile for the finalist (x = 0.3...1.0 incremental
  potentials) + hull/membership adjudication.
- Stage 3/4: cell mapping (constant OCP, 0.9 x C, baseline SEI, 4.8 V upper cut-off) ->
  1C discharge + calc-energy -> 4C_charge_45C (plating, thermal) + run-tr -> aging 100 cyc.
- Stage 5: run-qe finalist (true-voltage guard) if budget allows; replay of run-comp and
  envelope script; public-catalogue search record; deliverables.

## Budget allocation

- run-comp: ~3 batches x ~14 candidates (GPU, ~10 min each).
- Profile script: 8 states x 1 relaxation (GPU).
- run-pyamm/calc-energy/run-tr: ~10 runs (seconds-minutes each).
- run-qe: finalist only, CPU-scale (attempt; may not complete within budget — recorded
  honestly if not).
- Deliverables + render at closing.

## Risk and fallback plan

- R1: no layered candidate computes >= 4.6 V -> widen the TM space (Cr-, Ag-, V-Cu mixes,
  Co-rich high-voltage dopings) in one more batch; if the layered band is provably capped
  < 4.6, the contract is infeasible (non-layered ED-infeasible) -> honest negative result
  with layer-by-layer questioning.
- R2: computed charging potential > 4.8 V for the finalist -> compositional adjustment
  (dilute the high-voltage element) or reject and pick the next candidate.
- R3: ED below 327.18 for the mapped cell -> contradiction with the analysis above; recheck
  the mapping (density/molar-mass overrides) before anything else.
- R4: 4C plating or TR trigger -> same cell (fixed architecture) means the candidate's
  capacity/V is the only lever; verify nominal-capacity scaling; if still failing, negative.
- R5: run-qe too slow / fails to converge -> record honestly; the guard then rests on the
  literature-consistency evidence only, and the report must say so.

## References (domain basis, directional; no fabricated citations)

- Cu-based layered oxides as 4.5-4.8 V cathodes -> Arai et al., Solid State Ionics (1998)
  Li2CuO2/LiCuO2/NaCuO2 electrochemical study (to be verified at closing).
- 4.6-4.8 V cycling cathodes exist: LiNi0.5Mn1.5O4 (4.7 V), LiCoPO4 (4.78 V), LiCoMnO4 —
  task text itself.
- CHGNet screening calibration: task-provided calibration table (olivine Fe 3.443 vs 3.4;
  spinel/V families compute low; Ni-rich olivines inflated; layered NMC811 3.802 vs 3.8).
- Chen2020 parameter set + LNMO.json high-voltage mapping precedent (bda data dir).
- Plateau-OCP discharge in the fixed cell is anode-limited (measured this session with the
  LNMO.json base: 5.11 Ah) — the mapped cell inherits this fixed-cell behavior; labeled
  honestly in the report.

## Revision history

- 2026-09-10 (initial): plan written before round 1 results.
- 2026-09-10 (direction change, after round 2): d0/d10 O-redox layered line sits at the
  window edge (LiAlO2 4.598 V); round 3 refines the B-Al d0 system.
- 2026-09-10 (closing): honest negative result. The only window pass (AlB55 4.6413 V)
  fails the charging-potential gate at 7.410 V (limit 4.8 V); the pass was the signature
  of a pathological x=0.3 endpoint, fatal for the whole d0/d10 line. TM-redox layered caps
  ~4.0 V; non-layered families ED-infeasible under the 0.9-capacity rule. Nothing reported
  as passing. Final entry (verdict: negative) closes the audit; deliverables verified ALL
  PASS.
