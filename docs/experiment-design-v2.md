# 实验设计 v2：拿什么评、怎么打分

> 取代 `docs/experiment-design.md`（2026-08 那版，其横幅已声明作废）。
> 本文只写**评测**；设计变量能不能算，看 `battery-design-map.md`。
> 状态：2026-09-26 起。**任务集尚未定稿**，本文先定"形式"与"打分"。

---

## 一、评测要有三件东西，缺一件都不成立

| | 是什么 | 现状 |
|---|---|---|
| **① 设计空间** | agent **能动什么**——哪些量可自由设、哪些算得出、哪些只能查、哪些根本拿不到 | 见 `battery-design-map.md`；主表 27 行，四种判定（通·设 / 通·算 / 通·查 / ✗） |
| **② 任务与打分** | agent **被要求达成什么、怎么算分** | **本文**。任务形式见下三节；打分方案见第四节 |
| **③ 仿真器签字** | 证明它算出来的数**不是自说自话** | **最弱的一环**，见第五节。现有 4 款验证电芯（LG M50 / Kokam / Enertech）＋ 一组行驶循环，**但低温、高温老化、快充、针刺一条都没有** |

**①和②是耦合的**：① 决定了**哪些任务做得出来**。例：包覆剂与掺杂剂已判为 ✗，所以"靠掺杂提升循环寿命"这类任务在本工具里**构造性不可解**，写进任务集只会得到假失败。设计任务前必须先过一遍主表。

### 判据能用哪些指标（任务设计的前置门槛）

**任务文本里写哪几个指标不是随便挑的——只有仿真器有资格算的指标才能进判据。** 写进"算不准"的指标，判出来的达标是假的。

| 指标 | 算得准吗 | 进判据的条件 |
|---|---|---|
| **容量、电压** | ✅ | 已标定（LG M50：0.45% 容量 / 20.6 mV RMSE） |
| **能量密度 Wh/kg、Wh/L** | ✅ 但**口径要当心** | 我们是电极堆口径、规格书是整芯口径，**差约 1.6 倍**（见 5c）。比之前必须处理 |
| **内阻 DCR** | ⚠️ | 能算，但接触电阻那类参数是**查文献**来的，不是这套体系的实测 |
| **倍率（5C / 10C）** | ⚠️ | **必须用 DFN**——实测过 SPMe 在 5C 差 3 倍（0.141 vs 0.433 Ah） |
| **低温 −20 °C** | ⚠️ | 要标定过；现在还**没标定过低温** |
| **快充 / 析锂** | ⚠️ | 判据是**负极电位**；厂商的"支持 X C"是另一个口径——**要么统一口径，要么这条不进** |
| **循环寿命** | ⚠️ **要换判据** | 模型容量轨迹**有反方向伪影**（SEI 越多容量越多，1.648→2.185 Ah）——**不能用"容量保持率"，要换成 SEI 厚度**（现有 T2/T6/T7 判的就是 SEI 厚度，做对了） |
| **热失控起始温度** | ⚠️ | 能算，但三条副反应参数是**写死的文献值**（Kim 2019 / Coman 2016），**不随电芯材料变** |
| **针刺 / 过充通过性** | ⚠️ | 同上，且**短路电阻要实测** |
| **成本** | ✅ 但要标口径 | 材料成本，**是下界**（不含电解液、外壳、制造费用） |
| **日历老化** | ❌ | **没有静置工况**（`PROTOCOLS` 8 个里没有）＋ `SEI growth activation energy` 在 Chen2020 = 0 → **温度完全不生效** |
| **自放电** | ❌ | **没有模型**（PyBaMM `models/` 全目录 grep "self discharge" **0 命中**） |
| **制造可行性** | —— | 是**设计变量的边界**，不是算出来的量 |

**三条规则**：

1. **❌ 的两条不进任务文本**——写了也判不了，只会产生假失败。
2. **⚠️ 的可以进，但要写清条件**：倍率必须 DFN；循环寿命必须换判据；快充的判据要和厂商口径统一。
3. **✅ 的可以进，是任务的主力。**

**这张表和 `battery-design-map.md` 的主表配套**：那边说"agent **能动**什么"，这边说"agent **被要求达成**什么"——两张表从同一套工具能力推出来，必须一致。

---

## 二、结论：电池域**没有**"目标 + 约束"形式的公开基准

按四种查询（battery + benchmark / design + agent / inverse design + multi-objective / design + simulation + evaluation）系统检索后的结论：

**没有任何公开基准以"达成这些电芯指标、同时满足这些约束"的形式定义电池设计任务。**

电池领域现有的"基准"是四类别的：

| 类型 | 例子 | 为什么不是我们要的形式 |
|---|---|---|
| **预测类** | BatteryML（ICLR 2024，RUL/SOH 预测，7 个公开数据源） | 任务是估寿命，不是设计 |
| **参数反演类** | Battery-Sim-Agent（arXiv:2605.29560） | **有隐藏的标准答案** $\theta^*$，评分是离它多远；见下 |
| **问答题** | ChargeBD / ESS-LLM（液流电池，500 题） | 选择题 |
| **子问题集** | BTMS 基准（arXiv:2510.25219） | 12 个带约束的多目标热管理问题（蛇形流道、Tesla 阀、仿生冷板…），$\max$ 4 个带真约束如 $g_1 = T_{\max}\le 30.895$。**但没有评分方案、没有基线**——作者自己写明留给未来工作 |

**"参数反演"与"目标+约束"的区别，必须写清**，否则会被当成同类工作：

| | 参数反演 | 目标 + 约束设计 |
|---|---|---|
| 输入 | 一条观测曲线 $Y_{\rm obs}$（＋先验 $\theta_{\rm init}$） | 一段文字：目标指标 ＋ 硬约束 |
| 输出 | 一组参数 $\theta$ | 一个设计（值由 agent 自选） |
| **有无标准答案** | **有**——$\theta^*$ 藏在题里 | **没有** |
| 评分 | 离 $\theta^*$ 多远 | 约束满不满足 ＋ 目标值多高 |
| 搜索的性质 | **还原**一个已知的点 | **找**一个好点，可能根本不存在 |

**一句话**：反演题的答案是别人早就定好的；设计题的答案是自己找出来、以前没被定过的。**反演题自带答案所以不需要约束层；设计题没有答案，所以约束怎么判、分数怎么算必须先定死。**

