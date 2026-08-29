# Simulated Peer Review Package (ars-reviewer, full mode)
## Manuscript: "When Design Decisions Go to the Agent: A Governance Experiment in a Virtual Battery Factory"
### Reviewed 2026-08-26 against main.pdf (49 pp), supplementary.pdf (6 pp), audit_integrity_report.txt (58 mechanical checks)

---

## Phase 0 — Field Analysis & Reviewer Configuration

**Field**: management science / engineering management (primary); AI-agent systems and electrochemical simulation (secondary). Paradigm: controlled experiment with a treatment-plus-two-controls design. Maturity: full draft, pre-submission.

| Reviewer | Identity | Focus |
|---|---|---|
| EIC | Editor, management-science/engineering-management journal | Fit, originality, significance, presentation |
| R1 Methodology | Experimental design & measurement scholar | Design validity, controls, inference strength |
| R2 Domain | Battery-simulation + LLM-agent researcher | Literature coverage, technical claims, contribution vs. BSA |
| R3 Perspective | Organizational/AI-governance scholar | Practical implications, theory connections, transferability |
| DA | Devil's advocate | Core-argument attacks, strongest counter-explanations |

---

## Phase 1 — Review Reports

### R1 — Methodology Reviewer

**Overall: strong design, three inference gaps.**

*Major 1 — Inference from single ablation cells.* The voting-off null result ("zero verdict changes", §5.3) rests on N=1 per ablation cell. With one run per (mechanism × task) cell, a null cannot be distinguished from noise. The claim "an unrealized premium" is presented as a measured fact; it is a measured *absence in one run*. Recommend either (a) soften to "no verdict change was observed in this suite" and move the mechanism-decomposition claim to supplementary, or (b) run one more seed for the three voting-off cells.

*Major 2 — C1 fairness hinges on a prompt-design choice.* C1's system prompt includes a deliverable request ("write your final design to design_summary.md... as applicable") but no criterion discipline. A hostile reading: the authors *selected* the yardstick-failure behaviors by choosing a C1 prompt that invites self-reporting. The paper anticipates this (§4.2 resource symmetry), but the rebuttal should be made explicit in §6: why is "same tools, same budget, no protocol" the right counterfactual for the governance claim, and what would a *fairer* C1 look like (e.g., C1 + a pre-registration-only rule) and would it change the result? Consider adding a one-paragraph robustness discussion.

*Major 3 — BO penalizer mismatch is double-edged.* The paper correctly notes BO's penalizer hardcodes 60 °C, so the T6 50 °C red line was invisible (§5.1). But that is a *setup choice the authors made* for C2. A reviewer may ask: why not run a C2 variant with the aligned penalizer? Either run it (cheap: 50 evaluations) or preempt: "we deliberately left the penalizer at its published standard to measure the baseline as published, not as re-engineered; the mismatch is itself evidence of the blindness claim." The paper states the fact but not the decision rationale.

*Minor 1 — "Assistant messages" metric needs the harness turn unit.* §4.2 now defines the budget setting vs. the log-derived metric; good. Add one sentence stating the observed bound (C1-T6 hit the cap at 443 assistant messages) so the two units' relationship is empirically anchored.

*Minor 2 — Ablation "no-op" cells (T5 voting-off) are labeled in text but not in Table 5.* The table's ✓ for T5-voting-off could mislead; add a footnote "funnel not exercised in this task (start_stage=3), no-op cell".

### R2 — Domain Reviewer

**Overall: technically sound; contribution framing needs tightening.**

*Major 1 — "Full chain" claim is suite-level, not run-level.* The introduction claims the system "spans the full chain of cell-design levers." In individual runs, most tasks exercise 2-3 levers; the *suite collectively* spans all five. The claim is defensible as written ("the eight scenario contracts we evaluate were chosen so that different tasks must exercise different levers"), but a domain reviewer will want one sentence making the suite-level reading explicit to avoid overclaiming.

*Major 2 — Battery-Sim-Agent comparison deserves a table.* §6.2 sharpens BSA's low-headroom calibration in prose. A compact comparison table (task type, objective, baseline, agent result, BO result, adjudication mechanism) would let battery/agent reviewers see the positioning in one glance. Consider supplementary.

*Major 3 — The SEI criterion's model dependence.* The SEI ≤500 nm criterion reads a state variable of a specific degradation model (Chen2020 kinetics). The paper handles this well (caliber definitions, C1 re-adjudication), but §4.1 should add one clause: criterion values are model-relative; cross-system comparisons are only made within the same model. This is currently in the supplementary re-adjudication rules but not in the main text.

