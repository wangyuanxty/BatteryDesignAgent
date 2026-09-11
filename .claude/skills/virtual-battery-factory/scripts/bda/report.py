"""log.jsonl → self-contained HTML report (engineering blueprint template, deterministic
rendering, zero LLM).

Data sources:
- log.jsonl: criteria entry 0 + propose/funnel/evaluate/endorse/final entries
- <case_dir>/config.yaml: goal (optional, used only for the blueprint header)
- <case_dir>/cell/*.json: run-pyamm curve output (time_s/voltage_v/anode_potential_v)
"""

import csv
import json
import math
import re
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "report_template.html"

# Inline SVG curve geometry (viewBox 640×320)
_VIEW_W, _VIEW_H = 640, 320
_PAD_L, _PAD_R, _PAD_T, _PAD_B = 56, 20, 16, 40
_MAX_PTS = 400  # upper bound on sampling points per curve path


def _load_log(case_dir: str) -> list[dict]:
    p = Path(case_dir) / "log.jsonl"
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _attr_escape(s: str) -> str:
    """Escape HTML attribute values (used with single-quote delimiters)."""
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
    """Number display formatting: int as-is, float to significant digits, anything else as a string."""
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


def _variant_dict(c) -> dict:
    """struct/params → dict (params may be a JSON string; parse it)."""
    v = c.get("struct") or c.get("params")
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except (json.JSONDecodeError, TypeError):
            return {}
    return v if isinstance(v, dict) else {}


def _cand_type(c) -> str:
    """CandidateType (mechanical): smiles=molecule; base only=system;
    struct/params variants: electrolyte keys=formulation, else structure."""
    if not isinstance(c, dict):
        return "Molecule"
    if c.get("smiles"):
        return "Molecule"
    variant = _variant_dict(c)
    if variant:
        if any("electrolyte" in str(k).lower() or "transference" in str(k).lower() for k in variant):
            return "Formulation"
        return "Structure"
    if c.get("base"):
        return "System"
    return "Molecule"


def _cand_content(c) -> str:
    if not isinstance(c, dict):
        return str(c)
    if c.get("smiles"):
        return str(c["smiles"])
    if c.get("base"):
        return str(c["base"])
    variant = _variant_dict(c)
    if variant:
        return "; ".join(f"{k} = {_fmt_num(v)}" for k, v in variant.items())
    return ""


def _source_chip(c) -> str:
    source = str(c.get("source") or "") if isinstance(c, dict) else ""
    cls = "seed" if source.lower() == "seed" else "free" if source.lower() in ("free_gen", "free") else ""
    return f'<span class="chip tag {cls}">{_html_escape(source.upper())}</span>' if source and cls else ""


def _cand_component(c) -> str:
    """CandidateComponent (mechanical): molecule/formulation→Electrolyte;
    system→Cell system; struct/params keys→component."""
    t = _cand_type(c)
    if t in ("Molecule", "Formulation"):
        return "Electrolyte"
    if t == "System":
        return "Cell system"
    struct = _variant_dict(c) if isinstance(c, dict) else {}
    comps = []
    for k in struct:
        ks = str(k)
        if "Separator" in ks:
            comps.append("Separator")
        elif "collector" in ks:
            comps.append("Current collector")
        elif "Electrolyte" in ks:
            comps.append("Electrolyte")
        elif "Positive electrode" in ks:
            comps.append("Cathode")
        elif "Negative electrode" in ks:
            comps.append("Anode")
    if not comps:
        return "Structure"
    return " + ".join(dict.fromkeys(comps))  # dedupe, keep order


def _cand_row(c) -> str:
    """Candidate table row: candidate (name+source) | component | type | role | content."""
    if isinstance(c, dict):
        name = str(c.get("name") or "")
        role = str(c.get("role") or "")
        content = _cand_content(c)
        src = _source_chip(c)
    else:
        name, role, content, src = "", "", str(c), ""
    head = f"<b>{_html_escape(name)}</b>{src}" if name else f'<span class="sm">{_html_escape(content)}</span>'
    return (
        f"<tr><td>{head}</td><td>{_html_escape(_cand_component(c))}</td>"
        f"<td>{_html_escape(_cand_type(c))}</td><td>{_html_escape(role)}</td>"
        f"<td class='mono'>{_html_escape(content)}</td></tr>"
    )


_CAND_HEAD = "<tr><th>Candidate</th><th>Component</th><th>Type</th><th>Role</th><th>Content</th></tr>"


def _read_goal(case_dir: str) -> str | None:
    """Read the design goal from config.yaml (returns None when missing/corrupt, stated as-is)."""
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
    if "fail" in v or v in ("fail", "failed", "reject", "rejected", "no"):
        return "bad"
    if "pass" in v or v in ("pass", "passed", "ok", "yes"):
        return "ok"
    return "neutral"


def _verdict_badge(verdict: str) -> str:
    cls = _verdict_class(verdict)
    return f'<span class="badge {cls}">{_html_escape(str(verdict))}</span>'


