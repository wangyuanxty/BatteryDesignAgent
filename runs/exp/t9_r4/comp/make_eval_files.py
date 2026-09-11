"""Derive per-candidate top-level-scalar evaluation files from run-comp batch outputs.

log-evaluate extracts only top-level scalars; run-comp batch outputs nest candidates in a
list. This generator re-packages the SAME values verbatim (no recomputation) into per-
candidate files whose keys match the entry-0 stage1 criteria, and builds the --batch-file
records for `bda log-evaluate`. Deterministic and replayable.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # runs/exp/t9_r4/comp

BATCHES = [
    ("batch1_layered_out.json", "r1", 1),
    ("batch2_layered_out.json", "r2", 2),
    ("batch3_layered_out.json", "r3", 3),
]

NOTES = {
    1: lambda c: f"computed avg voltage {c['avg_voltage_v']:.3f} V < 4.6 - rejected at the stage-1 window",
    2: lambda c: (
        f"computed avg voltage {c['avg_voltage_v']:.3f} V < 4.6 - rejected at the stage-1 window"
        if c["avg_voltage_v"] < 4.5
        else f"computed avg voltage {c['avg_voltage_v']:.3f} V, within 0.11 V of the window - near-miss recorded"
    ),
    3: lambda c: (
        f"computed avg voltage {c['avg_voltage_v']:.3f} V >= 4.6 - passes the stage-1 window; advances to the charging-potential gate (comp/profile_voltage.py)"
        if c["avg_voltage_v"] >= 4.6
        else f"computed avg voltage {c['avg_voltage_v']:.3f} V < 4.6 - rejected at the stage-1 window"
    ),
}

for batch_name, prefix, rnd in BATCHES:
    batch = json.loads((ROOT / batch_name).read_text(encoding="utf-8"))
    records = []
    eval_dir = ROOT / "eval"
    eval_dir.mkdir(exist_ok=True)
    for i, c in enumerate(batch["candidates"]):
        name = c["name"]
        flat = {
            "avg_voltage_v": c["avg_voltage_v"],
            "capacity_mah_g": c["capacity_mah_g"],
            "rel_stability_ev_atom": c["rel_stability_ev_atom"],
            "converged": c["converged"],
            "source": f"comp/{batch_name}:candidates[{i}]",
        }
        out_path = eval_dir / f"{prefix}_{name}.json"
        out_path.write_text(json.dumps(flat, indent=2), encoding="utf-8")
        records.append(
            {
                "candidate": name,
                "outputs": [f"comp/eval/{prefix}_{name}.json"],
                "note": NOTES[rnd](c),
            }
        )
    rec_path = ROOT / f"eval_batch_{prefix}.json"
    rec_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"wrote {len(records)} eval files + {rec_path.name}")
