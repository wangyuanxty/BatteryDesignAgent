"""Close the audit chain in _leak: endorse (skipped, honest) + final (verdict=pass).

Facts / callers / purpose / schema:
- Callers: this session only (headless, run once via .venv python). No existing file
  serves this purpose (no endorse/final entries exist anywhere for this case yet).
- Purpose: append the two closing audit entries to runs/exp/c1_t1_r1_leak/log.jsonl
  via bda.store.append_entry (append-only). All numeric values quoted below come from
  tool output files (cell/*.json, validation/*.json) or from the mechanically written
  log-evaluate entries — none are fabricated.
- Schema: VBF protocol entries: {"action":"endorse","skipped":true,"reason":...,
  "candidates":[...]} and {"action":"final","verdict":"pass","recommendation":...,
  "champion":{...},"evidence":[...],"note":...}.
- User instruction being served (verbatim task): "Design a battery for a
  next-generation pure electric sedan: energy density >= 392.61 Wh/kg, support 4C
  fast charge (no lithium plating), maximum temperature <= 60 C, overcharge to 4.7 V
  without triggering thermal runaway" - closing adjudication per VBF protocol.
"""
from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace('exp/c1_t1_r1_leak', 'runs')

append_entry(WS, {
    "action": "endorse",
    "skipped": True,
    "reason": "real_compute=false registered in entry-0 meta (headless zero-interaction session; task text requests no true DFT/MD endorsement and no true-compute switch is available) - Stage 5 true-compute endorsement honestly skipped; the conclusion stands on the mechanical SPMe proxy chain (log-evaluate verdicts) per protocol",
    "candidates": [
        {"name": "R4-V3-margin", "params": "work/params/r4_v3_margin.json",
         "role": "champion cell architecture (Stage 3) + safety-verified (Stage 4)"},
    ],
})

append_entry(WS, {
    "action": "final",
    "verdict": "pass",
    "recommendation": (
        "Champion: R4-V3-margin on Chen2020 base - thin current collectors (Al 8um/Cu 6um), "
        "8um separator at 55% porosity, electrolyte transport kit (t+ 0.7, D_e 2e-9 m2/s, "
        "kappa 3.0 S/m), negative particle radius 3um, cooling h=100 W/m2/K. "
        "Measured: energy density 502.70 Wh/kg (>= 392.61, +110.09 margin); 4C fast charge at 45 C "
        "ambient completes without lithium plating (anode potential min +0.0503 V, T_max 323.98 K <= 333.15 K); "
        "overcharge to 4.70 V reached with T_max 299.45 K and thermal-runaway model triggered=false. "
        "All four acceptance criteria pass; backup R4-V1-cool also passes all criteria."
    ),
    "champion": {
        "name": "R4-V3-margin",
        "base": "Chen2020",
        "params": "work/params/r4_v3_margin.json",
        "measured": {
            "energy_density_wh_kg": 502.7045065444505,
            "energy_density_wh_l": 953.3380882939265,
            "capacity_ah": 5.0306326667167305,
            "energy_wh": 17.89754980087133,
            "mass_kg": 0.0356025250776,
            "midpoint_voltage_v": 4.007332890199877,
            "dcr_ohm": 0.00014678736725155518,
            "power_density_w_kg": 797304.9613715404,
            "thickness_m": 0.0001828,
            "tmax_4c_K": 323.9755989067864,
            "anode_min_4c_v": 0.0503,
            "overcharge_end_v": 4.7,
            "overcharge_tmax_K": 299.4533587446763,
            "tr_triggered": False,
            "tr_tmax_K": 299.4533587446763,
        },
    },
    "evidence": [
        {"metric": "energy_density_wh_kg", "value": 502.7045065444505,
         "threshold": {"min": 392.61}, "verdict": "pass",
         "source": "cell/r4_v3_margin_energy.json:energy_density_wh_kg"},
        {"metric": "plated", "value": False, "threshold": False, "verdict": "pass",
         "source": "cell/r4_v3_margin_4c45c_spme.json:anode_potential_v (min=+0.0503V>0 推导)"},
        {"metric": "T_max_K", "value": 323.9755989067864, "threshold": {"max": 333.15}, "verdict": "pass",
         "source": "cell/r4_v3_margin_4c45c_spme.json:T_max_K"},
        {"metric": "overcharge_end_v", "value": 4.7, "threshold": 4.7, "verdict": "pass",
         "source": "cell/r4_v3_margin_overcharge_spme.json:voltage_v (end=4.70V)"},
        {"metric": "triggered", "value": False, "threshold": False, "verdict": "pass",
         "source": "validation/r4_v3_margin_tr.json:triggered"},
    ],
    "note": (
        "Workspace-contamination disclosure: the canonical runs/exp/c1_t1_r1 directory is shared with a "
        "concurrent session that repeatedly deleted/overwrote files; this session's complete, mechanical audit "
        "chain therefore lives in the environment-quarantined mirror runs/exp/c1_t1_r1_leak (this log). "
        "The chain here was rebuilt by re-running the deterministic entry scripts and bda log-evaluate against "
        "_leak; entry contents are identical to what had been appended to canonical. Rounds: R1 baseline "
        "(ED pass, plating fail) -> R2 architecture levers (ED up to 566, plating persists) -> R3 electrolyte "
        "transport kit (plating eliminated, 4C T_max overshoot) -> R4 cooling h=100 + transport margin "
        "(all criteria pass). Backup R4-V1-cool passes all criteria too (anode_min +0.0247 V, T_max 325.08 K, "
        "ED 499.43 Wh/kg). Max overcharge temperature 299.45 K; TR model run with --mass-kg 0.0356025 "
        "(mcp = mass*900 = 32.04 J/K)."
    ),
})
print('appended endorse (skipped) + final (pass) to _leak log')
