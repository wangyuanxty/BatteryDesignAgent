# t9new_r1 — Design Plan: New Positive-Electrode Composition (grid storage, Chen2020 NMC811/anode profile)

**Task contract (verbatim thresholds):**
- System: Chen2020 NMC811/graphite profile; the new composition REPLACES the cathode; all other cell choices fixed.
- (A) Envelope: candidate run-comp point (avg_voltage, capacity, rel_stability) must be OUTSIDE the pre-registered
  84-compound documented-cathode convex hull (`runs/exp/known_set_comp/envelope_stats_comp.json`; adjudicated by
  `comp_envelope_check.py`, Delaunay outside test, replayable). Two pre-registered calibration outliers excluded from
  the hull: LiNiPO4 (7.016 V computed) and LiNi0.4Co0.3Fe0.3PO4 (6.067 V) — CHGNet Ni-olivine high-voltage
  overestimate family.
- (B) Property window: computed average voltage >= 4.95 V (run-comp, CHGNet; converged=false accepted at screening precision).
- (C) Bridge rule (no free parameters): constant OCP = computed average voltage; capacity = computed capacity x 0.90;
  SEI kinetics = baseline k0; ED_active = V x C x 0.9 (reported, not a criterion).
- (D) Closed-loop adjudication: finalist re-computed independently (run-comp replay + comp_envelope_check.py)
  + run-qe (QE voltage vs Li metal) + Materials-Project/catalog check; verdict records "not found in searched scope"
  (no absolute claim).
- Forbidden: non-molecular/structural levers (geometry, transport, kinetics overrides, system switches).

**Degree-of-freedom boundary:** composition formula only. Everything else locked (Chen2020 cell profile, bridge rule fixed).

## Objective decomposition

- Gate 1 (B): CHGNet computed avg voltage >= 4.95 V.
- Gate 2 (A): point outside the 84-point Delaunay hull in (V, C, stab).
- Adjudication (D): independent replay + QE + catalog check. Report honest.

## Known-set landscape (from envelope_stats_comp.json, 84 points)

- Layered oxides: V 3.1–4.03 V, C ~160–206 mAh/g, stab −0.99…−3.22. Deepest layered: NiMnMA 4.029 V.
- Olivines: V 3.34–5.114 V, C ~116.6–119.6 mAh/g, stab −1.90…−2.66. Deepest: LiNiCo55 5.1137 V (INSIDE hull, mechanically rejected).
- Excluded outliers: LiNiPO4 7.016 V; LiNi0.4Co0.3Fe0.3PO4 6.067 V (both documented; excluded from hull per pre-registered calibration note).
- Hull geometry: at olivine capacity (C≈117) the upper V bound is ≈5.114 (LiNiCo55 corner). Any point with
  V > ~5.2 at C≈117 is clearly outside. Points with C < 116.66 (below hull C-min) are outside the hull
  automatically (convex combination argument) — mechanical fact of the pre-registered hull.

## Candidate strategy (Round 1 screening, ~16 formulas)

1. **Ni-rich olivines (primary family)** — extend the known olivine corner beyond Ni=0.5:
   LiNi0.55Co0.45PO4, LiNi0.6Co0.4PO4, LiNi0.7Co0.3PO4, LiNi0.75Co0.25PO4, LiNi0.8Co0.2PO4,
   LiNi0.9Co0.1PO4, LiNi0.6Mn0.4PO4, LiNi0.7Mn0.3PO4, LiNi0.6Co0.2Mn0.2PO4.
   Rationale: CHGNet olivine voltage rises steeply with Ni fraction (Ni0.5Co0.5 = 5.11 → Ni1.0 = 7.02);
   Ni>0.5 compositions land above the hull's max-V corner → outside hull, V>=4.95.
   **Risk (disclosed):** same CHGNet Ni-olivine overestimate family as the excluded calibration outliers.
   Mitigation = the contract's own closed loop: run-qe gives an independent DFT voltage (literature LiNiPO4 ≈ 5.1 V,
   i.e. the family's real voltage is in the 4.9–5.2 V class). If QE < 4.95 the report says so honestly.
2. **High-voltage spinels** — TM sum = 2 → spinel Fd-3m dispatch: LiNi0.5Mn1.5O4 (LNMO), LiCoMnO4,
   LiNi0.5Mn1.2Co0.3O4, LiNi0.4Co0.1Mn1.5O4. Capacity ≈102–104 mAh/g < hull C-min (116.66) →
   envelope passes automatically IF V >= 4.95 (V is the question; CHGNet spinel V likely 4.5–4.9).
3. **Layered probe (ceiling confirmation):** LiNi0.9Mn0.05Mg0.05O2 — expected ≤ ~4.05 V (family ceiling).
4. **Fluorophosphate domain-limit probe:** Li2NiPO4F (P-containing → olivine dispatch with F approximated; disclosed).
   C ≈ 100.6 mAh/g → automatically below hull C-min.
5. **Mechanical control:** LiNi0.5Co0.5PO4 (= documented LiNiCo55) — must reproduce ≈5.11 V and be REJECTED by the
   envelope checker. Validates replayability of the adjudicator.

## Budget allocation

- Round-1 screening: ~16 candidates x 2 CHGNet states (RTX 4060, ~20–40 s/state) ≈ 10–25 min.
- Envelope adjudication: seconds (Delaunay test).
- run-qe finalist: olivine primitive 28 atoms, 3 states (full vc-relax + delith relax + Li metal), 32 cores.
  Estimated several hours — background. Extend `_PSEUDO_FILES` with P (sssp file present: P.pbe-n-rrkjus_psl.1.0.0.UPF);
  documented tool extension sanctioned by cli-commands.md.
- MP/catalog check: web search of Materials Project for the finalist formula (no API key in .env).

## Risk & fallback

- If no candidate clears BOTH gates (V>=4.95 AND outside hull) → honest negative result per contract.
- If screening passes but QE < 4.95 → report both numbers; verdict notes the CHGNet-family overestimate; final
  conclusion reflects the QE value (true-DFT signature is the endorsement, per protocol).
- If QE crashes/non-converges → record verbatim; contract says convergence failures recorded honestly.

## Domain references (directional basis)

- LiNiPO4 olivine ≈ 5.1 V vs Li (literature; e.g., Wolfenstine & Allen, J. Power Sources 2005 — domain memory, direction only).
- LNMO LiNi0.5Mn1.5O4 ≈ 4.7 V (well-documented high-voltage spinel).
- LiCoMnO4 ≈ 5.0 V (5-V spinel class, domain memory).
- CHGNet Ni-olivine overestimate: this repo's own pre-registered calibration note (envelope_stats_comp.json "excluded").
