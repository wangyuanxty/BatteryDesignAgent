"""log-evaluate：评估条目确定性写入（判定由代码完成，agent 只传候选与输出文件）。

背景：agent 在对话里评估候选（读仿真输出、口头下结论）不会自动落日志——
t1_r1_v3 实测 V1-V3 评估只存在于散文引用、审计链无条目。本命令把
"评估发生 → 条目存在"变成机械保证：

- criteria 取自 log.jsonl 第 0 条（开跑前预注册的阈值）
- metrics 从仿真输出 JSON 文件机械提取（plated 由 anode_potential_v 推导）
- verdict 由代码对照阈值判定（min/max 数值 / 布尔等值），agent 不得手写
- evidence 指向实际文件路径与键，数值永远有来源（杜绝幻觉数值）

verdict 规则：被检查的 criteria 非空且全部通过 → pass，否则 fail；
输出文件缺某 criteria 指标 → 记入 entry.unchecked 并在 note 追加说明
（阶段未到的指标属于合法缺失——材料轮评估不测 T_max，由最终
endorse/final 的"无证据不许结案"兜底全 criteria 覆盖）。
"""
import json
import sys
from pathlib import Path

from bda.store import CaseWorkspace, REPO_ROOT, append_entry

_STAGE_KEYS = ("stage1", "stage2", "stage3")  # meta 不参与判定


def load_criteria(ws: CaseWorkspace) -> dict:
    """log.jsonl 第 0 条 criteria（开跑前预注册）；缺失即错误。"""
    log_path = ws.path / "log.jsonl"
    if not log_path.exists():
        raise RuntimeError(f"log.jsonl 不存在：{log_path}（先写 criteria 第 0 条再评估）")
    for line in log_path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        if isinstance(entry.get("criteria"), dict):
            return entry["criteria"]
    raise RuntimeError("log.jsonl 第 0 条 criteria 未找到（评估判定需要预注册阈值）")


def flatten_criteria(criteria: dict) -> dict:
    """stage1–3 合并为扁平 {指标键: 阈值}（meta 不参与判定）。"""
    flat: dict = {}
    for k in _STAGE_KEYS:
        v = criteria.get(k)
        if isinstance(v, dict):
            flat.update(v)
    return flat


def extract_metrics(files: list[Path]) -> dict[str, tuple]:
    """仿真输出 JSON → {指标键: (值, 来源文件)}，后文件覆盖前文件（last-wins）。

    标量（int/float/bool）直接提取；`anode_potential_v` 列表保留给 plated 推导：
    criteria 常含 `plated: false`（要求无析锂）而输出无该键 → 由电压时序
    min < 0 机械推导（v3 人工条目同样口径）。推导结果以 `plated` 键进入
    metrics，`_plated_note` 内部键携带证据来源标注（两者都不进条目 metrics）。
    """
    metrics: dict[str, tuple] = {}
    potentials: dict[Path, list] = {}
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            continue
        for k, v in data.items():
            if isinstance(v, (int, float, bool)):
                metrics[k] = (v, f)
            elif k == "anode_potential_v" and isinstance(v, list) and v:
                potentials[f] = v
    if "plated" not in metrics and potentials:
        f, v = max(potentials.items(), key=lambda kv: len(kv[1]))  # 最完整时序
        mn = min(v)
        metrics["plated"] = (mn < 0.0, f)
        metrics["_plated_note"] = (
            f"anode_potential_v (min={mn:.4g}V{'<' if mn < 0 else '>'}0 推导)",
            f,
        )
    return metrics


def _rel_to(path: Path, base: Path) -> str:
    """来源路径相对化：在 base 下 → 相对 posix 串；否则回退绝对路径。"""
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def _threshold_ok(value, threshold) -> bool:
    """阈值三形态：{"min": n} / {"max": n} / 布尔等值 / 标量数值（视为 min）。"""
    if isinstance(threshold, dict):
        lo = threshold.get("min")
        hi = threshold.get("max")
        if lo is not None or hi is not None:
            # 有数值边界但 value 不可比（str/list）→ 不过；无任何边界 → 视为未限定通过
            if not isinstance(value, (int, float)):
                return False
            if isinstance(lo, (int, float)) and value < lo:
                return False
            if isinstance(hi, (int, float)) and value > hi:
                return False
        return True
    if isinstance(threshold, bool):
        return bool(value) == threshold
    if isinstance(threshold, (int, float)) and isinstance(value, (int, float)):
        return value >= threshold
    return False  # 无法判定的形态一律不过（宁可 fail 不可假 pass）


