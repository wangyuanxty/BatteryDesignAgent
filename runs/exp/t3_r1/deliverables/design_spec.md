# Cell Design Specification — VBF-T3R1-DS-001

| Field | Value | Source |
|---|---|---|
| Case | exp/t3_r1 — power-tool battery design | log.jsonl entry 0 |
| Document number | VBF-T3R1-DS-001 | delivery index |
| Generation date | 2026-08-25 | — |
| Status | Final (verdict: achieved, log.jsonl final entry) | bda log-evaluate R4 |

## 1. Design requirements (entry-0 criteria, verbatim from task text)

| Metric | Threshold | Layer |
|---|---|---|
| Nominal capacity | >= 2.0 Ah | stage2 |
| 5C discharge retention | >= 0.95 | stage2 |
| Power density | >= 4000.0 W/kg | stage2 |
| Maximum temperature (4C charge @45 C) | <= 333.15 K (60.00 C) | stage3 |
| Lithium plating at 4C charge | False (none) | stage3 |

## 2. System and chemistry

| Item | Value | Source |
|---|---|---|
| Base parameter set | Chen2020 (NMC811 / graphite, 1M LiPF6 EC/EMC) | SKILL.md anchor table; task text names no electrode system -> default with record |
| Cathode | NMC811, 40 um, porosity 0.42, particle radius 2.0 um | cell/p_v12.json |
| Anode | Graphite, 52 um, porosity 0.35, particle radius 2.5 um | cell/p_v12.json |
| Voltage window | 2.5 - 4.2 V | Chen2020 set |
| Electrode area | 0.065 m x 1.58 m = 0.1027 m2 | Chen2020 set / calc-energy |
| Stack thickness | 40+52+12+16+12 = 132 um | layer sum, calc-energy thickness_m |

## 3. Cell architecture (final design V12_BalancedCooling)

| Layer | Thickness [um] | Porosity | Particle radius [um] | Density [kg/m3] | Mass [g] | Source |
|---|---|---|---|---|---|---|
| Positive electrode (NMC811) | 40 | 0.42 | 2.0 | 3699 | 7.77 | Chen2020 set |
| Negative electrode (graphite) | 52 | 0.35 | 2.5 | 2060 | 5.75 | Chen2020 set |
| Separator (polyolefin) | 12 | 0.47 | - | 1548 | 0.26 | Chen2020 set |
| Positive current collector (Al) | 16 | - | - | 2702 | 4.44 | Chen2020 set |
| Negative current collector (Cu) | 12 | - | - | 8933 | 11.04 | Chen2020 set |
| Total (electrolyte excluded by contract) | — | — | — | — | 29.26 | calc-energy |

Layer masses are mechanically computed: mass = layer_kg_m2 x area (calc-energy output r4_v12_energy.json).

## 4. Electrolyte design

| Property | Value | Baseline (Chen2020) | Source |
|---|---|---|---|
| Conductivity kappa | 1.5 S/m | 0.9487 | cell/p_v12.json |
| Diffusivity D | 2.5e-10 m2/s | 1.769e-10 | cell/p_v12.json |
| Cation transference t+ | 0.35 | 0.2594 | cell/p_v12.json |

Rationale (round-2/3 attribution, log.jsonl): high-transport electrolyte is load-bearing for both 5C retention
and plating margin — V9 (kappa 1.2 / D 2.0e-10 / t+ 0.30) passed retention but eroded the plating margin to
+0.6 mV (cell/r3_v9_4c.json), so the aggressive values are retained. Values are transport-parameter
overrides of the baseline formulation (electrolyte formulation degree of freedom, widest interpretation
recorded in entry-0 meta.freedoms).

## 5. Thermal design

| Property | Value | Source |
|---|---|---|
| Cooling coefficient h | 20 W/m2/K | cell/p_v12.json |
| Ambient for rating | 25 C (discharge), 45 C (4C charge protocol) | bda protocols |

Rationale (round-3/4 attribution): h trades thermal margin against plating margin (warmer cell kinetically
suppresses plating): h=15 -> T_max 331.96 K / anode +14.9 mV (V8); h=30 -> T_max 326.86 K / anode +8.2 mV
(V11). h=20 lands both margins balanced (measured: T_max 329.77 K, anode min 12.1 mV)
and is realistic for a power tool (natural convection + tool-body conduction with light airflow).

## 6. Electrical ratings

| Rating | Value | Source |
|---|---|---|
| Nominal capacity Q_nom | 3.08 Ah | cell/p_v12.json (fixed-point iteration: measured 1C = 3.075 Ah, round 2 lesson) |
| 1C current | 3.08 A | Q_nom x 1 |
| 5C discharge current | 15.4 A | Q_nom x 5 |
| 4C charge current | 12.32 A | Q_nom x 4 |
| Midpoint voltage | 3.844 V | calc-energy midpoint_voltage_v |

## 7. Verification summary

See DVPR (VBF-T3R1-DVPR-001): all five criteria verified pass by DFN simulation, evidence
cell/r4_v12_*.json via bda log-evaluate (round 4, 5/5 checked, verdict pass). Iteration history in
log.jsonl (rounds 1-4) and report.html.

## 8. Design notes (honest limits)

- Electrolyte mass excluded from calc-energy by contract (parameter set lacks density; output
  electrolyte_included: false) — mass/power density slightly optimistic vs a real cell with electrolyte.
- True DFT/MD endorsement skipped (real_compute=false, entry-0 meta): no first-principles values claimed.
- 4C CC-only charge accepts ~0.81 Ah before the 4.2 V ceiling (cell/r4_v12_4c.json) — a CV taper phase is
  required for full charge; plating-free result is for the CC segment per protocol definition.
- Manufacturability drawings with tolerances, material datasheets, and process cards are outside the
  pure-simulation boundary and are not provided.
