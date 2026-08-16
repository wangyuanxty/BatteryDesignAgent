---
name: virtual-battery-factory
description: 虚拟电池工厂协议——三阶段电池设计闭环（材料→电芯→安全）加评估回退控制环。当用户要求设计电解液/添加剂并运行案例时使用。
---

# 虚拟电池工厂协议

你是电池设计智能体。你自带电化学领域知识；本协议只规定**流程、边界与反模式**，以及仿真库命令用法。所有结论级数值必须来自工具输出文件，不得凭记忆编造。

## 一、任务流程（线性，无阶段 4）

### 准备（每案例一次）

1. 读取案例配置（字段：`goal` 设计目标、`system` 材料体系、`max_rounds` 迭代预算、`seed_pool` 种子池、`ablations` 消融开关、`base_params` 参数集、`real_compute` 真计算开关）。配置与工作区路径以系统提示注入的 `配置:` / `工作区:` 字段为准（Agent SDK 启动器注入，工作区=配置所在目录；`runs/<case_id>/` 仅为无注入时的默认布局）。
2. 若 `log.jsonl` 已存在（续跑/resume）：从最后一条记录恢复状态，不重复执行已完成步骤（以产物文件存在为准）。
3. 从 `goal` 自然语言解析达标标准（指标名、阈值、单位），写入 `log.jsonl` 第 0 条后直接开跑。

对每个候选分子严格执行：

1. **阶段1 材料设计**（快环，零真计算）：生成候选（`seed_pool` + 自由生成）→ `run-mlp --model mace` → `run-mlp --model chgnet` → `run-xtb` → 按第四节合并约定建 consensus 输入 → `filter`（漏斗硬淘汰）→ `consensus`（三模型一致性投票）
   - 写 `propose` 与 `funnel` 日志条目
   - `consensus` 返回 `disputed` 的候选：不得淘汰即止，须推理改进（换取代基/生成变体）或明确给出淘汰理由后换新候选
2. **参数桥梁**：对通过候选执行 `bridge`，产出 PyBaMM 参数更新（props 数值来源写入日志）
   - props 数值来源规则：种子池候选用文献值（在日志中标注引用来源）；自由生成候选用领域估计值（标注 `estimate`）；来源必须写入日志；估计值不得冒充仿真输出——收尾时若该候选进入 Top-N，其 D/σ 由真 MD/文献背书复核
3. **阶段2 电芯设计**：`run-pyamm --protocol 1C_discharge --mode spme`，随后按需 `--mode dfn`
4. **阶段3 安全评估**：`run-pyamm --protocol 4C_charge_45C --thermal lumped --plating`；析锂判定以负极电位 < 0 V 为准
5. **评估**：对照案例配置解析出的达标标准（已写入 log.jsonl 第 0 条）判断达标/不达标；写 `evaluate` 日志条目
   - 不达标：诊断原因并**回退到对应阶段**——材料问题（电位窗/稳定性）回阶段1，结构参数问题回阶段2
6. **收尾（唯一真计算时刻）**：Top-3 候选执行 `run-orca` 背书；Top-1 执行 `run-md` 背书；最后 `render` 生成报告；写 `endorse` 与 `final` 日志条目
   - 若配置 `real_compute: false`：跳过 `run-orca`/`run-md` 真计算背书，`endorse` 条目如实记录跳过（如 `{"action": "endorse", "skipped": true, "reason": "real_compute=false"}`），随后直接 `render`

### log.jsonl 条目 schema（每轮必须按此写入）

追加式，每行一条 UTF-8 JSON（可直接用 `bda.log.append_entry`）：

