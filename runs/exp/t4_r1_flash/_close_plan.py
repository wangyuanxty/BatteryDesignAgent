"""Append closing status to design_plan.md (UTF-8 safe)."""
from pathlib import Path

p = Path(r"runs\exp\t4_r1_flash\design_plan.md")
closing = """

---

## Closing status (2026-08-25)

- Final candidate **B7_ThinCellE2_h40** confirmed at **DFN precision** (model_used=DFN, no fallback) in round-6 evaluate:
  -20 degC 1C retention 0.99286 (>= 0.95) | ED 460.06 Wh/kg (>= 327.18) | 899.25 Wh/L (>= 880.0) | 4C/45 degC T_max 329.61 K (<= 333.15) | plating-free (anode min +0.019 V) | overcharge 0.5C->4.7 V without thermal runaway (triggered=false).
- Stage 5 true DFT/MD endorsement: **skipped** (real_compute=false, contract meta); recorded as skipped, not fabricated.
- Audit: log.jsonl complete (entry 0 criteria/meta, plan + 1 plan update, R1-R5 propose/evaluate, round-6 final evaluate, endorse, final verdict **achieved**).
- Deliverables: 14 files in deliverables/ (7 sources + 7 PDFs), `bda verify-deliverables` ALL PASS.
"""
with p.open("a", encoding="utf-8") as f:
    f.write(closing)
print("design_plan.md closed, total bytes:", p.stat().st_size)
