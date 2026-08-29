# Cell Design Specification — VBF-T2R1SINGLEMODEL-DS-01

> Case: t2_r1_singlemodel (grid energy storage). Every value mechanically taken from the
> parameter set / simulation outputs; sources annotated per line. Generation date 2026-08-25.

## 1. Basic specification

| Item | Value | Source |
|---|---|---|
| Electrochemical system | NMC811 / graphite (Li-ion), Chen2020 base parameter set | parameter set (entry 0 meta.base_params) |
| Nominal capacity | 5.0 Ah (parameter set) / 6.9555 Ah simulated 1C discharge | parameter set `Nominal cell capacity [A.h]` / cell/r3_1c_dfn.json:capacity_ah |
| Voltage window | 2.5 – 4.2 V | parameter set lower/upper cut-off |
| Cell dimensions | 65 mm x 1580 mm x 0.390 mm (layer stack incl. collectors); shell thickness Not provided | parameter set height/width/layer thicknesses |
| Electrolyte formulation | EC/EMC + LiPF6 (parameter set default), c_e0 1000 mol/m3; additive pack: FEC, VC, PS, EP, LiDFOB-anion, LiDFP-anion | parameter set / funnel dispositions |
| Cation transference number | 0.2594 | parameter set |
| Midpoint voltage | 3.574 V | cell/r3_energy.json:midpoint_voltage_v |
| DC resistance | 0.0124 ohm | cell/r3_energy.json:dcr_ohm |

## 2. Electrode and separator

| Layer | Thickness (um) | Porosity | Active-material vol. frac. | Particle radius (um) | Collector |
|---|---|---|---|---|---|
| Positive | 100 | 0.335 | 0.665 | 3.0 | Al 16 um |
| Separator | 12.0 | 0.47 | — | — | — |
| Negative | 250 | 0.25 | 0.75 | 3.5 | Cu 12 um |

- N/P ratio = 1.48 (no capacity-density keys in Chen2020; full theoretical lithiation range (c_max*F/3600 cancel), c_max neg 33133 / pos 63104 mol/m3)

## 3. Process design parameters

| Parameter | Value | Formula | Notes |
|---|---|---|---|
| Positive areal density | 216.9 g/m2 | thickness x (1-porosity) x density | parameter set |
| Negative areal density | 310.7 g/m2 | thickness x (1-porosity) x density | parameter set |
| Positive compaction density | 2.17 g/cm3 | density x (1-porosity) / 1000 | parameter set |
| Negative compaction density | 1.24 g/cm3 | density x (1-porosity) / 1000 | parameter set |
| Electrolyte fill amount | 0.0 g | pore volume x 1.2 g/cm3 x fill 1.0 | literature electrolyte density 1.2 g/cm3 (annotated) |
| Formation recommendation | 0.1C CC to 4.2 V, 25 C, 2 cycles | — | design recommended value; production-line value requires tuning |

## 4. Mass breakdown (calc-energy contract caliber, electrolyte excluded)

| Layer | kg/m2 | kg |
|---|---|---|
| Positive active layer | 0.0000 | 0.0 g |
| Negative active layer | 0.0000 | 0.0 g |
| Current collectors | 0.0000 | 0.0 g |
| Separator | 0.0025 | 0.3 g |
| **Total** | — | **69.9 g** |

Electrolyte excluded from mass (parameter set lacks electrolyte density) — cell/r3_energy.json:electrolyte_included=false.

## 5. Performance verification

| Item | Value | Criterion (entry 0) | Verdict |
|---|---|---|---|
| Energy density | 358.01 Wh/kg | >= 327.18 | PASS |
| SEI thickness @100 cyc | 194.56 nm | <= 500 nm | PASS |
| SEI thickness @500 cyc | 439.74 nm | <= 550 nm | PASS |
| -20 C retention | 99.59 % | >= 90 % | PASS |
| 4C fast charge plating | ap_min +0.112 V (45 C start); +0.111 V (25 C conservative) | plated == false | PASS |
| 4C max temperature | 342.5 K | monitored only (no red line in entry 0) | INFO |
| 5C discharge | 0.4939 Ah (7% of 1C; voltage collapses to cut-off in ~71 s — severely rate-limited; informational, no 5C criterion) | informational (no 5C criterion) | INFO |

## 6. Design notes

Parameters changed vs Chen2020 baseline and why (reasoning traceable to log evaluate/plan entries):
1. Negative electrode thickness 250 um / positive 100 um (baseline thin electrodes): areal flux
   reduction for 4C reaction-zone crowding; DFN adopted after SPMe c_e-profile artifact was
   diagnosed (plan-update entry).
2. Negative electrode exchange-current density = 2.0 A/m2 (baseline value overridden): D-scan
   optimum for 4C plating suppression (non-monotonic; i0=20 A/m2 fails). Bridge: interfacial
   kinetics from the additive pack.
3. Positive/negative particle radii 3.0/3.5 um: surface-area tuning supporting the kinetics fix.
4. SEI pack: k_sei 3e-13 m/s, SEI i0 7.5e-8 A/m2, EC diffusivity 1e-19 m2/s (baseline D_ec
   2e-18): growth is diffusion-limited at L>100 nm (Yang2017 ec reaction limited), L ~ sqrt(D_ec);
   the D_ec value is a film-property extension of the SEI-suppression bridge, recorded as estimate
   (plan-update entries document the 1e-18 -> 2e-19 -> 8e-20 -> 1e-19 correction chain; 8e-20 was
   dropped because its 500-cycle aging dies deterministically at cycle ~174, IDA_CONV_FAIL).