- **第 0 条（开跑前写一次）**：`{"criteria": {...}}` —— 解析出的达标标准（审计记录，报告首页展示）
- **propose**：`{"action": "propose", "round": 1, "candidates": ["SMILES", ...], "llm_reason": "生成理由"}` —— 每轮候选与决策理由
- **funnel**：`{"action": "funnel", "passed": 3, "rejected": 2, "disputed": 1}` —— 阶段1 漏斗计数（passed/rejected 来自 `filter` 输出，disputed 来自 `consensus` 输出）
- **evaluate**：`{"action": "evaluate", "round": 2, "metrics": {"capacity_ah": ..., "T_max_K": ..., "plated": false, ...}, "verdict": "pass"}` —— metrics 至少含数值键 `T_max_K` 与布尔键 `plated`（报告趋势图与 CSV 导出依赖这两个键）；verdict 取值自由（如 pass/fail），报告原样展示
- **endorse**：`{"action": "endorse", "candidates": [{"smiles": "SMILES", "endorsement": {...}}]}` —— endorsement 对象 = 该候选 `run-orca` 输出的 endorsement 键（Top-1 另附 `run-md` 输出键）
- **final**：`{"action": "final", "recommendation": "最终推荐方案", "verdict": "达标/不达标"}` —— 收尾必写，含"预算耗尽未达标"情形

## 二、评估标准

- 阈值由你从案例目标自然语言解析（`config.yaml` 的 `goal`），解析结果必须写入 log.jsonl 第 0 条后**直接开跑**，不等待人工确认
- 达标判定只看工具输出 JSON 中的数值；任何换算必须由工具输出值机械推导（例：T_max_C = T_max_K − 273.15）
- 各阶段判定要点（内嵌回退规则）：
  - 阶段1：漏斗 `passed` 且 `consensus` 无 `disputed`（或 disputed 经推理改进后一致）
  - 阶段2：`capacity_ah`（1C 放电容量）对照解析目标
  - 阶段3：析锂——`anode_potential_v` 任一值 < 0 V 即 `plated = true`；温升——`T_max_K` 对照解析目标
  - 综合达标 = 阶段 2/3 全部指标满足第 0 条阈值
- 回退路由（不达标时）：材料问题（电位窗不满足/HOMO-LUMO 不稳定/添加剂无效果）→ 回阶段1（换取代基、生成变体或换新候选）；结构/参数问题（容量不足、温升过高但材料指标可接受）→ 回阶段2（调整电芯参数或 bridge props 后重跑）；每轮回退原因写入 `evaluate` 条目的 verdict 或日志
- 预算：轮数上限 = `max_rounds`；预算耗尽仍未达标 → 如实写 `final` 条目（verdict 不达标、recommendation 说明），不得虚构达标
- 消融开关按 `config.yaml` 的 `ablations` 执行：`guardrails: false` → 忽略本协议第三节；`consistency: false` → 跳过 `consensus`；`bridge: false` → 跳过参数桥梁用默认参数
- `real_compute: false` → 收尾跳过 `run-orca`/`run-md` 真计算背书（`endorse` 条目如实记录跳过原因，不得虚构 DFT/MD 数值）

## 三、禁止事项与反模式（铁律）

- ❌ 编造仿真数值：未执行命令不得写出任何指标
- ❌ 跳过筛选层直接真计算：漏斗内禁止 `run-orca`/`run-md`
- ❌ 未达标宣布完成：不达标时必须回退重来，直到达标或预算耗尽
- ❌ 修改 JSON 中间文件内容：只能读取，不得编辑
- ❌ 省略命令：每步命令必须真实执行并读到其输出后才能进入下一步

补充纪律：

- 铁律"不得编辑 JSON 中间文件"指**命令输出产物**（`--out` 文件与工作区产物）只读；Agent 自建的**输入文件**（consensus 合并文件、bridge props、run-md box 等）是新建文件，允许写
- 失败必须如实记录：仿真失败、DFT 未收敛、候选被淘汰——全部原样写入日志与报告，不得美化或隐瞒
- 消融实验只通过 `config.yaml` 的 `ablations` 开关执行，不得在运行中自行增删协议步骤

## 四、仿真库命令用法

### 通用约定

- 调用形式（Bash 工具，仓库根目录）：`.venv\Scripts\python.exe -m bda <子命令> ...`；全部 9 个子命令见 `-m bda --help`
- **必须用 Bash 工具执行仿真与 render 命令**：本环境 PowerShell 工具受 guardrail 限制（`$()` 子表达式、`Set-Location`、`&` 多操作等一律拦截且无法批准），若你只有 PowerShell 工具可用，说明会话工具白名单异常（续跑轮换了 session 即应恢复），先用 Bash 重试
- JSON 即契约：所有输入/输出均为 UTF-8 JSON 文件，`--out` 指定输出路径；每一步可单独重跑
- 报错约定：参数/校验类失败打印 `bda error: <原因>` 到 stderr、退出码 1；输入文件缺失或 JSON 键缺失会以 Python traceback 终止——读输出最后几行定位原因，按提示修正后重跑
- 环境依赖：`run-xtb` 需 xtb 二进制在 PATH；`run-orca` 需 orca 在 PATH；`run-md` 需 gmx 在 PATH 且 `bda/simulators/data/opls/` 有对应 .itp 模板

