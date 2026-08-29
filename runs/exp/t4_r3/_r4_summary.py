"""t4_r3: derive round-4 retentions + summarize V8/V9 (system switches)."""
import json

from bda.store import CaseWorkspace

ws = CaseWorkspace("exp/t4_r3", root="runs")

for v in ("V8", "V9"):
    lowt = json.loads((ws.path / f"cell/r4_{v}_1c_lowT_spme.json").read_text(encoding="utf-8-sig"))
    rt = json.loads((ws.path / f"cell/r4_{v}_1c_25C_spme.json").read_text(encoding="utf-8-sig"))
    en = json.loads((ws.path / f"cell/r4_{v}_energy.json").read_text(encoding="utf-8-sig"))
    hot = json.loads((ws.path / f"cell/r4_{v}_4C_45C_spme.json").read_text(encoding="utf-8-sig"))
    pct = 100.0 * lowt["capacity_ah"] / rt["capacity_ah"]
    ap_min = min(hot.get("anode_potential_v", [1.0]))
    out = {
        "lowT_retention_1C_pct": round(pct, 4),
        "capacity_ah_lowT_253K": lowt["capacity_ah"],
        "capacity_ah_25C": rt["capacity_ah"],
        "definition": "100 * capacity_ah(lowT_discharge 1C 253.15K) / capacity_ah(1C_discharge 298.15K), identical params; mechanical derivation from run-pyamm outputs",
    }
    (ws.path / f"bridge/r4_{v}_lowT_retention.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    inj = hot.get("injected_defaults", {})
    print(
        f"r4_{v}: retention={pct:6.2f}%  cap25C={rt['capacity_ah']:.4f}  cap_lowT={lowt['capacity_ah']:.4f}  "
        f"ED_kg={en['energy_density_wh_kg']:8.1f}  ED_L={en['energy_density_wh_l']:8.1f}  "
        f"E_wh={en['energy_wh']:.3f}  mass={en['mass_kg']:.4f}  T_max_4C={hot['T_max_K']:7.2f}  "
        f"anode_min={ap_min:+.4f}V  injected={len(inj)}keys  model={hot['model_used']}"
    )