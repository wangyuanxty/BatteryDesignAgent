# Design Verification Plan & Report

## Virtual tests
1. 1C discharge and contract-caliber `calc-energy`.
2. Coupled lumped-thermal 4C charge at 45 °C with plating enabled.
3. Mechanical evaluation against preregistered thresholds via `bda log-evaluate`.

## Results
All four evaluated candidates failed at least one criterion. Best ED was 475.969 Wh/kg versus 500.94 Wh/kg target. Every 4C candidate showed negative anode potential at some point, hence plating=true. The thermal limit passed in rounds 1–2 but failed for high-loading/system escalation.

## Conclusion
Verification does not support release or achievement. Physical abuse, nail penetration, and manufacturing validation were not requested and are not provided.
