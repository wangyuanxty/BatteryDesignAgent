import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t1_oa", "runs/portability")

entries = []

# Funnel log: start_stage=3, materials baseline + ceiling assessment conclusion
entries.append({
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "start_stage=3 (task names no explicit material/additive). Materials use system baseline (no molecular funnel). "
        "Base determination: task 'next-gen pure electric sedan' names no electrode system -> deterministic default Chen2020 (NMC811/graphite); "
        "ceiling assessment (R1 baseline): Chen2020 ED 400.29 Wh/kg and OKane2022 ED 405.68 Wh/kg already >= 392.61 -> ED is NOT the binding constraint; "
        "binding constraints are safety (4C plating, T_max). Graphite anode (Chen2020) plates fundamentally at 4C (anode -0.438 V, transport override barely moves it), "
        "while SiOx anode (OKane2022) does not plate at high T (anode +0.009 V) but overheats (T_max 368 K). "
        "-> system switched to OKane2022 (NMC811/graphite+SiOx, distinct negative OCP vs graphite) as the material-level lever for no-plating; "
        "overcharge-to-4.7V maps to NMC811 4.2V cutoff +0.5V. Sources: baseline parameter sets."
    ),
})

# Plan update: pivot from Chen2020 to OKane2022
entries.append({
    "action": "plan",
    "update": True,
    "reason": (
        "R1 finding: Chen2020 graphite plating at 4C is fundamental (anode -0.438 V; electrolyte conductivity 2.0-2.5 S/m + t+ 0.5-0.6 + particle 3->2 um only moved anode to -0.42..-0.43 V, still plating). "
        "OKane2022 SiOx anode does not plate (anode +0.009 V) but overheats at default cooling (T_max 368 K). "
        "Direction change: pivot base to OKane2022 and attack T_max via liquid cooling (h 10->80-200) + electrolyte transport to restore no-plating margin at the lower operating temperature."
    ),
    "candidate_strategy": (
        "OKane2022 base; raise cooling h to ~80-100 W/m2/K (liquid cooling) to cap T_max<=333 K; compensate the cooler-temperature plating tendency with "
        "high-conductivity electrolyte (sigma 2.5-3.0 S/m), high transference number (t+ 0.6), high diffusivity (D 3-4e-10 m2/s), and nanostructured anode (particle 0.8-2 um)."
    ),
    "budget_allocation": "safety fine-tune 3-5 rounds on OKane2022 (already spent: baseline+ceiling 1, Chen2020 transport 1).",
})

# Propose round 2: OKane2022 cooling
entries.append({
    "action": "propose",
    "round": 2,
    "candidates": [
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 50.0}, "name": "T1-cooling-50", "role": "OKane2022 + moderate liquid cooling h=50 to cap T_max"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 100.0}, "name": "T2-cooling-100", "role": "OKane2022 + strong liquid cooling h=100"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 200.0, "Electrolyte conductivity [S.m-1]": 2.0, "Cation transference number": 0.5}, "name": "T3-cooling-200-transport", "role": "OKane2022 + h=200 + transport boost (sigma 2.0, t+ 0.5)"},
    ],
    "llm_reason": "OKane2022 baseline: no plating (anode +0.009 V) but T_max 368 K (35 K over). Liquid cooling (thermal-management DOF) directly caps T_max; add electrolyte transport to hold no-plating margin as cooling lowers operating temperature.",
})

# Propose round 3: transport + nano particle sweet-spot sweep
entries.append({
    "action": "propose",
    "round": 3,
    "candidates": [
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 120.0, "Electrolyte conductivity [S.m-1]": 2.5, "Cation transference number": 0.6, "Electrolyte diffusivity [m2.s-1]": 3.0e-10, "Negative particle radius [m]": 3.0e-6, "Positive particle radius [m]": 3.0e-6}, "name": "T4-neg3um", "role": "h=120 + sigma2.5/t+0.6/D3e-10 + neg 3um"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 120.0, "Electrolyte conductivity [S.m-1]": 2.5, "Cation transference number": 0.6, "Electrolyte diffusivity [m2.s-1]": 3.0e-10, "Negative particle radius [m]": 2.0e-6, "Positive particle radius [m]": 3.0e-6}, "name": "T5-neg2um", "role": "T4 + smaller negative particle 2um"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 120.0, "Electrolyte conductivity [S.m-1]": 2.5, "Cation transference number": 0.6, "Electrolyte diffusivity [m2.s-1]": 3.0e-10, "Negative particle radius [m]": 3.0e-6, "Positive particle radius [m]": 3.0e-6, "Negative electrode thickness [m]": 9.0e-5}, "name": "T6-NP-boost", "role": "T4 + negative thickness 9.0e-5 (N/P boost)"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 100.0, "Electrolyte conductivity [S.m-1]": 2.5, "Cation transference number": 0.6, "Electrolyte diffusivity [m2.s-1]": 3.0e-10, "Negative particle radius [m]": 1.0e-6, "Positive particle radius [m]": 2.0e-6}, "name": "T7-neg1um", "role": "h=100 + neg 1um nanostructure"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 80.0, "Electrolyte conductivity [S.m-1]": 2.5, "Cation transference number": 0.6, "Electrolyte diffusivity [m2.s-1]": 3.0e-10, "Negative particle radius [m]": 1.0e-6, "Positive particle radius [m]": 2.0e-6}, "name": "T8-neg1um-h80", "role": "T7 with h=80 (warmer -> faster kinetics)"},
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 100.0, "Electrolyte conductivity [S.m-1]": 2.5, "Cation transference number": 0.6, "Electrolyte diffusivity [m2.s-1]": 3.0e-10, "Negative particle radius [m]": 1.0e-6, "Positive particle radius [m]": 1.0e-6}, "name": "T9-negpos1um", "role": "h=100 + neg & pos 1um"},
    ],
    "llm_reason": "T3 (h=200 + transport) got anode to -0.046 V (near pass). Smaller negative particles improve solid-diffusion-limited plating (T4 3um -0.035 -> T5 2um -0.0185); push to 1um nanostructure and tune cooling (h 80-120) to land T_max close to but under 333 K for faster kinetics.",
})

# Propose round 4: final aggressive margin + DFN verify
entries.append({
    "action": "propose",
    "round": 4,
    "candidates": [
        {"struct": {"Total heat transfer coefficient [W.m-2.K-1]": 80.0, "Electrolyte conductivity [S.m-1]": 3.0, "Cation transference number": 0.6, "Electrolyte diffusivity [m2.s-1]": 4.0e-10, "Negative particle radius [m]": 0.8e-6, "Positive particle radius [m]": 2.0e-6}, "name": "T10-final", "role": "final: h=80 + sigma3.0/t+0.6/D4e-10 + neg 0.8um nanostructured SiOx anode"},
    ],
    "llm_reason": "T7-T9 pass plating in SPMe but margin thin (anode +0.002..+0.005 V); DFN widens margin. T10 pushes conductivity 3.0 S/m, diffusivity 4e-10, neg particle 0.8um for comfortable no-plating margin; verify in DFN + compute ED + overcharge runaway.",
})

for e in entries:
    append_entry(ws, e)
print("appended", len(entries), "entries")
