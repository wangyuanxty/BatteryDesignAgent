# Deliverable Format: Design Verification Plan and Report `dvpr.md` (Required, virtual test version)

> Read on demand per SKILL.md Section 1, Step 7. Values are mechanically taken from simulation results and annotated with their source line by line; uncovered conditions are honestly written as "N/A (requires physical experiment)"; no numbers are written from memory.

- **Format**: Markdown table. One row per verification item: item / condition / result value / determination (vs criteria or safety threshold) / source.
- **Verification items that can be produced (as per existing simulation protocols)**:
  | Item | Condition | Result source |
  |------|------|---------|
  | 1C discharge capacity | `run-pyamm --protocol 1C_discharge` | simulation |
  | 4C fast-charge temperature rise | `run-pyamm --protocol 4C_charge_45C --thermal lumped` | simulation |
  | 4C fast-charge plating | same as above + `--plating`, determined by negative electrode potential < 0 V | simulation |
  | Voltage window | parameter set upper/lower limits | parameter set |
- **Items explicitly marked N/A**: nail penetration, overcharge to thermal runaway, crush, drop, cycle life (no aging model), rate-pulse internal resistance — write "N/A (beyond pure simulation boundary, requires physical experiment)".
- **Conclusion section**: pass/fail summary + list of uncovered items (directly cited for paper limitations).
