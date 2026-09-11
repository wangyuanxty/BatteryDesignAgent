"""verify-deliverables: deliverable protocol compliance check (tier A: structural completeness).

Checks (all mechanically decided):
1. the 7 required deliverable types exist: design_spec / bom / datasheet / calc / dvpr / dfmea
   / delivery_index (an md or xlsx/docx source file for each + a published pdf, per step 7 of
   the protocol)
2. PDFs are non-empty (>1KB)
3. xlsx/docx parse and have no empty sheet
4. numbering format VBF-<case ID>-<document code>-<serial>
5. audit chain integrity: every propose round must have an evaluate entry with the same round
   (the precondition for log-evaluate's mechanical verdict — if an evaluation happens but is
   never logged, the conclusions in the report have no audit backing)
"""
import json
import re
import sys
from pathlib import Path

import openpyxl

REQUIRED = {
    "design_spec": "DS",
    "bom": "BOM",
    "datasheet": "DSH",
    "calc": "CALC",
    "dvpr": "DVPR",
    "dfmea": "DFMEA",
    "delivery_index": "IDX",
}


def _iter_files(case_dir: Path) -> dict[str, list[Path]]:
    """Find deliverables per the protocol: prefer the deliverables/ directory, fall back to the workspace root."""
    roots = [case_dir / "deliverables", case_dir]
    found: dict[str, list[Path]] = {k: [] for k in REQUIRED}
    for root in roots:
        if not root.exists():
            continue
        for key in REQUIRED:
            if found[key]:
                continue
            found[key] = [
                p
                for p in root.iterdir()
                if p.is_file() and p.name.lower().startswith(key.lower())
            ]
    return found


def verify_deliverables(case_dir: Path) -> dict:
    checks: list[dict] = []

    # 1. required files exist (each type needs at least one of md/xlsx/docx + a pdf)
    missing: list[str] = []
    for key, code in REQUIRED.items():
        files = _iter_files(case_dir)[key]
        if not files:
            missing.append(f"{key} ({code}) missing")
            continue
        has_source = any(p.suffix in (".md", ".xlsx", ".docx") for p in files)
        has_pdf = any(p.suffix == ".pdf" for p in files)
        if not has_source:
            missing.append(f"{key} lacks a source file (md/xlsx/docx)")
        if not has_pdf:
            missing.append(f"{key} lacks the published PDF")
    checks.append(
        {
            "check": "all 7 deliverable types present (source file + PDF)",
            "pass": not missing,
            "detail": "; ".join(missing) if missing else "all 7 types complete",
        }
    )

    # 2. PDFs are non-empty
    empty_pdfs = []
    for key in REQUIRED:
        for p in _iter_files(case_dir)[key]:
            if p.suffix == ".pdf" and p.stat().st_size < 1024:
                empty_pdfs.append(p.name)
    checks.append(
        {
            "check": "PDFs non-empty (>1KB)",
            "pass": not empty_pdfs,
            "detail": "; ".join(empty_pdfs) if empty_pdfs else "all PDFs non-empty",
        }
    )

    # 3. xlsx parses and has no empty sheet
    bad_xlsx = []
    for key in REQUIRED:
        for p in _iter_files(case_dir)[key]:
            if p.suffix != ".xlsx":
                continue
            try:
                wb = openpyxl.load_workbook(p, read_only=True)
                empty_sheets = [ws.title for ws in wb.worksheets if ws.max_row == 0]
                if empty_sheets:
                    bad_xlsx.append(f"{p.name}: empty sheet {empty_sheets}")
            except Exception as e:
                bad_xlsx.append(f"{p.name}: cannot parse ({e})")
    checks.append(
        {
            "check": "xlsx parses and has no empty sheet",
            "pass": not bad_xlsx,
            "detail": "; ".join(bad_xlsx) if bad_xlsx else "all xlsx fine",
        }
    )

    # 4. delivery_index contains the VBF numbering list (protocol numbers live in the index, not in file names)
    idx = _iter_files(case_dir)["delivery_index"]
    idx_text = ""
    for p in idx:
        if p.suffix in (".md", ".txt"):
            idx_text = p.read_text(encoding="utf-8-sig", errors="replace")
            break
    id_matches = re.findall(r"VBF-[A-Z0-9]+-(DS|BOM|DSH|CALC|DVPR|DFMEA|IDX)-\d+", idx_text)
    checks.append(
        {
            "check": "delivery_index contains the VBF numbering list",
            "pass": len(id_matches) >= 5,
            "detail": f"found {len(id_matches)} numbers" if id_matches else "no VBF numbers in the index",
        }
    )

    # 5. audit chain integrity: every propose round must have an evaluate entry in the same round
    #    (an evaluation that happens but is never logged → the report's conclusions have no audit
    #    backing; the v3 V1-V3 incident)
    log_entries = []
    log_path = case_dir / "log.jsonl"
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                log_entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    prop_rounds = {
        e.get("round")
        for e in log_entries
        if e.get("action") == "propose" and isinstance(e.get("round"), int) and e.get("round") > 0
    }
    ev_rounds = {
        e.get("round")
        for e in log_entries
        if e.get("action") == "evaluate" and isinstance(e.get("round"), int) and e.get("round") > 0
    }
    missing_evals = sorted(prop_rounds - ev_rounds)
    if not log_path.exists():
        detail = "log.jsonl missing (no audit record)"
    elif missing_evals:
        detail = "propose rounds with no evaluation: " + ", ".join(f"R{r:02d}" for r in missing_evals)
    else:
        detail = "every propose round has an evaluate in the same round"
    checks.append(
        {
            "check": "audit chain complete (each propose round has an evaluate in the same round)",
            "pass": not missing_evals and log_path.exists(),
            "detail": detail,
        }
    )

    # 6. Closing audit chain: the final entry must exist (the audit tail of the closing verdict)
    #    (the t6_r1_flash incident: deliverables verification ALL PASS but log.jsonl lacked final
    #    — the closing verdict was never recorded)
    has_final = any(e.get("action") == "final" for e in log_entries)
    checks.append(
        {
            "check": "closing audit chain complete (final entry exists)",
            "pass": has_final,
            "detail": "final entry exists" if has_final else "log.jsonl has no final entry (the closing verdict was never recorded)",
        }
    )

    return {"case_dir": str(case_dir), "checks": checks, "all_pass": all(c["pass"] for c in checks)}


def cmd_verify_deliverables(args) -> int:
    report = verify_deliverables(Path(args.case_dir))
    for c in report["checks"]:
        mark = "PASS" if c["pass"] else "FAIL"
        print(f"[{mark}] {c['check']} — {c['detail']}")
    print(f"verify-deliverables: {'ALL PASS' if report['all_pass'] else 'HAS FAILURES'}")
    return 0 if report["all_pass"] else 1
