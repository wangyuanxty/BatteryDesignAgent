import json
import os

import pytest

from bda.store import append_entry
from bda.store import CaseWorkspace
from bda.report import render_report, export_csv
from bda.report import (
    _as_list,
    _attr_escape,
    _entry_stage,
    _fill_template,
    _fmt_num,
    _json_block,
    _stage_badge,
    _stage_range_badge,
    _threshold_text,
    _to_int,
    _verdict_class,
)


def _make_case(tmp_path):
    ws = CaseWorkspace("case1", root=str(tmp_path))
    append_entry(ws, {"round": 0, "criteria": {"T_max_C": 60, "plating_free": True}})
    append_entry(ws, {"round": 1, "action": "propose", "candidates": ["FEC"], "llm_reason": "seed"})
    append_entry(ws, {"round": 1, "action": "evaluate", "metrics": {"T_max_K": 325.0, "plated": False}, "verdict": "pass"})
    return ws


def _render(ws) -> str:
    html_path = render_report(str(ws.path))
    return open(html_path, encoding="utf-8").read()


@pytest.fixture
def full_case(tmp_path):
    """含 funnel/evaluate/endorse/final 四类条目的完整日志案例。"""
    ws = _make_case(tmp_path)
    append_entry(ws, {"action": "funnel", "passed": 3, "rejected": 2, "disputed": 1})
    append_entry(ws, {"action": "funnel", "passed": 1, "rejected": 0, "disputed": 1})
    append_entry(ws, {
        "round": 2, "action": "evaluate",
        "metrics": {"T_max_K": 318.0, "plated": False, "energy_density_Wh_kg": 500},
        "verdict": "pass",
    })
    append_entry(ws, {
        "action": "endorse",
        "candidates": [{"smiles": "CCOC(=O)O",
                        "endorsement": {"level": "ORCA-PBE0", "E_hartree": -343.12, "note": "stable"}}],
    })
    append_entry(ws, {"action": "final", "recommendation": "FEC 2wt%", "verdict": "达标"})
    return ws


def test_render_produces_self_contained_html(tmp_path):
    ws = _make_case(tmp_path)
    html_path = render_report(str(ws.path))
    html = open(html_path, encoding="utf-8").read()
    assert "<html" in html
    assert "60" in html  # criteria 阈值渲染
    assert "FEC" in html  # 候选渲染


def test_render_all_six_sections(tmp_path, full_case):
    ws = full_case
    html = _render(ws)
    for heading in ("任务概览与达标标准", "迭代轨迹", "漏斗统计", "阶段结果", "真DFT/MD 验证背书", "最终推荐", "设计说明"):
        assert heading in html
    assert "ORCA-PBE0" in html  # 真DFT/MD 验证背书中的 endorsement 值
    assert "energy_density_Wh_kg" in html  # 阶段结果表格渲染全部 metrics 键
    assert 'class="stat-num">4</div>' in html  # 漏斗计数跨条目求和（3+1）
    assert 'class="verdict ok"' in html  # final 达标结论


def test_render_missing_sections_show_placeholders(tmp_path):
    ws = _make_case(tmp_path)
    html = _render(ws)
    assert "暂无数据" in html
    assert "暂无推荐（预算耗尽或未达标）" in html


def test_export_csv(tmp_path):
    ws = _make_case(tmp_path)
    out_dir = str(ws.path / "csv")
    export_csv(str(ws.path), out_dir)
    files = os.listdir(out_dir)
    assert any(f.endswith(".csv") for f in files)


def test_blueprint_template_features(tmp_path):
    ws = _make_case(tmp_path)
    html = _render(ws)
    assert "SHEET 01" in html  # 图纸编号式 eyebrow
    assert "<details" in html  # 原生折叠卡片
    assert "{{" not in html  # 占位符无残留
    assert "--accent" in html  # 蓝图纸 CSS 令牌
    assert "prefers-reduced-motion" in html  # 尊重 reduced-motion
    assert "IntersectionObserver" in html  # 导航高亮


def test_round_cards_grouped_and_numbered(tmp_path, full_case):
    html = _render(full_case)
    assert "ROUND 01" in html
    assert "ROUND 02" in html
    assert '<details class="round" open>' in html  # 首轮默认展开
    assert "1 候选" in html  # 摘要行候选计数
    assert "T_max 318" in html  # 摘要行 T_max


