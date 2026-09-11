# T9_r1 FINAL REPORT — New positive-electrode composition for grid-storage cell (Chen2020 NMC811/anode profile)

**Run date:** 2026-09-10 (headless)
**Workspace:** `runs/exp/t9_r1` — only this workspace and the pre-registered data
(`runs/exp/known_set_comp/known_set.json`, `comp_envelope_check.py`) were used. No other runs'
workspaces were read or referenced.

## VERDICT: NEGATIVE RESULT

**No candidate composition attains the design window.** 44 candidates were screened across three
reachable prototype families (layered, olivine, spinel) plus a 2-candidate sanity batch. 12
candidates passed the mechanical layers (A0 membership, A1 envelope, B computed >= 5.3 V) — every
one is rejected by the B' true-voltage guard (documented overestimate families or literature true
voltage far below 5.3 V). The single non-family mechanical passer (LiVPO4) additionally fails (B) on
independent replay (5.246 V < 5.3 V). This result is reported honestly per contract: within the
machinery (prototype structures, CHGNet screening, QE element set), a composition that is genuinely
new, outside the documented envelope, and truly >= 5.3 V does not exist. The literature ceiling for
reversible true voltage (~5.0–5.3 V) is owned by materials that are themselves in the membership
list, so (A0) excludes them by construction.

---

## 1. Contract criteria and how each layer was applied

- **(A0) Membership** — mechanical: exact formula string vs the 99 documented formulas. Rejected
  on match. Checked per candidate via `adjudicate_batch.py` and independently by
  `comp_envelope_check.py --formula <F>` for the replayed representatives.
- **(A1) Envelope** — mechanical: computed point (avg V, C, rel_stab) must be OUTSIDE the
  pre-registered Delaunay hull of the 90 documented points. Checked by the pre-registered checker
  (`--point` and `--formula` paths).
- **(B) Window** — computed average voltage >= 5.3 V via run-comp (CHGNet, x_Li=0.3 window,
  CHGNet bcc-Li reference; converged=false accepted at screening precision). Baseline self-check:
  NMC811 computed E_full = -290.972 eV/48 at, E_Li = -1.8785 eV/at; NiCo85-layered computed 3.75 V
  vs literature NMC811 ~3.8 V — screening precision is consistent with the calibration note.
- **(B') True-voltage guard** — true (QE-level or literature-consistent) voltage >= 5.3 V, for a
  NON-cathode material. Computed-only highs from documented overestimate families (Ni-olivine,
  spinel deep-delithiation) are REJECTED at adjudication regardless of (B). Pre-registered
  calibration note applied: LiNiPO4 7.016 V and LiNi0.4Co0.3Fe0.3PO4 6.067 V are excluded;
  LiNiCo55 5.114 V is the same overestimate family — Ni-rich olivine computed values are NOT
  grounds for passing. No documented composition can pass B' (true ceiling ~5.0–5.1 V for
  documented cathodes; the only ~5.3 V true-voltage materials, Li2NiPO4F and LiCoMnO4, are in the
  membership list -> A0).
- **(C) Bridge rule** — no free parameters: OCP = computed avg V; C_cell = 0.9 x computed C
  (LNMO-anchored utilization); SEI k0 = baseline; ED_active = V x C x 0.9 (reported, not a
  criterion). Applied illustratively in §5; no candidate survived to be a finalist.
- **(D) Closed-loop adjudication** — independent replay (run-comp + envelope checker) executed for
  representative passers (§4); run-qe documented as not triggered (§6); catalog check verdicts
  recorded as "not found in searched scope" (§7).

## 2. Campaign summary

