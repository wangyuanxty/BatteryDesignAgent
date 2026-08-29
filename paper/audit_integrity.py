"""audit_integrity.py — pipeline stage ③: mechanical data-paper audit.

Every conclusion-grade number in the manuscript tables is checked against
the experiment artifacts (audit ledgers, BO trajectories, endorsement JSONs,
calibration files, portability workspaces). Output: audit_integrity_report.txt.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")

report: list[str] = []
fails = 0
checks = 0


def is_achieved(v):
    """achieved/pass are equivalent pass verdicts in the ledgers."""
    return v in ("achieved", "pass")


def check(name: str, actual, expected, tol: float | None = None) -> None:
    global fails, checks
    checks += 1
    ok = actual == expected if tol is None else abs(actual - expected) <= tol
    status = "PASS" if ok else "FAIL"
    if not ok:
        fails += 1
    report.append(f"[{status}] {name}: actual={actual!r} expected={expected!r}")


def final_of(run_dir: Path):
    p = run_dir / "log.jsonl"
    es = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    fins = [e for e in es if e.get("action") == "final"]
    return es, (fins[-1] if fins else None)


def last_metric(run_dir: Path, key: str):
    p = run_dir / "log.jsonl"
    es = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    for e in reversed(es):
        m = e.get("metrics", {}) if e.get("action") == "evaluate" else {}
        if isinstance(m.get(key), (int, float)):
            return m[key]
    return None


EXP = ROOT / "runs" / "exp"
POR = ROOT / "runs" / "portability"

# ---- 1. main matrix: governed verdicts (8 tasks × pro/flash) ----
for t in ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"]:
    for variant, tag in [("", "pro"), ("_flash", "flash")]:
        d = EXP / f"{t}_r1{variant}"
        if not d.exists():
            check(f"{t}{tag} run dir exists", False, True)
            continue
        _, fin = final_of(d)
        v = fin.get("verdict") if fin else None
        if v is None and tag == "flash" and t == "t6":
            report.append(f"[FAIL] t6flash verdict achieved: actual=None expected='achieved' (KNOWN DEFECT — documented in paper §5.4; missing final entry became a regression test)")
            fails += 1; checks += 1
            continue
        check(f"{t}{tag} verdict achieved", v, "achieved")

# key numbers cited in Table 3 and the supplementary margins table
check("T1 pro ED 553.98", round(last_metric(EXP / "t1_r1", "energy_density_wh_kg"), 2), 553.98, tol=0.01)
check("T2 pro ED 465.62", round(last_metric(EXP / "t2_r1", "energy_density_wh_kg"), 2), 465.62, tol=0.01)
check("T4 pro ED 471.55", round(last_metric(EXP / "t4_r1", "energy_density_wh_kg"), 2), 471.55, tol=0.01)
check("T6 pro Wh/L 1135.8", round(last_metric(EXP / "t6_r1", "energy_density_wh_l"), 1), 1135.8, tol=0.1)
check("T1 flash ED 459.4", round(last_metric(EXP / "t1_r1_flash", "energy_density_wh_kg"), 1), 459.4, tol=0.1)
check("T6 pro plateau 4.1145", round(last_metric(EXP / "t6_r1", "midpoint_voltage_v"), 4), 4.1145, tol=0.0001)
check("T8 pro mass 0.0398", round(last_metric(EXP / "t8_r1", "mass_kg"), 4), 0.0398, tol=0.0001)

# ---- SEI lever disclosure (margin paragraph, supplementary) ----
_t2log = (EXP / "t2_r1" / "log.jsonl").read_text(encoding="utf-8")
check("T2 final design k_SEI 1e-16 declared", "GridStore-Final" in _t2log and "1e-16" in _t2log, True)
check("T2 x0.01 variant SEI@500 500.4 in log", "500.364" in _t2log, True)
_t7log = (EXP / "t7_r1" / "log.jsonl").read_text(encoding="utf-8")
check("T7 no SEI kinetic override", "SEI kinetic rate constant [m.s-1]" not in _t7log, True)

# ---- resource anchoring (experiments.tex §4.2) ----
import re as _re
_n_calls = 0
for _t in ("t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"):
    _rl = EXP / f"{_t}_r1" / "run.log"
    if _rl.exists():
        _lines = [_l for _l in _rl.read_text(encoding="utf-8", errors="replace").splitlines()
                  if "command=" in _l]
        _n_calls += sum(1 for _l in _lines if "run-pyamm" in _l)
check("governed run-pyamm call total 203", _n_calls, 203)

# ---- BO 3-seed robustness (experiments.tex §4.2, supplementary tab:boseeds) ----
import json as _json
_bo_seed_ach = {
    "t1": (25, 28, 21), "t2": (0, 0, 0), "t3": (0, 0, 0), "t4": (34, 33, 32),
    "t5": (0, 0, 0), "t6": (0, 0, 0), "t7": (0, 0, 0), "t8": (10, 5, 1),
}
for _t, _counts in _bo_seed_ach.items():
    _trs = []
    for _d in ({"t1": "t1_r2", "t2": "t2_r2", "t3": "t3_r1", "t4": "t4_r1",
                "t5": "t5_r1", "t6": "t6_r1", "t7": "t7_r1", "t8": "t8_r1"}[_t],
               f"{_t}_seed5678", f"{_t}_seed9012"):
        _p = ROOT / "runs" / "c2" / _d / "bo_trajectory.json"
        _trs.append(_json.loads(_p.read_text(encoding="utf-8")) if _p.exists() else [])
    if len(_trs) == 3 and all(_trs):
        for _i, _n in enumerate(_counts):
            _c = 0
            for _x in _trs[_i]:
                # mechanical attainment per task (mirror of the analysis script)
                _ed = _x.get("energy_density_wh_kg"); _edl = _x.get("energy_density_wh_l")
                _mid = _x.get("midpoint_voltage_v"); _T = _x.get("T_max_K")
                _pl = _x.get("plated"); _mass = _x.get("mass_g"); _r5 = _x.get("ret5_pct")
                _lt = _x.get("lowt_retention_pct"); _sei = _x.get("sei_thickness_nm_end")
                _ok = {
                    "t1": _ed and _ed >= 392.61 and _pl is False and _T <= 333.15,
                    "t2": _ed and _ed >= 327.18 and _pl is False and _sei and _sei <= 500 and _lt and _lt >= 90,
                    "t3": _r5 is not None and _r5 >= 95 and _pl is False,
                    "t4": _ed and _ed >= 327.18 and _edl and _edl >= 880 and _lt and _lt >= 95,
                    "t5": _ed and _ed >= 500.94 and _pl is False and _T <= 333.15,
                    "t6": _edl and _edl >= 950 and _mid and _mid >= 4.1 and _pl is False and _T <= 323.15,
                    "t7": _ed and _ed >= 327.18 and _sei and _sei <= 550 and _pl is False,
                    "t8": _ed and _ed >= 446.18 and _r5 is not None and _r5 >= 90 and _mass and _mass <= 40 and _pl is False,
                }[_t]
                _c += 1 if _ok else 0
            check(f"BO {_t} seed{_i} attaining trials", _c, _n)
    else:
        check(f"BO {_t} 3-seed artifacts exist", False, True)

# ---- 2. BO baseline (Table 3, C2 column) ----
bo_best = {
    "t1": 514.13, "t2": 617.81, "t3": 442.45, "t4": 628.26,
    "t5": 626.87, "t6": 606.97, "t7": 577.15, "t8": 643.75,
}
bo_dir = {"t1": "t1_r2", "t2": "t2_r2", "t3": "t3_r1", "t4": "t4_r1",
          "t5": "t5_r1", "t6": "t6_r1", "t7": "t7_r1", "t8": "t8_r1"}
for t, expected in bo_best.items():
    p = ROOT / "runs" / "c2" / bo_dir[t] / "bo_trajectory.json"
    if not p.exists():
        check(f"BO {t} trajectory exists", False, True)
        continue
    traj = json.loads(p.read_text(encoding="utf-8"))
    best = max(x["objective"] for x in traj)
    check(f"BO {t} best objective", round(best, 2), expected, tol=0.01)

# ---- 2b. BO T6 aligned penalizer (50 C red line; results.tex §5.1 claim) ----
_p = ROOT / "runs" / "c2" / "t6_r1_aligned" / "bo_trajectory.json"
if _p.exists():
    _traj = json.loads(_p.read_text(encoding="utf-8"))
    check("BO t6 aligned trials", len(_traj), 50)
    _best = max(_traj, key=lambda x: x["objective"])
    check("BO t6 aligned best objective", round(_best["objective"], 2), 594.64, tol=0.01)
    _contract = [x for x in _traj
                 if x["energy_density_wh_l"] >= 950 and x["midpoint_voltage_v"] >= 4.1
                 and not x["plated"] and x["T_max_K"] <= 323.15]
    check("BO t6 aligned contract attained", len(_contract), 0)
    check("BO t6 aligned Wh/L-only clears", sum(1 for x in _traj if x["energy_density_wh_l"] >= 950), 30)
    check("BO t6 aligned safe trials", sum(1 for x in _traj if not x["plated"] and x["T_max_K"] <= 323.15), 0)
    check("BO t6 aligned plateau (best design)", round(_best["midpoint_voltage_v"], 4), 4.0065, tol=0.0001)
    _orig = json.loads((ROOT / "runs" / "c2" / "t6_r1" / "bo_trajectory.json").read_text(encoding="utf-8"))
    _c0 = [x for x in _orig
           if x["energy_density_wh_l"] >= 950 and x["midpoint_voltage_v"] >= 4.1
           and not x["plated"] and x["T_max_K"] <= 323.15]
    check("BO t6 original contract attained", len(_c0), 0)
    _b0 = max(_orig, key=lambda x: x["objective"])
    check("BO t6 original plateau (best design)", round(_b0["midpoint_voltage_v"], 4), 4.0065, tol=0.0001)

# ---- 3. ablation (Table 5) ----
abl = {
    "t2_r1_noceiling": "not achieved", "t5_r1_noceiling": "achieved", "t6_r1_noceiling": "not achieved",
    "t1_r1_noforce": "achieved", "t2_r1_noforce": "not achieved", "t3_r1_noforce": "achieved",
    "t4_r1_noforce": "achieved", "t7_r1_noforce": "achieved", "t8_r1_noforce": "achieved",
    "t2_r1_singlemodel": "achieved", "t5_r1_singlemodel": "achieved", "t6_r1_singlemodel": "achieved",
}
for run, expected in abl.items():
    _, fin = final_of(EXP / run)
    v = fin.get("verdict") if fin else None
    check(f"ablation {run} verdict", is_achieved(v) if v else v, is_achieved(expected))

# ---- seed replication (supplementary tab:replication; all 8 tasks × 3) ----
_seed_runs = {f"{t}_{r}" for t in ("t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8")
              for r in ("r2", "r3")}
for _w in sorted(_seed_runs):
    _, _fin = final_of(EXP / _w)
    _v = _fin.get("verdict") if _fin else None
    check(f"seed {_w} verdict", is_achieved(_v) if _v is not None else _v, True)

# ---- 3b. luna third-vendor leg (Table tab:main G-luna column) ----
_luna_expected = {"t1": "not achieved", "t2": "achieved", "t3": "achieved", "t4": "achieved",
                  "t5": "not achieved", "t6": "not achieved", "t7": "achieved", "t8": "not achieved"}
for _t, _expected in _luna_expected.items():
    _, _fin = final_of(EXP / f"{_t}_r1_luna")
    _v = _fin.get("verdict") if _fin else None
    check(f"luna {_t} verdict", is_achieved(_v) if _v is not None else _v, is_achieved(_expected))

# ---- 4. C1 re-adjudication numbers (Table 6; contract model, full declared design) ----
_repro = ROOT / "runs" / "c1_repro"
for _f, _label, _key, _expected, _tol in [
    ("o_d_full_nodiff.json", "C1-T2 SEI@100 full design 487.9", "sei_thickness_nm_end", 487.9, 0.1),
    ("o_full_500cyc.json", "C1-T2 SEI@500 full design 818.9", "sei_thickness_nm_end", 818.9, 0.1),
]:
    _p = _repro / _f
    if _p.exists():
        _d = json.loads(_p.read_text(encoding="utf-8"))
        check(_label, round(_d.get(_key, -1), 1), _expected, tol=_tol)
    else:
        check(f"{_label} artifact exists", False, True)
_p = _repro / "o_full_4c.json"
if _p.exists():
    _d = json.loads(_p.read_text(encoding="utf-8"))
    check("C1-T2 4C min potential -360.9 mV", round(min(_d["anode_potential_v"]) * 1000, 1), -360.9, tol=0.5)
else:
    check("C1-T2 4C re-run artifact exists", False, True)
_p1, _p5 = _repro / "o_t3_full_1c.json", _repro / "o_t3_full_5c.json"
if _p1.exists() and _p5.exists():
    _c1 = json.loads(_p1.read_text(encoding="utf-8"))["capacity_ah"]
    _c5 = json.loads(_p5.read_text(encoding="utf-8"))["capacity_ah"]
    check("C1-T3 full-design 5C/1C 94.1", round(_c5 / _c1 * 100, 1), 94.1, tol=0.1)
else:
    check("C1-T3 full-design re-run artifacts exist", False, True)
p1, p5 = ROOT / "runs" / "c1_t3_1c.json", ROOT / "runs" / "c1_t3_5c.json"
if p1.exists() and p5.exists():
    c1 = json.loads(p1.read_text(encoding="utf-8"))["capacity_ah"]
    c5 = json.loads(p5.read_text(encoding="utf-8"))["capacity_ah"]
    check("C1-T3 standard-diffusivity 5C/1C 84.8", round(c5 / c1 * 100, 1), 84.8, tol=0.1)
else:
    check("C1-T3 re-run artifacts exist", False, True)

# ---- 5. endorsement (Table 7): HOMO values from ORCA output ----
p = EXP / "t5_r1_flash" / "df_endorse_out.json"
if p.exists():
    d = json.loads(p.read_text(encoding="utf-8"))
    expected_homo = {"C1OC(=O)OC1F": -7.458, "C1=COC(=O)O1": -6.470,
                     "C1CCS(=O)(=O)O1": -7.151, "C1COS(=O)(=O)O1": -7.601}
    for c in d["candidates"]:
        exp = expected_homo.get(c["smiles"])
        if exp is not None:
            check(f"endorse HOMO {c['smiles'][:10]}", round(c["endorsement"]["homo_ev"], 3), exp, tol=0.002)
else:
    check("ORCA endorsement artifact exists", False, True)

# ---- 5b. CP2K cross-validation (Table 7, fourth column) ----
p = EXP / "t5_r1_flash" / "df_endorse_cp2k_out.json"
if p.exists():
    d = json.loads(p.read_text(encoding="utf-8"))
    expected_homo = {"C1OC(=O)OC1F": -7.461, "C1=COC(=O)O1": -6.319,
                     "C1CCS(=O)(=O)O1": -6.689, "C1COS(=O)(=O)O1": -7.230}
    for c in d["candidates"]:
        exp = expected_homo.get(c["smiles"])
        if exp is not None:
            check(f"CP2K HOMO {c['smiles'][:10]}", round(c["endorsement"]["homo_ev"], 3), exp, tol=0.002)
else:
    check("CP2K endorsement artifact exists", False, True)

# ---- 6. real-data anchor: capacity +0.45%, RMSE 20.6 mV ----
p = ROOT / "calibration" / "lgm50t" / "alignment_result.json"
if p.exists():
    d = json.loads(p.read_text(encoding="utf-8"))
    check("LG M50T capacity diff +0.45%", d.get("cap_diff_pct"), 0.45, tol=0.02)
    check("LG M50T RMSE 20.6 mV", d.get("rmse_mv"), 20.6, tol=0.2)
else:
    check("alignment artifact exists", False, True)

# ---- 7. portability (Table 13): six legs achieved ----
for leg in ["t1_oa", "t6_oa", "t1_lc", "t6_lc"]:
    _, fin = final_of(POR / leg)
    check(f"portability {leg} verdict", fin.get("verdict") if fin else None, "achieved")

# ---- 8. replication: 4 new seeds achieved ----
for run in ["t1_r2", "t1_r3", "t6_r2", "t6_r3"]:
    _, fin = final_of(EXP / run)
    check(f"replication {run} verdict", fin.get("verdict") if fin else None, "achieved")

# ---- 9. citation keys: bib entries vs \cite keys ----
tex = ""
for f in ["main.tex"] + [f"sections/{s}.tex" for s in
                         ["introduction", "literature", "framework", "experiments",
                          "results", "discussion", "conclusion"]]:
    tex += (ROOT / "paper" / f).read_text(encoding="utf-8")
cited = set()
for m in re.findall(r"cite(?:\[[^\]]*\])?\{([^}]+)\}", tex):
    cited.update(k.strip() for k in m.split(","))
bib = (ROOT / "paper" / "paper.bib").read_text(encoding="utf-8")
bkeys = set(re.findall(r"@\w+\{([^,]+),", bib))
check("citation keys all resolve", sorted(cited - bkeys), [])

# ---- write report ----
report.insert(0, f"=== Pipeline Stage 3: Integrity Audit ===\nchecks={checks} fails={fails}\n")
out = ROOT / "paper" / "audit_integrity_report.txt"
out.write_text("\n".join(report), encoding="utf-8")
print(f"integrity audit: {checks} checks, {fails} failures -> {out}")
for line in report:
    if line.startswith("[FAIL"):
        print(line)
