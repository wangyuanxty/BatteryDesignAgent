# DVP&R - VBF-T5R2-DVPR-01

Case t5_r2 - acceptance criteria from log.jsonl entry 0 (frozen contract). Method = bda simulator chain.

| ID | Requirement | Method | Target | Result | Verdict | Evidence |
|---|---|---|---|---|---|---|
| DVP-01 | Delivers contract capacity (nominal 6.5 Ah class) | simulated 1C CC discharge (DFN) | >= 6.5 Ah (design nominal) | 7.171 Ah | PASS | cell/r7_final_f2_energy_dfn.json capacity_ah |
| DVP-02 | Energy density >= 500.94 Wh/kg | calc-energy on 1C DFN discharge | >= 500.94 | 666.3 Wh/kg | PASS | cell/r7_final_f2_energy_dfn.json (log-evaluate round 7) |
| DVP-03 | 4C charge without lithium plating | 4C_charge_45C (1C disc + 4C CC to 4.2 V, 45 C) anode potential | min > 0 V | min +0.0506 V | PASS | cell/r7_final_f2_4c45.json anode_potential_v |
| DVP-04 | Max temperature <= 60 C at 4C | lumped thermal in 4C_charge_45C | <= 333.15 K | 330.984 K = 57.83 C | PASS | cell/r7_final_f2_4c45.json T_max_K |
| DVP-05 | Voltage window integrity | parameter-set bounds | 2.5 - 4.2 V | as designed | PASS | Chen2020 parameter set |
| DVP-06 | Mid-voltage / polarity | midpoint of 1C discharge | positive, stable | 3.78 V | PASS | cell/r7_final_f2_energy_dfn.json |

N/A rows (criteria not in contract OR simulator out of scope - honestly not simulated):

| ID | Requirement | Reason not run |
|---|---|---|
| DVP-07 | Nail penetration / internal-short thermal runaway | no such simulator in the protocol funnel; N/A (physical test required) |
| DVP-08 | Overcharge to thermal runaway (+0.5 V protocol) | overcharge protocol exists but is outside the frozen criteria; NOT run to avoid unrequested scope |
| DVP-09 | Crush / drop / vibration | mechanical abuse out of simulator scope |
| DVP-10 | Cycle life (rated) | not in acceptance criteria; informational aging run exists but its per-cycle capacity series is protocol-artifact-flagged - a rated cycle-life figure is NOT claimed |
| DVP-11 | Rate-pulse internal resistance spec | DCR reported informationally (2.538 mohm); no target registered in contract |