# Five-stage flow (1=planning, 2–4=funnel stages, 5=True DFT/MD endorsement; the stage
# numbering matches the SKILL.md flow. Stage 5 reuses the .badge.stage.end copper style to
# set it apart.)
_STAGE_LABELS = {1: "STAGE 1 Plan", 2: "STAGE 2 Materials", 3: "STAGE 3 Cell", 4: "STAGE 4 Safety", 5: "STAGE 5 True DFT/MD"}


def _stage_badge(stage: int | None) -> str:
    """Small STAGE badge (blueprint style: monospace 10.5px bordered badge, reusing .badge + --blue/--accent)."""
    if stage not in _STAGE_LABELS:
        return ""
    cls = "badge stage end" if stage == 5 else "badge stage"
    return f'<span class="{cls}">{_STAGE_LABELS[stage]}</span>'


def _stage_range_badge(lo: int, hi: int) -> str:
    """Round-card stage-range badge: a single stage reuses _stage_badge; a span shows STAGE N–M (en dash).
    The range is built only from numeric stages (1–5), and stage 5 (True DFT/MD endorsement) may take
    part in a range (e.g. STAGE 4–5); endorse/final entries do not enter round cards, and stage 5 is
    shown separately in the Flow overview row."""
    if lo == hi:
        return _stage_badge(lo)
    if lo not in _STAGE_LABELS or hi not in _STAGE_LABELS:
        return ""
    return f'<span class="badge stage">STAGE {lo}–{hi}</span>'


def _entry_stage(e: dict) -> int | None:
    """log entry → flow stage: plan=1 (overall design planning); mol. propose/funnel=2 (materials);
    struct propose=3 (cell); evaluate inferred from content (safety metrics=4, struct=3, else=2);
    endorse/final=5 (True DFT/MD endorsement)."""
    action = e.get("action")
    if action == "plan":
        return 1
    if action in ("endorse", "final"):
        return 5
    if action == "propose":
        has_struct = any(
            isinstance(c, dict) and c.get("struct") for c in _as_list(e.get("candidates"))
        )
        return 3 if has_struct else 2
    if action == "funnel":
        return 2
    if action == "evaluate":
        # Structured metrics first (safety metrics=stage 4, struct coverage=stage 3), with a text
        # fallback — not relying on the word "struct" happening to appear
        # (observed: the agent's log evaluate entries carry no "struct" wording, which used to be
        # misjudged as a materials round=2)
        metrics = e.get("metrics") or {}
        has_safety = isinstance(metrics.get("T_max_K"), (int, float)) or "plated" in metrics
        if has_safety:
            return 4
        text = json.dumps(e, ensure_ascii=False)
        if "struct" in text:
            return 3
        return 2
    return None


def _plot_stage(filename: str) -> int | None:
    """Curve filename → stage: discharge=3 (Cell design), charge/aging=4 (safety/aging assessment); if it cannot be decided, no stage is attached."""
    low = filename.lower()
    if "discharge" in low:
        return 3
    if "charge" in low or "aging" in low:
        return 4
    return None


def _threshold_text(value) -> str:
    if isinstance(value, bool):
        return "No plating" if not value else "Plating allowed"
    if isinstance(value, dict):
        parts = []
        if "min" in value:
            parts.append(f"≥ {_fmt_num(value['min'], sig=5)}")
        if "max" in value:
            parts.append(f"≤ {_fmt_num(value['max'], sig=5)}")
        return " · ".join(parts) if parts else ""
    return _fmt_num(value)


_STAGE_KEYS = ("stage1", "stage2", "stage3", "meta")
_STAGE_NAMES = {"stage1": "Materials design", "stage2": "Cell design", "stage3": "Safety assessment", "meta": "Case parameters"}
_STAGE1_UNITS = {"max_energy_ev": "eV", "max_homo_ev": "eV"}


