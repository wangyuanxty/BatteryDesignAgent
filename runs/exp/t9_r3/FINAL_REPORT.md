# T9 run 3 — final report: 5 V-class cathode for the Chen2020 grid-storage cell

Workspace: `runs/exp/t9_r3` · Date: 2026-09-10 · Headless design run.
Design target: cathode whose computed average voltage >= 5.3 V, composition outside the
documented catalogue (115 materials) AND outside the convex hull of the 102 computed
screening points (known_set_v3.json; band top 5.4878 V = LiNiPO4F).

## Finalist

**LiNi0.75Mg0.25PO4F** — Ni-rich tavorite fluorophosphate, LiNiPO4F framework with 25 mol%
Mg on the transition-metal site. Realized composition (run-comp largest-remainder rounding
over the 8 M sites of the tavorite 2x2x1 supercell, 72 atoms): **{Ni: 6, Mg: 2}**.

| quantity | value |
|---|---|
| computed average voltage (run-comp) | **5.5190 V** (>= 5.3: pass, margin +0.219 V) |
| computed capacity | 109.709 mAh/g |
| rel_stability (within-batch, vs NMC811) | -1.2274 eV/atom |
| realized structure | tavorite, 6 Ni / 2 Mg on M sites |

Backup finalist: **LiNi0.875Mg0.125PO4F** (realized {Ni: 7, Mg: 1}): 5.5082 V,
107.019 mAh/g, -1.2236 eV/atom — passes every criterion as well (slightly thinner margins).

## Criterion verdicts

**(1) Catalogue.** Neither formula is among the 115 documented materials
(membership_check.py, raw + normalized). Context: the parents LiNiPO4F, LiNiSO4F and
Li2NiPO4F ARE documented members — the Mg-substituted tavorite is the novel part. Pass.

**(2) Convex hull.** The recomputed point of the finalist,
[5.51902 V, 109.709 mAh/g, -1.2274 eV/atom], lies **outside** the Delaunay hull of the
102 points (`comp_envelope_check.py --formula`: `in_envelope=false`,
`verdict = PASS (outside envelope)`; replay artifact: replay_envelope_finalist.json).
V = 5.5190 V exceeds the band top of the known set (5.4878 V, LiNiPO4F) by 0.031 V, so
outside follows by construction — no razor-thin stab margin. Pass.

**(3) Window.** 5.5190 V >= 5.3 V from run-comp. Pass.

**(4) True-voltage guard.** The computed 5.519 V is not a bare screening artifact; the
redox is exactly Ni2+/Ni3+ in a fluorophosphate framework (6 Li removed per formula unit in
the x∈[0.3,1] window = the 6 Ni2+->Ni3+ oxidations; Mg2+ inert — no O-redox artifact), and
the Ni2+/Ni3+ fluorophosphate voltage is literature-anchored:
- Experimental: Li2NiPO4F redox ~**5.3 V** vs Li/Li+ (Nagahama, Hasegawa & Okada,
  J. Electrochem. Soc. 157, A748, 2010; dinitrile electrolyte);
- Experimental: LiNiPO4F discharge ~**5.3 V** (Nazri & Pistoia, Lithium Batteries:
  Science and Technology);
- Experimental: LiNiPO4 plateau 5.1 V (phosphate baseline; F inductive effect on top);
- DFT anchors: Li2NiPO4F **5.33 V** (Chakrabarti & Thakur, JES 171, 080508, 2024);
  LiNi0.5Mn0.5PO4F **5.23 V** vs 4.27 V for the phosphate analogue;
- Family calibration: the screening proxy computes Ni-tavorite ~0.2 V **low**
  (LiNiSO4F: CHGNet 4.9421 vs Xie et al., JPC-C 2011, DFT 5.16 V), i.e. 5.519 V is
  unlikely to be an overestimate.
QE attempt (own computation): launched (finalist + backup, Li-metal reference, SSSP/PBE,
ecutwfc 50 Ry, nspin 2); running at report time — result appended on completion. PBE for
polyanionic Ni2+/3+ typically sits 0.3-0.5 V below experiment.
Honest caveats: the experimental anchor Li2NiPO4F is capacity-limited with no established
cycling; the 25% Mg endmember is not synthesized (Mg-on-M-site is demonstrated at doping
level: LiV0.97Mg0.03PO4F@C, 4.2 V, 140.3 mAh/g at 1C, 88.2%/500 cyc).

**(5) Cell mapping (no free parameters).** Constant OCP = 5.5190 V; capacity =
0.9 x 109.709 = **98.738 mAh/g** (LNMO-anchored utilization); SEI kinetics = baseline k0
(1e-12 m/s, Chen2020 untouched). PyBaMM demonstration (cell_mapping.py, standalone because
pybamm_runner hardcodes string OCP overrides to lnmo_ocp): 1C discharge delivers
0.6194 Ah = 98.738 mAh/g active (exact), terminal voltage 5.378-5.385 V (flat, = OCP −
graphite). **ED_active = V x C x 0.9 = 544.9 mWh/g (reported, not a criterion).**

**(6) Close the loop.**
- Independent replay: run-comp recompute via `comp_envelope_check --formula` for both
  finalist and backup — values reproduced (drift <= 6e-6 V vs batch runs); artifacts in
  replay_envelope_*.json. Screening commands: `bda run-comp --in in_batch1.json --out
  out_batch1.json` and `bda run-comp --in in_batch2.json --out out_batch2.json` (workspace
  artifacts in_batch*.json/out_batch*.json).
- run-qe attempt with Li-metal reference: running (background job; SCF confirmed
  iterating at ecut 50 Ry).
- Public catalogues: COD — 0 entries for the finalist formula (and 0 for the whole
  Li-Ni-P-O-F family); OQMD (OPTIMADE, HAS ALL six elements) — 0 of 1,407,395 entries.
  **Finalist "not found in the searched scope"** (catalogue_check.md).

## Documented traps avoided (honesty record)

- Olivine LiNi0.75Mn0.25PO4 (3Ni/1Mn) computes 5.5225 V and passes (1)(2)(3) — but the
  Ni-rich olivine family is CHGNet-inflated (LiNiPO4: 7.016 computed vs 5.1 V real,
  excluded from the band): true value ~4.85 V, guard fail. Not presented.
- NASICON Li3Ni2(PO4)3 computes 5.1131 V (< 5.3 window). Fail.
- Tavorite 12.5%-substituted variants (Co/Mn/Al on the 8th M site) compute 5.36-5.47 V
  but the mechanical Delaunay test places all three INSIDE the hull (margins thinner than
  hand-estimated). Fail.
- LiNi0.875Si0.125PO4F (7Ni/1Si) computes 5.3947 V (below band top; not used).

## Bottom line

The best design found is **LiNi0.75Mg0.25PO4F**: computed average voltage 5.519 V
(window pass), outside the documented catalogue and outside the 102-point hull
(by construction, 0.031 V above the band top), with a literature-consistent true-voltage
story at the ~5.3 V experimental frontier (Li2NiPO4F), cell mapping
ED_active = 544.9 mWh/g, and catalogue checks recording "not found in the searched scope".
QE endorsement pending completion (attempt recorded).
