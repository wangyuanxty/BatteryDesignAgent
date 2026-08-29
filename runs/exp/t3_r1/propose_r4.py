from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")

entry = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 20.0},
         "name": "V12_BalancedCooling",
         "role": "V6 combo + h 20 W/m2/K (between V8 h=15 and V11 h=30; Q_nom 3.08 fixed point). "
                 "Round-3 attribution: cooling h trades T_max margin against plating margin "
                 "(V8 h=15: T 331.96 K / anode +14.9 mV; V11 h=30: T 326.86 K / anode +8.2 mV; "
                 "warmer cell kinetically suppresses plating). V12 targets balanced margins "
                 "(est. T ~329.5 K, anode ~+11 mV) with cooling realistic for a power tool "
                 "(natural convection + tool-body conduction with light airflow)."},
    ],
    "llm_reason": (
        "Round 3 gave two passing designs, each with one thin margin: V8 (h=15) sits 1.19 K under the "
        "60 C red line; V11 (h=30) holds only +8.2 mV plating margin and assumes aggressive cooling. "
        "V9 shows moderate electrolyte transport erases the plating margin (+0.6 mV) and V10 shows the "
        "porosity boost is load-bearing (plated at -4.3 mV), so both levers stay at V6 values. "
        "A single balanced candidate at h=20 should land both margins in comfortable territory; "
        "if it passes, it is the final design."
    ),
}

append_entry(WS, entry)
print("propose round 4 appended")
