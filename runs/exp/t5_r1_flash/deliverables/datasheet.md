# Technical Datasheet — t5_r1_flash

**Doc No. VBF-T5R1FLASH-DSH-01** · Customer-facing summary · Rev A (2026-08-25)

| Field | Value | Source |
|---|---|---|
| Rated capacity | 4.5 Ah (nominal, parameter set) · 8.26 Ah (simulated 1C, DFN) | LNMO.json; cell/r9_lnmo_r6_1c_dfn.json |
| Nominal voltage / window | 4.24 V midpoint · 2.5–4.7 V | calc-energy midpoint_voltage_v; LNMO.json cut-offs |
| Rated energy | 35.16 Wh | calc-energy energy_wh (V·I integration) |
| Energy density | 597.9 Wh/kg (contract caliber, electrolyte excluded; with electrolyte 501 Wh/kg informational) | calc-energy + contract mass formula |
| Volumetric energy density | 1141 Wh/L | calc-energy energy_density_wh_l |
| Maximum continuous discharge rate | 1C demonstrated (8.26 Ah); 5C not run in this case (N/A — not part of contract) | 1C_discharge protocol |
| Fast-charge capability | 4C @45 °C ambient: T_max 327.6 °C (≤60 °C ✓), no lithium plating (anode min +14.7 mV) | 4C_charge_45C DFN |
| Operating temperature range | 25 °C nominal / 45 °C fast-charge ambient (simulated conditions only) | protocol conditions |
| Cycle life | **Not simulated (requires aging model)** — must not fabricate | — |
| Safety determination | PASS: plating-free 4C charge; T_max within limit | dvpr.md |
| Dimensions / mass | stack 300 µm × 0.1027 m² · 58.8 g (contract) | calc-energy |
| DC resistance | 8.0 mΩ (formula caliber) | calc-energy dcr_ohm |
| Electrolyte | HiTrans-class transport (σ 6 S/m, t⁺ 0.7, D 1e-9 m²/s, estimate) + FEC/VC/PES/DTD additives | params; funnel3 |

**Limitations (honest):** cycle life, calendar aging, mechanical abuse (nail/crush/drop), overcharge-to-thermal-runaway, and low-temperature performance were not simulated — beyond the pure-simulation boundary of this case (see DVPR-01). Transport values are domain estimates pending true MD endorsement.