---

## 三、形式先例在隔壁领域，而且很成熟

| 基准 | 领域 | 任务形式 | 怎么打分 | 规模 |
|---|---|---|---|---|
| **BikeBench** ⭐ | 自行车车架设计 | 每例给文本需求 ＋ 人体尺寸 ＋ 用途；设计是 64 个参数；**10 个设计目标 ＋ 40 个设计约束** | **满足约束的解上的超体积** ＋ 平均约束违反量 ＋ 与 759 个留出设计的 MMD 相似度 ＋ 多样性；带排行榜；评测预算分档 | 100 例 |
| **EngDesign** ⭐ | 9 个工程域 | 每任务写明 design goals / constraints / performance requirements；四件套：任务描述、评分细则、评测管线、参考设计 | 仿真验证（SPICE / FEA / MATLAB），**0–100 分带部分分** | 101 题（67 开源，34 需 MATLAB/Cadence 许可） |
| **BOCoDe** | 工程设计与贝叶斯优化 | `evaluate(x)` 直接返回 **`(values, constraints)`**，约束写成 $g(x)\le 0$ | 标准 BO 指标 | 307 题（159 工程设计） |
| **GuacaMol** | 分子设计 | 目标导向多目标，模型拿到打分函数后迭代提议分子 | 分数归一到 $[0,1]$，按 top-1/top-10/top-100 加权 | 25 题 |
| **PMO** | 分子设计 | 优化，但**硬性 oracle 预算**（10K 次） | Top-10 AUC | 23 题 |
| **MLE-bench** | ML 工程 | 去打 Kaggle 比赛，够到奖牌线 | 公开排行榜阈值 | 75 个比赛 |

**对比一下 LLM 科学 agent 的基准**（说明"为什么不能直接拿来用"）：ScienceAgentBench（102 题，形式是**写出能复现论文流程的 Python 程序**）、DiscoveryBench（264 真题，形式是**重新发现论文结论**）、FIRE-Bench（claim 级 P/R/F1）、CORE-Bench（复现代码结果）、ChemBench / LAB-Bench（问答）。**都不含"工程设计 + 目标约束"这一层。**

---

## 四、要采纳的打分方案

**照 BikeBench 那一套，不自己发明**：

1. **主指标：约束满足解上的超体积（hypervolume）** —— 天然处理"不同任务量纲不同怎么合"，也天然对上我们"硬约束 ＋ 目标优化"的结构。
2. **副指标：平均约束违反量** —— 不达标时不是简单记 0 分，而是**报出差多远**，这样"够不着"才有信息量。
3. **接口形状：`evaluate(x) → (values, constraints)`**（照 BOCoDe），约束统一写成 $g(x)\le 0$。
4. **预算口径**：照 PMO，写明**仿真调用次数上限**——我们的 agent 与基线必须在同一预算下比。

**硬约束沿用现有划分**：析锂（负极电位）、最高温度、热失控触发、**成本**、**制造可行性**（后两条 2026-09-26 定为硬约束，口径见 `battery-design-map.md` 第五节）。

---

## 五、仿真器签字：有几款验证电芯、够不够

要让"我们达成 500 Wh/kg"这句话站得住，得先证明仿真器算的数跟真实电芯对得上。**这是审稿人第一个会问的。**

### 5a. 验证电芯清单（2026-09-26 查实）

**一个电芯要能用来验证，得同时有 ① 参数集、② 与该参数集同款的实测。** 两者齐的现在有这些：

| 验证电芯 | 参数集 | 实测（来源） | 覆盖工况 | 特别之处 |
|---|---|---|---|---|
| **LG M50**（21700，NMC811 ＋ 石墨-SiOx） | Chen2020 / ORegan2022 / OKane2022 等 **6 套** | Imperial College 数据集（**我们自己接的**）<br>Zenodo 10.5281/zenodo.10637534，CC BY 4.0；论文 Kirkaldy, N.; Samieian, M. A.; Offer, G. J.; Marinescu, M.; Patel, Y. *J. Power Sources* **2024**. DOI: 10.1016/j.jpowsour.2024.234185 | **0.1C 放电**，10/25/40 °C 多 SOC 区间 | 对标结果 **0.45% 容量 / 20.6 mV RMSE**；和我们大部分任务同体系 |
| **Kokam SLPB75106100**（软包，NCO/石墨） | Ecker2015 ×2 | **PyBaMM 自带**（`Ecker_1C.csv`、`Ecker_5C.csv`） | **1C、5C** | **验的是倍率** |
| **Enertech**（软包，2.28 Ah） | Ai2020 | **PyBaMM 自带**（13 个文件） | **0.1C / 0.5C / 1C / 2C**，且同时有**电压 ＋ 温度 ＋ 位移** | **唯一带完整裂纹参数**（Ai2020），**且自带形变实测**——目前唯一能验开裂模型的验证数据 |
| **行驶循环**（不是一个电芯） | —— | **PyBaMM 自带**（`UDDS.csv`、`US06.csv`、`WLTC.csv`、`car_current.csv`） | 动态工况 | **验的是动态工况** |

**⚠️ 不要搞错的一条**：PyBaMM 自带的 **26 个验证文件**里，**COMSOL 那 6 个（0.1C–3C、1+1D-3C）是软件对软件**（PyBaMM vs COMSOL），**不是实测，不能用来验证**。

**有参数集但没有配套实测的，不能用来验证**：Mohtat2020（NMC532 软包）、NCA_Kim2011（建模论文的设计算例，**不是实测商品电芯**）、Marquis2019 / Xu2019（归属存疑——两套写同一个 Kokam 型号但几何差一个量级；Xu2019 的 docstring 说钴酸锂、代码赋的是 NMC）。

### 5b. 还缺什么

**我们的任务涉及 5C 倍率、−20 °C 低温、4C 快充、45 °C 老化、针刺**——现有四处验证里：

- **倍率**：有 Kokam 5C、Enertech 2C ✅
- **动态工况**：有驱动循环 ✅
- **形变 / 开裂**：有 Enertech 位移 ✅
- **❌ 低温（−20 °C）：一条都没有**
- **❌ 高温老化（45 °C）：一条都没有**
- **❌ 快充（4C 以上）：没有**
- **❌ 针刺：没有**（那本来就要实测，见判据表）

