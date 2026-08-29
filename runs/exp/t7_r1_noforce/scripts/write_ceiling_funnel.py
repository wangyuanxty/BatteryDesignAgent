"""Write opening ceiling assessment funnel entry."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t7_r1_noforce", "D:/research/degradation_prognostics/Battery_Design_Agent/runs")
entry = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "Opening ceiling assessment (baseline characterization, ceiling_escalation ON but NOT triggered). "
        "Best-possible Chen2020-system probe = Ceiling Probe A (Cu 6um / Al 10um collectors, 10um separator, "
        "high-transport electrolyte sigma 2.5 S/m / t+ 0.5 / D 5e-10 m2/s, all bridge values domain estimates): "
        "measured ED 486.38 Wh/kg vs objective 327.18 (+48.7% headroom); 4C plating reachable (anode min +0.0254 V) "
        "with high-transport electrolyte (baseline electrolyte fails: min -0.1918 V -> plated); "
        "SEI 45C reachable (476.09 nm baseline / 507.94 nm probeA, both <= 550). "
        "Aging capacity trajectory shows the known climb artifact (1.50->1.99 Ah baseline, 0.97->1.75 Ah probeA: "
        "lithium loss shifts voltage window; sei_thickness_nm_end is the reliable indicator) - annotated honestly. "
        "Nail: both candidates triggered under default near-adiabatic cooling (hA=0.05 W/K; Chen2020 cell-model "
        "conductance = h 10 x A 0.00531 m2 = 0.0531 W/K, same convention). "
        "Conclusion: objective reachable within Chen2020 system; NO Stage 2 material escalation needed. "
        "Failing cause (nail) lives at thermal management - Stage 3 lever (Total heat transfer coefficient), "
        "mapped to run-tr hA = h x 0.00531 m2 (same cooling-area convention as the cell lumped model)."
    ),
}
append_entry(ws, entry)
print("ceiling funnel appended; entries:", len((ws.path / "log.jsonl").read_text(encoding="utf-8").strip().splitlines()))
