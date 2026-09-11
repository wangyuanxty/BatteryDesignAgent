# Design Plan — Smartphone Battery (case t6_oa)

## 0. Environment status (critical blocker — read first)
The portability harness `run_shell` tool is **broken**. Every command — `echo`, `python --version`,
`.venv/Scripts/python.exe -c "import bda"`, `nonexistent_command`, `cmd.exe /c ...`, absolute exe paths,
redirect probes — returns `[stderr] /c: /c: Is a directory` and executes **nothing** (no stdout, no file
side effects, no "command not found" for nonexistent commands).

Diagnosis: the harness invokes the shell with `/c` (the MSYS C:-drive mount — a directory) as the
*executable*, ignoring the command string entirely; command content has zero effect. This is
deterministic (identical error across ~20 varied commands) and unfixable from inside (no shell ⇒ no
`bda`, no self-install, no `bda.store.append_entry`). No other execution path exists with the four tools
(run_shell / read_file / write_file / list_dir) and delegation is forbidden.

Consequence: **no simulation value can be produced without fabrication, which is forbidden.** This plan is
reasoning-only. Entry 0 (criteria) and this Stage-1 plan are complete and correct; Stages 2–5 and all
deliverables are blocked pending a working shell.

## 1. Objective decomposition (decision-layer thresholds)
| Layer | Metric | Threshold | Output key |
|---|---|---|---|
| stage1 (molecular) | screening elimination lines | energy ≤ 0 eV; HOMO ≤ −6 eV | max_energy_ev / max_homo_ev |
| stage2 (cell) | volumetric energy density | ≥ 950 Wh/L | energy_density_wh_l |
| stage2 (cell) | voltage plateau | ≥ 4.1 V | midpoint_voltage_v |
| stage2 (cell) | anode SEI thickness after 100 cyc | ≤ 500 nm | sei_thickness_nm_end |
| stage3 (safety) | 4C fast-charge max temperature | ≤ 50 °C (323.15 K) | T_max_K |
| stage3 (safety) | 4C fast-charge lithium plating | none | plated (false) |

**Trade-off map**
- **Voltage plateau ≥ 4.1 V is the binding constraint.** NMC811/graphite discharge midpoint ≈ 3.6–3.8 V
  (anchor table) cannot meet it. It requires a high-voltage cathode: LNMO spinel (4.7 V class) → cell
  discharge midpoint ≈ 4.17 V. This forces a **system switch** (material design) → `start_stage = 2`.
- High cathode voltage raises electrolyte oxidative-decomposition risk (HOMO vs cathode potential) →
  oxidation-stable electrolyte / additive (molecular funnel).
- 4C no-plating ↔ high transport (σ/t⁺), small anode particle radius, adequate N/P; these raise ohmic
  heat and conflict with T_max ≤ 50 °C → liquid cooling h.
- Volumetric ED 950 Wh/L: high voltage helps (E = Q·V) plus thin current collectors / separator, high
  active fraction. Note 950 Wh/L is *contract-caliber* (electrolyte & casing excluded) — a very high bar.
- SEI ≤ 500 nm after 100 cycles: film-forming additive (FEC/VC) or coating; **requires an aging-capable
  base** (Chen2020 / OKane2022 carry SEI parameters). LNMO.json is a high-voltage cathode OCP and likely
  lacks SEI/aging + thermal/geometry parameters (run-pyamm would inject defaults with a trace).

## 2. Candidate strategy (first round + follow-up)
- Baseline characterization (blocked by shell): `LNMO.json` 1C discharge (spme→dfn) + calc-energy;
  `4C_charge_45C --thermal lumped --plating`; `aging_1C_100cyc` (SEI).
- System-switch risk: if LNMO.json lacks aging/SEI model → two-pronged: (a) patch LNMO OCP into an
  aging-capable base for SEI/aging; (b) bridge transport params (σ/t⁺/D) from molecular screening.
- Molecular candidates (Stage 2 funnel): FEC (fluoroethylene carbonate — SEI film-forming additive),
  VC (vinylene carbonate), and a high-voltage oxidative-stability additive (fluorinated solvent/nitrile).
  Three-model funnel (mace/chgnet/xtb) with elimination lines.
- Architecture variants (Stage 3): thin current collectors, thin separator, tuned porosity, small negative
  particle radius (plating resistance), N/P ratio, cooling h (T_max).

## 3. Budget allocation
- Stage 2 molecular funnel: ~2–3 rounds. Stage 3 architecture + aging: ~4–6 rounds. Stage 4 safety:
  embedded per round. Stage 5 true compute: skipped (`real_compute=false`).
  *(All moot while the shell is broken.)*

## 4. Risk and fallback
- LNMO system lacks aging/thermal/geometry parameters → patch LNMO OCP into an aging-capable base;
  T_max relying on injected defaults marked approximate.
- Voltage-plateau vs SEI requirements pull toward different bases → parameter bridge + system patch.
- 950 Wh/L + T_max ≤ 50 °C + no plating at 4C is a tight multi-objective Pareto corner; if infeasible
  within the boundary, report a negative result honestly (no threshold relaxation).
- Material bottleneck (oxidative stability window) → escalate to Stage 2 molecular design.

## 5. References (domain basis)
- High-voltage spinel LNMO cathode (4.7 V) for ≥ 4.1 V plateau → protocol §1.5 anchor table + domain experience.
- FEC/VC film-forming additives for anode SEI suppression → electrolyte literature (domain experience, no precise source).
- High-transport electrolyte (σ/t⁺) mitigates plating → transport-parameter literature (domain experience).
- No fabricated references; uncertain sources are marked "domain experience".
