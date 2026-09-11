"""T9_R2: build flat per-candidate metric files for bda log-evaluate (top-level scalars only).
All values are extracted mechanically from the tool outputs; nothing is typed by hand:
  - avg_voltage_v / capacity / rel_stability / converged  <- comp_batch1_out.json
  - in_envelope                                            <- envelope_batch1_results.json
  - in_known                                               <- known_set_v2.json membership (A0)
  - true_voltage_v (finalist only)                         <- b_prime_evidence.json
"""
import json
import sys
from pathlib import Path

REPO = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent")
sys.path.insert(0, str(REPO))
from comp_envelope_check import known_check  # noqa: E402

WS = REPO / "runs" / "exp" / "t9_r2"
KNOWN = REPO / "runs" / "exp" / "known_set_comp" / "known_set_v2.json"

batch = json.loads((WS / "comp_batch1_out.json").read_text(encoding="utf-8-sig"))
env = {e["name"]: e for e in
       json.loads((WS / "envelope_batch1_results.json").read_text(encoding="utf-8-sig"))}
bp = json.loads((WS / "b_prime_evidence.json").read_text(encoding="utf-8-sig")) if (WS / "b_prime_evidence.json").exists() else {}

finalist = "LiNiPO4F"
made = []
for c in batch["candidates"]:
    v = c.get("avg_voltage_v")
    if v is None or v < 5.3:
        continue
    f = c["formula"]
    flat = {
        "in_known": known_check(f, KNOWN),
        "avg_voltage_v": v,
        "capacity_mah_g": c["capacity_mah_g"],
        "rel_stability_ev_atom": c["rel_stability_ev_atom"],
        "converged": c["converged"],
        "in_envelope": env[f + " (" + c["name"] + ")"]["in_envelope"],
    }
    if f == finalist and bp:
        flat["true_voltage_v"] = bp["true_voltage_v"]
        out = WS / "finalist_metrics.json"
    else:
        out = WS / f"ev_{c['name']}.json"
    out.write_text(json.dumps(flat, indent=2, ensure_ascii=False), encoding="utf-8")
    made.append(str(out.name))
print("wrote:", made)