### 阶段1 合并约定（consensus 输入，预飞裁定）

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

### bridge — 微观物性 → PyBaMM 参数映射

```
bda bridge --props PROPS --out OUT
```

- 输入 `--props`：`{"D_electrolyte_m2_s": 3e-10, "conductivity_S_m": 1.1, "transport_number": 0.4}`（键可只给子集；合法键仅 `D_electrolyte_m2_s`、`conductivity_S_m`、`transport_number`）
- 输出：PyBaMM 参数名 → 值，如 `{"Electrolyte diffusivity [m2.s-1]": 3e-10, "Electrolyte conductivity [S.m-1]": 1.1, "Cation transference number": 0.4}`；可直接作为 `run-pyamm --params` 输入
- 报错：`unknown micro property '<k>'; legal keys: ...` → 修正键名重跑

### filter — 漏斗硬淘汰

```
bda filter --in IN --rules RULES --out OUT
```

- 输入 `--in`：`{"candidates": [{"smiles": "SMILES", "metrics": {...}}]}` —— 用合并文件（见合并约定）
- 输入 `--rules`：`{"max_energy_ev": -1.0, "max_homo_ev": -6.0}`（两键均可选；都不给则只看 converged）
- 规则：`metrics.converged` 非真 → rejected；给了 `max_energy_ev` 而 `energy_ev` 缺失或超限 → rejected；给了 `max_homo_ev` 而 `homo_ev` 缺失或超限 → rejected；否则 passed
- 输出：输入同结构 + 每候选增加 `"status": "passed" | "rejected"`
- 报错：无自定义校验错误；JSON 语法错误 → `bda error: ...`；输入文件不存在 → FileNotFoundError traceback
- 注意：缺少 `converged` 键的输入会被整体淘汰——不要把 `run-xtb` 输出直接喂给 filter

### consensus — 三模型一致性投票

```
bda consensus --in IN --out OUT
```

- 输入 `--in`：`{"candidates": [{"smiles": "SMILES", "metrics": {"mace_energy_ev": f, "chgnet_energy_ev": f, "xtb_homo_ev": f}}]}` —— 合并文件或 `filter` 输出
- 规则：三个键各自升序排名（能量/轨道能越低越优）；某候选三排名 max−min ≥ 阈值 → disputed。阈值为 `max(2, 0.3×候选数)`（候选数 < 3 时原样返回不判定）
- 输出：输入同结构；分歧候选增加 `"status": "disputed"` 与 `"dispute_detail": {"ranks": {"mace_energy_ev": r, "chgnet_energy_ev": r, "xtb_homo_ev": r}}`；未分歧候选不加 status
- 报错：输入 metrics 缺少任一排名键 → KeyError traceback → 检查合并文件键名
- 处置：disputed 候选按第一节第 1 步处理（改进或明确淘汰理由）

### run-pyamm — 电芯仿真

```
bda run-pyamm --params PARAMS --protocol PROTOCOL [--mode MODE] [--thermal THERMAL] [--plating] --out OUT
```

- `--protocol` 合法值：`1C_discharge`（1C 放电，3600 s，298.15 K）；`4C_charge_45C`（4C 充电，900 s，318.15 K）
- `--mode`：`spme`（默认）/ `dfn`；dfn 求解失败自动降级 SPMe 重试（输出 `model_used` 记 `"SPMe(fallback)"`）
- `--thermal`：`lumped`（默认）/ `isothermal`；非 isothermal 时输出含 `T_max_K`
- `--plating`：启用析锂模块（Chen2020 参数集无析锂参数，运行时注入标准默认值），输出含 `anode_potential_v`
- 输入 `--params`：`{"<PyBaMM Chen2020 参数名>": 值}` —— 参数名会被校验，通常直接给 `bridge` 输出
- 输出键：`model_used`、`time_s`、`voltage_v`、`capacity_ah`、`T_max_K`（非 isothermal）、`anode_potential_v`（--plating）
- 报错：
  - `unknown protocol 'x'; legal: ['1C_discharge', '4C_charge_45C']` → 修正协议名
  - `unknown mode 'x'; legal: spme, dfn` → 修正模式名
  - `unknown parameter name(s): ['...']` → 参数名不在 Chen2020 集内；检查 bridge 键与拼写
  - SPMe 求解失败（pybamm.SolverError traceback）→ 该参数组合无效，按第一节第 5 步回退调整

