# Simulation Library CLI Full Reference (`python -m bda`)

> Read on demand per the SKILL.md Section 4 guidance. The simulation library package lives in this skill's `scripts/bda/` (pip-editable-installed to this path; `python -m bda` invokes it).

## General conventions

- Invocation (Bash tool, repo root): `.venv\Scripts\python.exe -m bda <subcommand> ...`; all subcommands listed via `-m bda --help`
- The parameter bridge is a protocol rule (PyBaMM parameter-name mapping table in SKILL.md Section 1, Step 2); it has no CLI command.
- **Must use the Bash tool for simulation and render commands**: the PowerShell tool in this environment is guardrail-limited (`$()` subexpressions, `Set-Location`, `&` multi-operations are all blocked and unapprovable); if only PowerShell is available, the session tool allowlist is abnormal (resume rotation restores it) — retry with Bash first.
- JSON is the contract: all inputs/outputs are UTF-8 JSON files; `--out` specifies the output path; each step can be rerun independently.
- Same parameters must be reused (spec 5.2 invariant 3): all `run-*` commands check the store cache first, reusing on hit without recomputation. Cache directory = `cache/` under the `--out` file's directory (key = command parameter combination: run-pyamm: params+protocol+base+mode+thermal+plating; run-mlp: smiles+model; run-xtb: smiles; run-orca: smiles+charge+mult+functional; run-md: box+t_ns+engine; run-comp: candidates). Corrupt cache files (invalid JSON / non-object) are treated as misses and rewritten.
- Error convention: parameter/validation failures print `bda error: <reason>` to stderr with exit code 1; missing input files or missing JSON keys terminate with a Python traceback — read the last few output lines to locate the cause, fix per the hint, and rerun.
- Environment dependencies: `run-xtb` needs the xtb binary on PATH; `run-orca` needs orca on PATH; `run-cp2k` needs the MSYS2 CP2K binary (`C:\msys64\ucrt64\bin\cp2k_stack4g.exe`, stack-patched) and the CP2K data files under `C:\cp2k-data` (BASIS_MOLOPT / GTH_POTENTIALS / dftd3.dat); `run-qe` needs the MSYS2 pw.x (`C:\msys64\ucrt64\bin\pw_stack4g.exe`) and conda-forge SSSP pseudopotentials; `run-md` gromacs engine needs gmx on PATH and the .itp templates in the skill's `scripts/bda/simulators/data/opls/`, while the mace engine needs only mace-torch (no GROMACS, no templates).

## Stage 2 funnel judgment (no CLI command)

Funnel judgment (hard elimination lines + three-model heterogeneous voting) is executed per protocol rules — see SKILL.md Section 1, Step 1: run `run-mlp --model mace`, `run-mlp --model chgnet`, `run-xtb` for real, in order (same candidate list), then judge directly by reading the three output JSONs. No CLI command, no merged file needed.

## run-pyamm — cell simulation

```
bda run-pyamm --params PARAMS --protocol PROTOCOL [--base BASE] [--mode MODE] [--thermal THERMAL] [--plating] [--cycles N] --out OUT
```

- `--base`: PyBaMM parameter-set name (default `Chen2020`); **the case configuration's `base_params` field must be passed verbatim to `--base`** (e.g., `--base ORegan2022`). Parameter names from the parameter bridge mapping table (SKILL.md Section 1, Step 2) are cross-set shared names (`Electrolyte diffusivity [m2.s-1]`, etc.), so `--params` works directly with any parameter set.
- `--protocol` legal values:
  - `1C_discharge` (1C discharge, 3600 s, 298.15 K)
  - `0.1C_discharge` (0.1C low-rate discharge, 36000 s, 298.15 K — real-data alignment calibers)
  - `4C_charge_45C` (4C charge, 900 s, 318.15 K)
  - `5C_discharge` (5C high-rate discharge, 720 s — rate scenarios; **high rate recommends `--mode dfn`** — SPMe severely underestimates capacity at 5C)
  - `lowT_discharge` (1C discharge, -20 °C/253.15 K — low-temperature scenarios)
  - `overcharge` (first 1C discharge to lower cut-off, then 0.5C charge to upper cut-off +0.5 V — overcharge scenarios; output includes T_max_K)
  - `aging_1C_100cyc` (100 cycles of 1C constant-current charge/discharge, SEI ec reaction limited + isothermal; voltage limits taken from the parameter set itself)
  - `aging_1C_100cyc_45C` (same, but 45 °C/318.15 K high-temperature aging)
