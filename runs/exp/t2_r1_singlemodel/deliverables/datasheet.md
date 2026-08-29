# Technical Datasheet — VBF-T2R1SINGLEMODEL-DSH-01

> Case t2_r1_singlemodel — grid energy storage cell (virtual design). Generation date 2026-08-25.

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah (parameter set nominal); 6.9555 Ah (simulated 1C discharge) | parameter set / cell/r3_1c_dfn.json |
| Nominal voltage / window | 2.5 – 4.2 V; midpoint 3.574 V | parameter set / cell/r3_energy.json |
| Rated energy | 25.03 Wh | cell/r3_energy.json (V*I integration) |
| Energy density | 358.0 Wh/kg (contract caliber, electrolyte excluded) | cell/r3_energy.json |
| Max continuous discharge rate | 1C verified (6.9555 Ah); 5C 0.4939 Ah (7% of 1C; voltage collapses to cut-off in ~71 s — severely rate-limited; informational, no 5C criterion) | cell/r3_1c_dfn.json, cell/r3_5c_dfn.json |
| Fast-charge capability | 4C CC to 4.2 V: 5.57 Ah charged, anode potential min +0.112 V (no plating), T_max 342.5 K | cell/r3_4c45.json |
| Operating temperature range | -20 C discharge verified (retention 99.6 %); 45 C charge verified; storage limits Not provided | cell/r3_lowT.json / cell/r3_4c45.json |
| Cycle life (SEI) | 194.6 nm @100 cyc; 439.7 nm @500 cyc (DFN aging, ec reaction limited; capacity trajectory shows the standard climb artifact — SEI thickness is the reliable indicator) | cell/r3_aging100.json / cell/r3_aging500_d1e19.json |
| Safety determination | 4C plating-free (virtual); overcharge-coupled TR not triggered (partial-run T_max 322.7 K; DFN overcharge 4.7 V charge phase unsolvable — recorded verbatim); 5 W nail triggers TR (T_max 408.4 K) | cell/r3_tr.json / cell/r3_tr_nail.json |
| Dimensions and mass | 65 x 1580 x 0.390 mm (layer stack); 69.9 g (electrolyte excluded) | parameter set / cell/r3_energy.json |
