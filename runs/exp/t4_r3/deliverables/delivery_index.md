# 交付包索引 (delivery_index) — t4_r3

> 编号 VBF-T4R3-IDX-01 | 生成日期 2026-08-26 | 只登记实际生成的文件 (先列目录后写行); 封面签名栏留空待手签。

**案例名称**: t4_r3 — 极寒环境装备电芯 (-20C 1C 放电容量保持率 >= 95%; 能量密度 >= 327.18 Wh/kg; 体积能量密度 >= 880 Wh/L)
**编号规则**: VBF-T4R3-<文档码>-<序号> (案例 ID 去非字母数字并大写: t4_r3 -> T4R3; 序号两位, 同一文档码内从 01 起)
**生成日期**: 2026-08-26
**签署**: 编制: ____   审核: ____   批准: ____

## 文档码对照表 (协议固定)
| 文档码 | 含义 | 对应文件 |
|---|---|---|
| DS | 规格书 | design_spec.md |
| BOM | 物料清单 | bom.xlsx |
| DSH | 技术参数表 | datasheet.md |
| CALC | 计算表 | calc.xlsx |
| DVPR | 设计验证报告 | dvpr.md |
| DFMEA | 失效分析 | dfmea.md |
| CAD | 结构模型 (可选交付物; 无头会话无用户澄清, 未请求 -> 未产出) | -- |

## 文件清单
| 文件名 | 编号 | 格式 | 来源说明 |
|---|---|---|---|
| design_spec.md | VBF-T4R3-DS-01 | md | 设计规格书, 按 deliverable-design-spec 规范生成; 数值来自参数集/仿真输出, 逐行标注 |
| design_spec.pdf | VBF-T4R3-DS-01 | pdf | design_spec.md 发布版 (reportlab 一次性脚本导出) |
| report.html | VBF-T4R3-DS-02 | html | bda render log.jsonl 七段自包含报告 (工作区根目录) |
| bom.xlsx | VBF-T4R3-BOM-01 | xlsx | 物料清单, 按 deliverable-bom 规范 (openpyxl); 双口径 g/节 + kg/kWh |
| bom.pdf | VBF-T4R3-BOM-01 | pdf | bom.xlsx 发布版 (reportlab 表格导出) |
| datasheet.md | VBF-T4R3-DSH-01 | md | 技术参数表, 按 deliverable-datasheet 规范 |
| datasheet.pdf | VBF-T4R3-DSH-01 | pdf | datasheet.md 发布版 |
| calc.xlsx | VBF-T4R3-CALC-01 | xlsx | 设计计算表, 按 deliverable-calc-sheet 规范 (5 sheet: 输入/容量能量/能量密度/NP与质量/工艺参数, 每单元格附公式与来源列) |
| calc.pdf | VBF-T4R3-CALC-01 | pdf | calc.xlsx 发布版 |
| dvpr.md | VBF-T4R3-DVPR-01 | md | 设计验证计划与报告 (虚拟试验版), 按 deliverable-dvpr 规范 |
| dvpr.pdf | VBF-T4R3-DVPR-01 | pdf | dvpr.md 发布版 |
| dfmea.md | VBF-T4R3-DFMEA-01 | md | 设计 FMEA (定性版, 仿真信号依据), 按 deliverable-dfmea 规范 |
| dfmea.pdf | VBF-T4R3-DFMEA-01 | pdf | dfmea.md 发布版 |
| delivery_index.md | VBF-T4R3-IDX-01 | md | 交付包索引 (本文件), 按 deliverable-package 规范; 只登记实际生成文件 |
| delivery_index.pdf | VBF-T4R3-IDX-01 | pdf | 交付包索引发布版 (工程蓝图配色封面 #14283C/#1E5A8A/#C97B3D) |
