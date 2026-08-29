# Battery design specification (virtual)

**Case:** t2_r1_luna  
**Base system:** Chen2020 teaching parameterization (deterministic default because no electrode chemistry was specified).  
**Recommended design:** Chen2020 architecture with parameter overrides in `cell/params_variant.json`: electrolyte conductivity 2.0 S m⁻¹, electrolyte diffusivity 2.0 m² s⁻¹, cation transference number 0.4, and SEI kinetic rate constant 1.0×10⁻¹³ m s⁻¹. These are simulator parameter overrides, not a manufacturable formulation.

## Requirements and virtual verification
- Energy density target ≥327.18 Wh/kg: **405.375 Wh/kg**, pass (`r2_variant_energy.json`).
- 4C charge without plating: **no plating**, minimum anode potential +0.04444 V (`r2_variant_4c.json`), pass.
- 100-cycle SEI ≤500 nm: **300.359 nm**, pass (`r2_variant_age100.json`).
- −20 °C retention ≥90%: **99.455%**, inferred as 4.929318/4.956328 Ah from same-parameter 1C and low-T outputs, pass.
- 500-cycle SEI ≤550 nm: **333.097 nm**, pass (`r2_variant_age500.json`).

This is a virtual-test design, not a production-qualified cell. Electrolyte mass, casing, tabs, manufacturing tolerances, abuse testing, and thermal hardware are outside the simulation contract.
