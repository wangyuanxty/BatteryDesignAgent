"""t4_r3: build the deliverables package (7 docs: source + PDF) mechanically from tool-output files."""
import json
from pathlib import Path

import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from bda.store import CaseWorkspace

ws = CaseWorkspace("exp/t4_r3", root="runs")
DEL = ws.path / "deliverables"
DEL.mkdir(exist_ok=True)

def jload(p):
    return json.loads((ws.path / p).read_text(encoding="utf-8-sig"))

EN18 = jload("cell/r7_V18_energy.json")
EN17 = jload("cell/r7_V17_energy.json")
C25 = jload("cell/r7_V18_1c_25C_dfn.json")
CLT = jload("cell/r7_V18_1c_lowT_dfn.json")
C4C = jload("cell/r7_V18_4C_45C_dfn.json")
C4C17 = jload("cell/r7_V17_4C_45C_dfn.json")
RET = jload("bridge/r7_V18_lowT_retention.json")
RET17 = jload("bridge/r7_V17_lowT_retention.json")
DUMP = jload("param_dump_okane.json")

ap18 = min(C4C["anode_potential_v"])
ap17 = min(C4C17["anode_potential_v"])
area = EN18["area_m2"]
kwh = EN18["energy_wh"] / 1000.0
AREA = DUMP["Electrode height [m]"] * DUMP["Electrode width [m]"]
POR = (DUMP["Positive electrode porosity"], DUMP["Negative electrode porosity"], DUMP["Separator porosity"])
THK = (DUMP["Positive electrode thickness [m]"], DUMP["Negative electrode thickness [m]"])  # base electrodes, final design unchanged
SP = 8e-6  # final separator override
pore_cm3 = (THK[0] * POR[0] + THK[1] * POR[1] + SP * POR[2]) * AREA * 1e6   # cm3
elyte_g = pore_cm3 * 1.2                                                   # g, literature 1.2 g/cm3
LM = EN18["layer_kg_m2"]
m_pos, m_neg, m_al, m_cu, m_sep = (LM["positive_electrode"] * area * 1e3, LM["negative_electrode"] * area * 1e3,
                                   LM["positive_cc"] * area * 1e3, LM["negative_cc"] * area * 1e3,
                                   LM["separator"] * area * 1e3)
m_cell = m_pos + m_neg + m_al + m_cu + m_sep
m_cell_ely = m_cell + elyte_g
def kgelem(g):
    return g / 1000.0 / kwh
rs = lambda v, u: f"{v}{u}"
np_ratio = THK[1] / THK[0]
t18_c = C4C["T_max_K"] - 273.15

# ---------- BOM (xlsx) ----------
wb = openpyxl.Workbook()
sh = wb.active
sh.title = "bom"
sh.append(["组件", "材料", "质量 g/节", "kg/kWh", "来源标注"])
rows = [
    ("正极活性层(合计)", "NMC族活性层 (OKane2022 基准参数集)", True, None, "layer_kg_m2 x 面积 x (1-孔隙率) x 密度 [sourced: cell/r7_V18_energy.json:layer_kg_m2.positive_electrode]"),
    ("正极活性材料", "NMC族 (family per OKane2022 base set)", False, 0.96, "层质量 x 0.96 文献默认活性比 [estimated: 基准集无组分细分参数]"),
    ("正极导电剂", "炭黑类", False, 0.02, "层质量 x 0.02 文献默认 [estimated]"),
    ("正极粘结剂", "PVDF类", False, 0.02, "层质量 x 0.02 文献默认 [estimated]"),
    ("负极活性层(合计)", "石墨族活性层", True, None, "layer_kg_m2 x 面积 [sourced: ...layer_kg_m2.negative_electrode]"),
    ("负极活性材料", "石墨族 (family per OKane2022 base set)", False, 0.96, "层质量 x 0.96 文献默认活性比 [estimated]"),
    ("负极导电剂", "炭黑类", False, 0.01, "层质量 x 0.01 文献默认 [estimated]"),
    ("负极粘结剂", "CMC/SBR类", False, 0.03, "层质量 x 0.03 文献默认 [estimated]"),
    ("隔膜", "隔膜 (8 um, 孔隙率 0.47)", 8, None, "layer_kg_m2 = 8e-6 x (1-0.47) x 397 [sourced]"),
    ("电解液", "电解液 (配方方向估计, 密度按文献 1.2 g/cm3)", 9, None, "孔隙体积 x 1.2 g/cm3 [estimated: 密度文献默认值附标注]"),
    ("正极集流体", "铝箔 (8 um)", 10, None, "8e-6 x 2700 x 面积 [sourced]"),
    ("负极集流体", "铜箔 (6 um)", 11, None, "6e-6 x 8960 x 面积 [sourced]"),
    ("壳体与极耳", "--", 12, None, "Not modeled"),
]
for r in rows:
    lay, name, kind, frac, src = r[0], r[1], r[2], r[3], r[4]
    if kind is True:
        g = {"正极活性层(合计)": m_pos, "负极活性层(合计)": m_neg}[lay]
        sh.append([lay, name, round(g, 3), round(kgelem(g), 4), src])
    elif kind is False:
        base = {"正极活性材料": m_pos, "正极导电剂": m_pos, "正极粘结剂": m_pos,
                "负极活性材料": m_neg, "负极导电剂": m_neg, "负极粘结剂": m_neg}[lay]
        g = base * frac
        sh.append([lay, name, round(g, 3), round(kgelem(g), 4), src])
    elif lay == "隔膜":
        sh.append([lay, name, round(m_sep, 3), round(kgelem(m_sep), 4), src])
    elif lay == "电解液":
        sh.append([lay, name, round(elyte_g, 3), round(kgelem(elyte_g), 4), src])
    elif lay == "正极集流体":
        sh.append([lay, name, round(m_al, 3), round(kgelem(m_al), 4), src])
    elif lay == "负极集流体":
        sh.append([lay, name, round(m_cu, 3), round(kgelem(m_cu), 4), src])
    else:
        sh.append([lay, name, "Not modeled", "Not modeled", "壳体/极耳未建模 [honest]"])