def test_flow_overview_strip(tmp_path, full_case):
    """概览区流程一览条：四阶段徽章 + 由 log 条目机械推导的计数/结论摘要。"""
    html = _render(full_case)
    assert "流程一览" in html
    assert "阶段1 · 材料设计" in html
    assert "阶段2 · 电芯设计" in html
    assert "阶段3 · 安全评估" in html
    assert "真DFT/MD 验证" in html  # 收尾流程项更名为真DFT/MD 验证
    assert '<span class="badge stage end">STAGE 4</span>' in html
    assert "分子 propose 1 · funnel 2" in html
    assert "背书 1 · 终审 1 · 结论 达标" in html


def test_closing_phase_badge_is_stage_4(tmp_path, full_case):
    """endorse/final 对应徽章为 STAGE 4（end 铜色样式）；说明性文字为"真DFT/MD 验证"。"""
    html = _render(full_case)
    assert '<span class="badge stage end">STAGE 4</span>' in html
    assert "真DFT/MD 验证" in html
    assert "收尾" not in html
    assert '<span class="badge stage">STAGE 1</span>' in html  # 数字阶段徽章不受影响


def test_stage_badges_in_round_cards(tmp_path, full_case):
    """轮卡片带 STAGE 徽章：分子轮=STAGE 1；struct propose 轮=STAGE 2。"""
    html = _render(full_case)
    assert 'ROUND 01</span><span class="badge stage">STAGE 1</span>' in html
    # 独立工作区：与 full_case fixture 共享 tmp_path 会互相追加 log 条目
    ws = _make_case(tmp_path / "iso")
    append_entry(ws, {"round": 2, "action": "propose", "candidates": [
        {"struct": {"Positive electrode thickness [m]": 6.84e-5},
         "name": "结构方案B", "role": "正极减薄10%"}]})
    html2 = _render(ws)
    assert 'ROUND 02</span><span class="badge stage">STAGE 2</span>' in html2


def test_round_card_stage_range_badge(tmp_path):
    """跨阶段轮：轮卡片徽章显示 STAGE 2–3 范围（en dash），单阶段轮仍为单标。"""
    ws = _make_case(tmp_path)
    append_entry(ws, {"round": 2, "action": "propose", "candidates": [
        {"struct": {"Positive electrode thickness [m]": 6.84e-5},
         "name": "结构方案B", "role": "正极减薄10%"}]})
    append_entry(ws, {"round": 2, "action": "evaluate",
                      "metrics": {"T_max_K": 315.0, "plated": False},
                      "verdict": "pass", "note": "struct 方案结构安全评估"})
    html = _render(ws)
    assert 'ROUND 01</span><span class="badge stage">STAGE 1</span>' in html  # 单阶段轮=单标
    assert 'ROUND 02</span><span class="badge stage">STAGE 2–3</span>' in html  # 跨阶段轮=范围
    round02_tail = html.split("ROUND 02", 1)[1]
    assert '<span class="badge stage">STAGE 3</span>' not in round02_tail  # 不再仅显示最大阶段


def test_stage_badge_helpers_closing_phase_is_stage_4():
    """阶段 4（真DFT/MD 验证）沿用 end 铜色样式；范围徽章可含 4（如 STAGE 3–4）。"""
    assert _stage_badge(4) == '<span class="badge stage end">STAGE 4</span>'
    assert _stage_badge(1) == '<span class="badge stage">STAGE 1</span>'
    assert _stage_badge(None) == ""
    assert _stage_badge(0) == ""  # 0 不再是有效阶段键
    assert _stage_range_badge(4, 4) == _stage_badge(4)  # 单阶段 4 沿用 end 徽章
    assert _stage_range_badge(3, 4) == '<span class="badge stage">STAGE 3–4</span>'
    assert _stage_range_badge(2, 3) == '<span class="badge stage">STAGE 2–3</span>'
    assert _stage_range_badge(0, 4) == ""  # 无效阶段混入不产出范围


def test_entry_stage_maps_endorse_final_to_stage_4():
    """endorse/final 映射到阶段 4（真DFT/MD 验证）；其余阶段映射不变。"""
    assert _entry_stage({"action": "endorse"}) == 4
    assert _entry_stage({"action": "final"}) == 4
    assert _entry_stage({"action": "propose", "candidates": ["FEC"]}) == 1
    assert _entry_stage({"action": "funnel"}) == 1


