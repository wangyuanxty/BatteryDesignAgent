# t9new_r1 — working notes (session 2)

## Task parse
- Design new positive-electrode composition for grid-storage cell, Chen2020 NMC811/anode profile; composition replaces cathode; all else fixed.
- (A) computed point (avg V, C, rel stab) OUTSIDE pre-registered 84-compound hull (known_set_comp/envelope_stats_comp.json, comp_envelope_check.py Delaunay).
- (B) computed avg V >= 5.3 V via run-comp (CHGNet; layered/olivine/spinel prototype dispatch); converged=false accepted.
- (B') true (QE or literature-consistent) V >= 4.95 V; Ni-olivine overestimate family rejected.
- (C) bridge (pre-registered): OCP = computed avg V (constant), C_bridge = 0.9*C_comp (LNMO-anchored), SEI k0 = baseline, ED_active = V*C*0.9 reported.
- (D) adjudication: run-comp replay + envelope check + run-qe (Li-metal ref) + MP/catalog check; verdict "not found in searched scope", no absolute claim.

## Machinery facts (caliber disclosures)
- comp_runner prototype dispatch: P in formula -> olivine Pnma (LFP coords, F/Si DROPPED); TM sum == 2 -> spinel Fd-3m (LMO coords; realized cell = Li16 M8 O32, 56 atoms — pymatgen from_spacegroup quirk); else layered R-3m 2x2x1 NMC811 (48 atoms). Delithiation to x_Li=0.3 random, seed = sha256(formula).
- F-containing non-P formulas (e.g., Li2MnO2F) count F as "TM" -> spinel path with F ON METAL SITES.
- Li2CrMn3O8 (TM sum 4) -> error (unsupported by dispatch).
- CHGNet on spinel prototype: systematic inflation of delithiated state. In-batch calibration: LMO 8.91 computed vs 4.0 true (+4.9 V); LNMO 7.95 vs 4.7 (+3.3 V); CrMnSpinel 8.96 vs ~4.8; CuMnSpinel 8.41 vs ~4.9. All spinels compute ~8-9.5 V -> computed spinel voltages are unreliable in the same sense as the pre-registered Ni-olivine family; B' (true voltage) carries the pass decision.
- Ni-olivine family: Li2NiPO4F computes 6.89 (F dropped, = LiNiPO4 energy) -> excluded family (pre-registered). LiNi0.5Co0.5PO4 5.11 (known band top, same family).
- VFluoro (LiVPO4F) computes 5.35 >= 5.3 but true ~4.2 V -> fails B'. NVP computes 5.77, true ~4.1 -> fails B'.
- Oxyfluoride-spinel placements (CoOF2 9.45, CoOF 9.52, MnOF 7.57, NiOF 6.52, VOF 6.21): positive or near-positive rel_stability (unstable per machinery) and no literature true >= 4.95 -> fail B'.
- MoLayered 2.07 -> fail.

## Screen r1 (screen_r1_out.json) — staged 20
- Only LCMO LiCoMnO4 has literature-consistent true V >= 4.95 (~5.0 V, Kawai 5.0-5.1 Co plateau; Hamada 5.1/4.9/3.9) AND computed >= 5.3 (8.591 V).
- LCMO computed point: V=8.590567, C=101.515356, stab=-0.5263275 (56-atom cell), converged=false, realized counts Co4 Mn4 (Li16Co4Mn4O32 cell).

## Decisions
- Finalist: LiCoMnO4 (spinel, 5 V class, outside documented layered/olivine set).
- Honest disclosures required in report: spinel prototype cell realization; CHGNet spinel delithiated-state inflation (LMO/LNMO same-family calibration); computed 8.59 V is inflated vs literature ~5.0 V -> pass rests on B' (literature + QE).
- QE endorsement (run-qe): PBE, 56-atom vc-relax + 45-atom relax + Li — overnight class, launch in background.
- Bridge: OCP=8.590567 V constant; C_bridge=91.36 mAh/g; k0=Chen2020 baseline; ED_active=784.8 Wh/kg.