sh.append(["合计(不含电解液, 合同口径=calc-energy)", "--", round(m_cell, 3), round(kgelem(m_cell), 4),
           "cell/r7_V18_energy.json:mass_kg x1000 [sourced]"])
sh.append(["合计(含电解液, 补充口径)", "--", round(m_cell_ely, 3), round(kgelem(m_cell_ely), 4), "补充计算, 电解液密度文献默认 [estimated]"])
sh.append(["电池能量", "--", "", f"{EN18['energy_wh']:.6f} kWh", "calc-energy 时间积分 V·I [sourced]"])
sh2 = wb.create_sheet("caliber_notes")
sh2.append(["口径说明"])
for t in ["电解液密度 1.2 g/cm3 为文献默认值 (基准参数集无电解液密度参数) [estimated]",
          "电极活性/导电/粘结剂质量拆分比例 (0.96/0.02/0.02, 0.96/0.01/0.03) 为文献默认值, 基准集无组分细分参数 [estimated]",
          "质量/能量口径: calc-energy 合同口径 = 电解液不计入质量与体积 (electrolyte_included:false) [sourced]",
          "kg/kWh = 质量g /1000 / 电池能量kWh (电池能量 0.018342 kWh, 来自 1C 25C DFN 放电积分) [inferred]",
          "壳体/极耳 Not modeled [honest]"]:
    sh2.append([t])
wb.save(DEL / "bom.xlsx")

# ---------- CALC (xlsx) ----------
def sheet(name):
    w2.create_sheet(name)
    return w2[name]
w2 = openpyxl.Workbook()
s1 = w2.active
s1.title = "input_parameters"
s1.append(["参数", "取值", "单位", "来源"])
inp = [
    ("正极集流体厚度", 8, "um", "r7_V18_params.json (覆盖基准 16um) [sourced]"),
    ("负极集流体厚度", 6, "um", "r7_V18_params.json (覆盖基准 12um) [sourced]"),
    ("隔膜厚度", 8, "um", "r7_V18_params.json (覆盖基准 12um) [sourced]"),
    ("总换热系数 h", 50, "W/m2/K", "r7_V18_params.json (覆盖基准 10) [sourced]"),
    ("负极颗粒半径", 2.0, "um", "r7_V18_params.json (覆盖基准 5.86) [sourced]"),
    ("正极颗粒半径", 2.5, "um", "r7_V18_params.json (覆盖基准 5.22) [sourced]"),
    ("电解液电导率 sigma", 2.2, "S/m", "r7_V18_params.json (覆盖基准 ~0.31) [estimated: 配方方向估计, 参数桥接]"),
    ("电解液扩散系数 D", 6.0e-10, "m2/s", "r7_V18_params.json [estimated: 配方方向估计]"),
    ("阳离子迁移数 t+", 0.5, "--", "r7_V18_params.json (覆盖基准 0.2594) [estimated]"),
    ("正极厚度", 75.6, "um", "param_dump_okane.json (基准, 未覆盖) [sourced]"),
    ("负极厚度", 85.2, "um", "param_dump_okane.json (基准, 未覆盖) [sourced]"),
    ("正/负/隔膜孔隙率", "0.335/0.25/0.47", "--", "param_dump_okane.json [sourced]"),
    ("正/负/隔膜密度", "3262/1657/397", "kg/m3", "param_dump_okane.json [sourced]"),
    ("Al/Cu 集流体密度", "2700/8960", "kg/m3", "param_dump_okane.json [sourced]"),
    ("电极高度 x 宽度", "0.065 x 1.58", "m", "param_dump_okane.json [sourced]"),
    ("标称容量", 5.0, "Ah", "param_dump_okane.json [sourced]"),
    ("电压窗口", "2.5 - 4.2", "V", "param_dump_okane.json [sourced]"),
    ("基准参数集", "OKane2022", "--", "run-pyamm --base OKane2022 [sourced]"),
]
for k, v, u, src in inp:
    s1.append([k, v, u, src])

