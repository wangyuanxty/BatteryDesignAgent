# 交付物索引 Delivery Index

**案例**: VBF-T7-R1-FLASH · **生成日期**: 2026-08-25 · **版本**: 1.0

**封面信息**: 案例名 HEV 电池设计（虚拟电池工厂 VBF 协议，case t7_r1_flash）；编号方案 VBF-<CASE-ID-UPPER>-<doc-code>-<serial>；签名栏留空（虚拟测试版）。

## 文件清单

| 文件名 | 编号 | 格式 | 来源说明 |
|---|---|---|---|
| design_spec.md | VBF-T7R1FLASH-DS-001 | Markdown（可编辑源） | 电芯设计规格书：体系/电极/工艺/质量/性能验证（值取自参数集与仿真输出，逐行标注来源） |
| datasheet.md | VBF-T7R1FLASH-DSH-001 | Markdown（可编辑源） | 技术数据表：容量/能量/密度/快充/安全判定（循环寿命如实标注 Not simulated） |
| dvpr.md | VBF-T7R1FLASH-DVPR-001 | Markdown（可编辑源） | 设计验证计划与报告（虚拟测试版）：12 项验证，7 项仿真覆盖 + 4 项 N/A 如实标注 |
| dfmea.md | VBF-T7R1FLASH-DFMEA-001 | Markdown（可编辑源） | 设计 FMEA（定性版，基于仿真信号）：5 项失效模式 + 缓解措施 |
| bom.xlsx | VBF-T7R1FLASH-BOM-001 | Excel（可编辑源） | 物料清单：双口径 g/电芯 与 kg/kWh；导电剂/粘结剂配比文献默认并标注 |
| calc.xlsx | VBF-T7R1FLASH-CALC-001 | Excel（可编辑源） | 设计计算书：输入参数/容量能量/能量密度/NP与质量/工艺参数，逐格来源列 |
| design_spec.pdf | VBF-T7R1FLASH-DS-001 | PDF（发布版） | design_spec.md 的发布版 |
| datasheet.pdf | VBF-T7R1FLASH-DSH-001 | PDF（发布版） | datasheet.md 的发布版 |
| dvpr.pdf | VBF-T7R1FLASH-DVPR-001 | PDF（发布版） | dvpr.md 的发布版 |
| dfmea.pdf | VBF-T7R1FLASH-DFMEA-001 | PDF（发布版） | dfmea.md 的发布版 |
| bom.pdf | VBF-T7R1FLASH-BOM-001 | PDF（发布版） | bom.xlsx 的发布版（数据同源） |
| calc.pdf | VBF-T7R1FLASH-CALC-001 | PDF（发布版） | calc.xlsx 的发布版（数据同源） |

## 结论摘要

FC-4a 通过全部 4 项合同指标（机械判定，值均来自仿真输出文件）：
- 能量密度 **427.04 Wh/kg** ≥ 327.18 ✓（r3_fc4a_energy.json）
- 4C 快充无析锂 **+28.5 mV** ≥ 0 ✓（r3_fc4a_4c_dfn.json, DFN）
- SEI 100 圈 45 °C **496.9 nm** ≤ 550 ✓（r3_fc4a_aging45.json）
- 针刺 10 W 无热失控 **triggered=false**（T_max 309.2 / 322.7 K）✓（r3_fc4a_nail.json / _hot.json）

报告与审计链：`../report.html`（七节 HTML 报告，由 log.jsonl 确定性渲染）；`../log.jsonl`（全部审计条目）。