def test_criteria_min_max_thresholds(tmp_path):
    ws = CaseWorkspace("case2", root=str(tmp_path))
    append_entry(ws, {"criteria": {
        "energy_density_wh_kg": {"min": 300.0},
        "T_max_K": {"max": 333.15},
        "plating_rule": "anode_potential_v < 0 V => plated=true",
    }})
    html = _render(ws)
    assert "≥ 300" in html
    assert "≤ 333.15" in html
    assert "plating_rule" in html


def test_kpi_colors_and_threshold_compare(tmp_path):
    ws = CaseWorkspace("case3", root=str(tmp_path))
    append_entry(ws, {"criteria": {
        "energy_density_wh_kg": {"min": 300.0},
        "T_max_K": {"max": 333.15},
    }})
    append_entry(ws, {"round": 1, "action": "evaluate",
                      "metrics": {"energy_density_wh_kg": 200.0, "capacity_ah": 4.6,
                                  "T_max_K": 400.0, "plated": True},
                      "verdict": "fail"})
    html = _render(ws)
    assert html.count("kpi-num bad") == 3  # 能量密度 / T_max / 析锂 均不达标
    assert "析锂风险" in html
    assert "阈值 ≥ 300" in html
    assert "阈值 ≤ 333.15" in html

    ws2 = CaseWorkspace("case3ok", root=str(tmp_path))
    append_entry(ws2, {"criteria": {
        "energy_density_wh_kg": {"min": 300.0},
        "T_max_K": {"max": 333.15},
    }})
    append_entry(ws2, {"round": 1, "action": "evaluate",
                       "metrics": {"energy_density_wh_kg": 327.0, "capacity_ah": 4.6,
                                   "T_max_K": 310.0, "plated": False},
                       "verdict": "pass"})
    html2 = _render(ws2)
    assert html2.count("kpi-num ok") == 3
    assert "无析锂" in html2
    assert "°C" in html2  # T_max 机械换算摄氏


def test_criteria_stage_layered_render(tmp_path):
    """新协议分层 criteria：每阶段一个区块，带阶段徽章与达成列（目标 vs 达成）。"""
    ws = CaseWorkspace("caseL", root=str(tmp_path))
    append_entry(ws, {"criteria": {
        "stage1": {"max_energy_ev": 0.0, "max_homo_ev": -6.0},
        "stage2": {"capacity_ah": {"min": 4.0}, "energy_density_wh_kg": {"min": 300.0}},
        "stage3": {"T_max_K": {"max": 333.15}, "plated": False},
        "meta": {"max_rounds": 30, "real_compute": False},
    }})
    append_entry(ws, {"round": 1, "action": "funnel", "passed": 3, "rejected": 2, "disputed": 0})
    append_entry(ws, {"round": 1, "action": "evaluate",
                      "metrics": {"capacity_ah": 4.6, "energy_density_wh_kg": 366.9,
                                  "T_max_K": 320.0, "plated": False},
                      "verdict": "pass"})
    html = _render(ws)
    assert "材料设计" in html and "电芯设计" in html and "安全评估" in html  # 阶段区块名
    assert "≤ 0 eV" in html and "≤ -6 eV" in html  # stage1 淘汰线（上限语义）
    assert "≥ 300" in html and "≤ 333.15" in html  # stage2/3 阈值
    assert '<span class="badge ok">✓</span>' in html  # 达成列达标行
    assert "全部达成" in html  # stage2/3 头部聚合徽章
    assert "无析锂" in html  # plated 阈值文本
    assert "预算 30 轮" in html  # meta 区块渲染
    assert "真计算关闭" in html


def test_criteria_legacy_flat_grouped_by_stage(tmp_path):
    """旧扁平 criteria 按键名归组：温度/析锂→stage3，空阶段如实提示。"""
    ws = _make_case(tmp_path)  # criteria: {"T_max_C": 60, "plating_free": True}
    html = _render(ws)
    assert "安全评估" in html
    assert "60" in html
    assert "未设置单独目标" in html  # stage1/stage2 空 → 如实提示，不伪造