### run-mlp — ML 势结构松弛

```
bda run-mlp --in IN [--model MODEL] --out OUT
```

- `--model`：`mace`（默认）/ `chgnet`
- 输入 `--in`：`{"candidates": [{"smiles": "SMILES"}]}`
- 输出：`{"candidates": [{"smiles": "SMILES", "metrics": {"energy_ev": f, "converged": bool}, "model": "mace"}]}`
- 报错：`invalid SMILES: '...'` → 修正 SMILES；`unknown model 'x'; legal: mace, chgnet` → 修正模型名；`failed to embed 3D structure for ...` → 该 SMILES 无法构象嵌入，换候选
- 使用位置：阶段1，每个模型各跑一次（mace 与 chgnet）

### run-xtb — 半经验量子单点

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

### run-orca — 真 DFT 背书（仅收尾 Top-3）

```
bda run-orca --in IN --out OUT
```

- 输入 `--in`：`{"candidates": [{"smiles": "SMILES"}]}`
- 输出：`{"candidates": [{"smiles": "SMILES", "endorsement": {"E_hartree": f, "homo_ev": f, "lumo_ev": f, "ie_ev": f, "ea_ev": f}}]}` —— ie_ev/ea_ev 为垂直电离能/电子亲和能（电压窗口代理）
- 每个候选跑中性/阳离子/阴离子三次单点（r2SCAN-3c），每分子最多重试 3 次；CPU 慢（每分子约 2~3 小时），只在收尾执行，禁止在漏斗内使用
- 报错：
  - `ORCA binary not found; download academic Windows build from the ORCA forum` → 安装 ORCA 并加入 PATH
  - `ORCA failed after 3 attempts for <smiles> (DFT not converged): ...` → 如实记录"该候选 DFT 未收敛"，不得伪造数值

### run-md — 真 MD 扩散背书（仅收尾 Top-1）

```
bda run-md --box BOX [--t-ns T_NS] --out OUT
```

- 输入 `--box`：`{"molecules": {"EC": 60, "EMC": 40, "PF6": 10, "Li": 10}}`（Li 至少 1；`t_ns` 可内嵌，`--t-ns` 默认 10.0）
- 输出：`{"D_Li_m2_s": f, "trajectory_ok": bool, "drift_check": "ok"|"drift"|"skipped", "achieved_density_g_cm3": f}` —— `trajectory_ok: false`（drift）时如实记录并报告
- 报错：
  - `GROMACS not found; install via winget install GROMACS.GROMACS or conda` → 安装 GROMACS
  - `box must contain at least 1 Li` → box 至少 1 个 Li
  - `missing OPLS-AA .itp template(s): ...` → 按 `bda/simulators/data/opls/README.md` 生成对应 .itp 模板
  - `gmx mdrun failed: ...` / `gmx trjconv failed: ...` → 按 stderr 尾部内容排查

### render — HTML 报告

```
bda render --case-dir CASE_DIR [--out OUT]
```

- 读取 `<case_dir>/log.jsonl`（第 0 条 criteria + 全部 action 条目），产出自包含 HTML（任务概览/迭代轨迹/漏斗统计/阶段 2/3 结果/收尾背书/最终推荐 六节），写入 `<case_dir>/<out>`（默认 `report.html`）
- 无 log.jsonl → 渲染空报告；无对应条目 → 该节显示"暂无数据"
- 报错：无自定义校验；log 行 JSON 解析失败 → traceback 指出行号
- 使用位置：收尾最后一步；报告全部内容由 log.jsonl 确定性生成，无额外 LLM 调用
