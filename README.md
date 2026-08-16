# 虚拟电池工厂（Virtual Battery Factory）

LLM Agent 驱动的跨尺度虚拟电池设计平台——材料基因 → 电池性能的自动翻译层：在纯软件仿真环境中完成"材料设计 → 电芯设计 → 安全评估"闭环，全程不依赖物理实验。

- 设计文档（20 项锁定决策、架构、消融矩阵）：[docs/superpowers/specs/2026-08-15-virtual-battery-factory-design.md](docs/superpowers/specs/2026-08-15-virtual-battery-factory-design.md)
- 实施计划：[docs/superpowers/plans/2026-08-15-virtual-battery-factory.md](docs/superpowers/plans/2026-08-15-virtual-battery-factory.md)
- 协议层宿主细节：[host/README.md](host/README.md)

## 安装

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev,ml,host]"
```

外部二进制（仅收尾真计算背书需要；各 runner 以 `PATH` 查找可执行文件，装好目录加入 `PATH` 即可）：

| 二进制 | 用途 | 安装来源 |
|---|---|---|
| xtb | 半经验量子单点（漏斗粗排） | [github.com/grimme-lab/xtb/releases](https://github.com/grimme-lab/xtb/releases)（Windows zip，解压目录含 `xtb.exe`） |
| ORCA | 真 DFT 收尾背书（Top-3，CPU 挂夜） | [faccts.de/orca](https://www.faccts.de/orca/)（学术免费许可，解压目录含 `orca.exe`） |
| GROMACS | 真 MD 收尾背书（Top-1） | [gromacs.org/Downloads](https://www.gromacs.org/Downloads) 或 `winget install GROMACS.GROMACS`（`bin` 目录含 `gmx.exe`） |

ML 势（MACE-MP/CHGNet）由 pip `[ml]` 附带，无需额外二进制。`real_compute: false` 的案例（如冒烟案例）不依赖上述任何二进制。

运行宿主前，在项目根目录创建 `.env`：`DEEPSEEK_API_KEY=<你的 key>`（宿主启动时引导为 `ANTHROPIC_AUTH_TOKEN`，密钥不落盘；详见 [host/README.md](host/README.md)）。

## 运行

V1 主案例 `cases/fast_charge_v1.yaml`：EC/EMC + LiPF6 体系，4C 快充下的析锂与温升（T_max < 60℃ 且无析锂），30 轮预算，收尾 Top-3 `run-orca` + Top-1 `run-md` 真计算背书（挂夜，约一夜一案例）：

```powershell
.venv\Scripts\python.exe host/run.py --config cases/fast_charge_v1.yaml
```

**工作区 = 案例配置所在目录**（`log.jsonl`、`session_id`、`report.html`、`csv/` 及各阶段产物子目录均落在此处）。论文实验建议按设计文档 §5.1 布局把案例复制到独立目录再跑：

```powershell
New-Item -ItemType Directory -Force runs/fast_charge_v1
Copy-Item cases/fast_charge_v1.yaml runs/fast_charge_v1/config.yaml
.venv\Scripts\python.exe host/run.py --config runs/fast_charge_v1/config.yaml
```

**resume（续跑）**：重跑同一条命令即自动续跑——session id 持久化在工作区 `session_id` 文件，断点状态以工作区产物（`log.jsonl`）为准，无需人工传 id；删除 `session_id` 文件则从零开始新会话。

## 消融实验

全部通过案例配置开关执行，不改代码（各开关回答的问题对照设计文档 §10.1）。复制案例 YAML 后修改 `ablations`：

```yaml
ablations:
  guardrails: false    # 关闭反模式护栏（SKILL.md 第三章）：护栏贡献多少？
  consistency: false   # 关闭三模型一致性检查：不置信信号贡献多少？
  bridge: false        # 关闭参数桥梁（微观结果不回流，用默认文献参数）：跨尺度桥梁贡献多少？
```

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
