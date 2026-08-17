import base64
import csv
import io
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _load_log(case_dir: str) -> list[dict]:
    p = Path(case_dir) / "log.jsonl"
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


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


def _candidate_names(log: list[dict]) -> list[str]:
    names = []
    for e in log:
        for c in _as_list(e.get("candidates")):
            if isinstance(c, dict):
                names.append(str(c.get("smiles") or c))
            else:
                names.append(str(c))
    return sorted(set(names))


def _trend_chart_html(log: list[dict]) -> str:
    """温度趋势图：matplotlib 画图 → PNG → base64 内嵌 <img>，无外部资源依赖。"""
    points = [
        (e.get("round"), m.get("T_max_K"))
        for e in log
        if e.get("action") == "evaluate"
        for m in [e.get("metrics", {})]
        if isinstance(m.get("T_max_K"), (int, float))
    ]
    if not points:
        return ""
    rounds = [r for r, _ in points]
    temps = [t for _, t in points]
    fig, ax = plt.subplots(figsize=(6, 2.5), dpi=110)
    ax.plot(rounds, temps, "o-", color="#c0392b")
    ax.set_xlabel("round")
    ax.set_ylabel("T_max_K")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f'<img alt="温度趋势图" src="data:image/png;base64,{b64}">'


def _trajectory_section_html(log: list[dict]) -> str:
    """迭代轨迹：每轮候选与 Agent 决策理由（propose 条目）。"""
    proposals = [e for e in log if e.get("action") == "propose"]
    if not proposals:
        return "<h2>迭代轨迹</h2><p>暂无数据</p>"
    rows = []
    for e in proposals:
        cands = "、".join(str(c) for c in _as_list(e.get("candidates")))
        rows.append(
            "<tr>"
            f"<td>{_html_escape(str(e.get('round', '')))}</td>"
            f"<td>{_html_escape(cands)}</td>"
            f"<td>{_html_escape(str(e.get('llm_reason', '')))}</td>"
            "</tr>"
        )
    table = "<table><tr><th>轮</th><th>候选</th><th>决策理由</th></tr>" + "".join(rows) + "</table>"
    return "<h2>迭代轨迹</h2>" + table


def _funnel_section_html(log: list[dict]) -> str:
    """漏斗统计：通过/淘汰/分歧计数，跨条目求和。"""
    entries = [e for e in log if e.get("action") == "funnel"]
    if not entries:
        return "<h2>漏斗统计</h2><p>暂无数据</p>"
    totals = {"passed": 0, "rejected": 0, "disputed": 0}
    for e in entries:
        for k in totals:
            totals[k] += _to_int(e.get(k))
    labels = {"passed": "通过", "rejected": "淘汰", "disputed": "分歧"}
    rows = "".join(
        f"<tr><td>{_html_escape(labels[k])}</td><td>{totals[k]}</td></tr>" for k in totals
    )
    return "<h2>漏斗统计</h2><table><tr><th>类别</th><th>数量</th></tr>" + rows + "</table>"


def _stage23_section_html(log: list[dict]) -> str:
    """阶段 2/3 结果：全部 metrics 键的逐轮表格 + 温度趋势图 + 最新判定摘要。"""
    evals = [e for e in log if e.get("action") == "evaluate"]
    if not evals:
        return "<h2>阶段 2/3 结果</h2><p>暂无数据</p>"
    metric_keys = sorted({k for e in evals for k in e.get("metrics", {})})
    header = (
        "<tr><th>轮</th>"
        + "".join(f"<th>{_html_escape(k)}</th>" for k in metric_keys)
        + "<th>判定</th></tr>"
    )
    rows = []
    for e in evals:
        m = e.get("metrics", {})
        cells = [f"<td>{_html_escape(str(e.get('round', '')))}</td>"]
        cells += [f"<td>{_html_escape(str(m.get(k, '')))}</td>" for k in metric_keys]
        cells.append(f"<td>{_html_escape(str(e.get('verdict', '')))}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    latest = evals[-1]
    summary = (
        "<p>最新判定（第 "
        f"{_html_escape(str(latest.get('round', '')))} 轮）："
        f"{_html_escape(str(latest.get('verdict', '')))}</p>"
    )
    chart = _trend_chart_html(log)
    chart_html = f"<h3>温度趋势</h3>{chart}" if chart else ""
    table = "<table>" + header + "".join(rows) + "</table>"
    return "<h2>阶段 2/3 结果</h2>" + table + chart_html + summary


def _endorse_section_html(log: list[dict]) -> str:
    """收尾背书：每个候选的 endorsement dict 以 <pre> JSON 展示。"""
    entries = [e for e in log if e.get("action") == "endorse"]
    if not entries:
        return "<h2>收尾背书</h2><p>暂无数据</p>"
    blocks = []
    for e in entries:
        for cand in _as_list(e.get("candidates")):
            if not isinstance(cand, dict):
                cand = {"smiles": str(cand), "endorsement": {}}
            smiles = str(cand.get("smiles", ""))
            endorsement = cand.get("endorsement", {})
            blocks.append(
                f"<p>候选：{_html_escape(smiles)}</p>"
                f"<pre>{_html_escape(_json_block(endorsement))}</pre>"
            )
    return "<h2>收尾背书</h2>" + "".join(blocks)


def _final_section_html(log: list[dict]) -> str:
    """最终推荐方案与指标达标清单：最终条目的 recommendation 与 verdict。"""
    fallback = "<h2>最终推荐方案与指标达标清单</h2><p>暂无推荐（预算耗尽或未达标）</p>"
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
        parts.append(f"<p><strong>推荐方案：</strong>{_html_escape(rec)}</p>")
    if verdict:
        parts.append(f"<p><strong>结论：</strong>{_html_escape(verdict)}</p>")
    return "<h2>最终推荐方案与指标达标清单</h2>" + "".join(parts)


def render_report(case_dir: str, out_html: str = "report.html") -> str:
    log = _load_log(case_dir)
    criteria = log[0].get("criteria", {}) if log else {}
    candidates = "".join(f"<li>{_html_escape(c)}</li>" for c in _candidate_names(log))
    html = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>案例报告</title>
<style>body{{font-family:system-ui;max-width:900px;margin:2em auto;padding:0 1em}}
table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:4px 8px}}
pre{{background:#f7f7f7;padding:8px;overflow-x:auto}}</style>
</head><body>
<h1>虚拟电池工厂 · 案例报告</h1>
<h2>任务概览与达标标准</h2><pre>{_html_escape(_json_block(criteria))}</pre>
<h2>涉及候选</h2><ul>{candidates}</ul>
{_trajectory_section_html(log)}
{_funnel_section_html(log)}
{_stage23_section_html(log)}
{_endorse_section_html(log)}
{_final_section_html(log)}
</body></html>"""
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
