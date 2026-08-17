# 虚拟电池工厂（Virtual Battery Factory）

LLM Agent 驱动的跨尺度虚拟电池设计平台——材料基因 → 电池性能的自动翻译层：在纯软件仿真环境中完成"材料设计 → 电芯设计 → 安全评估"闭环，全程不依赖物理实验。

- 设计文档（20 项锁定决策、架构、消融矩阵）：[docs/superpowers/specs/2026-08-15-virtual-battery-factory-design.md](docs/superpowers/specs/2026-08-15-virtual-battery-factory-design.md)
- 实施计划：[docs/superpowers/plans/2026-08-15-virtual-battery-factory.md](docs/superpowers/plans/2026-08-15-virtual-battery-factory.md)

## 入口与结构

- **主入口 `run.py`**（仓库根）：Agent SDK 薄启动器——加载协议 skill（`.claude/skills/virtual-battery-factory/SKILL.md`）全文注入系统提示，经内置 Bash 工具驱动仿真库 `python -m bda` 跑设计闭环。**不注册任何自定义工具**。
- 协议 skill 自包含于 `.claude/skills/virtual-battery-factory/`：`SKILL.md`（协议）+ `references/cli-commands.md`（命令文档）+ `scripts/bda/`（仿真库，pip editable 安装映射）+ `assets/cases/`（样例案例）。环境缺失时按协议第 0 步由 Agent 自行安装。

## 安装

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".claude/skills/virtual-battery-factory/scripts[dev,ml,host]"
```

外部二进制（仅收尾真计算背书需要；各 runner 以 `PATH` 查找可执行文件，装好目录加入 `PATH` 即可）：

| 二进制 | 用途 | 安装来源 |
|---|---|---|
| xtb | 半经验量子单点（漏斗粗排） | [github.com/grimme-lab/xtb/releases](https://github.com/grimme-lab/xtb/releases)（Windows zip，解压目录含 `xtb.exe`） |
| ORCA | 真 DFT 收尾背书（Top-3，CPU 挂夜） | [faccts.de/orca](https://www.faccts.de/orca/)（学术免费许可，解压目录含 `orca.exe`） |
| GROMACS | 真 MD 收尾背书（Top-1） | [gromacs.org/Downloads](https://www.gromacs.org/Downloads) 或 `winget install GROMACS.GROMACS`（`bin` 目录含 `gmx.exe`） |

ML 势（MACE-MP/CHGNet）由 pip `[ml]` 附带，无需额外二进制。`real_compute: false` 的案例（如冒烟案例）不依赖上述任何二进制。

### 环境引导（密钥不落盘）

运行前在项目根目录创建 `.env`：`DEEPSEEK_API_KEY=<你的 key>`。启动时 `run.py` 按序引导（全部可被已存在的环境变量覆盖）：

| 变量 | 缺省值 | 说明 |
|---|---|---|
| `ANTHROPIC_BASE_URL` | `https://api.deepseek.com/anthropic` | Anthropic 兼容端点（DeepSeek 官方提供）；指向其他代理时覆盖 |
| `ANTHROPIC_MODEL` | `deepseek-v4-pro` | 模型名 |
| `ANTHROPIC_AUTH_TOKEN` | 取 `.env` 的 `DEEPSEEK_API_KEY` | 凭证；已有 `ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_API_KEY` 则不再读 `.env` |

密钥只注入子进程环境变量，不写入任何文件、不打印。连通性冒烟：`.venv\Scripts\python.exe run.py --smoke-test`（单次 query 返回 `smoke ok` 即通；无凭证时测试自动 skip）。

## 运行

**用户唯一输入 = 自然语言**，全程无需手写或查看任何 YAML。在 Claude Code 对话里直接说设计目标即可（如"设计一款能量密度 ≥ 400 Wh/kg 且 4C 快充无析锂的电池"）：

1. skill 用 AskUserQuestion 逐项澄清（目标量化 / 起点判定（是否从阶段 2 开始）/ 体系 / 预算 / 消融 / 真计算开关，均带默认值）
2. 澄清后 skill 自动生成配置、写入工作区并执行闭环
3. 批量实验同样用自然语言发起："跑 N=3"、"跑消融矩阵"、"关掉 guardrails 跑一次"——skill 生成各变体配置并依次以 `run.py` 挂夜执行

样例设计目标（自然语言示例与推荐设置，也是澄清时的默认值来源）见 `.claude/skills/virtual-battery-factory/assets/examples.md`，共五类：快充/析锂添加剂、电压窗口拓宽、能量密度目标驱动（以上全流程）、结构参数优化（从阶段 2 开始）、最小冒烟（真计算关）。

收尾 Top-3 `run-orca` + Top-1 `run-md` 真计算背书（挂夜，约一夜一案例）。**工作区 = 配置所在目录**（`log.jsonl`、`session_id`、`report.html`、`csv/` 及各阶段产物子目录均落在此处）；resume：重跑同一条命令即自动续跑（session id 持久化在工作区 `session_id` 文件，删除该文件则从零开始新会话）。

## 消融实验

全部通过案例配置开关执行，不改代码（各开关回答的问题对照设计文档 §10.1）。开关含义（澄清时作为选项呈现，或直接对 skill 说）：

| 开关 | 关闭时回答的问题 |
|------|----------------|
| `guardrails: false` | 反模式护栏（SKILL.md 第三章）贡献多少？ |
| `consistency: false` | 三模型一致性检查贡献多少？ |
| `bridge: false` | 参数桥梁（微观结果不回流，用默认文献参数）贡献多少？ |

三个开关全 `true` 即完整系统（主结果）。论文消融矩阵 7 组 × N=3、一夜一组约 3 周（设计文档 §10）；`runs/<case_id>/csv/` 汇总各案例图表数据绘制论文图表。

## 报告

收尾自动生成自包含 HTML 报告（任务概览 → 迭代轨迹 → 漏斗统计 → 阶段 2/3 结果 → 真计算背书 → 最终推荐），浏览器直接打开工作区的 `report.html`（`runs/<case_id>/` 布局下即 `runs/<case_id>/report.html`）。

## 测试

```powershell
# 快速测试（跳过慢测试）
.venv\Scripts\python.exe -m pytest -m "not slow"

# 全量（含各 runner 慢冒烟：PyBaMM / MACE-MP / xTB / ORCA / MD，无对应二进制时自动跳过）
.venv\Scripts\python.exe -m pytest
```
