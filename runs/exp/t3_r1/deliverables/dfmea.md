# Design FMEA (qualitative) — VBF-T3R1-DFMEA-001

Qualitative design FMEA on the final design V12_BalancedCooling. Ratings: S=severity, O=occurrence,
D=detection (1-10, 10 worst). Mitigations reference round measurements (log.jsonl).

| Failure mode | Effect | S | O | D | Design controls / mitigation | Residual risk |
|---|---|---|---|---|---|---|
| Lithium plating during 4C charge | Capacity loss, internal short risk | 9 | 2 | 3 | Thin electrodes (40/52 um), porosity 0.42/0.35, high-transport electrolyte, measured anode min +12.1 mV; V10 showed porosity rollback alone plates (-4.3 mV) | Electrolyte transport aging erodes margin (V9: +0.6 mV at kappa 1.2) -> recommend periodic anode-potential-aware charge control |
| Cell over-temperature at fast charge | Electrolyte degradation, venting | 7 | 3 | 2 | h=20 W/m2/K specified; measured 56.6 C at 4C/45 C (3.38 K margin); lumped-thermal DFN verification | Margin consumed if cooling degrades (dust, insulation) -> pack-level thermal monitor recommended |
| 5C-rate capacity fade / power loss | Tool stalls under load | 6 | 5 | 4 | Measured retention 97.5% at BOL; DCR 4.4 mOhm | Cycle-life rate fade not tested (aging protocol available for follow-up) |
| Thickness/porosity manufacturing deviation | Plating margin or retention loss | 5 | 4 | 3 | Single-lever attribution (R2): V1-V5 quantify each lever's effect; tolerance stackup can be re-simulated with the same pipeline | No tolerance band specified (drawings outside simulation boundary) |
| Charge CV-phase heating beyond CC segment | T exceeds 60 C in taper | 5 | 3 | 2 | CC-only 4C measured; CV phase not simulated (protocol limitation) | Recommend CV-phase thermal verification in follow-up |
| Electrolyte density unmodeled mass | Power density over-estimate | 3 | 8 | 1 | Contract excludes electrolyte mass (electrolyte_included: false) — disclosed on datasheet | Est. few-% overstatement; real-cell verification required |

FMEA scope note: pure-simulation boundary — no abuse (nail/overcharge) tests performed (not in task criteria).