- `--cycles`: override aging cycle count (default 100)
- `--mode`: `spme` (default) / `dfn`; dfn solver failure auto-degrades to SPMe retry (output `model_used` records `"SPMe(fallback)"`)
- `--thermal`: `lumped` (default) / `isothermal`; non-isothermal output includes `T_max_K`. The aging protocol internally fixes isothermal; `--thermal`/`--plating` are ignored
- `--plating`: enable plating module (Chen2020 parameter set has no plating parameters; standard defaults injected at runtime), output includes `anode_potential_v`
- Input `--params`: `{"<PyBaMM parameter name>": value}` — parameter names validated against the chosen parameter set, typically written per the mapping table in SKILL.md Section 1, Step 2
- Output keys: `model_used`, `time_s`, `voltage_v`, `capacity_ah`, `T_max_K` (non-isothermal), `anode_potential_v` (--plating); aging protocol outputs `model_used`, `protocol: "aging"`, `cycle_numbers`, `capacity_ah_per_cycle`, `sei_thickness_nm_end`
- Errors:
  - `unknown protocol 'x'; legal: [...]` → fix protocol name
  - `unknown mode 'x'; legal: spme, dfn` → fix mode name
  - `unknown parameter name(s): ['...']` → parameter name not in the chosen parameter set; check key names/spelling per the SKILL.md Section 1, Step 2 mapping table
  - `base parameter set has no 'SEI kinetic rate constant [m.s-1]'; ...` → chosen system has no aging model (e.g., ORegan2022); aging protocol only on aging-capable sets (Chen2020/OKane2022 etc.); honestly record N/A for systems without aging models
  - SPMe solve failure (pybamm.SolverError traceback) → parameter combination invalid; adjust per SKILL.md Section 1, Step 5 fallback
- Aging-protocol note: under standard SEI models the capacity trajectory may show a non-monotonic climb-then-saturate artifact (lithium loss shifts the voltage window) — annotate honestly in reports/evaluation, do not treat as normal degradation; coating/doping vs baseline must compare on the same system

## run-mlp — ML potential structure relaxation

```
bda run-mlp --in IN [--model MODEL] --out OUT
```

- `--model`: `mace` (default) / `chgnet`
- Input `--in`: `{"candidates": [{"smiles": "SMILES"}]}`
- Output: `{"candidates": [{"smiles": "SMILES", "metrics": {"energy_ev": f, "converged": bool}, "model": "mace"}]}`
- Errors: `invalid SMILES: '...'` → fix SMILES; `unknown model 'x'; legal: mace, chgnet` → fix model name; `failed to embed 3D structure for ...` → SMILES cannot be conformer-embedded, switch candidate
- Where used: Stage 2, once per model (mace and chgnet)

## run-xtb — semi-empirical quantum single point

```
bda run-xtb --in IN --out OUT
```

- Input `--in`: `{"candidates": [{"smiles": "SMILES"}]}`
- Output: `{"candidates": [{"smiles": "SMILES", "metrics": {"homo_ev": f, "lumo_ev": f}}]}`
- Errors:
  - `xtb binary not found; install from https://github.com/grimme-lab/xtb/releases and put xtb.exe on PATH` → install xtb and add to PATH
  - `failed to embed 3D structure for ...` → switch candidate
  - `xtb failed: <last 500 chars of stderr>` → troubleshoot per stderr content (structure/convergence issues)
  - `failed to parse HOMO/LUMO from xtb output` / `failed to parse total energy from xtb output` → computation ran but output artifact missing; switch conformer or candidate and rerun

## run-orca — true DFT endorsement (only closing Top-3)

```
bda run-orca --in IN --out OUT
```

