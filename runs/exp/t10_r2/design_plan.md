# Design Plan — t10_r2 (SEI-forming additive for grid storage, Chen2020 NMC811/graphite)

## Objective decomposition (decision-layer thresholds)

| Layer | Metric | Threshold | Source |
|---|---|---|---|
| stage1 (molecular) | total energy (mace) | ≤ 0.0 eV | funnel hard line |
| stage1 | xTB HOMO | ≤ −6.0 eV (funnel hard line); ≤ −13.74 eV (property window) | contract (B) |
| stage1 | envelope | OUTSIDE 82-point hull (Delaunay) | contract (A) |
| stage2 (cell) | SEI thickness @100 cyc, 1C | ≤ 370 nm | contract (C) |
| stage2 | energy density | ≥ 327.18 Wh/kg | contract (C) |
| stage3 (safety) | thermal-runaway during 4C charge | triggered = false | contract (C) |

Expected trade-off direction: the only lever is the additive's xTB HOMO → SEI kinetic rate constant via the
pre-registered k-rule. Deeper HOMO ⇒ smaller k ⇒ thinner SEI (better). No ED/safety coupling: the additive
parameter (`SEI kinetic rate constant [m.s-1]`) enters only the aging model, so 1C-discharge energy density
and 4C-charge thermal behavior are identical to baseline for every candidate (expected ≈ baseline values).

## Candidate strategy

The envelope requirement forces novelty: every one of the 82 documented compounds (deepest = triflyl fluoride,
xTB HOMO −14.14 eV) is *inside* the hull and is mechanically rejected. A passing candidate must either (i)
push xTB HOMO beyond the deepest vertex (HOMO < ≈ −14.14 eV) or (ii) land on an unusual (MACE, CHGNet)
per-atom-energy combination outside a hull facet.

Direction: maximize electron withdrawal per atom → deeply bound HOMO + strongly negative per-atom ML energy.
Round-1 scaffold families (all novel relative to the 82, none identical to a documented SMILES):
  - sulfonyl fluorides beyond triflyl fluoride: sulfuryl fluoride SO2F2, cyanosulfonyl fluoride, fluorosulfonyl isocyanate
  - perfluoro nitriles / cyanogen fluoride
  - trifluoronitromethane (CF3-NO2; nitromethane is documented, CF3-NO2 is not)
  - bis(trifluoromethyl)sulfone (CF3)2SO2, pentafluoroethylsulfonyl fluoride C2F5SO2F
  - CF3-SF5 (trifluoromethyl sulfur pentafluoride) — extremely electron-poor, deep HOMO
  - sulfuryl chloride fluoride SO2FCl

Fallback direction if none lands outside the hull: push further electron withdrawal (SF5-sulfonyl fluorides,
bis-sulfonyl imides) or a deliberately unusual per-atom-energy branch (highly strained / multi-F small ring).

## Budget allocation

- Round 1: 10 candidates through the full funnel (mace → chgnet → xtb → envelope_check).
- Envelope passes + HOMO ≤ −13.74 → advance to cell (k-rule → aging_1C_100cyc → 1C_discharge + calc-energy → 4C_charge_45C + run-tr).
- ~4–6 rounds budgeted for candidate generation; negative result reported honestly if exhausted.

## Risk & fallback plan

- Risk 1 (biggest): no generated molecule beats triflyl fluoride's −14.14 eV HOMO in xTB GFN2 → cannot exit the hull on the HOMO axis. Fallback: exploit the (MACE, CHGNet) axes — deep-per-atom-energy, unusual composition.
- Risk 2: a molecule exits the hull but its k-rule k still yields SEI > 370 nm. Fallback: deepen HOMO further / re-check k-rule arithmetic.
- Risk 3: RDKit/xtb embed failure on hypervalent S (SF5). Fallback: drop that candidate, note honestly.
- Risk 4: 4C-charge plating (baseline) — this is a locked-architecture property, additive-neutral; recorded as observation, not a pass/fail gate (task does not require plating=no).

## References (domain basis)

- Deep HOMO via perfluorinated/strong-EWG substituents → domain experience (no precise source).
- Sulfonyl-fluoride SEI chemistry (S=O/F → LiF/SO2-rich SEI) → domain experience.
- Chen2020 SEI kinetic-rate-constant coupling to additive HOMO → pre-registered k-rule in this contract.

## Revision history

- v1 (2026-09-09): initial plan.
