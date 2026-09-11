# Design Plan — t9_r1

## Case
Design a **NEW SEI-forming electrolyte additive** for a grid-storage cell on the
**Chen2020 NMC811/graphite** system (base = Chen2020, start_stage = 2,
real_compute = false).

## Objective decomposition (decision-layer thresholds, verbatim from task)

| Layer | Metric | Threshold | Verdict rule |
|---|---|---|---|
| stage1 (molecular) | mace/chgnet `converged` | true | must converge |
| stage1 | `energy_ev` (mace/chgnet) | ≤ 0.0 eV | `{"max": 0.0}` |
| stage1 | `homo_ev` (xtb) | ≤ −6.0 eV | `{"max": -6.0}` |
| stage2 (cell) | `energy_density_wh_kg` | ≥ 327.18 | `{"min": 327.18}` |
| stage2 | `sei_thickness_nm_end` (aging 1C ×100) | ≤ 550 nm | `{"max": 550.0}` |
| stage3 (safety) | `triggered` (thermal runaway) | false | equality |
| stage3 | `plated` (4C charge) | false | equality |

**Trade-off expectation.** The binding novelty constraint is molecular (additive
must be NEW, ∉ {FEC, VC, PS, DTD} and ∉ project candidates). Cell-level metrics
are expected to be non-binding on the baseline: Chen2020 baseline 100-cycle SEI
is ≈ 449 nm (already < 550), and energy density is a cell-architecture property
(unchanged by a trace additive, electrolyte excluded from mass). The real
design work is therefore (a) invent a novel, plausible SEI former that clears the
three-model funnel, and (b) map it — via an **explicitly labeled estimate** — to a
reduced SEI growth rate, which is the only molecular-to-cell lever permitted.
No cell-parameter override (geometry/transport/SEI-constant-as-solution/system)
is used.

## Candidate strategy (round 1)

Propose 4 novel cyclic-carbonate/sulfite SEI formers with electron-withdrawing
(F) or polymerizable (vinyl) substituents → high reduction potential → reduced
preferentially before electrolyte to build a dense LiF/SO₃-rich SEI:

1. **FVC** — 4-fluoro-1,3-dioxol-2-one (fluoro-vinylene carbonate), `O=C1OC=C(F)O1`
2. **DFEC** — 4,5-difluoro-1,3-dioxolan-2-one, `O=C1OC(F)C(F)O1`
3. **FES** — 4-fluoro-1,3,2-dioxathiolane 2-oxide (fluoro-ethylene sulfite), `O=S1OC(F)CO1`
4. **VEC** — 4-vinyl-1,3-dioxolan-2-one (vinyl ethylene carbonate), `C=CC1OC(=O)O1`

All four are mechanically distinct from the exclusion set (FEC `C1OC(=O)OC1F` /
`FC1COC(=O)O1` / `O=C1OC(F)CO1`, VC `O=C1OC=CO1`, PS `O=S1(=O)CCCO1`, DTD
`O=S1(=O)OCCO1`).

**Follow-up direction**: rank passers by (energy, HOMO) ascending; if any
candidate is disputed (three-model spread) or eliminated, generate a substituent
variant (add/reposition F, or swap carbonate→sulfite).

## Parameter bridge (molecular → cell, estimate-labeled)

The additive's cell effect is SEI-growth suppression. Bridge =
`"SEI kinetic rate constant [m.s-1]"` (coating suppressing SEI growth,
ec-reaction-limited). The winning additive is mapped to a **conservative**
reduction — ×0.5 of the Chen2020 baseline SEI kinetic rate constant — labeled as
a domain **estimate** (FEC-class strong film formers are routinely reported to
slow SEI growth; signal-scale reference from SKILL: Chen2020 kinetics ×0.1 →
449→385 nm). The reduction is the additive's mechanism, NOT the solution; the
path is the molecule. Transport (σ/t⁺/D), geometry, and system are locked.

## Budget allocation

- Stage 2 funnel: 1 round, 4 candidates × (mace + chgnet + xtb) = 12 sub-runs.
- Stage 3 cell: baseline 1C discharge (SPMe) + calc-energy; baseline aging;
  additive aging (SEI-constant ×0.5). ≈ 4 run-pyamm + 1 calc-energy.
- Stage 4 safety: 4C charge (thermal lumped + plating), overcharge, run-tr. ≈ 3.
- Closing: log-evaluate, render, endorse (skipped: real_compute=false), final.
- Total budget ≈ 2–3 rounds; no re-planning unless three-strike triggers.

## Risk & fallback plan

- **Risk 1 — funnel elimination** (embed failure / HOMO > −6 eV / energy > 0).
  Fallback → Stage 2: substituent variant generation; the funnel is a fast loop.
- **Risk 2 — energy density < 327.18 on baseline.** Architecture/transport are
  locked, so this cannot be "tuned"; if it fails, the gap is attributable to the
  base system, recorded honestly, and the additive (unchanged ED) cannot close
  it — would be reported as a negative on that metric. (Checked first in Stage 3
  via baseline calc-energy before committing the additive mapping.)
- **Risk 3 — 4C charge plating/thermal on baseline.** Same: locked levers mean
  the additive (SEI-only effect) cannot move 4C plating/T_max; recorded honestly
  if baseline fails. (SKILL note: Chen2020 has no plating params → defaults
  injected with trace; T_max may be approximate — marked as such.)

## References (domain basis; real sources only)

- Direction: fluorinated cyclic carbonates (FEC-class) form LiF-rich, denser SEI
  that slows continued growth → Zhang, S. S., *J. Power Sources* 162 (2006)
  1379–1394 ("A review on electrolyte additives for lithium-ion batteries").
- Direction: electrolyte/additive fundamentals and SEI chemistry → Xu, K.,
  *Chem. Rev.* 104 (2004) 4303–4417.
- Direction: sulfur-containing additives (sulfite/sultone) → Li₂SO₃/Li₂SO₄-rich
  SEI, improved thermal stability → domain experience (no precise source).
- Direction: SEI growth-rate calibration signal (Chen2020 kinetics ×0.1 →
  449→385 nm) → this skill's SKILL.md Stage-3 note (measured signal scale).
