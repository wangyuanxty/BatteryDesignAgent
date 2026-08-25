"""verify-deliverables：交付物协议合规检查（档位 A：结构完整性）。

检查项（全部机械判定）：
1. 7 类必出交付物存在：design_spec / bom / datasheet / calc / dvpr / dfmea / delivery_index
   （每类 md 或 xlsx/docx 源文件 + pdf 发布版，按协议第 7 步）
2. PDF 非空（>1KB）
3. xlsx/docx 可解析且无空 sheet
4. 编号格式 VBF-<案例ID>-<文档码>-<序号>
5. 审计链完整性：每个 propose 轮必须有同 round 的 evaluate 条目（log-evaluate 机械判定
   的前提——评估发生却不落日志，报告里的结论就没有审计背书）
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
    """按协议找交付物：优先 deliverables/ 目录，回退工作区根。"""
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

    # 1. 必出文件存在（每类至少 md/xlsx/docx 之一 + pdf）
    missing: list[str] = []
    for key, code in REQUIRED.items():
        files = _iter_files(case_dir)[key]
        if not files:
            missing.append(f"{key}（{code}）缺失")
            continue
        has_source = any(p.suffix in (".md", ".xlsx", ".docx") for p in files)
        has_pdf = any(p.suffix == ".pdf" for p in files)
        if not has_source:
            missing.append(f"{key} 缺源文件（md/xlsx/docx）")
        if not has_pdf:
            missing.append(f"{key} 缺 PDF 发布版")
    checks.append(
        {
            "check": "7 类交付物齐全（源文件 + PDF）",
            "pass": not missing,
            "detail": "; ".join(missing) if missing else "7 类全部齐备",
        }
    )

    # 2. PDF 非空
    empty_pdfs = []
    for key in REQUIRED:
        for p in _iter_files(case_dir)[key]:
            if p.suffix == ".pdf" and p.stat().st_size < 1024:
                empty_pdfs.append(p.name)
    checks.append(
        {
            "check": "PDF 非空（>1KB）",
            "pass": not empty_pdfs,
            "detail": "; ".join(empty_pdfs) if empty_pdfs else "全部 PDF 非空",
        }
    )

    # 3. xlsx 可解析且无空 sheet
    bad_xlsx = []
    for key in REQUIRED:
        for p in _iter_files(case_dir)[key]:
            if p.suffix != ".xlsx":
                continue
            try:
                wb = openpyxl.load_workbook(p, read_only=True)
                empty_sheets = [ws.title for ws in wb.worksheets if ws.max_row == 0]
                if empty_sheets:
                    bad_xlsx.append(f"{p.name}: 空 sheet {empty_sheets}")
            except Exception as e:
                bad_xlsx.append(f"{p.name}: 无法解析 ({e})")
    checks.append(
        {
            "check": "xlsx 可解析且无空 sheet",
            "pass": not bad_xlsx,
            "detail": "; ".join(bad_xlsx) if bad_xlsx else "xlsx 全部正常",
        }
    )

    # 4. delivery_index 内容含 VBF 编号清单（协议编号在索引里，不在文件名）
    idx = _iter_files(case_dir)["delivery_index"]
    idx_text = ""
    for p in idx:
        if p.suffix in (".md", ".txt"):
            idx_text = p.read_text(encoding="utf-8-sig", errors="replace")
            break
    id_matches = re.findall(r"VBF-[A-Z0-9]+-(DS|BOM|DSH|CALC|DVPR|DFMEA|IDX)-\d+", idx_text)
    checks.append(
        {
            "check": "delivery_index 含 VBF 编号清单",
            "pass": len(id_matches) >= 5,
            "detail": f"找到 {len(id_matches)} 个编号" if id_matches else "索引中无 VBF 编号",
        }
    )

    # 5. 审计链完整性：每个 propose 轮必须有同 round 的 evaluate 条目
    #    （评估发生却不落日志 → 报告中的结论无审计背书，v3 的 V1-V3 事故）
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
        detail = "log.jsonl 缺失（无审计记录）"
    elif missing_evals:
        detail = "缺评估的 propose 轮: " + ", ".join(f"R{r:02d}" for r in missing_evals)
    else:
        detail = "所有 propose 轮均有同轮 evaluate"
    checks.append(
        {
            "check": "审计链完整（每 propose 轮有同轮 evaluate）",
            "pass": not missing_evals and log_path.exists(),
            "detail": detail,
        }
    )

    # 6. 收尾审计链：final 条目必须存在（收尾判词的审计尾）
    #    （t6_r1_flash 事故：交付验证 ALL PASS 但 log.jsonl 缺 final — 收尾未落判词）
    has_final = any(e.get("action") == "final" for e in log_entries)
    checks.append(
        {
            "check": "收尾审计链完整（final 条目存在）",
            "pass": has_final,
            "detail": "final 条目存在" if has_final else "log.jsonl 缺 final 条目（收尾未落判词）",
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
