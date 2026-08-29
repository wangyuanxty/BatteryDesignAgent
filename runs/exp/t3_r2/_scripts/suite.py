"""Candidate suite driver (in-process bda library, same code path as the CLI).

For a candidate params file (without 'Nominal cell capacity [A.h]'):
1. Nominal loop: 1C DFN with nominal=5.0 -> cap c1; nominal := c1 -> 1C DFN -> c2;
   repeat while drift > 2%; final nominal = last realized capacity.
2. Suite on final nominal: 1C dfn (recorded), 5C dfn, 4C_charge_45C dfn (lumped+plating),
   calc-energy, derived metrics file.
3. Writes final params file (with nominal) for traceability.

Usage: python suite.py <label> <params.json> <outdir>
"""
import json
import sys
from pathlib import Path

from bda.energy import calc_energy
from bda.simulators.pybamm_runner import run_simulation

label, params_path, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
outdir = Path(outdir)
params = json.loads(Path(params_path).read_text(encoding="utf-8-sig"))

def run(protocol, nominal, mode, plating=False):
    p = dict(params)
    p["Nominal cell capacity [A.h]"] = nominal
    return run_simulation(p, protocol, base="Chen2020", mode=mode,
                          thermal="lumped", plating=plating)

# --- nominal consistency loop (audited plan-update rule) ---
nominal = 5.0
prev_cap = None
for it in range(4):
    d = run("1C_discharge", nominal, "dfn")
    cap = d["capacity_ah"]
    log2 = []
    if prev_cap is not None:
        drift = abs(cap - prev_cap) / prev_cap
        log2.append(f"it{it} cap={cap:.4f} drift={drift:.4f}")
        if drift <= 0.02:
            break
    prev_cap, nominal = cap, cap
else:
    print(f"[{label}] nominal loop max iterations reached; last cap={prev_cap:.4f}")
loop_note = "; ".join(log2) if log2 else f"nominal loop first cap={prev_cap:.4f}"

final_params = dict(params)
final_params["Nominal cell capacity [A.h]"] = nominal
(outdir / f"{label}_params_final.json").write_text(
    json.dumps(final_params, ensure_ascii=False, indent=2), encoding="utf-8")

p = lambda name: str(outdir / f"{label}_{name}.json")
d1 = run("1C_discharge", nominal, "dfn")
Path(p("1c_dfn")).write_text(json.dumps(d1), encoding="utf-8")
d5 = run("5C_discharge", nominal, "dfn")
Path(p("5c_dfn")).write_text(json.dumps(d5), encoding="utf-8")
d4 = run("4C_charge_45C", nominal, "dfn", plating=True)
Path(p("4c_dfn")).write_text(json.dumps(d4), encoding="utf-8")

energy = calc_energy(str(outdir / f"{label}_params_final.json"), p("1c_dfn"), "Chen2020")
Path(p("energy")).write_text(json.dumps(energy, ensure_ascii=False, indent=2), encoding="utf-8")

ret = round(d5["capacity_ah"] / d1["capacity_ah"], 4)
derived = {
    "capacity_retention_5c": ret,
    "t_max_5c_k": round(float(d5["T_max_K"]), 4),
    "derivation": (
        f"capacity_retention_5c = 5C capacity {d5['capacity_ah']:.4f} Ah / 1C capacity "
        f"{d1['capacity_ah']:.4f} Ah (same params incl. nominal={nominal:.4f} Ah); "
        f"t_max_5c_k = T_max_K of the 5C run. {loop_note}"
    ),
}
Path(p("derived")).write_text(json.dumps(derived, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps({
    "label": label,
    "nominal_final_ah": round(nominal, 4),
    "cap_1c_ah": round(d1["capacity_ah"], 4),
    "cap_5c_ah": round(d5["capacity_ah"], 4),
    "retention_5c": ret,
    "t_1c_k": round(float(d1["T_max_K"]), 4),
    "t_5c_k": round(float(d5["T_max_K"]), 4),
    "t_4c_k": round(float(d4["T_max_K"]), 4),
    "anode_min_v": round(min(d4["anode_potential_v"]), 5),
    "dcr_ohm": round(energy["dcr_ohm"], 6),
    "power_density_w_kg": round(energy["power_density_w_kg"], 1),
    "mass_kg": round(energy["mass_kg"], 4),
    "model_used": d4["model_used"],
}, ensure_ascii=False))