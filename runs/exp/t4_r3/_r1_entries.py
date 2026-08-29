"""t4_r3: derive low-T retention JSON (mechanical) + write round-1 propose entry + ceiling-assessment funnel entry."""
import json

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")


def derive_retention(out_name: str, lowt: str, rt: str) -> dict:
    lowt_d = json.loads((ws.path / lowt).read_text(encoding="utf-8-sig"))
    rt_d = json.loads((ws.path / rt).read_text(encoding="utf-8-sig"))
    cap_lowt = float(lowt_d["capacity_ah"])
    cap_rt = float(rt_d["capacity_ah"])
    pct = 100.0 * cap_lowt / cap_rt
    out = {
        "lowT_retention_1C_pct": round(pct, 4),
        "capacity_ah_lowT_253K": cap_lowt,
        "capacity_ah_25C": cap_rt,
        "definition": "100 * capacity_ah(lowT_discharge 1C 253.15K) / capacity_ah(1C_discharge 298.15K), identical params; mechanical derivation from run-pyamm outputs",
    }
    (ws.path / out_name).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_name, "->", out["lowT_retention_1C_pct"], "%")
    return out


derive_retention(
    "bridge/r1_base_lowT_retention.json",
    "cell/r1_base_1c_lowT_spme.json",
    "cell/r1_base_1c_25C_spme.json",
)

propose_r1 = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "struct": {},
            "name": "base_Chen2020",
            "role": "baseline characterization: NMC811/graphite Chen2020 set, empty overrides; anchors retention/ED/vol-ED/T_max/plating and feeds the opening ceiling assessment",
        }
    ],
    "llm_reason": (
        "Round 1 executes the plan's baseline characterization. Empty params; materials = system "
        "baseline (start_stage=3, anchor verified: graphite_LGM50_ocp_Chen2020, NMC811 63104 mol/m3). "
        "Measured (SPMe): cap25C=4.9478 Ah, cap_lowT=4.9196 Ah (retention 99.43%), ED=400.29 Wh/kg, "
        "vol-ED=843.49 Wh/L, 4C45C T_max=332.35 K, anode pot min=-0.438 V (plated). "
        "Gaps: energy_density_wh_l (843.49 vs 880) and plated=true."
    ),
}
append_entry(ws, propose_r1)
print("propose r1 written")

ceiling = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "CEILING ASSESSMENT (opening, ceiling_escalation=ON): measured baseline energy 17.395 Wh at "
        "200.8 um pack (843.5 Wh/L, 400.3 Wh/kg). Contract volume = layer thickness x area; energy at 1C "
        "is time-capped by 3600 s x 5 A (~5 Ah drawn, baseline already 4.948 Ah), so the vol-ED lever is "
        "NOT electrode thickening (volume grows faster than drawable energy) but inactive-layer slimming: "
        "CCs 16+12 um -> 8+6 um and separator 12 -> 8 um cut thickness 200.8 -> 182.8 um (-9%), "
        "projecting ~926 Wh/L and ~490 Wh/kg at unchanged energy; plating margin via N/P (neg 100 um) "
        "and transport boost (sigma/t+/D) fits within 327.18/880 comfortably. "
        "Estimate: best-possible Chen2020 architecture+formulation ceiling >= 900 Wh/L / 480 Wh/kg — "
        "OBJECTIVE BELOW CEILING -> no Stage 2 material escalation needed; stay in Stage 3/4 space "
        "(collected per wall-clock, estimate not masquerading as sim output; sims follow per round)."
    ),
}
append_entry(ws, ceiling)
print("ceiling-assessment funnel written")
print("log.jsonl now has", len((ws.path / "log.jsonl").read_text(encoding="utf-8").splitlines()), "entries")