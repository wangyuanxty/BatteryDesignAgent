# Deliverable Format: Cell Design Specification `design_spec.md` (Required)

> Read on demand per SKILL.md Section 1, Step 7. Values are mechanically taken from the parameter set / simulation results / literature and annotated with their source line by line; missing items are honestly written as "Not provided"; no numbers are written from memory.

- **Format**: Markdown, primarily tables.
- **Sections and fields**:
  1. Basic specification: electrochemical system, nominal capacity (Ah), voltage window (V), cell dimensions (height × width × thickness mm; mark "Not provided" when shell thickness has no parameter), electrolyte formulation (including additive candidates), cation transference number
  2. Electrode and separator: layer thicknesses (µm), porosity, current collector material and thickness, N/P ratio (= negative electrode capacity density × thickness ÷ positive electrode capacity density × thickness)
  3. Process design parameters (table below, merged into this section)
  4. Mass breakdown: mass of each layer and total mass (g, with formula-caliber note)
  5. Performance verification table: 1C capacity, energy density, 4C temperature rise, plating determination — each row accompanied by the pass/fail determination (✓/✗ vs criteria item 0)
  6. Design notes: which parameters were changed in this case and why (citing the reasoning from the evaluate log)

### Process Design Parameter Formulas

| Parameter | Formula | Unit Notes |
|------|------|---------|
| Areal density | thickness × (1 − porosity) × electrode density | g/m² |
| Compaction density | electrode density × (1 − porosity) | kg/m³ → g/cm³ divide by **1000** (common thousand-fold error point) |
| Electrolyte fill amount | pore volume × electrolyte density × fill factor | electrolyte density uses a literature value (e.g. 1.2 g/cm³) with annotation |
| Formation recommendation | e.g. "0.1C CC to 4.2V, 25℃, 2 cycles" | annotate "design recommended value; actual production-line value requires tuning" |
