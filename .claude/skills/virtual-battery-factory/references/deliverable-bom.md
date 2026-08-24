# Deliverable Format: Bill of Materials `bom.md` or `bom.xlsx` (Required)

> Read on demand per SKILL.md Section 1, Step 7. Values are mechanically taken from the parameter set / simulation results / literature and annotated with their source line by line; missing items are honestly written as "Not provided"; no numbers are written from memory.

- **Dual caliber**: g/cell and kg/kWh.
- **Rows**: positive electrode active material / positive electrode conductive additive / positive electrode binder, negative electrode active material / negative electrode conductive additive / negative electrode binder, separator, electrolyte, positive current collector Al, negative current collector Cu; enclosure and tabs (annotate "Not modeled").
- **Formulas**:
  - Component mass = coating thickness × area × volume fraction × density (volume fraction from the parameter set; when conductive additive/binder have no parameters, use literature default values with annotation)
  - kg/kWh = component mass ÷ cell energy (kWh, from simulation integration)
  - Electrolyte mass = pore volume × electrolyte density (when the parameter is missing, use the literature value 1.2 g/cm³ with annotation)
- **Summary rows**: total mass, total energy, material usage per unit energy (kg/kWh total).
