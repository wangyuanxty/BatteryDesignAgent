"""t4_r3: summarize round-7 DFN outputs + retain my_Tu summary."""
import json

from bda.store import CaseWorkspace

ws = CaseWorkspace("exp/t4_r3", root="runs")

for name in ("r7_V17_1c_25C_dfn", "r7_V17_1c_lowT_dfn", "r7_V17_4C_45C_dfn"):
    d = json.loads((ws.path / f"cell/{name}.json").read_text(encoding="utf-8-sig"))
    scal = {k: v for k, v in d.items() if isinstance(v, (int, float, bool))}
    ap = d.get("anode_potential_v")
    print(f"{name}: {scal}")
    if ap:
        print(f"   anode_min={min(ap):+.4f}V  len={len(ap)}")