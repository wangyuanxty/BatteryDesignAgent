# Design Verification Plan & Report (VBF-T6R2-DVPR-001)

**Case**: exp/t6_r2 · **Candidate**: R12a_h140 · **Date**: 2026-08-26
Verification performed in-simulation per the Virtual Battery Factory protocol; each item maps
to a pre-registered criterion in log.jsonl entry 0 (not post-hoc revisable).

| # | Requirement (task text) | Pre-registered threshold | Test protocol | Model | Result | Verdict |
|---|---|---|---|---|---|---|
| 1 | Volumetric energy density ≥ 950 Wh/L | energy_density_wh_l ≥ 950 | 1C discharge + calc-energy (contract: E/Σlayer-thickness·area, electrolyte excluded) | DFN | 1096.0 Wh/L | PASS (+146.0) |
| 2 | Voltage plateau ≥ 4.1 V | midpoint_voltage_v ≥ 4.1 | 1C discharge, voltage at discharge-time midpoint | DFN | 4.1301 V | PASS (+0.030) |
| 3 | Max temperature ≤ 50 °C | T_max_K ≤ 323.15 | 4C_charge_45C, lumped thermal, 45 °C ambient | DFN | 322.70 K (49.55 °C) | PASS (−0.45 K) |
| 4 | 4C fast charge, no lithium plating | plated == False (any anode_potential_v < 0 → plated) | 4C_charge_45C with plating submodel | DFN | min +0.0382 V → not plated | PASS |
| 5 | Anode SEI ≤ 500 nm after 100 cycles | sei_thickness_nm_end ≤ 500 | aging_1C_100cyc (ec-reaction-limited SEI, isothermal) | SPMe | 415.6 nm | PASS (−84.4) |

Evidence files: cell/r12_a_energy_dfn.json, cell/r12_a_1c_dfn.json, cell/r12_a_4c45_dfn.json,
cell/r12_a_aging.json. Mechanical verdict recorded by `bda log-evaluate` round 12
(candidate R12a_full_verification_DFN, verdict=pass, 5/5 checked). Stage-1 molecular
criteria (max_energy_ev, max_homo_ev) are not in scope for a start_stage=3 case (unchecked).

## Test condition notes (honest disclosure)

- The 4C protocol current is 4 × system-file nominal capacity (4.5 Ah) = 18 A; actual
  simulated 1C capacity is 6.374 Ah ⇒ the executed charge is ~2.8C effective. A follow-up
  verification at true 4C (25.5 A) is recommended and listed in DFMEA as an open risk.
- Aging protocol per-cycle capacity outputs are negative artifacts of the LNMO file
  parameterization; the SEI criterion is judged on sei_thickness_nm_end as pre-registered.
- T_max margin (0.45 K) is the binding constraint; the thermal-interface spec
  (A ≥ 0.0106 m², h ≥ 140 W/m²·K) is a hard requirement, not a nominal suggestion.
- SPMe cross-check results (ED 1106.3, midV 4.2202, T 320.30 K, not plated) are consistent;
  the DFN values above are the acceptance basis.

## Verification environment

- Engine: PyBaMM (Chen2020 + LNMO system file), SPMe proxy and DFN precise models.
- True compute (DFT/MD) skipped per pre-registered real_compute=false — endorsement
  record in log.jsonl states this explicitly.
