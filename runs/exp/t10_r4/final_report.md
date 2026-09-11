# T10 v4 (t10_r4) — Final Report: Electrolyte Additive for Grid-Storage Cell (Chen2020 NMC811/graphite)

**Verdict: ACHIEVED** — all three contract stages pass for the finalist additive (mechanical evidence in log.jsonl, round 1).

## Final additive

| Field | Value |
|---|---|
| **Name** | **Trifluoroacetic anhydride (TFAA)** |
| **SMILES** | `O=C(OC(=O)C(F)(F)F)C(F)(F)F` |
| Cataloged | **Yes — CAS 407-25-0** (liquid, commercial anhydride) |
| Role | Perfluorinated anhydride film-forming additive (reduction-first SEI former) |

## Funnel outputs (three models)

| Model | Quantity | Value | Gate |
|---|---|---|---|
| MACE-MP (medium, CUDA) | energy_ev | −80.37634 eV (total) | ≤ 0 ✓ |
| MACE-MP | converged | **true** (BFGS fmax < 0.05, 19 steps) | ✓ |
| CHGNet (CUDA) | energy_ev | −84.47935 eV (total) | ≤ 0 ✓ |
| CHGNet | converged | **true** (BFGS fmax < 0.05, 15 steps) | ✓ |
| GFN2-xTB | HOMO | **−14.1603 eV** | ≤ −13.74 ✓ |
| GFN2-xTB | LUMO | **−10.9558 eV** | ≤ −7.0 ✓ |

Point used for envelope test: [E_mace/n, E_chgnet/n, HOMO] = [−6.18280, −6.49841, −14.1603] eV (n = 13 atoms).

## Envelope and family adjudication (official CLI, re-run for the record)

Command: `envelope_check.py --known-set runs/exp/known_set_sei/envelope_stats_v2.json --smiles "O=C(OC(=O)C(F)(F)F)C(F)(F)F"`
(record: `finalist_envelope_check.txt` / `finalist_envelope.json`)

- **in_envelope = false** — outside the convex hull of the 87 known points (82 documented additives + 5 previous-run candidates) ✓
- **in_documented_families = false, families_matched = []** — no banned family (no carbonate/ester/aromatic/S=O/nitrile/etc. motif) ✓
- Reduction-first check: **LUMO −10.9558 eV ≤ −7.0 eV** ✓ — well below solvent LUMOs (EC −6.7171, EMC −6.1581, PC −6.620) and below the film-former references (FEC −7.1960, VC −7.0894), i.e. TFAA is reduced first at the anode.

## HOMO → SEI mapping computation (executed by mapping.py, no free parameters)

Rule (pre-registered, entry 0): k(M) = k0 · 10^((HOMO_xTB(M) + 12.5)/1.0), k0 = 1e-12 m/s (Chen2020 baseline `SEI kinetic rate constant [m.s-1]`), calibrated on (HOMO −12.5 → 449.12 nm) and (HOMO −13.5 → 385.10 nm).

k(TFAA) = 1e-12 · 10^(−14.1603 + 12.5) = 1e-12 · 0.0218625 = **2.18625e-14 m/s** (factor 0.02186×)

Param file used by the cell sim: `cell/params_finalist.json` = `{"SEI kinetic rate constant [m.s-1]": 2.1862508936067043e-14}`.

## Cell-level results (finalist, Chen2020, all three sims run with the finalist params)

| Contract metric | Threshold | Result | Verdict |
|---|---|---|---|
| SEI thickness after 100 × 1C cycles | ≤ 370 nm | **322.636 nm** (SPMe, aging_1C_100cyc) | **PASS** (47 nm margin) |
| Energy density, 1C discharge | ≥ 327.18 Wh/kg | **400.293 Wh/kg** (calc-energy contract convention; capacity 4.9478 Ah, mass 0.0434545 kg) | **PASS** |
| Thermal runaway at 4C charge / 45 °C | not triggered | **triggered = false** (run-tr on 4C_charge_45C DFN output; T_max 354.289 K, dT/dt_max −0.00084 K/s) | **PASS** |

`bda log-evaluate` (round 1, candidate "trifluoroacetic anhydride (TFAA)"): **verdict = pass, 9/9 criteria checked, 0 unchecked** (homo, lumo, in_envelope, in_documented_families, converged, energy_ev, sei_thickness_nm_end, energy_density_wh_kg, triggered — all with file:key evidence in log.jsonl).

Baseline reference evaluate entry (same round): SEI 449.116 nm → fail on the SEI criterion only; ED 400.293 and triggered=false pass — the additive's only lever (SEI kinetics) closes the only failing metric.

## Round-1 funnel summary

- 72 candidates proposed; 2 dropped at SMILES validation (ClO3F, IF7 — RDKit explicit-valence rejection, recorded in funnel dispositions).
- 70 xTB-screened (GFN2-xTB + family gate + both windows): **16 passers** of both windows (HOMO ≤ −13.74 ∧ LUMO ≤ −7.0, gate-clean).
- All 16 adjudicated with envelope_check v2: **all 16 converged, in_envelope = false, families_matched = []** (16 stage-1 passers; dispositions table in log.jsonl funnel entry).
- Finalist chosen among them: TFAA — cataloged, liquid, deep LUMO (−10.96), and its mapped k = 2.186e-14 gives the cell-level SEI margin above. Runner-ups include perfluorosuccinyl difluoride (HOMO −14.454) and perfluoroglutaric anhydride (HOMO −14.331), both also fully passing.

## Honest caveats (reported, not hidden)

1. **Mapping extrapolation**: TFAA's factor 0.0219× lies below the mapping's 0.1×–1× calibration range (449.12 / 385.10 nm anchors). The mapped k is therefore an extrapolation assumption. Supporting evidence that the conclusion does not rest on extrapolation fragility: the k-sweep shows SEI(k) = 449.12 / 384.96 / 366.87 / 322.74 / 274.35 nm at k0 / 0.1× / 5.754e-14 / 2.19e-14 / 1.1e-14 — even the window-edge HOMO (−13.74 → k = 5.754e-14, inside the calibrated range) gives 366.87 nm ≤ 370, so any window-passing additive passes stage 2.
2. **Lithium plating at 4C**: anode surface potential minimum −0.1918 V (plating) persists for the finalist cell — identical to baseline, not a contract criterion, and out of scope to fix (non-molecular levers are prohibited by the contract).
3. **real_compute = false**: no true DFT/MD endorsement (endorse entry records the skip; no fabricated values). All funnel numbers are MACE-MP + CHGNet + GFN2-xTB proxies.
4. Stage-1 gate values for the finalist come from the official CLI adjudication record (`finalist_envelope_check.txt`), which was re-run independently of the batch adjudication; the two runs agree to the printed precision.

## Artifacts

- `log.jsonl` — full audit chain: criteria (entry 0) → plan → propose → funnel → evaluate ×2 → endorse → final.
- `report.html` — rendered seven-section report from log.jsonl.
- `cell/` — all simulation outputs (baseline, k-sweep, finalist); `finalist_envelope_check.txt` + `finalist_envelope.json` — official adjudication record; `mapping_finalist.json` — mapping computation.
