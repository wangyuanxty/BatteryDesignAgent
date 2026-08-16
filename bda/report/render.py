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
    return f'<h2>温度趋势</h2><img alt="温度趋势图" src="data:image/png;base64,{b64}">'


def render_report(case_dir: str, out_html: str = "report.html") -> str:
    log = _load_log(case_dir)
    criteria = log[0].get("criteria", {}) if log else {}
    rows = []
    for e in log:
        if e.get("action") == "evaluate":
            m = e.get("metrics", {})
            rows.append(
                f"<tr><td>{_html_escape(str(e.get('round', '')))}</td>"
                f"<td>{_html_escape(str(m.get('T_max_K', '')))}</td>"
                f"<td>{_html_escape(str(m.get('plated', '')))}</td>"
                f"<td>{_html_escape(str(e.get('verdict', '')))}</td></tr>"
            )
    candidates = {c for e in log for c in e.get("candidates", [])}
    chart = _trend_chart_html(log)
    html = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>案例报告</title>
<style>body{{font-family:system-ui;max-width:900px;margin:2em auto;padding:0 1em}}
table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:4px 8px}}</style>
</head><body>
<h1>虚拟电池工厂 · 案例报告</h1>
<h2>任务概览与达标标准</h2><pre>{_html_escape(json.dumps(criteria, ensure_ascii=False, indent=2))}</pre>
<h2>涉及候选</h2><ul>{''.join(f'<li>{_html_escape(c)}</li>' for c in sorted(candidates))}</ul>
<h2>迭代轨迹（评估行）</h2>
<table><tr><th>轮</th><th>T_max_K</th><th>析锂</th><th>判定</th></tr>{''.join(rows)}</table>
{chart}
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
