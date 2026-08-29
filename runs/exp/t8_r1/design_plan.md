# Design Plan — t8_r1: Long-Endurance Drone Battery

Case: `t8_r1` · Workspace: `runs/exp/t8_r1` · Zero-interaction run (no clarification; entry 0 is the audit contract)

## 1. Objective decomposition (decision-layer thresholds, verbatim from task text)

| Metric | Threshold | Layer | Protocol source |
|---|---|---|---|
| Energy density | ≥ 446.18 Wh/kg | stage2 | `calc-energy` (contract caliber: ∫V·I₁C dt ÷ Σ layer_th×(1−ε)×density×area; electrolyte excluded — same formula for all tasks) |
| 5C capacity retention | ≥ 90% | stage2 | `5C_discharge` capacity ÷ same-params `1C_discharge` capacity (both DFN; mechanically computed by agent, written to disk for `log-evaluate`) |
| Cell mass | ≤ 40 g (= 0.04 kg) | stage2 | `calc-energy` `mass_kg`; satisfied by area scaling at closing (see §3) |
| Max temperature | ≤ 333.15 K (60 °C, protocol default — task silent) | stage3 | `4C_charge_45C` safety exam, lumped thermal, `T_max_K` |
| Lithium plating | none (`plated=false`, protocol default) | stage3 | `4C_charge_45C` + `--plating`; `anode_potential_v` min < 0 → plated |

**Trade-off expectation (multi-objective)**: ED vs 5C-retention is the central Pareto tension — thick high-loading electrodes raise ED but raise areal current density at 5C (diffusion/concentration-polarization limited); thin power electrodes keep 5C but dilute active mass with collectors/separator. ED vs T_max: thicker electrodes → higher I²R and higher thermal mass imbalance. All three are hard constraints — no relaxation without entry-0 amendment (forbidden).

## 2. Candidate strategy

**Start**: `start_stage: 3` (task text involves no new materials — pure performance objective → cell/architecture/formulation space on the existing system). Materials run at system baseline (Chen2020). Base determination: task text names no electrode system → protocol default **Chen2020**; discriminant anchor dumped and verified (NMC811/graphite, no SiOx, SEI rate 1e-12, geometry 0.065×1.58 m, 5 Ah nominal, native mass 43.45 g).

**Rounds** (2–4 candidates per round, each fully simulated + `log-evaluate`-recorded):

