# T9 v9 prep — cross-domain prototype validation and a sealed-envelope integrity audit

**Date:** 2026-09-10 (pre-run; part of v9 preparation. No v9 run had started when this was written.)
**Artifacts:** `anchor_in.json` / `anchor_out.json` (cross-domain anchors), `anchor_spinel_in.json` /
`anchor_spinel_out.json` (spinel anchors, post-fix). Command:
`bda run-comp --in <in> --out <out>`.

Two things are recorded here: (1) the literature voltage anchors for every prototype the v9
contract makes computable, and (2) an integrity audit of the sealed v8 envelope that the anchors
exposed.

---

## 1. Cross-domain prototype anchors (CHGNet screening caliber)

The v9 contract widens the computable frameworks from 3 to 6 (adding tavorite phosphate,
tavorite sulfate, NASICON). A new template must first reproduce a known literature voltage,
otherwise the family is excluded honestly rather than used.

| framework | parent | V_calc (V) | literature (V) | deviation | verdict |
|---|---|---|---|---|---|
| olivine (**control, path unchanged**) | LiFePO4 | **3.443** | 3.4 | +0.04 | ✅ pipeline sound |
| tavorite sulfate | LiFeSO4F | **3.436** | 3.6 | −0.16 | ✅ admitted |
| tavorite phosphate | LiVPO4F | 3.580 | 4.1 | **−0.52** | ⚠️ admitted with a declared family calibration |
| NASICON | Li3V2(PO4)3 | 3.347 | 3.8 | **−0.45** | ⚠️ admitted with a declared family calibration |
| new-capability probe | LiNiSO4F | 4.942 | 5.35 (DFT only) | −0.41 | observation |

Baseline self-check: NMC811 layered path `e_full = −290.97 eV`, `converged = False` — identical to
the value in the v8 report, i.e. **strict dispatch did not perturb the original three frameworks**.

**Reading:** V-bearing frameworks are systematically **underestimated by ~0.45–0.52 V**, Fe-based
ones are nearly unbiased. Consequence for the window criterion (B, "computed voltage ≥ 5.3 V"):
cross-domain candidates are *disadvantaged* by construction; conversely (B′) already rejects the
overestimating families. This asymmetry is pre-registered in the v9 contract as a family
calibration note — declared before the run, not explained after it.

`converged = false` throughout is the known screening-caliber behavior, not a failure.

## 2. 🔴 The spinel prototype had the Li and M sites swapped

**Symptom.** `build_doped_structure("LiMn2O4")` produced **Li16 Mn8 O32 (= Li2MO4)** instead of
Li8 Mn16 O32: Li occupied octahedral holes (6 × O at 1.732 Å) and M sat **3.385 Å from every
oxygen** (i.e. not bonded at all). Its "voltages" were therefore meaningless — the six spinel
points in the sealed v8 envelope all fall in the 7.8–8.9 V range:

| formula | V in sealed envelope |
|---|---|
| LiMn2O4 | 8.911 |
| LiCrMnO4 | 8.631 |
| LiCoMnO4 | 8.597 |
| LiCu0.5Mn1.5O4 | 8.389 |
| LiNi0.5Mn1.5O4 | 8.263 |
| LiNiVO4 | 8.195 |

These six points alone set the upper end of the hull's voltage extent (envelope spans 3.119–8.911 V).

**Root cause.** `pymatgen`'s `Structure.from_spacegroup("Fd-3m", ...)` applies the
**origin-choice-1** setting, whereas the literature/COD description of a spinel
(`Fd-3m :2`) uses **origin choice 2**. The same fractional coordinate `(1/8,1/8,1/8)` generates a
**16-fold** site in one setting and an **8-fold** site in the other. The code had been written in
the choice-2 convention → Li and M were swapped.

**Fix.** Write the coordinates in the setting the library actually applies: Li on the 8-fold site
`(1/2,1/2,1/2)`, M on the 16-fold site `(1/8,1/8,1/8)`, O on 32e with `x = 0.3622` (= 0.625 − 0.2628),
cell `a = 8.251 Å` from **COD 1513964**. Verified against that CIF: identical cell volume and
coordination spectra — **Li 4 × O at 1.97 Å (tetrahedral), M 6 × O at 1.96 Å (octahedral)**.

**Post-fix anchors:**

| candidate | V_calc before fix | V_calc after fix | literature |
|---|---|---|---|
| LiMn2O4 | (7.8–8.9 V garbage range) | **3.77** | ~4.0 (4 V plateau) |
| LiNi0.5Mn1.5O4 | 8.263 (sealed) | **4.334** | ~4.7 |
| LiCo2O4 | 8.010 (v8 sanity batch) | **3.89** | — |