def check_against_criteria(metrics: dict[str, tuple], thresholds: dict, base: Path) -> tuple[list, list]:
    """→ (evidence 列表, unchecked 键列表)。evidence 指向文件:键，判定结果由代码给出。

    base = case 目录：来源路径相对化（审计日志跨机器可重放，不嵌绝对路径）。
    """
    evidence: list[dict] = []
    unchecked: list[str] = []
    for key, threshold in thresholds.items():
        if key not in metrics:
            unchecked.append(key)
            continue
        value, src = metrics[key]
        source = f"{_rel_to(src, base)}:{key}"
        if key == "plated" and "_plated_note" in metrics:
            note, _ = metrics["_plated_note"]
            source = f"{_rel_to(src, base)}:{note}"
        ok = _threshold_ok(value, threshold)
        evidence.append(
            {
                "metric": key,
                "value": value,
                "threshold": threshold,
                "verdict": "pass" if ok else "fail",
                "source": source,
            }
        )
    return evidence, unchecked


def _evaluate_one(case_dir: Path, records: list, candidate: str, outputs: list[str], note: str) -> dict:
    """单个候选评估（内部共用）：读输出文件 → 机械判定 → 返回条目（不落盘）。"""
    thresholds = None  # 每候选共享同轮 criteria，由调用方传入（见 _evaluate_record）

    files: list[Path] = []
    for arg in outputs:
        p = None
        for cand in (case_dir / arg, REPO_ROOT / arg, Path(arg)):
            if cand.exists() and cand.is_file():
                p = cand
                break
        if p is None:
            raise RuntimeError(f"输出文件不存在：{arg}")
        files.append(p)
    if not files:
        raise RuntimeError("无有效输出文件")
    metrics = extract_metrics(files)
    evidence, unchecked = check_against_criteria(metrics, dict(records), base=case_dir)
    if not evidence:
        raise RuntimeError("输出文件中没有任何 criteria 指标（metrics 为空或键不匹配）")
    verdict = "pass" if all(ev["verdict"] == "pass" for ev in evidence) else "fail"
    note_raw = note or ""
    if unchecked:
        note_raw = (note_raw + "｜" if note_raw else "") + "未检查 criteria: " + ", ".join(unchecked)
    entry = {
        "action": "evaluate",
        "metrics": {
            k: v
            for k, (v, _) in metrics.items()
            if not k.startswith("_") and isinstance(v, (int, float, bool))
        },
        "verdict": verdict,
        "evidence": evidence,
        "note": note_raw,
    }
    if candidate:
        entry["candidate"] = candidate
    if unchecked:
        entry["unchecked"] = unchecked
    return entry


def cmd_log_evaluate(args) -> int:
    case_dir = Path(args.case_dir)
    if not case_dir.is_absolute():
        case_dir = REPO_ROOT / case_dir
    ws = CaseWorkspace(case_dir.name, str(case_dir.parent), create=False)
    criteria = load_criteria(ws)
    thresholds = flatten_criteria(criteria)

    if getattr(args, "batch_file", None):
        # 批量模式：一次评估多个候选，每个候选逐条落 evaluate 条目（机械判定）
        import json as _json

        batch = _json.loads(Path(args.batch_file).read_text(encoding="utf-8-sig"))
        if not isinstance(batch, list) or not batch:
            raise RuntimeError("--batch-file 必须是非空列表 [{'candidate': 'V1', 'outputs': [...], 'note': ...}]")
        for rec in batch:
            if "outputs" not in rec:
                raise RuntimeError(f"batch 记录缺 outputs 键: {rec}")
            rec_round = rec.get("round", args.round)
            entry = _evaluate_one(case_dir, thresholds, rec.get("candidate", ""), rec["outputs"], rec.get("note", ""))
            entry["round"] = rec_round
            append_entry(ws, entry)
            print(
                f"log-evaluate 已记录: round={rec_round} "
                f"candidate={entry.get('candidate', '-')} verdict={entry['verdict']} "
                f"checked={len(entry['evidence'])} unchecked={len(entry.get('unchecked', []))}"
            )
        return 0

    entry = _evaluate_one(case_dir, thresholds, args.candidate or "", args.outputs, args.note or "")
    entry["round"] = args.round
    append_entry(ws, entry)

    print(
        f"log-evaluate 已记录: round={args.round} "
        f"candidate={args.candidate or '-'} verdict={entry['verdict']} "
        f"checked={len(entry['evidence'])} unchecked={len(entry.get('unchecked', []))}"
    )
    for ev in entry["evidence"]:
        print(f"  [{ev['verdict'].upper()}] {ev['metric']} = {ev['value']} 阈值={ev['threshold']} 来源={ev['source']}")
    if entry.get("unchecked"):
        print(f"  [!] 未检查 criteria: {', '.join(entry['unchecked'])}（输出文件缺指标，评估不完整）", file=sys.stderr)
    return 0