def test_flow_goal_and_achieve_lines(tmp_path):
    """流程一览条每阶段带 目标/达成 两行（由 criteria 与 log 机械推导）。"""
    ws = CaseWorkspace("caseF", root=str(tmp_path))
    append_entry(ws, {"criteria": {
        "stage1": {"max_homo_ev": -6.0},
        "stage2": {"energy_density_wh_kg": {"min": 300.0}},
        "stage3": {"T_max_K": {"max": 333.15}, "plated": False},
    }})
    append_entry(ws, {"round": 1, "action": "funnel", "passed": 2, "rejected": 1, "disputed": 0})
    append_entry(ws, {"round": 1, "action": "evaluate",
                      "metrics": {"energy_density_wh_kg": 366.9, "T_max_K": 320.0, "plated": False},
                      "verdict": "pass"})
    html = _render(ws)
    assert '<span class="g-label">目标</span>' in html
    assert '<span class="g-label">达成</span>' in html
    assert "HOMO ≤ -6 eV" in html
    assert "能量密度 ≥ 300" in html
    assert "PASS 2 · DISP 0" in html
    assert '<b class="goal-ok">✓</b>' in html


def test_criteria_stage_achieve_bad_and_missing(tmp_path):
    """不达标行显示 ✗；无数据行显示破折号；无 funnel 的阶段头部为未执行。"""
    ws = CaseWorkspace("caseB", root=str(tmp_path))
    append_entry(ws, {"criteria": {
        "stage2": {"energy_density_wh_kg": {"min": 300.0}},
        "stage3": {"T_max_K": {"max": 333.15}, "plated": False},
    }})
    append_entry(ws, {"round": 1, "action": "evaluate",
                      "metrics": {"energy_density_wh_kg": 137.1, "T_max_K": 400.0},
                      "verdict": "fail"})
    html = _render(ws)
    assert '<span class="badge bad">✗</span>' in html
    assert "部分未达成" in html
    assert '<span class="badge mute">未执行</span>' in html  # stage1 无 funnel
    assert '<span class="badge mute">—</span>' in html  # plated 无数据


def test_threshold_text_bool():
    assert _threshold_text(False) == "无析锂"
    assert _threshold_text(True) == "析锂允许"


def test_funnel_dispositions_table(tmp_path):
    """funnel 逐候选处置表（dispositions）以表格渲染，status 映射徽章颜色。"""
    ws = CaseWorkspace("caseD", root=str(tmp_path))
    append_entry(ws, {"criteria": {"stage1": {"max_homo_ev": -6.0}}})
    append_entry(ws, {"round": 1, "action": "funnel", "passed": 2, "rejected": 1, "disputed": 1,
                      "detail": "一句话判定依据",
                      "dispositions": [
                          {"name": "FEC", "status": "passed", "reason": "HOMO 远低于线"},
                          {"name": "VC", "status": "rejected", "reason": "与FEC重叠"},
                          {"name": "PS", "status": "disputed", "reason": "双模型能量最优但 HOMO 靠后"},
                      ]})
    html = _render(ws)
    assert "候选" in html and "处置" in html and "理由" in html  # 表头
    assert '<span class="badge ok">passed</span>' in html
    assert '<span class="badge bad">rejected</span>' in html
    assert '<span class="badge warn">disputed</span>' in html
    assert "一句话判定依据" in html


def test_evaluate_comparison_table(tmp_path):
    """evaluate 多候选对比表（comparison）以 候选×指标×结论 表格渲染。"""
    ws = CaseWorkspace("caseC", root=str(tmp_path))
    append_entry(ws, {"criteria": {"stage2": {"energy_density_wh_kg": {"min": 300.0}}}})
    append_entry(ws, {"round": 2, "action": "evaluate",
                      "metrics": {"energy_density_wh_kg": 330.1, "T_max_K": 312.57, "plated": False},
                      "verdict": "pass",
                      "comparison": [
                          {"name": "结构方案B", "metrics": {"energy_density_wh_kg": 313.6, "T_max_K": 312.75, "plated": False}, "verdict": "pass"},
                          {"name": "结构方案D", "metrics": {"energy_density_wh_kg": 330.1, "T_max_K": 312.57, "plated": False}, "verdict": "pass"},
                      ],
                      "note": "D 负极加厚最优。"})
    html = _render(ws)
    assert "结构方案B" in html and "结构方案D" in html
    assert "313.6" in html
    assert "无析锂" in html  # 布尔指标按语义显示
    assert "D 负极加厚最优。" in html


