"""log.jsonl → 自包含 HTML 报告（工程蓝图纸模板，确定性渲染，零 LLM）。

数据源：
- log.jsonl：criteria 第 0 条 + propose/funnel/evaluate/endorse/final 条目
- <case_dir>/config.yaml：goal（可选，仅用于图纸头展示）
- <case_dir>/cell/*.json：run-pyamm 曲线输出（time_s/voltage_v/anode_potential_v）
"""

import csv
import json
import math
import re
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "report_template.html"

# 内联 SVG 曲线几何（viewBox 640×320）
_VIEW_W, _VIEW_H = 640, 320
_PAD_L, _PAD_R, _PAD_T, _PAD_B = 56, 20, 16, 40
_MAX_PTS = 400  # 每条曲线路径的采样点数上限


def _load_log(case_dir: str) -> list[dict]:
    p = Path(case_dir) / "log.jsonl"
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _attr_escape(s: str) -> str:
    """HTML 属性值转义（配合单引号定界使用）。"""
    return _html_escape(str(s)).replace('"', "&quot;").replace("'", "&#39;")


def _to_int(v) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def _json_block(v) -> str:
    try:
        return json.dumps(v, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        return str(v)


def _as_list(v) -> list:
    if isinstance(v, list):
        return v
    return [v] if v else []


def _fmt_num(v, sig: int = 4) -> str:
    """数值展示格式化：int 原样、float 取有效数字、其余转字符串。"""
    if isinstance(v, bool):
        return str(v).lower()
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if not math.isfinite(v):
            return str(v)
        if abs(v) >= 1e6 or (v != 0 and abs(v) < 1e-4):
            return f"{v:.3e}"
        return f"{v:.{sig}g}"
    return str(v)


def _candidate_names(log: list[dict]) -> list[str]:
    names = []
    for e in log:
        for c in _as_list(e.get("candidates")):
            if isinstance(c, dict):
                names.append(str(c.get("smiles") or c.get("name") or c))
            else:
                names.append(str(c))
    return sorted(set(names))


def _read_goal(case_dir: str) -> str | None:
    """从 config.yaml 读取设计目标（缺失/损坏时返回 None，如实标注）。"""
    p = Path(case_dir) / "config.yaml"
    if not p.exists():
        return None
    try:
        import yaml

        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        goal = data.get("goal") if isinstance(data, dict) else None
        return str(goal) if goal else None
    except Exception:
        return None


def _verdict_class(verdict: str) -> str:
    v = str(verdict).strip().lower()
    if not v:
        return "neutral"
    if "不达标" in v or v in ("fail", "failed", "reject", "rejected", "no"):
        return "bad"
    if "达标" in v or v in ("pass", "passed", "ok", "yes"):
        return "ok"
    return "neutral"


def _verdict_badge(verdict: str) -> str:
    cls = _verdict_class(verdict)
    return f'<span class="badge {cls}">{_html_escape(str(verdict))}</span>'


# 四阶段流程（1–3=漏斗阶段，4=真DFT/MD 验证；阶段编号与 SKILL.md 流程一致。
# 阶段 4 沿用 .badge.stage.end 铜色样式区分。）
_STAGE_LABELS = {1: "STAGE 1", 2: "STAGE 2", 3: "STAGE 3", 4: "STAGE 4"}


def _stage_badge(stage: int | None) -> str:
    """STAGE 小标（blueprint 风格：等宽 10.5px 边框徽章，沿用 .badge + --blue/--accent）。"""
    if stage not in _STAGE_LABELS:
        return ""
    cls = "badge stage end" if stage == 4 else "badge stage"
    return f'<span class="{cls}">{_STAGE_LABELS[stage]}</span>'


def _stage_range_badge(lo: int, hi: int) -> str:
    """轮卡片阶段范围徽章：单阶段沿用 _stage_badge；跨阶段显示 STAGE N–M（en dash）。
    范围仅由数字阶段（1–4）构成，阶段 4（真DFT/MD 验证）可参与范围（如 STAGE 3–4）；
    endorse/final 条目不进轮卡片，阶段 4 在流程一览条中单独显示。"""
    if lo == hi:
        return _stage_badge(lo)
    if lo not in _STAGE_LABELS or hi not in _STAGE_LABELS:
        return ""
    return f'<span class="badge stage">STAGE {lo}–{hi}</span>'


def _entry_stage(e: dict) -> int | None:
    """log 条目 → 阶段：endorse/final=4（真DFT/MD 验证）；分子 propose/funnel=1；struct propose=2；
    evaluate 按条目内容推断（提及 struct/结构 → 含安全指标为 3，否则 2；否则视为材料轮=1）。"""
    action = e.get("action")
    if action in ("endorse", "final"):
        return 4
    if action == "propose":
        has_struct = any(
            isinstance(c, dict) and c.get("struct") for c in _as_list(e.get("candidates"))
        )
        return 2 if has_struct else 1
    if action == "funnel":
        return 1
    if action == "evaluate":
        text = json.dumps(e, ensure_ascii=False)
        if "struct" in text or "结构" in text:
            metrics = e.get("metrics") or {}
            has_safety = isinstance(metrics.get("T_max_K"), (int, float)) or "plated" in metrics
            return 3 if has_safety else 2
        return 1
    return None


def _plot_stage(filename: str) -> int | None:
    """曲线文件名 → 阶段：discharge=2（电芯设计）、charge45=3（安全评估）；无法判定则不贴。"""
    low = filename.lower()
    if "discharge" in low:
        return 2
    if "charge" in low:
        return 3
    return None


def _threshold_text(value) -> str:
    if isinstance(value, bool):
        return "无析锂" if not value else "析锂允许"
    if isinstance(value, dict):
        parts = []
        if "min" in value:
            parts.append(f"≥ {_fmt_num(value['min'], sig=5)}")
        if "max" in value:
            parts.append(f"≤ {_fmt_num(value['max'], sig=5)}")
        return " · ".join(parts) if parts else ""
    return _fmt_num(value)


_STAGE_KEYS = ("stage1", "stage2", "stage3", "meta")
_STAGE_NAMES = {"stage1": "材料设计", "stage2": "电芯设计", "stage3": "安全评估", "meta": "案例参数"}
_STAGE1_UNITS = {"max_energy_ev": "eV", "max_homo_ev": "eV"}


def _normalize_criteria(criteria: dict) -> dict[str, dict]:
    """criteria → {"stage1"/"stage2"/"stage3"/"meta": {...}}。

    新协议为显式分层（stageN/meta 键）；旧日志为扁平键（如 T_max_C），按键名归组：
    电位窗/淘汰线（homo/energy_ev/voltage/window）→ stage1；容量/能量密度（capacity/density）→ stage2；
    温度/析锂（t_max/temp/plat）→ stage3；其余 → meta。
    """
    norm: dict[str, dict] = {}
    for k in _STAGE_KEYS:
        v = criteria.get(k)
        norm[k] = dict(v) if isinstance(v, dict) else {}
    rest = {k: v for k, v in criteria.items() if k not in _STAGE_KEYS}
    if rest:
        legacy = {k: {} for k in _STAGE_KEYS}
        for k, v in rest.items():
            kl = str(k).lower()
            if "homo" in kl or "energy_ev" in kl or "voltage" in kl or "window" in kl:
                legacy["stage1"][k] = v
            elif "capacity" in kl or "density" in kl:
                legacy["stage2"][k] = v
            elif "t_max" in kl or "temp" in kl or "plat" in kl:
                legacy["stage3"][k] = v
            else:
                legacy["meta"][k] = v
        for k in _STAGE_KEYS:
            norm[k] = {**legacy[k], **norm[k]}
    return norm


def _flat_thresholds(criteria: dict) -> dict:
    """stage1–3 阈值合并为扁平字典（KPI/达成列机械比较用；meta 不参与）。"""
    norm = _normalize_criteria(criteria)
    merged: dict = {}
    for k in ("stage1", "stage2", "stage3"):
        merged.update(norm[k])
    return merged


def _achieve_cell(value, spec) -> str:
    """单指标达成格：数值 vs {"min"/"max"} 阈值 → ✓/✗ 徽章 + 达成值；无数据 → 破折号。"""
    if isinstance(value, bool):
        show = "无析锂" if not value else "析锂风险"
        if isinstance(spec, bool):
            mark = '<span class="badge ok">✓</span>' if value == spec else '<span class="badge bad">✗</span>'
            return f"{show} {mark}"
        return f'{show} <span class="badge mute">—</span>'
    if isinstance(value, (int, float)):
        show = _fmt_num(value)
        if isinstance(spec, dict):
            checks = []
            if "min" in spec and isinstance(spec["min"], (int, float)):
                checks.append(value >= spec["min"])
            if "max" in spec and isinstance(spec["max"], (int, float)):
                checks.append(value <= spec["max"])
            if checks:
                mark = '<span class="badge ok">✓</span>' if all(checks) else '<span class="badge bad">✗</span>'
                return f"{show} {mark}"
        return f'{show} <span class="badge mute">—</span>'
    return '<span class="badge mute">—</span>'


def _stage_achieve_badge(stage_key: str, stage_dict: dict, metrics: dict, funnel_latest: dict | None) -> str:
    """阶段头部"达成"徽章：stage1 看漏斗；stage2/3 看指标对照；无数据 → mute。"""
    if stage_key == "stage1":
        if funnel_latest is None:
            return '<span class="badge mute">未执行</span>'
        n, m = _to_int(funnel_latest.get("passed")), _to_int(funnel_latest.get("disputed"))
        # 分歧不是失败（协议："分歧是'该动脑子'的信号"），处置留痕于漏斗明细；
        # 阶段 1 达成 = 有候选通过漏斗（passed > 0）
        cls = "ok" if n > 0 else "bad"
        return f'<span class="badge {cls}">达成 · PASS {n} · DISP {m}</span>'
    verdicts: list[bool] = []
    for k, spec in stage_dict.items():
        v = metrics.get(k)
        if isinstance(v, bool) and isinstance(spec, bool):
            verdicts.append(v == spec)
        elif isinstance(v, (int, float)) and isinstance(spec, dict) and ("min" in spec or "max" in spec):
            if "min" in spec and isinstance(spec["min"], (int, float)):
                verdicts.append(v >= spec["min"])
            if "max" in spec and isinstance(spec["max"], (int, float)):
                verdicts.append(v <= spec["max"])
    if not verdicts:
        return '<span class="badge mute">未执行</span>'
    if all(verdicts):
        return '<span class="badge ok">全部达成</span>'
    return '<span class="badge bad">部分未达成</span>'


def _criteria_html(criteria: dict, log: list[dict]) -> str:
    if not criteria:
        return (
            '<p class="empty">暂无数据</p>'
            '<p class="hint">log.jsonl 第 0 条未提供达标标准（criteria）。</p>'
        )
    norm = _normalize_criteria(criteria)
    metrics = _latest_metrics(log)
    funnels = [e for e in log if e.get("action") == "funnel"]
    funnel_latest = funnels[-1] if funnels else None
    blocks = []
    for stage_key, name in (("stage1", "材料设计"), ("stage2", "电芯设计"),
                            ("stage3", "安全评估"), ("meta", "案例参数")):
        stage_dict = norm.get(stage_key, {})
        if stage_key == "meta":
            head = ('<div class="stage-goal-head"><span class="badge mute">META</span>'
                    f'<span class="stage-goal-name">{name}</span></div>')
            if not stage_dict:
                table = '<p class="empty">未提供</p>'
            else:
                rows = "".join(
                    "<tr>"
                    f"<th scope='row'>{_html_escape(str(k))}</th>"
                    f"<td class='num'>{_html_escape(_fmt_num(v))}</td>"
                    "</tr>"
                    for k, v in stage_dict.items()
                )
                table = f'<table class="tbl"><tr><th>参数</th><th>值</th></tr>{rows}</table>'
            blocks.append(f'<div class="stage-goal meta">{head}{table}</div>')
            continue
        stage_num = int(stage_key[-1])
        head = (
            f'<div class="stage-goal-head">{_stage_badge(stage_num)}'
            f'<span class="stage-goal-name">{name}</span>'
            f"{_stage_achieve_badge(stage_key, stage_dict, metrics, funnel_latest)}</div>"
        )
        if not stage_dict:
            table = '<p class="empty">未设置单独目标（综合目标见其他阶段）</p>'
            blocks.append(f'<div class="stage-goal">{head}{table}</div>')
            continue
        has_achieve = stage_key in ("stage2", "stage3")
        head_cells = "<tr><th>指标</th><th>阈值</th>" + ("<th>达成</th>" if has_achieve else "") + "<th>说明</th></tr>"
        rows = []
        for k, v in stage_dict.items():
            if stage_key == "stage1" and not isinstance(v, (dict, bool)):
                unit = _STAGE1_UNITS.get(k, "")
                threshold = f"≤ {_fmt_num(v)}" + (f" {unit}" if unit else "")
            else:
                threshold = _threshold_text(v)
            meta = (
                " · ".join(f"{mk}={_fmt_num(mv)}" for mk, mv in v.items() if mk not in ("min", "max"))
                if isinstance(v, dict)
                else ""
            )
            cells = (
                f"<th scope='row'>{_html_escape(str(k))}</th>"
                f"<td class='num'>{_html_escape(threshold)}</td>"
            )
            if has_achieve:
                cells += f"<td class='num'>{_achieve_cell(metrics.get(k), v)}</td>"
            cells += f"<td class='crit-meta'>{_html_escape(meta)}</td>"
            rows.append(f"<tr>{cells}</tr>")
        table = f'<table class="tbl">{head_cells}{"".join(rows)}</table>'
        blocks.append(f'<div class="stage-goal">{head}{table}</div>')
    return f'<div class="stage-goals">{"".join(blocks)}</div>'


def _candidates_html(log: list[dict]) -> str:
    names = _candidate_names(log)
    if not names:
        return '<p class="empty">暂无数据</p>'
    chips = "".join(f'<span class="chip mono">{_html_escape(c)}</span>' for c in names)
    return f'<div class="chips">{chips}</div>'


def _goal_mark(ok: bool) -> str:
    return '<b class="goal-ok">✓</b>' if ok else '<b class="goal-bad">✗</b>'


def _goal_parts(stage_key: str, stage_dict: dict) -> str:
    """阶段目标压缩文本：'E ≤ 0.0 eV · HOMO ≤ −6.0 eV' / '能量密度 ≥ 300 Wh/kg' 等。"""
    labels = {
        "max_energy_ev": "E", "max_homo_ev": "HOMO",
        "energy_density_wh_kg": "能量密度", "capacity_ah": "容量", "T_max_K": "T_max",
    }
    units = {"max_energy_ev": "eV", "max_homo_ev": "eV", "energy_density_wh_kg": "Wh/kg", "T_max_K": "K"}
    parts = []
    for k, v in stage_dict.items():
        if isinstance(v, bool):
            parts.append(_threshold_text(v))
            continue
        if isinstance(v, str):
            continue  # 自由文本规则（如 plating_rule）不进入压缩目标行
        label = labels.get(k, str(k))
        if isinstance(v, dict):
            t = _threshold_text(v)
            parts.append(f"{label} {t}" if t else f"{label} {_fmt_num(v)}")
        else:
            sign = "≤ " if stage_key == "stage1" else ""
            unit = units.get(k, "")
            parts.append(f"{label} {sign}{_fmt_num(v)}{' ' + unit if unit else ''}")
    return " · ".join(parts) if parts else "未设置目标"


def _flow_achieve(stage_key: str, stage_dict: dict, log: list[dict]) -> str:
    """流程条达成摘要：stage1 看最新漏斗；stage2/3 看最新评估指标对照。"""
    if stage_key == "stage1":
        funnels = [e for e in log if e.get("action") == "funnel"]
        if not funnels:
            return "—"
        f = funnels[-1]
        n, m = _to_int(f.get("passed")), _to_int(f.get("disputed"))
        # 阶段 1 达成 = 有候选通过漏斗（分歧已处置，留痕于漏斗明细）
        return f"PASS {n} · DISP {m} {_goal_mark(n > 0)}"
    metrics = _latest_metrics(log)
    if not stage_dict or not metrics:
        return "—"
    parts = []
    for k, v in stage_dict.items():
        mv = metrics.get(k)
        if isinstance(v, bool) and isinstance(mv, bool):
            parts.append(f"{'无析锂' if not mv else '析锂风险'}{_goal_mark(mv == v)}")
        elif isinstance(mv, (int, float)) and isinstance(v, dict) and ("min" in v or "max" in v):
            ok = True
            if "min" in v and isinstance(v["min"], (int, float)):
                ok = ok and mv >= v["min"]
            if "max" in v and isinstance(v["max"], (int, float)):
                ok = ok and mv <= v["max"]
            parts.append(f"{_fmt_num(mv)}{_goal_mark(ok)}")
    return " · ".join(parts) if parts else "—"


def _flow_html(log: list[dict], cell_files: list[tuple[str, dict]], criteria: dict) -> str:
    """概览区流程一览条：四阶段徽章，各带计数/结论摘要 + 目标与达成（由 criteria 与 log 机械推导）。

    阶段1 材料设计=分子 propose/funnel；阶段2 电芯设计=struct propose/discharge 曲线；
    阶段3 安全评估=charge45 曲线；阶段4 真DFT/MD 验证=endorse/final（含最终结论）。
    """
    mol_prop = struct_prop = funnel_n = endorse_n = final_n = 0
    for e in log:
        action = e.get("action")
        if action == "funnel":
            funnel_n += 1
        elif action == "endorse":
            endorse_n += 1
        elif action == "final":
            final_n += 1
        elif action == "propose":
            for c in _as_list(e.get("candidates")):
                if isinstance(c, dict) and c.get("struct"):
                    struct_prop += 1
                else:
                    mol_prop += 1
    n_discharge = sum(1 for fname, _ in cell_files if _plot_stage(fname) == 2)
    n_charge45 = sum(1 for fname, _ in cell_files if _plot_stage(fname) == 3)
    finals = [e for e in log if e.get("action") == "final"]
    verdict = str(finals[-1].get("verdict") or "") if finals else ""
    close_sum = f"背书 {endorse_n} · 终审 {final_n}" + (f" · 结论 {verdict}" if verdict else "")
    norm = _normalize_criteria(criteria)
    items = (
        (1, "阶段1 · 材料设计", f"分子 propose {mol_prop} · funnel {funnel_n}"),
        (2, "阶段2 · 电芯设计", f"结构 propose {struct_prop} · 放电曲线 {n_discharge}"),
        (3, "阶段3 · 安全评估", f"4C 快充曲线 {n_charge45}"),
        (4, "真DFT/MD 验证", close_sum),
    )
    blocks = []
    for stage, name, count in items:
        goal_html = ""
        if stage in (1, 2, 3):
            stage_key = f"stage{stage}"
            stage_dict = norm.get(stage_key, {})
            goal_html = (
                f'<div class="flow-goal"><span class="g-label">目标</span>'
                f"<span>{_html_escape(_goal_parts(stage_key, stage_dict))}</span></div>"
                f'<div class="flow-goal"><span class="g-label">达成</span>'
                f"<span>{_flow_achieve(stage_key, stage_dict, log)}</span></div>"
            )
        blocks.append(
            f'<div class="flow-item {"end" if stage == 4 else ""}">{_stage_badge(stage)}'
            f'<div class="flow-name">{_html_escape(name)}</div>'
            f'<div class="flow-count">{_html_escape(count)}</div>{goal_html}</div>'
        )
    return f'<div class="flow">{"".join(blocks)}</div>'


def _kpi_compare(value, thresholds: dict, key: str, direction: str) -> tuple[str, str]:
    """关键结果 vs 扁平化阈值（stage1–3 合并）的机械比较 → (颜色类, 阈值说明)。"""
    spec = thresholds.get(key)
    thr = spec.get(direction) if isinstance(spec, dict) else None
    if not isinstance(value, (int, float)) or not isinstance(thr, (int, float)):
        return "", ""
    ok = (value >= thr) if direction == "min" else (value <= thr)
    sign = "≥" if direction == "min" else "≤"
    return ("ok" if ok else "bad"), f"阈值 {sign} {_fmt_num(thr, sig=5)}"


def _kpi_item(label: str, value, unit: str, cls: str, sub: str) -> str:
    num = _fmt_num(value) if value is not None else "N/A"
    cls = cls or ("mute" if value is None else "")
    unit_html = f'<span class="kpi-unit">{_html_escape(unit)}</span>' if unit else ""
    return (
        f'<div class="kpi-item"><div class="kpi-label">{_html_escape(label)}</div>'
        f'<div class="kpi-num {cls}">{_html_escape(num)}{unit_html}</div>'
        f'<div class="kpi-sub">{_html_escape(sub)}</div></div>'
    )


def _latest_metrics(log: list[dict]) -> dict:
    for e in reversed(log):
        if e.get("action") == "evaluate" and isinstance(e.get("metrics"), dict):
            return e["metrics"]
    return {}


def _kpi_html(metrics: dict, criteria: dict) -> str:
    thresholds = _flat_thresholds(criteria)
    items = []
    for key, label, unit, direction in (
        ("energy_density_wh_kg", "能量密度", "Wh/kg", "min"),
        ("capacity_ah", "放电容量", "Ah", None),
        ("T_max_K", "最高温度", "K", "max"),
    ):
        value = metrics.get(key) if isinstance(metrics.get(key), (int, float)) else None
        cls, sub = "", ""
        if direction and value is not None:
            cls, sub = _kpi_compare(value, thresholds, key, direction)
        if key == "T_max_K" and value is not None:
            conv = f"≈ {value - 273.15:.1f} °C"
            sub = f"{sub} · {conv}" if sub else conv
        items.append(_kpi_item(label, value, unit, cls, sub))
    plated = metrics.get("plated")
    if isinstance(plated, bool):
        if not plated:
            items.append(_kpi_item("析锂判定", "无析锂", "", "ok", "负极电位全程 ≥ 0 V"))
        else:
            items.append(_kpi_item("析锂判定", "析锂风险", "", "bad", "负极电位曾 < 0 V"))
    else:
        items.append(_kpi_item("析锂判定", None, "", "mute", "未提供"))
    return f'<div class="kpi-grid">{"".join(items)}</div>'


def _header_html(case_dir: str, log: list[dict], criteria: dict) -> str:
    case_name = Path(case_dir).name or "case"
    goal = _read_goal(case_dir) or "（设计目标未记录于 config.yaml）"
    meta_criteria = _normalize_criteria(criteria).get("meta", {})
    meta = []
    if "max_rounds" in meta_criteria:
        meta.append(f"预算 {_fmt_num(meta_criteria['max_rounds'])} 轮")
    if "real_compute" in meta_criteria:
        meta.append("真计算开启" if meta_criteria["real_compute"] is True else "真计算关闭")
    meta_html = "".join(f"<span>{_html_escape(m)}</span>" for m in meta)

    final_entries = [e for e in log if e.get("action") == "final"]
    verdict = str(final_entries[-1].get("verdict") or "") if final_entries else ""
    if not verdict:
        verdict, vcls = "未判定", "neutral"
    else:
        vcls = _verdict_class(verdict)
    verdict_html = (
        '<div class="verdict-block"><div class="eyebrow light">Conclusion · 结论</div>'
        f'<div class="verdict {vcls}">{_html_escape(verdict)}</div></div>'
    )

    metrics = _latest_metrics(log)
    return (
        '<div class="head-row">'
        '<div class="head-main">'
        '<div class="eyebrow light">Virtual Battery Factory · Case Design Report</div>'
        f'<h1 class="case-name">{_html_escape(case_name)}</h1>'
        f'<p class="goal">{_html_escape(goal)}</p>'
        f'<p class="head-meta">{meta_html}</p>'
        "</div>"
        f"{verdict_html}"
        "</div>"
        f"{_kpi_html(metrics, criteria)}"
    )


def _propose_html(e: dict) -> str:
    parts = []
    for cand in _as_list(e.get("candidates")):
        if isinstance(cand, dict):
            smiles = str(cand.get("smiles") or "")
            name = str(cand.get("name") or "")
            role = str(cand.get("role") or "")
            source = str(cand.get("source") or "")
        else:
            smiles, name, role, source = str(cand), "", "", ""
        if name:
            inner = f"<b>{_html_escape(name)}</b>"
            if role:
                inner += f" · {_html_escape(role)}"
            if smiles:
                inner += f' <span class="sm">{_html_escape(smiles)}</span>'
        else:
            inner = f'<span class="sm">{_html_escape(smiles)}</span>'
        tag = ""
        if source:
            cls = "seed" if source.lower() == "seed" else "free" if source.lower() in ("free_gen", "free") else ""
            tag = f'<span class="chip tag {cls}">{_html_escape(source.upper())}</span>'
        parts.append(f'<span class="chip">{inner}</span>{tag}')
    reason = e.get("llm_reason")
    reason_html = f'<p class="reason">{_html_escape(str(reason))}</p>' if reason else ""
    return (
        '<div class="blk"><div class="blk-label">Propose · 候选方案</div>'
        f'<div class="chips">{"".join(parts)}</div>{reason_html}</div>'
    )


def _funnel_entry_html(e: dict) -> str:
    chips = "".join(
        f'<span class="chip">{lab} <b class="num">{_to_int(e.get(k))}</b></span>'
        for k, lab in (("passed", "PASS"), ("rejected", "REJECT"), ("disputed", "DISP."))
    )
    detail = e.get("detail")
    detail_html = f"<p>{_html_escape(str(detail))}</p>" if detail else ""
    return f'<div class="blk"><div class="blk-label">Funnel · 漏斗判定</div>{chips}{detail_html}</div>'


def _evaluate_html(e: dict) -> str:
    metrics = e.get("metrics") or {}
    rows = "".join(
        f"<tr><td>{_html_escape(str(k))}</td>"
        f"<td class='num'>{_html_escape(_fmt_num(v))}</td></tr>"
        for k, v in metrics.items()
    )
    verdict = e.get("verdict")
    verdict_html = _verdict_badge(str(verdict)) if verdict else '<span class="badge mute">N/A</span>'
    note = e.get("note")
    note_html = f'<p class="reason">{_html_escape(str(note))}</p>' if note else ""
    return (
        f'<div class="blk"><div class="blk-label">Evaluate · 评估 {verdict_html}</div>'
        f'<table class="tbl"><tr><th>指标</th><th>数值</th></tr>{rows}</table>{note_html}</div>'
    )


def _rounds_html(log: list[dict]) -> str:
    groups: dict[int, list[dict]] = {}
    for e in log:
        r = e.get("round")
        if r is None or _to_int(r) <= 0:
            continue
        if e.get("action") not in ("propose", "funnel", "evaluate"):
            continue
        groups.setdefault(_to_int(r), []).append(e)
    if not groups:
        return '<p class="empty">暂无数据</p>'
    cards = []
    first_round = min(groups)
    for r, entries in sorted(groups.items()):
        ev = next((e for e in entries if e.get("action") == "evaluate"), None)
        verdict = str(ev.get("verdict") or "") if ev else ""
        badge = _verdict_badge(verdict) if verdict else ""
        stages = [s for s in (_entry_stage(e) for e in entries) if s is not None]
        stage_html = _stage_range_badge(min(stages), max(stages)) if stages else ""
        subs = []
        prop = next((e for e in entries if e.get("action") == "propose"), None)
        if prop:
            subs.append(f"{len(_as_list(prop.get('candidates')))} 候选")
        m = ev.get("metrics", {}) if ev else {}
        if isinstance(m.get("T_max_K"), (int, float)):
            subs.append(f"T_max {_fmt_num(m['T_max_K'])} K")
        if isinstance(m.get("plated"), bool):
            subs.append("无析锂" if not m["plated"] else "析锂风险")
        sub = f'<span class="round-sub">{" · ".join(subs)}</span>' if subs else ""
        body = []
        for e in entries:
            action = e.get("action")
            if action == "propose":
                body.append(_propose_html(e))
            elif action == "funnel":
                body.append(_funnel_entry_html(e))
            elif action == "evaluate":
                body.append(_evaluate_html(e))
        open_attr = " open" if r == first_round else ""
        cards.append(
            f'<details class="round"{open_attr}><summary>'
            f'<span class="round-no">ROUND {r:02d}</span>{stage_html}{badge}{sub}'
            f'</summary><div class="round-body">{"".join(body)}</div></details>'
        )
    return "".join(cards)


def _funnel_html(log: list[dict]) -> str:
    entries = [e for e in log if e.get("action") == "funnel"]
    if not entries:
        return '<p class="empty">暂无数据</p>'
    totals = {k: sum(_to_int(e.get(k)) for e in entries) for k in ("passed", "rejected", "disputed")}
    stats = (
        f'<div class="stat pass"><div class="stat-num">{totals["passed"]}</div>'
        '<div class="stat-label">Passed · 通过</div></div>'
        f'<div class="stat rej"><div class="stat-num">{totals["rejected"]}</div>'
        '<div class="stat-label">Rejected · 淘汰</div></div>'
        f'<div class="stat dis"><div class="stat-num">{totals["disputed"]}</div>'
        '<div class="stat-label">Disputed · 分歧</div></div>'
    )
    details = []
    for e in entries:
        r = e.get("round")
        label = f"R{_to_int(r):02d}" if r is not None else "R—"
        detail = e.get("detail")
        detail_html = f"<p>{_html_escape(str(detail))}</p>" if detail else ""
        details.append(f'<div class="funnel-detail"><span class="chip">{label}</span>{detail_html}</div>')
    return f'<div class="stats">{stats}</div>{"".join(details)}'


def _load_cell_curves(case_dir: str) -> list[tuple[str, dict]]:
    """cell/*.json 中 run-pyamm 曲线输出（含 time_s 与至少一条等长曲线序列）。"""
    cell_dir = Path(case_dir) / "cell"
    if not cell_dir.is_dir():
        return []
    out = []
    for p in sorted(cell_dir.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        t = data.get("time_s")
        if not isinstance(t, list) or len(t) < 2:
            continue
        if not any(
            isinstance(data.get(k), list) and len(data.get(k)) == len(t)
            for k in ("voltage_v", "anode_potential_v")
        ):
            continue
        out.append((p.name, data))
    return out


def _svg_plot(filename: str, data: dict) -> str:
    """run-pyamm 输出 → 内联 SVG 曲线（网格 + 双序列 + 轴标注 + tooltip 数据）。"""
    t = data["time_s"]
    series = {
        k: data[k]
        for k in ("voltage_v", "anode_potential_v")
        if isinstance(data.get(k), list) and len(data.get(k)) == len(t)
    }
    tmin, tmax = min(t), max(t)
    x0, x1 = _PAD_L, _VIEW_W - _PAD_R
    y0, y1 = _PAD_T, _VIEW_H - _PAD_B
    stride = max(1, math.ceil(len(t) / _MAX_PTS))
    span_t = (tmax - tmin) or 0.0
    elements = []
    tooltip: dict[str, list[list[float]]] = {}

    for i in range(9):
        gx = x0 + (x1 - x0) * i / 8
        elements.append(f'<line class="grid" x1="{gx:.1f}" y1="{y0}" x2="{gx:.1f}" y2="{y1}"/>')
    for i in range(5):
        gy = y0 + (y1 - y0) * i / 4
        elements.append(f'<line class="grid" x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}"/>')
    elements.append(f'<line class="axis" x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}"/>')
    elements.append(f'<line class="axis" x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}"/>')

    for key, cls in (("voltage_v", "s-voltage"), ("anode_potential_v", "s-anode")):
        vals = series.get(key)
        if vals is None:
            continue
        vmin, vmax = min(vals), max(vals)
        span = (vmax - vmin) or 0.0
        pts, rows = [], []
        for i in range(0, len(t), stride):
            px = x0 + (t[i] - tmin) / span_t * (x1 - x0) if span_t else x0
            py = y1 - (vals[i] - vmin) / span * (y1 - y0) if span else (y0 + y1) / 2
            pts.append(f"{px:.1f},{py:.1f}")
            rows.append([round(t[i], 2), round(vals[i], 4)])
        elements.append(f'<path class="{cls}" d="M{" L".join(pts)}"/>')
        tooltip[f"{key}"] = rows
        side = 1 if key == "voltage_v" else -1
        if side > 0:
            elements.append(f'<text x="{x0 - 6}" y="{y0 + 4}" text-anchor="end">{_fmt_num(vmax)}</text>')
            elements.append(f'<text x="{x0 - 6}" y="{y1 + 4}" text-anchor="end">{_fmt_num(vmin)}</text>')
        else:
            elements.append(f'<text x="{x1 + 6}" y="{y0 + 4}" fill="var(--accent)">{_fmt_num(vmax)}</text>')
            elements.append(f'<text x="{x1 + 6}" y="{y1 + 4}" fill="var(--accent)">{_fmt_num(vmin)}</text>')

    if "voltage_v" in series:
        elements.append(f'<text x="{x0 + 4}" y="{y0 + 10}" fill="var(--blue)">— voltage_v [V]</text>')
    if "anode_potential_v" in series:
        ly = y0 + (26 if "voltage_v" in series else 10)
        elements.append(f'<text x="{x0 + 4}" y="{ly}" fill="var(--accent)">-- anode_potential_v [V]</text>')

    t_max = data.get("T_max_K")
    if isinstance(t_max, (int, float)):
        elements.append(
            f'<text x="{x1}" y="{y0 + 10}" text-anchor="end">T_max = {_fmt_num(t_max)} K</text>'
        )

    tmid = (tmin + tmax) / 2
    for tv, anchor, tx in ((tmin, "start", x0), (tmid, "middle", (x0 + x1) / 2), (tmax, "end", x1)):
        elements.append(
            f'<text x="{tx:.1f}" y="{y1 + 18}" text-anchor="{anchor}">{_fmt_num(tv)}</text>'
        )
    elements.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{_VIEW_H - 8}" text-anchor="middle">time [s]</text>')

    model = str(data.get("model_used") or "N/A")
    label = f"{filename} 曲线（模型 {model}）"
    return (
        f'<svg class="plot" viewBox="0 0 {_VIEW_W} {_VIEW_H}" role="img" '
        f'aria-label="{_attr_escape(label)}" '
        f"data-series='{_attr_escape(json.dumps(tooltip))}'>"
        f"<title>{_html_escape(f'{filename} — model {model}')}</title>"
        + "".join(elements)
        + "</svg>"
    )


def _plots_html(cell_files: list[tuple[str, dict]]) -> str:
    if not cell_files:
        return (
            '<p class="empty">暂无数据</p>'
            '<p class="hint">cell/ 目录下未发现 run-pyamm 曲线输出'
            "（含 time_s 与 voltage_v / anode_potential_v 的 JSON）。</p>"
        )
    figures = []
    for idx, (fname, data) in enumerate(cell_files, start=1):
        model = str(data.get("model_used") or "N/A")
        chips = f'<span class="chip">MODEL {_html_escape(model)}</span>'
        if isinstance(data.get("T_max_K"), (int, float)):
            chips += f'<span class="chip">T_max {_fmt_num(data["T_max_K"])} K</span>'
        stage_html = _stage_badge(_plot_stage(fname))
        figures.append(
            "<figure class='plot'><figcaption>"
            f'<span class="eyebrow" style="margin:0">Plot {idx:02d}</span>'
            f'<span class="fname">{_html_escape(fname)}</span>{stage_html}{chips}'
            "</figcaption>"
            f'<div class="plot-wrap">{_svg_plot(fname, data)}<div class="tooltip" hidden></div></div>'
            "</figure>"
        )
    return "".join(figures)


def _endorse_html(log: list[dict]) -> str:
    entries = [e for e in log if e.get("action") == "endorse"]
    if not entries:
        return '<p class="empty">暂无数据</p>'
    blocks = []
    for e in entries:
        if e.get("skipped"):
            reason = str(e.get("reason") or "未说明原因")
            names = " · ".join(
                str(c.get("name") or c.get("smiles") or c) if isinstance(c, dict) else str(c)
                for c in _as_list(e.get("candidates"))
            )
            names_html = (
                f'<br><span class="reason">候选：{_html_escape(names)}</span>' if names else ""
            )
            blocks.append(
                '<div class="skipped"><span class="badge mute">Skipped</span> '
                f'真计算背书已跳过<span class="reason"> — {_html_escape(reason)}</span>'
                f"{names_html}</div>"
            )
            continue
        for cand in _as_list(e.get("candidates")):
            if not isinstance(cand, dict):
                cand = {"smiles": str(cand), "endorsement": {}}
            smiles = str(cand.get("smiles") or "")
            name = str(cand.get("name") or "")
            endorsement = cand.get("endorsement")
            if endorsement is None:
                endorsement = {k: v for k, v in cand.items() if k not in ("smiles", "name")}
            head = f"<b>{_html_escape(name)}</b> " if name else ""
            head += f'<span class="sm">{_html_escape(smiles)}</span>'
            blocks.append(
                f'<div class="endorse-cand"><div class="endorse-head">{head}</div>'
                f'<pre class="term">{_html_escape(_json_block(endorsement))}</pre></div>'
            )
    return "".join(blocks)


def _final_html(log: list[dict]) -> str:
    fallback = '<p class="empty">暂无推荐（预算耗尽或未达标）</p>'
    entries = [e for e in log if e.get("action") == "final"]
    if not entries:
        return fallback
    latest = entries[-1]
    rec = str(latest.get("recommendation") or "")
    verdict = str(latest.get("verdict") or "")
    if not rec and not verdict:
        return fallback
    parts = []
    if rec:
        parts.append(f'<blockquote class="final-quote">{_html_escape(rec)}</blockquote>')
    if verdict:
        parts.append(f'<div class="final-verdict">结论 {_verdict_badge(verdict)}</div>')
    return "".join(parts)


def _notes_html(log: list[dict]) -> str:
    blocks = []
    for e in log:
        action = e.get("action")
        text = None
        if e.get("note"):
            text = str(e["note"])
        elif action == "funnel" and e.get("detail"):
            text = str(e["detail"])
        if text is None:
            continue
        r = e.get("round")
        rl = f"R{_to_int(r):02d}" if r is not None else "R—"
        blocks.append(
            f'<div class="note"><span class="chip">{_html_escape(str(action))}</span> '
            f'<span class="chip">{rl}</span><p>{_html_escape(text)}</p></div>'
        )
    if not blocks:
        return '<p class="empty">暂无数据</p>'
    return "".join(blocks)


def _fill_template(parts: dict[str, str]) -> str:
    """模板占位符一次性替换；缺位即报错（宁可失败也不产出残缺报告）。"""
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    missing: list[str] = []

    def _sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in parts:
            missing.append(key)
            return m.group(0)
        return parts[key]

    html = re.sub(r"\{\{(\w+)\}\}", _sub, template)
    if missing:
        raise ValueError(f"template placeholders not provided: {sorted(set(missing))}")
    return html


def render_report(case_dir: str, out_html: str = "report.html") -> str:
    log = _load_log(case_dir)
    criteria = log[0].get("criteria", {}) if log else {}
    if not isinstance(criteria, dict):
        criteria = {}
    cell_files = _load_cell_curves(case_dir)
    parts = {
        "TITLE": f"{Path(case_dir).name} · 虚拟电池工厂设计报告",
        "HEADER": _header_html(case_dir, log, criteria),
        "CRITERIA_TABLE": _criteria_html(criteria, log),
        "FLOW": _flow_html(log, cell_files, criteria),
        "CANDIDATES": _candidates_html(log),
        "ROUNDS": _rounds_html(log),
        "FUNNEL": _funnel_html(log),
        "PLOTS": _plots_html(cell_files),
        "ENDORSE": _endorse_html(log),
        "FINAL": _final_html(log),
        "NOTES": _notes_html(log),
    }
    html = _fill_template(parts)
    out_path = Path(case_dir) / out_html
    out_path.write_text(html, encoding="utf-8")
    return str(out_path)


def export_csv(case_dir: str, out_dir: str) -> None:
    log = _load_log(case_dir)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    evals = [e for e in log if e.get("action") == "evaluate"]
    with open(out / "iterations.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["round", "T_max_K", "plated", "verdict"])
        for e in evals:
            m = e.get("metrics", {})
            w.writerow([e.get("round", ""), m.get("T_max_K", ""), m.get("plated", ""), e.get("verdict", "")])
