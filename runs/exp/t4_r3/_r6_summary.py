"""t4_r3: derive round-6 retentions + summarize V14/V16/V17."""
import json

from bda.store import CaseWorkspace

ws = CaseWorkspace("exp/t4_r3", root="runs")

for v in ("V14", "V16", "V17"):
    lowt = json.loads((ws.path / f"cell/r6_{v}_1c_lowT_spme.json").read_text(encoding="utf-8-sig"))
    rt = json.loads((ws.path / f"cell/r6_{v}_1c_25C_spme.json").read_text(encoding="utf-8-sig"))
    en = json.loads((ws.path / f"cell/r6_{v}_energy.json").read_text(encoding="utf-8-sig"))
    hot = json.loads((ws.path / f"cell/r6_{v}_4C_45C_spme.json").read_text(encoding="utf-8-sig"))
    pct = 100.0 * lowt["capacity_ah"] / rt["capacity_ah"]
    ap_min = min(hot.get("anode_potential_v", [1.0]))
    out = {
        "lowT_retention_1C_pct": round(pct, 4),
        "capacity_ah_lowT_253K": lowt["capacity_ah"],
        "capacity_ah_25C": rt["capacity_ah"],
        "definition": "100 * capacity_ah(lowT_discharge 1C 253.15K) / capacity_ah(1C_discharge 298.15K), identical params; mechanical derivation from run-pyamm outputs",
    }
    (ws.path / f"bridge/r6_{v}_lowT_retention.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"r6_{v}: retention={pct:6.2f}%  cap25C={rt['capacity_ah']:.4f}  cap_lowT={lowt['capacity_ah']:.4f}  "
        f"ED_kg={en['energy_density_wh_kg']:8.1f}  ED_L={en['energy_density_wh_l']:8.1f}  "
        f"E_wh={en['energy_wh']:.3f}  T_max_4C={hot['T_max_K']:7.2f}  anode_min={ap_min:+.4f}V  "
        f"model={hot['model_used']}"
    )