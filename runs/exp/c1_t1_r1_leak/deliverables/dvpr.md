# Design Verification Plan and Report (DVP&R) - c1_t1_r1
VBF-C1T1R1-DVPR-001 | Virtual Battery Factory

| # | Requirement | Protocol | Result | Verdict | Evidence |
|---|---|---|---|---|---|
| 1 | ED >= 392.61 Wh/kg | 1C discharge + calc-energy contract | 502.70 Wh/kg | PASS | cell/r4_v3_margin_energy.json |
| 2 | 4C fast charge without lithium plating | 4C_charge_45C protocol, 20 A, --plating, SPMe | anode potential min +0.0503 V | PASS | cell/r4_v3_margin_4c45c_spme.json |
| 3 | T_max <= 60 C in every scenario | lumped thermal, 45 C ambient (4C); overcharge 298.15 K ambient | 4C: 323.98 K; overcharge: 299.45 K | PASS | cell/r4_v3_margin_4c45c_spme.json / cell/r4_v3_margin_overcharge_spme.json |
| 4 | Overcharge to 4.7 V without thermal runaway | 0.5C charge to cut-off + 0.5 V (4.70 V), then run-tr --sim coupling (--mass-kg 0.0356025) | reached 4.70 V; triggered = false | PASS | validation/r4_v3_margin_tr.json |
| 5 | (backup) all criteria on alternative | same protocols on R4-V1-cool | ED 499.43; anode min +0.0247 V; T_max 325.08 K; TR not triggered | PASS | cell/r4_v1_cool_*.json, validation/r4_v1_cool_tr.json |
| 6 | (negative control) cooling ceiling | h=150 on R4-V4-coolmax | anode min -0.0006 V -> plated | FAIL (informs h upper bound) | cell/r4_v4_coolmax_4c45c_spme.json |

Verification method note: verdicts on rows 1-4 are mechanically recorded by
`bda log-evaluate` in log.jsonl (round 4, candidate R4-V3-margin: verdict=pass,
checked=4). Rows 5-6 are the same protocol applied to backup/negative-control variants.
