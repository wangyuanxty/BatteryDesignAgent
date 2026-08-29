# -*- coding: utf-8 -*-
"""Minimal in-place format fix: R5 propose candidate final_archN_DFNconf had 'struct' as a string
(the renderer expects a dict of parameter overrides). Replace with the referenced params dict —
substance unchanged (same candidate, same params file)."""
import json
from pathlib import Path

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
log = WS / "log.jsonl"
params = json.loads((WS / "candidates" / "r4_archN_params.json").read_text(encoding="utf-8-sig"))

lines = log.read_text(encoding="utf-8-sig").splitlines()
out, fixed = [], False
for line in lines:
    line = line.strip()
    if not line:
        continue
    e = json.loads(line)
    if e.get("action") == "propose" and e.get("round") == 5:
        for c in e.get("candidates", []):
            if c.get("name") == "final_archN_DFNconf" and isinstance(c.get("struct"), str):
                c["struct"] = dict(params)
                fixed = True
    out.append(json.dumps(e, ensure_ascii=False))
log.write_text("\n".join(out) + "\n", encoding="utf-8")
print("fixed:", fixed)