def test_candidates_and_propose_tables(tmp_path):
    """候选以表格展示（候选/部件/类型/说明/内容）：SHEET 01 总表与轮次卡片均含部件归属。"""
    ws = _make_case(tmp_path)
    append_entry(ws, {"round": 1, "action": "propose", "candidates": [
        {"smiles": "FC1COC(=O)O1", "name": "FEC", "role": "氟代碳酸酯成膜剂", "source": "seed"},
        {"struct": {"Positive electrode thickness [m]": 6.84e-05}, "name": "结构方案B", "role": "正极减薄10%"},
        {"struct": {"Separator thickness [m]": 1e-05}, "name": "结构方案F", "role": "隔膜减薄"},
        {"struct": {"Positive current collector thickness [m]": 1e-05, "Negative current collector thickness [m]": 8e-06}, "name": "结构方案G", "role": "集流体减薄"},
        {"struct": {"Electrolyte conductivity [S.m-1]": 1.2}, "name": "溶剂方案H", "role": "高电导配方"},
        {"base": "Prada2013", "name": "体系LFP", "role": "LFP/石墨体系"},
    ]})
    html = _render(ws)
    assert "<th>候选</th>" in html and "<th>部件</th>" in html and "<th>类型</th>" in html
    assert "<td>分子</td>" in html and "<td>结构</td>" in html and "<td>体系</td>" in html
    assert "<td>电解液</td>" in html  # 分子/配方 → 电解液
    assert "<td>隔膜</td>" in html  # Separator → 隔膜
    assert "<td>集流体</td>" in html  # collector → 集流体
    assert "<td>正极</td>" in html  # Positive electrode → 正极
    assert "<td>电芯体系</td>" in html  # base → 电芯体系
    assert "Positive electrode thickness [m] = 6.840e-05" in html  # struct 参数内容（科学计数）
    assert "Prada2013" in html  # 体系内容
    assert "氟代碳酸酯成膜剂" in html  # 角色说明
    assert 'class="tbl cand"' in html  # 定列宽样式


def test_rounds_overview_table(tmp_path, full_case):
    """迭代轨迹顶部轮次总览表：轮次/阶段/候选数/指标/结论。"""
    html = _render(full_case)
    assert "轮次总览" in html
    assert "<th>能量密度 Wh/kg</th>" in html
    assert "R01" in html and "R02" in html
    assert "500" in html  # R2 evaluate 的 energy_density_Wh_kg 渲染
    assert "无析锂" in html


def test_trend_charts_with_threshold_lines(tmp_path):
    """逐轮趋势柱状图：能量密度含目标线、T_max 含上限线。"""
    ws = CaseWorkspace("caseT", root=str(tmp_path))
    append_entry(ws, {"criteria": {
        "stage2": {"energy_density_wh_kg": {"min": 300.0}},
        "stage3": {"T_max_K": {"max": 333.15}},
    }})
    append_entry(ws, {"round": 1, "action": "evaluate",
                      "metrics": {"energy_density_wh_kg": 327.0, "T_max_K": 312.62, "plated": False},
                      "verdict": "pass"})
    append_entry(ws, {"round": 2, "action": "evaluate",
                      "metrics": {"energy_density_wh_kg": 330.1, "T_max_K": 312.57, "plated": False},
                      "verdict": "pass"})
    html = _render(ws)
    assert "能量密度趋势" in html
    assert "T_max 趋势" in html
    assert 'class="bar"' in html
    assert 'class="thr"' in html  # 阈值参考线
    assert "目标 ≥ 300" in html
    assert "上限 ≤ 333.15" in html
    assert "R01" in html  # 柱标签


def test_cell_curve_svg_rendered(tmp_path):
    ws = _make_case(tmp_path)
    t = [i * 10.0 for i in range(30)]
    data = {
        "model_used": "SPMe",
        "time_s": t,
        "voltage_v": [4.0 - i * 0.02 for i in range(30)],
        "anode_potential_v": [0.1 - i * 0.004 for i in range(30)],
        "T_max_K": 312.65,
    }
    (ws.path / "cell" / "round_1_FEC_discharge.json").write_text(
        json.dumps(data), encoding="utf-8")
    html = _render(ws)
    assert '<svg class="plot"' in html
    assert "round_1_FEC_discharge.json" in html
    assert "MODEL SPMe" in html
    assert "data-series=" in html
    assert 'd="M' in html  # 直接由数据画 path
    assert "anode_potential_v [V]" in html
    assert "time [s]" in html
    assert "T_max =" in html
    assert "aria-label" in html