| batch | file | candidates | outcome |
|---|---|---|---|
| sanity | `screen_sanity.json` | 2 | LiCo2O4 passes mechanics (8.010 V, stab -0.216 above all 90 known points) -> B'-rejected (spinel deep-delithiation; true 3.2–4.0 V, Choi & Manthiram); LiNi0.7Co0.3PO4 5.105 V fails (B) |
| batch 1 | `screen_batch1.json` | 22 | 8 pass A0+A1+B (all family-rejected at B') |
| batch 2 | `screen_batch2.json` | 20 | 4 pass A0+A1+B (all family-rejected at B') |

Total: 44 screened + 2 sanity. All formulas were checked not in the 99-member list (A0 ok).

## 3. The 12 mechanical passers (A0 + A1 + B) and their B' adjudication

All 12 returned `PASS (outside envelope)` from the pre-registered checker
(`point_verdicts_all.json`). All 12 are B'-REJECTED:

| # | candidate | formula | V (batch) | C | stab | B' verdict (grounds) |
|---|---|---|---|---|---|---|
| 1 | NiCo91-olivine | LiNi0.9Co0.1PO4 | 7.004 | 116.8 | -1.812 | REJECT — Ni-olivine overestimate family; realized TM = Ni4 (pure LiNiPO4 realized; excluded calibration 7.016 V reproduced); true olivine ceiling 5.1 V |
| 2 | NiFe73-olivine | LiNi0.7Fe0.3PO4 | 6.199 | 117.4 | -1.961 | REJECT — Ni-olivine family; true Ni olivine <= 5.1 V (Fe lowers) |
| 3 | NiPO4F-tavorite | LiNiPO4F | 6.931 | 104.5 | -1.812 | REJECT — Ni-olivine/tavorite family (documented AMPO4F framework); ~5.3 V claims belong to the Li2NiPO4F system, a documented cathode; exact-composition evidence weak; computed value unreliable per calibration |
| 4 | NiMg91-olivine | LiNi0.9Mg0.1PO4 | 6.955 | 119.4 | -1.813 | REJECT — Ni-olivine family; realized TM = Ni4 |
| 5 | LiNi2O4-spinel | LiNi2O4 | 7.972 | 99.6 | +0.313 | REJECT — spinel deep-delithiation family (x_Li=0.3 window beyond reversible range of a 1-Li-per-fu spinel); true Ni spinel redox 4.6–4.8 V, O-2p edge ~5.0 V |
| 6 | LiCoNiO4-spinel | LiCoNiO4 | 8.740 | 99.5 | +0.008 | REJECT — spinel deep-delithiation; true Co/Ni spinel redox 4.6–5.0 V |
| 7 | LiNiFeO4-spinel | LiNiFeO4 | 7.921 | 101.2 | -0.135 | REJECT — spinel deep-delithiation; true ~4.5–5.0 V |
| 8 | Mn15Fe05O4-spinel | LiMn1.5Fe0.5O4 | 7.755 | 103.5 | -0.777 | REJECT — spinel deep-delithiation; true Mn3+/4+ 4.1 V + Fe3+/4+ ~4.9–5.0 V (LiFeMnO4 documented 5V-class, < 5.3) |
| 9 | NiFe82-olivine | LiNi0.8Fe0.2PO4 | 6.199 | 117.2 | -1.961 | REJECT — Ni-olivine family; true <= 5.1 V |
| 10 | VPO4-olivine | LiVPO4 | 5.863 | 122.7 | -2.640 | REJECT — true voltage literature-consistent ~4.1 V (vanadyl-phosphate V3+/V4+ family operates 3.8–4.2 V: LiVPO4F tavorites avg 4.13–4.22 V; Li3V2(PO4)3 plateau 3.77 V, 2-Li plateau ~4.1 V). Computed 5.863 V >> true. No >= 5.3 V claim exists. QE impossible (V absent from registered pseudopotential set). Additionally: independent replay computes 5.246 V < 5.3 -> fails (B) on recomputation |
| 11 | LiV2O4-spinel | LiV2O4 | 8.669 | 108.6 | -0.942 | REJECT — spinel-family computed high; true LiV2O4 is a metallic spinel with Li insertion ~2.5–3 V (anode-type); no >= 5.3 V cathode claim |
| 12 | Mn15Cr05O4-spinel | LiMn1.5Cr0.5O4 | 9.008 | 104.6 | -0.794 | REJECT — spinel deep-delithiation; true Cr3+/Cr4+ plateau 4.8 V in LiCrxMn2-xO4 (documented 5V-class spinel, < 5.3) |

**Non-passers (mechanical):** all layered candidates (incl. exotic diluents W/Mo/Sb/Ge/Ti/Te/Sn)
computed 2.94–4.03 V -> fail (B). NiCo82 (5.422), NiCo75 (5.415), LiTi2O4 (7.432),
Mn15Co05O4 (8.348), Ni05Ti15O4 (8.336), LiMn1.5Al0.5O4 (7.990) INSIDE hull -> A1 reject.
LiCuPO4 4.912 V, Li2NiO3 3.895 V, Li2CuO2 3.644 V, LiMnPO4F 3.584 V, LiFePO4F 3.452 V,
Li2Ni0.5Mn0.5O3 3.646 V, NiMn-olivines 4.80–4.84 V, CoMn91 4.507 V, NiFe64 4.584 V -> fail (B).

## 4. Closed-loop replay (criterion D, mechanical part)

Independent recomputation via the pre-registered checker (`comp_envelope_check.py --formula <F>`,
full CHGNet re-run + A0 + A1) for 3 representatives:

| formula | V replay | V batch | C replay | stab replay | envelope verdict |
|---|---|---|---|---|---|
| LiNi0.9Co0.1PO4 | 6.909 | 7.004 | 116.80 | -1.813 | PASS (outside envelope), A0 ok |
| LiMn1.5Cr0.5O4 | 9.002 | 9.008 | 104.61 | -0.793 | PASS (outside envelope), A0 ok |
| LiVPO4 | **5.246** | 5.863 | 122.74 | -2.566 | PASS (outside envelope), A0 ok — but V < 5.3 -> (B) fails in replay |

Run-to-run energy noise (CHGNet relaxer perturbation) shifts LiVPO4 across the 5.3 V threshold:
its (B) pass is not reproducible and its B' rejection stands on true-voltage grounds regardless.

## 5. Bridge rule (C) — illustrative computation for the mechanically strongest candidates

The bridge rule applies to a surviving finalist; none survives, so these are reported as
illustrative only and DO NOT constitute a design:

| candidate | OCP = V_comp (V) | C_cell = 0.9 x C (mAh/g) | ED_active = V x C x 0.9 (Wh/kg) | status |
|---|---|---|---|---|
| LiNi0.9Co0.1PO4 (replay) | 6.909 | 105.1 | 726.3 | B'-rejected (Ni-olivine family) |
| LiMn1.5Cr0.5O4 (replay) | 9.002 | 94.1 | 847.6 | B'-rejected (spinel deep-delithiation) |
| LiVPO4 (replay) | 5.246 | 110.5 | 579.5 | fails (B) in replay; B'-rejected (true ~4.1 V) |

SEI kinetics = baseline k0 in all cases (no levers applied; no candidate reached cell integration).

## 6. run-qe (criterion D) — not triggered (documented)

QE voltage computation is documented as vacuous for this campaign:
- Every candidate that passed the mechanical layers is B'-rejected at adjudication "regardless of
  (B)", i.e., QE could not rescue them: Ni-olivine and spinel passers are rejected by family
  (computed-only highs are explicitly not grounds for passing), and QE would only confirm the
  documented true voltages of those families (<= 5.1 V olivine ceiling; 4.0–5.0 V spinel redox).
- The single non-family passer, LiVPO4, contains V, which is absent from the registered QE
  pseudopotential set {Li, Ni, Mn, Co, O, P, Si, Mg} — QE computation is impossible for it; and its
  literature-consistent true voltage (~4.1 V) already fails B'.
- No non-family candidate computed >= 5.3 V, so no B'-eligible finalist existed for QE to verify.

## 7. Catalog check (criterion D) — "not found in searched scope"

Public web catalog/literature checks (no MP API key available; Materials Project not directly
fetchable in this environment — recorded honestly):
- The only two materials with documented true voltage at the >= 5.0–5.3 V class — Li2NiPO4F
  (~5.3 V, JES 2010 experiment; DFT 5.33 V, Chakrabarti & Thakur JES 2024) and LiCoMnO4 (5.0–5.3 V
  plateaus, UMD 5.3 V Li-metal cell) — are both in the membership list (A0 excludes them).
- None of the 12 mechanical passers was found as a documented cathode composition in the searched
  scope with a true voltage >= 5.3 V; where literature exists it contradicts the computed value:
  LiCo2O4 3.2–4.0 V (Choi & Manthiram JES 2002), LiNiPO4 5.1 V olivine ceiling, spinel Ni 4.6–4.8 V,
  Cr3+/4+ 4.8 V, LiVPO4 family ~4.1 V.
- Verdict recorded per contract: **"not found in searched scope"** — no absolute claim made.

## 8. Evidence files (workspace `runs/exp/t9_r1`)

- `screen_sanity.json` — sanity batch (baseline NMC811 calibration, LiCo2O4, LiNi0.7Co0.3PO4)
- `screen_batch1.json` — 22 candidates
- `screen_batch2.json` — 20 candidates
- `adjudicate_batch.py` — mechanical A0/A1/B adjudication (exact membership string match +
  pre-registered Delaunay hull)
- `point_verdicts_all.json` — pre-registered `--point` verdicts for all 12 passers: all
  PASS (outside envelope)
- `replay_NiCo91.json`, `replay_MnCr.json`, `replay_VPO4.json` — independent `--formula` replays
- `hull_probe.py` — hull geometry mapping (escape routes exist; Delaunay test decides each case)
- `notes.md` — full running log incl. B' literature evidence

## 9. Conclusion

The design window (new, outside-envelope, computed AND true average voltage >= 5.3 V) is not
attainable by any candidate this machinery can express. The mechanical layers are passable only
through the two pre-registered overestimate families (Ni-olivine, spinel deep-delithiation) or
through LiVPO4, whose computed high is not reproducible on replay and whose true voltage is ~4.1 V.
Per the contract, this negative result is reported honestly; no cathode-replacement composition is
delivered.
