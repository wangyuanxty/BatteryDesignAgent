# Round-3 comparison table (mechanically read from outputs; appended as its own log entry).
import json

from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")
CELL = WS.path / "cell"


def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)


rows = []
for name, tag in [
    ("V7_NPMargin", "v7"),
    ("V8_Cooling15", "v8"),
    ("V9_ModerateElectrolyte", "v9"),
    ("V10_NoPorosityBoost", "v10"),
    ("V11_FixedPointCombo", "v11"),
]:
    d1 = load(CELL / f"r3_{tag}_1c.json")
    d4 = load(CELL / f"r3_{tag}_4c.json")
    dd = load(CELL / f"r3_{tag}_derived.json")
    en = load(CELL / f"r3_{tag}_energy.json")
    metrics = {
        "capacity_ah": round(d1["capacity_ah"], 3),
        "retention_5c": dd["retention_5c"],
        "T_max_K": round(dd["T_max_K"], 2),
        "anode_min_v": round(min(d4.get("anode_potential_v", [])), 4) if d4.get("anode_potential_v") else None,
        "power_density_w_kg": round(en["power_density_w_kg"], 1),
        "dcr_ohm": round(en["dcr_ohm"], 6),
        "mass_kg": round(en["mass_kg"], 5),
    }
    verdict = "pass" if (
        metrics["capacity_ah"] >= 2.0
        and metrics["retention_5c"] >= 0.95
        and metrics["T_max_K"] <= 333.15
        and metrics["anode_min_v"] is not None and metrics["anode_min_v"] >= 0.0
        and metrics["power_density_w_kg"] >= 4000.0
    ) else "fail"
    rows.append({"name": name, "metrics": metrics, "verdict": verdict})

append_entry(WS, {"action": "comparison", "round": 3, "table": rows})
print("comparison entry appended:", json.dumps(rows, ensure_ascii=False)[:400], "...")
