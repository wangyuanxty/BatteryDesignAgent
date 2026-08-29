# Design FMEA (qualitative, simulation-signal based) — VBF-T1LC-DFMEA-01

Qualitative version, based on simulation signals. Severity (S) / Occurrence (O) rated High/Medium/Low by magnitude of simulated value vs threshold. Complete process/supplier FMEA is N/A (beyond pure simulation boundary).

| Failure mode | Failure cause | Simulation signal (detectability basis) | S | O | Design-side mitigation |
|---|---|---|---|---|---|
| Negative electrode lithium plating (fast charge) | anode surface Li saturation / transport polarization at 4C | anode_potential_v min (final +0.0368 V vs baseline −0.19 V) | High | Low | high-transport electrolyte (σ 2.5 S/m, t⁺ 0.6), negative particle 3.0 µm |
| Thermal runaway from temperature rise | insufficient heat rejection at 4C | T_max_K 328.56 K vs 333.15 K limit (baseline 354.3 K) | High | Low | liquid cooling h=60 W/m²/K, lower ohmic heat via transport |
| Overcharge (4.7 V) thermal runaway | cathode oxygen release / side reactions above 4.2 V | run-tr triggered = false | High | Low | verified no TR at 4.7 V; keep 4.2 V operating cut-off |
| Electrolyte oxidative decomposition (voltage window) | electrolyte HOMO above cathode potential at high voltage | N/A (no DFT, real_compute=false) | Medium | Medium | HOMO/IE-EA not endorsed; note as open item for true-DFT |
| Insufficient capacity | low active utilization / low first-cycle lithiation | 1C capacity_ah 5.03 Ah | Medium | Low | verified above 5 Ah nominal |

## Conclusion

- Highest-risk items: plating and thermal runaway — both mitigated in the final design and verified passing.
- Open item: electrolyte oxidative-stability window not first-principles-endorsed (real_compute=false); flagged for follow-up true-DFT.
- Complete FMEA (process/supplier failures, manufacturing variability) is N/A (beyond pure simulation boundary).
