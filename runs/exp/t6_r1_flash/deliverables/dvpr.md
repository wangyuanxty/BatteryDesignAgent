# Design Verification Plan & Report — finN-2e19

**Document**: VBF-T6R1F-DVPR-01 | **Case**: t6_r1_flash | **Date**: 2026-08-25 | **Model fidelity**: SPMe (screening) + DFN (final endorsement, task 5)

## 1. Verification Matrix

| # | Criterion | Requirement | Method | Protocol | Result | Verdict |
|---|---|---|---|---|---|---|
| M1 | Volumetric energy density | ≥ 950 Wh/L | calc-energy (contract formula) | 1C_discharge, DFN | 1171.7 Wh/L | **PASS** |
| M2 | Voltage plateau | ≥ 4.1 V | midpoint voltage | 1C_discharge, DFN | 4.145 V | **PASS** |
| M3 | SEI after 100 cycles | ≤ 500 nm | SEI thickness (Yang2017 EC-limited) | aging_1C_100cyc, SPMe (DFN 1-cyc x-check) | 292.2 nm | **PASS** |
| M4 | 4C charge, no plating | plated = false | anode potential min ≥ 0 | 4C_charge_45C (18 A to 4.7 V, plating model) | −0.019 V (DFN) → plated | **FAIL** (boundary, see §3) |
| M5 | Max temperature | ≤ 50 °C (323.15 K) | T_max (lumped thermal, DFN heat) | 4C_charge_45C, 45 °C amb, h=300 | 322.50 K | **PASS** |

## 2. Evidence Files (case-relative)

| Metric | File | Key |
|---|---|---|
| M1, M2 | cell/r5_finN_dfn_1c_calc.json | energy_density_wh_l, midpoint_voltage_v |
| M3 | cell/r5_finN2e19_aging.json | sei_thickness_nm_end |
| M4, M5 | cell/r5_finN_dfn_h300_4c.json | anode_potential_v (min), T_max_K |
| M3 x-check | cell/r5_finN_dfn_aging.json | sei_thickness_nm_end (1 cyc) |

Audit trail: log.jsonl entries — propose R1–R5, evaluate R1(2)/R2(5)/R3(5)/R4(4)/R5(10), plan (initial + 2 updates), design finN-2e19, verify DFN.

## 3. M4 Failure Analysis (documented boundary)

- **Observation**: every configuration with a real 4C charge (5.3–7.4 Ah) shows anode minimum −0.21…−0.26 V (SPM) / −0.02 V (DFN) at the cutoff; every mechanically-passing configuration delivers ≤ 0.003 Ah (degenerate charge, rejected).
- **Root cause**: LNMO OCP ceiling 4.706 V ≡ charge cutoff 4.7 V → at the cutoff the anode potential is pinned by the cathode side (`ap = U_pos+η_pos−4.7−φ_e(sep)`); φ_e(sep) ≈ +0.2 V is dominated by electrolyte potential in the anode (measured 11× ohmic estimate) and cannot be removed with physical parameters (σ ≳ 100 S/m required).
- **Rounds to establish**: 3 consecutive rounds (R3–R5), same cause → three-strike questioning recorded in plan update 2.
- **Decision**: retain a real 6.68 Ah 4C charge (the functional intent of "4C fast charge") and record M4 as fail; degenerate "passes" explicitly not claimed. This is a system/protocol interaction, not a fixable component defect (see DFMEA FM-1).
- **Residual options** (outside this case's degrees of freedom): lower charge cutoff (usage-mode parameter, excluded), different cathode system (electrode system locked by task).

## 4. DFN Cross-Validation (task 5)

| Quantity | SPMe | DFN | Δ |
|---|---|---|---|
| ED (Wh/L) | 1172.1 | 1171.7 | −0.03% |
| Midpoint (V) | 4.248 | 4.145 | −2.4% |
| Capacity (Ah) | 6.347 | 6.324 | −0.4% |
| 4C charge (Ah) | 6.97 | 6.68 | −4.2% |
| Anode min (V) | −0.262 | −0.019 | — |
| T_max @h120 (K) | 321.9 | 326.1 | +4.3 K |

SPMe is adequate for ED/capacity screening; **thermal and plating verdicts taken at DFN fidelity**.

## 5. Pass/Fail Summary

**3/4 criteria PASS with margin; M4 FAIL (documented protocol-level boundary). Case verdict: partial pass with honest M4 record.**
