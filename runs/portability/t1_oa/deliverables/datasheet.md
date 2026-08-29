# Technical Datasheet — VBF-T1OA-DSH-01

> Next-generation pure electric sedan cell (virtual design). Values from parameter set / simulation output; sources annotated.

| Field | Value | Source |
|---|---|---|
| Rated capacity | 5.0 Ah nominal / 5.057 Ah (1C DFN verified) | parameter set / `cell/T10_1c_dfn.json` |
| Nominal voltage / window | 2.5 – 4.2 V (midpoint 3.74 V at 1C) | parameter set / `cell/T10_energy_dfn.json` |
| Rated energy | 18.55 Wh (1C discharge integration) | `cell/T10_energy_dfn.json:energy_wh` |
| Gravimetric energy density | 426.89 Wh/kg (contract caliber, electrolyte excluded) | `cell/T10_energy_dfn.json` |
| Volumetric energy density | 899.5 Wh/L (contract caliber) | `cell/T10_energy_dfn.json` |
| Maximum continuous discharge rate | 1C (5 A) verified; 4C charge verified for fast charge | simulation protocol |
| Fast-charge capability | 4C charge @45 °C: T_max 324.55 K (51.4 °C), no lithium plating (anode min +0.0341 V) | `cell/T10_4c_dfn.json` |
| Operating temperature range | simulated at 298 K (discharge) and 318 K (4C charge); full range Not simulated | simulation protocols |
| Cycle life | Not simulated (aging model not run for this chemistry) — must not fabricate | — |
| Safety | no plating at 4C; T_max ≤ 60 °C; overcharge to 4.70 V without thermal runaway (triggered=false) | `cell/T10_4c_dfn.json`, `cell/T10_tr.json` |
| Dimensions | 65 mm × 1580 mm × 200.8 µm (active stack) | parameter set / calc-energy |
| Mass | 43.45 g (active stack, electrolyte & casing excluded) | `cell/T10_energy_dfn.json:mass_kg` |
| Chemistry | NMC811 / graphite+SiOx (OKane2022) | parameter set |