**Consequence for the interpretation of v8.** The v8 contract pre-registered "spinel
deep-delithiation" as an *overestimate family* of the chemistry. That attribution is wrong: those
values were artefacts of a structure-construction bug. The B′ true-voltage guard still rejected
them, but for the wrong stated reason, and the v8 report's "12 mechanical passers" are dominated
by candidates whose numbers came from the broken builder.

**Regression guard.** `tests/test_frameworks.py` now asserts composition, site counts and
coordination numbers for all six frameworks. It fails on the pre-fix spinel builder.

## 3. Integrity audit of the sealed v8 envelope (90 points)

Every sealed point's formula was re-dispatched under strict rules:

| framework | points | status |
|---|---|---|
| layered LiMO2 | 53 | supported, builder unchanged |
| olivine LiMPO4 | 30 | supported, builder validated by the 3.443 V control |
| spinel LiM2O4 | 6 | **invalid — built with the swapped-site bug; must be recomputed** |
| `Li2MnO3` | 1 | **unsupported framework** — the old "everything else → layered" default force-fitted it into the NMC811 prototype (V = 3.119) |

So 7 of the 90 sealed points were produced by machinery that cannot be justified today. The v9
pre-registration (`known_set` v2) therefore recomputes those points with the corrected builders
and records the revision before the run.

## 4. Literature check: documented members of the new families

Verified against published sources (subagent sweep; "not found in searched scope" where nothing
could be located):

- **Tavorite fluorophosphates:** LiVPO4F (~4.2 V, exp) and LiFePO4F (~2.75 V, exp) are real;
  **LiMnPO4F / LiCoPO4F / LiNiPO4F are not** — DFT-only (Mueller 2011, *Chem. Mater.* 23, 3854).
  The genuine Co/Ni members are the *Li2MPO4F* orthorhombic family (Li2CoPO4F ~4.8 V,
  Li2NiPO4F ~5.3 V — Nagahama 2010, *JES* 157, A748), a different framework.
- **Fluorosulfates:** LiFeSO4F (3.6 V, Barpanda 2010, *Nat. Mater.* 9, 68), triplite LiFeSO4F
  (3.90 V, *Nat. Mater.* 10, 772), Li2Fe(SO4)2 (3.83 V), LiFeSO4OH (3.6 V) are real.
  **LiMnSO4F / LiCoSO4F / LiNiSO4F were synthesized but are electrochemically inactive**
  (Barpanda 2010, *J. Mater. Chem.* 20, 1659) — the only "≥5.3 V" sulfate lead has no measured
  redox activity.
- **NASICON:** Li3V2(PO4)3 (3.8 V), Li3Fe2(PO4)3 (2.8 V), Li3Cr2(PO4)3 (~4.8 V, Cr4+/Cr3+) are
  documented; Li3Ti2(PO4)3 is real but an anode-side (~2.5 V) phase;
  Li3Mn2(PO4)3 / Li3Ni2(PO4)3 have no experimental literature (DFT records only).

**True-voltage ceiling, refined:** the highest *sustained* average discharge voltage reported for
a cycling cathode is **~4.8 V** (LiCoMnO4 / LiCoPO4); the highest *plateau* is **5.1 V**
(LiNiPO4); the highest *redox-potential* claim is **~5.3 V** (Li2NiPO4F, capacity-limited, cycling
not established). No documented cathode sustains ≥ 5.0 V average in a conventional carbonate
electrolyte. DFT-only claims ≥ 5.3 V exist (LiNiPO4F 5.50 V first-Li; Li2NiPO4F 5.33 V).

## 5. Provenance

- LiVPO4F (tavorite phosphate): P-1, a=5.184 b=5.312 c=7.266 Å, α=107.58 β=107.95 γ=98.45°
  (powder refinement, OSTI; cf. ICSD 184601: a=5.1708 b=5.3083 c=7.2631 Å).
- LiFeSO4F (tavorite sulfate): P-1, a=5.1747 b=5.4943 c=7.2224 Å, α=106.522 β=107.210 γ=97.791°
  (Barpanda et al., *Nat. Mater.* 2011, supplementary).
- Li3V2(PO4)3 (NASICON): P2₁/c, a=8.6201 b=8.6013 c=14.7465 Å, β=125.204° (COD **2237423**).
- LiMn2O4 (spinel): Fd-3m, a=8.251 Å (COD **1513964**).

**Reproduce:**
```
D:/anaconda/envs/py312/python.exe -m bda run-comp --in runs/exp/t9_v9_prep/anchor_in.json --out runs/exp/t9_v9_prep/anchor_out.json
D:/anaconda/envs/py312/python.exe -m bda run-comp --in runs/exp/t9_v9_prep/anchor_spinel_in.json --out runs/exp/t9_v9_prep/anchor_spinel_out.json
D:/anaconda/envs/py312/python.exe -m pytest tests/test_frameworks.py -q
```
