# Design Specification — Smartphone Lithium-Ion Battery (LNMO 4.7 V-class)

**Document**: VBF-T6R1F-DS-01 | **Case**: t6_r1_flash | **Date**: 2026-08-25 | **Status**: Final (DFN-verified)

## 1. Objective

Design a smartphone battery meeting (adjudicable contract, log.jsonl entry 0):

| Metric | Requirement |
|---|---|
| M1 Volumetric energy density | ≥ 950 Wh/L |
| M2 Voltage plateau (midpoint) | ≥ 4.1 V |
| M3 Anode SEI thickness after 100 cycles | ≤ 500 nm |
| M4 4C fast charge without lithium plating | plated = false (anode potential ≥ 0 V) |
| M5 Maximum temperature at 4C charge | ≤ 50 °C (323.15 K) |

Base system: LNMO high-voltage spinel cathode (4.7 V-class) / graphite (library parameter set `LNMO.json`, Chen2020 + LNMO OCP overlay). All five degree-of-freedom categories adjustable (electrode system fixed to LNMO by task; electrolyte, architecture, particle size, thermal management free).

## 2. Final Design Parameters (finN-2e19)

| Parameter | Value |
|---|---|
| Positive electrode: LNMO spinel, thickness 74 µm, active volume fraction 0.665 | particle radius 2.0 µm |
| Negative electrode: graphite, thickness **120 µm**, active volume fraction **0.65** | particle radius 3.0 µm |
| Separator thickness | 8 µm |
| Current collectors | Al 8 µm / Cu 6 µm |
| Electrolyte | high-transference high-conductivity additive electrolyte: σ = 20 S/m, t⁺ = 0.9, D = 1e-9 m²/s |
| SEI EC diffusivity (LiF-rich SEI design) | 2e-19 m²/s |
| Thermal management (effective h) | **300 W/m²K** (vapor chamber + graphite + Al frame; h=250 verified minimum) |
| Cell footprint | height 0.065 m × width 1.58 m (area 0.1027 m², runner convention) |
| Nominal capacity (1C) | 6.32 Ah (DFN) |

## 3. Verified Performance (DFN precision unless noted)

| Metric | Value | Threshold | Verdict | Evidence |
|---|---|---|---|---|
| M1 ED volumetric | 1171.7 Wh/L | ≥ 950 | **PASS** | cell/r5_finN_dfn_1c_calc.json |
| M2 Midpoint voltage | 4.145 V | ≥ 4.1 | **PASS** | cell/r5_finN_dfn_1c_calc.json |
| M3 SEI @100 cycles | 292.2 nm | ≤ 500 | **PASS** | cell/r5_finN2e19_aging.json |
| M4 4C charge plating | plated (anode min −0.019 V) | false | **FAIL (documented boundary)** | cell/r5_finN_dfn_h300_4c.json |
| M5 T_max @4C, 45 °C amb | 322.5 K (49.4 °C) | ≤ 323.15 | **PASS** | cell/r5_finN_dfn_h300_4c.json |

Supporting: capacity 6.32 Ah, energy 26.2 Wh, mass 45.9 g (electrolyte excluded), ED gravimetric 569.9 Wh/kg, DCR 4.8 mΩ, 4C charge acceptance 6.68 Ah (DFN) / 6.97 Ah (SPM), charge duration ~22.3 min (1336 s).

## 4. M4 Statement (protocol-level feasibility boundary)

M4 is **structurally unpassable** for the LNMO system at the 4.7 V charge cutoff with a real charge. Mechanism (Rounds 3–5, 15+ configurations, three-strike questioning):

1. The charge is anode-capacity-limited: the graphite surface saturates (stoichiometry → 1.0) near 7 Ah, before the cathode window is exhausted; at that instant `anode_potential = U_pos(surf) + η_pos − 4.7 − φ_e(sep) ≈ −0.2 V`.
2. Enlarging the anode shifts termination to the protocol cutoff (4.7 V) — but then `U_pos(sto→0) = 4.706 V ≈ 4.7 V` (LNMO OCP ceiling equals the cutoff), so `anode_potential ≈ +0.02 − φ_e(sep) < 0` because the measured electrolyte potential at the separator `φ_e(sep) ≈ +0.2 V` is ~11× the ohmic estimate; lifting it would require σ ≳ 100 S/m (physically impossible).
3. All anode-side levers cancel by construction (`U_neg`, `η_neg`, anode stoichiometry do not enter the anode potential at the cutoff); cathode kinetics levers are mass-transfer-limited; the only mechanically-"passing" configurations deliver 0–0.003 Ah charge legs (0.1–0.6 s) — vacuous passes rejected as protocol-gaming.

The final design therefore delivers a **real 4C charge (6.68–6.97 Ah)** and records M4 as a documented, mechanism-level failure; every other criterion is passed with margin. This is the honest, reproducible conclusion of the case.

## 5. Design Rationale (funnel trace)

| Round | Direction | Outcome |
|---|---|---|
| R1 | Baseline + ceiling characterization (Chen2020 vs LNMO) | ED 1005 Wh/L, SEI 753 nm, T_max 364 K — M1 marginal, M3/M4/M5 fail |
| R2 | Architecture: thin separator/CC, N/P down | ED 1110 Wh/L — M1 secured; M3/M4/M5 open |
| R3 | Electrolyte transport (σ/t⁺/D) + thermal h | t⁺ 0.7+σ 2: charge 5.3 Ah real, plating persists (anode saturation mechanism identified); h 60: T 329 K fail |
| R4 | SEI D_ec lever (diffusion-limited growth) | 753→505 nm at 8e-19 — M3 within reach; t⁺ 0.9/σ 5/D 1e-9 + h120 → T 322 K pass; plating mechanism fully diagnosed (three-strike #1-2) |
| R5 | N/P boundary sweep → dense short anode + extreme transport (finN) + D_ec 2e-19 | M1 1172, M2 4.25, M3 292 nm, M5 321.9 K, real 7 Ah 4C charge — M4 still plated (three-strike #3 → questioning conclusion, plan update) |
| DFN | Precision verification (task 5) | M1/M2 confirmed; M5 forces h 120→300 (lumped SPM under-predicted peak by 4.3 K); M4 confirmed plated (−0.019 V) |

## 6. References

- LNMO 4.7 V-class cathode parameter set: VBF simulation library `scripts/bda/simulators/data/LNMO.json` (anchor: OCP(0.5)≈4.7 V).
- Chen2020 base parameterization: Chen et al., *J. Electrochem. Soc.* 167 (2020) 080534 — "Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models".
- SEI growth (EC reaction-limited, diffusion-limited regime): Yang, Xu, Hua et al., *J. Electrochem. Soc.* 164 (2017) A3139 — "Modeling of Lithium Plating Induced Aging of Lithium-Ion Batteries".
- Plating vs. charging trade-off review: O'Kane, Campbell et al., *Phys. Chem. Chem. Phys.* 24 (2022) — "Lithium-ion battery degradation: what you need to know".
- High transference number electrolyte direction: Diederichsen, McShane, McCloskey, *ACS Energy Lett.* 2 (2017) 2563 — "Promising Routes to a High Li⁺ Transference Number Electrolyte".
- Smartphone vapor-chamber cooling effective h ≈ 250–350 W/m²K: domain experience (no precise source).
- σ = 20 S/m liquid electrolyte: aggressive additive/solvent formulation estimate (domain experience, no precise source); flagged in log entry `props_source`.
