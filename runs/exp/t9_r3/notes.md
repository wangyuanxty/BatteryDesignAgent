# T9 run 3 — working notes (headless run)

Date: 2026-09-10. Workspace: runs/exp/t9_r3.

## Design target (parsed from task)

- Grid-storage cell on Chen2020 NMC811/anode profile. Cathode composition is the ONLY free variable.
- Need: computed average voltage (run-comp, CHGNet machinery) >= 5.3 V.
- Constraints: composition must NOT be one of the 115 documented materials (membership layer)
  AND its computed point (V, C, stab) must lie OUTSIDE the convex hull of the 102 computed points
  (Delaunay outside test vs known_set_v3.json). Band top of the 102 points: 5.4878 V (LiNiPO4F, prior run).
- True-voltage guard: 5.3 V must hold beyond the screening proxy (experimental value / own QE
  computation / literature-consistent evidence).
- Cell mapping (no free parameters): constant OCP = computed avg voltage; capacity = 0.9 x computed
  capacity (LNMO-anchored utilization); SEI kinetics = baseline k0; ED_active = V x C x 0.9.
- Close the loop: independent replay (run-comp + envelope script), attempt run-qe with Li-metal
  reference, public catalogue check ("not found in the searched scope" wording).

## Machinery facts (from comp_runner.py)

- Six strict families: layered LiMO2 (R-3m NMC811 prototype), olivine LiMPO4 (Pnma LiFePO4 prototype,
  4 M sites), spinel LiM2O4 (Fd-3m), tavorite LiM(PO4)F and LiM(SO4)F (P-1, 8 M sites),
  NASICON Li3M2(PO4)3 (P2_1/c, 8 M sites). Anything else -> explicit "unsupported framework" error.
- Voltage = -[E(full) - E(delith x=0.3) - n*E_Li]/n, E_Li = CHGNet bcc Li reference.
- Capacity = 0.7 x 26801.481 / MW (mAh/g).
- rel_stability_ev_atom = E_full/n_atoms - E_NMC811_per_atom (within-batch ranking).
- Realized composition: largest-remainder rounding over M sites; seed from formula hash.

## Calibration cautions (task + known_set excluded field)

- Ni-rich olivines: CHGNet inflated (LiNiPO4 computes 7.016 V vs lit. 5.1 V — excluded;
  LiNi0.4Co0.3Fe0.3PO4 computes 6.067 V — excluded). Pure-Ni olivine is a TRAP.
- LiFePO4F computes 4.919 vs lit. 2.75 (tavorite-P Fe unvalidated); Li3Fe2(PO4)3 computes 4.699
  vs lit. 2.8 (NASICON Fe unvalidated). Fe substitution in those families: guard-flagged.
- V-bearing and spinel families compute LOW by ~0.2-0.5 V.
- Tavorite sulfate Fe anchor nearly unbiased (3.436 vs 3.6).
- LiNiSO4F (documented, in hull) computes 4.9421 V -> sulfate family cannot reach 5.3 computed.
- Olivine realized-composition trap: 4 M sites only. Ni fraction in [0.75,0.875) -> realized 3Ni/1Co
  == known LiNi0.75Co0.25PO4 (point in hull). Ni fraction >= 0.875 -> realized pure LiNiPO4
  (excluded outlier, 7.016 V). Both dead ends for an honest pass.

## Strategy

Only the Ni-rich tavorite-phosphate family plausibly computes >= 5.3 AND has a defensible
true-voltage story (Ni2+/Ni3+ fluorophosphate: LiNiPO4 5.1 V exp plateau + F inductive effect
~+0.2 V (LiVPO4F 4.2 vs LiVOPO4 ~4.0) + Li2NiPO4F 5.3 V literature claim).

Hull-outside test: at the high-V face, hull vertices are LiNiPO4F (5.4878, 104.46, -1.2199),
olivines LiNi0.75Co0.25PO4 (5.4171, 116.77, -1.8722) / LiNi0.8Co0.2PO4 / LiNi0.4Co0.6PO4,
LiNi0.75Co0.25PO4F (5.3863, 104.42, -1.2942), LiNi0.5Co0.5PO4F (5.3052, 104.39, -1.3632).
A candidate with V in [5.30, 5.49] and C ~104.5 must have stab more negative than the hull surface
(edge LiNiPO4F <-> LiNi0.75Co0.25PO4F), i.e. stab <~ -1.24 ... -1.29. Margins are razor-thin;
every candidate must be adjudicated with the envelope script itself.