**可补的实测数据**（下面这些**没有配套参数集，要自己反演出一套参数**——那是一项独立工作，不是拿来即用）：

| 数据集 | 补什么工况 | 许可 |
|---|---|---|
| **Panasonic 18650PF**（Kollmeyer, Mendeley 10.17632/wykht8y7tg.1） | **5 个温度** ＋ HPPC ＋ 阻抗；电芯建模参数化的标准集 | CC BY 4.0 |
| **ISU-ILCC**（10.25380/iastate.22582234） | 238 个软包、63 种工况，**倍率 × 放电深度**矩阵，11.19 GB 原始数据 | CC BY 4.0 |
| **XJTU**（10.5281/zenodo.10963339） | 55 × 18650 NCM523，**1 Hz** 采样，含随机游走与卫星工况 | CC BY |
| **Oxford**（10.5287/bodleian:KO2kdmYGg） | **Artemis 城市驱动循环**；254 MB .mat | **ODbL**（不是 CC BY，若再分发派生表要注意） |
| **CALiSol-23**（10.1038/s41597-024-03575-8） | **实测电解液电导率 13,825 点**（38 溶剂 × 14 锂盐 × 浓度 × 温度）——给输运参数签字 | CC BY 4.0 |

**注意**：CALCE、Battery Archive、Sandia、NASA 部分条目**没有开放许可**；Battery Archive 的批量 CSV 只能发邮件索取。

**"没有设计参数"这件事不影响评测**：公开数据里没有任何一个把设计参数（厚度 / 孔隙率 / N-P）与实测性能配在一起，但**那是"能不能和别人比设计"的问题，不是"能不能评方法能力"的问题**——后者只需要同一套仿真器 ＋ 同一份任务文本。**唯一受影响的是：不能写"我们的设计与已发表电芯比更好"。**

### 5c. 和厂商规格书比之前，必须处理质量口径（2026-09-26）

**"拿真实电芯的规格书比指标"这条路，第一项就会撞上口径差。**

厂商规格书的 Wh/kg、Wh/L 是**整芯**口径（含电解液、外壳、集流体）。我们的 `calc-energy` 是**电极堆**口径。实测（Chen2020 几何）：

| 口径 | 质量 | Wh/kg |
|---|---|---|
| 电极堆（现在） | 43.45 g | **418** |
| ＋ 电解液 | 49.90 g | 364 |
| 整芯（LG M50T 约 70 g） | ~70 g | **259** |

**差约 1.6 倍。直接比，就是白送 61%。**

**处理办法（已定，见 `battery-design-map.md` 第 1b 节）**：

1. **口径定为"电极堆 ＋ 电解液"，不含封装**
2. **不与规格书比绝对值**；要比就比**同一封装下的相对改进**——同封装下外壳质量近似不变，改进的方向与量级基本不受影响
3. 论文里把口径**写死在方法学**，别让读者把 418 Wh/kg 读成整芯值

**前置工作**：并进电解液要先有一个电解液密度（文献值，EC:EMC 有实测）；并进去之后**所有能量密度的数都会变**（约 −13%），任务目标值要跟着重标。

---

## 六、基线电芯清单（厂商规格书，2026-09-27）

> **用途**：若走"拿真实电芯的规格书比不变差"这条路，基线从这里挑。
> **完整字段**（含 Wh/kg 的计算输入、逐条出处与 URL）在 `calibration/specsheets/` 的
> `21700.md` / `pouch-prismatic.md` / `18650.md`。**下表只留选基线要看的几列，出处不重复列。**

### 6a. 圆柱 21700（13 款，NMC / NCA）

| 型号 | 标称容量 · 电压 | Wh/kg | Wh/L | 最大持续放电 | 循环寿命（条件） |
|---|---|---|---|---|---|
| **LG INR21700M50LT (2021)** | 4800 mAh basis (doc: 1C=4800 mA) · 3.69 V | 269.6 \* | 713.5 \* | 3.0C (14 400 mA) at 10–25 °C | 1,000 cyc, ≥80% of initial energy |
| **LG INR21700M50LT (2020)** | 4800 mAh basis · 3.69 V | 266.9 \* | 714.0 \* | 3.0C (14 400 mA) | 1,000 cyc, ≥80% of initial energy |
| **LG INR21700 M50T (2018)** | 4850 mAh basis (doc: 1C=4850 mA) · 3.63 V | 260.0 \* | 712.0 \* | 3.0C (14 550 mA) at 10–25 °C | **300 cyc**, 80% of initial energy |
| **Molicel INR-21700-P42A** | 4200 typ / 4000 min mAh (15.5 Wh typ) · 3.6 V | 230 stated / 221.4 \* | 615 stated / 596.8 \* | 45 A | **not stated** (chart to 500 cyc only) |
| **Molicel INR-21700-P45B** | 4500 typ / 4300 min mAh (16.2 Wh typ) · 3.6 V | 242 stated / 231.4 \* | 643 stated / 633.1 \* | 45 A | **not stated** |
| **Molicel INR-21700-P50B** | 5000 typ / 4850 min mAh (18.0 Wh typ) · 3.6 V | 260 stated / 253.5 \* | 714 stated / 703.4 \* | 60 A | **not stated** |
| **Samsung INR21700-40T** | 4000 min std / 3900 min rated mAh · 3.6 V | 205.7 \* | 579.2 \* | 35 A (45 A with 80 °C cut) | 250 cyc, **60%** |
| **Samsung INR21700-48G** | 4700 min / 4800 typ mAh; 17.04/17.4 Wh · 3.6 V | 247.0–252.2 \* | 694.7–709.4 \* | 9.6 A (pulse 35 A/10 s) | 500 cyc, 75% @23 °C **and** 500 cyc, 70% @45 °C |
| **Samsung INR21700-50E** | 4900 std / 4753 rated mAh · 3.6 V | 255.7 \* | 702.5 \* | 9.8 A | 500 cyc, 80% |
| **Samsung INR21700-50S** | 5000 typ / 4800 rated mAh · 3.6 V | 250.0 \* | 718.7 \* | 25 A (45 A with 80 °C cut) | 250 cyc **60%** @25 A; 100 cyc **60%** @45 A |
| **Samsung INR21700-50G** | 4850 mAh min · **3.63 V** | 253.3 \* | 717.7 \* | 9.7 A | 1,000 cyc, 80% |
| **Samsung INR21700-30T** | 3000 std / 2950 rated mAh · 3.6 V | 156.5 \* | 434.4 \* | 35 A | 250 cyc, **60%** |
| **Lishen LR2170SA** | 4000 nom / 3900 min mAh · 3.65 V | 211.6 \* | 556.8 \* | 3.0C (12 000 mA) at 5–45 °C | 1,000 cyc, 80% of first-cycle capacity |

