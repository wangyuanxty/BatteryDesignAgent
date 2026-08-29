# Cell Design Specification

## Basic specification
- System: Chen2020 baseline parameter set; architecture candidate TinySeparatorParticles.
- Contract targets: energy density >=446.18 Wh/kg; 5C retention >=90%; cell mass <=0.040 kg.
- Result: **not achieved**.

## Performance verification
| Metric | Value | Source | Result |
|---|---:|---|---|
| Energy density | 427.476639 Wh/kg | cell/v5_derived.json | FAIL |
| Cell mass | 0.043216827 kg | cell/v5_derived.json | FAIL |
| 5C retention | 0.335044 | cell/v5_derived.json | FAIL |

Architecture parameters: separator 1 um; positive/negative particle radius 1 um. Electrolyte excluded from contract mass per calc-energy output. Dimensions and casing: Not provided.
