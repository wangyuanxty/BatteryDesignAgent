# Closing log entries: endorse (skipped, real_compute=false) + final (recommendation + verdict).
from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": (
        "real_compute=false (task text did not request true DFT/MD endorsement; protocol default). "
        "The final design V12_BalancedCooling is architecture + electrolyte-transport-parameter level "
        "on the baseline Chen2020 system (NMC811/graphite, 1M LiPF6 EC/EMC): no new molecules or "
        "electrode compositions were invented, so there is no Top-N molecular candidate requiring "
        "first-principles signing. run-orca/run-cp2k/run-md/run-qe were not executed; no DFT/MD "
        "values are claimed anywhere in this case."
    ),
    "candidates": ["V12_BalancedCooling"],
}
append_entry(WS, endorse)

final = {
    "action": "final",
    "recommendation": (
        "Select V12_BalancedCooling (cell/p_v12.json) as the power-tool cell design: NMC811/graphite "
        "(Chen2020 base), positive 40 um / negative 52 um, particle radii 2.0/2.5 um, porosity 0.42/0.35, "
        "separator 12 um (eps 0.47), Al 16 um / Cu 12 um current collectors, electrolyte kappa 1.5 S/m, "
        "D 2.5e-10 m2/s, t+ 0.35, cooling h = 20 W/m2/K, voltage window 2.5-4.2 V, Q_nom 3.08 Ah, "
        "electrode area 0.1027 m2. Measured DFN results vs entry-0 criteria: 1C capacity 3.075 Ah >= 2.0; "
        "5C retention 0.9753 >= 0.95; 4C charge at 45 C ambient T_max 329.77 K (56.62 C) <= 333.15 K with "
        "anode potential min +12.1 mV (no lithium plating); power density 32629.6 W/kg >= 4000 "
        "(calc-energy: mass 29.26 g, DCR 4.41 mOhm, 379.0 Wh/kg, 818.2 Wh/L, midpoint 3.844 V). "
        "Balanced safety margins: 3.38 K thermal, +12.1 mV plating. All values sourced from "
        "cell/r4_v12_*.json via bda log-evaluate round 4 (verdict=pass, 5/5 checked). "
        "Cooling h=20 W/m2/K is realistic for a power tool (natural convection + tool-body conduction "
        "with light airflow). Design limits stated honestly: electrolyte mass excluded from calc-energy "
        "by contract (parameter set lacks density); true DFT/MD endorsement skipped (real_compute=false); "
        "4C CC-only charge accepts ~0.81 Ah before the 4.2 V ceiling (CV phase would be needed for full charge)."
    ),
    "verdict": "achieved",
}
append_entry(WS, final)
print("endorse + final appended")
