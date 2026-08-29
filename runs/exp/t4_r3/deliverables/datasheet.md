# 技术参数表 (datasheet) — t4_r3

> 编号 VBF-T4R3-DSH-01 | 2026-08-26 | 面向客户字段; 值逐行标注来源; 未仿真项不虚构。

| 字段 | 值 | 来源 |
|---|---|---|
| 额定容量 (Ah) | 标称 5.0 Ah (参数集) / 仿真验证 5.0383 Ah (1C 25C DFN) | param_dump_okane.json + r7_V18_1c_25C_dfn.json |
| 标称电压 / 窗口 (V) | 中点电压 3.671 V / 窗口 2.5 - 4.2 V | r7_V18_energy.json:midpoint_voltage_v + param_dump_okane.json |
| 额定能量 (Wh) | 18.342 Wh (V·I 时间积分) | r7_V18_energy.json:energy_wh |
| 能量密度 (Wh/kg) | 514.8 Wh/kg (合同口径, 电解液不计入) | r7_V18_energy.json + calc-energy 质量公式 |
| 体积能量密度 (Wh/L) | 977.0 Wh/L (合同口径, 电解液/壳体不计入) | r7_V18_energy.json |
| 最大连续放电倍率 | 1C (~5.0 A 标称); 1C 全窗放电验证 5.0383 Ah @25C | 仿真结果 |
| 快充能力 | 4C@45C: T_max 330.45 K (57.30C), 无析锂 (负极最负电位 +0.0155 V, 裕量薄) | r7_V18_4C_45C_dfn.json |
| 工作温度范围 | 已验证点: 放电 -20C (保持率 97.97%) / 25C; 充电 45C。全连续区间未扫描; -20C 为暖启动协议 (无冷浸平衡), 真实冷浸保持率待物理验证 | 仿真输出, 诚实附注 |
| 循环寿命 | Not simulated (本案例未执行老化协议 — 不虚构) | honest |
| 安全判定 | 快充析锂: 未检出 (plated=false); 温升 330.45 K <= 333.15 K | r7_V18_4C_45C_dfn.json |
| 尺寸与质量 | 电极 65 mm x 1580 mm (展开); 层叠厚 182.8 um (隔膜 8 + Al 8 + Cu 6 um); 壳体厚 Not provided; 质量 35.629 g (合同口径, 不含电解液; 含电解液 41.839 g) | r7_V18_energy.json + param_dump_okane.json |

功率密度 6843.7 W/kg (V_OC²/(4·DCR)/mass, DCR 17.31 mΩ) | r7_V18_energy.json [sourced]