def _normalize_criteria(criteria: dict) -> dict[str, dict]:
    """criteria → {"stage1"/"stage2"/"stage3"/"meta": {...}}.

    The new protocol is explicitly layered (stageN/meta keys); old logs use flat keys (such as
    T_max_C), grouped by key name: potential window/elimination line (homo/energy_ev/voltage/
    window) → stage1; capacity/Energy density (capacity/density) → stage2; temperature/plating
    (t_max/temp/plat) → stage3; everything else → meta.
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
    """Merge the stage1–3 Thresholds into a flat dict (for the mechanical KPI/Achieved column comparison; meta does not participate)."""
    norm = _normalize_criteria(criteria)
    merged: dict = {}
    for k in ("stage1", "stage2", "stage3"):
        merged.update(norm[k])
    return merged


def _achieve_cell(value, spec) -> str:
    """Single Metric Achieved cell: value vs {"min"/"max"} Threshold → ✓/✗ badge + the Achieved value; no data → em dash."""
    if isinstance(value, bool):
        show = "No plating" if not value else "Plating risk"
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
    """Stage-header "Achieved" badge: stage1 looks at the funnel; stage2/3 look at the metric comparison; no data → mute."""
    if stage_key == "stage1":
        if funnel_latest is None:
            return '<span class="badge mute">Not run</span>'
        n, m = _to_int(funnel_latest.get("passed")), _to_int(funnel_latest.get("disputed"))
        # Divergence is not failure (the protocol: "divergence is a signal to think harder"), and
        # its handling is recorded in the funnel detail;
        # stage 2 Achieved = some candidate passed the funnel (passed > 0)
        cls = "ok" if n > 0 else "bad"
        return f'<span class="badge {cls}">Achieved · PASS {n} · DISP {m}</span>'
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
        return '<span class="badge mute">Not run</span>'
    if all(verdicts):
        return '<span class="badge ok">All achieved</span>'
    return '<span class="badge bad">Partially achieved</span>'


def _criteria_html(criteria: dict, log: list[dict]) -> str:
    if not criteria:
        return (
            '<p class="empty">No data</p>'
            '<p class="hint">No criteria recorded (log.jsonl entry 0 missing).</p>'
        )
    norm = _normalize_criteria(criteria)
    metrics = _latest_metrics(log)
    funnels = [e for e in log if e.get("action") == "funnel"]
    funnel_latest = funnels[-1] if funnels else None
    blocks = []
    for stage_key, name in (("stage1", "Materials design"), ("stage2", "Cell design"),
                            ("stage3", "Safety assessment"), ("meta", "Case parameters")):
        stage_dict = norm.get(stage_key, {})
        if stage_key == "meta":
            head = ('<div class="stage-goal-head"><span class="badge mute">META</span>'
                    f'<span class="stage-goal-name">{name}</span></div>')
            if not stage_dict:
                table = '<p class="empty">Not provided</p>'
            else:
                rows = "".join(
                    "<tr>"
                    f"<th scope='row'>{_html_escape(str(k))}</th>"
                    f"<td class='num'>{_html_escape(_fmt_num(v))}</td>"
                    "</tr>"
                    for k, v in stage_dict.items()
                )
                table = f'<table class="tbl"><tr><th>Parameter</th><th>Value</th></tr>{rows}</table>'
            blocks.append(f'<div class="stage-goal meta">{head}{table}</div>')
            continue
        stage_num = int(stage_key[-1])
        head = (
            f'<div class="stage-goal-head">{_stage_badge(stage_num)}'
            f'<span class="stage-goal-name">{name}</span>'
            f"{_stage_achieve_badge(stage_key, stage_dict, metrics, funnel_latest)}</div>"
        )
        if not stage_dict:
            table = '<p class="empty">No separate targets (see other stages)</p>'
            blocks.append(f'<div class="stage-goal">{head}{table}</div>')
            continue
        has_achieve = stage_key in ("stage2", "stage3")
        head_cells = "<tr><th>Metric</th><th>Threshold</th>" + ("<th>Achieved</th>" if has_achieve else "") + "<th>Note</th></tr>"
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
    """SHEET 01 candidates involved: master table of all propose/endorse candidates, deduplicated (in first-appearance order)."""
    seen: dict[str, object] = {}
    order: list[str] = []
    for e in log:
        for c in _as_list(e.get("candidates")):
            key = str(c.get("name") or c.get("smiles") or "") if isinstance(c, dict) else str(c)
            if key and key not in seen:
                seen[key] = c
                order.append(key)
    if not order:
        return '<p class="empty">No data</p>'
    rows = "".join(_cand_row(seen[k]) for k in order)
    return f'<table class="tbl cand">{_CAND_HEAD}{rows}</table>'


def _goal_mark(ok: bool) -> str:
    return '<b class="goal-ok">✓</b>' if ok else '<b class="goal-bad">✗</b>'


def _goal_parts(stage_key: str, stage_dict: dict) -> str:
    """Compressed stage-goal text: 'E ≤ 0.0 eV · HOMO ≤ −6.0 eV' / 'Energy density ≥ 300 Wh/kg', etc."""
    labels = {
        "max_energy_ev": "E", "max_homo_ev": "HOMO",
        "energy_density_wh_kg": "Energy density", "capacity_ah": "Capacity", "T_max_K": "T_max",
    }
    units = {"max_energy_ev": "eV", "max_homo_ev": "eV", "energy_density_wh_kg": "Wh/kg", "T_max_K": "K"}
    parts = []
    for k, v in stage_dict.items():
        if isinstance(v, bool):
            parts.append(_threshold_text(v))
            continue
        if isinstance(v, str):
            continue  # free-text rules (such as plating_rule) do not enter the compressed goal row
        label = labels.get(k, str(k))
        if isinstance(v, dict):
            t = _threshold_text(v)
            parts.append(f"{label} {t}" if t else f"{label} {_fmt_num(v)}")
        else:
            sign = "≤ " if stage_key == "stage1" else ""
            unit = units.get(k, "")
            parts.append(f"{label} {sign}{_fmt_num(v)}{' ' + unit if unit else ''}")
    return " · ".join(parts) if parts else "No targets"


def _flow_achieve(stage_key: str, stage_dict: dict, log: list[dict]) -> str:
    """Flow-row Achieved summary: stage1 looks at the latest funnel; stage2/3 look at the latest evaluation's metric comparison."""
    if stage_key == "stage1":
        funnels = [e for e in log if e.get("action") == "funnel"]
        if not funnels:
            return "—"
        f = funnels[-1]
        n, m = _to_int(f.get("passed")), _to_int(f.get("disputed"))
        # stage 2 Achieved = some candidate passed the funnel (divergence already handled, recorded in the funnel detail)
        return f"PASS {n} · DISP {m} {_goal_mark(n > 0)}"
    metrics = _latest_metrics(log)
    if not stage_dict or not metrics:
        return "—"
    parts = []
    for k, v in stage_dict.items():
        mv = metrics.get(k)
        if isinstance(v, bool) and isinstance(mv, bool):
            parts.append(f"{'No plating' if not mv else 'Plating risk'}{_goal_mark(mv == v)}")
        elif isinstance(mv, (int, float)) and isinstance(v, dict) and ("min" in v or "max" in v):
            ok = True
            if "min" in v and isinstance(v["min"], (int, float)):
                ok = ok and mv >= v["min"]
            if "max" in v and isinstance(v["max"], (int, float)):
                ok = ok and mv <= v["max"]
            parts.append(f"{_fmt_num(mv)}{_goal_mark(ok)}")
    return " · ".join(parts) if parts else "—"