s2 = sheet("capacity_and_energy")
s2.append(["项目", "数值", "公式", "来源"])
for row in [
    ("1C 放电容量 (25C, DFN)", f"{C25['capacity_ah']:.4f} Ah", "1C 恒流放电至电压窗口下限", "cell/r7_V18_1c_25C_dfn.json:capacity_ah [sourced]"),
    ("1C 放电容量 (-20C, DFN)", f"{CLT['capacity_ah']:.4f} Ah", "同参数, 环境 253.15 K", "cell/r7_V18_1c_lowT_dfn.json:capacity_ah [sourced]"),
    ("-20C 容量保持率", f"{RET['lowT_retention_1C_pct']:.2f} %", "100 x cap_LT / cap_25C", "bridge/r7_V18_lowT_retention.json [inferred, 机械推导]"),
    ("电池能量", f"{EN18['energy_wh']:.4f} Wh", "∫V·I_1C dt /3600, I_1C=5.0A 标称", "cell/r7_V18_energy.json:energy_wh [sourced]"),
]:
    s2.append(row)

s3 = sheet("energy_density")
s3.append(["项目", "数值", "公式", "来源"])
for row in [
    ("电池质量(合同口径)", f"{EN18['mass_kg']*1000:.3f} g", "Σ 层厚 x (1-孔隙率) x 密度 x 面积 (电解液不计入)", "cell/r7_V18_energy.json:mass_kg [sourced]"),
    ("电池体积(合同口径)", f"{EN18['volume_m3']*1e6:.3f} cm3", "Σ 层厚 x 面积 (电解液/壳体不计入)", "cell/r7_V18_energy.json:volume_m3 [sourced]"),
    ("质量能量密度", f"{EN18['energy_density_wh_kg']:.1f} Wh/kg", "能量 Wh / 质量 kg", "cell/r7_V18_energy.json:energy_density_wh_kg [sourced]"),
    ("体积能量密度", f"{EN18['energy_density_wh_l']:.1f} Wh/L", "能量 Wh / 体积 m3 /1000", "cell/r7_V18_energy.json:energy_density_wh_l [sourced]"),
]:
    s3.append(row)

s4 = sheet("np_and_mass")
s4.append(["项目", "数值", "公式", "来源"])
s4.append(["N/P (厚度比)", f"{np_ratio:.3f}", "负极厚 85.2 / 正极厚 75.6 um (最终设计保持基准电极厚度不变); 化学计量容量密度未由参数导出, 为厚度比近似", "param_dump_okane.json [inferred, 附注]"])
for name, lm, den in [("正极活性层", LM["positive_electrode"], "75.6um x (1-0.335) x 3262"),
                      ("负极活性层", LM["negative_electrode"], "85.2um x (1-0.25) x 1657"),
                      ("Al集流体(8um)", LM["positive_cc"], "8um x 2700"),
                      ("Cu集流体(6um)", LM["negative_cc"], "6um x 8960"),
                      ("隔膜(8um)", LM["separator"], "8um x (1-0.47) x 397")]:
    s4.append([name + " kg/m2", round(lm, 6), den, "cell/r7_V18_energy.json:layer_kg_m2 [sourced]"])
    s4.append([name + " g/节", round(lm * area * 1e3, 3), "kg/m2 x 面积(0.1027 m2) x1000", "[inferred 机械推导]"])

s5 = sheet("process_parameters")
s5.append(["项目", "数值", "公式(单位注意点)", "来源"])
for row in [
    ("正极面密度", f"{LM['positive_electrode']*1000:.2f} g/m2", "厚度 x (1-孔隙率) x 密度", "[inferred 机械推导]"),
    ("负极面密度", f"{LM['negative_electrode']*1000:.2f} g/m2", "厚度 x (1-孔隙率) x 密度", "[inferred 机械推导]"),
    ("正极压实密度", f"{DUMP['Positive electrode density [kg.m-3]']*(1-POR[0])/1000:.3f} g/cm3", "密度 x (1-孔隙率) / 1000 (千倍除错点)", "[inferred 机械推导]"),
    ("负极压实密度", f"{DUMP['Negative electrode density [kg.m-3]']*(1-POR[1])/1000:.3f} g/cm3", "密度 x (1-孔隙率) / 1000", "[inferred 机械推导]"),
    ("电解液注入量", f"{elyte_g:.3f} g", f"孔隙体积 {pore_cm3:.3f} cm3 x 电解液密度 1.2 g/cm3 (填充系数 1.0 假设)", "[estimated: 密度文献默认值, 填充系数假设]"),
    ("化成建议", "0.1C CC 至 4.2V, 25C, 2 次", "设计推荐值; 产线实际值需调机", "[design recommended, 附注]"),
]:
    s5.append(row)
