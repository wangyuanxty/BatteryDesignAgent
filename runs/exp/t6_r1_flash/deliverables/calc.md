# Calculation Report — finN-2e19

**Document**: VBF-T6R1F-CALC-01 | **Case**: t6_r1_flash | **Date**: 2026-08-25 | **Method**: contract-caliber `calc-energy` (bda), DFN/SPMe simulation (pybamm via run-pyamm)

## 1. Energy Density (contract formula, all tasks)

```
ED = ∫V·I_1C dt / Σ(layer thickness×(1−porosity)×density×area)
```

- I_1C = Nominal cell capacity × 1 = 4.5 A (LNMO base nominal)
- Area = 0.065 m × 1.58 m = 0.1027 m²
- Layers: pos/neg active layers (porosity-corrected), pos/neg current collectors (no porosity), separator; **electrolyte excluded** (parameter set lacks density — `electrolyte_included: false`, annotated honestly)
- Integral: trapezoidal ∫V dt over 1C discharge × 4.5 A ÷ 3600

| Quantity | SPM | DFN (final) |
|---|---|---|
| Capacity | 6.347 Ah | 6.324 Ah |
| Energy | 26.97 Wh | 26.18 Wh |
| Mass | 50.3 g | 45.9 g |
| ED volumetric | 1172.1 Wh/L | **1171.7 Wh/L** |
| ED gravimetric | 541.7 Wh/kg | 569.9 Wh/kg |
| Midpoint voltage | 4.248 V | 4.145 V |
| Thickness | — | 217.6 µm |

M1 verdict: **PASS** (1171.7 ≥ 950, DFN). M2 verdict: **PASS** (4.145 ≥ 4.1, DFN).

## 2. Thermal (4C charge, 45 °C ambient, lumped thermal)

Energy balance: m·cp·dT/dt = Q_gen − h·A·(T−T_amb). DFN-resolved heat generation (anode saturation + electrolyte ohmic + polarization + entropy).

| h (W/m²K) | T_max (K, DFN) | vs 323.15 |
|---|---|---|
| 120 | 326.12 | fail +3.0 |
| 200 | 323.83 | fail +0.7 |
| 250 | 323.05 | pass −0.1 |
| 300 | **322.50** | **pass −0.65** |

M5 verdict: **PASS** at h = 300 W/m²K (design spec; h=250 verified minimum). SPM at h=120 under-predicted DFN peak by 4.3 K (321.9 vs 326.1) — DFN adopted for the thermal spec.

## 3. SEI Growth (100 cycles, 1C, isothermal, Yang2017 EC-reaction-limited model)

Diffusion-limited regime (L_sei ≥ ~300 nm): j_sei ∝ −F·c₀·k/(1 + L/D_ec·k) ≈ −F·c₀·D_ec/L → **L ∝ √(D_ec·t)**.

| D_ec (m²/s) | SEI end (nm, SPM 100 cyc) |
|---|---|
| 1e-18 (base) | 559 |
| 6e-19 | 568 (deeper-cycling arch) |
| 3e-19 | 356.6 |
| **2e-19 (final)** | **292.2** |
| DFN 1-cycle cross-check | 27.4 (consistent with √t scaling: 292/√100 ≈ 29) |

M3 verdict: **PASS** (292.2 ≤ 500) with 42% margin.

## 4. Plating Boundary (M4) — mechanism calculation

At the 4.7 V cutoff, from circuit balance: `ap = U_pos(surf) + η_pos − V − φ_e(sep)`.

- Measured (finM, SPM): U_pos = 4.4546 V (surf sto 0.149), η_pos = +0.0151 V, φ_e(sep) = +0.196 V → ap = −0.22 V ✓ (measured −0.2204)
- Cathode ceiling limit: U_pos(sto→0) = 4.706 V → best-case ap = 4.706+0.015−4.7−φ_e(sep) = +0.021−φ_e(sep)
- φ_e(sep) measured ~11× ohmic estimate (κ_eff effective ~0.1 S/m at σ 5); to reach ap ≥ 0 requires σ ≳ 100 S/m — physically impossible
- Anode-side terms (U_neg, η_neg, stoichiometry) cancel at the cutoff by construction (the anode surface is saturated; the cutoff fires on V, which pins φ_s,neg = U_pos+η_pos−4.7)

M4 verdict: **FAIL** — documented protocol-level boundary (LNMO OCP ceiling 4.706 V ≈ charge cutoff 4.7 V); DFN confirms plated (−0.019 V, real 6.68 Ah charge).

## 5. Verification Hierarchy

| Protocol | Model | Output |
|---|---|---|
| 1C_discharge + calc-energy | SPMe / DFN | ED, midpoint, capacity, DCR |
| 4C_charge_45C (45 °C, 18 A to 4.7 V, plating on) | SPMe / DFN | charge Ah, anode min, T_max |
| aging_1C_100cyc (isothermal) | SPMe (DFN 1-cyc cross-check) | SEI thickness end |
