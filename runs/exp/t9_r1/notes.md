# T9_r1 — Grid-storage cell, new positive-electrode composition (Chen2020 NMC811/anode profile)

Headless run, 2026-09-10. Workspace: `runs/exp/t9_r1`. Pre-registered data: `runs/exp/known_set_comp/known_set.json` (membership 99 / hull points 90), `comp_envelope_check.py` (repo root).

## 1. Design target (parsed from contract t9_v8_contract.txt)

- Replace ONLY the cathode composition of the Chen2020 NMC811/anode cell. All other cell choices fixed.
- (A0) formula must NOT be one of the 99 documented members (mechanical, `comp_envelope_check.py --formula`).
- (A1) computed point (V, C, stab) must be OUTSIDE the Delaunay hull of the 90 documented points (mechanical, `--point`).
- (B)  computed average voltage >= 5.3 V (run-comp, CHGNet; converged=false accepted at screening precision).
- (B') true voltage >= 5.3 V, QE-level or literature-consistent, for a NON-cathode material;
      computed-only highs from the documented overestimate families (Ni-olivine, spinel deep-delithiation)
      are REJECTED at adjudication regardless of (B).
- (C) bridge rule (no free params): OCP = computed avg V; C_cell = 0.9 x computed C (LNMO-anchored utilization);
      SEI k0 = baseline; ED_active = V x C x 0.9 (reported, not a criterion).
- (D) finalist: independent replay (run-comp + envelope) + run-qe + MP/catalog check; verdict records
      "not found in searched scope" — no absolute claim.
- If nothing attains the window: report the negative result honestly.

## 2. Tools available (verified)

- `D:/anaconda/envs/py312/python.exe`: torch 2.13.0+cu126 (CUDA ok), chgnet 0.3.0 (elements Z=1..94), pymatgen 2026.8.13, bda (editable).
- `python -m bda run-comp --in IN --out OUT` — CHGNet screening: NMC811 2x2x1 layered prototype (48 at) /
  Pnma olivine prototype (28 at, if P in formula) / Fd-3m spinel prototype (56 at, if TM sum = 2);
  voltage over x_Li 0.3 window incl. CHGNet bcc-Li reference; C = 0.7 F/3.6 / mw.
- `python -m bda run-qe` — pw.x at C:\msys64\ucrt64\bin\pw_stack4g.exe (present), SSSP efficiency pseudopotentials
  (present) for {Li,Ni,Mn,Co,O,P,Si,Mg} ONLY. CPU hours per state (28-56 atom cells).
- `python comp_envelope_check.py --formula F | --point V C stab` — mechanical A0/A1 verdicts.
- No MP API key in .env → catalog check via public materialsproject.org lookup (web).

## 3. Candidate strategy

- In-family extrapolation is excluded by design (guidance). Families reachable by run-comp prototypes:
  layered (TM sum=1), olivine (P-bearing), spinel (TM sum=2).
- Batches: (1) Ni-olivine variants, non-Ni olivines, spinel variants, layered variants, exotic
  high-valence layered (W/Mo/Sb/Ge/Ti/Te). All formulas NOT in the 99-member list.
- Expect: Ni-olivines/spinels may pass A0+A1+B computationally (overestimate families) -> B' rejects.
  Layered/exotic will fail B (V < 5.3) or B' (no literature, no QE pseudopotentials).

## 4. Key evidence so far

### Sanity batch (`screen_sanity.json`)
- baseline NMC811: E_full = -290.972 eV (48 at), E_Li = -1.8785 eV/at (CHGNet), converged=false (accepted).
- LiCo2O4 (spinel prototype): V=8.010, C=99.37, stab=-0.2157 -> stab above ALL 90 known points
  (max known stab = -0.3610, LiNiVO4) -> mechanically OUTSIDE hull. BUT: spinel deep-delithiation
  overestimate family -> B' reject regardless. (Also x=0.3 delithiation of a spinel is beyond the
  reversible window; true LiCo2O4 voltage ~5.0 V class, not >= 5.3 V.)
- LiNi0.7Co0.3PO4 (olivine prototype): V=5.105 < 5.3 -> fails (B). (Ni-olivine family anyway.)

### Batch 1 (`screen_batch1.json`, 22 candidates, mechanical adjudication via `adjudicate_batch.py`)

