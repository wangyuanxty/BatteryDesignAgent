"""Write funnel (start_stage=3 statement) + Round 1 propose entries."""
import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t7_r1_noforce", "D:/research/degradation_prognostics/Battery_Design_Agent/runs")

funnel = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "start_stage=3: this case starts at Stage 3; materials use system baseline. "
        "Chosen base parameter set: Chen2020. Matching basis: task text names no electrode system -> protocol anchor-table "
        "default Chen2020 (recorded). Discriminant anchor verified by parameter dump before first run: pure-graphite negative "
        "(Negative electrode exchange-current density = graphite_LGM50_Chen2020 function; negative density 1657 kg/m3; "
        "no SiOx capacity/density keys), NMC811 positive, SEI aging model present (SEI kinetic rate constant 1e-12 m/s). "
        "props source: baseline (parameter-set values)."
    ),
}
append_entry(ws, funnel)

probe_struct = {
    "Positive current collector thickness [m]": 1.0e-05,
    "Negative current collector thickness [m]": 6.0e-06,
    "Separator thickness [m]": 1.0e-05,
    "Electrolyte conductivity [S.m-1]": 2.5,
    "Electrolyte diffusivity [m2.s-1]": 5.0e-10,
    "Cation transference number": 0.5,
}
propose = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "struct": {},
            "name": "Baseline Chen2020",
            "role": "baseline characterization: unmodified Chen2020 across all four contract protocols (1C discharge, calc-energy, 4C charge 45C, aging 45C, nail 10 W)",
        },
        {
            "struct": probe_struct,
            "name": "Ceiling Probe A",
            "role": "mass-minimized architecture (Cu 6um / Al 10um collectors, 10um separator) + high-transport electrolyte (sigma 2.5 S/m, D 5e-10 m2/s, t+ 0.5) to bound best-possible Chen2020-system ED and 4C plating margin (opening ceiling assessment)",
        },
    ],
    "llm_reason": (
        "exploration_force OFF - propose only what the ceiling decision demands. Baseline anchors all four metrics; "
        "Ceiling Probe A probes the ED ceiling: parameter dump shows Cu collector (12um, 8960 kg/m3) = ~25% of cell mass, "
        "so CC+separator minimization is the dominant mass lever of the Chen2020 architecture space; high-transport "
        "electrolyte bounds the 4C plating margin (Logan & Dahn 2020 direction). Electrolyte transport values are domain "
        "ESTIMATES (not simulation outputs): sigma 2.5 S/m, D 5e-10 m2/s, t+ 0.5. Electrode thickness/porosity kept at "
        "baseline to avoid confounding; the probe answers 'is the objective reachable without leaving the Chen2020 system'."
    ),
}
append_entry(ws, propose)
print("funnel + propose R1 appended; total entries:", len((ws.path / "log.jsonl").read_text(encoding="utf-8").strip().splitlines()))
