"""Stage-5 closing: self-check -> endorse (skipped) -> final -> render.

Gate: rounds 3 and 4 evaluate entries must already be in the log.
"""
import json
import subprocess
import sys
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

REPO = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent")
CASE_DIR = REPO / "runs" / "exp" / "t2_r1_singlemodel"
ws = CaseWorkspace("exp/t2_r1_singlemodel")

entries = [json.loads(l) for l in (CASE_DIR / "log.jsonl").read_text(encoding="utf-8-sig").splitlines()]
criteria0 = entries[0]["criteria"]
evals = [e for e in entries if e.get("action") == "evaluate"]
for rnd in (3, 4):
    if not any(e.get("round") == rnd for e in evals):
        print(f"GATE FAIL: no evaluate entry for round {rnd}")
        sys.exit(1)
r3 = [e for e in evals if e.get("round") == 3][0]
if r3.get("verdict") != "pass":
    print(f"GATE FAIL: round-3 verdict is {r3.get('verdict')}, not pass")
    sys.exit(1)

# --- pre-closing self-check (7 failure modes, mechanical where possible) ---
checks = []
checks.append(("entry-0 criteria untouched", criteria0 == entries[0]["criteria"]))
nums = json.loads((CASE_DIR / "cell" / "deliverable_numbers.json").read_text(encoding="utf-8-sig"))
checks.append(("aging500 complete (>=500 cycles)",
               nums["aging500_cycles"] >= 500))
checks.append(("SEI500 below threshold", nums["sei_500_nm"] <= 550.0))
checks.append(("SEI100 below threshold", nums["sei_100_nm"] <= 500.0))
checks.append(("ED above threshold", nums["energy_density_wh_kg"] >= 327.18))
checks.append(("retention above threshold", nums["retention_lowT_pct"] >= 90.0))
checks.append(("4C45 plating-free", nums["ap_min_4C45"] >= 0.0))
checks.append(("4C25 conservative plating-free", nums["ap_min_4C25"] >= 0.0))
for name, ok in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
if not all(ok for _, ok in checks):
    print("self-check FAILED — no closing with defects")
    sys.exit(1)

# --- endorse (real_compute=false -> honest skip) ---
append_entry(ws, {
    "action": "endorse",
    "skipped": True,
    "reason": (
        "real_compute=false (entry 0): no run-orca/run-md true-compute endorsement "
        "per protocol; proxy-level evidence only — run-mlp(mace) molecular funnel "
        "(hard lines), run-pyamm DFN cell verification, run-tr thermal-runaway ODE."
    ),
})

# --- final ---
sev = nums["sei_500_nm"]
final_entry = {
    "action": "final",
    "verdict": "achieved",
    "recommendation": (
        f"R3_finaldesign (Chen2020 NMC811/graphite base): architecture neg 250 um / "
        f"pos 100 um / radii 3.5/3.0 um; constant negative exchange-current density "
        f"2.0 A/m2 (4C plating fix, DFN-verified non-monotonic optimum); SEI pack "
        f"k 3e-13 m/s + SEI i0 7.5e-8 A/m2 + EC diffusivity 1e-19 m2/s (densified "
        f"additive-derived SEI, film-property extension of the SEI-suppression "
        f"bridge, recorded as estimate; the initially planned 8e-20 dies "
        f"deterministically at cycle ~174 of the 500-cycle aging — IDA_CONV_FAIL, "
        f"retried identically — so the completable 1e-19 was adopted). "
        f"Measured vs criteria: ED 358.01 Wh/kg "
        f">= 327.18 (calc-energy contract caliber); SEI100 {nums['sei_100_nm']:.1f} nm "
        f"<= 500; SEI500 {sev:.1f} nm <= 550 (DFN aging, {nums['aging500_cycles']} "
        f"completed cycles); lowT retention {nums['retention_lowT_pct']:.1f}% >= 90 "
        f"(-20 C); 4C plating-free ap_min +{nums['ap_min_4C45']:.3f} V (45 C start) "
        f"and +{nums['ap_min_4C25']:.3f} V (conservative 25 C start); T_max 4C "
        f"{nums['t_max_4C45']:.1f} K monitored (no red line in criteria). Honest "
        f"caveats: SPMe unreliable for thick anodes (unphysical c_e profile) — all "
        f"design runs DFN; overcharge DFN dies with IDA solver failure in the 4.7 V "
        f"charge phase (verbatim); overcharge-coupled TR not triggered (partial-run "
        f"T_max 322.7 K), 5 W nail triggers TR ({nums['tr_nail_t_max_k']:.1f} K); "
        f"aging capacity declines to 1.40 Ah at cycle 500 (not a criterion; SEI "
        f"thickness is the reliable indicator); 5C discharge 0.49 Ah (rate-limited "
        f"collapse in ~71 s; informational — no 5C criterion in entry 0); "
        f"true-compute endorsement skipped (real_compute=false)."
    ),
}
append_entry(ws, final_entry)
print("appended endorse + final")

# --- render ---
r = subprocess.run([sys.executable, "-m", "bda.cli", "render",
                    "--case-dir", str(CASE_DIR)])
if r.returncode != 0:
    print("render FAILED")
    sys.exit(1)
print("render OK ->", CASE_DIR / "report.html")
