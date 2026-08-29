# 设计验证计划与报告 (DVPR, 虚拟试验版) — t4_r3

> 编号 VBF-T4R3-DVPR-01 | 2026-08-26 | 每行一项: 项目/条件/结果值/判定/来源; 未覆盖条件如实写 N/A; 无凭记忆数值。

| 验证项 | 条件 | 结果值 | 判定 (vs entry-0 判据) | 来源 |
|---|---|---|---|---|
| 1C 放电容量 | run-pyamm 1C_discharge, 298.15 K, DFN | 5.0383 Ah | PASS (信息性; 任务无容量阈值) | cell/r7_V18_1c_25C_dfn.json:capacity_ah |
| 低温容量保持率 | lowT_discharge 1C, 253.15 K, DFN | 97.97% | PASS (>= 95%) | bridge/r7_V18_lowT_retention.json [inferred: 100xcap_LT/cap_25C] |
| 4C 快充温升 | 4C_charge_45C, lumped 热模型, DFN | T_max 330.45 K (相对 318.15 K 环境 +12.30 K) | PASS (<= 333.15 K) | cell/r7_V18_4C_45C_dfn.json:T_max_K |
| 4C 快充析锂 | 同上 + plating 模块, 负极电位 < 0 V 判定 | 负极最负电位 +0.0155 V | PASS (=false; 裕量薄附注) | cell/r7_V18_4C_45C_dfn.json:anode_potential_v |
| 能量密度 | calc-energy 合同口径 (1C 25C 积分) | 514.8 Wh/kg | PASS (>= 327.18) | cell/r7_V18_energy.json:energy_density_wh_kg |
| 体积能量密度 | 同上 | 977.0 Wh/L | PASS (>= 880) | cell/r7_V18_energy.json:energy_density_wh_l |
| 电压窗口 | 参数集上下限 | 2.5 - 4.2 V | PASS (设计继承基准窗口) | param_dump_okane.json |

| 未覆盖项 | 判定 |
|---|---|
| 针刺 / 过充至热失控 / 挤压 / 跌落 / 倍率脉冲内阻 | N/A (超出纯仿真边界, 需物理试验) |
| 循环寿命 | N/A (基准集具备老化模型但本案例未执行老化协议) |
| 低温充电析锂 | N/A (run-pyamm 无低温充电协议) |

**结论**: 已产出的 7 项虚拟验证全部 PASS (机械判定, bda log-evaluate R1-R7 审计可回放); 未覆盖项 6 项, 均为物理试验边界 — 论文局限性小节直接引用本表。备选 V17 (h=60) 同项亦全 PASS (保持率 97.91%, T_max 328.63 K, 负极 +0.0138 V)。
