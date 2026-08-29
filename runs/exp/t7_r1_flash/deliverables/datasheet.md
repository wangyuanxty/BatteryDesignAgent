# 技术数据表 Technical Datasheet

**案例**: VBF-T7R1FLASH-DSH-001 · **生成日期**: 2026-08-25 · **版本**: 1.0

| 字段 | 数值 | 来源 |
|---|---|---|
| 额定容量 (Ah) | 标称 5.0；仿真 1C 放电 5.038 | 参数集 + r3_fc4a_1c.json |
| 标称电压 / 窗口 (V) | 中点 4.007 / 2.5–4.2 | calc-energy midpoint_voltage_v / 参数集 |
| 额定能量 (Wh) | 17.95 | r3_fc4a_energy.json:energy_wh（∫V·I dt） |
| 能量密度 (Wh/kg) | 427.04 | 合同口径（见 calc.xlsx） |
| 体积能量密度 (Wh/L) | 883.8 | r3_fc4a_energy.json（合同口径，不含壳体） |
| 直流内阻 (mΩ) | 0.16 | calc-energy 机械推导（ΔV/ΔI at 10% t） |
| 最大持续放电倍率 | 1C 全放（仿真）；5C 级高倍率需 DFN 复核 | 1C 仿真结果（本任务未要求 5C） |
| 快充能力 | 4C（20 A）45 °C：负极电位 min 28.5 mV（≥0 无析锂），T_max 49.5 °C，4.2 V 截止前接受 0.43 Ah | r3_fc4a_4c_dfn.json |
| 工作温度范围 | 45 °C 高温老化/快充协议；25 °C 能量/1C 协议（仿真条件如实给出；宽温域未覆盖） | 各协议条件 |
| 循环寿命 | **Not simulated（需要老化模型之外的长循环模型）** | 如实标注，未编造 |
| 安全判定 | 针刺 10 W：无热失控（triggered=false，T_max 36.1 °C / 热态 49.5 °C）；4C 无析锂 | run-tr / run-pyamm 输出 |
| 尺寸与质量 | 层叠厚 0.2 mm × 1027 cm² 极片面积；质量 42.0 g（合同口径，不含电解液/壳体） | calc-energy |

**注意**：所有数值来自虚拟仿真（virtual battery factory），量产前需物理验证；未覆盖项（循环寿命、低温、壳体机械）如实标注。
