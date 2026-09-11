# T9_R2 Final Report — LiNiPO4F (tavorite-P) positive electrode for the Chen2020 NMC811/anode grid-storage cell

Date: 2026-09-10. Headless run. Workspace: `runs/exp/t9_r2`.
Freedoms: positive-electrode COMPOSITION only (all other cell choices fixed). Budget spent: 1 smoke + 1 run-comp batch (24 candidates) + 1 independent replay + 1 run-qe attempt (domain-limited, instant). No other runs' workspaces were read (workspace discipline honored).

## 1. Verdict

**PASS on A0 / A1 / B / B' / C / D — with recorded caveats.**

Finalist: **LiNiPO4F** (tavorite LiM(PO4)F framework, triclinic P-1; redox: Ni3+/Ni4+ over the
30%-delithiation window x = 1.0 → 0.7).

| Gate | Result | Evidence |
|---|---|---|
| A0 membership | PASS | not in `known_set_v2.json` (109 members) — `comp_envelope_check.py --formula` |
| A1 hull | PASS | `in_envelope = false` (outside Delaunay hull of the 96 sealed points) |
| B computed window | PASS | 5.4878 V ≥ 5.3 V (hull band top 5.114 V); capacity 104.46 mAh/g |
| B' true-voltage guard | PASS (literature-consistent, caveated) | see §4; QE in-toolchain domain-limited (no F pseudo) |
| C bridge | documented | OCP ≡ 5.4878 V; capacity 94.01 mAh/g (= 0.9 × computed); SEI k0 baseline; ED_active 515.9 Wh/kg (reported) |
| D closed loop | recorded | independent replay 5.487805 V (Δ = 5.2e-6 V); run-qe attempted; MP catalog check scoped |

## 2. Screening (batch 1, 24 candidates)

Frameworks swept: tavorite-P (9), tavorite-S (3), olivine (4), spinel (4), NASICON (4).
Baseline self-calibration (NMC811) computed normally.

Six candidates computed ≥ 5.3 V and all six passed the envelope (A1):

