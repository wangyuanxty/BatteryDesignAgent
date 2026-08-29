# Design Specification — VBF-T6_R1_LUNA-DS-001

## Status
Virtual design verification only; **not achieved** within the Chen2020 baseline boundary.

## Contract requirements
- Volumetric energy density: ≥950 Wh/L
- 4C charge without lithium plating
- Maximum temperature: ≤50 °C (323.15 K)
- 100-cycle SEI thickness: ≤500 nm
- Voltage plateau: ≥4.1 V

## Tested design
Chen2020 baseline with Architecture-V3 overrides: positive/negative particle radius 1 µm, electrolyte conductivity 2.5 S/m, total heat transfer coefficient 50 W m⁻² K⁻¹. These are simulation inputs, not manufacturing specifications.

## Verification outcome
Architecture-V3: 895.5999365 Wh/L, 321.6325618 K (48.4826 °C), plating true, SEI 373.7647636 nm. Energy density and plating fail; temperature and SEI pass. Source: `cell/r3_v3_energy.json`, `cell/r3_v3_safety.json`, `cell/r3_v3_aging.json`.

Manufacturing drawings, tolerances, and process cards are outside the virtual-simulation boundary.
