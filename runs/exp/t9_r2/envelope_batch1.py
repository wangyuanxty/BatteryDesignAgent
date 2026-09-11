"""T9_R2: A1 hull adjudication for all batch-1 candidates with computed avg_voltage >= 5.3 V.
Replayable: reads comp_batch1_out.json, prints + writes JSON verdicts (no recompute).
"""
import json
import sys
from pathlib import Path

REPO = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent")
sys.path.insert(0, str(REPO))
from comp_envelope_check import adjudicate  # noqa: E402

WS = REPO / "runs" / "exp" / "t9_r2"
KNOWN = REPO / "runs" / "exp" / "known_set_comp" / "known_set_v2.json"

out = json.loads((WS / "comp_batch1_out.json").read_text(encoding="utf-8"))
results = []
for c in out["candidates"]:
    v = c.get("avg_voltage_v")
    if v is None or v < 5.3:
        continue
    pt = [v, c.get("capacity_mah_g", 0), c.get("rel_stability_ev_atom", 0)]
    res = adjudicate(pt, f"{c['formula']} ({c['name']})", path=KNOWN)
    results.append(res)
    print(json.dumps(res, ensure_ascii=False))

(WS / "envelope_batch1_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nwrote {len(results)} verdicts -> envelope_batch1_results.json")
