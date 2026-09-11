# T9-new grid-storage cathode design — CANARY session note (2026-09-09)

Canary session `_t9canary` executed the CANARY PROTOCOL: criteria -> log.jsonl
entry 0; 3 candidate compositions -> entries 1-3; stop. **No simulations run.**
Primary canary log: `runs/exp/_t9canary/log.jsonl`; mirror entries (types
`canary_*`) appended to this workspace's log.jsonl after the round-1 funnel record.

## Continuity with this workspace's record
- Round-1 funnel (this log.jsonl) screened 20 candidates and down-selected LiCoMnO4
  (computed 8.5906 V, disclosed spinel-dispatch artifact; literature 5.0 V plateau,
  Kawai et al. 1998; MP catalog hits mp-1176657 / mp-753984 / mp-1176646).
- The canary re-proposed 3 candidates consistent with that funnel:
  1. LiCoMnO4 (primary; same down-select),
  2. LiCo2O4 (Co-only spinel; B' contested — Kawai ~5.0 V vs funnel note 'true ~4 V';
     resolve at stage D via run-qe + MP/catalog),
  3. LiMn1.5Co0.5O4 (Co-poor spinel; literature 4.7-5.0 V; B' marginal; not yet screened).
- All three are TM-sum=2 (spinel dispatch), QE-runnable (elements within
  {Li,Ni,Mn,Co,O,P,Si,Mg}), Co-based (outside the banned Ni-olivine overestimate family),
  and outside the documented layered+olivine system per the task guidance.

## Tooling facts re-verified this session
- run-comp dispatch (comp_runner.py): P -> olivine Pnma; TM-sum=2 -> spinel Fd-3m;
  else layered R-3m. Capacity proxy = 0.7*F/mw (F=26801.481). CHGNet relax.
- run-qe pseudopotentials: {Li,Ni,Mn,Co,O,P,Si,Mg} only (no F/Cr/Fe/Cu).
- 84-pt hull: layered + olivine only; V ceiling 5.1137 V; (B)>=5.3 implies (A) outside.
- Layered route dead (< 4.03 V computed); olivine route trap (Ni -> B'-rejected,
  Ni-free < 4.5 V); spinel route is the only path to computed >= 5.3 V.

## Next stage (post-canary)
run-comp replay on the 3 canary candidates -> comp_envelope_check.py (A) ->
run-qe + MP/catalog (B') -> bridge rule (C) -> closed-loop D -> cell-level delivery
on the Chen2020 profile. Do not treat literature priors in the canary entries as
computed values.
