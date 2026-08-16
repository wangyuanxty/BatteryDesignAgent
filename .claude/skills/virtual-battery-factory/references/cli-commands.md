# 仿真库 CLI 完整参考（`python -m bda`）

> 由 SKILL.md 第四章指引按需读取。仿真库包位于本 skill 的 `scripts/bda/`（pip 以 editable 安装映射至此，`python -m bda` 即调用它）。

## 通用约定

- 调用形式（Bash 工具，仓库根目录）：`.venv\Scripts\python.exe -m bda <子命令> ...`；全部 9 个子命令见 `-m bda --help`
- **必须用 Bash 工具执行仿真与 render 命令**：本环境 PowerShell 工具受 guardrail 限制（`$()` 子表达式、`Set-Location`、`&` 多操作等一律拦截且无法批准），若你只有 PowerShell 工具可用，说明会话工具白名单异常（续跑轮换了 session 即应恢复），先用 Bash 重试
- JSON 即契约：所有输入/输出均为 UTF-8 JSON 文件，`--out` 指定输出路径；每一步可单独重跑
- 同参数必复用（spec 5.2 不变式 3）：所有 `run-*` 命令先查 store 缓存，命中直接复用不重算。缓存目录 = `--out` 文件所在目录下的 `cache/`（键 = 命令参数组合：run-pyamm: params+protocol+base+mode+thermal+plating；run-mlp: smiles+model；run-xtb: smiles；run-orca: smiles+charge+mult+functional；run-md: box+t_ns+engine）。缓存文件损坏（非法 JSON / 非对象）按未命中处理并重写
- 报错约定：参数/校验类失败打印 `bda error: <原因>` 到 stderr、退出码 1；输入文件缺失或 JSON 键缺失会以 Python traceback 终止——读输出最后几行定位原因，按提示修正后重跑
- 环境依赖：`run-xtb` 需 xtb 二进制在 PATH；`run-orca` 需 orca 在 PATH；`run-md` 需 gmx 在 PATH 且 skill 内 `scripts/bda/simulators/data/opls/` 有对应 .itp 模板

## 阶段1 合并约定（consensus 输入，预飞裁定）

依次真实执行 `run-mlp --model mace`、`run-mlp --model chgnet`、`run-xtb`（同一候选清单），将三次输出合并为一个新建文件（如 `candidates/round_N_merged.json`）作为 `filter`/`consensus` 的输入。合并规则：

- `run-mlp` 输出键为 `metrics.energy_ev` + `"model"` 字段：`model == "mace"` 的 `energy_ev` → 键 `mace_energy_ev`；`model == "chgnet"` 的 `energy_ev` → 键 `chgnet_energy_ev`
- `run-xtb` 输出键为 `metrics.homo_ev`/`lumo_ev`：`homo_ev` → 键 `xtb_homo_ev`（`lumo_ev` 可一并保留）
- 同时保留 `converged`、`energy_ev`（mace 值）、`homo_ev`（xtb 值）——`filter` 读取这三个键，`consensus` 读取三个排名键 `mace_energy_ev`、`chgnet_energy_ev`、`xtb_homo_ev`；一个合并文件同时满足两者，且 `filter` 输出可直接作为 `consensus` 输入

合并文件示例（数值为占位，以实际输出为准）：

```json
{"candidates": [
  {"smiles": "C1COC(=O)O1", "metrics": {
    "converged": true, "energy_ev": -123.45,
    "mace_energy_ev": -123.45, "chgnet_energy_ev": -122.98,
    "homo_ev": -8.12, "lumo_ev": 0.41, "xtb_homo_ev": -8.12
  }}
]}
```

## bridge — 微观物性 → PyBaMM 参数映射

```
bda bridge --props PROPS --out OUT
```

- 输入 `--props`：`{"D_electrolyte_m2_s": 3e-10, "conductivity_S_m": 1.1, "transport_number": 0.4}`（键可只给子集；合法键仅 `D_electrolyte_m2_s`、`conductivity_S_m`、`transport_number`）
- 输出：PyBaMM 参数名 → 值，如 `{"Electrolyte diffusivity [m2.s-1]": 3e-10, "Electrolyte conductivity [S.m-1]": 1.1, "Cation transference number": 0.4}`；可直接作为 `run-pyamm --params` 输入
- 报错：`unknown micro property '<k>'; legal keys: ...` → 修正键名重跑

## filter — 漏斗硬淘汰

```
bda filter --in IN --rules RULES --out OUT
```