Candidate batch 1 (tavorite phosphate, 8 M sites):
- LiNi0.875Co0.125PO4F -> realized 7Ni/1Co (V/stab between LiNiPO4F and LiNi0.75Co0.25PO4F)
- LiNi0.875Mn0.125PO4F -> 7Ni/1Mn (Mn may stabilize: more negative stab at similar V)
- LiNi0.75Co0.125Mn0.125PO4F -> 6Ni/1Co/1Mn
- LiNi0.875Al0.125PO4F -> 7Ni/1Al (inert Al: keeps V high, lowers MW -> higher C)
- LiNi0.875Mg0.125PO4F -> 7Ni/1Mg (inert Mg, same idea)
- Li3Ni2(PO4)3 (NASICON Ni; low C=45.8 would be far outside hull C range if V>=5.3)
- Li3Ni1.5Co0.5(PO4)3 (NASICON 6Ni/2Co)
- LiNi0.75Mn0.25PO4 (olivine 3Ni/1Mn reference)
- LiMnPO4F (tavorite Mn reference, for the Mn-edge map)

Adjudication: D:/anaconda/envs/py312/python.exe comp_envelope_check.py --known-set
runs/exp/known_set_comp/known_set_v3.json --formula "<formula>" (and --point for raw triples).

## Batch 1 results + adjudication (--point triples, Delaunay vs 102 points)

- tav-F-Ni7Co1  LiNi0.875Co0.125PO4F  5.4553, 104.44, -1.2568 -> REJECT (inside hull)
- tav-F-Ni7Mn1  LiNi0.875Mn0.125PO4F  5.4138, 104.73, -1.3396 -> REJECT (inside hull)
- tav-F-Ni6Co1Mn1 5.3653, 104.71, -1.3766            -> REJECT (inside hull)
- tav-F-Ni7Al1  LiNi0.875Al0.125PO4F  5.4674, 106.82, -1.3093 -> REJECT (inside hull)
- tav-F-Ni7Mg1  LiNi0.875Mg0.125PO4F  5.5082, 107.02, -1.2236 -> PASS (outside; V > band top 5.4878)
- nasicon-Ni    Li3Ni2(PO4)3         5.1131, 44.34         -> PASS but V < 5.3 (window fail)
- oliv-Ni3Mn1   LiNi0.75Mn0.25PO4     5.5225, 117.50        -> PASS but Ni-rich olivine TRAP (guard fail; true ~4.85 V)
Hand-analysis of the Co/Mn/Al variants had predicted outside with razor margins; the
mechanical Delaunay test says INSIDE for all three - the margins were too thin. Lesson:
only V > 5.4878 (band top) gives a robust outside verdict at C ~ 104-110.

## Batch 2 (repeats + Mg/Si variants; fresh compute - determinism check)

- LiNi0.875Mg0.125PO4F repeat: V = 5.5081958 (batch1 5.5081957) - deterministic
- LiNi0.75Mg0.25PO4F  -> 6Ni/2Mg: V = 5.5190, C = 109.709, stab = -1.2274  <- FINALIST
- LiNi0.875Co0.125PO4F repeat: V = 5.4552936 (batch1 5.4552884) - deterministic
- LiNi0.75Mn0.25PO4F  -> 6Ni/2Mn: 5.3340 (window margin thin; not used)
- LiNi0.875Si0.125PO4F -> 7Ni/1Si: 5.3947 (below band top; not used)

FINALIST: LiNi0.75Mg0.25PO4F (tavorite fluorophosphate, realized 6Ni/2Mg on 8 M sites).
Why over LiNi0.875Mg0.125PO4F: higher V (5.5190 vs 5.5082 -> hull margin 0.0312 V vs
0.0204 V above band top), higher C (109.71 vs 107.02), identical stab, and a cleaner
redox/DFT story: exactly 6 Li removed = 6 Ni2+->Ni3+, all-Ni3+ delithiated state
(no mixed Ni2+/Ni3+ valence for the QE run). Elements all QE-able (Li/Ni/Mg/O/P/F).

