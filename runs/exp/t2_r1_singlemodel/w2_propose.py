"""Round-2 propose entry: additive-bridge pack + architecture variants."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t2_r1_singlemodel", root="runs/exp")

entry = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {"name": "V1_SEI_pack",
         "role": "film-forming additive bridge (FEC+PS+LiDFOB): SEI kinetic rate "
         "constant 1e-12->3e-13 m/s (x0.3) and SEI reaction exchange current "
         "density 1.5e-7->7.5e-8 A/m2 (x0.5) - targets SEI<=500nm@100cyc and "
         "<=550nm@500cyc",
         "struct": {"SEI kinetic rate constant [m.s-1]": 3e-13,
                    "SEI reaction exchange current density [A.m-2]": 7.5e-8}},
        {"name": "V2_kinetics",
         "role": "interfacial kinetics bridge (LiDFOB/LiDFP additive pack): "
         "negative electrode exchange-current density set to constant 2.0 A/m2 "
         "(baseline function gives ~0.1-0.8 A/m2 over the charge range at 45C; "
         "x4-20 estimate, literature Rct reduction 50-90% for borate/phosphate "
         "additive electrolytes) - lowers anode activation overpotential at 4C",
         "struct": {"Negative electrode exchange-current density [A.m-2]": 2.0}},
        {"name": "V3_thick_4C",
         "role": "architecture for 4C plating: positive thickness 75.6->100 um "
         "and negative thickness 85.2->150 um (areal flux density down ~33-43%, "
         "N/P 0.67->1.09), particle radii reduced (positive 5.22->3.0 um, "
         "negative 5.86->3.5 um) to shorten diffusion response time; raises "
         "capacity headroom and ED",
         "struct": {"Positive electrode thickness [m]": 1.0e-4,
                    "Negative electrode thickness [m]": 1.5e-4,
                    "Positive particle radius [m]": 3.0e-6,
                    "Negative particle radius [m]": 3.5e-6}},
        {"name": "V4_combined",
         "role": "reserve: V1+V2+V3 combined full design (evaluated round 3)",
         "struct": {"SEI kinetic rate constant [m.s-1]": 3e-13,
                    "SEI reaction exchange current density [A.m-2]": 7.5e-8,
                    "Negative electrode exchange-current density [A.m-2]": 2.0,
                    "Positive electrode thickness [m]": 1.0e-4,
                    "Negative electrode thickness [m]": 1.5e-4,
                    "Positive particle radius [m]": 3.0e-6,
                    "Negative particle radius [m]": 3.5e-6}},
    ],
    "llm_reason": "Round-1 baseline: ED 400.3 Wh/kg PASS, SEI100 449 nm PASS, "
    "SEI500 778 nm FAIL (need ~x0.5 kinetics; bridge x0.3 for margin, "
    "L~sqrt(k)), lowT retention 99.4% PASS (cold-start rerun with Initial "
    "temperature 253.15 K - note: protocol only sets ambient, cell must start "
    "at test temperature; same correction for 45C 4C runs, 318.15 K), 4C "
    "charge FAIL: anode surface potential -0.44 V (plating) and charge "
    "terminates at 26 s/0.029 Ah. Mechanism check: eta_act~0.1 V (i0~0.8 A/m2 "
    "at 45C mid-SOC) - plating is surface-concentration-driven (slow solid "
    "diffusion D_s,neg=3.3e-14, D_s,pos=4e-15 excluded as levers), so reduce "
    "per-particle flux via thicker electrodes + smaller particles and cut "
    "activation overpotential via the kinetics bridge. Ceiling assessment "
    "(Stage-3 opening, baseline): ED ceiling of the Chen2020 architecture "
    "space is well above 327.18 (baseline 400.3 already passes) -> no "
    "material escalation needed for ED; binding constraints are SEI500 and 4C "
    "plating, both addressable via additive bridge + architecture. "
    "Test-condition note: lowT/4C45 runs set Initial temperature to the "
    "protocol ambient (253.15/318.15 K) so the cell is at the named test "
    "temperature - recorded for audit; the 4C criterion will also be re-"
    "checked at the default 298.15 K start as a conservative cross-check.",
}

append_entry(ws, entry)
print("propose R2 written")
