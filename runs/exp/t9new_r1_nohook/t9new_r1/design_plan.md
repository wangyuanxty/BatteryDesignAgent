# t9new_r1 — Design Plan: New Positive-Electrode Composition (grid storage, Chen2020 NMC811/anode profile)

**Task contract (verbatim thresholds):**
- System: Chen2020 NMC811/graphite profile; candidate composition REPLACES the cathode; all other cell choices fixed.
- (A) Envelope: candidate run-comp point (avg_voltage, capacity, rel_stability) must be OUTSIDE the pre-registered
  84-compound documented-cathode convex hull (`runs/exp/known_set_comp/envelope_stats_comp.json`; adjudicated by
  `comp_envelope_check.py`, Delaunay outside test, replayable). All 84 documented compounds are inside it.
  Calibration note: two Ni-olivine members excluded (LiNiPO4 7.016 V, LiNi0.4Co0.3Fe0.3PO4 6.067 V) and the
  computed band top itself (LiNiCo55 5.114 V) is in the same CHGNet Ni-olivine overestimate family.
- (B) Property window: computed average voltage >= 5.3 V (above the entire computed known band and outside the
  documented high-voltage family). run-comp machinery (CHGNet; layered/olivine prototype dispatch; other prototypes
  disclosed as domain limits) must converge-energy per screening caliber (converged=false accepted at screening precision).
