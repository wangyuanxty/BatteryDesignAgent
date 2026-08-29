"""translate_report.py — one-shot: translate Chinese UI strings in report.py to English."""
import sys

sys.stdout.reconfigure(encoding="utf-8")

M = [
    ("无析锂", "No plating"), ("析锂风险", "Plating risk"), ("析锂允许", "Plating allowed"),
    ("未执行", "Not run"), ("全部达成", "All achieved"), ("部分未达成", "Partially achieved"),
    ("未提供", "Not provided"), ("暂无数据", "No data"), ("未判定", "Not judged"),
    ("材料设计", "Materials design"), ("电芯设计", "Cell design"), ("安全评估", "Safety assessment"),
    ("案例参数", "Case parameters"), ("能量密度", "Energy density"), ("放电容量", "Capacity"),
    ("最高温度", "Max temperature"), ("析锂判定", "Plating"), ("容量", "Capacity"),
    ("未设置目标", "No targets"), ("候选方案", "Candidates"), ("漏斗判定", "Judgment"),
    ("轮次总览", "Round overview"), ("趋势", "Trends"), ("通过", "Passed"), ("淘汰", "Rejected"),
    ("分歧", "Disputed"), ("真计算背书已跳过", "True-compute endorsement skipped"),
    ("未说明原因", "no reason given"), ("暂无推荐（未达标）", "No recommendation (not achieved)"),
    ("未设置单独目标（综合目标见其他阶段）", "No separate targets (see other stages)"),
    ("（设计目标未记录于 config.yaml）", "(design goal not recorded in config.yaml)"),
    ("真计算开启", "True compute ON"), ("真计算关闭", "True compute OFF"),
    ("候选：", "Candidates: "), ("曲线（模型 ", "curves (model "),
    ("能量密度趋势（evaluate 逐轮）", "Energy density trend (per evaluate round)"),
    ("T_max 趋势（evaluate 逐轮）", "T_max trend (per evaluate round)"),
    ("虚拟电池工厂设计报告", "Virtual Battery Factory Design Report"),
    ("阈值 ", "limit "), ("目标 ≥", "target ≥"), ("上限 ≤", "limit ≤"),
    ("结论 ", "Verdict "), ("Conclusion · 结论", "Conclusion"),
    ("候选", "Candidate"), ("部件", "Component"), ("类型", "Type"),
    ("说明", "Role"), ("内容", "Content"), ("处置", "Disposition"), ("理由", "Reason"),
    ("指标", "Metric"), ("数值", "Value"), ("参数", "Parameter"), ("值", "Value"),
    ("阶段1 · 总体设计规划", "Stage 1 · Overall planning"),
    ("阶段2 · 材料设计", "Stage 2 · Materials design"),
    ("阶段3 · 电芯设计", "Stage 3 · Cell design"),
    ("阶段4 · 安全评估", "Stage 4 · Safety assessment"),
    ("阶段5 · 真DFT/MD 验证", "Stage 5 · True DFT/MD endorsement"),
    ("分子 propose ", "mol. propose "), ("结构 propose ", "struct. propose "),
    ("放电曲线 ", "discharge curves "), ("4C 快充曲线 ", "4C charge curves "),
    ("背书 ", "Endorse "), ("终审 ", "Final "),
    ("达成 · PASS", "Achieved · PASS"),
    ("轮次", "Round"), ("阶段", "Stage"), ("候选数", "Cands"), ("析锂", "Plating"),
    ("STAGE 1 规划", "STAGE 1 Plan"), ("STAGE 2 材料", "STAGE 2 Materials"),
    ("STAGE 3 电芯", "STAGE 3 Cell"), ("STAGE 4 安全", "STAGE 4 Safety"),
    ("STAGE 5 真DFT/MD", "STAGE 5 True DFT/MD"),
    ('return "分子"', 'return "Molecule"'), ('return "体系"', 'return "System"'),
    ('return "配方"', 'return "Formulation"'), ('return "结构"', 'return "Structure"'),
    ('return "电解液"', 'return "Electrolyte"'), ('return "电芯体系"', 'return "Cell system"'),
    ('comps.append("隔膜")', 'comps.append("Separator")'),
    ('comps.append("集流体")', 'comps.append("Current collector")'),
    ('comps.append("电解液")', 'comps.append("Electrolyte")'),
    ('comps.append("正极")', 'comps.append("Cathode")'),
    ('comps.append("负极")', 'comps.append("Anode")'),
    ('if t in ("分子", "配方"):', 'if t in ("Molecule", "Formulation"):'),
    ('if t == "体系":', 'if t == "System":'),
    ("负极电位全程 ≥ 0 V", "anode potential >= 0 V throughout"),
    ("负极电位曾 < 0 V", "anode potential dipped below 0 V"),
    ("cell/ 目录下未发现 run-pyamm 曲线输出", "no run-pyamm curve outputs found under cell/"),
    ("（含 time_s 与 voltage_v / anode_potential_v 的 JSON）。",
     "(JSON with time_s and voltage_v / anode_potential_v)."),
    ('"；".join', '"; ".join'),
]

for path in [
    r".claude\skills\virtual-battery-factory\scripts\bda\report.py",
    r".claude\skills\virtual-battery-factory\scripts\build\lib\bda\report.py",
]:
    t = open(path, encoding="utf-8").read()
    n = 0
    for a, b in M:
        if a in t:
            t = t.replace(a, b)
            n += 1
    open(path, "w", encoding="utf-8").write(t)
    print(path, ":", n, "replacements")

# report remaining Chinese (informational)
import re
t = open(r".claude\skills\virtual-battery-factory\scripts\bda\report.py", encoding="utf-8").read()
rest = sorted(set(re.findall(r"[一-龥][^\"'`]*", t)))
print("remaining Chinese snippets:", len(rest))
for s in rest[:25]:
    print("  ", s[:70])
