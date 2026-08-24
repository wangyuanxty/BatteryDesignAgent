# 仿真库 CLI 完整参考（`python -m bda`）

> 由 SKILL.md 第四章指引按需读取。仿真库包位于本 skill 的 `scripts/bda/`（pip 以 editable 安装映射至此，`python -m bda` 即调用它）。

## 通用约定

- 调用形式（Bash 工具，仓库根目录）：`.venv\Scripts\python.exe -m bda <子命令> ...`；全部 7 个子命令见 `-m bda --help`
- 参数桥梁为协议规则（PyBaMM 参数名映射表见 SKILL.md 第一节第 2 步），无对应 CLI 命令。
- **必须用 Bash 工具执行仿真与 render 命令**：本环境 PowerShell 工具受 guardrail 限制（`$()` 子表达式、`Set-Location`、`&` 多操作等一律拦截且无法批准），若你只有 PowerShell 工具可用，说明会话工具白名单异常（续跑轮换了 session 即应恢复），先用 Bash 重试
- JSON 即契约：所有输入/输出均为 UTF-8 JSON 文件，`--out` 指定输出路径；每一步可单独重跑
- 同参数必复用（spec 5.2 不变式 3）：所有 `run-*` 命令先查 store 缓存，命中直接复用不重算。缓存目录 = `--out` 文件所在目录下的 `cache/`（键 = 命令参数组合：run-pyamm: params+protocol+base+mode+thermal+plating；run-mlp: smiles+model；run-xtb: smiles；run-orca: smiles+charge+mult+functional；run-md: box+t_ns+engine；run-comp: candidates）。缓存文件损坏（非法 JSON / 非对象）按未命中处理并重写
- 报错约定：参数/校验类失败打印 `bda error: <原因>` 到 stderr、退出码 1；输入文件缺失或 JSON 键缺失会以 Python traceback 终止——读输出最后几行定位原因，按提示修正后重跑
- 环境依赖：`run-xtb` 需 xtb 二进制在 PATH；`run-orca` 需 orca 在 PATH；`run-md` 需 gmx 在 PATH 且 skill 内 `scripts/bda/simulators/data/opls/` 有对应 .itp 模板

## 阶段2 漏斗判定（无对应 CLI 命令）

漏斗判定（硬淘汰线 + 三模型异质投票）由协议规则执行，见 SKILL.md 第一节第 1 步——依次真实执行 `run-mlp --model mace`、`run-mlp --model chgnet`、`run-xtb`（同一候选清单）后，直接读取三次输出 JSON 判定，无对应 CLI 命令、无需合并文件。

## run-pyamm — 电芯仿真

```
bda run-pyamm --params PARAMS --protocol PROTOCOL [--base BASE] [--mode MODE] [--thermal THERMAL] [--plating] [--cycles N] --out OUT
```

- `--base`：PyBaMM 参数集名（默认 `Chen2020`）；**案例配置的 `base_params` 字段必须原样传给 `--base`**（如 `--base ORegan2022`）。参数桥梁映射表（SKILL.md 第一节第 2 步）的参数名为跨参数集共享名（`Electrolyte diffusivity [m2.s-1]` 等），故 `--params` 可直接配合任一参数集使用
- `--protocol` 合法值：
  - `1C_discharge`（1C 放电，3600 s，298.15 K）
  - `4C_charge_45C`（4C 充电，900 s，318.15 K）
  - `5C_discharge`（5C 高倍率放电，720 s——倍率场景；**高倍率建议 `--mode dfn`**，SPMe 在 5C 下严重低估容量）
  - `lowT_discharge`（1C 放电，-20 ℃/253.15 K——低温场景）
  - `overcharge`（先 1C 放至下限，再 0.5C 充至上限+0.5 V——过充场景，输出含 T_max_K）
  - `aging_1C_100cyc`（100 圈 1C 恒流充放，SEI ec reaction limited + isothermal，电压上下限取参数集自身值）
  - `aging_1C_100cyc_45C`（同上，但 45 ℃/318.15 K 高温老化）
