# T9-new grid-storage cathode design — CANARY session notes (2026-09-09)

Session: `_t9canary` (canary protocol). Design workspace: `runs/exp/t9new_r1`.
Protocol executed: criteria -> log.jsonl entry 0; 3 candidate compositions -> entries 1-3;
canary_stop -> entry 4. **No simulations were run this session.**

## Task parsed
- Positive-electrode composition for a grid-storage cell on the Chen2020 NMC811/anode
  profile. Composition replaces the cathode; every other cell choice is fixed.
- Contract: (A) computed point outside the 84-compound documented-cathode hull;
  (B) computed avg V >= 5.3 V; (B') true V >= 4.95 V, Ni-olivine overestimates rejected;
  (C) OCP = computed V, capacity = computed x 0.90; (D) closed-loop adjudication later.
- Guidance: documented cathodes cannot reach the window under a true-voltage measure;
  in-family extrapolation is not a path; must leave the documented chemistry system.
  Non-molecular levers forbidden.

## Tooling explored (read-only, this session)
- `comp_envelope_check.py` (repo root): Delaunay hull adjudication over
  `envelope_stats_comp.json`; `--point V C stab` and `--formula` modes.
- `.claude/skills/virtual-battery-factory/scripts/bda/simulators/comp_runner.py`
  (run-comp): CHGNet full/delithiated(x=0.3) relax; dispatch: P-containing ->
  olivine Pnma; TM-sum=2 -> spinel Fd-3m; else -> layered R-3m NMC811.
  Capacity proxy = 0.7*F/mw (F=26801.481); V from full/delithiated energies vs bcc-Li.
- `qe_runner.py` (run-qe): SSSP pseudopotentials for exactly
  {Li, Ni, Mn, Co, O, P, Si, Mg}. No F/Cr/Fe/Cu/Ti/Al.
- Pre-registered `known_set_comp/`: 84 documented cathodes (layered + olivine; no
  spinels); hull V ceiling = 5.1137 V; excluded outliers = CHGNet Ni-olivine
  overestimates (7.016/6.067 V) — the family the B' guard bans.
- Own workspace context: `t9new_r1/log.jsonl` round-1 funnel (20 screened; down-select
  LiCoMnO4, computed 8.5906 V flagged as spinel-dispatch artifact; Ni-olivine 6.89 V
  banned; V-olivine B'-fails; Co-fluorophosphate computes 4.42 V); `catalog_mp_check.json`
  has MP hits for CoLiMnO4 (mp-1176657, mp-753984, mp-1176646).

## Routing analysis
- (B) >= 5.3 V automatically implies (A) (hull V ceiling 5.1137).
- Layered route: hull max 4.03 V computed -> dead. Olivine route: trap — Ni computes
  inflated (B'-rejected); Ni-free computes < 4.5 V -> dead. All P-containing formulas
  dispatch there -> excluded.
- Only the spinel (TM-sum=2) prototype can plausibly reach computed >= 5.3 V, and among
  QE-runnable elements only Co3+/4+ (~5.0 V true) clears B'. Proposals = Co-Mn spinel
  sweep, outside the documented layered+olivine system per guidance.

## Proposals (canary entries 1-3; mirror appended to t9new_r1/log.jsonl)
1. **LiCoMnO4** (primary; prior down-select) — Co 5 V spinel, literature ~5.0 V
   (Kawai 1998), MP-catalog present, QE-clean. Bridged capacity ~91 mAh/g.
2. **LiCo2O4** (aggressive) — Co-only spinel; B' contested (Kawai ~5.0 V vs prior
   funnel note 'true ~4 V'); resolve at stage D. Bridged capacity ~89 mAh/g.
3. **LiMn1.5Co0.5O4** (Co-poor fallback) — literature 4.7-5.0 V, B' marginal;
   highest capacity of the trio (~92 mAh/g bridged).

All three: TM-sum=2 (spinel dispatch), QE-runnable, Co-based (outside the Ni-olivine
guard family). Voltage figures in the log are literature priors / prior workspace
records, explicitly labeled; capacity proxies are deterministic run-comp arithmetic.

## File placement rationale
- `_t9canary/log.jsonl` = this session's canary log (primary; harness convention per
  run.py:224 / verify_deliverables.py:126 / audit.py:7 read `case_dir/log.jsonl`).
- `t9new_r1/log.jsonl` = prior adjudication record, preserved byte-exact; canary
  entries appended with distinct `canary_*` types as a mirror.

## Next stage (post-canary, with an execution channel)
1. run-comp replay on entries 1-3; 2. comp_envelope_check.py (A);
3. run-qe + MP/catalog true-voltage adjudication (B'); 4. bridge rule (C);
5. closed-loop D chain; then cell-level delivery on the Chen2020 profile.

No simulated values were produced or recorded this session.
