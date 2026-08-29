# Technical Datasheet — VBF-T5R3-DSH-01

**Product**: NMC811 / graphite flagship-vehicle pouch cell (virtual design, DFN-verified) · **Date**: 2026-08-26 · **Case**: t5_r3

| Field | Value | Source |
|---|---|---|
| Rated capacity (Ah) | 5.0 Ah nominal (parameter set); 5.0442 Ah simulation-verified (1C, DFN) | `param_dump.txt`; `cell/r6_y4_1c_dfn.json:capacity_ah` |
| Nominal voltage / voltage window (V) | Window 2.5 – 4.2 V; 1C midpoint 3.832 V | `param_dump.txt`; `cell/r6_y4_energy_dfn.json:midpoint_voltage_v` |
| Rated energy (Wh) | 18.2855 Wh (1C discharge integration) | `cell/r6_y4_energy_dfn.json:energy_wh` |
| Energy density | **535.72 Wh/kg** (contract caliber, electrolyte excluded); 995.79 Wh/L | `cell/r6_y4_energy_dfn.json:energy_density_wh_kg / energy_density_wh_l` |
| Maximum continuous discharge rate | 1C (5 A) verified by 1C_discharge protocol at 298.15 K; higher-rate discharge not simulated | `r6_y4_1c_dfn.json`; 5C/lowT protocols not part of task metrics |
| Fast-charge capability | **4C CC (20 A): 0 → ≈69% SOC (3.48 Ah) in 626 s**, then 4.2 V cut-off; T_max 327.60 K; anode potential never below 0 V (min +0.0200 V) → **no plating signature**. CV tail beyond cut-off not simulated (current decays below 4C; plating risk monotonically decreases with current — domain reasoning, not a simulated claim). Unmodified baseline clamps at ≈26 s (0.14 Ah): this design extends the CC window ≈24× | `r6_y4_4c_dfn.json:time_s/voltage_v/anode_potential_v/T_max_K` |
| Operating temperature range | Verified points: 298.15 K 1C discharge; 318.15 K ambient 4C charge (cell peak 327.60 K). Full-range map N/A (lowT/highT protocols not part of task metrics) | protocol definitions in `bda` runner |
| Cycle life | **Not simulated (requires aging model)** — not provided, must not be inferred | — |
| Safety determination | 4C fast charge: no plating (min anode potential +0.0200 V ✓) and T_max 327.60 K ≤ 333.15 K ✓. Overcharge/nail/crush: N/A (beyond pure-simulation boundary, requires physical experiment) | `r6_y4_4c_dfn.json` |
| Dimensions and mass | Stack 178.8 µm × 0.1027 m² electrode area (0.065 m × 1.58 m); 34.13 g (contract, electrolyte excluded) / 40.28 g incl. electrolyte estimate (1.2 g/cm³, annotated); enclosure not provided | `r6_y4_energy_dfn.json:thickness_m/area_m2/mass_kg` + `param_dump.txt` |

*This datasheet is a virtual-simulation document. Every value is mechanically derived from command outputs; no physical cell has been built. True-compute endorsement skipped (`real_compute=false`, recorded in log.jsonl endorse entry).*