- 输入 `--in`：`{"candidates": [{"smiles": "SMILES", "metrics": {...}}]}` —— 用合并文件（见合并约定）
- 输入 `--rules`：`{"max_energy_ev": -1.0, "max_homo_ev": -6.0}`（两键均可选；都不给则只看 converged）
- 规则：`metrics.converged` 非真 → rejected；给了 `max_energy_ev` 而 `energy_ev` 缺失或超限 → rejected；给了 `max_homo_ev` 而 `homo_ev` 缺失或超限 → rejected；否则 passed
- 输出：输入同结构 + 每候选增加 `"status": "passed" | "rejected"`
- 报错：无自定义校验错误；JSON 语法错误 → `bda error: ...`；输入文件不存在 → FileNotFoundError traceback
- 注意：缺少 `converged` 键的输入会被整体淘汰——不要把 `run-xtb` 输出直接喂给 filter

## consensus — 三模型一致性投票

```
bda consensus --in IN --out OUT
```

- 输入 `--in`：`{"candidates": [{"smiles": "SMILES", "metrics": {"mace_energy_ev": f, "chgnet_energy_ev": f, "xtb_homo_ev": f}}]}` —— 合并文件或 `filter` 输出
- 规则：三个键各自升序排名（能量/轨道能越低越优）；某候选三排名 max−min ≥ 阈值 → disputed。阈值为 `max(2, 0.3×候选数)`（候选数 < 3 时原样返回不判定）
- 输出：输入同结构；分歧候选增加 `"status": "disputed"` 与 `"dispute_detail": {"ranks": {"mace_energy_ev": r, "chgnet_energy_ev": r, "xtb_homo_ev": r}}`；未分歧候选不加 status
- 报错：输入 metrics 缺少任一排名键 → KeyError traceback → 检查合并文件键名
- 处置：disputed 候选按 SKILL.md 第一节第 1 步处理（改进或明确淘汰理由）

## run-pyamm — 电芯仿真

```
bda run-pyamm --params PARAMS --protocol PROTOCOL [--base BASE] [--mode MODE] [--thermal THERMAL] [--plating] --out OUT
```

- `--base`：PyBaMM 参数集名（默认 `Chen2020`）；**案例配置的 `base_params` 字段必须原样传给 `--base`**（如 `--base ORegan2022`）。bridge 输出的参数名为跨参数集共享名（`Electrolyte diffusivity [m2.s-1]` 等），故 `--params` 可直接配合任一参数集使用
- `--protocol` 合法值：`1C_discharge`（1C 放电，3600 s，298.15 K）；`4C_charge_45C`（4C 充电，900 s，318.15 K）
- `--mode`：`spme`（默认）/ `dfn`；dfn 求解失败自动降级 SPMe 重试（输出 `model_used` 记 `"SPMe(fallback)"`）
- `--thermal`：`lumped`（默认）/ `isothermal`；非 isothermal 时输出含 `T_max_K`
- `--plating`：启用析锂模块（Chen2020 参数集无析锂参数，运行时注入标准默认值），输出含 `anode_potential_v`
- 输入 `--params`：`{"<PyBaMM 参数名>": 值}` —— 参数名会按所选参数集校验，通常直接给 `bridge` 输出
- 输出键：`model_used`、`time_s`、`voltage_v`、`capacity_ah`、`T_max_K`（非 isothermal）、`anode_potential_v`（--plating）
- 报错：
  - `unknown protocol 'x'; legal: ['1C_discharge', '4C_charge_45C']` → 修正协议名
  - `unknown mode 'x'; legal: spme, dfn` → 修正模式名
  - `unknown parameter name(s): ['...']` → 参数名不在所选参数集内；检查 bridge 键与拼写
  - SPMe 求解失败（pybamm.SolverError traceback）→ 该参数组合无效，按 SKILL.md 第一节第 5 步回退调整

## run-mlp — ML 势结构松弛

```
bda run-mlp --in IN [--model MODEL] --out OUT
```

- `--model`：`mace`（默认）/ `chgnet`
- 输入 `--in`：`{"candidates": [{"smiles": "SMILES"}]}`
- 输出：`{"candidates": [{"smiles": "SMILES", "metrics": {"energy_ev": f, "converged": bool}, "model": "mace"}]}`
- 报错：`invalid SMILES: '...'` → 修正 SMILES；`unknown model 'x'; legal: mace, chgnet` → 修正模型名；`failed to embed 3D structure for ...` → 该 SMILES 无法构象嵌入，换候选
- 使用位置：阶段1，每个模型各跑一次（mace 与 chgnet）

