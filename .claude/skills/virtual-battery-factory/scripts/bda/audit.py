"""log-evaluate: deterministic writing of evaluation entries (the verdict is computed by
code; the agent only passes the candidate and the output files).

Background: when the agent evaluates a candidate in the conversation (reads simulation
output, states a conclusion verbally) nothing is logged automatically — as observed in
t1_r1_v3, where the V1-V3 evaluations existed only as prose references and the audit chain
had no entries. This command turns "an evaluation happened → an entry exists" into a
mechanical guarantee:

- criteria come from entry 0 of log.jsonl (the thresholds pre-registered before the run)
- metrics are extracted mechanically from the simulation output JSON files (plated is
  derived from anode_potential_v)
- the verdict is computed by code against the thresholds (min/max numbers / boolean
  equality); the agent must not write it by hand
- evidence points at the actual file paths and keys, so every number always has a source
  (no hallucinated values)

Verdict rule: the checked criteria are non-empty and all pass → pass, otherwise fail;
if an output file is missing a criterion's metric → it is recorded in entry.unchecked and
a note is appended (a metric whose stage has not been reached yet is a legitimate
absence — a materials-round evaluation does not measure T_max — and the final
endorse/final "no evidence, no closing" rule backstops full criteria coverage).
"""
import json
import sys
from pathlib import Path

from bda.store import CaseWorkspace, REPO_ROOT, append_entry

_STAGE_KEYS = ("stage1", "stage2", "stage3")  # meta does not participate in the verdict


def load_criteria(ws: CaseWorkspace) -> dict:
    """criteria from entry 0 of log.jsonl (pre-registered before the run); missing is an error."""
    log_path = ws.path / "log.jsonl"
    if not log_path.exists():
        raise RuntimeError(f"log.jsonl not found: {log_path} (write the criteria entry 0 before evaluating)")
    for line in log_path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        if isinstance(entry.get("criteria"), dict):
            return entry["criteria"]
    raise RuntimeError("no criteria entry at line 0 of log.jsonl (the verdict needs pre-registered thresholds)")


def flatten_criteria(criteria: dict) -> dict:
    """Merge stage1–3 into a flat {metric key: threshold} (meta does not participate in the verdict)."""
    flat: dict = {}
    for k in _STAGE_KEYS:
        v = criteria.get(k)
        if isinstance(v, dict):
            flat.update(v)
    return flat


def extract_metrics(files: list[Path]) -> dict[str, tuple]:
    """Simulation output JSON → {metric key: (value, source file)}, later files override
    earlier ones (last-wins).

    Scalars (int/float/bool) are extracted directly; the `anode_potential_v` list is kept
    for deriving plated: criteria often contain `plated: false` (requiring no lithium
    plating) while the output has no such key → it is derived mechanically from the voltage
    time series min < 0 (the same convention as the manual v3 entry). The derived result
    enters metrics under the key `plated`, and the internal key `_plated_note` carries the
    evidence provenance annotation (neither enters the entry's metrics).
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
        f, v = max(potentials.items(), key=lambda kv: len(kv[1]))  # most complete time series
        mn = min(v)
        metrics["plated"] = (mn < 0.0, f)
        metrics["_plated_note"] = (
            f"anode_potential_v (min={mn:.4g}V{'<' if mn < 0 else '>'}0 derived)",
            f,
        )
    return metrics


def _rel_to(path: Path, base: Path) -> str:
    """Make the source path relative: under base → relative posix string, else the absolute path."""
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def _threshold_ok(value, threshold) -> bool:
    """Three threshold forms: {"min": n} / {"max": n} / boolean equality / scalar number (treated as min)."""
    if isinstance(threshold, dict):
        lo = threshold.get("min")
        hi = threshold.get("max")
        if lo is not None or hi is not None:
            # A numeric bound exists but value is not comparable (str/list) → fail; no bound
            # at all → treat as unconstrained and pass
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
    return False  # any form that cannot be decided fails (better a fail than a false pass)


def check_against_criteria(metrics: dict[str, tuple], thresholds: dict, base: Path) -> tuple[list, list]:
    """→ (evidence list, unchecked key list). evidence points at file:key and the verdict is
    produced by code.

    base = the case directory: source paths are relativized (the audit log must be
    replayable across machines, so no absolute paths are embedded).
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
    """Evaluate a single candidate (shared internally): read output files → mechanical
    verdict → return the entry (without writing it to disk)."""
    thresholds = None  # every candidate shares the same round's criteria, passed in by the caller (see _evaluate_record)

    files: list[Path] = []
    for arg in outputs:
        p = None
        for cand in (case_dir / arg, REPO_ROOT / arg, Path(arg)):
            if cand.exists() and cand.is_file():
                p = cand
                break
        if p is None:
            raise RuntimeError(f"output file does not exist: {arg}")
        files.append(p)
    if not files:
        raise RuntimeError("no valid output files")
    metrics = extract_metrics(files)
    evidence, unchecked = check_against_criteria(metrics, dict(records), base=case_dir)
    if not evidence:
        raise RuntimeError("no criteria metric in the output files (metrics empty or keys do not match)")
    verdict = "pass" if all(ev["verdict"] == "pass" for ev in evidence) else "fail"
    note_raw = note or ""
    if unchecked:
        note_raw = (note_raw + " | " if note_raw else "") + "unchecked criteria: " + ", ".join(unchecked)
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
        # Batch mode: evaluate several candidates at once, writing one evaluate entry per
        # candidate (mechanical verdict)
        import json as _json

        batch = _json.loads(Path(args.batch_file).read_text(encoding="utf-8-sig"))
        if not isinstance(batch, list) or not batch:
            raise RuntimeError("--batch-file must be a non-empty list [{'candidate': 'V1', 'outputs': [...], 'note': ...}]")
        for rec in batch:
            if "outputs" not in rec:
                raise RuntimeError(f"batch record is missing the outputs key: {rec}")
            rec_round = rec.get("round", args.round)
            entry = _evaluate_one(case_dir, thresholds, rec.get("candidate", ""), rec["outputs"], rec.get("note", ""))
            entry["round"] = rec_round
            append_entry(ws, entry)
            print(
                f"log-evaluate recorded: round={rec_round} "
                f"candidate={entry.get('candidate', '-')} verdict={entry['verdict']} "
                f"checked={len(entry['evidence'])} unchecked={len(entry.get('unchecked', []))}"
            )
        return 0

    entry = _evaluate_one(case_dir, thresholds, args.candidate or "", args.outputs, args.note or "")
    entry["round"] = args.round
    append_entry(ws, entry)

    print(
        f"log-evaluate recorded: round={args.round} "
        f"candidate={args.candidate or '-'} verdict={entry['verdict']} "
        f"checked={len(entry['evidence'])} unchecked={len(entry.get('unchecked', []))}"
    )
    for ev in entry["evidence"]:
        print(f"  [{ev['verdict'].upper()}] {ev['metric']} = {ev['value']} threshold={ev['threshold']} source={ev['source']}")
    if entry.get("unchecked"):
        print(f"  [!] unchecked criteria: {', '.join(entry['unchecked'])} (output files are missing metrics; the evaluation is incomplete)", file=sys.stderr)
    return 0
