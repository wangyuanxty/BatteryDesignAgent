# Deliverable Format: Design FMEA `dfmea.md` (Required, qualitative version)

> Read on demand per SKILL.md Section 1, Step 7. Qualitative ratings are based on simulation risk signals; annotate "qualitative version, based on simulation signals"; no numbers are written from memory.

- **Format**: Markdown table. One row per failure mode: failure mode / failure cause / simulation signal (detectability basis) / qualitative severity / qualitative occurrence / design-side mitigation recommendation.
- **Failure modes that can be listed based on existing simulation signals**:
  | Failure mode | Simulation signal source |
  |---------|-------------|
  | Negative electrode plating (fast charge) | `anode_potential_v < 0 V` |
  | Thermal runaway risk (temperature rise exceeds limit) | `T_max_K` vs threshold |
  | Electrolyte oxidative decomposition (voltage window) | HOMO/IE-EA vs voltage window (final DFT endorsement caliber) |
  | Insufficient capacity | 1C `capacity_ah` vs target |
- **Severity/occurrence**: S (high/medium/low), O (high/medium/low) three-level qualitative rating, basis = the magnitude of the simulation value deviating from the threshold; RPN can use a simplified qualitative matrix of S×O (annotate the qualitative caliber).
- **Conclusion section**: list of highest-risk items + statement that mitigation measures have been implemented in the design; the complete FMEA (including process/supplier failures) is annotated "N/A (beyond pure simulation boundary)".
