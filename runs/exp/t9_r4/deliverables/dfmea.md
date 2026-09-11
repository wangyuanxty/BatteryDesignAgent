# VBF-T9R4-DFMEA-001 Failure Modes & Effects (design phase)

t9_r4 - grid-storage cell cathode on the Chen2020 NMC811/graphite profile
Result: HONEST NEGATIVE (no candidate satisfies the full contract; nothing reported as passing)

| Failure mode | Effect | Cause | S | O | D | Mitigation / outcome |
|---|---|---|---|---|---|---|
| d0/d10 O-redox top-of-charge pathology | charging potential far above the electrolyte anodic limit | pathological x=0.3 endpoint (last Li in a deep trap; ~9 eV off-trend) | 10 | 8 | 3 | MEASURED: AlB55 7.410 V -> line abandoned |
| Avg-voltage artifact (sharp 50:50 peak) | false window pass | unstable delithiated state inflates the average | 8 | 6 | 3 | Detected by the incremental-profile co-gate before any cell work |
| TM-redox layered voltage cap ~4.0 V | window unreachable | 3d redox levels of the family | 8 | 8 | 2 | Envelope documented across 42 candidates |
| Non-layered ED infeasibility | ED < 327.18 under the 0.9-capacity rule | capacity bounds of olivine/spinel/tavorite/NASICON | 8 | 7 | 2 | Decisive calc: only layered can pass |
| Relaxation non-convergence (fmax 0.1/300 steps) | mV-level noise in voltages | FIRE step budget; universal in this machinery | 2 | 8 | 1 | Reproducibility checked: independent re-compute within 6 mV |
| Overestimate-prone family claims | guard failure | Ni-rich olivine inflation (LiNiPO4 7.016 vs 5.1) | 6 | 5 | 2 | Not used; layered family self-calibrates (NMC811 3.80 vs 3.8) |
| Session/background loss | compute lost | harness kills background tasks at turn end | 4 | 6 | 2 | Checkpointed gate script (one state per blocking call) |

Residual risk accepted: none - the negative result is over-determined by walls (i) and (ii),
independent of relaxation noise.