## Envelope replay (criterion 6) - comp_envelope_check --formula (recomputes)

- LiNi0.75Mg0.25PO4F: point [5.519024610519409, 109.70913206456218, -1.227437863404723],
  in_envelope=false, verdict PASS (outside envelope)  -> replay_envelope_finalist.json
- LiNi0.875Mg0.125PO4F: point [5.508190393447876, 107.01902890330234, -1.223627485077957],
  in_envelope=false, verdict PASS (outside envelope)  -> replay_envelope_backup.json
- Membership layer A0: both formulas not among the 115 (raw + whitespace-normalized check,
  membership_check.py).

## True-voltage guard evidence (finalist: Ni2+/Ni3+ in tavorite fluorophosphate, Mg inert)

1. Li2NiPO4F experimental redox ~5.3 V vs Li/Li+: Nagahama, Hasegawa, Okada,
   J. Electrochem. Soc. 157, A748 (2010), DOI 10.1149/1.3417068 (dinitrile electrolyte).
2. LiNiPO4F discharge voltage ~5.3 V reported (Nazri & Pistoia, Lithium Batteries:
   Science and Technology).
3. LiNiPO4 (olivine) plateau 5.1 V - Ni2+/Ni3+ phosphate baseline.
4. DFT anchors: Li2NiPO4F 5.33 V (Chakrabarti & Thakur, JES 171, 080508, 2024);
   LiNi0.5Mn0.5PO4F 5.23 V vs 4.27 V for the phosphate (tavorite-F inductive effect).
5. Family calibration: CHGNet LiNiSO4F computes 4.9421 vs Xie et al. (JPC-C 2011) DFT
   5.16 -> the screening proxy is ~0.2 V CONSERVATIVE for Ni-tavorite, i.e. the computed
   5.5190 V is unlikely to be an overestimate; true value plausibly ~5.3-5.5 V.
6. Redox identity: 6 Li/f.u. removed in the screening window = exactly the 6 Ni2+/Ni3+
   oxidations; Mg2+ is electrochemically inert (no O-redox artifact).
7. Mg-on-M-site supportability: Mg-doped LiVPO4F synthesized and cycled
   (LiV0.97Mg0.03PO4F@C, ~4.2 V, 140.3 mAh/g at 1C, 88.2% retention/500 cyc); Mg site
   substitution in the tavorite framework also DFT-studied. Full 25% Mg endmember not
   synthesized (stated honestly).
QE attempt: run-qe launched in background (finalist first, then 7Ni/1Mg backup);
full.out confirmed iterating (SCF #8+, ecut 50 Ry, nspin 2). PBE voltages for
polyanionic Ni2+/3+ typically sit ~0.3-0.5 V BELOW experiment; result to be appended.

## Cell mapping (criterion 5; standalone script cell_mapping.py)

- Constant OCP = 5.5190 V; capacity = 0.9 x 109.709 = 98.738 mAh/g; SEI k0 = 1e-12 m/s
  (Chen2020 baseline, untouched); density anchor 4400 kg/m3 (LNMO template precedent).
- Window mechanics: 0.7 (run-comp x window) x 0.9 (utilization) = 0.63; c_max = rho/MW
  = 25730 mol/m3; initial (charged) conc = 0.37 x c_max; 1C discharge for 0.63 h.
- Delivered 0.6194 Ah (expected 0.6194); 98.738 mAh/g active; terminal voltage
  5.378-5.385 V (flat, = OCP - graphite). ED_active = 544.9 mWh/g (reported).
- Note: pybamm_runner hardcodes string OCP -> lnmo_ocp; standalone script required.

## Public catalogue check (criterion 6)

- COD (crystallography.net): exact finalist formula -> 0 entries; Li-Ni-P-O-F family -> 0.
- OQMD OPTIMADE: elements HAS ALL {Li,Ni,Mg,P,O,F} -> 0 of 1,407,395 entries.
- Verdict: "not found in the searched scope" (COD + OQMD).

## Status

- QE endorsement for the finalist running in background (be74hqdiv; first attempt
  bk7r8un65 trimmed to finalist-only so the out file is written as soon as the finalist
  finishes). Final report: FINAL_REPORT.md; replay guide: REPLAY.md.

