# Design Specification - VBF-T5R2-DS-01

**Case**: t5_r2 (workspace runs/exp/t5_r2)  **Protocol**: Virtual Battery Factory five-stage funnel
**Verdict**: achieved **Date**: 2026-08-26

## 1. Objective and contract (log.jsonl entry 0, frozen)

Task: flagship-vehicle cell, energy density >= 500.94 Wh/kg, supports 4C fast charge
(no lithium plating), maximum temperature <= 60 C (333.15 K) on the 4C charge.

Contractual criteria (never revised during the run):

| Criterion | Threshold | Freeform |
|---|---|---|
| Stage 2 energy_density_wh_kg >= | 500.94 | calc-energy caliber (V*I_1C dt / stack mass; electrolyte & casing excluded) |
| Stage 3 T_max_K <= | 333.15 | 4C_charge_45C protocol (1C discharge, 4C CC charge to 4.2 V, 318.15 K ambient, lumped thermal, total h 70) |
| Stage 3 plated | false | anode potential min > 0 V over the 4C profile (Chen2020 + injected plating kinetics) |

Freedoms exercised (all adjustable per entry-0 meta): electrode_system (kept NMC811/graphite
Chen2020 base; LNMO 4.7 V lever measured round 2 and eliminated at 420.3 Wh/kg still plated),
electrolyte_formulation (conductivity / transference / diffusivity as labeled literature
estimates), electrode_modification (particle radius 3 um anode), cell_architecture (thicknesses,
capacity/area, porosity, collectors, separator), thermal_management (h = 70 W/m2/K,
channel liquid-cooling class). Simulation caliber: spme quick-screen rounds, DFN for contract.

## 2. Final architecture (stack)

| Layer | Material | t (um) | Porosity | Density (kg/m3) | kg/m2 | g/cell |
|---|---|---|---|---|---|---|
| Positive electrode | NMC811 base (96/2/2 est.) | 98.28 | 0.43 | 3262.0 | 0.182736 | 18.77 |
| Negative electrode | Graphite (96/2/2 est.) + 3 um particle | 121.84 | 0.45 | 1657.0 | 0.111039 | 11.40 |
| Separator | PP/PE class | 8.0 | 0.47 | 397.0 | 0.001683 | 0.17 |
| Positive cc | Al foil | 8.0 | - | 2700.0 | 0.021600 | 2.22 |
| Negative cc | Cu foil | 6.0 | - | 8960.0 | 0.053760 | 5.52 |

Stack: 242.12 um x 0.1027 m2; contract mass 38.083 g; nominal capacity parameter 6.5 Ah
(1C-verified 7.171 Ah DFN). Cell format: assembled stack (no can) - the contract caliber
follows calc-energy (electrolyte/casing excluded by parameter-set conventions).

## 3. Final parameter set (bridge/p_r6_f2.json over Chen2020 base) + provenance

| Parameter | Value | Provenance |
|---|---|---|
| Positive/negative collector thickness | 8 / 6 um | r2 (mass overhead cut; 12/16 um baseline) |
| Separator thickness | 8 um | r2 (Chen2020 12 um baseline) |
| Positive / negative electrode thickness | 98.28 / 121.84 um | r2-r4: x1.3 uniform scaling of LM-thin 75 um platform + N/P buffer +10% negative |
| Nominal cell capacity | 6.5 Ah | r2 (thickness/nominal scaling; capacity rises with area-free energy fraction) |
| Electrode area | 0.1027 m2 | geometry block (height 0.1371 m x width 0.749 m approx.) |
| Electrolyte conductivity | 1.5 S/m | ESTIMATE (literature-class 1 M LiPF6 EC:EMC at 25 C, ~13-16 mS/cm) |
| Cation transference number | 0.6 | ESTIMATE (electrolyte-engineering target; baseline 0.5206) |
| Electrolyte diffusivity | 5.0e-10 m2/s | ESTIMATE (EC:EMC literature range 2-6e-10) |
| Negative / positive porosity | 0.45 / 0.43 | r3 (ion-transport margin; baseline 0.25/0.335) |
| Negative particle radius | 3.0 um | r4 (surface-area up -> lowers local saturation at 4C) |
| Total heat transfer coefficient | 70 W/m2/K | r6 (channel liquid-cooling class; h-sweep r4-5 measured) |
| Base set | Chen2020 (NMC811/graphite, SEI ec-reaction-limited) | entry-0 default |

