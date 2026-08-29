# Design FMEA — VBF-T6_R1_LUNA-DFMEA-001

| Failure mode | Effect | Evidence/risk | Mitigation |
|---|---|---|---|
| Lithium plating during 4C charge | Safety and capacity loss | V3 minimum anode potential −0.5405 V; plated=true | High-voltage/material redesign, electrolyte transport validation, lower charge rate if requirement changes (not relaxed here) |
| Excess heat | Thermal stress | Baseline 332.3520 K; V3 321.6326 K | Cooling and small particles improved temperature; validate hardware thermal path |
| Insufficient volumetric energy | Smartphone runtime shortfall | V3 895.5999 Wh/L vs 950 Wh/L | Switch to high-voltage system and optimize loading |
| SEI growth | Resistance/capacity fade | V3 373.7648 nm, passes limit | Continue SEI mitigation and validate long-cycle behavior |
| Voltage plateau below contract | Insufficient usable voltage | Baseline midpoint 3.9352 V vs 4.1 V | High-voltage cathode/system design |

Qualitative virtual FMEA only; severity/occurrence/detection ratings and manufacturing controls were not provided by the simulation boundary.
