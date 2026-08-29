# 电芯设计规格书 (design_spec) — t4_r3

> 编号 VBF-T4R3-DS-01 | 生成日期 2026-08-26 | 值逐行标注来源; 未提供项如实写 "Not provided"; 无凭记忆数值。

## 1. 基本规格
| 项目 | 值 | 来源 |
|---|---|---|
| 电化学体系 | NMC族正极 / 石墨族负极 (OKane2022 基准参数集, LGM50 谱系) | param_dump_okane.json (基准集) [sourced] |
| 标称容量 | 5.0 Ah (仿真验证 5.0383 Ah @1C 25C DFN) | param_dump_okane.json / r7_V18_1c_25C_dfn.json:capacity_ah |
| 电压窗口 | 2.5 - 4.2 V | param_dump_okane.json |
| 电芯尺寸 | 电极 65 mm (高) x 1580 mm (宽, 展开) x 182.8 um (层叠厚度: 正极 75.6 + 负极 85.2 + 隔膜 8 + Al 8 + Cu 6 um) | param_dump_okane.json + r7_V18_energy.json:thickness_m |
| 壳体厚度 | Not provided (参数集中无壳体参数) | honest |
| 电解液配方 | 配方方向估计: sigma=2.2 S/m, D=6.0e-10 m2/s, t+=0.5 (无分子级添加剂候选 — 本案例为能级 Stage 3 起跑, 未走 Stage 2 分子漏斗) | r7_V18_params.json [estimated, 参数桥接] |
| 阳离子迁移数 | 0.5 (覆盖基准 0.2594) | 同上 |

## 2. 电极与隔膜
| 层 | 厚度 um | 孔隙率 | 材料/密度 kg/m3 | 来源 |
|---|---|---|---|---|
| 正极活性层 | 75.6 | 0.335 | 3262 | param_dump_okane.json |
| 负极活性层 | 85.2 | 0.25 | 1657 | param_dump_okane.json |
| 隔膜 | 8 (覆盖 12) | 0.47 | 397 | r7_V18_params.json + param_dump_okane.json |
| 正极集流体 | 8 (覆盖 16) | -- | Al 2700 | r7_V18_params.json + param_dump_okane.json |
| 负极集流体 | 6 (覆盖 12) | -- | Cu 8960 | r7_V18_params.json + param_dump_okane.json |
| N/P | 1.127 (厚度比 85.2/75.6; 化学计量容量密度参数未导出 — 厚度比近似; 最终设计保持基准电极厚度不变, 第2轮曾探索 N/P~1.18 未解镀锂) | -- | param_dump_okane.json [inferred] + log.jsonl R2 |

## 3. 工艺设计参数
| 参数 | 值 | 公式 | 来源 |
|---|---|---|---|
| 正极面密度 | 163.99 g/m2 | 厚度 x (1-孔隙率) x 密度 | [inferred 机械推导] |
| 负极面密度 | 105.88 g/m2 | 同上 | [inferred 机械推导] |
| 正极压实密度 | 2.169 g/cm3 | 密度 x (1-孔隙率) / 1000 (千倍易错点) | [inferred 机械推导] |
| 负极压实密度 | 1.243 g/cm3 | 同上 | [inferred 机械推导] |
| 电解液注入量 | 6.210 g | 孔隙体积 5.175 cm3 x 1.2 g/cm3 (电解液密度文献默认值, 填充系数 1.0 假设) | [estimated, 附注] |
| 化成建议 | 0.1C CC 至 4.2V, 25C, 2 次 | 设计推荐值; 产线实际值需调机 (附注) | [design recommended] |

## 4. 质量分解 (g/节)
| 层 | 质量 g | 公式 | 来源 |
|---|---|---|---|
| 正极活性层 | 16.842 | layer_kg_m2 x 面积 (0.1027 m2) | r7_V18_energy.json:layer_kg_m2 [sourced] |
| 负极活性层 | 10.874 | 同上 | [sourced] |
| Al 集流体 (8um) | 2.218 | 同上 | [sourced] |
| Cu 集流体 (6um) | 5.521 | 同上 | [sourced] |
| 隔膜 (8um) | 0.173 | 同上 (含 (1-孔隙率) 因子) | [sourced] |
| 合计 (合同口径) | 35.629 | 电解液不计入 (calc-energy 合同口径) | [sourced] |
| 电解液 (补充) | 6.210 | 孔隙体积 x 1.2 g/cm3 | [estimated] |
| 合计 (含电解液) | 41.838 | 补充口径 | [inferred] |

## 5. 性能验证 (逐项判定 vs entry-0 判据)
| 项目 | 值 | 判据 (entry-0, 逐字) | 判定 | 来源 |
|---|---|---|---|---|
| 1C 容量 (25C, DFN) | 5.0383 Ah | 标称 5.0 Ah (任务未设容量阈值) | ✓ 信息性通过 | r7_V18_1c_25C_dfn.json:capacity_ah |
| -20C 容量保持率 | 97.97% | min 95 | ✓ | bridge/r7_V18_lowT_retention.json [inferred] |
| 质量能量密度 | 514.8 Wh/kg | min 327.18 | ✓ | r7_V18_energy.json [sourced] |
| 体积能量密度 | 977.0 Wh/L | min 880 | ✓ | r7_V18_energy.json [sourced] |
| 4C 充电最高温度 | 330.45 K (57.30C) | max 333.15 K | ✓ | r7_V18_4C_45C_dfn.json:T_max_K |
| 4C 充电析锂 | 负极最负电位 +0.0155 V | plated = false (无电位<0) | ✓ (裕量薄, 附注) | r7_V18_4C_45C_dfn.json:anode_potential_v |

判定机械口径: verdict/evidence 由 `bda log-evaluate` R7 生成 (V18_ok_h50_elx_plus_DFN verdict=pass, checked=5)。

## 6. 设计说明 (本案例改动及依据, 引出自评估日志)
- **平台切换 (R4/R5)**: Chen2020 基线 4C45 必析锂 (负极电位末端跳水) 且 ED_L 843.5<880 — 动力学温度无关性使其无低温真实物理; 按"材料瓶颈升级"规则切换 OKane2022 (含 Arrhenius 温度依赖), log R4/R5 evaluate 有据。
- **薄化非活性层 (R1起)**: Al 16->8um / Cu 12->6um / 隔膜 12->8um 提升体积能量密度 (1C 能量受 ~5Ah 时间封顶, 加厚电极无用), 从 ED_L 843.5 -> 977.0。
- **颗粒细化 (R5起)**: 正 5.22->2.5um, 负 5.86->2.0um 增大反应面积, 恢复低温动力学 (h=40 时保持率从 85.2% 回到 95.65%)。
- **电解液输运方向 (R6)**: sigma=2.2 S/m / D=6.0e-10 / t+=0.5 为配方方向估计 [estimated], 参数桥接映射。
- **h 权衡 (R5-R7)**: h 升 -> T_max 降但低温保持率降 (低温放电期间电芯更冷); h=60 与 h=50 两候选 DFN 双过 (R7 evaluate 两候选均 pass), 推荐 h=50 (析锂裕量更宽 +0.0155 V), h=60 为保守冷却替代 (+0.0138 V)。
- **诚实附注**: 低温协议同参数含初始温度 — 无冷浸平衡模拟 (暖启动伪影); 镀锂裕量 ~15 mV 且与冷却热降额耦合 (h=40 区域失败, R5 有据); ED 为层叠合同口径 (电解液/壳体不计入); 循环寿命未仿真 (未跑老化协议)。