- `--cycles`：覆盖老化协议圈数（默认 100）
- `--mode`：`spme`（默认）/ `dfn`；dfn 求解失败自动降级 SPMe 重试（输出 `model_used` 记 `"SPMe(fallback)"`）
- `--thermal`：`lumped`（默认）/ `isothermal`；非 isothermal 时输出含 `T_max_K`。老化协议内部固定 isothermal，`--thermal`/`--plating` 被忽略
- `--plating`：启用析锂模块（Chen2020 参数集无析锂参数，运行时注入标准默认值），输出含 `anode_potential_v`
- 输入 `--params`：`{"<PyBaMM 参数名>": 值}` —— 参数名会按所选参数集校验，通常按 SKILL.md 第一节第 2 步的参数名映射表书写
- 输出键：`model_used`、`time_s`、`voltage_v`、`capacity_ah`、`T_max_K`（非 isothermal）、`anode_potential_v`（--plating）；老化协议输出 `model_used`、`protocol: "aging"`、`cycle_numbers`、`capacity_ah_per_cycle`、`sei_thickness_nm_end`
- 报错：
  - `unknown protocol 'x'; legal: [...]` → 修正协议名
  - `unknown mode 'x'; legal: spme, dfn` → 修正模式名
  - `unknown parameter name(s): ['...']` → 参数名不在所选参数集内；对照 SKILL.md 第一节第 2 步的映射表检查键名与拼写
  - `base parameter set has no 'SEI kinetic rate constant [m.s-1]'; ...` → 所选体系无老化模型（如 ORegan2022）；老化协议只能用带 SEI 参数的老化体系（Chen2020/OKane2022 等），无老化模型时如实记录 N/A
  - SPMe 求解失败（pybamm.SolverError traceback）→ 该参数组合无效，按 SKILL.md 第一节第 5 步回退调整
- 老化协议注意事项：容量轨迹在标准 SEI 模型下可能出现先爬升后饱和的非单调伪影（锂损失导致电压窗口偏移）——报告/评估中如实标注，不得当作正常衰减；包覆/掺杂与基线须在同一体系上对比

## run-mlp — ML 势结构松弛

```
bda run-mlp --in IN [--model MODEL] --out OUT
```

- `--model`：`mace`（默认）/ `chgnet`
- 输入 `--in`：`{"candidates": [{"smiles": "SMILES"}]}`
- 输出：`{"candidates": [{"smiles": "SMILES", "metrics": {"energy_ev": f, "converged": bool}, "model": "mace"}]}`
- 报错：`invalid SMILES: '...'` → 修正 SMILES；`unknown model 'x'; legal: mace, chgnet` → 修正模型名；`failed to embed 3D structure for ...` → 该 SMILES 无法构象嵌入，换候选
- 使用位置：阶段2，每个模型各跑一次（mace 与 chgnet）

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

- 读取 `<case_dir>/log.jsonl`（第 0 条 criteria + 全部 action 条目），产出自包含 HTML（任务概览/迭代轨迹/漏斗统计/阶段结果/真DFT/MD 验证背书/最终推荐/设计说明 七节），写入 `<case_dir>/<out>`（默认 `report.html`）
- 无 log.jsonl → 渲染空报告；无对应条目 → 该节显示"暂无数据"
- 报错：无自定义校验；log 行 JSON 解析失败 → traceback 指出行号
- 使用位置：收尾最后一步；报告全部内容由 log.jsonl 确定性生成，无额外 LLM 调用

## run-comp — 电极组分筛选（CHGNet 周期弛豫）

```
bda run-comp --in IN --out OUT
```

- **环境要求**：CUDA 版 torch（GPU 弛豫 ~20 秒/状态）；CPU 版 torch 弛豫不收敛（已实测）。本机 `.venv` 为 CPU torch，用 `D:/anaconda/envs/py312/python.exe -m bda run-comp ...`（py312 已装 chgnet/pymatgen/ase + torch 2.13.0+cu126）
- 输入 `--in`：`{"candidates": [{"formula": "Li(Ni0.7Mn0.05Co0.05Si0.1Mg0.1)O2", "name": "NMC-SiMg"}]}` —— NMC811 晶格位点替换，TM 分数和须为 1
- 输出：`{"baseline": {NMC811 能量 + Li 金属参考}, "candidates": [{formula, realized_tm_counts, avg_voltage_v, capacity_mah_g, e_full_ev, e_delith_ev, converged, rel_stability_ev_atom}], "calibration_note"}`
- 口径（如实声明，写入报告）：
  - 平均电压 = −[E(Li_x2)−E(Li_x1)−n_removed·E_Li]/n_removed（x∈[0.3,1]，含 Li 金属参考；NMC811 自校准 ≈3.82 vs 文献 3.8 V）
  - 容量 = 0.7 Li × F/3.6 ÷ 摩尔质量（理论代理，NMC811 ≈194 mAh/g）
  - `rel_stability_ev_atom` 仅看批内相对排序（弛豫未严格收敛，同一组分两次弛豫能量差可达 ~1 eV/atom）
  - `converged=false` 常见（300 步 FIRE 未达 fmax 0.1）——能量已达筛选精度，如实标注
  - 真背书：收尾用 `run-qe`（周期 DFT，见下节）——漏斗内一律为 CHGNet 代理口径
