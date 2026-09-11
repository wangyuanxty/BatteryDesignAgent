# T9_R2 Design Plan — New positive-electrode composition (Chen2020 NMC811/anode profile)

Date: 2026-09-10. Headless run. Workspace: `runs/exp/t9_r2`.

## 1. Objective parsing (contract verbatim)

Design a new positive-electrode composition for a grid-storage cell on the Chen2020
NMC811/anode profile. The composition replaces the cathode; all other cell choices fixed.

Adjudication gates (all pre-registered, replayable):
- **A0 (membership)**: exact formula must NOT be in `known_set_v2.json` membership (109 entries).
  Mechanical: `python comp_envelope_check.py --known-set runs/exp/known_set_comp/known_set_v2.json --formula <f>`.
- **A1 (hull)**: computed point (avg V, capacity, rel stability) must be OUTSIDE the Delaunay hull
  of the 96 sealed points. Same tool, `in_envelope` must be false.
- **B (computed window)**: run-comp `avg_voltage_v >= 5.3 V` (band top of hull = 5.114 V, a
  Ni-olivine overestimate-family entry).
- **B' (true-voltage guard)**: true (QE-level or literature-consistent) voltage >= 5.3 V.
  Computed-only values from Ni-olivine overestimate family and from unvalidated template cases
  (Fe-tavorite/NASICON) are NOT admissible. Documented true-voltage ceiling ~4.8 V sustained /
  5.1 V plateau / 5.3 V capacity-limited claim (Li2NiPO4F). No documented material can pass.
- **C (bridge)**: OCP = computed avg voltage (constant); capacity = 0.90 × computed capacity
  (LNMO-anchored utilization); SEI kinetics = baseline k0; ED_active = V × C × 0.9 (reported, not a criterion).
- **D (closed loop)**: finalist re-computed independently (run-comp replay + envelope check +
  run-qe + Materials-Project/catalog check); verdict records "not found in searched scope".

## 2. Domain-limit inventory (constrains the search)

1. **run-comp strict dispatch**: only layered LiMO2, olivine LiMPO4, spinel LiM2O4,
   tavorite LiM(PO4)F, tavorite LiM(SO4)F, NASICON Li3M2(PO4)3 are computable. Anything else →
   "unsupported framework" error (never fitted). Oxyfluorides Li2MPO4F, Li2MnO2F, etc. are NOT
   computable (membership-only).
2. **run-qe pseudopotential table**: only {Li, Ni, Mn, Co, O, P, Si, Mg} (qe_runner.py
   `_PSEUDO_FILES`). No F, S, V, Fe, Cr, Ti, Cu → **tavorite frameworks (contain F/S) can never
   be QE-endorsed**; NASICON with V/Fe/Cr/Ti can never be QE-endorsed. B' via QE is possible only
   for layered/olivine/spinel/NASICON built from {Ni, Mn, Co, Si, Mg}.
3. **Framework calibration (pre-registered)**: V-bearing and spinel frameworks compute LOW by
   ~0.2–0.5 V; Ni-olivine computes HIGH (overestimate family, top 7.0 V vs true 5.1 V); Fe in
   tavorite/NASICON templates unvalidated (computed +1.9…+2.2 V vs literature).
4. **Literature ceiling**: sustained avg discharge ≤ 4.8 V; plateau ≤ 5.1 V; redox claim 5.3 V
   (Li2NiPO4F, documented). A true >= 5.3 V needs chemistry outside documented families.

## 3. Candidate strategy

**Where can run-comp (B) possibly reach >= 5.3 V?**
- Hull data: non-Ni computed values top at LiNiSO4F 4.94 V. Only Ni-containing compositions in
  CHGNet-inflated environments (Ni-olivine, possibly Ni-tavorite) can plausibly exceed 5.3.