def test_cell_curve_edge_shapes(tmp_path):
    """恒定序列 / 恒定时间 / 超长降采样 / 仅负极电位：全部可渲染。"""
    ws = _make_case(tmp_path)
    cell = ws.path / "cell"
    (cell / "round_1_const_discharge.json").write_text(json.dumps({
        "model_used": "SPMe", "time_s": [0.0, 1.0, 2.0],
        "voltage_v": [3.7, 3.7, 3.7]}), encoding="utf-8")
    (cell / "round_1_zerotime.json").write_text(json.dumps({
        "model_used": "DFN", "time_s": [5.0, 5.0, 5.0],
        "voltage_v": [4.0, 3.9, 3.8]}), encoding="utf-8")
    (cell / "round_1_anode_only.json").write_text(json.dumps({
        "model_used": "DFN", "time_s": [0.0, 1.0],
        "anode_potential_v": [0.2, -0.1]}), encoding="utf-8")
    big_t = [i * 1.0 for i in range(900)]
    (cell / "round_1_long_discharge.json").write_text(json.dumps({
        "model_used": "DFN", "time_s": big_t,
        "voltage_v": [4.2 - i * 0.001 for i in range(900)]}), encoding="utf-8")
    html = _render(ws)
    assert html.count('<svg class="plot"') == 4
    assert "round_1_anode_only.json" in html
    assert "round_1_long_discharge.json" in html


def test_cell_non_curve_files_ignored(tmp_path):
    ws = _make_case(tmp_path)
    cell = ws.path / "cell"
    (cell / "round_1_summary.json").write_text(json.dumps({
        "mass_params_used": {}, "candidates": {}}), encoding="utf-8")
    (cell / "bad.json").write_text("not json at all", encoding="utf-8")
    (cell / "short.json").write_text(json.dumps(
        {"time_s": [0.0], "voltage_v": [4.0]}), encoding="utf-8")
    (cell / "mismatch.json").write_text(json.dumps(
        {"time_s": [0.0, 1.0], "voltage_v": [4.0]}), encoding="utf-8")
    (cell / "sub.json").mkdir()  # 目录伪装成曲线文件 → OSError 分支
    html = _render(ws)
    assert '<svg class="plot"' not in html
    assert "cell/ 目录下未发现" in html  # 如实说明，不伪造曲线


def test_render_without_log_or_cell_dir(tmp_path):
    d = tmp_path / "bare"
    d.mkdir()
    html_path = render_report(str(d))
    html = open(html_path, encoding="utf-8").read()
    assert "SHEET 01" in html  # 空日志也产出完整骨架
    assert "暂无数据" in html
    assert "未判定" in html


def test_endorse_skipped_shown_honestly(tmp_path):
    ws = _make_case(tmp_path)
    append_entry(ws, {"action": "endorse", "skipped": True,
                      "reason": "real_compute=false（交互调试）",
                      "candidates": [{"smiles": "CCO", "name": "X"}]})
    html = _render(ws)
    assert "真计算背书已跳过" in html
    assert "real_compute=false（交互调试）" in html
    assert "Skipped" in html


def test_endorse_plain_string_candidate(tmp_path):
    ws = _make_case(tmp_path)
    append_entry(ws, {"action": "endorse", "candidates": ["CCOC(=O)O"]})
    html = _render(ws)
    assert "CCOC(=O)O" in html
    assert '<pre class="term">{}</pre>' in html  # 无 endorsement 如实显示空对象


def test_html_escape_of_log_content(tmp_path):
    ws = _make_case(tmp_path)
    append_entry(ws, {"round": 1, "action": "evaluate",
                      "metrics": {"T_max_K": 320.0, "plated": False},
                      "verdict": "pass",
                      "note": "注入<script>alert(1)</script> & <b>bold</b>"})
    append_entry(ws, {"round": 2, "action": "propose", "candidates": ["A<B&C"]})
    html = _render(ws)
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<script>alert" not in html
    assert "&lt;b&gt;bold&lt;/b&gt;" in html
    assert "A&lt;B&amp;C" in html


def test_header_goal_from_config(tmp_path):
    ws = _make_case(tmp_path)
    (ws.path / "config.yaml").write_text(
        "goal: 设计一款能量密度 ≥ 300 Wh/kg 的电池\n", encoding="utf-8")
    html = _render(ws)
    assert "设计一款能量密度 ≥ 300 Wh/kg 的电池" in html