def _flow_html(log: list[dict], cell_files: list[tuple[str, dict]], criteria: dict) -> str:
    """Overview-area Flow overview row: five stage badges, each with a count/conclusion summary plus
    target and Achieved (mechanically derived from criteria and log).

    Stage 1 overall design planning = plan entries; stage 2 Materials design = mol. propose/funnel
    (verdict layer stage1); stage 3 Cell design = struct propose/discharge curves (verdict layer
    stage2); stage 4 Safety assessment = charge45 curves (verdict layer stage3); stage 5 True DFT/MD
    endorsement = endorse/final (including the final conclusion).
    """
    mol_prop = struct_prop = funnel_n = endorse_n = final_n = plan_n = 0
    for e in log:
        action = e.get("action")
        if action == "funnel":
            funnel_n += 1
        elif action == "endorse":
            endorse_n += 1
        elif action == "final":
            final_n += 1
        elif action == "plan":
            plan_n += 1
        elif action == "propose":
            for c in _as_list(e.get("candidates")):
                if isinstance(c, dict) and c.get("struct"):
                    struct_prop += 1
                else:
                    mol_prop += 1
    n_discharge = sum(1 for fname, _ in cell_files if _plot_stage(fname) == 3)
    n_charge45 = sum(1 for fname, _ in cell_files if _plot_stage(fname) == 4)
    finals = [e for e in log if e.get("action") == "final"]
    verdict = str(finals[-1].get("verdict") or "") if finals else ""
    close_sum = f"Endorse {endorse_n} · Final {final_n}" + (f" · Verdict {verdict}" if verdict else "")
    norm = _normalize_criteria(criteria)
    # Flow stage → verdict layer key mapping (numbering is independent; stages 2/3/4 correspond to verdict layers stage1/2/3)
    stage_to_key = {2: "stage1", 3: "stage2", 4: "stage3"}
    items = (
        (1, "Stage 1 · Overall planning", f"plan {plan_n} · design_plan.md"),
        (2, "Stage 2 · Materials design", f"mol. propose {mol_prop} · funnel {funnel_n}"),
        (3, "Stage 3 · Cell design", f"struct. propose {struct_prop} · discharge curves {n_discharge}"),
        (4, "Stage 4 · Safety assessment", f"4C charge curves {n_charge45}"),
        (5, "Stage 5 · True DFT/MD endorsement", close_sum),
    )
    blocks = []
    for stage, name, count in items:
        goal_html = ""
        if stage in (2, 3, 4):
            stage_key = stage_to_key[stage]
            stage_dict = norm.get(stage_key, {})
            goal_html = (
                f'<div class="flow-goal"><span class="g-label">Goal</span>'
                f"<span>{_html_escape(_goal_parts(stage_key, stage_dict))}</span></div>"
                f'<div class="flow-goal"><span class="g-label">Achieved</span>'
                f"<span>{_flow_achieve(stage_key, stage_dict, log)}</span></div>"
            )
        blocks.append(
            f'<div class="flow-item {"end" if stage == 5 else ""}">{_stage_badge(stage)}'
            f'<div class="flow-name">{_html_escape(name)}</div>'
            f'<div class="flow-count">{_html_escape(count)}</div>{goal_html}</div>'
        )
    return f'<div class="flow">{"".join(blocks)}</div>'