- 报错：`TM fractions must sum to 1` → 修组分；`no transition-metal species` → 公式缺少 TM

## run-qe — 周期 DFT 真背书（仅收尾 Top 组分）

```
bda run-qe --in IN --out OUT
```

- **环境**：MSYS2 的 QE（原生 Windows，非虚拟机）：`winget install MSYS2.MSYS2`，改 pacman 镜像（TUNA，见安装备注），`pacman -S mingw-w64-ucrt-x86_64-quantum-espresso`，pw.exe 在 `C:\msys64\ucrt64\bin\`；赝势用 conda-forge `sssp` 包目录（`D:\anaconda\envs\py312\share\sssp\efficiency`，可用环境变量 `QE_PSEUDO_DIR` 覆盖）
- **两个已踩坑（本机已处理，勿重蹈）**：① MSYS2 原版 pw.exe 栈保留仅 2MB，计算初始化即栈溢出（0xC00000FD）——需用 pefile 打补丁复制为 `pw_stack4g.exe`（栈保留 4GB），runner 自动优先使用；② Fortran namelist 中反斜杠是转义符——runner 生成输入时已自动把 Windows 路径转正斜杠
- 输入 `--in`：`{"candidates": [{"formula": "Li(Ni0.8Mn0.1Co0.1)O2", "name": "NMC811"}]}`
- 输出：每候选 `{formula, realized_tm_counts, avg_voltage_v, e_full_ev, e_delith_ev, e_li_metal_ev, converged, wall_time_s}` —— 电压公式与 run-comp 一致（含 Li 金属参考）
- 计算口径：ecutwfc 50 Ry / ecutrho 400（SSSP efficiency 标准）；nspin=2 铁磁初猜（Ni/Mn/Co）；满锂 vc-relax + 去锂固定晶胞 relax + bcc Li vc-relax；CPU 小时级（12 原子原胞 ~1 小时/态、48 原子超胞挂夜）——**仅收尾执行，漏斗内禁止**（同 run-orca 铁律）
- 报错：
  - `pw.x not found; install MSYS2 ...` → 按指引装 MSYS2 的 quantum-espresso 包
  - `QE pseudopotential dir not found; ...` → 装 conda-forge sssp 包或设 QE_PSEUDO_DIR
  - `no SSSP efficiency pseudopotential entry for element X` → 该元素不在内置赝势表（Li/Ni/Mn/Co/O/Si/Mg），补 _PSEUDO_FILES 映射
  - `pw.x produced no total energy for ...` → 读工作目录 *.out 排查（SCF 不收敛常见：加 mixing_beta/换初始磁矩）

## log-evaluate — 评估落条目（verdict/evidence 机械判定）

```
bda log-evaluate --case-dir D --round N --outputs F... [--candidate 名] [--note 诊断]
```

- **为什么存在**：v3 事故——agent 在对话里评估 V1-V3（数值都真实）却从不落日志，报告轮卡片 propose-only 却引用"第 1 轮结论"。本命令把"评估发生 → 条目存在"变成机械保证：verdict 由代码对照第 0 条 criteria 计算，agent 不得手写 verdict、不得自行 append_entry 写 evaluate
- **前置**：`--case-dir` 的 log.jsonl 必须有第 0 条 criteria（开跑前预注册）；缺失 → `bda error` + 退出码 1（不可判定的评估直接拒绝）
- **输入 `--outputs`**：仿真输出 JSON 文件路径（`--case-dir` 相对、仓库根相对或绝对均可），多个可并列；标量键（int/float/bool）全部提取进 `metrics`（后文件覆盖前文件）
- **plated 自动推导**：输出无 `plated` 键但含 `anode_potential_v` 时序 → `min < 0` 判定析锂，evidence 来源标注 `anode_potential_v (min=X.XXXV<0 推导)`——与人工判定口径一致
- **verdict 规则**：阈值形态 `{"min": n}`（大于等于）/ `{"max": n}` / 布尔等值 / 标量（视为 min）；已检查指标全部通过 → `pass`，否则 `fail`；输出缺某 criteria 指标 → 记 `unchecked` 并在 note 追加"未检查 criteria: ..."（阶段未到属合法缺失，verdict 按已检查指标判定）
- **输出条目**：`{"action": "evaluate", "round": N, "metrics": {...标量}, "verdict": "pass"|"fail", "evidence": [{"metric", "value", "threshold", "verdict", "source": "文件:键"}, ...], "candidate"?, "unchecked"?, "note"?}`——evidence 来源为 case 相对路径（审计日志跨机器可重放）
- **同轮多候选**：每个被评估的候选落一条（同 round 多次调用，`--candidate` 区分）；报告按 round 合并展示
- **报错**：
  - `log.jsonl 第 0 条 criteria 未找到` → 先写 criteria 再评估
  - `输出文件不存在：...` → 检查路径（相对 case-dir 的 cell/ 目录）
  - `输出文件中没有任何 criteria 指标` → 输出文件键与 criteria 完全不匹配，检查是否传错了文件
  - 阈值 dict 有边界但 value 非数值 → 判 fail（不可判形态一律不过，宁可 fail 不可假 pass）

## verify-deliverables — 交付物协议合规检查

```
bda verify-deliverables --case-dir D
```

- **检查项（全部机械判定）**：① 7 类交付物齐全（design_spec/bom/datasheet/calc/dvpr/dfmea/delivery_index，每类源文件 + PDF 发布版）② PDF 非空（>1KB）③ xlsx 可解析且无空 sheet ④ delivery_index 含 VBF 编号清单（≥5 个）⑤ **审计链完整：每个 propose 轮必须有同 round 的 evaluate 条目**（log-evaluate 协议前提——评估发生却不落日志，报告结论无审计背书）
- **输出**：逐项 `[PASS]/[FAIL]` + 汇总 `ALL PASS`/`HAS FAILURES`；退出码 0/1
- **报错处置**：FAIL 即协议未满足，按 detail 修正后重跑（如"缺评估的 propose 轮: R01" → 补 log-evaluate 落条目）；`log.jsonl 缺失` → 协议运行必须有日志

## calc-energy — 合同口径能量密度（所有任务共用同一公式）

```
bda calc-energy --sim S [--params P] [--base B] --out O
```

- **公式（合同口径，杜绝跨任务抄先例）**：`ED = ∫V·I_1C dt / Σ(层厚×(1−孔隙率)×密度×面积)`
  - 放电能量 = `voltage_v`×`time_s` 的梯形积分 × I_1C，÷3600 得 Wh；I_1C = `Nominal cell capacity [A.h]` × 1（恒流）
  - 面积 = `Electrode height [m]` × `Electrode width [m]`
  - 层：正/负极活性层（乘孔隙率因子）、正/负集流体（无孔隙因子）、隔膜——全部由 `--base`（默认 Chen2020）或 `--params` 覆盖的参数集取值
  - **电解液不计入质量**（参数集缺密度）——输出 `electrolyte_included: false` 如实标注
- **输入**：`--sim` = 放电仿真输出 JSON（必须含 `voltage_v` 列表、`time_s` 列表、`capacity_ah` 标量）；`--params` 可选，覆盖参数集（run-pyamm 用的同款 params 文件）
- **输出**：`{capacity_ah, energy_wh, mass_kg, energy_density_wh_kg, volume_m3, energy_density_wh_l, thickness_m, midpoint_voltage_v, dcr_ohm, power_density_w_kg, layer_kg_m2（各层 kg/m²）, area_m2, electrolyte_included: false, note}`
  - `energy_density_wh_l` = 能量/体积（体积 = Σ层厚×面积，合同口径不含电解液/外壳）
  - `midpoint_voltage_v` = 放电时间中点电压（平台电压近似）；`dcr_ohm` = 直流内阻（起始 OCV 与 10% 放电处压差 ÷ I_1C）；`power_density_w_kg` = V_OC²/(4·DCR) ÷ 质量
  - 判定与报告都以此文件的 `energy_density_wh_kg` 为准
- **报错**：`bda error: ...` + 退出码 1——参数键缺失（`KeyError`）、`--sim` 不是合法 JSON、数值类型不符；先查 `--sim` 是否指向 1C 放电输出、`--base` 是否有对应键

## run-tr — 热失控三副反应 ODE（阶段4 滥用场景）

```
bda run-tr [--sim S] [--t-init T] [--x0 X] [--t-max T] [--mcp M] [--hA H] [--t-amb T] [--q-nail W] --out OUT
```

- **模型**：零维集总热平衡 + 三副反应 Arrhenius 动力学（SEI 分解 / 负极-电解液 / 正极-电解液），scipy BDF 刚性积分；反应物一次消耗保证能量守恒（T_max 有界）
- **触发判定（机械）**：dT/dt > 1 K/s（温升拐点）或 T ≥ 573 K（300℃ 红线）→ `triggered: true` + `trigger_time_s`
- **过充→热失控自动耦合**：`--sim` 传 run-pyamm 输出（如 overcharge 协议），自动读取其 `T_max_K` 作为初始温度
- **针刺**：`--q-nail` 短路产热源（W）
- **输出键**：`triggered`、`trigger_time_s`、`T_max_K`、`T_final_K`、`dTdt_max_K_s`、`T_series_K`、`t_series_s`、`params`
- **报错**：`--sim` 文件缺 `T_max_K` 键 → 应传 run-pyamm 输出 JSON

## run-cp2k — 分子真 DFT 交叉验证（仅收尾 Top-3，可选）

```
bda run-cp2k --in IN --out OUT
```

- **与 run-orca 同构输出**（同一批分子两套独立程序结果对照，消除程序实现差异的疑虑）：`{"candidates": [{"smiles": ..., "endorsement": {E_hartree, homo_ev, lumo_ev, ie_ev, ea_ev, converged}}]}`——`ie_ev`/`ea_ev` 为阳/阴离子态在中性优化几何上的**垂直**单点值（与 run-orca 口径一致）
- **方法**：PBE + D3(BJ) 色散校正、DZVP-MOLOPT-SR-GTH 短程基组 + GTH-PBE 赝势（H/C/O/F/N/S/P/B/Li）、20 Å 真空盒孤立分子（PERIODIC NONE + Poisson MT）；中性态 GEO_OPT，离子态 ENERGY 单点
- **环境**：MSYS2 `pacman -S mingw-w64-ucrt-x86_64-cp2k`；数据文件 `C:\cp2k-data`（BASIS_MOLOPT/GTH_POTENTIALS/dftd3.dat，从 cp2k/cp2k GitHub data/ 下载，可用环境变量 `CP2K_DATA_DIR` 覆盖）
- **两个已踩坑（runner 已自动处理）**：① MSYS2 原版 cp2k.ssmp.exe 栈保留 2MB，大分子初始化即溢出——runner 自动优先用 pefile 补丁版 `cp2k_stack4g.exe`；② DBCSR 在 SCF 启动时直读 `/proc/self/statm`（Windows CRTL 无路径翻译）——runner 自动在 `C:\proc\self\statm` 放静态页面数文件，且经 MSYS2 bash 执行、OMP_NUM_THREADS 限 8（32 线程易内存吃满崩溃）、OMP_STACKSIZE 512M
- **代价**：CPU 分钟级/小分子（FEC 级 10 原子 ≈ 15-40 分钟/分子）——**仅收尾 Top-3 执行，漏斗内禁止**（同 run-orca 铁律；`real_compute: false` 时跳过）
- **报错**：
  - `cp2k not found; install: ...` → 按指引装 MSYS2 的 cp2k 包
  - `CP2K data dir not found; ...` → 下载数据文件到 `C:\cp2k-data` 或设 CP2K_DATA_DIR
  - `invalid SMILES: ...` / `failed to embed 3D structure ...` → RDKit 无法解析/生成构象，检查 SMILES
  - `cp2k produced no total energy` → 读工作目录 *.out 排查（SCF 不收敛常见：加大 EPS_SCF 容差或 MAX_SCF）
  - 单候选失败不中断整体：该候选输出 `{"smiles": ..., "error": "..."}`，其余候选正常返回