- Input `--in`: `{"candidates": [{"smiles": "SMILES"}]}`
- Output: `{"candidates": [{"smiles": "SMILES", "endorsement": {"E_hartree": f, "homo_ev": f, "lumo_ev": f, "ie_ev": f, "ea_ev": f}}]}` — ie_ev/ea_ev are vertical ionization energy/electron affinity (voltage-window proxies)
- Per candidate: gas-phase geometry optimization of neutral/cation/anion three times (r2SCAN-3c + OPT, automatic single point after optimization); spin multiplicity derived from electron count parity per charge state (even→singlet, odd→doublet); max 3 retries per molecule; CPU-slow (~2–3 hours per molecule), only at closing; forbidden inside the funnel
- Errors:
  - `ORCA binary not found; download academic Windows build from the ORCA forum` → install ORCA and add to PATH
  - `ORCA failed after 3 attempts for <smiles> (DFT not converged): ...` → honestly record "this candidate's DFT did not converge"; do not fabricate values

## run-md — true MD diffusion endorsement (only closing Top-1)

```
bda run-md --box BOX [--engine ENGINE] [--t-ns T_NS] --out OUT
```

- Input `--box`: `{"molecules": {"EC": 60, "EMC": 40, "PF6": 10, "Li": 10}}` (Li ≥ 1; `t_ns` may be embedded; `--t-ns` default 10.0)
- `--engine`: `gromacs` (default) / `mace`. `mace` = ASE + MACE-MP Langevin NVT (fixed-seed box, 298.15 K, 1 fs step), requires only mace-torch, no GROMACS/.itp templates; for Top-1 cross-validation run both engines and compare D_Li_m2_s.
- Output: `{"D_Li_m2_s": f, "trajectory_ok": bool, "drift_check": "ok"|"drift"|"skipped", "achieved_density_g_cm3": f}` — on `trajectory_ok: false` (drift) record and report honestly (mace drift criterion = last-20% mean MACE potential energy drifting > 5% from the middle segment)
- Errors:
  - `unknown engine 'x'; legal: gromacs, mace` → fix engine name
  - `GROMACS not found; install via winget install GROMACS.GROMACS or conda` → install GROMACS (gromacs engine only)
  - `mace engine requires mace-torch; install via \`pip install mace-torch\`` → install mace-torch (mace engine only)
  - `box must contain at least 1 Li` → box needs ≥ 1 Li
  - `missing OPLS-AA .itp template(s): ...` → generate the corresponding .itp templates per the skill's `scripts/bda/simulators/data/opls/README.md` (gromacs engine only)
  - `gmx mdrun failed: ...` / `gmx trjconv failed: ...` → troubleshoot per trailing stderr content

## render — HTML report

```
bda render --case-dir CASE_DIR [--out OUT]
```

- Reads `<case_dir>/log.jsonl` (entry 0 criteria + all action entries), produces a self-contained HTML (task overview / iteration trajectory / funnel statistics / stage results / true DFT-MD endorsement / final recommendation / design notes — seven sections), written to `<case_dir>/<out>` (default `report.html`)
- No log.jsonl → renders an empty report; no corresponding entry → section shows "no data yet"
- Errors: no custom validation; log-line JSON parse failure → traceback pointing at the line number
- Where used: last closing step; report content deterministically generated from log.jsonl, no extra LLM calls

## run-comp — electrode composition screening (CHGNet periodic relaxation)

```
bda run-comp --in IN --out OUT
```

- **Environment requirement**: CUDA torch (GPU relaxation ~20 s/state); CPU torch relaxation does not converge (measured). Local `.venv` is CPU torch — use `D:/anaconda/envs/py312/python.exe -m bda run-comp ...` (py312 has chgnet/pymatgen/ase + torch 2.13.0+cu126)
- Input `--in`: `{"candidates": [{"formula": "Li(Ni0.7Mn0.05Co0.05Si0.1Mg0.1)O2", "name": "NMC-SiMg"}]}` — NMC811 lattice site substitution; TM fractions must sum to 1
- Output: `{"baseline": {NMC811 energy + Li metal reference}, "candidates": [{formula, realized_tm_counts, avg_voltage_v, capacity_mah_g, e_full_ev, e_delith_ev, converged, rel_stability_ev_atom}], "calibration_note"}`
- Definitions (stated honestly, written to the report):
  - Average voltage = −[E(Li_x2)−E(Li_x1)−n_removed·E_Li]/n_removed (x∈[0.3,1], includes Li metal reference; NMC811 self-calibration ≈3.82 vs literature 3.8 V)
  - Capacity = 0.7 Li × F/3.6 ÷ molar mass (theoretical proxy; NMC811 ≈194 mAh/g)
  - `rel_stability_ev_atom` is for within-batch relative ranking only (relaxation not strictly converged; energy difference for the same composition between two relaxations can be ~1 eV/atom)
  - `converged=false` is common (300-step FIRE with fmax 0.1 not reached) — energy at screening precision; annotate honestly
  - True endorsement: `run-qe` at closing (periodic DFT, next section) — inside the funnel it is ALWAYS the CHGNet proxy definition