w2.save(DEL / "calc.xlsx")

# ---------- markdown docs ----------
DATE = "2026-08-26"
CASE = "t4_r3"

def emit(name, text):
    (DEL / name).write_text(text, encoding="utf-8")

design_spec = f"""# 电芯设计规格书 (design_spec) — {CASE}

> 编号 VBF-T4R3-DS-01 | 生成日期 {DATE} | 值逐行标注来源; 未提供项如实写 "Not provided"; 无凭记忆数值。

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
| N/P | {np_ratio:.3f} (厚度比 85.2/75.6; 化学计量容量密度参数未导出 — 厚度比近似; 最终设计保持基准电极厚度不变, 第2轮曾探索 N/P~1.18 未解镀锂) | -- | param_dump_okane.json [inferred] + log.jsonl R2 |

## 3. 工艺设计参数
| 参数 | 值 | 公式 | 来源 |
|---|---|---|---|
| 正极面密度 | {LM['positive_electrode']*1000:.2f} g/m2 | 厚度 x (1-孔隙率) x 密度 | [inferred 机械推导] |
| 负极面密度 | {LM['negative_electrode']*1000:.2f} g/m2 | 同上 | [inferred 机械推导] |
| 正极压实密度 | {DUMP['Positive electrode density [kg.m-3]']*(1-POR[0])/1000:.3f} g/cm3 | 密度 x (1-孔隙率) / 1000 (千倍易错点) | [inferred 机械推导] |
| 负极压实密度 | {DUMP['Negative electrode density [kg.m-3]']*(1-POR[1])/1000:.3f} g/cm3 | 同上 | [inferred 机械推导] |
| 电解液注入量 | {elyte_g:.3f} g | 孔隙体积 {pore_cm3:.3f} cm3 x 1.2 g/cm3 (电解液密度文献默认值, 填充系数 1.0 假设) | [estimated, 附注] |
| 化成建议 | 0.1C CC 至 4.2V, 25C, 2 次 | 设计推荐值; 产线实际值需调机 (附注) | [design recommended] |

## 4. 质量分解 (g/节)
| 层 | 质量 g | 公式 | 来源 |
|---|---|---|---|
| 正极活性层 | {m_pos:.3f} | layer_kg_m2 x 面积 (0.1027 m2) | r7_V18_energy.json:layer_kg_m2 [sourced] |
| 负极活性层 | {m_neg:.3f} | 同上 | [sourced] |
| Al 集流体 (8um) | {m_al:.3f} | 同上 | [sourced] |
| Cu 集流体 (6um) | {m_cu:.3f} | 同上 | [sourced] |
| 隔膜 (8um) | {m_sep:.3f} | 同上 (含 (1-孔隙率) 因子) | [sourced] |
| 合计 (合同口径) | {m_cell:.3f} | 电解液不计入 (calc-energy 合同口径) | [sourced] |
| 电解液 (补充) | {elyte_g:.3f} | 孔隙体积 x 1.2 g/cm3 | [estimated] |
| 合计 (含电解液) | {m_cell_ely:.3f} | 补充口径 | [inferred] |

## 5. 性能验证 (逐项判定 vs entry-0 判据)
| 项目 | 值 | 判据 (entry-0, 逐字) | 判定 | 来源 |
|---|---|---|---|---|
| 1C 容量 (25C, DFN) | {C25['capacity_ah']:.4f} Ah | 标称 5.0 Ah (任务未设容量阈值) | ✓ 信息性通过 | r7_V18_1c_25C_dfn.json:capacity_ah |
| -20C 容量保持率 | {RET['lowT_retention_1C_pct']:.2f}% | min 95 | ✓ | bridge/r7_V18_lowT_retention.json [inferred] |
| 质量能量密度 | {EN18['energy_density_wh_kg']:.1f} Wh/kg | min 327.18 | ✓ | r7_V18_energy.json [sourced] |
| 体积能量密度 | {EN18['energy_density_wh_l']:.1f} Wh/L | min 880 | ✓ | r7_V18_energy.json [sourced] |
| 4C 充电最高温度 | {C4C['T_max_K']:.2f} K ({t18_c:.2f}C) | max 333.15 K | ✓ | r7_V18_4C_45C_dfn.json:T_max_K |
| 4C 充电析锂 | 负极最负电位 {ap18:+.4f} V | plated = false (无电位<0) | ✓ (裕量薄, 附注) | r7_V18_4C_45C_dfn.json:anode_potential_v |

判定机械口径: verdict/evidence 由 `bda log-evaluate` R7 生成 (V18_ok_h50_elx_plus_DFN verdict=pass, checked=5)。

## 6. 设计说明 (本案例改动及依据, 引出自评估日志)
- **平台切换 (R4/R5)**: Chen2020 基线 4C45 必析锂 (负极电位末端跳水) 且 ED_L 843.5<880 — 动力学温度无关性使其无低温真实物理; 按"材料瓶颈升级"规则切换 OKane2022 (含 Arrhenius 温度依赖), log R4/R5 evaluate 有据。
- **薄化非活性层 (R1起)**: Al 16->8um / Cu 12->6um / 隔膜 12->8um 提升体积能量密度 (1C 能量受 ~5Ah 时间封顶, 加厚电极无用), 从 ED_L 843.5 -> 977.0。
- **颗粒细化 (R5起)**: 正 5.22->2.5um, 负 5.86->2.0um 增大反应面积, 恢复低温动力学 (h=40 时保持率从 85.2% 回到 95.65%)。
- **电解液输运方向 (R6)**: sigma=2.2 S/m / D=6.0e-10 / t+=0.5 为配方方向估计 [estimated], 参数桥接映射。
- **h 权衡 (R5-R7)**: h 升 -> T_max 降但低温保持率降 (低温放电期间电芯更冷); h=60 与 h=50 两候选 DFN 双过 (R7 evaluate 两候选均 pass), 推荐 h=50 (析锂裕量更宽 +0.0155 V), h=60 为保守冷却替代 (+0.0138 V)。
- **诚实附注**: 低温协议同参数含初始温度 — 无冷浸平衡模拟 (暖启动伪影); 镀锂裕量 ~15 mV 且与冷却热降额耦合 (h=40 区域失败, R5 有据); ED 为层叠合同口径 (电解液/壳体不计入); 循环寿命未仿真 (未跑老化协议)。
"""
emit("design_spec.md", design_spec)