- Layered: hull max 4.03 → dead. Spinel: computes systematically LOW, hull max 4.33 → dead.
- NASICON: hull max 4.40 (Cr) → dead unless Ni-in-NASICON inflates (unvalidated template; QE too
  slow at 80 atoms → weak B' path).
- Tavorite-S: Ni endmember 4.94 (documented) → dead.
- **Tavorite-P with Ni/Co/Mn/Cr/Cu: unvalidated template, unknown CHGNet behavior** — the one
  unexplored framework where computed values might exceed 5.3. B' path is literature-only
  (no F pseudo → no QE). Must search literature; if none, record domain limit honestly.
- **Ni-olivines (Ni >= ~0.6)**: computed >= 5.3 almost certain (overestimate family), and QE-able.
  B' requires run-qe >= 5.3 V. Expected physics ~4.9–5.1 V (plateau bound) — likely negative,
  but the contract's mechanical B' definition is "QE-level", so run-qe is the arbiter.

**Batches** (diverse, ~24 candidates, one run-comp batch):
- Tavorite-P exploration: LiNiPO4F, LiNi0.75Co0.25PO4F, LiNi0.5Co0.5PO4F, LiCoPO4F, LiMnPO4F,
  LiCrPO4F, LiNi0.5Mn0.5PO4F, LiNi0.5V0.5PO4F, LiCuPO4F.
- Tavorite-S bound: LiNi0.75Co0.25SO4F, LiNi0.5Co0.5SO4F, LiCuSO4F.
- Olivine (QE-able; overestimate family): LiNi0.8Co0.2PO4, LiNi0.75Co0.25PO4, LiNi0.6Co0.4PO4, LiNi0.4Co0.6PO4.
- Spinel (QE-able; compute-low family — completeness check): LiCo2O4, LiNi0.5Co1.5O4, LiNiCoO4,
  LiNi0.75Co1.25O4.
- NASICON (QE-able but slow; unvalidated Ni): Li3Ni2(PO4)3, Li3NiCo(PO4)3, Li3Co2(PO4)3, Li3Mn2(PO4)3.

All formulas avoid exact-match with the 109 membership entries (verified programmatically before screening).

**Fallback ladder**:
1. If a QE-able candidate computes >= 5.3 → run-qe it (B'). QE >= 5.3 → pass (D).
2. If tavorite-P computes >= 5.3 but no literature/QE path → document as B-passing but
   B'-unsatisfiable (domain limit: no F pseudo; no literature found) → negative.
3. If nothing computes >= 5.3 → negative result with full evidence (contract allows and asks
   for honest negative reporting).

## 4. Budget allocation

- run-comp: ~20 s/state GPU. Batch of 24 candidates ≈ 50 relaxations ≈ 20–30 min. Up to 3 batches.
- run-qe: only for closing finalist(s) (forbidden inside funnel). Olivine 28-atom cell ≈ hours;
  spinel 56-atom ≈ overnight; NASICON 80-atom ≈ too slow (excluded from QE planning unless
  everything else fails and time permits).
- Web/literature search: for B' literature evidence on non-documented compositions (tavorite-P
  Ni/Co/Cu, high-voltage spinels) — recorded with sources.
- Materials-Project/catalog check (D): search for finalist formula in public catalogs.

## 5. Risk and fallback

- **Risk 1**: no candidate computes >= 5.3 outside overestimate families → honest negative.
- **Risk 2**: only Ni-olivines compute >= 5.3; QE returns < 5.3 (expected ~5.0) → negative on B';
  record QE numbers as evidence.
- **Risk 3**: QE runtime (overnight) exceeds harness budget → run QE in background, record state;
  if incomplete at close, record honestly.
- **Risk 4**: run-comp non-convergence (converged=false is known screening-precision behavior —
  energies still usable at screening precision; noted per batch).

## 6. References (domain basis, no fabrication)

- CHGNet relaxation + NMC811 prototype: this repo's comp_runner.py docstrings (provenance inlined).
- Tavorite LiVPO4F / LiFeSO4F structures: provenance inlined in comp_runner.py builders
  (OSTI/ICSD 184601; Barpanda et al. Nat. Mater. 2011 supp.).
- NASICON Li3V2(PO4)3: COD 2237423 (inlined).
- High-voltage cathode voltage landscape (LiNiPO4 5.1 V plateau, LiCoMnO4/LiCoPO4 ~4.8 V,
  Li2NiPO4F ~5.3 V claim): contract-declared literature ceiling (pre-registered); direction-only.
- LiMn2O4/LNMO spinel voltages: contract calibration note (pre-registered).