1. **R1 — baseline characterization** (Chen2020 default architecture): 1C DFN (+SPMe quick screen), 5C DFN, `calc-energy`, 4C-45°C lumped+plating exam. Purpose: (a) locate baseline vs 446.18 Wh/kg / 90% / plating; (b) **opening ceiling assessment** — theoretical best ED of this system under best-possible architecture+formulation (ultra-thin foils, thin separator, optimal porosity, high-transport electrolyte) vs the objective; objective above ceiling → escalate to Stage 2 material/system design.
2. **R2+ — architecture levers** (propose 2–4/round, `{"struct": {...}}`): current-collector thickness ↓ (Al 16→8 µm, Cu 12→6 µm — industry ultra-thin foil floor; big mass lever, no model penalty since collector ohmic drop isn't in the model and Chen2020 carries explicit `Cell volume [m3]`), particle radius ↓ (cathode 5.22→2 µm, anode 5.86→3 µm — diffusion time constant r²/D is the dominant 5C limiter), separator thickness/porosity, electrode thickness ±, porosity ↑, N/P.
3. **Formulation candidates** (electrolyte freedom, parameter-bridge `{"struct": {...}}` on `Electrolyte conductivity [S.m-1]` / `Cation transference number` / `Electrolyte diffusivity [m2.s-1]`, literature-sourced values, listed before each run): σ ~1.3 S/m (optimized LiPF6 EC/EMC, literature), t⁺ 0.26→0.4 (high-transference electrolyte, literature), D 2.6e-10.
4. **Thermal management** (if T_max binds): `Total heat transfer coefficient [W.m-2.K-1]` 10→25–50 (drone forced airflow, design justification).
5. **Escalation path** (if ceiling < 446.18): Stage 2 system-switch candidates — OKane2022 (NMC811/SiOx with cracking model; same geometry/densities → same contract mass, need to verify capacity/OCP edge) or LNMO overlay (`data/LNMO.json`, 4.7 V-class, midpoint ≈4.17 V) — each really simulated at Stages 3/4 before any claim.

**Fallback routing** (per-round, always on): capacity/retention/ED shortfall with clean material metrics → Stage 3 parameter rework (same scale); potential-window/transport ceiling → escalate to Stage 2 (cross-scale).

## 3. Budget allocation

- R1 baseline: 4 runs (1C SPMe + 1C DFN + 5C DFN + 4C45 DFN+plating) + calc-energy — ≈ 8–12 min.
- R2–R6: ~2–4 candidates/round ≈ 8–15 runs/round; DFN runs dominate (≈1–3 min each). Total planned ≈ 6 rounds ≈ 45–75 min compute; hard stop only at harness budget exhaustion (no round cap per protocol).
- `real_compute: false` → Stage 5 true DFT/MD skipped; `endorse` records the skip honestly.
- Aging protocol not required (no cycle-life metric in task); reserved only if a coating/doping candidate enters.

## 4. Risk and fallback plan

| Risk | Trigger | Response |
|---|---|---|
| Baseline 5C retention ≪ 90% (diffusion-limited, τ≈r²/D ≈ 6800 s at 5.2 µm) | R1 5C DFN | Particle radius ↓ (primary lever, measured per protocol as high-rate enabler), porosity ↑, t⁺/σ ↑, thickness ↓; re-check ED after each |
| ED ceiling below 446.18 | Ceiling assessment | Escalate to Stage 2 (system switch OKane2022 SiOx / LNMO; composition candidates if needed) |
| 4C-charge plating | Safety exam | Anode particle ↓, N/P ↑, t⁺ ↑; plating is a charge-side exam — if only plating fails after 3 strikes, question the boundary honestly (task specifies 5C *discharge*; 4C charge is the protocol-standard exam) and record, never silently drop |
| T_max > 333.15 K at 5C | R1+ T_max_K | Cooling h ↑ (drone airflow), thin electrodes; T_max source marked exact (Chen2020 has native thermal params — no injected defaults) |
| Mass > 40 g | calc-energy | Area scaling f = 0.04/mass (exact; ED/retention/T_max invariant — see entry 0 `mass_scaling`); re-run full protocol on scaled cell at closing |
| Three strikes, same cause | 3 consecutive failed rounds | Stop blind tuning; question system / task-boundary / metric assumptions layer-by-layer in `final.escalation`; close as negative result only if "unreachable within boundary", otherwise change direction |

## 5. References (directional basis; real sources only)

- Default system parameterization: Chen et al., "Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models", J. Electrochem. Soc. 167 080534 (2020) — source of the `Chen2020` PyBaMM set (model anchor for NMC811/graphite + SEI aging). [real; pybamm's documented citation]
- SiOx-containing anode system: O'Kane et al., J. Electrochem. Soc. 169 (2022) — `OKane2022` PyBaMM set (NMC811/SiOx + cracking model), escalation option for anode capacity density. [real; article number not asserted]
- LNMO high-voltage spinel (4.7 V-class, midpoint ≈4.17 V): library `data/LNMO.json` overlay (skill asset) + LNMO spinel cathode literature — escalation option via voltage boost. [library asset + domain experience]
- High-rate particle design: smaller particle radius reduces solid-diffusion time constant r²/D — domain experience (no precise source); protocol measurement note (T1 run: particle size is a high-rate lever).
- Ultra-thin current collectors (6 µm Cu / 8 µm Al): commercially available foils — industry domain experience (no precise source).
- Electrolyte transport overrides (σ≈1.3 S/m optimized LiPF6 EC/EMC; t⁺ 0.4 class high-transference electrolytes): concentration-cell and conductivity literature (Landesfeind et al., J. Electrochem. Soc. 2019 — already the functional form in ORegan2022 set; Nyman 2008 — functional form in Chen2020). [real; used as directional values, marked `literature` at bridge time]
