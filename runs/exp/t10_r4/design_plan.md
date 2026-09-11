# Design Plan — T10 v4 contract: electrolyte additive for SEI suppression (grid storage, Chen2020 NMC811/graphite)

Workspace: `runs/exp/t10_r4`. Zero-interaction execution (headless task, contract text carries all parameters).

## 1. Objective decomposition (decision layers)

| Layer | Criterion | Threshold | Tool |
|---|---|---|---|
| stage1 (molecular) | xTB HOMO (SEI-suppression window) | ≤ −13.74 eV | run-xtb / envelope_check |
| stage1 (molecular) | xTB LUMO (reduction-first, additive must be reduced before solvent) | ≤ −7.0 eV | run-xtb / envelope_check |
| stage1 (molecular) | family gate | families_matched empty (no S=O, C#N, ester, carbonate, aromatic ring, dialkyl ether, B, Si, amide, nitro, quinone, P) | envelope_check.py |
| stage1 (molecular) | envelope gate | in_envelope = false (outside convex hull of 87 known points in [E_mace/atom, E_chgnet/atom, HOMO]) | envelope_check.py --known-set envelope_stats_v2.json |
| stage1 (molecular) | ML convergence | MACE & CHGNet converged, energy < 0 | run-mlp |
| stage2 (cell) | SEI thickness after 100×1C cycles | ≤ 370 nm (baseline k0 → 449.12 nm; 0.1×k0 → 385.10 nm) | run-pyamm aging_1C_100cyc |
| stage2 (cell) | energy density on 1C discharge | ≥ 327.18 Wh/kg (calc-energy contract convention) | run-pyamm 1C_discharge + calc-energy |
| stage3 (safety) | thermal-runaway trigger under 4C charge at 45 °C | triggered = false | run-pyamm 4C_charge_45C + run-tr --sim |

Parameter mapping (declared rule, no free parameters, executed by code):
`k(M) = k0 · 10^((HOMO_xTB(M) + 12.5)/1.0)`, with `k0 = 1e-12 m/s` = Chen2020 baseline `"SEI kinetic rate constant [m.s-1]"` (dumped from pybamm ParameterValues). Calibration anchors: HOMO −12.5 → k0 → 449.12 nm; HOMO −13.5 → 0.1·k0 → 385.10 nm. At the window edge HOMO = −13.74 → k = 10^(−1.24)·k0 = 5.754e-14 m/s. The mapping is calibrated over the 0.1×–1× range; extrapolation below 0.1× (HOMO < −13.5) is an assumption and will be reported as such.

## 2. Degree-of-freedom boundary (meta.freedoms)

- Electrode system: LOCKED → Chen2020 (task text: "Chen2020 NMC811/graphite profile").
- Electrolyte formulation (σ/t⁺/D): LOCKED (transport parameters may not be used to reach the target).
- Electrode modification: LOCKED except the declared additive SEI-kinetics mapping (the only allowed lever; geometry, kinetic overrides other than the mapping, and system switches are prohibited).
- Cell architecture: LOCKED (no thickness/porosity/N-P/collector/particle-size changes).
- Thermal management: LOCKED (contract-default cooling h=10).
- Answer must be a molecule. real_compute = false (no true DFT/MD endorsement; endorse entry records the skip).

## 3. Candidate strategy

**Baseline first** (round 0): characterize Chen2020 at k0: aging 100×1C → SEI (expect ≈449 nm), 1C discharge + calc-energy → ED, 4C_charge_45C + run-tr → triggered. This fixes the non-molecular part of the contract (ED/TR are baseline properties; the additive lever only moves SEI kinetics).

**Chemistry (round 1)**: the target region (HOMO ≤ −13.74 ∧ LUMO ≤ −7.0) is normally reached by S=O chemistry (triflyl fluoride −14.14, bis(CF3)sulfone −14.30), but the family gate bans any S=O, nitrile, ester/carbonate, amide, aromatic ring, ether, B/Si/P, nitro, quinone. Remaining electro-withdrawing motifs: acyl fluorides (COF), α-dicarbonyls, anhydrides (mechanically not esters: the bridging O has carbonyl-C neighbors on both sides), ketenes, isocyanates/isothiocyanates, thiocarbonyls (C=S), sulfur(VI)/sulfur fluorides (SF6, SF4, SF5-R, S2F10), N–F compounds (NF3, N2F4, R-NF2), hypofluorites (C–O–F, not a dialkyl ether), perfluoro aliphatic alkenes/cyclic ketones, imines/oximes, thioesters (C(=O)–S is not an ester), halogen oxyfluorides (ClO3F). Strategy: maximally electron-poor small molecules combining several of these motifs (e.g., SF5-C(=O)-F, FOC-COF, CF3-CO-COF).

**Hull avoidance**: the hull's deep-HOMO face is spanned by F-rich S/O/N points with MACE per-atom energies ≈ −5.1…−6.5 eV/atom (triflyl fluoride, SO2F2, CF3CN, CF3NO2) down to DFEC (−7.77). A survivor must either have HOMO deeper than the deepest vertex (−14.2961) or sit outside the per-atom-energy cross-section of the hull at its HOMO. Adjudicate every survivor with envelope_check.py (mechanically).

**Round 2+ fallback directions**: (a) deepen HOMO by stacking more EWGs (SF5/NF2/COF combinations); (b) if survivors land inside the hull, shift per-atom energy by composition (more F per heavy atom) or deepen HOMO past −14.30; (c) three-strike rule with layer-by-layer questioning if no molecule clears all gates.

## 4. Budget allocation

- xTB probes: ~60 molecules in round 1 (seconds each), 1–3 refinement rounds of ~15 each.
- MACE/CHGNet + envelope adjudication: only on xTB survivors (CUDA, ~30–60 s per molecule).
- Cell simulations: baseline (3 runs) + finalist (3 runs: aging / 1C+calc-energy / 4C+run-tr); ~6–8 run-pyamm calls total.

## 5. Risk and fallback plan

- R1 (no molecule passes both HOMO and LUMO windows): tighten EWGs — SF5/NF2/COF hybrids, more F; if nothing passes, negative result honestly.
- R2 (survivors are inside the hull): adjust composition for per-atom-energy offset or HOMO < −14.2961; re-adjudicate.
- R3 (SEI target unreachable): the mapping at HOMO −13.74 gives 0.0575·k0; the calibration trend (449.12 → 385.10 over 0.1×–1×) extrapolates to ≈369–372 nm at 0.0575× — near the 370 nm line, so the margin is thin; candidates with HOMO deeper than −13.74 give a bigger factor reduction. If the cell sim returns SEI > 370 nm, deeper-HOMO variants are the fallback (still within the window).
- R4 (ED/TR fail at baseline): these are baseline properties; no molecular lever can fix them under the non-molecular-lever prohibition → negative result honestly.

## 6. References (domain basis)

- Deep-HOMO film-formers cluster around S=O/CN/NO2 electron-withdrawing chemistry → known-set statistics (triflyl fluoride −14.14 eV, bis(CF3)sulfone −14.30 eV; envelope_stats_v2.json), domain experience (no precise source).
- Reduction-first additive design (LUMO below solvent LUMO) → contract reference values (EC −6.7171, EMC −6.1581, PC −6.620, FEC −7.1960, VC −7.0894 eV, measured in this pipeline).
- SEI kinetics × additive HOMO monotone screening rule → declared contract mapping, calibrated on two simulated points (449.12 nm, 385.10 nm).
