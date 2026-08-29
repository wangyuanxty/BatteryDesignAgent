# Design Verification Plan & Report (virtual test) — VBF-T6R1-DVPR-01

Candidate: lnmo_r8_d6 (bridge/params_final.json). All results DFN fidelity, tool-output sourced. One row per verification item.

| # | Item | Condition | Result value | Determination | Source |
|---|---|---|---|---|---|
| 1 | 1C discharge capacity | 1C, 25 °C ambient | 6.198 Ah | informational (no capacity criterion in contract) | cell/r8_d6_1c_dfn.json:capacity_ah |
| 2 | Volumetric energy density | 1C discharge energy ÷ cell volume | 1135.8 Wh/L | ✓ ≥ 950 Wh/L (+19.6%) | cell/r8_d6_energy_dfn.json:energy_density_wh_l |
| 3 | Voltage plateau | discharge midpoint | 4.1145 V | ✓ ≥ 4.1 V (+14.5 mV) | cell/r8_d6_energy_dfn.json:midpoint_voltage_v |
| 4 | 4C fast-charge temperature rise | 4C CC charge to 4.7 V at 45 °C ambient (protocol: 1C discharge to 2.5 V + 4C charge), lumped thermal | 321.42 K = 48.27 °C | ✓ ≤ 323.15 K (margin 1.73 K) | cell/r8_d6_4c_dfn.json:T_max_K |
| 5 | 4C fast-charge plating | min anode surface potential over full protocol | +0.01096 V | ✓ plated = false (margin 11.0 mV; min occurs at charge end) | cell/r8_d6_4c_dfn.json:anode_potential_v |
| 6 | SEI thickness after 100 cycles | aging_1C_100cyc, DFN, isothermal | 385.3 nm | ✓ ≤ 500 nm (margin 114.7 nm) | cell/r8_d6_aging_dfn.json:sei_thickness_nm_end |
| 7 | DC resistance | midpoint DCR | 6.38 mΩ | informational | cell/r8_d6_energy_dfn.json:dcr_ohm |

**Items explicitly N/A (beyond pure simulation boundary, require physical experiment):** nail penetration; overcharge to thermal runaway; crush; drop; cycle life to end-of-life (only 100-cycle SEI growth simulated — no capacity-fade EOL model); rate-pulse internal resistance (DCR reported is midpoint-calculated, not pulse).

**Conclusion:** All five contract criteria PASS at DFN fidelity (verified items 2–6). Uncovered conditions listed above are cited here directly as paper limitations. Verification is virtual — no physical cells were built or tested.
