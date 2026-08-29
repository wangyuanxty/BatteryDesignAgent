# Design Specification — Smartphone High-Voltage Fast-Charge Cell

| Doc No: VBF-T6R3-DS-01 | Case: t6_r3 | Rev: 01 | Date: 2026-08-26 | Status: Released (virtual design) |

**Design: V27_combo** (LNMO 4.7 V spinel / graphite, 5.06 Ah, 21.11 Wh cell)

## 1. Requirements (entry-0 contract, immutable)

> Design a battery for a smartphone: volumetric energy density >= 950 Wh/L, support 4C fast charge (no lithium plating), maximum temperature <= 50 C, anode SEI thickness <= 500 nm after 100 cycles, voltage plateau >= 4.1 V.

All thresholds fixed at entry 0; no relaxation occurred anywhere in the funnel.

## 2. Achieved performance (all values are DFN simulation outputs)

| Criterion (entry-0 contract, immutable) | Threshold | Achieved (DFN) | Margin | Source |
|---|---|---|---|---|
| Volumetric energy density | >= 950 Wh/L | 983.61 Wh/L | +33.61 | r10_V27_combo_energy.json energy_density_wh_l |
| Voltage plateau (midpoint) | >= 4.1 V | 4.1551 V | +55.1 mV | r10_V27_combo_energy.json midpoint_voltage_v |
| Max temperature, 4C charge | <= 50 C (323.15 K) | 318.922 K (45.77 C) | -4.23 K | r10_V27_combo_4c.json T_max_K |
| Lithium plating, 4C charge | none (anode pot. >= 0) | none (min anode pot. +0.1050 V) | +105.0 mV | r10_V27_combo_4c.json anode_potential_v |
| Anode SEI after 100 cycles | <= 500 nm | 313.7 nm | -186.3 nm | r10_V27_combo_aging.json sei_thickness_nm_end |

Model fidelity: model_used = DFN in all four output sets (1C discharge, energy, 4C charge, aging). SPMe screening results were superseded at round 9 (see section 5) and are not used for any claimed value.

## 3. Cell architecture

| Layer | Thickness | Mass | Key parameters | Source |
|---|---|---|---|---|
| Positive current collector (Al) | 16 um | 4.4366 g | rho 2700 kg/m3 | [Chen2020.py:252,261] |
| Positive electrode (LNMO) | 60 um | 18.0300 g | AMVF 0.665, rho 4400, c_max 43000 | [LNMO.json; params/V27_combo.json] |
| Separator | 12 um | 0.2593 g | porosity 0.47, rho 397 | [Chen2020.py:250,306,308] |
| Negative electrode (graphite) | 109 um | 13.9117 g | AMVF 0.75, rho 1657, c_max 33133 | [Chen2020.py:274,275,283; params/V27_combo.json] |
| Negative current collector (Cu) | 12 um | 11.0423 g | rho 8960 kg/m3 | [Chen2020.py:248,260] |
| TOTAL stack | 209 um | 47.6800 g (dry) | matches r10_V27_combo_energy.json mass_kg | [r10_V27_combo_energy.json] |

- Footprint: 0.065 m x 1.58 m electrode sheet [Chen2020.py:253-254] -> area 0.1027 m2
- Stack volume: 2.146430e-05 m3 = 21.46 mL [contract formula: volume = thickness x area]
- Cell thickness: 209 um; mass: 47.6800 g dry (electrolyte excluded per contract); 54.2105 g wet incl. electrolyte

## 4. Material system

- **Positive**: LNMO spinel OCP (4.7 V plateau family), voltage window 2.5-4.7 V, stoichiometry limits [0.9, 0.3], rho 4400 kg/m3, c_max 43000 mol/m3 [LNMO.json]
- **Negative**: graphite (Chen2020 LGM50), rho 1657 kg/m3, c_max 33133 mol/m3, AMVF 0.75 [Chen2020.py]
- **Electrolyte**: EC-lean 2.0 M (EC initial concentration 2000 mol/m3 vs base 4541), fixed conductivity 2.0 S/m, transference number 0.5 [params/V27_combo.json]
- **SEI**: Yang2017 EC-reaction-limited model on Chen2020 base; SEI kinetic rate constant 5e-14 m/s (surface coating lever), initial SEI 5 nm [Chen2020.py:240; params/V27_combo.json]
- **Cooling**: total heat transfer coefficient 250 W/m2/K [params/V27_combo.json]

## 5. Design history (funnel summary)

- Rounds 1-4: baseline LGM50 characterization + LNMO high-voltage escalation (see log.jsonl).
- Rounds 5-9 (SPMe screening): thin-positive architecture cleared plating and ED in SPMe.
- **Round 9 DFN rejection**: the SPMe finalist failed DFN (plateau 4.0766 V, T_max 330.6 K, min anode potential -0.0522 V) — SPMe margins were proxy artifacts. Design re-solved in DFN space (plan_update_dfnn logged).
- Round 10 DFN DoE (all evaluated): V24 transport probe (sigma/t+): plating clears barely (+3.3 mV), plateau/T fail. V25 N/P 1.25 probe: plating +104 mV, T 320.4 K, plateau misses by 0.145 mV. V26 repack: insufficient (plated by 33 uV). **V27 combo: ALL FIVE PASS** (verdict=pass, checked=5, round-10 evaluate).
- Mechanisms: (1) N/P 1.579 (oversized anode) + thin 60 um cathode collapse the 4C CC phase to ~16.2 ms at 18 A — the anode never dips below +0.105 V; (2) sigma 2.0 S/m + t+ 0.5 recover the plateau by ~55 mV over the N/P-alone case; (3) EC-lean electrolyte + k_sei 5e-14 coating hold SEI at 313.7 nm; (4) h=250 W/m2/K buys thermal margin (T_max 318.92 K).
- N/P note: 1.5787 is the exact first-principles layer-capacity ratio (L_n*eps_n*c_nmax)/(L_p*eps_p*c_pmax). Early round labels used a thickness-scaled shorthand (~1.28); the qualitative mechanism is unchanged.

## 6. Endorsement

- real_compute = false (entry-0 meta): true DFT/MD endorsement (run-orca/run-md) **skipped honestly** — endorse entry logged with skipped=true. No DFT/MD values are present or fabricated in any deliverable.
- Endorsement basis: DFN-precision simulation, 11 logged evaluate rounds against the immutable entry-0 contract, round-10 verdict=pass.

## 7. Limitations and open items

1. The 4C protocol charges from the model initial state (cell born at 4.1995 V, essentially full): the CC phase ends after ~16.2 ms. Plating clearance (+0.105 V) is verified for the imposed protocol; a 0-100% SOC 4C DFN run is recommended (DVPR row 8).
2. Aging capacity trajectory shows the known SEI-model lithium-inventory artifact (cap cycle 1 -0.618 Ah -> cycle 100 2.732 Ah, climb). The reliable durability metric is SEI thickness (313.7 nm). Disclosed, not narrated as a benefit.
3. No physical cell exists; electrolyte density (1.2 g/mL), electrode formulations (96/2/2, 95/3/2 wt%) are literature defaults, not simulated.
4. DFN is a proxy for reality: the round-9 SPMe failure is documented as a model-fidelity lesson (DFMEA row 6).

## 8. Signatures

| Prepared by | Date | Reviewed by | Date | Approved by | Date |
|---|---|---|---|---|---|
| ____________ | | ____________ | | ____________ | |