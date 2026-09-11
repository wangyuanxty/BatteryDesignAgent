"""Round-4 (charging-potential gate) eval files: merge profile outputs with batch-3 values.

The profile script (comp/profile_voltage.py) outputs avg_voltage_v + charging_potential_v
+ density per candidate but no capacity; capacity_mah_g is copied verbatim from the batch-3
run-comp output. Keys are top-level scalars matching entry-0 stage1 criteria
(avg_voltage_v min 4.6, charging_potential_v max 4.8). Deterministic and replayable.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # runs/exp/t9_r4/comp

profile = json.loads((ROOT / "profile_out.json").read_text(encoding="utf-8"))
batch3 = json.loads((ROOT / "batch3_layered_out.json").read_text(encoding="utf-8"))
by_name = {c["name"]: c for c in batch3["candidates"]}

records = []
eval_dir = ROOT / "eval"
for p in profile["profiles"]:
    name = p.get("name") or p.get("formula")
    if "error" in p:
        records.append({"candidate": name, "outputs": [], "note": f"profile error: {p['error']}"})
        continue
    b = by_name.get(name)
    flat = {
        "avg_voltage_v": p["avg_voltage_v"],
        "charging_potential_v": p["charging_potential_v"],
        "max_incremental_v": p["max_incremental_v"],
        "capacity_mah_g": b["capacity_mah_g"] if b else None,
        "rel_stability_ev_atom": b["rel_stability_ev_atom"] if b else None,
        "density_g_cm3": p["density_g_cm3"],
        "density_source": p["density_source"],
        "converged": p["converged"],
        "source": "comp/profile_out.json + comp/batch3_layered_out.json",
    }
    if flat["capacity_mah_g"] is None:
        del flat["capacity_mah_g"]
        del flat["rel_stability_ev_atom"]
    out_path = eval_dir / f"r4_{name}.json"
    out_path.write_text(json.dumps(flat, indent=2), encoding="utf-8")
    records.append({"candidate": name, "outputs": [f"comp/eval/r4_{name}.json"], "note": f"charging-potential gate: computed avg {p['avg_voltage_v']:.3f} V, charging potential {p['charging_potential_v']:.3f} V"})

rec_path = ROOT / "eval_batch_r4.json"
rec_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
print(f"wrote {len(records)} round-4 eval files + {rec_path.name}")