## run-xtb — 半经验量子单点

```
bda run-xtb --in IN --out OUT
```

- 输入 `--in`：`{"candidates": [{"smiles": "SMILES"}]}`
- 输出：`{"candidates": [{"smiles": "SMILES", "metrics": {"homo_ev": f, "lumo_ev": f}}]}`
- 报错：
  - `xtb binary not found; install from https://github.com/grimme-lab/xtb/releases and put xtb.exe on PATH` → 安装 xtb 并加入 PATH
  - `failed to embed 3D structure for ...` → 换候选
  - `xtb failed: <stderr 尾部 500 字符>` → 按 stderr 内容排查（结构/收敛问题）
  - `failed to parse HOMO/LUMO from xtb output` / `failed to parse total energy from xtb output` → 计算虽跑完但产物缺失，换构象或换候选重跑

## run-orca — 真 DFT 背书（仅收尾 Top-3）

```
bda run-orca --in IN --out OUT
```

- 输入 `--in`：`{"candidates": [{"smiles": "SMILES"}]}`
- 输出：`{"candidates": [{"smiles": "SMILES", "endorsement": {"E_hartree": f, "homo_ev": f, "lumo_ev": f, "ie_ev": f, "ea_ev": f}}]}` —— ie_ev/ea_ev 为垂直电离能/电子亲和能（电压窗口代理）
- 每个候选跑中性/阳离子/阴离子三次气相几何优化（r2SCAN-3c + OPT，优化后自动单点），自旋多重度按各电荷态电子数奇偶推导（偶→单重态、奇→二重态）；每分子最多重试 3 次；CPU 慢（每分子约 2~3 小时），只在收尾执行，禁止在漏斗内使用
- 报错：
  - `ORCA binary not found; download academic Windows build from the ORCA forum` → 安装 ORCA 并加入 PATH
  - `ORCA failed after 3 attempts for <smiles> (DFT not converged): ...` → 如实记录"该候选 DFT 未收敛"，不得伪造数值

## run-md — 真 MD 扩散背书（仅收尾 Top-1）

```
bda run-md --box BOX [--engine ENGINE] [--t-ns T_NS] --out OUT
```

- 输入 `--box`：`{"molecules": {"EC": 60, "EMC": 40, "PF6": 10, "Li": 10}}`（Li 至少 1；`t_ns` 可内嵌，`--t-ns` 默认 10.0）
- `--engine`：`gromacs`（默认）/ `mace`。`mace` = ASE + MACE-MP Langevin NVT（固定种子盒、298.15 K、1 fs 步长），只需 mace-torch，不需要 GROMACS 与 .itp 模板；Top-1 交叉验证时可两引擎各跑一次对比 D_Li_m2_s
- 输出：`{"D_Li_m2_s": f, "trajectory_ok": bool, "drift_check": "ok"|"drift"|"skipped", "achieved_density_g_cm3": f}` —— `trajectory_ok: false`（drift）时如实记录并报告（mace 引擎的 drift 判据 = 逐帧 MACE 势能的后 20% 均值相对中段漂移 > 5%）
- 报错：
  - `unknown engine 'x'; legal: gromacs, mace` → 修正引擎名
  - `GROMACS not found; install via winget install GROMACS.GROMACS or conda` → 安装 GROMACS（仅 gromacs 引擎）
  - `mace engine requires mace-torch; install via \`pip install mace-torch\`` → 安装 mace-torch（仅 mace 引擎）
  - `box must contain at least 1 Li` → box 至少 1 个 Li
  - `missing OPLS-AA .itp template(s): ...` → 按 skill 内 `scripts/bda/simulators/data/opls/README.md` 生成对应 .itp 模板（仅 gromacs 引擎）
  - `gmx mdrun failed: ...` / `gmx trjconv failed: ...` → 按 stderr 尾部内容排查

## render — HTML 报告

```
bda render --case-dir CASE_DIR [--out OUT]
```

- 读取 `<case_dir>/log.jsonl`（第 0 条 criteria + 全部 action 条目），产出自包含 HTML（任务概览/迭代轨迹/漏斗统计/阶段 2/3 结果/收尾背书/最终推荐 六节），写入 `<case_dir>/<out>`（默认 `report.html`）
- 无 log.jsonl → 渲染空报告；无对应条目 → 该节显示"暂无数据"
- 报错：无自定义校验；log 行 JSON 解析失败 → traceback 指出行号
- 使用位置：收尾最后一步；报告全部内容由 log.jsonl 确定性生成，无额外 LLM 调用
