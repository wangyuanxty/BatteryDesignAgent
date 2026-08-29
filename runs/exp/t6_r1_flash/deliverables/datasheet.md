# Datasheet — finN-2e19 Smartphone Battery (LNMO 4.7 V-class)

**Document**: VBF-T6R1F-DSH-01 | **Case**: t6_r1_flash | **Date**: 2026-08-25 | **Values**: DFN simulation (SPM in parentheses where differing)

## 1. Electrical Characteristics

| Parameter | Value | Conditions |
|---|---|---|
| Nominal capacity | 6.32 Ah (6.35) | 1C discharge, 25 °C, 2.5–4.7 V |
| Nominal energy | 26.2 Wh | 1C discharge |
| Midpoint voltage (plateau) | 4.145 V (4.248) | voltage at discharge-time midpoint |
| Operating voltage window | 2.5 – 4.7 V | CC charge cutoff 4.7 V |
| DC resistance | 4.8 mΩ | OCV − V @10% DOD ÷ 1C |
| Power density | 20.4 kW/kg | V_OC²/(4·DCR)/mass |
| Self-heating / peak T | 49.4 °C (322.5 K) | 4C charge, 45 °C ambient, h=300 |

## 2. Fast-Charge Behavior (4C = 18 A, 45 °C ambient)

| Parameter | Value |
|---|---|
| Charge acceptance | 6.68 Ah (6.97) — **real charge, 22.3 min** |
| Max temperature (h=300) | 322.5 K — **≤ 50 °C PASS** |
| Anode min potential | −0.019 V (DFN) / −0.262 V (SPM) — **plating flagged (M4 fail, see design_spec §4)** |
| h sensitivity | 326.1 K (h120) / 323.8 (h200) / 323.1 (h250) / 322.5 (h300) |

## 3. Aging (100 cycles, 1C, isothermal)

| Parameter | Value |
|---|---|
| SEI thickness end-of-test | 292 nm (D_ec 2e-19) — **≤ 500 nm PASS**; bracket: 357 nm @3e-19 |
| SEI growth regime | diffusion-limited (L ∝ √(D_ec·t)) |

## 4. Physical Characteristics (contract caliber; electrolyte/casing excluded)

| Parameter | Value |
|---|---|
| Stack thickness | 217.6 µm |
| Footprint area | 0.1027 m² (0.065 m × 1.58 m runner convention) |
| Mass | 45.9 g |
| Volume | 22.35 cm³ |
| Energy density (vol) | 1171.7 Wh/L |
| Energy density (grav) | 569.9 Wh/kg |
| Electrolyte included | No (parameter set lacks density — contract caliber) |

## 5. Electrode/Electrolyte System

- Cathode: LNMO spinel (LiNi₀.₅Mn₁.₅O₄), 74 µm, ε 0.665, r_p = 2.0 µm, OCP ceiling 4.706 V.
- Anode: graphite, 120 µm, ε_act 0.65, r_p = 3.0 µm.
- Electrolyte: high-transference (t⁺ 0.9), high-conductivity (σ 20 S/m, D 1e-9) additive formulation.
- SEI: LiF-rich (EC diffusivity 2e-19 m²/s).
- Cooling: vapor chamber + graphite + Al frame, effective h = 300 W/m²K (h=250 minimum verified).

## 6. Compliance Summary

| Criterion | Value | Requirement | Verdict |
|---|---|---|---|
| ED volumetric | 1171.7 Wh/L | ≥ 950 | PASS |
| Plateau voltage | 4.145 V | ≥ 4.1 | PASS |
| SEI @100 cyc | 292 nm | ≤ 500 | PASS |
| No plating @4C | plated | false | **FAIL — documented protocol boundary** (real charge retained) |
| T_max @4C | 322.5 K | ≤ 323.15 | PASS |

## 7. Caveats

- All values simulation-derived (SPMe + DFN cross-check); no hardware build.
- Electrolyte transport parameters (σ 20 S/m, t⁺ 0.9) are aggressive estimates — see design_spec §6.
- The M4 fail is a system-level (LNMO cutoff) interaction, not a component defect — see design_spec §4 and DFMEA.