Passers of A0+A1+B (V >= 5.3, outside hull, not in membership) — ALL in documented overestimate families:
| candidate | formula | V | C | stab | family |
|---|---|---|---|---|---|
| NiCo91-olivine | LiNi0.9Co0.1PO4 (realized Ni4) | 7.004 | 116.8 | -1.812 | Ni-olivine |
| NiFe73-olivine | LiNi0.7Fe0.3PO4 | 6.199 | 117.4 | -1.961 | Ni-olivine |
| NiPO4F-tavorite | LiNiPO4F (realized Ni4) | 6.931 | 104.5 | -1.812 | Ni-olivine (documented tavorite AMPO4F framework) |
| NiMg91-olivine | LiNi0.9Mg0.1PO4 (realized Ni4) | 6.955 | 119.4 | -1.813 | Ni-olivine |
| LiNi2O4-spinel | LiNi2O4 | 7.972 | 99.6 | +0.313 | spinel deep-delith |
| LiCoNiO4-spinel | LiCoNiO4 | 8.740 | 99.5 | +0.008 | spinel deep-delith |
| LiNiFeO4-spinel | LiNiFeO4 | 7.921 | 101.2 | -0.135 | spinel deep-delith |
| Mn15Fe05O4-spinel | LiMn1.5Fe0.5O4 | 7.755 | 103.5 | -0.777 | spinel deep-delith |

- Ni-olivine computed values reproduce the excluded LiNiPO4 overestimate (7.016 V excluded;
  LiNi0.9X0.1PO4 realized = all-Ni sites -> 6.95-7.00 V). Unreliable per pre-registered calibration note.
- Spinels: x_Li=0.3 window on a 1-Li-per-fu spinel is far beyond the reversible window; computed
  7.8-8.7 V vs true Ni/Fe/Mn/Co spinel redox 4.0-5.0 V -> deep-delithiation overestimate.
- All 8 are B'-REJECTED at adjudication regardless of (B). LiMn1.5Al0.5O4: INSIDE hull (A1 reject).
- All layered candidates fail (B) (max computed 4.03 V, LiNi0.8Sb0.2O2). Exotic high-valence
  diluents (W/Mo/Sb/Ge/Ti) do NOT produce computed >= 5.3 V on the layered prototype (3.02-4.03 V).
- LiCuPO4: 4.912 V < 5.3 -> fails (B) (Cu3+/Cu2+ theoretical 5.3 V not realized in CHGNet or in
  reversible practice).
- Li2NiO3: 3.895 V (fails B).

### Batch 2 (`screen_batch2.json`, 20 candidates, mechanical adjudication via `adjudicate_batch.py`)

Passers of A0+A1+B (V >= 5.3, outside hull, not in membership):
| candidate | formula | V | C | stab | family |
|---|---|---|---|---|---|
| NiFe82-olivine | LiNi0.8Fe0.2PO4 | 6.199 | 117.2 | -1.961 | Ni-olivine |
| VPO4-olivine | LiVPO4 | 5.863 | 122.7 | -2.640 | vanadyl phosphate (NOT a named overestimate family) |
| LiV2O4-spinel | LiV2O4 | 8.669 | 108.6 | -0.942 | spinel deep-delith |
| Mn15Cr05O4-spinel | LiMn1.5Cr0.5O4 | 9.008 | 104.6 | -0.794 | spinel deep-delith |

- NiCo82 (5.422) and NiCo75 (5.415) computed >= 5.3 but INSIDE hull -> A1 reject.
- LiTi2O4 (7.432), Mn15Co05O4 (8.348), Ni05Ti15O4 (8.336) INSIDE hull -> A1 reject.
- All layered (Te/Sn/W/Mo diluents), MnPO4F (3.584), FePO4F (3.452), Li2CuO2 (3.644),
  Li2Ni0.5Mn0.5O3 (3.646) fail (B).

### B' adjudication of the 12 mechanical passers (all REJECTED)
- 6 Ni-olivines (NiCo91 7.004, NiFe73 6.199, NiPO4F 6.931, NiMg91 6.955, NiFe82 6.199, all with
  NiCo75/NiCo82-class compositions) — pre-registered Ni-olivine overestimate family; true ceiling
  LiNiPO4 5.1 V; realized-TM counts show Ni4 (pure LiNiPO4 realized) in several -> excluded-calibration
  reproduction. B' REJECT regardless of (B).
- 5 spinels (LiNi2O4 7.972, LiCoNiO4 8.740, LiNiFeO4 7.921, Mn15Fe05O4 7.755, Mn15Cr05O4 9.008) —
  spinel deep-delithiation family (x_Li=0.3 window beyond reversible range of 1-Li-per-fu spinel);
  true spinel redox 4.0-5.0 V (Ni 4.6-4.8, Cr3+/4+ 4.8, O-2p edge ~5.0). B' REJECT.
