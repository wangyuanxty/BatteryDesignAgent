# 设计计划：t2_r1_noceiling（电网储能电池）

日期：2026-08-25 ｜ 案例：t2_r1_noceiling ｜ 协议：Virtual Battery Factory（消融开关：ceiling_escalation OFF）

## 1. 目标分解（契约：阈值逐项与任务文本一致）

| 指标 | 阈值 | 判定层 | 协议/口径 |
|---|---|---|---|
| 质量能量密度 | ≥ 327.18 Wh/kg | stage2 | calc-energy 合同口径（电解液不计入质量，输出键 energy_density_wh_kg） |
| 4C 快充无析锂 | plated = false | stage3 | 4C_charge_45C，lumped 热耦合 + plating 模块；负极表面电位（隔膜界面）任意时刻 < 0 V → 析锂 |
| 负极 SEI 厚度（100 次 1C 循环） | ≤ 500 nm | stage2 | aging_1C_100cyc 输出 sei_thickness_nm_end（负极端面最大厚度） |
| 负极 SEI 厚度（500 次 1C 循环） | ≤ 550 nm | stage2 | aging_1C_100cyc --cycles 500 |
| −20 ℃ 放电容量保持率 | ≥ 0.90 | stage2 | lowT_discharge(253.15 K) capacity_ah ÷ 1C_discharge(298.15 K) capacity_ah（机械推导） |

任务文本未给出最高温度红线：T_max_K 仅记录于 evaluate metrics，不判定。

多目标权衡预期：
- ED↑（厚电极 / 薄集流体 / 薄隔膜 / 低孔隙） ↔ 4C 析锂裕度↓、低温传输↓：ED 与倍率/低温呈 Pareto 冲突；
- 小粒径 → 反应动力学改善（抗析锂、低温好）；SEI 每循环增量与负极局部电流密度相关（方向待仿真验证）；
- N/P↑（负极加厚）→ ED 略降（死重/死体积），负极局部电流密度↓ → SEI 生长可能放缓（待验证）；
- 任务未给优先级 → 全部为硬约束，须同时满足。

## 2. 候选策略

- R1：基线表征（Chen2020 全默认参数）：1C 放电 + calc-energy + 老化 100/500 圈 + 低温 + 4C 安全，建立差距画像；
- R1 附带：开场天花板评估（ceiling_escalation OFF：只评估、不升级）——在薄集流体/薄隔膜/最优孔隙/高传输电解液组合下估算现有体系 ED 与 4C 安全极限，结论写入 funnel 日志；若天花板低于目标，按消融注记不转入材料设计，仅在架构空间内尽力并如实记录；
- R2–R7：架构/配方变体（每轮 2–4 个，exploration_force ON）：
  - ED 组：正极增厚、集流体减薄、隔膜减薄、孔隙率下调；
  - 动力学组：粒径缩小、电解液 σ↑（配方自由度，宽解释）、t⁺↑；
  - SEI 组：负极增厚 / N-P 上调、负极粒径上调；
  - 组合组：多杠杆打包（单因素诊断 → 组合优化）；
- R8+：达标候选 DFN 复核 1C/4C（DFN 失败自动降级 SPMe），锁定最终设计；
- 每轮 log-evaluate 机械判定 + 失败原因定位（症状→尺度：容量/温升=架构参数层 → Stage 3 回退；电位窗/稳定性=材料层 → 材料升级被消融开关禁用，仅记录不执行）。

## 3. 预算分配

- 基线表征 + 天花板评估：1 轮（约 6 个仿真）；
- 架构单因素诊断：2 轮；
- 组合优化 + 安全/低温/老化复核：5–7 轮；
- 终选 DFN 复核 + 交付件：1–2 轮；
- 合计约 10–12 轮；无轮次上限，直到达标或回合预算耗尽。

## 4. 风险与回退计划

- ED 风险：Chen2020（NMC811/石墨，电解液不计质量）基线 ED 需先实测；若架构空间封顶仍 < 327.18 → 三振规则三层提问（体系/边界/指标）→ 如实负结果（注明"若放宽至 X 可达"）。
- 低温风险：−20 ℃ 保持率 ≥ 0.9 对电解液传输/动力学苛刻；杠杆=配方 σ/D（可调）+ 小粒径 + 薄电极。若受参数集温敏函数限制 → 三振提问。
- SEI 风险：SEI 动力学参数锁定（涂层属材料设计，消融禁用）→ 仅架构缓解（N/P、粒径、局部电流密度）；SKILL 信号级参考：Chen2020 SEI 动力学 ×0.1 时 100 圈 449→385 nm——基线 100 圈约 449 nm 量级，500 圈 ≤550 nm 上限可能紧张，第一优先验证。
- 4C 析锂：45 ℃ 环境有利；杠杆=σ_e↑ / 负极粒径↓ / 孔隙与 N-P 平衡；安全评估必须 lumped 热耦合（否则温升虚假）。
- 已知口径：Chen2020 初始为放电态（正极 27% 锂化）→ 首圈容量偏低属已知，不比首圈；标准 SEI 模型容量轨迹可能先升后饱和（伪象）→ 如实标注，可靠指标为 sei_thickness_nm_end；容量变化时同步更新 Nominal cell capacity [A.h]（=该设计实测 1C 放电容量，机械推导），保持 1C/4C 倍率定义诚实。

## 5. 领域依据（真实来源；不确定处标注领域经验）

- 参数集本体：Chen et al., "Development of Experimental Techniques and Parameterization of a Physico-Chemical Model for a Lithium-ion Battery", J. Electrochem. Soc. 167, 080534 (2020)（PyBaMM Chen2020 参数化）。
- 析锂判据（负极电位 < 0 V vs Li/Li⁺）：Waldmann, Hogg, Wohlfahrt-Mehrens, "Li plating as unwanted phenomenon in lithium-ion cells – A review", J. Power Sources 384 (2018) 107–124。
- 低温性能由电解液传输主导：Zhang, Xu, Jow, "The low temperature performance of Li-ion batteries", J. Power Sources 115 (2003) 137–140。
- SEI 生长（EC 还原，ec reaction limited 模型）：PyBaMM SEI 模型文档；Safari–Delacourt 类反应受限 SEI 建模——领域经验（无更精确来源处已标注）。
- 集流体/隔膜减薄提 ED、小粒径提倍率：领域经验（无精确来源）。

## 6. 修订历史

- 2026-08-25 初版（v1）。
