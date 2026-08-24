# Deliverable Format: Technical Datasheet `datasheet.md` (Required)

> Read on demand per SKILL.md Section 1, Step 7. Values are mechanically taken from the parameter set / simulation results / literature and annotated with their source line by line; missing items are honestly written as "Not provided"; no numbers are written from memory.

Standard customer-facing fields:

| Field | Source |
|------|------|
| Rated capacity (Ah) | nominal value from parameter set + simulation-verified value |
| Nominal voltage / voltage window (V) | parameter set |
| Rated energy (Wh) | simulation integration (time integration of V·I) |
| Energy density (Wh/kg) | simulation + contract-caliber mass formula |
| Maximum continuous discharge rate | 1C simulation result |
| Fast-charge capability | 4C simulation temperature rise and plating results |
| Operating temperature range | honestly given per simulation conditions |
| Cycle life | **annotate "Not simulated (requires aging model)" — must not fabricate** |
| Safety determination | plating/temperature rise determination results |
| Dimensions and mass | parameter set + mass formula |
