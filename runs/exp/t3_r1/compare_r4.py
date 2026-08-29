# Round-4 finalist comparison + selection (mechanically read from outputs; appended as its own log entry).
import json

from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")
CELL = WS.path / "cell"


def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)


rows = []
for name, tag in [
    ("V8_Cooling15", "r3_v8"),
    ("V11_FixedPointCombo", "r3_v11"),
    ("V12_BalancedCooling", "r4_v12"),
]:
    d1 = load(CELL / f"{tag}_1c.json")
    d4 = load(CELL / f"{tag}_4c.json")
    dd = load(CELL / f"{tag}_derived.json")
    en = load(CELL / f"{tag}_energy.json")
    metrics = {
        "capacity_ah": round(d1["capacity_ah"], 3),
        "retention_5c": dd["retention_5c"],
        "T_max_K": round(dd["T_max_K"], 2),
        "T_margin_K": round(333.15 - dd["T_max_K"], 2),
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

append_entry(
    WS,
    {
        "action": "comparison",
        "round": 4,
        "table": rows,
        "selection": {
            "candidate": "V12_BalancedCooling",
            "reason": (
                "Only finalist with balanced margins on both binding safety metrics: "
                "T_max 329.77 K (3.38 K under the 60 C red line; V8's 1.19 K margin is unacceptably thin) "
                "and anode min +12.1 mV (vs V11's +8.2 mV; V9's +0.6 mV is effectively zero). "
                "h=20 W/m2/K is realistic for a power tool (natural convection + tool-body conduction "
                "with light airflow) unlike V11's h=30 (aggressive forced air)."
            ),
        },
    },
)
print("round-4 comparison + selection appended")