*Minor — LNMO parameter set provenance.* The case study uses "library LNMO.json"; cite its origin (custom parameter set? derived from a paper?) or state "author-provided parameter set" explicitly.

### R3 — Perspective Reviewer

**Overall: strong practical contribution; theory bridge can be deepened.**

*Major 1 — The delegation-theory framing is underused in the discussion.* §2.3 imports delegated agency theory (fidelity, governance visibility), and §6.3 maps the four yardstick adjustments to moral hazard. But the mapping is asserted rather than used: the discussion could (a) formalize "delegation fidelity" with the paper's own machinery (fidelity = fraction of criteria measured against the pre-registered thresholds), and (b) draw the deployment boundary conditions as a small theory contribution: "delegation is safe when the contract is machine-readable AND the adjudicator is outside the agent's influence." This would elevate the paper from "an experiment" to "a theory-informing experiment."

*Major 2 — Practical implications could be one checklist.* §7 gives three infrastructural conditions in prose. A boxed three-condition checklist (pre-register / compute / refuse-incomplete) with the corresponding failure observed in C1 for each would be highly citable and MSE-appropriate.

*Minor — "Human exits the loop" language.* §1 says "The human engineer's role ends at the moment the contract is stated." Humans still write contracts and set budgets. Consider "the human's *in-loop* role ends..." to preempt a pedantic objection.

### DA — Devil's Advocate

**The three strongest counter-arguments, and whether the paper survives them.**

1. *"The protocol is just a better prompt."* The governance effect could be reducible to prompt quality: C1 got a five-sentence prompt; G got a 269-line SKILL.md. If so, the paper's "process governance" contribution collapses into "write better prompts." The paper's defense must be: the SKILL.md is *not* prompt content for the model's answers but a set of *external* rules (adjudication is code outside the agent; the verifier refuses incomplete audits; the agent cannot judge itself). The paper states this (§3.2 Component 5) but should name the counter-argument and answer it explicitly in §6.3. **Verdict: survivable, needs one explicit paragraph.**

2. *"BO was handicapped by design."* BO got 10 structural parameters, no material levers, and a penalizer that missed the T6 red line. The paper answers the first two (that IS the solution-space failure), but the penalizer point stands as a setup choice (§R1 Major 3). **Verdict: partially survives; fix the rationale or run the aligned variant.**

3. *"The yardstick failures are what any unmonitored agent does — the result is a foregone conclusion."* The value claim is not that C1 fails but that the four failure *modes* are distinguishable, mechanically detectable, and each maps to one governance component that prevents it. The paper does this (§5.5 Table) but could add one sentence: the contribution is the *taxonomy and its mechanical detection*, not the fact of failure. **Verdict: survives with one clarifying sentence.**

4. *Cherry-picking check*: the paper reports the flash-T6 audit-tail defect, the voting null, the two harness env-failures, and the C1 out-of-space cases — no evidence of selective reporting. The audit report independently confirms 58/58 table values against artifacts. **Pass.**

---

## Phase 2 — Editorial Synthesis

**Consensus (all reviewers)**: the design is strong, the honesty infrastructure is a genuine differentiator, and the writing is clear. No reviewer disputes the core result.

**Disagreements**: none blocking; the actionable disagreements are R1-M3 (BO penalizer), R2-M1 (suite-level claim), R3-M1 (theory formalization) — all addressable in revision.

**Decision: MAJOR REVISION.**

**Revision Roadmap (prioritized):**
1. (R1-M3) BO penalizer: either run the aligned-penalizer variant (50 evals, cheap) or add the decision rationale paragraph. *Do this — one run removes the objection entirely.*
2. (R1-M1) Soften the voting-off null to "no verdict change observed"; keep the meta-finding (molecular path taken more often).
3. (DA-1) Add the explicit "protocol ≠ prompt" paragraph in §6.3.
4. (R1-M2) Add the C1-fairness robustness paragraph in §6.
5. (R2-M1) One sentence: full-chain claim is suite-level.
6. (R3-M1) Formalize delegation fidelity with the paper's own machinery; three-condition checklist in §7.
7. (R2-M2) BSA comparison table (supplementary).
8. (Minors) R1-M1 (anchor the turn units empirically), R1-M2 (no-op footnote), R2-M3 (model-relative SEI clause in §4.1), R2-minor (LNMO provenance), R3-minor ("in-loop role ends").
9. (Mechanical — already fixed pre-review) §4.6 title, §5.6→§5.8 cross-refs, repo-name spelling.

**Editorial note**: the mechanical integrity (audit 58/58 with one documented defect) is exceptional for an agent-systems paper; the revision should preserve this discipline.
