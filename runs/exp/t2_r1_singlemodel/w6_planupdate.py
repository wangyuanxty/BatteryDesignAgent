"""Plan-update entry: D_ec finalization driven by solver-completion measurement."""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

REPO = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent")
CASE_DIR = REPO / "runs" / "exp" / "t2_r1_singlemodel"
ws = CaseWorkspace("exp/t2_r1_singlemodel")

entry = {
    "action": "plan",
    "update": True,
    "reason": (
        "key measurement overturns plan expectation (trigger 3): aging-500 at D_ec=8e-20 dies "
        "deterministically at cycle ~174 (IDA_CONV_FAIL at t=1559961.475 s, |h|=hmin; retried "
        "identically) -> 8e-20 cannot produce a 500-cycle SEI value. Fallback D_ec=1e-19 "
        "completes all 500 cycles with SEI 439.74 nm <= 550. D_ec chain: 1e-18 -> 585.18 nm "
        "@100 / 1083.29 nm @500; 2e-19 -> 272.64 / 611.79; 1e-19 -> (re-measuring) / 439.74."
    ),
    "candidate_strategy": (
        "FINAL SEI pack: D_ec = 1e-19 m2/s (500-cycle completable + criterion met). "
        "params_r3*.json updated from 8e-20 to 1e-19. 4C/energy/lowT outputs unaffected by "
        "D_ec (D_ec only enters SEI growth; those protocols verified identical across D_ec "
        "edits). SEI100 re-measured at 1e-19 (predicted ~194 nm by measured exponent 0.475; "
        "criterion <= 500 with huge margin). Old 8e-20 aging100 kept as "
        "cell/r3_aging100_d8e20.json (audit)."
    ),
    "budget_allocation": "aging100 re-measure + closing (evaluates, endorse-skip, final, deliverables).",
}
already = [json.loads(l) for l in (CASE_DIR / "log.jsonl").read_text(encoding="utf-8-sig").splitlines()]
if any(e.get("action") == "plan" and e.get("update")
       and "dies deterministically at cycle" in str(e.get("reason", "")) for e in already):
    print("plan-update already appended — skipping append")
else:
    append_entry(ws, entry)
    print("plan-update appended")

# also refresh design_plan.md revision history line
plan = CASE_DIR / "design_plan.md"
text = plan.read_text(encoding="utf-8-sig")
marker = "## Revision history"
if marker in text:
    text = text.split(marker)[0] + marker + f"""

- 2026-08-25 (D_ec finalization): aging-500 @8e-20 dies deterministically at cycle ~174
  (IDA_CONV_FAIL, retried identically) -> cannot complete 500 cycles. Fallback 1e-19
  completes 500 cycles, SEI500 439.74 nm <= 550. FINAL D_ec = 1e-19 (params_r3*.json
  updated; 4C/energy/lowT unaffected — D_ec only enters SEI growth; SEI100 re-measured)."""
    plan.write_text(text, encoding="utf-8")
    print("design_plan.md revision history updated")
