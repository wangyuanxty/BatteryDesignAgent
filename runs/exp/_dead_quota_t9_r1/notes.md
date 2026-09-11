# T9-R1 Composition Design — Working Notes

Headless task. Contract: design a new positive-electrode composition for a
grid-storage cell on the Chen2020 NMC811/anode profile. Criteria A0/A1 (sealed
known-set), B (computed V >= 5.3 V), B' (true V >= 5.3 V), C (bridge rule),
D (closed-loop adjudication).

## Process findings (environment)

1. Workspace runs/exp/t9_r1 contains only an empty run.log (fresh arm).
2. Pre-registered data present: known_compositions.json (100 entries),
   rebuild_envelope.py, batch_comp.py, extend_spinels_screen.py.
3. **ANOMALY**: runs/exp/known_set_comp/envelope_stats_comp.json is MISSING.
   Repo-wide search found no copy. comp_envelope_check.py crashes with
   FileNotFoundError in BOTH modes (--formula and --point) — including the
   A0 known-hit branch (it reads the envelope file for n_known).
   Verified 2026-09-09:
   - `.venv\Scripts\python.exe comp_envelope_check.py --formula "LiNi0.5Mn0.5O2"` -> FileNotFoundError
   - `.venv\Scripts\python.exe comp_envelope_check.py --point 4.2 190 -1.5` -> FileNotFoundError
   The A0 membership *comparison* itself remains executable directly against
   known_compositions.json (pure JSON equality). A1 (Delaunay outside test)
   cannot use the pre-registered hull; a clearly-labeled reconstruction may be
   built in THIS workspace from run-comp over the known list (per documented
   calibration note: LiNiPO4 and LiNi0.4Co0.3Fe0.3PO4 excluded as Ni-olivine
   overestimate family).
   NOTE: since the documented computed band top is 5.114 V (LiNiCo55), any
   candidate with computed V >= 5.3 V is outside the hull by construction
   (convex combinations of V <= 5.114 cannot reach 5.3). B => A1.
4. run-comp env: D:/anaconda/envs/py312 (torch 2.13.0+cu126 CUDA, chgnet 0.4.2,
   bda importable). SKILL.md forbids .venv (CPU torch) for run-comp.
5. run-qe env: pw.x required (MSYS2 pw_stack4g.exe or py312 Library\bin\pw.x);
   SSSP efficiency pseudos only for Li/Ni/Mn/Co/O/P/Si/Mg — candidates needing
   other elements (Fe, Cu, Cr, V, ...) cannot be QE-endorsed with this setup.
   QE cost: 12-atom cell ~1 h/state; layered supercell 48 atoms "hours";
   olivine primitive 28 atoms, spinel primitive 56 atoms.
6. No mp_api client in py312; Materials-Project catalog check must go through
   the web (mp website / literature).

## Machinery recap (bda comp_runner)

- Prototype dispatch: contains P -> olivine Pnma (LFP); TM count sum == 2 ->
  spinel Fd-3m (LMO); else layered R-3m (NMC811 2x2x1 supercell, 48 atoms).
- Voltage: average of delithiation x=1.0 -> 0.3, vs CHGNet bcc Li reference.
- Capacity = 0.7 * F/3.6 / MW(formula); rel_stability vs NMC811 per-atom.
- Calibration note: NMC811 baseline should compute ~3.8 V avg.
- Documented overestimate families (B' rejects): Ni-containing olivines
  (LiNiPO4 7.016 V, LiNi0.4Co0.3Fe0.3PO4 6.067 V, band top LiNiCo55 5.114 V)
  and spinel deep-delithiation.

## Bridge rule (C)

Constant OCP = computed average voltage; C_cell = 0.90 * computed capacity;
SEI k0 = Chen2020 baseline; ED_active = V * C * 0.9 (reported, not criterion).
