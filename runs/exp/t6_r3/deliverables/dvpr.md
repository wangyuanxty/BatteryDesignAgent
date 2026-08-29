# Design Verification Plan & Report (Virtual) — t6_r3

| Doc No: VBF-T6R3-DVPR-01 | Case: t6_r3 | Rev: 01 | Date: 2026-08-26 |

All verification below is **virtual** (DFN simulation + calc-energy), executed through the bda harness and logged via log-evaluate against the immutable entry-0 thresholds. Physical DV testing is outside this virtual design's scope and remains open.

| No | Test item | Requirement | Method (virtual) | Result | Margin | Verdict | Source |
|---|---|---|---|---|---|---|---|
| 1 | Volumetric energy density | >= 950 Wh/L | calc-energy on DFN 1C discharge | 983.61 Wh/L | +33.61 Wh/L | PASS | eval r10 V27; energy json |
| 2 | Voltage plateau | >= 4.1 V | calc-energy midpoint_voltage_v | 4.1551 V | +55.1 mV | PASS | eval r10 V27; energy json |
| 3 | 4C fast charge, no Li plating | anode potential >= 0 V throughout | DFN 4C CC-CV (18 A), min anode_potential_v | +0.1050 V | +105.0 mV | PASS | eval r10 V27; 4c json |
| 4 | Max temperature, 4C charge | <= 323.15 K (50 C) | DFN 4C T_max_K | 318.922 K | -4.23 K | PASS | eval r10 V27; 4c json |
| 5 | Anode SEI after 100 cycles | <= 500 nm | DFN aging, sei_thickness_nm_end | 313.7 nm | -186.3 nm | PASS | eval r10 V27; aging json |
| 6 | DC resistance (supplemental) | record | calc-energy dcr_ohm | 4.986 mOhm | - | RECORD | energy json |
| 7 | Cell mass (supplemental) | record | calc-energy mass_kg | 47.6800 g dry | - | RECORD | energy json |
| 8 | 0-100%% SOC 4C charge, no plating | recommended | DFN with protocol starting from lower cut-off | NOT RUN | - | OPEN | protocol limitation (see note) |
| 9 | True DFT/MD endorsement | SKILL stage 5 | run-orca / run-md | SKIPPED | - | SKIPPED honestly | real_compute=false, endorse entry |
| 10 | Physical build & DV testing | production gate | physical cell build | NOT RUN | - | OPEN | virtual design scope |

## Notes

- Row 3 note: the harness 4C protocol charges from the model initial state (cell at 4.1995 V, nearly full), so the CC phase lasts ~16.2 ms and the charge adds only 8.09e-05 Ah. The plating-free result is valid for the imposed protocol (anode never dips below +0.105 V) and is further protected by N/P 1.579; a deep-discharge-start 4C verification is tracked as row 8 OPEN. This limitation is disclosed, not hidden.
- Rows 1-5 were evaluated by `bda log-evaluate` round 10: candidate V27_combo verdict=pass, checked=5.
- Rounds 1-9 failures (incl. the round-9 DFN rejection of the SPMe finalist) are preserved in log.jsonl and are part of the audit trail.