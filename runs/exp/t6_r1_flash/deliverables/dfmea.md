# DFMEA — finN-2e19 Smartphone Battery

**Document**: VBF-T6R1F-DFMEA-01 | **Case**: t6_r1_flash | **Date**: 2026-08-25 | **Severity/occurrence/detection**: 1–10 scale (10 = worst); RPN = S×O×D

## FM-1: Lithium plating during 4C fast charge (M4)

| Item | Value |
|---|---|
| Failure mode | Anode potential < 0 V at the 4.7 V charge cutoff → Li deposition on graphite surface |
| Effect | Capacity fade, safety risk; violates M4 |
| Cause | LNMO OCP ceiling (4.706 V) ≈ charge cutoff (4.7 V): anode potential pinned at −0.02…−0.26 V by cathode side; φ_e(sep) ≈ +0.2 V (electrolyte potential in anode) |
| Current controls | High-transference electrolyte (t⁺ 0.9, σ 20 S/m, D 1e-9) — reduces φ_e; dense short anode (120 µm, ε 0.65) — shortens conduction path; verified at DFN |
| S / O / D / **RPN** | 9 / 9 / 2 / **162** |
| Verification | 4C_charge_45C with plating model: plated (DFN −0.019 V, SPM −0.262 V) → **residual risk confirmed** |
| Recommended action | Out of DOF scope: lower charge cutoff (< 4.65 V, usage-mode — excluded), cathode with OCP ceiling > 4.7 V (electrode system locked), or asymmetric plating-aware charging profiles. Residual risk documented in design_spec §4. |

## FM-2: Thermal excursion at 4C (M5)

| Item | Value |
|---|---|
| Failure mode | T_max > 50 °C during 4C charge at 45 °C ambient |
| Effect | Aging acceleration, safety margin loss |
| Cause | 4C polarization heat + 45 °C ambient; lumped-SPM underestimates peak by 4.3 K |
| Current controls | Vapor chamber + graphite + Al frame: h = 300 W/m²K (h=250 verified minimum); DFN-verified 322.5 K |
| S / O / D / **RPN** | 7 / 3 / 4 / **84** |
| Verification | DFN h-sweep: 120→326.1 fail, 200→323.8 fail, 250→323.1 pass, 300→322.5 pass |
| Recommended action | Keep h ≥ 300; monitor in production with thermocouple on tab (O→2). |

## FM-3: SEI overgrowth > 500 nm by 100 cycles (M3)

| Item | Value |
|---|---|
| Failure mode | SEI thickness exceeds 500 nm → Li inventory loss, impedance rise |
| Effect | Capacity fade, power loss |
| Cause | EC permeation through SEI (diffusion-limited growth L ∝ √(D_ec·t)); deep per-cycle cycling |
| Current controls | LiF-rich SEI (D_ec 2e-19 m²/s): 292.2 nm @100 cyc (42% margin); bracket 356.6 nm @3e-19 |
| S / O / D / **RPN** | 6 / 2 / 5 / **60** |
| Verification | aging_1C_100cyc (SPMe), DFN 1-cycle cross-check 27.4 nm |
| Recommended action | None (margin adequate); re-verify at 45 °C cycling if duty cycle changes. |

## FM-4: Capacity fade beyond 20% (system-level)

| Item | Value |
|---|---|
| Failure mode | End-of-life capacity < 80% before warranty life |
| Effect | Customer-visible runtime loss |
| Cause | SEI consumption + (if FM-1 occurs) plating-induced loss — FM-1 is the dominant driver |
| Current controls | FM-1/FM-3 mitigations |
| S / O / D / **RPN** | 5 / 3 / 5 / **75** |
| Verification | aging capacity trend recorded (see log aging outputs); no contractual retention criterion |
| Recommended action | Tied to FM-1 resolution. |

## FM-5: Energy density shortfall (M1)

| Item | Value |
|---|---|
| Failure mode | ED_vol < 950 Wh/L |
| Effect | Cannot meet product requirement |
| Cause | Mass/volume overrun, porosity increase, electrolyte inventory growth |
| Current controls | Thin separator (8 µm) / thin CC (8/6 µm); dense electrodes (ε_neg 0.65); measured 1171.7 Wh/L (23% margin) |
| S / O / D / **RPN** | 4 / 2 / 4 / **32** |
| Verification | calc-energy (contract formula), DFN |
| Recommended action | None. |

## FM-6: Plateau voltage below 4.1 V (M2)

| Item | Value |
|---|---|
| Failure mode | Midpoint < 4.1 V |
| Effect | Fails spec; power electronics design point shifts |
| Cause | LNMO OCP shape (inherent) + polarization at 1C |
| Current controls | Minimal polarization (small particles r 2.0 µm, high-σ electrolyte); measured 4.145 V (DFN, margin 0.045 V) |
| S / O / D / **RPN** | 5 / 1 / 4 / **20** |
| Verification | calc-energy midpoint, DFN |
| Recommended action | Margin is the thinnest among passing criteria — monitor particle-size control in production. |

## Priority Ranking

| Rank | FM | RPN | Status |
|---|---|---|---|
| 1 | FM-1 Plating (M4) | 162 | **Residual risk — documented boundary** |
| 2 | FM-4 Capacity fade | 75 | Linked to FM-1 |
| 3 | FM-2 Thermal (M5) | 84 | Mitigated (h=300) |
| 4 | FM-3 SEI (M3) | 60 | Mitigated (D_ec 2e-19) |
| 5 | FM-6 Plateau (M2) | 20 | Passed |
| 6 | FM-5 ED (M1) | 32 | Passed |