- Errors: `TM fractions must sum to 1` → fix composition; `no transition-metal species` → formula lacks TM

## run-qe — periodic DFT true endorsement (only closing Top composition)

```
bda run-qe --in IN --out OUT
```

- **Environment**: MSYS2's QE (native Windows, not a VM): `winget install MSYS2.MSYS2`, switch pacman mirror (TUNA, see install notes), `pacman -S mingw-w64-ucrt-x86_64-quantum-espresso`; pw.exe at `C:\msys64\ucrt64\bin\`; pseudopotentials from conda-forge `sssp` package directory (`D:\anaconda\envs\py312\share\sssp\efficiency`, override with env var `QE_PSEUDO_DIR`)
- **Two known pitfalls (already handled on this machine; do not repeat)**: ① MSYS2 stock pw.exe reserves only 2 MB stack — initialization stack-overflows (0xC00000FD) — needs pefile patching to `pw_stack4g.exe` (4 GB stack reserve); the runner auto-prefers it; ② backslash is an escape character in Fortran namelists — the runner auto-converts Windows paths to forward slashes when generating input
- Input `--in`: `{"candidates": [{"formula": "Li(Ni0.8Mn0.1Co0.1)O2", "name": "NMC811"}]}`
- Output: per candidate `{formula, realized_tm_counts, avg_voltage_v, e_full_ev, e_delith_ev, e_li_metal_ev, converged, wall_time_s}` — voltage formula same as run-comp (includes Li metal reference)
- Computational definitions: ecutwfc 50 Ry / ecutrho 400 (SSSP efficiency standard); nspin=2 ferromagnetic guess (Ni/Mn/Co); lithiated vc-relax + delithiated fixed-cell relax + bcc Li vc-relax; CPU hours (12-atom primitive cell ~1 h/state, 48-atom supercell overnight) — **closing only, forbidden inside the funnel** (same iron rule as run-orca)
- Errors:
  - `pw.x not found; install MSYS2 ...` → install the MSYS2 quantum-espresso package per guidance
  - `QE pseudopotential dir not found; ...` → install conda-forge sssp package or set QE_PSEUDO_DIR
  - `no SSSP efficiency pseudopotential entry for element X` → element not in the built-in pseudopotential table (Li/Ni/Mn/Co/O/Si/Mg); extend the _PSEUDO_FILES mapping
  - `pw.x produced no total energy for ...` → read *.out in the work directory (SCF non-convergence is common: add mixing_beta / change initial magnetization)

## log-evaluate — evaluate entry recorder (mechanical verdict/evidence)

```
bda log-evaluate --case-dir D --round N --outputs F... [--candidate name] [--note diagnosis]
```