datasheet = f"""# 技术参数表 (datasheet) — {CASE}

> 编号 VBF-T4R3-DSH-01 | {DATE} | 面向客户字段; 值逐行标注来源; 未仿真项不虚构。

| 字段 | 值 | 来源 |
|---|---|---|
| 额定容量 (Ah) | 标称 5.0 Ah (参数集) / 仿真验证 5.0383 Ah (1C 25C DFN) | param_dump_okane.json + r7_V18_1c_25C_dfn.json |
| 标称电压 / 窗口 (V) | 中点电压 3.671 V / 窗口 2.5 - 4.2 V | r7_V18_energy.json:midpoint_voltage_v + param_dump_okane.json |
| 额定能量 (Wh) | 18.342 Wh (V·I 时间积分) | r7_V18_energy.json:energy_wh |
| 能量密度 (Wh/kg) | 514.8 Wh/kg (合同口径, 电解液不计入) | r7_V18_energy.json + calc-energy 质量公式 |
| 体积能量密度 (Wh/L) | 977.0 Wh/L (合同口径, 电解液/壳体不计入) | r7_V18_energy.json |
| 最大连续放电倍率 | 1C (~5.0 A 标称); 1C 全窗放电验证 5.0383 Ah @25C | 仿真结果 |
| 快充能力 | 4C@45C: T_max 330.45 K ({t18_c:.2f}C), 无析锂 (负极最负电位 {ap18:+.4f} V, 裕量薄) | r7_V18_4C_45C_dfn.json |
| 工作温度范围 | 已验证点: 放电 -20C (保持率 97.97%) / 25C; 充电 45C。全连续区间未扫描; -20C 为暖启动协议 (无冷浸平衡), 真实冷浸保持率待物理验证 | 仿真输出, 诚实附注 |
| 循环寿命 | Not simulated (本案例未执行老化协议 — 不虚构) | honest |
| 安全判定 | 快充析锂: 未检出 (plated=false); 温升 330.45 K <= 333.15 K | r7_V18_4C_45C_dfn.json |
| 尺寸与质量 | 电极 65 mm x 1580 mm (展开); 层叠厚 182.8 um (隔膜 8 + Al 8 + Cu 6 um); 壳体厚 Not provided; 质量 35.629 g (合同口径, 不含电解液; 含电解液 41.839 g) | r7_V18_energy.json + param_dump_okane.json |

功率密度 6843.7 W/kg (V_OC²/(4·DCR)/mass, DCR 17.31 mΩ) | r7_V18_energy.json [sourced]
"""
emit("datasheet.md", datasheet)

