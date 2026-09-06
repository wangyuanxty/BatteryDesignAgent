---
Author response status (2026-09-07): M1 RESOLVED (abstract + §6.1 reworded);
minor #2/#3/#4 RESOLVED (Table 3 T6 cell, Fig. 8 caption note, limitations
naming of the two defect runs); #6 partially RESOLVED (grep sweep run,
one instance fixed, final pass advised before submission). #1 and #5 left
as optional polish — trail table widened further; §5.6 sentence placement
judged acceptable. Compile: main.pdf 62 pp + supplementary.pdf 16 pp,
citations 59/59, floats 27/27, audit 135 checks with the 2 disclosed
defects only.
---

# Reviewer Comments — Round 3 (ars-reviewer, full mode)

Target: Management Science and Engineering (international)
Manuscript: "When Design Decisions Go to the Agent: A Governance Experiment in a Virtual
Battery Factory" — main.pdf (61 pp) + supplementary.pdf (16 pp) + audit_integrity_report.txt
(135 checks, 2 known-and-disclosed audit-chain defects)

Overall: the manuscript is in good shape and the changes since Round 2 (four-model matrix,
compression 74→61 pp, figure cleanup, em-dash hygiene) move it forward. One internal
inconsistency and a handful of presentation issues remain. Recommended decision: MINOR
REVISION (single consistency fix, no new experiments).

---

## MAJOR (one)

**M1. The three-model voting narrative contradicts the paper's own results.**

- Abstract: "heterogeneous three-model voting was never exercised in this suite"
- §6.1 (Discussion): "the molecular funnel was never entered, so its three-model vote was
  never exercised"
- But §5.3 (Ablation): "with the three-model vote off, the molecular path was actually
  taken *more* often (six molecules ...)", and the T6 trail (Table 7, Funnel row) records
  "candidates benchmarked by three-model vote ... four molecules below the HOMO line";
  §5.4 also describes flash-T5 reaching LNMO via the material funnel with FEC/VC/PES/DTD
  passing the funnel.

The funnel was entered and the vote was **exercised** (in the multi-candidate ranking
sense) in at least T5/T6; what the ablation shows is that the vote was never
**dispositive**: disabling it changed no verdict. "Never exercised" / "never entered" is
factually wrong and a careful reviewer will catch it (the contradiction is visible within
a single page span). Fix by rewording both places, e.g.:
- Abstract: "...the molecular funnel's three-model vote was exercised but never
  verdict-changing in this suite"
- §6.1: "...in this suite the funnel's vote was never entered as a roadblock: it was
  exercised but never dispositive, because the cheapest routes (parameter bridges and
  system switches) always sufficed"

---

## MINOR

1. **Table 7 (round trail) density.** The five-column longtable still hyphenates
   aggressively in the reasoning column ("arti-facts", "ratio-nale", "bottle-neck").
   Standard typesetting behavior in narrow columns, but consider one more widening of the
   reasoning column (or dropping the verbatim thinking quotes to the supplementary for the
   two longest rows, R03/R06), if page budget allows.

2. **Table 3: residual cell wrap.** The C1 cell "(budget)" on T6 breaks after the open
   parenthesis (no internal break point). Suggest "× budget exhausted" or re-wrapping the
   cell content ("$\times$ (budget)") with an explicit break opportunity.

3. **Fig. 8 caption vs panels.** Caption says "T1: 553.98 vs 459.4 Wh/kg and a plating
   failure on both foreign-vendor legs", but the bars themselves carry only the ED values
   (the luna/mimo bars sit above the contract line with a red outline). The caption is
   correct; consider adding "(red outline = failed criterion)" to the note line so the
   symbol is self-explanatory.

4. **Known audit defects exposure.** The audit report contains two disclosed FAILs
   (t6flash, t1mimo missing final ledger entry). Both are documented in Section 5.4 and
   the Table 3 note; consider one explicit sentence in the Limitations "(i) Replication"
   naming the two runs by ID, so a reviewer does not have to re-derive them from the
   supplementary ledger.

5. **Post-compression §5.6 flow.** The compressed walk-through reads cleanly; one nit: the
   sentence "the trail also shows the multi-precision discipline working at the cell
   scale" arrives before the reader has seen the DFN flip described in the trail table.
   Consider moving it to after the mechanical-adjudication paragraph (which already
   narrates R06), or keep one clause of anticipation.

6. **Em-dash hygiene aftermath.** The automated conversion produced a handful of
   restructured sentences; spot checks pass, but one instance required a manual fix
   ("metadata: which" → "metadata, which"). Please re-read the conversion diff once for
   similar relative-clause constructions before submission (grep for `: which/that/and`).

---

## What is NOT a problem (verified)

- Four-model matrix consistency: abstract/intro/conclusion/§6.1(i)/Table 3 agree
  (8/8 pro+flash, 4/8 luna, 4/8 mimo, {T2,T3,T7} four-model stable set).
- "32-run matrix + 12 ablations" arithmetic: 8×4 = 32 ✓.
- Figures: Fig 9 (three panels) is clean; Table 3/6 now wrap at word boundaries.
- Data-paper reconciliation: 135 audit checks; the 2 FAILs are documented defects, and
  the audit's own regression-test story is a strength of the paper.
- Supplementary T6 section carries the moved materials without loss (candidate sheet,
  datasheet, design params, two curves, and the "deliverable labels its own estimates"
  observation).

## Suggested decision

MINOR REVISION. M1 is a ten-minute reword with no experimental impact; the rest is
polish. No further runs required.
