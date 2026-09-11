# t10_r3 — Grid-storage cell additive design (T10 v3 contract)

Date: 2026-09-10. Workspace: runs/exp/t10_r3.

## Contract summary

- Cell: Chen2020 NMC811/graphite profile. Architecture, electrolyte base, transport,
  kinetic parameters, SEI baseline k0 all FIXED. Only the additive molecule may change.
- Targets:
  1. Envelope: computed point (E_mace/atom, E_chgnet/atom, HOMO_xTB) OUTSIDE convex hull
     of the known set (87 pts: 82 documented + 5 from previous run). Hull ref:
     runs/exp/known_set_sei/envelope_stats_v2.json. Adjudicated by
     runs/exp/known_set_sei/envelope_check.py.
  2. Family gate: families_matched empty (families: nitrile, S=O, ester, carbonate,
     aromatic ring, dialkyl ether, B, Si, amide, nitro, quinone, P3 phosphite, P5 phosphate).
  3. Property window: xTB HOMO <= -13.74 eV.
  4. Cell window: SEI <= 370 nm after 100 cyc 1C; energy density >= 327.18 Wh/kg
     (calc-energy convention); no thermal-runaway trigger under 4C charge at 45 C.
  5. Fixed mapping (no free parameters): k(M) = k0 * 10^((HOMO_xTB + 12.5)/1.0),
     k0 = Chen2020 baseline = 1e-12 m/s. Calibrated on two simulated points:
     k=k0 -> 449.12 nm, k=0.1*k0 -> 385.10 nm. Extrapolation below 0.1x is an
     assumption and must be reported as such.
- Known-set geometry fact: hull min over vertices = -14.2961 eV (bis(trifluoromethyl)sulfone),
  so any candidate with xTB HOMO < -14.2961 eV is guaranteed outside the hull.

## Candidate strategy (as executed)

Panel (all perfluorinated, no O/aromatic/B/Si/P/C#N/C=O): perfluorotributylamine (FC-43),
perfluorohexane, perfluorotriethylamine, perfluoropentane, tris(trifluoromethyl)amine,
sulfur hexafluoride (probe). See funnel_summary.json for all numbers.

## Results (final)

- **FINAL: perfluorotributylamine (FC-43, CAS 311-89-7)** — cataloged industrial
  fluorinert liquid, bp 178 C.
  SMILES FC(F)(F)C(F)(F)C(F)(F)C(F)(F)N(C(F)(F)C(F)(F)C(F)(F)C(F)(F)F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F
- Funnel: mace -224.632431 eV (conv true), chgnet -236.717163 eV (conv false, screening
  precision), xtb HOMO -14.9642 eV.
- Envelope: in_envelope=false (point [-5.615811, -5.917929, -14.9642]; hull min HOMO
  -14.2961). Family gate: families_matched=[].
- Mapping: k = 1e-12 * 10^(-2.4642) = 3.4340e-15 m/s (0.003434x k0) -> params_pfta.json.
- Cell: SEI 162.52 nm (<=370) | ED 400.29 Wh/kg (>=327.18) | 4C/45C T_max 332.35 K,
  run-tr triggered=false.
- Calibration replicated: 449.116 nm (k0) / 384.960 nm (0.1x) vs contract 449.12/385.10.
- Window-edge check: k(-13.74)=5.7544e-14 -> SEI 366.87 nm <= 370. Consistent.
- Panel all pass gates; ncf3 deepest (-15.7893, SEI 38.99 nm) but gaseous at RT;
  pfpent -15.0496 (SEI 143.74 nm), pfhex -14.9147 (173.78), pftea -14.8818 (181.36).
  sf6 eliminated (HOMO -9.2861).

## Issues encountered (on the record)

1. **envelope_check.py --funnel branch defective as shipped**: reads top-level "model" key;
   bda writes model per candidate. Fails with "need mace+chgnet+xtb candidate outputs;
   check schemas" even on the pre-registered files. Verbatim record:
   envelope/funnel_branch_error_record.txt. Adjudication: same fixed script's --smiles path
   (identical funnel algorithms + identical hull/family code) + mechanical cross-check from
   bda funnel outputs via the script's own load_tri/families_matched
   (envelope/hull_crosscheck.py). All routes agree.
2. **Extrapolation**: all passing k values are 0.0005-0.0042x k0, below the 0.1x calibration
   floor; flagged in report as the declared-rule extrapolation assumption.
3. **Plating flag at 4C/45C**: anode potential min -0.4385 V -> mechanical plated=true.
   Fixed-cell property (additive cannot move it); outside the adjudicated criteria;
   reported honestly in report.md §8.
4. **CHGNet converged=false** for pfta/pftea — not an elimination line (energy at screening
   precision), recorded as-is.

## Discipline

- Only this workspace + pre-registered data (known_set_sei/) used; no other runs read.
- All conclusion-grade numbers come from tool output files; mapping executed from funnel
  outputs, not chosen. Extrapolation flagged, spectator-chemistry caveat stated.
- log.jsonl audit chain: criteria / plan / propose / funnel / evaluate (bda log-evaluate,
  verdict=pass) / final (verdict=achieved).