def _kpi_compare(value, thresholds: dict, key: str, direction: str) -> tuple[str, str]:
    """Key results vs the flattened Thresholds (stage1–3 merged), compared mechanically → (color class, Threshold description)."""
    spec = thresholds.get(key)
    thr = spec.get(direction) if isinstance(spec, dict) else None
    if not isinstance(value, (int, float)) or not isinstance(thr, (int, float)):
        return "", ""
    ok = (value >= thr) if direction == "min" else (value <= thr)
    sign = "≥" if direction == "min" else "≤"
    return ("ok" if ok else "bad"), f"Threshold {sign} {_fmt_num(thr, sig=5)}"


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
        ("energy_density_wh_kg", "Energy density", "Wh/kg", "min"),
        ("capacity_ah", "Capacity", "Ah", None),
        ("T_max_K", "Max temperature", "K", "max"),
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
            items.append(_kpi_item("Plating", "No plating", "", "ok", "anode potential stayed ≥ 0 V"))
        else:
            items.append(_kpi_item("Plating", "Plating risk", "", "bad", "anode potential dropped below 0 V"))
    else:
        items.append(_kpi_item("Plating", None, "", "mute", "Not provided"))
    return f'<div class="kpi-grid">{"".join(items)}</div>'


def _header_html(case_dir: str, log: list[dict], criteria: dict) -> str:
    case_name = Path(case_dir).name or "case"
    goal = _read_goal(case_dir) or "(Goal not recorded in config.yaml)"
    meta_criteria = _normalize_criteria(criteria).get("meta", {})
    meta = []
    if "real_compute" in meta_criteria:
        meta.append("Real compute on" if meta_criteria["real_compute"] is True else "Real compute off")
    meta_html = "".join(f"<span>{_html_escape(m)}</span>" for m in meta)

    final_entries = [e for e in log if e.get("action") == "final"]
    verdict = str(final_entries[-1].get("verdict") or "") if final_entries else ""
    if not verdict:
        verdict, vcls = "Not adjudicated", "neutral"
    else:
        vcls = _verdict_class(verdict)
    verdict_html = (
        '<div class="verdict-block"><div class="eyebrow light">Conclusion</div>'
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
    cands = _as_list(e.get("candidates"))
    rows = "".join(_cand_row(c) for c in cands)
    table = f'<table class="tbl cand">{_CAND_HEAD}{rows}</table>' if rows else ""
    reason = e.get("llm_reason")
    reason_html = f'<p class="reason">{_html_escape(str(reason))}</p>' if reason else ""
    return (
        '<div class="blk"><div class="blk-label">Propose · Candidates</div>'
        f"{table}{reason_html}</div>"
    )


def _funnel_entry_html(e: dict) -> str:
    chips = "".join(
        f'<span class="chip">{lab} <b class="num">{_to_int(e.get(k))}</b></span>'
        for k, lab in (("passed", "PASS"), ("rejected", "REJECT"), ("disputed", "DISP."))
    )
    table = ""
    disp = _as_list(e.get("dispositions"))
    if disp:
        rows = []
        for d in disp:
            if isinstance(d, dict):
                name = str(d.get("name") or "")
                status = str(d.get("status") or "")
                reason = str(d.get("reason") or "")
                cls = {"rejected": "bad", "passed": "ok", "disputed": "warn"}.get(status, "mute")
                badge = f'<span class="badge {cls}">{_html_escape(status)}</span>'
                rows.append(
                    f"<tr><td>{_html_escape(name)}</td><td>{badge}</td>"
                    f"<td>{_html_escape(reason)}</td></tr>"
                )
            else:
                rows.append(f"<tr><td>{_html_escape(str(d))}</td><td></td><td></td></tr>")
        table = (
            f'<table class="tbl"><tr><th>Candidate</th><th>Disposition</th><th>Reason</th></tr>'
            f'{"".join(rows)}</table>'
        )
    detail = e.get("detail")
    detail_html = f"<p>{_html_escape(str(detail))}</p>" if detail else ""
    return f'<div class="blk"><div class="blk-label">Funnel · Screening</div>{chips}{table}{detail_html}</div>'


def _evaluate_html(e: dict) -> str:
    metrics = e.get("metrics") or {}
    rows = "".join(
        f"<tr><td>{_html_escape(str(k))}</td>"
        f"<td class='num'>{_html_escape(_fmt_num(v))}</td></tr>"
        for k, v in metrics.items()
    )
    verdict = e.get("verdict")
    verdict_html = _verdict_badge(str(verdict)) if verdict else '<span class="badge mute">N/A</span>'
    cmp_table = ""
    comp = _as_list(e.get("comparison"))
    if comp:
        keys: list[str] = []
        for c in comp:
            if isinstance(c, dict):
                for k in (c.get("metrics") or {}):
                    if k not in keys:
                        keys.append(k)
        if keys:
            head = (
                "<tr><th>Candidate</th>"
                + "".join(f"<th>{_html_escape(str(k))}</th>" for k in keys)
                + "<th>Verdict</th></tr>"
            )
            body = []
            for c in comp:
                if not isinstance(c, dict):
                    body.append(f"<tr><td>{_html_escape(str(c))}</td></tr>")
                    continue
                name = str(c.get("name") or c.get("candidate") or "")
                m = c.get("metrics") or {}
                cells = f"<td>{_html_escape(name)}</td>"
                for k in keys:
                    if k not in m:
                        cells += "<td class='num'>—</td>"
                    elif isinstance(m[k], bool):
                        cells += f"<td class='num'>{'No plating' if not m[k] else 'Plating risk'}</td>"
                    else:
                        cells += f"<td class='num'>{_html_escape(_fmt_num(m[k]))}</td>"
                v = c.get("verdict")
                cells += (
                    f"<td>{_verdict_badge(str(v))}</td>" if v
                    else '<td><span class="badge mute">—</span></td>'
                )
                body.append(f"<tr>{cells}</tr>")
            cmp_table = f'<table class="tbl">{head}{"".join(body)}</table>'
    note = e.get("note")
    note_html = f'<p class="reason">{_html_escape(str(note))}</p>' if note else ""
    return (
        f'<div class="blk"><div class="blk-label">Evaluate {verdict_html}</div>'
        f'<table class="tbl"><tr><th>Metric</th><th>Value</th></tr>{rows}</table>{cmp_table}{note_html}</div>'
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
        return '<p class="empty">No data</p>'
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
            subs.append(f"{len(_as_list(prop.get('candidates')))} candidates")
        m = ev.get("metrics", {}) if ev else {}
        if isinstance(m.get("T_max_K"), (int, float)):
            subs.append(f"T_max {_fmt_num(m['T_max_K'])} K")
        if isinstance(m.get("plated"), bool):
            subs.append("No plating" if not m["plated"] else "Plating risk")
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


def _rounds_ov_html(log: list[dict]) -> str:
    """Round overview table at the top of the iteration trajectory: round/stage/candidate count/key metrics/conclusion (mechanically derived from propose/evaluate)."""
    groups: dict[int, list[dict]] = {}
    for e in log:
        r = e.get("round")
        if r is None or _to_int(r) <= 0:
            continue
        if e.get("action") not in ("propose", "funnel", "evaluate"):
            continue
        groups.setdefault(_to_int(r), []).append(e)
    if not groups:
        return ""
    rows = []
    for r, entries in sorted(groups.items()):
        ev = next((e for e in entries if e.get("action") == "evaluate"), None)
        prop = next((e for e in entries if e.get("action") == "propose"), None)
        stages = [s for s in (_entry_stage(e) for e in entries) if s is not None]
        stage_html = _stage_range_badge(min(stages), max(stages)) if stages else ""
        n_cand = len(_as_list(prop.get("candidates"))) if prop else 0
        m = ev.get("metrics", {}) if ev else {}
        ed = (
            _fmt_num(m["energy_density_wh_kg"])
            if isinstance(m.get("energy_density_wh_kg"), (int, float))
            else "—"
        )
        cap = _fmt_num(m["capacity_ah"]) if isinstance(m.get("capacity_ah"), (int, float)) else "—"
        tmax = _fmt_num(m["T_max_K"]) if isinstance(m.get("T_max_K"), (int, float)) else "—"
        if isinstance(m.get("plated"), bool):
            plated = (
                '<span class="badge ok">No plating</span>' if not m["plated"]
                else '<span class="badge bad">Plating risk</span>'
            )
        else:
            plated = '<span class="badge mute">—</span>'
        verdict = str(ev.get("verdict") or "") if ev else ""
        v_html = _verdict_badge(verdict) if verdict else '<span class="badge mute">—</span>'
        rows.append(
            f"<tr><td class='num'>R{_to_int(r):02d}</td><td>{stage_html}</td>"
            f"<td class='num'>{n_cand}</td><td class='num'>{_html_escape(ed)}</td>"
            f"<td class='num'>{_html_escape(cap)}</td><td class='num'>{_html_escape(tmax)}</td>"
            f"<td>{plated}</td><td>{v_html}</td></tr>"
        )
    head = (
        "<tr><th>Round</th><th>Stage</th><th>Cands</th><th>Energy density Wh/kg</th>"
        "<th>Capacity Ah</th><th>T_max K</th><th>Plating</th><th>Verdict</th></tr>"
    )
    return f'<div class="ov-head">Round overview</div><table class="tbl ov">{head}{"".join(rows)}</table>'


def _trend_bars(caption: str, rows: list[tuple[str, float]], threshold: tuple | None) -> str:
    """Per-round metric bar chart (inline SVG); threshold = (value, label) draws a reference line."""
    W, H = 340, 200
    pad_l, pad_r, pad_t, pad_b = 42, 12, 16, 28
    vals = [v for _, v in rows if isinstance(v, (int, float))]
    if not vals:
        return ""
    tvals = [threshold[0]] if threshold and isinstance(threshold[0], (int, float)) else []
    lo, hi = min(vals + tvals), max(vals + tvals)
    if lo > 0:
        lo = 0.0
    span = (hi - lo) or 1.0
    n = len(rows)
    gap = (W - pad_l - pad_r) / n
    bw = min(46.0, gap * 0.6)
    els = []
    for i in range(3):
        gy = pad_t + (H - pad_t - pad_b) * i / 2
        els.append(f'<line class="grid" x1="{pad_l}" y1="{gy:.1f}" x2="{W - pad_r}" y2="{gy:.1f}"/>')
        els.append(
            f'<text x="{pad_l - 4}" y="{gy + 3:.1f}" text-anchor="end">{_fmt_num(hi - span * i / 2)}</text>'
        )
    els.append(f'<line class="axis" x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H - pad_b}"/>')
    els.append(f'<line class="axis" x1="{pad_l}" y1="{H - pad_b}" x2="{W - pad_r}" y2="{H - pad_b}"/>')
    for i, (label, v) in enumerate(rows):
        x = pad_l + gap * i + (gap - bw) / 2
        h = (v - lo) / span * (H - pad_t - pad_b)
        y = H - pad_b - h
        els.append(f'<rect class="bar" x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}"/>')
        els.append(
            f'<text x="{pad_l + gap * i + gap / 2:.1f}" y="{H - pad_b + 15:.1f}" '
            f'text-anchor="middle">{_html_escape(str(label))}</text>'
        )
        els.append(
            f'<text x="{pad_l + gap * i + gap / 2:.1f}" y="{y - 5:.1f}" '
            f'text-anchor="middle">{_fmt_num(v)}</text>'
        )
    if threshold and isinstance(threshold[0], (int, float)):
        ty = H - pad_b - (threshold[0] - lo) / span * (H - pad_t - pad_b)
        els.append(f'<line class="thr" x1="{pad_l}" y1="{ty:.1f}" x2="{W - pad_r}" y2="{ty:.1f}"/>')
        els.append(
            f'<text class="t-label" x="{W - pad_r}" y="{ty - 5:.1f}" text-anchor="end">'
            f'{_html_escape(str(threshold[1]))} {_fmt_num(threshold[0], sig=5)}</text>'
        )
    svg = (
        f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{_attr_escape(caption)}">'
        f"<title>{_html_escape(caption)}</title>" + "".join(els) + "</svg>"
    )
    return f'<div class="trend"><div class="trend-caption">{_html_escape(caption)}</div>{svg}</div>'


def _trends_html(log: list[dict], criteria: dict) -> str:
    """Per-round Energy density/T_max Trends chart (mechanically derived from evaluate metrics; Threshold lines come from criteria)."""
    evals = [e for e in log if e.get("action") == "evaluate"]
    ed_rows: list[tuple[str, float]] = []
    tmax_rows: list[tuple[str, float]] = []
    for e in evals:
        r = e.get("round")
        label = f"R{_to_int(r):02d}" if r is not None else "R—"
        m = e.get("metrics") or {}
        if isinstance(m.get("energy_density_wh_kg"), (int, float)):
            ed_rows.append((label, m["energy_density_wh_kg"]))
        if isinstance(m.get("T_max_K"), (int, float)):
            tmax_rows.append((label, m["T_max_K"]))
    if not ed_rows and not tmax_rows:
        return ""
    thr = _flat_thresholds(criteria)
    ed_thr = None
    spec = thr.get("energy_density_wh_kg")
    if isinstance(spec, dict) and "min" in spec:
        ed_thr = (spec["min"], "Target ≥")
    tmax_thr = None
    spec = thr.get("T_max_K")
    if isinstance(spec, dict) and "max" in spec:
        tmax_thr = (spec["max"], "Limit ≤")
    charts = []
    if ed_rows:
        charts.append(_trend_bars("Energy density trend (per evaluate round)", ed_rows, ed_thr))
    if tmax_rows:
        charts.append(_trend_bars("T_max trend (per evaluate round)", tmax_rows, tmax_thr))
    if not charts:
        return ""
    return f'<div class="ov-head">Trends</div><div class="trends">{"".join(charts)}</div>'


def _funnel_html(log: list[dict]) -> str:
    entries = [e for e in log if e.get("action") == "funnel"]
    if not entries:
        return '<p class="empty">No data</p>'
    totals = {k: sum(_to_int(e.get(k)) for e in entries) for k in ("passed", "rejected", "disputed")}
    stats = (
        f'<div class="stat pass"><div class="stat-num">{totals["passed"]}</div>'
        '<div class="stat-label">Passed</div></div>'
        f'<div class="stat rej"><div class="stat-num">{totals["rejected"]}</div>'
        '<div class="stat-label">Rejected</div></div>'
        f'<div class="stat dis"><div class="stat-num">{totals["disputed"]}</div>'
        '<div class="stat-label">Disputed</div></div>'
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
    """run-pyamm curve output among cell/*.json (containing time_s and at least one equal-length curve series)."""
    cell_dir = Path(case_dir) / "cell"
    if not cell_dir.is_dir():
        return []
    out = []
    for p in sorted(cell_dir.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            # e.g. log-evaluate --batch-file inputs (rN_batch_eval.json are JSON
            # lists) carry no curves; skip non-dict payloads instead of crashing.
            continue
        t = data.get("time_s")
        if isinstance(t, list) and len(t) >= 2:
            if any(
                isinstance(data.get(k), list) and len(data.get(k)) == len(t)
                for k in ("voltage_v", "anode_potential_v")
            ):
                out.append((p.name, data))
            continue
        # Aging protocol output shape: cycle_numbers + capacity_ah_per_cycle
        cn = data.get("cycle_numbers")
        cap = data.get("capacity_ah_per_cycle")
        if (
            isinstance(cn, list)
            and isinstance(cap, list)
            and len(cn) == len(cap) >= 2
        ):
            out.append((p.name, data))
    return out


def _svg_plot(filename: str, data: dict) -> str:
    """run-pyamm output → inline SVG curve (grid + series + axis labels + tooltip data).

    Discharge/fast-charge protocols: time_s on the x-axis, a voltage_v/anode_potential_v pair of series;
    aging protocol: cycle_numbers on the x-axis, a single capacity_ah_per_cycle series.
    """
    aging = isinstance(data.get("capacity_ah_per_cycle"), list) and isinstance(
        data.get("cycle_numbers"), list
    )
    if aging:
        t = data["cycle_numbers"]
        series = {"capacity_ah_per_cycle": data["capacity_ah_per_cycle"]}
    else:
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

    for key, cls in (
        ("voltage_v", "s-voltage"),
        ("anode_potential_v", "s-anode"),
        ("capacity_ah_per_cycle", "s-voltage"),
    ):
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
        side = 1 if key in ("voltage_v", "capacity_ah_per_cycle") else -1
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
    if "capacity_ah_per_cycle" in series:
        elements.append(f'<text x="{x0 + 4}" y="{y0 + 10}" fill="var(--blue)">— capacity [Ah]</text>')

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
    elements.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{_VIEW_H - 8}" text-anchor="middle">{"cycle" if aging else "time [s]"}</text>')

    model = str(data.get("model_used") or "N/A")
    label = f"{filename} curves (model {model})"
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
            '<p class="empty">No data</p>'
            '<p class="hint">No run-pyamm curve output found in cell/'
            " (JSON with time_s and voltage_v / anode_potential_v).</p>"
        )
    figures = []
    for idx, (fname, data) in enumerate(cell_files, start=1):
        model = str(data.get("model_used") or "N/A")
        chips = f'<span class="chip">MODEL {_html_escape(model)}</span>'
        if isinstance(data.get("T_max_K"), (int, float)):
            chips += f'<span class="chip">T_max {_fmt_num(data["T_max_K"])} K</span>'
        if isinstance(data.get("sei_thickness_nm_end"), (int, float)):
            chips += f'<span class="chip">SEI_end {_fmt_num(data["sei_thickness_nm_end"])} nm</span>'
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
        return '<p class="empty">No data</p>'
    blocks = []
    for e in entries:
        if e.get("skipped"):
            reason = str(e.get("reason") or "reason not recorded")
            names = " · ".join(
                str(c.get("name") or c.get("smiles") or c) if isinstance(c, dict) else str(c)
                for c in _as_list(e.get("candidates"))
            )
            names_html = (
                f'<br><span class="reason">Candidates: {_html_escape(names)}</span>' if names else ""
            )
            blocks.append(
                '<div class="skipped"><span class="badge mute">Skipped</span> '
                f'True-compute endorsement skipped<span class="reason"> — {_html_escape(reason)}</span>'
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
    fallback = '<p class="empty">No recommendation (not achieved)</p>'
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
        parts.append(f'<div class="final-verdict">Conclusion {_verdict_badge(verdict)}</div>')
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
        return '<p class="empty">No data</p>'
    return "".join(blocks)


def _fill_template(parts: dict[str, str]) -> str:
    """One-shot replacement of the template placeholders; a missing slot is an error (better to fail than to emit a defective report)."""
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
        "TITLE": f"{Path(case_dir).name} · Virtual Battery Factory Design Report",
        "HEADER": _header_html(case_dir, log, criteria),
        "CRITERIA_TABLE": _criteria_html(criteria, log),
        "FLOW": _flow_html(log, cell_files, criteria),
        "CANDIDATES": _candidates_html(log),
        "ROUNDS_OV": _rounds_ov_html(log),
        "TRENDS": _trends_html(log, criteria),
        "ROUNDS": _rounds_html(log),
        "FUNNEL": _funnel_html(log),
        "PLOTS": _plots_html(cell_files),
        "ENDORSE": _endorse_html(log),
        "FINAL": _final_html(log),
        "NOTES": _notes_html(log),
    }
    html = _fill_template(parts)
    out_p = Path(out_html)
    # out semantics: a plain filename → relative to case_dir (default report.html); containing a
    # directory (absolute/full relative) → the full path
    # (observed: a full relative path used to get concatenated into a doubled case_dir/full-path directory)
    out_path = Path(case_dir) / out_html if out_p.parent == Path(".") else out_p
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
