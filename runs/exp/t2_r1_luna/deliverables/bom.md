# Bill of materials (virtual model)

| Component | Specification | Status/source |
|---|---|---|
| Positive electrode | Chen2020 parameter-set positive electrode | simulator baseline |
| Negative electrode | Chen2020 parameter-set negative electrode | simulator baseline |
| Electrolyte transport | conductivity 2.0 S/m; diffusivity 2.0 m²/s; t+ 0.4 | `cell/params_variant.json` overrides |
| SEI-control proxy | SEI kinetic rate 1.0×10⁻¹³ m/s | `cell/params_variant.json` override |
| Separator/current collectors | Chen2020 defaults | simulator baseline |
| Casing/tabs | Not provided by simulation contract | not modeled |