dvpr = f"""# 设计验证计划与报告 (DVPR, 虚拟试验版) — {CASE}

> 编号 VBF-T4R3-DVPR-01 | {DATE} | 每行一项: 项目/条件/结果值/判定/来源; 未覆盖条件如实写 N/A; 无凭记忆数值。

| 验证项 | 条件 | 结果值 | 判定 (vs entry-0 判据) | 来源 |
|---|---|---|---|---|
| 1C 放电容量 | run-pyamm 1C_discharge, 298.15 K, DFN | {C25['capacity_ah']:.4f} Ah | PASS (信息性; 任务无容量阈值) | cell/r7_V18_1c_25C_dfn.json:capacity_ah |
| 低温容量保持率 | lowT_discharge 1C, 253.15 K, DFN | {RET['lowT_retention_1C_pct']:.2f}% | PASS (>= 95%) | bridge/r7_V18_lowT_retention.json [inferred: 100xcap_LT/cap_25C] |
| 4C 快充温升 | 4C_charge_45C, lumped 热模型, DFN | T_max {C4C['T_max_K']:.2f} K (相对 318.15 K 环境 +{C4C['T_max_K']-318.15:.2f} K) | PASS (<= 333.15 K) | cell/r7_V18_4C_45C_dfn.json:T_max_K |
| 4C 快充析锂 | 同上 + plating 模块, 负极电位 < 0 V 判定 | 负极最负电位 {ap18:+.4f} V | PASS (=false; 裕量薄附注) | cell/r7_V18_4C_45C_dfn.json:anode_potential_v |
| 能量密度 | calc-energy 合同口径 (1C 25C 积分) | {EN18['energy_density_wh_kg']:.1f} Wh/kg | PASS (>= 327.18) | cell/r7_V18_energy.json:energy_density_wh_kg |
| 体积能量密度 | 同上 | {EN18['energy_density_wh_l']:.1f} Wh/L | PASS (>= 880) | cell/r7_V18_energy.json:energy_density_wh_l |
| 电压窗口 | 参数集上下限 | 2.5 - 4.2 V | PASS (设计继承基准窗口) | param_dump_okane.json |

| 未覆盖项 | 判定 |
|---|---|
| 针刺 / 过充至热失控 / 挤压 / 跌落 / 倍率脉冲内阻 | N/A (超出纯仿真边界, 需物理试验) |
| 循环寿命 | N/A (基准集具备老化模型但本案例未执行老化协议) |
| 低温充电析锂 | N/A (run-pyamm 无低温充电协议) |

**结论**: 已产出的 7 项虚拟验证全部 PASS (机械判定, bda log-evaluate R1-R7 审计可回放); 未覆盖项 6 项, 均为物理试验边界 — 论文局限性小节直接引用本表。备选 V17 (h=60) 同项亦全 PASS (保持率 97.91%, T_max 328.63 K, 负极 {ap17:+.4f} V)。
"""
emit("dvpr.md", dvpr)

dfmea = f"""# 设计 FMEA (定性版, 基于仿真信号) — {CASE}

> 编号 VBF-T4R3-DFMEA-01 | {DATE} | 定性评级基于仿真风险信号; 标注 "qualitative version, based on simulation signals"; 无凭记忆数值。

| 失效模式 | 失效原因 | 仿真信号 (可检测性依据) | 定性严重度 S | 定性频度 O | 设计侧缓解建议 |
|---|---|---|---|---|---|
| 负极析锂 (快充) | 4C 充电末端负极表面电位贴近 0 V | anode_potential_v 最负值 {ap18:+.4f} V (< 0 即析锂); 裕量仅 ~15 mV, h=40 区域实溃 (R5 V13: -0.417 V) | High | Medium | 保持 h=50 设计点; 模组级充电热管理/预加热控制; 实测确认 |
| 温升过热 | 高倍率充电产热超冷却能力 | T_max 330.45 K vs 333.15 K 限, 裕量 +2.7 K | High | Low | 冷却降额保护 (h 不可低于 ~50 区间); 模组级散热验证 |
| 电解液高压氧化分解 | 4.2 V 上限窗口 | 电压窗口来自成熟基准集; 真 DFT HOMO/IE-EA 背书跳过 (real_compute=false) | Medium | Low | 维持 4.2 V; 后续真计算背书路线图 |
| 容量不足 | 活性层载量不足或传质受限 | 1C 5.0383 Ah vs 标称 5.0 Ah | Medium | Low | 面积/载量继承基准 (未改动) |
| 低温容量塌缩 | -20C 动力学/传质恶化 | lowT 保持率 97.97% (裕量 +2.97 pts); 暖启动伪影 (无冷浸平衡) 或侵蚀裕量 | Medium | Medium | 冷浸试验确认; 必要时预加热策略 (自产热) |
| 低温充电析锂 | -20C 充电未仿真 | 无低温充电协议输出 | High | Not simulated | 禁止无预加热的 -20C 快充; 物理试验必须项 |

**结论**: 最高风险项 = 快充析锂裕量薄 (+0.0155 V) 与低温冷浸保持率不确定性; 缓解措施已写入设计 (h=50 设计点 + 亚微米颗粒半径 + 输运标量提升 [estimated]); 完整 FMEA (制程/供应链失效) 标注 N/A (超出纯仿真边界)。
"""
emit("dfmea.md", dfmea)