- LiV2O4 (8.669) — spinel-family computed; true LiV2O4 is a metallic spinel, Li insertion ~2.5-3 V
  (anode-type); no >= 5.3 V cathode claim. B' REJECT.
- LiVPO4 (5.863) — NOT a named overestimate family, but true voltage literature-consistent ~4.1 V:
  vanadyl-phosphate V3+/V4+ family operates 3.8-4.2 V (LiVPO4F tavorites ~4.13-4.22 V avg;
  Li3V2(PO4)3 plateau 3.77 V, 2-Li plateau ~4.1 V). 5.863 V computed >> 4.1 V true -> B' fails
  (no >= 5.3 V literature claim exists). QE impossible: V absent from registered pseudopotential set.
- Verdict: no candidate attains the window. Negative result (final).

### Closed-loop replay (pre-registered checker, independent recomputation)
- `comp_envelope_check.py --point V C stab` run for all 12 passers -> `point_verdicts_all.json`:
  all 12 "PASS (outside envelope)" (in_envelope=False) — mechanical A1 confirmed.
- `comp_envelope_check.py --formula <F>` replays (full CHGNet recompute + A0 + A1) launched for
  3 representatives: LiNi0.9Co0.1PO4 -> `replay_NiCo91.json`, LiMn1.5Cr0.5O4 -> `replay_MnCr.json`,
  LiVPO4 -> `replay_VPO4.json`. Replay values (vs batch):
  - LiNi0.9Co0.1PO4: V 6.909 (batch 7.004), C 116.80 (same), stab -1.813 -> PASS outside, A0 ok.
  - LiMn1.5Cr0.5O4: V 9.002 (batch 9.008), C 104.61 (same), stab -0.793 -> PASS outside, A0 ok.
  - LiVPO4: V **5.246** (batch 5.863), C 122.74 (same), stab -2.566 -> PASS outside, A0 ok, but
    replay V < 5.3 -> (B) fails in independent recomputation (relaxation noise straddles threshold).
    B' rejects regardless (true ~4.1 V). This removes the only non-family mechanical passer.
- Catalog check (Materials Project / literature, web): LiCo2O4 true activity ~3.2-4.0 V (Choi &
  Manthiram); LiVPO4 family ~4.1 V; LiNiPO4 5.1 V; LiCrxMn2-xO4 Cr3+/4+ 4.8 V; Li2NiPO4F / LiCoMnO4
  (the only true >= 5.0-5.3 V materials) both in membership -> A0. No candidate composition was found
  as a documented cathode in the searched scope; verdict recorded as "not found in searched scope".

### B' literature (web, 2026-09-10)
- Only two materials documented at true ~5.3 V: Li2NiPO4F (JES 2010 exp ~5.3 V; DFT 5.33 V
  Chakrabarti&Thakur JES 2024) and LiCoMnO4 (UMD 5.0-5.3 V plateaus, 5.3 V Li cell).
  BOTH are in the membership list -> A0 rejects.
- LiNiPO4 = 5.1 V ceiling for olivines. No reversible material > 5.3 V documented.
- Cu-based (Li2CuP2O7 ~5.3 V theoretical, NON-reversible >5 V, phase unstable; Li4Cu4O2(SO4)4 4.7 V rev) -> not valid.
- LiMSO4F (M=Ni,Co) fluorosulfates: no redox activity observed below 5 V (Barpanda et al.) -> unusable.
- LiNiPO4F: ~5.3 V claims in the wild are attributed to the Li2NiPO4F system (tavorite AMPO4F family,
  a DOCUMENTED cathode framework); exact-composition evidence weak; Ni-olivine-family computed values
  unreliable regardless -> B' reject path.
- UMD LiCoMnO4 5.3 V Li-metal cell (5.0-5.3 V plateaus, electrolyte stable to 5.5 V) = documented
  spinel, in membership list -> A0 rejects. This is the practical true-voltage ceiling of the field.
- LiCo2O4 true activity ~3.2-4.0 V (Choi & Manthiram JES 2002; 2008 structural study) -> computed
  8.01 V is a deep-delithiation overestimate, NOT a true voltage.
- Spinel Ni redox true values: Ni2+/3+ ~4.6 V, Ni3+/4+ ~4.8 V; O-2p edge ~5.0 V -> spinel family
  cannot be true >= 5.3 V.
- Hull geometry probe (hull_probe.py): envelope has interior bands; escape routes exist via
  stab too-high (spinel band, stab > -0.36) or stab too-low (Ni-olivine band at V~5.5-7, stab <= -2.0),
  and via V too high at fixed C. Delaunay test decides each candidate mechanically.
