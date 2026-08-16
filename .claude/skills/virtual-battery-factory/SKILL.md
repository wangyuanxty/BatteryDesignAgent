---
name: virtual-battery-factory
description: 虚拟电池工厂协议——三阶段电池设计闭环（材料→电芯→安全）加评估回退控制环。当用户要求设计电解液/添加剂并运行案例时使用。
---

# 虚拟电池工厂协议

你是电池设计智能体。你自带电化学领域知识；本协议只规定**流程、边界与反模式**，以及仿真库命令用法。所有结论级数值必须来自工具输出文件，不得凭记忆编造。

本 skill 的目录结构：`SKILL.md`（本协议）＋ `references/cli-commands.md`（仿真库命令完整参考，需要参数细节/IO 结构/报错处置时用 Read 读取）＋ `scripts/bda/`（仿真库 Python 包，pip editable 安装映射至此）。

## 一、任务流程（线性，无阶段 4）

### 准备（每案例一次）

0. **环境自检与自装**（每次会话开始先做）：
   - 检查 `.venv\Scripts\python.exe -c "import bda"` 能否成功；能 → 跳过本步
   - 不能 → 自己安装环境（Bash 执行，勿等用户）：仓库根有 `pyproject.toml` 时建虚拟环境并 `pip install -e ".[dev,ml,host]"`；仅拿到本 skill 文件夹（无仓库）时改为 `pip install -e <本skill目录>/scripts`（scripts/ 内有独立 pyproject.toml）。ml 额外依赖（torch/mace-torch/chgnet）体积大，按阶段 1 需要再装亦可，但收尾 run-md 的 mace 引擎必须有 mace-torch
   - 外部二进制（xtb/orca/gmx）不在 pip 范围：缺失时对应命令会给出安装指引，按指引装或如实记录跳过
1. 读取案例配置（字段：`goal` 设计目标、`system` 材料体系、`max_rounds` 迭代预算、`seed_pool` 种子池、`ablations` 消融开关、`base_params` 参数集、`real_compute` 真计算开关）。配置与工作区路径以系统提示注入的 `配置:` / `工作区:` 字段为准（Agent SDK 启动器注入，工作区=配置所在目录；`runs/<case_id>/` 仅为无注入时的默认布局）。
2. 若 `log.jsonl` 已存在（续跑/resume）：从最后一条记录恢复状态，不重复执行已完成步骤（以产物文件存在为准）。
3. 从 `goal` 自然语言解析达标标准（指标名、阈值、单位），写入 `log.jsonl` 第 0 条后直接开跑。

对每个候选分子严格执行：

1. **阶段1 材料设计**（快环，零真计算）：生成候选（`seed_pool` + 自由生成）→ `run-mlp --model mace` → `run-mlp --model chgnet` → `run-xtb` → 按合并约定建 consensus 输入 → `filter`（漏斗硬淘汰）→ `consensus`（三模型一致性投票）
   - 写 `propose` 与 `funnel` 日志条目
   - `consensus` 返回 `disputed` 的候选：不得淘汰即止，须推理改进（换取代基/生成变体）或明确给出淘汰理由后换新候选
2. **参数桥梁**：对通过候选执行 `bridge`，产出 PyBaMM 参数更新（props 数值来源写入日志）
   - props 数值来源规则：种子池候选用文献值（在日志中标注引用来源）；自由生成候选用领域估计值（标注 `estimate`）；来源必须写入日志；估计值不得冒充仿真输出——收尾时若该候选进入 Top-N，其 D/σ 由真 MD/文献背书复核
3. **阶段2 电芯设计**：`run-pyamm --base <案例配置 base_params> --protocol 1C_discharge --mode spme`，随后按需 `--mode dfn`
4. **阶段3 安全评估**：`run-pyamm --base <案例配置 base_params> --protocol 4C_charge_45C --thermal lumped --plating`；析锂判定以负极电位 < 0 V 为准
5. **评估**：对照案例配置解析出的达标标准（已写入 log.jsonl 第 0 条）判断达标/不达标；写 `evaluate` 日志条目
   - 不达标：诊断原因并**回退到对应阶段**——材料问题（电位窗/稳定性）回阶段1，结构参数问题回阶段2
6. **收尾（唯一真计算时刻）**：Top-3 候选执行 `run-orca` 背书；Top-1 执行 `run-md` 背书；最后 `render` 生成报告；写 `endorse` 与 `final` 日志条目
   - 若配置 `real_compute: false`：跳过 `run-orca`/`run-md` 真计算背书，`endorse` 条目如实记录跳过（如 `{"action": "endorse", "skipped": true, "reason": "real_compute=false"}`），随后直接 `render`

### log.jsonl 条目 schema（每轮必须按此写入）

追加式，每行一条 UTF-8 JSON（格式与 `bda.log.append_entry` 写入一致）：

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

## 四、仿真库命令速查

调用形式（Bash 工具，仓库根目录）：`.venv\Scripts\python.exe -m bda <子命令> ...`。**完整参数/IO 结构/报错处置见 `references/cli-commands.md`（需要细节时用 Read 读取）**——特别是阶段1的合并约定与 run-pyamm 的 `--base` 传参规则，首次运行前必读。

| 子命令 | 用途 | 使用位置 |
|--------|------|---------|
| `run-mlp --in IN [--model mace\|chgnet] --out OUT` | ML 势结构松弛（能量/收敛） | 阶段1，mace 与 chgnet 各一次 |
| `run-xtb --in IN --out OUT` | 半经验单点（HOMO/LUMO） | 阶段1 |
| `filter --in IN --rules RULES --out OUT` | 漏斗硬淘汰（converged/能量/HOMO 淘汰线） | 阶段1 |
| `consensus --in IN --out OUT` | 三模型一致性投票（分歧标记 disputed） | 阶段1 |
| `bridge --props PROPS --out OUT` | 微观物性 → PyBaMM 参数映射 | 参数桥梁 |
| `run-pyamm --params P --protocol X [--base B] [--mode M] [--thermal T] [--plating] --out O` | 电芯仿真（放电/快充/热/析锂，DFN 自动降级） | 阶段2/3 |
| `run-orca --in IN --out OUT` | 真 DFT 背书（气相优化+HOMO/LUMO+IE/EA） | 仅收尾 Top-3 |
| `run-md --box B [--engine gromacs\|mace] [--t-ns T] --out O` | 真 MD 扩散背书（MSD→D，漂移检测） | 仅收尾 Top-1 |
| `render --case-dir D [--out O]` | log.jsonl → 自包含 HTML 报告（六节） | 收尾最后一步 |

通用纪律（细节见 references）：同参数必复用（run-* 先查 `--out` 同目录 `cache/`）；`bda error: ...` 到 stderr + 退出码 1 = 参数/校验失败，读原因修正重跑；必须用 Bash 工具执行（PowerShell 受 guardrail 限制）。
