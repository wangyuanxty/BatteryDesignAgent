"""Analyze round-1 xTB screen: family gate + HOMO/LUMO windows + ranking."""
import json
import sys
from pathlib import Path

REPO = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent")
sys.path.insert(0, str(REPO / "runs/exp/known_set_sei"))
from envelope_check import families_matched

HOMO_MAX = -13.74
LUMO_MAX = -7.0

d = json.loads(Path(REPO / "runs/exp/t10_r4/candidates/r1_xtb.json").read_text(encoding="utf-8"))
rows = []
for c in d["candidates"]:
    m = c["metrics"]
    rows.append({
        "smiles": c["smiles"],
        "homo": m["homo_ev"],
        "lumo": m["lumo_ev"],
        "gate": families_matched(c["smiles"]),
        "pass_homo": m["homo_ev"] <= HOMO_MAX,
        "pass_lumo": m["lumo_ev"] <= LUMO_MAX,
    })

pass_both = [r for r in rows if r["pass_homo"] and r["pass_lumo"] and not r["gate"]]
print(f"total {len(rows)}; pass HOMO<={HOMO_MAX}: {sum(r['pass_homo'] for r in rows)}; "
      f"pass LUMO<={LUMO_MAX}: {sum(r['pass_lumo'] for r in rows)}; "
      f"gate violations: {[r['smiles'] for r in rows if r['gate']]}")
print("\n== PASS BOTH WINDOWS (and gate-clean) ==")
for r in sorted(pass_both, key=lambda r: r["homo"]):
    print(f"  {r['smiles']:50s} HOMO {r['homo']:8.3f}  LUMO {r['lumo']:8.3f}")
print("\n== near misses (HOMO<=-12.8 and LUMO<=-6.5, gate-clean), sorted by HOMO ==")
near = [r for r in rows if not r["gate"] and r["homo"] <= -12.8 and r["lumo"] <= -6.5 and r not in pass_both]
for r in sorted(near, key=lambda r: r["homo"]):
    print(f"  {r['smiles']:50s} HOMO {r['homo']:8.3f}  LUMO {r['lumo']:8.3f} "
          f"dh={HOMO_MAX - r['homo']:+.3f} dl={LUMO_MAX - r['lumo']:+.3f}")
print("\n== LUMO pass but HOMO short (gate-clean), sorted by HOMO ==")
short_homo = [r for r in rows if not r["gate"] and r["pass_lumo"] and not r["pass_homo"]]
for r in sorted(short_homo, key=lambda r: r["homo"])[:15]:
    print(f"  {r['smiles']:50s} HOMO {r['homo']:8.3f}  LUMO {r['lumo']:8.3f}")
print("\n== HOMO pass but LUMO short (gate-clean), sorted by LUMO ==")
short_lumo = [r for r in rows if not r["gate"] and r["pass_homo"] and not r["pass_lumo"]]
for r in sorted(short_lumo, key=lambda r: r["lumo"])[:15]:
    print(f"  {r['smiles']:50s} HOMO {r['homo']:8.3f}  LUMO {r['lumo']:8.3f}")