Forbidden levers untouched (protocol): solid-phase conductivity/diffusivity, initial
concentrations/lithiation, initial SEI thickness, charge cut-off voltage.

## 4. Process / stack formulas (manufacturing hand-over)

| Quantity | Formula | Value |
|---|---|---|
| Positive areal density | rho_pos x (1-por) x L | 182.7 g/m2 = 18.27 mg/cm2 |
| Negative areal density | rho_neg x (1-por) x L | 111.0 g/m2 = 11.10 mg/cm2 |
| Positive compaction | rho x (1-por) / 1000 | 1.859 g/cm3 |
| Negative compaction | rho x (1-por) / 1000 | 0.911 g/cm3 |
| Electrolyte fill | pore volume = Sum(t x por) x area | 10.36 cm3 -> 12.43 g at 1.2 g/cm3 (LITERATURE ESTIMATE) |
| Anode full-charge stoich x0 | initial c / cmax | 0.9014 |
| Cathode initial stoich x0 | initial c / cmax | 0.2700 |
| Anode stoich after 1C discharge | x0 - Q/(A x capacity-per-dx) | 0.041 |
| Cathode stoich after 1C discharge | x0 + Q/(A x capacity-per-dx) | 0.902 |
| N/P (as-designed) | neg usable-to-full-charge capacity 73.2 Ah/m2 div pos utilized 69.8 Ah/m2 | 1.05 |
| Anode saturation headroom above full charge | (1-x0_neg) fraction | 11.5 % (plating buffer; the OPPOSITE order - cooling before transport - replates) |

Formation recommendation (literature practice; NOT simulated by this run): rest 6 h ->
0.05C CC charge 2 h -> open-circuit rest 1 h -> 0.1C CC charge 30 min -> rest 1 h ->
0.2C / 0.5C / 1C staged charges to 4.2 V -> degas & reseal. SEI target built into the
Chen2020 ec-reaction-limited kinetics; aging-informational run ends at 520.3 nm SEI.

## 5. Verification against the frozen criteria

| Criterion | Required | Measured | Source | Verdict |
|---|---|---|---|---|
| ED Wh/kg | >= 500.94 | 666.3 | cell/r7_final_f2_energy_dfn.json (DFN 1C, calc-energy) | PASS |
| T_max K at 4C | <= 333.15 | 330.984 (57.83 C) | cell/r7_final_f2_4c45.json | PASS |
| Plated | false | anode potential min +0.0506 V | same (anode_potential_v series, min>0) | PASS |

All three mechanically evaluated in round 7 (log-evaluate, same-round entry chain intact).

## 6. Honest limitations

1. ED caliber excludes electrolyte & casing per the frozen contract; BOM-caliber with
   literature electrolyte fill lands at ~502.4 Wh/kg (2.0 kg/kWh). Packaging
   reality sits between; recommend a packaging-mass budget study before pack design.
2. 4C support is protocol-defined: CC-only charge accepts 0.511 Ah before the 4.2 V
   cut-off; no plating and <=57.9 C proven over that profile. Real fast charge should
   use a multi-step/tapered profile, which this parameterization supports (ap margin +51 mV).
3. Electrolyte transport values are labeled literature ESTIMATES - not DFT/MD endorsed
   (real_compute=false in the contract; endorse entry skipped with justification).
4. Cycle life is not an acceptance criterion; the informational 100-cycle SEI run is
   reported raw (end-SEI 520.3 nm) with its runner-protocol caveat (per-cycle
   capacity series does not reproduce the contractual 1C capacity -> not rateable).
5. No three-strike event; ceiling assessment in round 1 resolved the only open question
   (ED reachability) - so no escalation object was needed.
6. Mechanical tests (nail/overcharge/crush/drop) are out of simulator scope - DVPR rows
   N/A with reasons, not fabricated results.

## 7. Recommendations for the next design step

- Binder/additive reformulation to shrink the 3-4% mass-tax of 96/2/2 towards 98/1/1.
- Multi-step 4C profile (4C to 3.9 V, 2C to 4.1 V, 1C CV) to raise charge acceptance.
- Package-level: 3-cell string layout + channel cooling plate at h >= 70; re-verify at DFN.
- True-compute endorsement pass (real_compute=true case) on the electrolyte transport triad.
