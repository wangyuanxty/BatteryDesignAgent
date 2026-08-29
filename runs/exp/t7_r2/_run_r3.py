# -*- coding: utf-8 -*-
"""Round-3 suite: 4 candidates x (1C DFN + 4C45 DFN plating + aging SPMe + calc-energy
+ nail run-tr hA=0.4248 + hot probe). Library CLI via subprocess (same cache path as manual CLI)."""
import json
import subprocess
import sys
import time
from pathlib import Path

RUN = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t7_r2")
PY = sys.executable

CANDIDATES = [
    ("r3_t1", "bridge/r3_t1.json"),
    ("r3_t2", "bridge/r3_t2.json"),
    ("r3_t3", "bridge/r3_t3.json"),
    ("r3_t4", "bridge/r3_t4.json"),
]


def run(args):
    cmd = [PY, "-m", "bda"] + args
    t0 = time.time()
    r = subprocess.run(cmd, cwd=str(RUN), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    dt = time.time() - t0
    status = "OK" if r.returncode == 0 else f"FAIL(rc={r.returncode})"
    print(f"[{dt:7.1f}s] bda {args[0]:14s} {status}", flush=True)
    if r.stdout.strip():
        print("   stdout:", r.stdout.strip()[:300], flush=True)
    if r.returncode != 0:
        print("   stderr:", r.stderr.strip()[:1200], flush=True)
        raise SystemExit(1)


summary = {}
for name, params_rel in CANDIDATES:
    params_abs = str((RUN / params_rel).resolve())
    onec = str((RUN / "cell" / f"{name}_1c.json").resolve())
    fourc = str((RUN / "cell" / f"{name}_4c45.json").resolve())
    aging = str((RUN / "cell" / f"{name}_aging45.json").resolve())
    energ = str((RUN / "cell" / f"{name}_energy.json").resolve())
    nail = str((RUN / "validation" / f"{name}_nail.json").resolve())
    nailhot = str((RUN / "validation" / f"{name}_nail_hot.json").resolve())

    print(f"\n=== {name} ===", flush=True)
    run(["run-pyamm", "--params", params_abs, "--protocol", "1C_discharge",
         "--base", "Chen2020", "--mode", "dfn", "--out", onec])
    run(["run-pyamm", "--params", params_abs, "--protocol", "4C_charge_45C",
         "--base", "Chen2020", "--mode", "dfn", "--thermal", "lumped", "--plating",
         "--out", fourc])
    run(["run-pyamm", "--params", params_abs, "--protocol", "aging_1C_100cyc_45C",
         "--base", "Chen2020", "--mode", "spme", "--cycles", "100", "--out", aging])
    run(["calc-energy", "--params", params_abs, "--sim", onec,
         "--base", "Chen2020", "--out", energ])

    edata = json.loads(Path(energ).read_text(encoding="utf-8-sig"))
    mass = float(edata["mass_kg"])
    run(["run-tr", "--mass-kg", f"{mass:.12g}", "--q-nail", "10", "--hA", "0.4248",
         "--out", nail])
    run(["run-tr", "--mass-kg", f"{mass:.12g}", "--q-nail", "10", "--hA", "0.4248",
         "--t-init", "318.15", "--out", nailhot])

    f4 = json.loads(Path(fourc).read_text(encoding="utf-8-sig"))
    a = json.loads(Path(aging).read_text(encoding="utf-8-sig"))
    n = json.loads(Path(nail).read_text(encoding="utf-8-sig"))
    nh = json.loads(Path(nailhot).read_text(encoding="utf-8-sig"))
    rec = {
        "mass_kg": mass,
        "energy_density_wh_kg": edata.get("energy_density_wh_kg"),
        "anode_min_v": round(min(f4["anode_potential_v"]), 6),
        "T_max_4C_K": f4["T_max_K"],
        "cap_4C_ah": f4["capacity_ah"],
        "sei_nm": a["sei_thickness_nm_end"],
        "nail_trig": n["triggered"], "nail_Tmax": n["T_max_K"],
        "nailhot_trig": nh["triggered"], "nailhot_Tmax": nh["T_max_K"],
        "nailhot_ttrig": nh["trigger_time_s"],
    }
    summary[name] = rec
    print("   SUMMARY:", json.dumps(rec, ensure_ascii=False), flush=True)

print("\nALL_DONE")
print(json.dumps(summary, ensure_ascii=False, indent=2))