# ---------- file list (single source of truth for index md + pdf) ----------
FILES = [
    ("design_spec.md", "VBF-T4R3-DS-01", "md", "设计规格书, 按 deliverable-design-spec 规范生成; 数值来自参数集/仿真输出, 逐行标注"),
    ("design_spec.pdf", "VBF-T4R3-DS-01", "pdf", "design_spec.md 发布版 (reportlab 一次性脚本导出)"),
    ("report.html", "VBF-T4R3-DS-02", "html", "bda render log.jsonl 七段自包含报告 (工作区根目录)"),
    ("bom.xlsx", "VBF-T4R3-BOM-01", "xlsx", "物料清单, 按 deliverable-bom 规范 (openpyxl); 双口径 g/节 + kg/kWh"),
    ("bom.pdf", "VBF-T4R3-BOM-01", "pdf", "bom.xlsx 发布版 (reportlab 表格导出)"),
    ("datasheet.md", "VBF-T4R3-DSH-01", "md", "技术参数表, 按 deliverable-datasheet 规范"),
    ("datasheet.pdf", "VBF-T4R3-DSH-01", "pdf", "datasheet.md 发布版"),
    ("calc.xlsx", "VBF-T4R3-CALC-01", "xlsx", "设计计算表, 按 deliverable-calc-sheet 规范 (5 sheet: 输入/容量能量/能量密度/NP与质量/工艺参数, 每单元格附公式与来源列)"),
    ("calc.pdf", "VBF-T4R3-CALC-01", "pdf", "calc.xlsx 发布版"),
    ("dvpr.md", "VBF-T4R3-DVPR-01", "md", "设计验证计划与报告 (虚拟试验版), 按 deliverable-dvpr 规范"),
    ("dvpr.pdf", "VBF-T4R3-DVPR-01", "pdf", "dvpr.md 发布版"),
    ("dfmea.md", "VBF-T4R3-DFMEA-01", "md", "设计 FMEA (定性版, 仿真信号依据), 按 deliverable-dfmea 规范"),
    ("dfmea.pdf", "VBF-T4R3-DFMEA-01", "pdf", "dfmea.md 发布版"),
    ("delivery_index.md", "VBF-T4R3-IDX-01", "md", "交付包索引 (本文件), 按 deliverable-package 规范; 只登记实际生成文件"),
    ("delivery_index.pdf", "VBF-T4R3-IDX-01", "pdf", "交付包索引发布版 (工程蓝图配色封面 #14283C/#1E5A8A/#C97B3D)"),
]

# ---------- PDFs ----------
def safe(s):
    return (str(s).replace("✓", "PASS").replace("✗", "FAIL").replace("≥", ">=").replace("≤", "<=")
            .replace("µm", "um").replace("×", "x").replace("°", " deg ").replace("±", "+/-")
            .replace("Ω", "ohm").replace("∫", "INT").replace("·", " * "))

styles = getSampleStyleSheet()
BLUE, MID, COPPER = colors.HexColor("#14283C"), colors.HexColor("#1E5A8A"), colors.HexColor("#C97B3D")

def build_pdf(path, title, subtitle, sections, cover=False):
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=14*mm, rightMargin=14*mm,
                            topMargin=14*mm, bottomMargin=14*mm,
                            title=title, author="virtual-battery-factory (headless)")
    story = []
    if cover:
        t = Table([[Paragraph(safe(title), styles["Title"])],
                   [Paragraph(safe(subtitle), styles["Normal"])]],
                  colWidths=[182*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BLUE),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("LINEBELOW", (0, 0), (-1, -1), 2, COPPER),
            ("TOPPADDING", (0, 0), (-1, -1), 18),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ]))
        story += [t, Spacer(1, 8*mm)]
    else:
        story += [Paragraph(safe(title), styles["Title"]), Spacer(1, 2*mm),
                  Paragraph(safe(subtitle), styles["Normal"]), Spacer(1, 5*mm)]
    for hdr, rows in sections:
        story.append(Paragraph(safe(hdr), styles["Heading2"]))
        hdr_row = rows[0]
        data = [[Paragraph(f"<b>{safe(c)}</b>", styles["Normal"]) for c in hdr_row]]
        for r in rows[1:]:
            data.append([Paragraph(safe(c), styles["Normal"]) for c in r])
        n = len(hdr_row)
        t = Table(data, colWidths=[182*mm/n]*n, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), MID),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA5B1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F6")]),
        ]))
        story += [t, Spacer(1, 4*mm)]
    doc.build(story)

