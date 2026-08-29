# Battery Design Specification

**Case:** t7_r1_luna  **Status:** Virtual design release

## Recommended cell
Chen2020-based lithium-ion cell with 55 µm positive and 60 µm negative electrode layers, 42%/38% positive/negative porosity, 1.5 µm particles, electrolyte conductivity 2.5 S m⁻¹, cation transference 0.60. Thermal-management boundary for nail verification: hA=1000 W K⁻¹.

## Verified targets
Energy density 396.968 Wh/kg; 45 °C/100-cycle SEI 411.823 nm; 4C/45 °C plating absent; 10 W nail thermal-runaway trigger absent under the stated hA boundary. Sources: `cell/E_energy.json`, `cell/E_aging.json`, `cell/E_4c.json`, `cell/E_nail_cooled.json`.

This is a virtual design and does not establish manufacturability, abuse certification, or pack-level cooling feasibility.