def test_header_goal_corrupt_config_fallback(tmp_path):
    ws = _make_case(tmp_path)
    (ws.path / "config.yaml").write_text("goal: [unclosed\n", encoding="utf-8")
    html = _render(ws)
    assert "（设计目标未记录于 config.yaml）" in html


def test_notes_collect_note_and_detail(tmp_path):
    ws = _make_case(tmp_path)
    append_entry(ws, {"action": "funnel", "passed": 1, "rejected": 0,
                      "disputed": 0, "detail": "detail-text-1"})
    append_entry(ws, {"round": 2, "action": "evaluate",
                      "metrics": {"T_max_K": 318.0, "plated": False},
                      "verdict": "pass", "note": "note-text-1"})
    html = _render(ws)
    assert "note-text-1" in html
    assert "detail-text-1" in html


def test_render_is_deterministic(tmp_path, full_case):
    p1 = render_report(str(full_case.path), "r1.html")
    p2 = render_report(str(full_case.path), "r2.html")
    assert open(p1, encoding="utf-8").read() == open(p2, encoding="utf-8").read()


def test_verdict_variants(tmp_path):
    ws = _make_case(tmp_path)
    append_entry(ws, {"action": "final", "recommendation": "x", "verdict": "不达标"})
    html = _render(ws)
    assert 'class="verdict bad"' in html
    assert 'class="badge bad"' in html

    ws2 = _make_case(tmp_path)
    append_entry(ws2, {"action": "final", "recommendation": "x", "verdict": "未知结论"})
    html2 = _render(ws2)
    assert 'class="verdict neutral"' in html2

    ws3 = _make_case(tmp_path)
    append_entry(ws3, {"action": "final", "recommendation": "x"})
    html3 = _render(ws3)
    assert "未判定" in html3  # 无 verdict 的 final 不伪装结论

    ws4 = _make_case(tmp_path)
    append_entry(ws4, {"action": "final"})
    html4 = _render(ws4)
    assert "暂无推荐（预算耗尽或未达标）" in html4  # 空 final 条目如实回退


def test_propose_dict_candidates_with_name_and_role(tmp_path):
    ws = _make_case(tmp_path)
    append_entry(ws, {"round": 2, "action": "propose",
                      "candidates": [
                          {"smiles": "FC1COC(=O)O1", "name": "FEC",
                           "role": "氟代碳酸酯成膜剂"},
                          {"smiles": "N#CCCC#N", "name": "SN"},
                          "CCOC(=O)O",
                      ]})
    html = _render(ws)
    assert "FEC" in html  # name 渲染
    assert "氟代碳酸酯" in html  # role 渲染
    assert "FC1COC(=O)O1" in html  # SMILES 作为次要信息仍显示
    assert "SN" in html  # role 缺失只显示 name
    assert "CCOC(=O)O" in html  # 纯字符串候选仍兼容


def test_propose_dict_candidates_with_source(tmp_path):
    ws = _make_case(tmp_path)
    append_entry(ws, {"round": 2, "action": "propose",
                      "candidates": [
                          {"smiles": "FC1COC(=O)O1", "name": "FEC", "source": "seed"},
                          {"smiles": "N#CCCC#N", "name": "SN", "source": "free_gen"},
                          {"smiles": "O=S1(=O)OCCO1"},
                      ]})
    html = _render(ws)
    assert "FC1COC(=O)O1" in html
    assert "tag seed" in html
    assert "tag free" in html
    assert "SEED" in html
    assert "FREE_GEN" in html


def test_unit_helpers():
    assert _fmt_num(True) == "true"
    assert _fmt_num(327.0) == "327"
    assert _fmt_num(1e9) == "1.000e+09"
    assert _fmt_num(1e-5) == "1.000e-05"
    assert _fmt_num(float("inf")) == "inf"
    assert _fmt_num("x") == "x"
    assert _attr_escape("a\"b'c") == "a&quot;b&#39;c"
    assert _json_block(object()).startswith("<object")
    assert _threshold_text({}) == ""
    assert _to_int("abc") == 0
    assert _as_list(5) == [5]
    assert _as_list(None) == []
    assert _as_list([]) == []
    assert _verdict_class("达标") == "ok"
    assert _verdict_class("不达标") == "bad"
    assert _verdict_class("pass") == "ok"
    assert _verdict_class("fail") == "bad"
    assert _verdict_class("待定") == "neutral"
    assert _verdict_class("") == "neutral"
    with pytest.raises(ValueError):
        _fill_template({})