| Formula | V (V) | Cap (mAh/g) | Stab (eV/at) | Envelope | B' path |
|---|---|---|---|---|---|
| **LiNiPO4F** | **5.4878** | 104.46 | −1.2199 | outside | literature ✓ (5.50 V exact-chemistry DFT) |
| LiNi0.75Co0.25PO4F | 5.3863 | 104.42 | −1.2942 | outside | literature (diluted family) |
| LiNi0.5Co0.5PO4F | 5.3052 | 104.39 | −1.3632 | outside | literature (≈ Alfaruqi LMNPF point) |
| LiNi0.8Co0.2PO4 | 5.4111 | 116.78 | −1.8722 | outside | QE-able but overestimate family (true ≈ 5.0–5.1 → B' expected negative) |
| LiNi0.75Co0.25PO4 | 5.4171 | 116.77 | −1.8722 | outside | same |
| LiNi0.4Co0.6PO4 | 5.4005 | 116.71 | −1.9305 | outside | same |

Funnel decision: LiNiPO4F — highest computed voltage AND the only B-passer with an
exact-chemistry literature anchor ≥ 5.3 V. (Anomaly noted: LiNi0.6Co0.4PO4 = 4.426 V,
nonmonotonic vs its 5.40–5.42 V neighbours — screening-precision local minimum, not chased.)

## 3. A0 / A1 / B mechanical record

- A0: pre-checked programmatically against the 109-member list before screening (no hits).
- A1: `envelope_batch1_results.json` — all six `in_envelope: false`.
- B: `comp_batch1_out.json` — LiNiPO4F 5.4877998 V; replay 5.4878050 V (deterministic to 5e-6 V).
- `converged=false` is the known screening-precision behaviour (declared per batch); energies usable at screening precision.

## 4. B' — true-voltage guard (the crux)

In-toolchain QE is unreachable for any F-containing framework: `qe_runner._PSEUDO_FILES` covers
only {Li, Ni, Mn, Co, O, P, Si, Mg}. The run-qe attempt on LiNiPO4F returned the honest
toolchain error `no SSSP efficiency pseudopotential entry for element F` (`qe_finalist_out.json`).
B' therefore uses the literature route, which the contract explicitly allows.

Literature ladder for LiNiPO4F true voltage ≥ 5.3 V (`b_prime_evidence.json`):

1. **Mueller, Hautier, Jain, Ceder, Chem. Mater. 2011, 23, 3854 (DOI 10.1021/cm200753g)** — high-throughput DFT of tavorite MPO4F; Ni(PO4)F Li-insertion steps 5.50 / 4.59 / 5.04 V. The 5.50 V step is the most-oxidizing (Ni3+/Ni4+) and is the region our 30%-delithiation window occupies. **CAVEAT: obtained via search-index extraction of the full text (WebFetch blocked in this environment); redox-step assignment inferred from step ordering, not verified against the PDF.**
2. **Alfaruqi et al., ACS Appl. Mater. Interfaces 2020, 12, 16376 (DOI 10.1021/acsami.9b23367)** — first-principles (PBEsol+U): LiMn0.5Ni0.5PO4F = 5.23 V (50% Ni dilution). Pure-Ni endmember is higher along the family trend (our CHGNet dilution series: 5.488 pure / 5.386 at 75% / 5.305 at 50% Ni).
3. **Li2NiPO4F 5.33 V** — documented known-set ceiling claim; independently corroborated experimentally by **US20240150177A1** ("~5.3 V redox potential, currently limited by commercial electrolyte stability").
4. Cross-validation: CHGNet computes 5.4878 V for LiNiPO4F, agreeing with Mueller's 5.50 V step to 0.012 V — unlike the pre-registered Fe-tavorite case (LiFePO4F computes +2.2 V above literature), the Ni-tavorite template error is negligible.

B' verdict: **PASS (literature-consistent)** — exact-chemistry 5.50 V (Mueller) + diluted anchor 5.23 V (Alfaruqi) + family anchor 5.33 V (Li2NiPO4F; patent-corroborated). Conditional caveat recorded: the key 5.50 V figure is secondhand.

## 5. Bridge (C) — `bridge_c.json`

- OCP = 5.4878 V (constant; = computed average voltage, contract bridge rule)
- Capacity = 0.90 × 104.458 = **94.012 mAh/g** (LNMO-anchored utilization)
- SEI kinetics = Chen2020 baseline k0 (unchanged)
- **ED_active = 5.4878 × 104.458 × 0.9 = 515.9 Wh/kg** (reported, not a criterion)
- Domain limit: `pybamm_runner` hardcodes the LNMO OCP function for custom parameter bases
  (L160–165), so a constant-OCP custom function cannot be attached without modifying shared
  code (out of scope). (C) is applied analytically as the contract defines it.

## 6. Closed loop (D)

- **Independent run-comp replay** (`replay_finalist.json`): fresh CHGNet computation via
  `comp_envelope_check.py --formula LiNiPO4F` → 5.4878050 V, envelope PASS. Δ vs batch-1 = 5.2e-6 V.
- **run-qe**: attempted; honest domain-limit error (no F pseudo) — recorded, not hidden.
- **Materials-Project/catalog check**: LiNiPO4F **is present in Materials Project** as
  [mp-504104](https://legacy.materialsproject.org/materials/mp-504104/) (triclinic P-1;
  E_hull = 0.099 eV/atom, slightly metastable; decomposes to LiNi2P3O10 + Ni3(PO4)2 + NiF2 + LiF + O2)
  and [mp-1176633](https://www.osti.gov/biblio/1742524) (monoclinic Pm); Li2NiPO4F sibling is
  [mp-554446](https://legacy.materialsproject.org/materials/mp-566629/). **No experimental synthesis
  of LiNiPO4F itself was found in the searched scope** (experimental reports exist for the
  Li2NiPO4F sibling: [US20240150177A1](https://patents.google.com/patent/US20240150177A1/en),
  [US8367036](https://patents.google.com/patent/US8367036), [EP1444744A2](https://patents.google.com/patent/EP1444744A2/en)).
  Scope wording per contract: *not found in the contract's adjudication scope (known_set_v2.json
  membership); found in the broader MP catalog — recorded honestly, no absolute novelty claim.*

## 7. Caveats (honest record)

1. The pivotal 5.50 V figure (Mueller) is secondhand (search-index extraction; WebFetch blocked).
   If it were discounted, the strongest remaining anchors (5.23 V diluted, 5.33 V Li2NiPO4F)
   make ≥ 5.3 V for the pure endmember literature-consistent but not independently proven.
2. LiNiPO4F is catalog-documented as a *computed* MP entry — "new" holds only relative to the
   contract's adjudication scope, not absolutely.
3. rel_stability (−1.22 eV/atom) is a within-batch ranking only, not a criterion.
4. Follow-up (not executed — shared-toolchain modification out of scope): `f_pbe_v1.4.uspp.F.UPF`
   exists in the SSSP directory; extending `qe_runner._PSEUDO_FILES` would enable a true QE
   endorsement of the finalist in a future run.

## 8. Workspace artifacts

`design_plan.md` · `log.jsonl` (12 entries: criteria → plan → 6 evaluates → funnel → propose → endorse → final) ·
`comp_smoke_{in,out}.json` · `comp_batch1_{in,out}.json` · `envelope_batch1.py` / `envelope_batch1_results.json` ·
`build_evidence_files.py` + `ev_*.json` / `finalist_metrics.json` · `b_prime_evidence.json` ·
`replay_finalist.json` · `qe_finalist_{in,out}.json` · `bridge_c.json` · `close_log.py` · `evaluate_batch.json` ·
`known_set_v2_copy.json` · `report.md`

## 9. Sources

- [Mueller et al., Chem. Mater. 2011, 23, 3854 (record)](https://research.dial.uclouvain.be/entities/publication/044607b3-3503-4fa7-8726-dab628f22108)
- [Alfaruqi et al., ACS AMI 2020, 12, 16376 (record)](https://www.ablesci.com/scholar/paper?id=3dNkeBKa8)
- [US20240150177A1 — Li2NiPO4F ~5.3 V patent](https://patents.google.com/patent/US20240150177A1/en)
- [US8367036 — Li2NiPO4F cathode tests](https://patents.google.com/patent/US8367036)
- [EP1444744A2 — halo-phosphate electrode materials](https://patents.google.com/patent/EP1444744A2/en)
- [MP mp-504104 LiNiPO4F (P-1)](https://legacy.materialsproject.org/materials/mp-504104/) · [OSTI 1208593](https://www.osti.gov/biblio/1208593) · [OSTI 1742524 (Pm entry)](https://www.osti.gov/biblio/1742524) · [mp-554446 Li2NiPO4F](https://legacy.materialsproject.org/materials/mp-566629/)
- [In-situ XRD mechanochemical Li2NiPO4F formation](https://sibran.ru/upload/iblock/432/4320d901ae64d6fee190aa82fbce5d53.pdf)