def emit_pdf(base, title, sections, cover=False):
    build_pdf(DEL / f"{base}.pdf", title, f"Case {CASE} | {DATE} | generated by bda (headless) | PDF release",
              sections, cover=cover)

def parse_md_table(md):
    rows = []
    for line in md.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(c and set(c) <= {"-"} for c in cells):
                continue  # markdown separator row
            rows.append(cells)
    return rows

DESIGN_TABLES = []
DESIGN_TABLES = [("Basic specification", parse_md_table(design_spec.split("## 1.")[1].split("## 2.")[0])),
                 ("Electrodes and separator", parse_md_table(design_spec.split("## 2.")[1].split("## 3.")[0])),
                 ("Process design parameters", parse_md_table(design_spec.split("## 3.")[1].split("## 4.")[0])),
                 ("Mass breakdown (g/cell)", parse_md_table(design_spec.split("## 4.")[1].split("## 5.")[0])),
                 ("Performance verification vs entry-0 criteria", parse_md_table(design_spec.split("## 5.")[1].split("## 6.")[0])),
                 ("Design notes", [["Notes"], [design_spec.split("## 6.")[1].strip()[:1500]]])]
emit_pdf("design_spec", f"Cell Design Specification — {CASE}", DESIGN_TABLES)
emit_pdf("datasheet", f"Technical Datasheet — {CASE}",
         [(f"Datasheet — {CASE}", parse_md_table(datasheet))])
emit_pdf("dvpr", f"Design Verification Plan and Report (virtual) — {CASE}",
         [(f"DVPR — {CASE}", parse_md_table(dvpr))])
emit_pdf("dfmea", f"Design FMEA (qualitative, simulation-signal based) — {CASE}",
         [(f"DFMEA — {CASE}", parse_md_table(dfmea))])

# bom.pdf / calc.pdf — mirror the xlsx tables
wb3 = openpyxl.load_workbook(DEL / "bom.xlsx", read_only=True)
emit_pdf("bom", f"Bill of Materials — {CASE}",
         [(f"BOM g/cell and kg/kWh", [c for c in wb3["bom"].iter_rows(values_only=True)]),
          ("Caliber notes", [c for c in wb3["caliber_notes"].iter_rows(values_only=True)])])
wb4 = openpyxl.load_workbook(DEL / "calc.xlsx", read_only=True)
emit_pdf("calc", f"Design Calculation Sheet — {CASE}",
         [(n, list(wb4[n].iter_rows(values_only=True))) for n in wb4.sheetnames])

# ---------- delivery index ----------
INDEX_MD = f"""# 交付包索引 (delivery_index) — {CASE}

> 编号 VBF-T4R3-IDX-01 | 生成日期 {DATE} | 只登记实际生成的文件 (先列目录后写行); 封面签名栏留空待手签。

**案例名称**: {CASE} — 极寒环境装备电芯 (-20C 1C 放电容量保持率 >= 95%; 能量密度 >= 327.18 Wh/kg; 体积能量密度 >= 880 Wh/L)
**编号规则**: VBF-T4R3-<文档码>-<序号> (案例 ID 去非字母数字并大写: t4_r3 -> T4R3; 序号两位, 同一文档码内从 01 起)
**生成日期**: {DATE}
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
"""
for name, num, fmt, desc in FILES:
    INDEX_MD += f"| {name} | {num} | {fmt} | {desc} |\n"
emit("delivery_index.md", INDEX_MD)

idx_rows = [[f if not isinstance(f, str) else f for f in [name, num, fmt, desc]] for name, num, fmt, desc in FILES]
build_pdf(DEL / "delivery_index.pdf", f"Delivery Package Index — {CASE}", "Engineering blueprint cover | clickable file list follows",
          [("Document code reference", [["Code", "Meaning", "File"]] +
            [["DS", "Specification", "design_spec.md"], ["BOM", "Bill of Materials", "bom.xlsx"],
             ["DSH", "Datasheet", "datasheet.md"], ["CALC", "Calculation sheet", "calc.xlsx"],
             ["DVPR", "Design verification report", "dvpr.md"], ["DFMEA", "Failure analysis", "dfmea.md"],
             ["CAD", "Structure model (optional; not requested in headless session -> not produced)", "--"]]),
           ("File list (row-identical to delivery_index.md)", [["File", "Number", "Format", "Source"]]
            + idx_rows), ("Sign-off", [["Prepared"], [""], ["Reviewed"], [""], ["Approved"], [""]])],
          cover=True)

print("deliverables written:")
for p in sorted(DEL.iterdir()):
    print(f"  {p.name:22s} {p.stat().st_size:>8d} B")