- (B') True-voltage guard: candidate must satisfy a true (QE-level or literature-consistent) voltage >= 4.95 V;
  computed-only high values from the Ni-olivine overestimate family are rejected at adjudication regardless of (B).
- (C) Bridge rule (no free parameters): constant OCP = computed average voltage; capacity = computed capacity x 0.90
  (utilization, LNMO-anchored); SEI kinetics = baseline k0 (composition does not change SEI); ED_active = V x C x 0.9
  (reported, not a criterion).
- (D) Closed-loop adjudication: finalist re-computed independently (run-comp replay + comp_envelope_check.py)
  + run-qe (QE voltage with Li-metal reference) + Materials-Project/catalog check; verdict records
  "not found in searched scope" (absolute claim is not made).
- Forbidden: non-molecular/structural levers (geometry, transport, kinetics overrides, system switches).
- GUIDANCE: documented cathodes do NOT reach this window under a true-voltage measure; Ni-olivine in-family
  extrapolation is not a path; attaining the window requires leaving the documented cathode chemistry system
  (fluorophosphates, oxyfluorides, other frameworks), computed honestly.

## Objective decomposition

- Gate 1 (B): CHGNet computed avg voltage >= 5.3 V.
- Gate 2 (A): point outside the 84-point Delaunay hull in (V, C, stab).
  Mechanical fact: hull max V = 5.114 V (LiNiCo55 corner, inside hull) -> any V >= 5.3 point is automatically
  outside the hull in the V dimension (convex-combination argument). Hull C-min = 116.66 mAh/g -> points with
  C < 116.66 are outside in the C dimension as well.
- Gate 3 (B'): true voltage >= 4.95 V (QE-level or literature-consistent); Ni-olivine-family computed values rejected.
- Adjudication (D): independent replay + QE + catalog check; report honest.

## run-comp machinery (as pre-registered, read from comp_runner.py)

- Prototype dispatch: formula contains P -> olivine Pnma (LiMPO4, 4 M sites, F/Si ignored in structure, disclosed);
  no P and TM sum = 2 -> spinel Fd-3m (Li 8a / M 16d / O 32e, disclosed as domain limit);
  no P and TM sum = 1 -> layered R-3m 2x2x1 supercell (12 Li / 12 TM / 24 O);
  otherwise ValueError (recorded honestly).
- Voltage: V = -(E_full - E_delith - n_removed * E_Li)/n_removed, x_Li in [1.0, 0.3], seed from formula hash;
  E_Li from CHGNet bcc Li per batch; capacity = 0.7 * F / mw(formula).
- Calibration data (known set + prior t9new_r1_45arm run, old contract):
  - Layered oxides compute 3.1-4.03 V (ceiling NiMnMA 4.029).
  - Ni-free olivines compute <= 4.10 V (OliCoFe64); Ni-containing olivines 4.02-7.02 V with strong nonlinearity
    (Ni0.4 mixes: 4.58-6.07; Ni>=0.75: 5.42-7.02) — the CHGNet Ni-olivine overestimate family.
  - Spinel dispatch computes ~8.2-9.0 V for LNMO/LCMO-type (delithiated-spinel artifact; true voltages 4.7-5.0).
  - F-containing P-free formulas with TM sum != 1 or 2 -> ValueError (F counts as TM in layered path).
  - Li2NiPO4F computes identically to LiNiPO4 (6.86 V; olivine prototype, F ignored) — the machinery cannot
    distinguish fluorophosphates from parent olivines.

## Consequence analysis (before screening)

- (A) is automatically satisfied by (B): V >= 5.3 > 5.114 = hull max V.
- Within the pre-registered machinery, computed V >= 5.3 is reachable ONLY by:
  (i) Ni-rich olivines (Ni >= ~0.4 site fraction; noisy) — BANNED family per B'/GUIDANCE;
  (ii) spinel prototype dispatch (~8.2 V, domain-limit artifact) — true voltages of documented spinels are
  4.7 (LNMO) to ~4.9-5.0 (LiCoMnO4 5-V spinel class) — B' is the decisive gate;
  (iii) unknown CHGNet behavior for exotic M (Cu/V/Cr/Mo/F-on-M-sites) — to be probed empirically.
- Imported fluorophosphates (guidance flagship) compute as parent olivines in this machinery:
  Li2CoPO4F -> LiCoPO4 structure -> ~3.71 V (fails (B) honestly). Documented as such.

## Candidate strategy (Round 1 screening, 20 formulas)

1. Controls: LiNi0.5Co0.5PO4 (hull-interior control, must reproduce ~5.11 and REJECT);
   LiNi0.5Mn1.5O4 + LiCoMnO4 (spinel dispatch replays); Li2NiPO4F (Ni-olivine-family probe; expect ~6.86).
2. Imported fluorophosphates (P -> olivine): Li2CoPO4F, LiVPO4F, LiCuPO4, Li3V2(PO4)3.
3. Imported oxyfluorides (TM sum = 2 -> spinel dispatch, F on 16d M sites, disclosed): Li2MnO2F, Li2CoO2F,
   LiCoOF, Li2NiO2F, Li2VO2F.
4. Other frameworks: LiCo2O4 (Co-spinel), LiCrMnO4 (Cr/Mn spinel), LiNi0.5V1.5O4, LiCu0.5Mn1.5O4,
   LiMn2O4 (spinel control), Li2MoO3 (layered Mo probe), Li2CrMn3O8 (TM sum 4 -> ValueError probe).

Round 2 direction depends on round 1: refine any family that computes >= 5.3 with a defensible true voltage
>= 4.95 (QE-level or literature-consistent) and is not the Ni-olivine overestimate family.

## Budget allocation

- Round-1 screening: 20 candidates x 2 CHGNet states (RTX GPU, ~20-45 s/state) + baseline ~ 15-40 min.
- Envelope adjudication: seconds (Delaunay test, replayable).
- run-qe finalist (closing only): olivine primitive 28 atoms ~1 h/state (3 states) or spinel 56 atoms hours/state —
  background. QE = SSSP-efficiency PBE, no +U (PBE known to under-estimate TM redox voltages; disclosed).
- MP/catalog check: web search (no API key in .env) — records "not found in searched scope" if applicable.

## Risk & fallback

- If the only >= 5.3 computed values are Ni-olivine family or spinel domain-limit artifacts whose true voltage
  < 4.95 -> honest negative result per contract (report computed evidence, QE, and catalog status verbatim).
- PBE-QE may under-estimate true voltages (no +U): B' adjudication also accepts literature-consistent >= 4.95;
  both numbers reported.

## Domain references (directional basis)

- LiNiPO4 olivine ~5.1 V vs Li (literature; e.g., Wolfenstine & Allen, J. Power Sources 2005 — domain memory, direction only).
- LiNi0.5Mn1.5O4 ~4.7 V (documented high-voltage spinel; well established).
- LiCoMnO4 ~4.9-5.0 V (5-V spinel class; Kawai et al. 1999-type reports — domain memory, direction only).
- Li2CoPO4F fluorophosphate ~4.9-5.0 V (DFT/experimental reports — domain memory, direction only).
- CHGNet Ni-olivine overestimate: this repo's own pre-registered calibration note (envelope_stats_comp.json "excluded").

## Revision history
- r1 (initial): plan as above, written before any simulation for this contract.