### 6b. 方形 / 软包（6 款，NMC）

| 型号 | 标称容量 · 电压 | Wh/kg | Wh/L | 最大持续放电 | 循环寿命（条件） |
|---|---|---|---|---|---|
| **Samsung SDI 94 Ah (EV cell)** | 94 Ah **minimum** (1/3C, 25 °C, discharge, 2.7–4.15 V). Energy 345 Wh min (1/3… | **165 (V, stated as "specific energy (min.)")** | Not given by vendor. **Computed: 354 Wh/L** using 345 Wh / 0.9731 L, volume fr… | **150 A continuous discharge (25 °C) ≈ 1.6C**; peak 409 A. Charge: 72 A contin… | **3,200 cycles to EOL80% / 5,200 cycles to EOL70%, at 0.5C/1C, room temp.** Al… |
| **Kokam SLPB78205130H (High Power NMC Cell)** | 16 Ah. **Nominal voltage NOT stated in this document.** Note: the vendor-state… | **150 (V)** | Not given by vendor. **Computed: 252 Wh/L** using vendor's own numbers: 150 Wh… | **8C continuous, 12C pulse** (vendor C-rate table); AC-IR 1.2 mΩ | Not stated in this document |
| **Kokam SLPB100216216H (High Power NMC Cell)** | 40 Ah. **Nominal voltage NOT stated.** The vendor-stated 157 Wh/kg with 0.94 k… | **157 (V)** | Not given by vendor. **Computed: 279 Wh/L** using 157 Wh/kg x 0.94 kg = 147.6 … | **8C continuous, 12C pulse**; AC-IR 0.8 mΩ | Not stated in this document |
| **Kokam SLPB120216216 (High Energy NMC Cell)** | 53 Ah. **Nominal voltage NOT stated.** The vendor-stated 179 Wh/kg with 1.09 k… | **179 (V)** | Not given by vendor. **Computed: 317 Wh/L** using 179 Wh/kg x 1.09 kg = 195.1 … | **5C continuous, 8C pulse**; AC-IR 0.9 mΩ | Not stated in this document |
| **Kokam SLPB160460330 (High Energy NMC Cell)** | 240 Ah (largest in vendor table). **Nominal voltage NOT stated.** 197 Wh/kg wi… | **197 (V)** | Not given by vendor. **Computed: 272 Wh/L** using 197 Wh/kg x 4.51 kg = 888.5 … | **2C continuous, 3C pulse**; AC-IR 0.5 mΩ | Not stated in this document |
| **CATL S5E891 (48 Ah NMC prismatic, P/N FC-N48-S5E891-5AEL)** | **≥ 48 Ah minimum at 1C** (≥ 50 Ah at 0.33C). Energy **≥ 172.8 Wh at 1C** (≥ 1… | **212 (V, at 0.33C) / 200 (V, at 1C)** — vendor states both | **521 (V, at 0.33C) / 490 (V, at 1C)** — vendor states both | **Maximum continuous discharge 96 A @ 25 °C (= 2C), 46 A @ 0 °C, 24 A @ -20 °C… | **≥ 1,500 cycles, capacity fade to 80 %, at 25 ± 2 °C, 24 A charge / 48 A disc… |

### 6c. 圆柱 18650（31 款）

| 型号 | 标称容量 · 电压 | Wh/kg | Wh/L | 最大持续放电 | 循环寿命（条件） |
|---|---|---|---|---|---|
| **Panasonic NCR18650BF** | Rated 3200 mAh @20 °C / min 3250 mAh, typ 3350 mAh @25 °C; 3.6 V nom. Charge C… | **248 Wh/kg (vendor)**; a second column gives 219 Wh/kg — Panasonic states the… | **677 Wh/l (vendor)**; second column 600 Wh/l | Not stated as a rating. Discharge-rate chart plotted 0.2C (650 mA) / 0.5C (162… | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Panasonic NCR18650PF** | Rated 2700 mAh @20 °C / min 2750 mAh, typ 2900 mAh @25 °C; 3.6 V nom. Charge C… | **207 Wh/kg (vendor)**; second column 200 Wh/kg — same "bare cell without tube… | **577 Wh/l (vendor)**; second column 559 Wh/l | Not stated as a rating. Discharge-rate chart plotted 0.2C (550 mA) / 0.5C (137… | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Murata US18650VTC5** | Nominal 2600 mAh, rated (min) 2500 mAh; 3.6 V nom. Reference charge (for capac… | **Computed 211 Wh/kg** — not given by vendor. Inputs: 2.600 Ah × 3.6 V = 9.36 … | **Computed 534 Wh/L** — not given by vendor. Same 9.36 Wh; volume from vendor … | Not stated as a rating. Discharge-rate chart plotted 2.5 A / 5 A / 10 A / 15 A… | **1000 cycles shown** (chart end, no EoL criterion stated). Condition: charge … |
| **Murata US18650VTC5A** | Nominal 2600 mAh, rated (min) 2500 mAh; 3.6 V nom. Reference charge: CCCV 2.5 … | **Computed 208 Wh/kg** — not given by vendor. Inputs: 2.600 Ah × 3.6 V = 9.36 … | **Computed 534 Wh/L** — not given by vendor. Same 9.36 Wh; volume from vendor … | Not stated as a rating. Discharge-rate chart plotted 2.5 A / 5 A / 10 A / 15 A… | **1000 cycles shown** (chart end, no EoL criterion stated). Condition: charge … |
| **Murata US18650VTC6** | Nominal 3120 mAh, rated (min) 3000 mAh; 3.6 V nom. Reference charge: CCCV 3.0 … | **Computed 241 Wh/kg** — not given by vendor. Inputs: 3.120 Ah × 3.6 V = 11.23… | **Computed 641 Wh/L** — not given by vendor. Same 11.232 Wh; volume from vendo… | Not stated as a rating. Discharge-rate chart plotted 3 A / 5 A / 10 A / 15 A /… | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge 2… |
| **Molicel INR-18650-P26A** | Typical 2600 mAh / 9.5 Wh; 3.6 V nominal; charge 4.2 V, discharge 2.5 V. Charg… | **190 Wh/kg (vendor)** — vendor states "Gravimetric 190 Wh/kg" | **535 Wh/l (vendor)** — vendor states "Volumetric 535 Wh/l" | **35 A (vendor)** — listed as "Discharge Current Maximum" | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Panasonic/Sanyo UR18650F** | Rated (min) 2450 mAh @20 °C; capacity min 2500 mAh, **typ 2600 mAh** @25 °C; *… | **193 Wh/kg (vendor)** — "Gravimetric: 193 Wh/kg", footnote "Energy density ba… | **544 Wh/l (vendor)** — "Volumetric: 544 Wh/l", same bare-cell basis | Not stated as a rating. Discharge-rate chart plotted 0.2C / 0.5C / 1C / 2C (te… | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Panasonic/Sanyo UR18650A** | Rated (min) 2100 mAh @20 °C; capacity min 2150 mAh, **typ 2250 mAh** @25 °C; *… | **176 Wh/kg (vendor)** — "Gravimetric: 176 Wh/kg", footnote "Energy density ba… | **453 Wh/l (vendor)** — "Volumetric: 453 Wh/l", same bare-cell basis | Not stated as a rating. Discharge-rate chart plotted 0.2C / 0.5C / 1C / 2C / 3… | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Panasonic/Sanyo UR18650RX** | Rated (min) 1950 mAh @20 °C; capacity min 1950 mAh, **typ 2050 mAh** @25 °C; *… | **155 Wh/kg (vendor)** — "Gravimetric: 155 Wh/kg", footnote "Energy density ba… | **413 Wh/l (vendor)** — "Volumetric: 413 Wh/l", same bare-cell basis | Not stated as a rating. Discharge-rate chart plotted 0.2C / 0.5C / 1C / 2C / 1… | **No cycle-life data in the vendor sheet** — the "Cycle Life Characteristics" … |
| **Panasonic/Sanyo UR18650ZTA** | Two spec columns. Col 1: rated (min) 2850 mAh @20 °C; min 2900 mAh, **typ 3000… | **220 Wh/kg (vendor)** for col 1; **199 Wh/kg** for col 2. Footnote: "Energy d… | **620 Wh/l (vendor)** for col 1; **561 Wh/l** for col 2, same bare-cell basis | Not stated as a rating. Discharge-rate chart plotted 0.2C (580 mA) / 0.5C (145… | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Molicel INR-18650-P28A** | Typical 2800 mAh / 10.3 Wh; minimum 2700 mAh / 9.56 Wh; **3.6 V** nominal; cha… | **219 Wh/kg (vendor)** — "Gravimetric 219 Wh/kg" | **589 Wh/l (vendor)** — "Volumetric 589 Wh/l" | **35 A (vendor)** — "Discharge Current Maximum" | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Molicel INR-18650-M30A** | Typical 3000 mAh / 10.8 Wh; minimum 2900 mAh / 10.4 Wh; **3.6 V** nominal; cha… | **234 Wh/kg (vendor)** — "Gravimetric 234 Wh/kg" | **632 Wh/l (vendor)** — "Volumetric 632 Wh/l" | **10 A (vendor)** — "Discharge Current Maximum" | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Molicel INR-18650-M35A** | Typical 3450 mAh / 12.5 Wh; minimum 3350 mAh / 11.9 Wh; **3.6 V** nominal; cha… | **264 Wh/kg (vendor)** — "Gravimetric 264 Wh/kg" | **730 Wh/l (vendor)** — "Volumetric 730 Wh/l" | **10 A (vendor)** — "Continuous Discharge Current Maximum" | **400 cycles shown** (chart end, no EoL criterion stated). Condition as printe… |
| **Molicel INR-18650A** | Minimum 2500 mAh / 9.0 Wh (no typical given); **3.6 V** nominal; charge 4.2 V,… | **205 Wh/kg (vendor)** — "Gravimetric 205 Wh/kg" | **520 Wh/l (vendor)** — "Volumetric 520 Wh/l" | **20 A (vendor)** — "Continuous Discharge Current Maximum" | **600 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Molicel INR-18650-P30B** | Typical 3000 mAh / 10.8 Wh; minimum 2900 mAh / 10.4 Wh; **3.6 V** nominal; cha… | **234 Wh/kg (vendor)** — "Gravimetric 234 Wh/kg" | **631 Wh/l (vendor)** — "Volumetric 631 Wh/l" | **30 A continuous (vendor)** — "Discharge Current Continuous 30 A (80 °C cut-o… | **500 cycles shown** (chart end, no EoL criterion stated). Condition printed o… |
| **Molicel IHR-18650B** | Typical 2250 mAh / 8.4 Wh; minimum 2150 mAh / 7.8 Wh; **3.6 V** nominal; charg… | **175 Wh/kg (vendor)** — "Gravimetric 175 Wh/kg" | **503 Wh/l (vendor)** — "Volumetric 503 Wh/l" | **4.4 A (vendor)** — "Discharge Current Maximum", with the vendor footnote "* … | **300 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Molicel ICR-18650J** | Typical 2370 mAh / 9.0 Wh; minimum 2300 mAh / 8.4 Wh; **3.7 V** nominal; charg… | **187 Wh/kg (vendor)** — "Gravimetric 187 Wh/kg" | **517 Wh/l (vendor)** — "Volumetric 517 Wh/l" | **5 A (≤45 °C) / 4 A (≤60 °C) (vendor)** — "Discharge Current Maximum", with t… | **300 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Molicel ICR-18650K** | Typical 2600 mAh / 9.8 Wh; minimum 2500 mAh / 9.4 Wh; **3.7 V** nominal; charg… | **205 Wh/kg (vendor)** — "Gravimetric 205 Wh/kg" | **588 Wh/l (vendor)** — "Volumetric 588 Wh/l" | **5 A (≤45 °C) / 4 A (≤60 °C) (vendor)** — "Discharge Current Maximum", with t… | **300 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Molicel ICR-18650M** | Typical 2800 mAh / 10.5 Wh; minimum 2700 mAh / 10.2 Wh; **3.7 V** nominal; cha… | **222 Wh/kg (vendor)** — "Gravimetric 222 Wh/kg" | **631 Wh/l (vendor)** — "Volumetric 631 Wh/l" | **5 A (≤45 °C) / 4 A (≤60 °C) (vendor)** — "Discharge Current Maximum", with t… | **300 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Tenpower INR18650-32HE** | 3200 mAh / 11.52 Wh nominal; **3.6 V** nominal; charge 4.2 V, discharge 2.5 V.… | **245 Wh/kg (vendor)** — "Gravimetric 245 Wh/kg" | **696 Wh/L (vendor)** — "Volumetric 696 Wh/L" | **10 A (vendor)** — "Continuous Discharge Current Maximum" | **1000 cycles shown** (chart end, no EoL criterion stated). Condition: charge … |
| **Panasonic NCR18650B** | Rated (min) 3200 mAh @20 °C; capacity min 3250 mAh, **typ 3350 mAh** @25 °C; *… | **243 Wh/kg (vendor)** — "Gravimetric: 243 Wh/kg", footnote "Energy density ba… | **676 Wh/l (vendor)** — "Volumetric: 676 Wh/l", same bare-cell basis | Not stated as a rating. Discharge-rate chart plotted 0.2C / 0.5C / 1C / 2C (te… | **500 cycles shown** (chart end, no EoL criterion stated). Condition: charge C… |
| **Panasonic NCR18650GA** | Rated 3300 mAh @20 °C; capacity min 3350 mAh, **typ 3450 mAh** @25 °C; **3.6 V… | **224 Wh/kg (vendor)** — "Gravimetric 224 Wh/kg", footnote "Energy density is … | **693 Wh/l (vendor)** — "Volumetric 693 Wh/l", same bare-cell basis | Not stated as a rating. Discharge-rate chart plotted 2 A / 4 A / 6 A / 8 A / 1… | **500 cycles shown** (chart end, no EoL criterion stated). Condition as printe… |
| **Samsung SDI INR18650-25R** | Nominal discharge capacity **2500 mAh** (charge 1.25 A, 4.20 V CCCV, 125 mA cu… | **Computed 200 Wh/kg** — not given by vendor. Inputs: 2.500 Ah × 3.6 V = 9.0 W… | **Computed 526 Wh/L** — not given by vendor. Same 9.0 Wh; volume from vendor d… | **20 A continuous at 25 °C (vendor)** — "3.7 Max. continuous discharge", with … | **250 cycles with a stated end criterion**: "With standard charge and maximum … |
| **Samsung SDI INR18650-35E** | Standard discharge capacity min **3350 mAh** (charge 0.5C = 1700 mA, 4.2 V, 0.… | **Computed 241 Wh/kg** — not given by vendor. Inputs: 3.350 Ah × 3.6 V = 12.06… | **Computed 684 Wh/L** — not given by vendor. Same 12.06 Wh; volume from vendor… | **8 A continuous; 13 A non-continuous (vendor)** — "3.8 Max. Discharge Current… | **500 cycles with a stated end criterion**: charge 1020 mA with 100 mA cut-off… |
| **Samsung SDI INR18650-29E** | Nominal capacity **2850 mAh** typical (0.2C, 2.50 V discharge), minimum 2750 m… | **Computed 217 Wh/kg** — not given by vendor. Inputs: 2.850 Ah × 3.65 V = 10.4… | **Computed 602 Wh/L** — not given by vendor. Same 10.403 Wh; volume from vendo… | **2750 mA continuous; 8250 mA non-continuous (vendor)** — "3.8. Max. Discharge… | **500 cycles with a stated end criterion**: charge 1735 mA with 0.05C cut-off;… |
| **LG Energy Solution INR18650MH1** | Rated capacity nominal **3200 mAh**, minimum 3100 mAh (by standard charge/disc… | **Computed 266 Wh/kg** — not given by vendor. Inputs: 3.200 Ah × 3.70 V = 11.8… | **Computed 683 Wh/L** — not given by vendor. Same 11.84 Wh; volume from vendor… | By temperature, vendor-stated: 0.5C (1550 mA) at −20~10 °C; **6.0 A at 10~25 °… | **Two stated cycle-life criteria, both numerical**: (a) 0.5C/0.5C — charge CC/… |
| **Molicel INR-18650-P22S** | Typical 2200 mAh / 7.92 Wh; minimum 2000 mAh / 7.2 Wh; **3.6 V** nominal; char… | **147 Wh/kg (vendor)** — "Gravimetric 147 Wh/kg" | **403 Wh/L (vendor)** — "Volumetric 403 Wh/L" | **36 A (vendor)** — "Discharge Current Maximum", with the printed qualificatio… | Cycle-life chart present in the datasheet but the plotted values were not read… |
| **Samsung SDI ICR18650-26F** | Nominal capacity **2600 mAh** (0.2C, 2.75 V discharge); minimum 2550 mAh. Char… | **Computed 205 Wh/kg** — not given by vendor. Inputs: 2.600 Ah × 3.7 V = 9.62 … | **Computed 557 Wh/L** — not given by vendor. Same 9.62 Wh; volume from vendor … | **5200 mA at 25 °C ambient (vendor)** — "3.9 Max. Discharge Current: 5200mA(am… | **300 cycles with a stated end criterion**: charge with 0.05C cut-off; dischar… |
| **BAK N18650CH** | Typical capacity **2.6 Ah @0.2C**; cell voltage **3.6 V** nominal; charge limi… | **Computed 203 Wh/kg** — not given by vendor. Inputs: 2.6 Ah × 3.6 V = 9.36 Wh… | **Computed 534 Wh/L** — not given by vendor. Same 9.36 Wh; volume from vendor … | **3C max discharge; 1C max charge (vendor)** | **1000 cycles shown** (chart end, no EoL criterion stated). Condition printed … |
| **BAK N18650CL-29** | Typical capacity **2.9 Ah @0.2C**; cell voltage **3.6 V** nominal; charge limi… | **Computed 227 Wh/kg** — not given by vendor. Inputs: 2.9 Ah × 3.6 V = 10.44 W… | **Computed 595 Wh/L** — not given by vendor. Same 10.44 Wh; volume from vendor… | **3C max discharge; 1C max charge (vendor)** | **800 cycles shown** (chart end, no EoL criterion stated). Condition printed o… |
| **BAK N18650CR-35E** | Typical capacity **3.5 Ah @0.2C**; cell voltage **3.6 V** nominal; charge limi… | **Computed 268 Wh/kg** — not given by vendor. Inputs: 3.5 Ah × 3.6 V = 12.6 Wh… | **Computed 719 Wh/L** — not given by vendor. Same 12.6 Wh; volume from vendor … | **3C max discharge; 1C max charge (vendor)** | **800 cycles shown** (chart end, no EoL criterion stated). Condition printed o… |

**6a–6c 合计 50 款**，体系都是 NMC / NCA / NCO，和我们对得上。

### 6d. LFP / LTO —— 体系不符，**只能当对照，不能当基线**

| 型号 | 标称容量 · 电压 | Wh/kg | Wh/L | 最大持续放电 | 循环寿命（条件） |
|---|---|---|---|---|---|
| **A123 Systems AMP20M1HD-A (Nanophosphate Li-ion Prismatic Pouch Cell)** | 19.5 Ah **minimum** (rev MD100105-03, 2012); 19.6 Ah min in rev -01 (2011). 65… | **131 (V)** | **247 (V)** | Datasheet gives "Discharge Power (nominal) 1200 W" and specific power 2400 W/k… | Chart only: "Typical Capacity Fade as a Function of Cycles", **100% DoD, +1C/-… |
| **EVE Energy LF105 (LiFePO4 prismatic cell)** | 105.0 Ah **minimum** (0.5C/0.5C, 25 ± 2 °C, 2.5–3.65 V, fresh cell). Energy ≥ … | Not given by vendor. **Computed: 170 Wh/kg** using ≥336.0 Wh / 1.980 kg (weigh… | Not given by vendor. **Computed: 354 Wh/L** using 336.0 Wh / 0.9499 L, volume … | **Maximum continuous discharge current 1 C (= 105 A)**; standard discharge 0.5… | **4,000 cycles, capacity retention ≥ 80 %, at 300 kgf ± 20 kgf initial compres… |
| **CATL LEP64J4K1 (120 Ah cell, ESS)** | **120 Ah typical** (25 ± 2 °C, 1C discharge, fresh cell). Operating voltage 2.… | Not given by vendor. **Computed: 135 Wh/kg** using 384 Wh (120 Ah x 3.2 V) / 2… | Not given by vendor. **Computed: 277 Wh/L** using 384 Wh / 1.3864 L, volume fr… | **Maximum continuous discharge current 1.0 C (= 120 A)**. Standard discharge 1… | **≥ 3,500 cycles, 25 ± 2 °C, 300 ± 20 kgf initial clamping force, standard cha… |
| **Toshiba SCiB 20Ah (high-energy type)** | 20 Ah rated, **2.3 V nominal** | **89 (V)** | **176 (V)** | Not published as a C-rate. **Output power 1,200 W at SOC 50 %, 10 s, 25 °C; in… | "**over 70 % of its capacity after 20,000 charge/discharge cycles**". Conditio… |
| **Toshiba SCiB 23Ah (high-energy type)** | 23 Ah rated, **2.3 V nominal** | **96 (V)** | **202 (V)** | Output power 1,000 W (SOC 50 %, 10 s, 25 °C); input 1,000 W. No continuous rat… | As high-energy family: >70 % after 20,000 cycles (3C/3C, 25 °C per brochure) |
| **Toshiba SCiB 26Ah (high-energy type)** | 26 Ah rated, **2.3 V nominal** | **106 (V)** | **229 (V)** | Output power 1,200 W (SOC 50 %, 10 s, 25 °C); input 1,500 W. No continuous rat… | As high-energy family: >70 % after 20,000 cycles (3C/3C, 25 °C per brochure) |
| **Toshiba SCiB 2.9Ah (high-power type)** | 2.9 Ah rated, **2.4 V nominal** | **46 (V)** | **85 (V)** | Output power 520 W (SOC 50 %, 10 s, 25 °C); input 410 W. No continuous rating … | "**over 80 % of its initial capacity after 40,000 charge/discharge cycles**" *… |
| **Toshiba SCiB 10Ah (high-power type)** | 10 Ah rated, **2.4 V nominal** | **47 (V)** | **92 (V)** | Output power 1,800 W (SOC 50 %, 10 s, 25 °C); input 1,500 W. No continuous rat… | **Not stated** |
| **Toshiba SCiB 20Ah-HP (combination type)** | 20 Ah rated, **2.3 V nominal** | **84 (V)** | **176 (V)** | Output performance 1,900 W (SOC 50 %, 10 s, 25 °C); input 1,900 W. No continuo… | Not stated on this page |
| **BYD CB98 (47.7 Ah pouch)** | 47.7 Ah; 152.64 Wh; **3.2 V nominal**. Voltage range 3.75–2.0 V/cell. AC-IR 1.… | Not given by vendor. **Computed: 151 Wh/kg** using 152.64 Wh / 1.01 kg (weight… | Not given by vendor. **Computed: 267 Wh/L** using 152.64 Wh / 0.571278 L (257.… | Charge 47.7 A @ 25 °C (**1C**) via 0.5C+0.2C+0.05C profile. Discharge **50 A @… | **Not stated in this 4-page document** — no cycle-life figure appears |
| **BYD BYDC16 (C16-200Ah short-blade cell)** | **Rated capacity 200 Ah; rated energy 640 Wh; nominal voltage 3.20 V**. Charge… | Not given by vendor. **Computed: 141 Wh/kg** using 640 Wh / 4.53 kg (weight 4.… | Not given by vendor. **Computed: 286 Wh/L** using 640 Wh / 2.239536 L (416.0 x… | **Maximum continuous discharge current 300 A @ 25 °C (= 1.5C)**; continuous ch… | **Not stated** — this 3-page document gives no cycle-life figure (it claims on… |
| **SVOLT 184Ah blade cell (蜂巢能源)** | **184 Ah** outgoing capacity (≥184 Ah at 25 °C, 61.5 A (1/3C) discharge to 2.0… | **≥ 166 (V, at 1C) / ≥ 175 (V, at 1/3C)** — vendor states both | Not given by vendor (needs the section-8 drawing, which is not in the text lay… | Discharge power **≥ 1,753 W @ 25 ± 3 °C, 50 % SOC, 10 s**; power density **≥ 5… | **≥ 2,500 cycles**, condition: **25 °C, step charge / 1C discharge, 3–100 % SO… |
| **CALB L173F120A (中航锂电)** | **Nominal capacity 120 Ah** (the document also prints "Minimal Capacity 123 Ah… | Not given by vendor. **Computed: 132 Wh/kg** using 384 Wh (120 Ah x 3.2 V) / 2… | Not given by vendor. **Computed: 276 Wh/L** using 384 Wh / 1.39398 L (173.9 x … | **Maximum continuous discharge current 120 A (= 1C)**. Maximum pulse discharge… | **≥ 2,000 cycles.** Condition: standard charge; **120.0 A (1C) constant-curren… |
| **Gotion IFR28148115A-52Ah (国轩高科)** | **≥ 53.5 Ah at 0.33C / ≥ 52 Ah at 1C**. **Nominal voltage 3.2 V at 0.33C (3.1 … | **≥ 175 (V, at 0.33C/0.33C)** — vendor states it | **≥ 350 (V, at 0.33C/0.33C)** — vendor states it | Standard charge 52 A (1C) CC to 3.65 V then CV to 2.6 A; standard discharge 52… | **2,000 cycles at room temperature** — condition: **80 % capacity retention, 2… |
| **Lishen LP37173207-150Ah (力神)** | **150 Ah nominal; 3.2 V nominal** (I1 = 150 A). Charge cut-off 3.65 V; dischar… | Not given by vendor. Weight 2900 ± 50 g — vendor states no Wh/kg | Not given by vendor | **Maximum discharge current at room temperature: 1 I1 continuous (= 150 A, 1C)… | **Four grade points: 200 cycles ≥ 97 % initial capacity; 500 cycles ≥ 95 %; 80… |
| **Lithium Werks APR18650M1B** | Voltage **3.3 V** nominal; capacity @23 °C typical **1.2 Ah** (min 1.15 Ah); e… | **Computed 95 Wh/kg** — not given by vendor. Inputs: 3.96 Wh (vendor); mass 41… | **Computed 227 Wh/L** — not given by vendor. Same 3.96 Wh; volume from vendor … | **30 A continuous (25C rate); 50 A pulse for 10 s (42C rate) (vendor)**. Minim… | **> 4000 cycles at 1C/1C, 100 % DOD (vendor)** — numerically stated, not a cha… |

### 6e. 这张清单要连带的六条

**一、厂商给的 Wh/kg 自己也有口径。** Panasonic 明写它的 248 Wh/kg 是 *calculated using bare cell dimensions (**without tube**)*，同一份表另一列是 **219**——**同型号差 29 Wh/kg**。**所以不只我们要对齐口径，厂商之间也不一致。**

**二、循环寿命那一列，标"读数"的是我们自己在图上量的。** Panasonic、Murata、Molicel、BAK、Tenpower 都只画曲线不给数字。**引用时必须带这个标注**，不能写成厂商声明。把数字写进规格书的只有：Samsung 25R/35E/29E/26F、LG MH1、Lithium Werks APR18650M1B。

**三、"未给"是真的没给，不是没查到。** Molicel 三款（21700）、Kokam 四款、BYD 两款**没有循环寿命**；**Kokam 四款连标称电压都没有**；**Panasonic UR18650RX 的循环寿命面板原文写着 "Under Construction"**。**没有基线值就没有可比的项——这些不能当"不变差"里的基线。**

**四、LG M50 的整芯质量，LG 自己给了三个数**：M50LT(2021) **67.5 ± 1.0 g**（不含垫圈）/ M50LT(2020) **68.2 ± 1.0 g**（含套管+垫圈）/ M50T(2018) **70.0 g 上限**。**差 2.5 g ≈ 10 Wh/kg**——同一颗电芯引用不同文档，出来的能量密度不一样，**用哪份要写清**。（按 67.5 g 算是 **269 Wh/kg**，与 5c 按 70 g 估的 259 差 4%，那个 1.61 倍的口径差站得住。）

**五、一个矛盾要记下**：PyBaMM 的 Chen2020 摘要说负极是 *bi-component Graphite-SiOx*，但 **LG 自己的产品安全数据表**把负极活性材料列成 **"Carbon (proprietary)"，成分表里没有任何含硅物质**；正极写的是 "Cobalt Lithium Manganese oxide"（NMC）——对得上。**"M50 是石墨-SiOx 负极"这个说法 LG 自己不认。** 要么 SiOx 低到归进 proprietary carbon，要么论文写错了。**这条会影响"哪个参数集代表哪个真实体系"，用之前要定。**

**六、这份清单**不是**所有型号。** 拿不到的：LG MJ1 / M36 / HG2 / HE2 / F1L / M26（**LG 不公开 18650 规格书**）、Samsung 30Q / 32E / 20R / 15M、Murata VTC4 / VTC6A（**murata.com 上就没发布**）、Panasonic NCR18650A、EVE / Lishen / Sunpower。**这是"厂商不发布"或"站点拿不到"，不是没找。**

---
## 七、检索时要避的坑（已经踩过的）

| | |
|---|---|
| **不要引 "Bills et al. 2023, 1000+ 电芯"** | 不存在。实际是 22 个 Sony VTC6（*Sci. Data* **2023**, *10*, 344） |
| **不要引 "Hsieh et al. 2021, 279 电芯"** | 查无实据——限定作者 + 期刊 + 年份 + 主题的 Crossref 查询零结果 |
| **不要写 "MOVE" 数据集** | 这个名字查不到任何电池数据集 |
| **arXiv 不是全部** | ASL-BO（*Bayesian Optimization with Large Language Models for Analog Circuit Sizing*，Zhou 等，武汉大学 / 国科大）在 arXiv 上搜不到，但它是真实存在的会议论文——**以 arXiv 为界的检索会漏掉会议论文** |
| **0.1 / 0.8 这两个发射率值不要随手填** | 领域两派差 3–8 倍且**没人测过真电芯壳**；Yeardley 2020 的敏感性分析说该参数占输出方差约 79.6%。详见 `battery-design-map.md` 第七节 |

---

## 附：待办

- [ ] **任务集定稿**——现有 T1–T8 是自定的，要不要扩、要不要按 BikeBench 的形式重写任务描述
- [ ] **打分方案落地**——超体积计算脚本、约束违反量口径
- [ ] **补验证数据**——至少覆盖常温倍率、低温、高温老化、一个快充或驱动工况
- [ ] **决定是否把任务集作为基准发布**——电池域**没有**这种形式的基准，我们是第一个做的话，这本身是贡献
