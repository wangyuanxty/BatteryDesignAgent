"""Rebuild known_set_comp after spinel extension (T9 v8 sealing).

Reads comp_out_spinels.json (run with CUDA py312), appends the documented
spinel family computed points to the envelope hull, and appends the
documented non-computable high-voltage frameworks (tavorite fluorophosphates,
NASICON, oxyfluorides, Na cathodes) to the known-composition membership list.

Usage (repo root): python rebuild_envelope.py
"""
import json
from pathlib import Path

BASE = Path("runs/exp/known_set_comp")

# Documented cathode frameworks whose structures run-comp cannot represent
# (no prototype; computed points would be a different compound, e.g. F dropped).
# Membership-layer only - never enter the hull.
LIST_ONLY = [
    {"name": "LiVPO4F",   "formula": "LiVPO4F",      "note": "tavorite fluorophosphate, lit ~4.3-4.5 V"},
    {"name": "Li2CoPO4F", "formula": "Li2CoPO4F",    "note": "tavorite fluorophosphate, lit ~4.9-5.0 V"},
    {"name": "Li2NiPO4F", "formula": "Li2NiPO4F",    "note": "tavorite fluorophosphate, theoretical"},
    {"name": "NVP",       "formula": "Li3V2(PO4)3",  "note": "NASICON, lit ~4.0 V"},
    {"name": "Li2MnO2F",  "formula": "Li2MnO2F",     "note": "oxyfluoride, lit (Rossen/Manthiram-era & 2020s)"},
    {"name": "Li2NiO2F",  "formula": "Li2NiO2F",     "note": "oxyfluoride, theoretical/experimental reports"},
    {"name": "Na3V2",     "formula": "Na3V2(PO4)3",  "note": "Na NASICON cathode, lit ~3.4 V"},
]

env = json.loads((BASE / "envelope_stats_comp.json").read_text(encoding="utf-8"))
spin = json.loads((BASE / "comp_out_spinels.json").read_text(encoding="utf-8"))

added: list[dict] = []
for c in spin.get("candidates", []):
    if c.get("avg_voltage_v") is not None:
        added.append({
            "name": c["name"], "formula": c["formula"],
            "V": c["avg_voltage_v"], "C": c.get("capacity_mah_g", 0) or 0,
            "stab": c.get("rel_stability_ev_atom", 0) or 0,
        })

old_n = env["n"]
env["points"] = env["points"] + added
env["n"] = len(env["points"])
env["sealing"] = {
    "added_spinels": [a["name"] for a in added],
    "membership_only": len(LIST_ONLY),
    "note": "v8 sealing: documented high-voltage frameworks fully covered (hull points + membership list)",
}
(BASE / "envelope_stats_comp.json").write_text(
    json.dumps(env, indent=2, ensure_ascii=False), encoding="utf-8")

kc = json.loads((BASE / "known_compositions.json").read_text(encoding="utf-8"))
existing = {c["formula"] for c in kc}
new_entries = [{"name": a["name"], "formula": a["formula"]} for a in added]
new_entries += [e for e in LIST_ONLY if e["formula"] not in existing]
new_entries = [{"name": e["name"], "formula": e["formula"]} for e in new_entries]
kc = kc + new_entries
(BASE / "known_compositions.json").write_text(
    json.dumps(kc, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"hull points: {old_n} -> {env['n']} (+{len(added)} spinels)", flush=True)
print(f"known list: {len(kc)} entries (+{len(new_entries)})", flush=True)
for a in added:
    print(f"  {a['name']:12s} V={a['V']:.3f} C={a['C']:.1f} stab={a['stab']:.3f}", flush=True)
