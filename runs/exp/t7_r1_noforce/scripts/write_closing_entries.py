"""Write plan-update, endorse (skip), and final entries."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t7_r1_noforce", "D:/research/degradation_prognostics/Battery_Design_Agent/runs")

plan_update = {
    "action": "plan",
    "update": True,
    "reason": (
        "Key assumption overturned by simulation (R4): SEI-coating lever (SEI kinetic rate constant x0.75) is nearly "
        "inert at 45C because the PyBaMM Yang2017 ec-reaction-limited SEI is solvent-diffusion-limited at ~500 nm "
        "(L*k/D_ec ~ 1e9 >> 1). Empirical decomposition (R2/R3/R4): negative electrode thickness drives SEI "
        "(+~7 nm/um) while negative particle radius drives 4C plating margin (~-17 mV/um) and is ~SEI-neutral "
        "(surface-area effect offset by lower 1C polarization)."
    ),
    "candidate_strategy": (
        "Pivot: thin negative (85.2 um) + small particles (4.0 um) + retained coating (monotone, ~-18 nm) + liquid "
        "cooling h=100 W/m2/K. R5 passes all four criteria with margins: ED 491.47 Wh/kg, SEI 510.51 nm (+39.5 nm "
        "margin), anode min +0.0153 V, nail triggered=false."
    ),
    "budget_allocation": "R1-R5 design rounds spent; closing next (endorse-skip, final, render, deliverables).",
}
append_entry(ws, plan_update)

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": (
        "real_compute=false (protocol default; task text did not request true DFT/MD endorsement). Final design "
        "contains no molecular funnel candidates (materials = Chen2020 system baseline + parameter-bridge estimates "
        "for electrolyte transport (sigma 2.5 S/m, t+ 0.5, D 5e-10 m2/s) and Al2O3 ALD negative coating "
        "(SEI k x0.75), all marked estimate in propose entries). No fabricated DFT/MD values."
    ),
}
append_entry(ws, endorse)

final = {
    "action": "final",
    "recommendation": (
        "HEV cell design achieved on Chen2020 NMC811/graphite system (no material switch needed; ceiling probe "
        "486 Wh/kg >> objective). Final design (round 5): negative 85.2 um graphite, 4.0 um particles with Al2O3 ALD "
        "coating (SEI k 7.5e-13); positive 75.6 um NMC811; separator 10 um; Cu 6 um / Al 10 um current collectors; "
        "high-transport electrolyte (sigma 2.5 S/m, t+ 0.5, D 5e-10 m2/s, bridge estimates); liquid cooling "
        "h=100 W/m2/K (hA = h x A_cool 0.00531 m2 = 0.531 W/K). Measured: ED 491.47 Wh/kg (>=327.18, +164.3), "
        "SEI 510.51 nm after 100 cyc 45C (<=550, +39.5 nm), 4C charge 45C plated=false (anode min +0.0153 V), "
        "nail 10 W triggered=false (T_final 317 K, t_init = 4C T_max 325.5 K); capacity 5.01 Ah, DCR 2.64 mOhm, "
        "power density 43.2 kW/kg. Design facts: cooling is a load-bearing design element - without it (near-adiabatic "
        "hA=0.05 W/K) nail triggers (R1: 70-72 s); electrolyte transport is load-bearing for plating (baseline "
        "electrolyte plates at 4C, R1: anode -0.192 V). Both are design decisions recorded per round, not test "
        "condition relaxation; thresholds unchanged from entry 0."
    ),
    "verdict": "achieved",
}
append_entry(ws, final)
print("plan-update + endorse + final appended; entries:",
      len((ws.path / "log.jsonl").read_text(encoding="utf-8").strip().splitlines()))