- **Why it exists**: v3 incident — the agent evaluated V1-V3 in conversation (real values) but never wrote log entries, so the report's round cards were propose-only yet cited "round 1 conclusions". This command turns "evaluation happened → entry exists" into a mechanical guarantee: verdict computed by code against entry-0 criteria; the agent must not hand-write verdict or append_entry an evaluate itself.
- **Prerequisite**: `--case-dir`'s log.jsonl must have entry-0 criteria (pre-registered before running); missing → `bda error` + exit code 1 (non-judgable evaluations rejected outright)
- **Input `--outputs`**: simulation output JSON file paths (relative to `--case-dir`, repo-root-relative, or absolute, all accepted; multiple allowed); scalar keys (int/float/bool) all extracted into `metrics` (later files overwrite earlier ones)
- **plated auto-derivation**: output without `plated` key but with `anode_potential_v` series → `min < 0` determines plating; evidence source annotated `anode_potential_v (min=X.XXXV<0 derived)` — consistent with manual judgment
- **verdict rules**: threshold forms `{"min": n}` (greater-or-equal) / `{"max": n}` / boolean equality / scalar (treated as min); all checked metrics pass → `pass`, else `fail`; output missing a criteria metric → record `unchecked` and append "unchecked criteria: ..." to note (legitimate gap when stage not yet reached; verdict judged on checked metrics)
- **Output entry**: `{"action": "evaluate", "round": N, "metrics": {...scalars}, "verdict": "pass"|"fail", "evidence": [{"metric", "value", "threshold", "verdict", "source": "file:key"}, ...], "candidate"?, "unchecked"?, "note"?}` — evidence source is case-relative path (audit log replayable across machines)
- **Multiple candidates in same round**: one entry per evaluated candidate (multiple calls same round, distinguished by `--candidate`); report merges display by round
- Errors:
  - `entry-0 criteria not found in log.jsonl` → write criteria before evaluating
  - `output file does not exist: ...` → check path (relative to case-dir's cell/ directory)
  - `no criteria metrics in output files` → output keys entirely mismatch criteria; check whether the wrong file was passed
  - threshold dict has bound but value non-numeric → fail (non-judgable forms always fail — rather fail than fake pass)

## verify-deliverables — deliverable protocol-compliance check

```
bda verify-deliverables --case-dir D
```

- **Check items (all mechanical)**: ① 7 deliverable categories complete (design_spec/bom/datasheet/calc/dvpr/dfmea/delivery_index, each with source file + PDF release) ② PDF non-empty (>1KB) ③ xlsx parseable with no empty sheets ④ delivery_index contains a VBF numbering list (≥5) ⑤ **audit chain complete: every propose round must have a same-round evaluate entry** (log-evaluate protocol prerequisite — evaluation without log entries leaves report conclusions without audit backing)
- **Output**: per-item `[PASS]/[FAIL]` + summary `ALL PASS`/`HAS FAILURES`; exit code 0/1
- **Error handling**: FAIL = protocol unmet; fix per detail and rerun (e.g., "propose round without evaluation: R01" → add log-evaluate entries); `missing log.jsonl` → protocol execution must have logs

## calc-energy — contract-caliber energy density (same formula for all tasks)

```
bda calc-energy --sim S [--params P] [--base B] --out O
```

- **Formula (contract caliber, preventing cross-task precedent copying)**: `ED = ∫V·I_1C dt / Σ(layer thickness×(1−porosity)×density×area)`
  - Discharge energy = trapezoidal integral of `voltage_v`×`time_s` × I_1C, ÷3600 for Wh; I_1C = `Nominal cell capacity [A.h]` × 1 (constant current)
  - Area = `Electrode height [m]` × `Electrode width [m]`
  - Layers: positive/negative active layers (porosity factor applied), positive/negative current collectors (no porosity factor), separator — all from the parameter set used by `--base` (default Chen2020) or overridden by `--params`
  - **Electrolyte excluded from mass** (parameter set lacks density) — output `electrolyte_included: false` annotated honestly
- **Input**: `--sim` = discharge simulation output JSON (must contain `voltage_v` list, `time_s` list, `capacity_ah` scalar); `--params` optional, overrides the parameter set (the same params file used by run-pyamm)
- **Output**: `{capacity_ah, energy_wh, mass_kg, energy_density_wh_kg, volume_m3, energy_density_wh_l, thickness_m, midpoint_voltage_v, dcr_ohm, power_density_w_kg, layer_kg_m2 (per layer kg/m²), area_m2, electrolyte_included: false, note}`
  - `energy_density_wh_l` = energy/volume (volume = Σ layer thickness×area; contract caliber excludes electrolyte/casing)
  - `midpoint_voltage_v` = voltage at discharge-time midpoint (plateau-voltage approximation); `dcr_ohm` = DC resistance (start OCV − voltage at 10% discharge ÷ I_1C); `power_density_w_kg` = V_OC²/(4·DCR) ÷ mass
  - Judgment and report use this file's `energy_density_wh_kg`
- **Errors**: `bda error: ...` + exit code 1 — missing parameter keys (`KeyError`), `--sim` not valid JSON, numeric type mismatch; first check `--sim` points to a 1C discharge output and `--base` has the corresponding keys

## run-tr — thermal-runaway three-side-reaction ODE (Stage 4 abuse scenarios)

```
bda run-tr [--sim S] [--mass-kg M] [--t-init T] [--x0 X] [--t-max T] [--mcp M] [--hA H] [--t-amb T] [--q-nail W] --out OUT
```

- **Model**: zero-dimensional lumped thermal balance + three-side-reaction Arrhenius kinetics (SEI decomposition / negative-electrolyte / positive-electrolyte), scipy BDF stiff integration; first-order reactant consumption guarantees energy conservation (bounded T_max)
- **Trigger judgment (mechanical)**: dT/dt > 1 K/s (temperature-rise inflection) or T ≥ 573 K (300°C red line) → `triggered: true` + `trigger_time_s`
- **Overcharge → thermal runaway auto-coupling**: `--sim` passes run-pyamm output (e.g., overcharge protocol), auto-reads its `T_max_K` as initial temperature
- **Nail**: `--q-nail` short-circuit heat source (W)
- **Output keys**: `triggered`, `trigger_time_s`, `T_max_K`, `T_final_K`, `dTdt_max_K_s`, `T_series_K`, `t_series_s`, `params`
- **--mass-kg mandatory**: pass the cell mass from calc-energy's `mass_kg` → mcp = mass×900; otherwise mcp fixed at 1000 systematically distorts small cells (t7_r1 incident: a 40 g cell was judged as 1 kg)
- **Errors**: `--sim` file missing `T_max_K` key → should pass a run-pyamm output JSON

## run-cp2k — molecular true DFT cross-validation (only closing Top-3, optional)

```
bda run-cp2k --in IN --out OUT
```

- **Isomorphic output with run-orca** (same batch of molecules under two independent programs, removing program-implementation-difference concerns): `{"candidates": [{"smiles": ..., "endorsement": {E_hartree, homo_ev, lumo_ev, ie_ev, ea_ev, converged}}]}` — `ie_ev`/`ea_ev` are **vertical** single points of cation/anion states on the neutral optimized geometry (consistent with run-orca)
- **Method**: PBE + D3(BJ) dispersion correction, DZVP-MOLOPT-SR-GTH short-range basis + GTH-PBE pseudopotentials (H/C/O/F/N/S/P/B/Li), 20 Å vacuum box for isolated molecules (PERIODIC NONE + Poisson MT); neutral state GEO_OPT, ionic states ENERGY single points
- **Environment**: MSYS2 `pacman -S mingw-w64-ucrt-x86_64-cp2k`; data files `C:\cp2k-data` (BASIS_MOLOPT/GTH_POTENTIALS/dftd3.dat, downloaded from the cp2k/cp2k GitHub data/ directory; override with env var `CP2K_DATA_DIR`)
- **Two known pitfalls (runner auto-handles)**: ① MSYS2 stock cp2k.ssmp.exe reserves 2 MB stack — large molecules overflow at initialization — runner auto-prefers the pefile-patched `cp2k_stack4g.exe`; ② DBCSR reads `/proc/self/statm` at SCF start (no Windows CRTL path translation) — runner places a static page-count file at `C:\proc\self\statm`, runs via MSYS2 bash, caps OMP_NUM_THREADS at 8 (32 threads easily exhaust memory and crash), OMP_STACKSIZE 512M
- **Cost**: CPU minutes per small molecule (FEC-class 10 atoms ≈ 15–40 min/molecule) — **closing Top-3 only, forbidden inside the funnel** (same iron rule as run-orca; skipped when `real_compute: false`)
- **Errors**:
  - `cp2k not found; install: ...` → install the MSYS2 cp2k package per guidance
  - `CP2K data dir not found; ...` → download data files to `C:\cp2k-data` or set CP2K_DATA_DIR
  - `invalid SMILES: ...` / `failed to embed 3D structure ...` → RDKit cannot parse/generate conformer; check SMILES
  - `cp2k produced no total energy` → read *.out in the work directory (SCF non-convergence common: loosen EPS_SCF tolerance or increase MAX_SCF)
  - Single-candidate failure does not break the whole batch: that candidate outputs `{"smiles": ..., "error": "..."}`, the rest return normally
