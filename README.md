# Virtual Battery Factory

An LLM-agent-driven, cross-scale virtual battery design platform: a fully
software-simulated closed loop spanning material design, cell design, and
safety assessment --- with no dependence on physical experiments.

The agent executes a **fixed design workflow** (five-stage multi-precision
funnel, evaluation-and-fallback routing, code-computed verdicts with an
evidence-chain audit ledger) specified entirely in natural language. The
workflow itself is a self-contained declarative artifact
(`.claude/skills/virtual-battery-factory/`) and is harness-independent by
construction --- cross-harness portability runs under the OpenAI Agents SDK
and LangChain live in `portability/`.

## Entry point and structure

- **`run.py`** (repo root): a thin Agent SDK launcher. It loads the workflow
  skill (`.claude/skills/virtual-battery-factory/SKILL.md`) verbatim into the
  agent's system prompt and drives the simulation library `python -m bda`
  through the harness's built-in shell tool. No custom tools are registered.
- The workflow skill is self-contained under
  `.claude/skills/virtual-battery-factory/`: `SKILL.md` (the workflow rules),
  `references/cli-commands.md` (command reference),
  `scripts/bda/` (the simulation library, pip-editable install), and
  `assets/` (sample cases). If the environment is missing, the agent
  installs it itself per workflow step 0.
- **Cross-harness runs** (portability experiment, §5.7 of the paper):
  `portability/oa_sdk/run_oa.py` (OpenAI Agents SDK --- workflow
  injected as instructions) and `portability/langchain/run_lc.py`
  (LangChain --- workflow loaded via an on-demand `load_skill` tool), with
  batch drivers `run_oa_matrix.py` / `run_lc_matrix.py`.

## Installation

```powershell
# Environment: D:/anaconda/envs/py312 (Python 3.12, CUDA) — the single environment for this
# repo since 2026-09-10; the former repo-local .venv was retired. bda is installed editable
# from the skill directory (re-run the line below only if dependencies need reinstalling):
D:/anaconda/envs/py312/python.exe -m pip install -e ".claude/skills/virtual-battery-factory/scripts[dev,ml,host]"
```

External binaries (needed only for the closing true-compute endorsement;
each runner locates the executable via `PATH`):

| Binary | Purpose | Source |
|---|---|---|
| xtb | Semi-empirical quantum single points (funnel pre-screen) | [github.com/grimme-lab/xtb/releases](https://github.com/grimme-lab/xtb/releases) |
| ORCA | True DFT endorsement (Top-3) | [faccts.de/orca](https://www.faccts.de/orca/) (academic license) |
| GROMACS | True MD endorsement (Top-1) | [gromacs.org/Downloads](https://www.gromacs.org/Downloads) |

ML potentials (MACE-MP/CHGNet) ship with the `[ml]` extra. Cases with
`real_compute: false` need none of the above.

### Environment bootstrap (no secrets on disk)

Create `.env` in the repo root before running:
`DEEPSEEK_API_KEY=<your key>`. `run.py` resolves configuration in order
(existing environment variables always win):

| Variable | Default | Meaning |
|---|---|---|
| `ANTHROPIC_BASE_URL` | `https://api.deepseek.com/anthropic` | Anthropic-compatible endpoint |
| `ANTHROPIC_MODEL` | `official-deepseek-v4-pro` | Model name; `deepseek-v4-pro` is normalized to the official channel |
| `ANTHROPIC_AUTH_TOKEN` | `.env`'s `DEEPSEEK_API_KEY` | Credential; skipped if an Anthropic token is already set |

Secrets are injected only into child-process environment variables, never
written to files, never printed. Connectivity smoke test:
`D:/anaconda/envs/py312/python.exe run.py --smoke-test`.

## Running

**The user's only input is natural language** --- no YAML is ever written or
read by hand. State the design objective directly (e.g., "design a battery
with energy density ≥ 400 Wh/kg and 4C fast charge without lithium
plating"):

1. The skill clarifies item by item via AskUserQuestion (objective
   quantification / starting stage / system / ablation / true-compute
   switch --- all with defaults).
2. After clarification the skill records the criteria, writes them into the
   workspace audit ledger (entry 0), and executes the closed loop.
3. Batch experiments are launched in natural language too ("run N=3", "run
   the ablation matrix") --- each variant becomes a headless `run.py` session.

The closing true-compute endorsement (`run-orca` Top-3, `run-md` Top-1) is
reserved for finalists. **Workspace = the run directory** (`log.jsonl`,
`report.html`, `csv/`, and per-stage artifact subdirectories).

## Ablation experiments

Ablation is declared in the task text itself (the natural-language input
remains the only entry point) and recorded in entry-0 metadata; the workflow
rules are fixed and always on:

| Declaration in the task text | What it answers |
|---|---|
| `reachability_escalation off` | Contribution of the reachability check → material-design escalation |
| `exploration_force off` | Contribution of the forced 2–4 architecture variants per round |
| `funnel_voting off` | Contribution of three-model heterogeneous voting in the molecular funnel |

All on = the full system (main results). See the paper
(`paper/main.tex`, §5.3) for the executed ablation matrix.

## Reporting

Closing a case auto-generates a self-contained HTML report (overview →
iteration trail → funnel statistics → stage results → true-compute
endorsement → final recommendation); open `report.html` in the workspace.

## Tests

```powershell
# fast tests (skip slow)
D:/anaconda/envs/py312/python.exe -m pytest -m "not slow"

# full suite (runner smoke tests auto-skip when the binary is missing)
D:/anaconda/envs/py312/python.exe -m pytest
```

## Repository policy

Versioned: the manuscript (`paper/`, excluding build and preview products),
the experiment artifacts (`runs/`, including the audit ledgers), the
documentation (`docs/`), and the literature (`references/`).

Gitignored: `data/`, `.env` and `runs/.env_local` (secrets are never
committed), plus the paper build and preview products listed in
`.gitignore`.
