# -*- coding: utf-8 -*-
"""从三份 specsheet 抽取 66 条任务，落成机器可读 JSON。

原则：能可靠抽的抽，抽不准的留 null 并记进 parse_failed——不硬猜。
另分 spec_gaps：那是规格书本来就没给，不是解析失败。
"""
import io, sys, re, json, collections
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = Path("D:/Temp/specsheets")
OUT = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\benchmark")
OUT.mkdir(exist_ok=True)


def clean(x):
    return re.sub(r"\s+", " ", x.strip())


def strip_md(x):
    return x.replace("**", "").strip()


def rows(fn, idx, cap_from2=False):
    out = []
    for l in open(BASE / fn, encoding="utf-8"):
        if not l.startswith("|") or "---" in l:
            continue
        c = [clean(x) for x in l.strip("|").split("|")]
        if len(c) < 10 or c[0].startswith("Model"):
            continue
        if not (c[0].startswith("**") or c[0][:1].isupper()):
            continue
        g = lambda k: c[idx[k]] if idx.get(k) is not None and idx[k] < len(c) else ""
        out.append({
            "model": strip_md(c[0]),
            "form": g("form"), "chem": g("chem"),
            "cap": f"{c[1]} · {c[2]}" if cap_from2 else g("cap"),
            "whkg": strip_md(g("whkg")), "whl": strip_md(g("whl")),
            "dis": strip_md(g("dis")), "cyc": strip_md(g("cyc")),
            "cite": g("cite"),
            "src_file": f"calibration/specsheets/{fn}",
        })
    return out


RECS = (rows("21700.md", {"cap": 1, "whkg": 5, "whl": 6, "dis": 7, "cyc": 8, "cite": 9}, True)
        + rows("pouch-prismatic.md", {"form": 1, "chem": 2, "cap": 3, "whkg": 4, "whl": 5,
                                      "dis": 6, "cyc": 7, "cite": 9})
        + rows("18650.md", {"chem": 1, "cap": 2, "whkg": 3, "whl": 4, "dis": 5, "cyc": 6, "cite": 9}))

PH = r"(?:[A-Za-z][A-Za-z/().-]*\s+)*"          # 数字与单位之间的词
GAP = re.compile(r"not stated|not given|No cycle|Under Construction|deliberately incomplete|not read", re.I)


def f1(s):
    m = re.search(r"([\d,]+(?:\.\d+)?)", s)
    return float(m.group(1).replace(",", "")) if m else None


def parse(r):
    lost, gap = [], []
    # 容量：数字 + 若干词 + mAh/Ah
    cap_ah = None
    m = re.search(r"([\d.,]+)\s*" + PH + r"(m?Ah)\b", r["cap"])
    if m:
        cap_ah = float(m.group(1).replace(",", ""))
        if m.group(2) == "mAh":
            cap_ah /= 1000.0
    else:
        lost.append("capacity")
    whkg = f1(r["whkg"])
    if whkg is None:
        lost.append("wh_kg")
    # 来源：厂商给的还是我们算的
    if re.search(r"\*|computed", r["whkg"], re.I):
        whkg_basis = "derived"
    elif re.search(r"\(v[\s,)]|\(vendor|vendor", r["whkg"], re.I):
        whkg_basis = "vendor_stated"
    else:
        whkg_basis = None
    whl = f1(r["whl"])
    # 循环寿命
    cyc = eol = None
    if GAP.search(r["cyc"]):
        gap.append("cycle_life")
    else:
        m = re.search(r"([\d,]+)\s*" + PH + r"cyc", r["cyc"])
        if m:
            cyc = f1(m.group(1))
        else:
            lost.append("cycles")
        m2 = re.search(r"(\d+)\s*%", r["cyc"])
        if m2:
            eol = int(m2.group(1)) / 100.0
        else:
            gap.append("eol_criterion")
    # 循环寿命是厂商写的数，还是从图上读的
    if re.search(r"my reading|reading of the plotted|read off", r["cyc"], re.I):
        cyc_basis = "read_off_chart"
    elif cyc or gap:
        cyc_basis = "vendor_stated" if cyc else None
    else:
        cyc_basis = None
    c_rate = None
    m = re.search(r"([\d.]+)\s*C\b", r["dis"])
    if m:
        c_rate = float(m.group(1))
    amps = None
    m = re.search(r"([\d,]+)\s*A\b", r["dis"])
    if m:
        amps = f1(m.group(1))
    if c_rate is None and amps is None:
        gap.append("max_discharge")
    return ({"capacity_ah": cap_ah, "wh_kg": whkg, "wh_kg_basis": whkg_basis, "wh_l": whl,
             "cycles": int(cyc) if cyc else None, "cycles_basis": cyc_basis, "eol_frac": eol,
             "max_discharge_C": c_rate, "max_discharge_A": amps}, lost, gap)


def cls_of(r):
    s = r["chem"] + r["cap"]
    if any(w in s for w in ("LFP", "LTO", "LiFePO4", "lithium iron", "铁锂")):
        return "lfp_lto"
    if "pouch" in r["form"].lower() or "prismatic" in r["form"].lower():
        return "pouch_prismatic"
    return "cylindrical"


TPL = {
    "cylindrical": {"scenario": "High-energy cylindrical (automotive / general)",
                    "objectives": [{"metric": "energy_density_wh_kg", "direction": "max"},
                                   {"metric": "rate_retention_5C_1C", "direction": "max"}]},
    "pouch_prismatic": {"scenario": "Pouch or prismatic (consumer / automotive)",
                        "objectives": [{"metric": "energy_density_wh_l", "direction": "max"},
                                       {"metric": "energy_density_wh_kg", "direction": "max"}]},
    "lfp_lto": {"scenario": "Long-life and low-cost (stationary storage / second life)",
                "objectives": [{"metric": "cycle_life", "direction": "max"},
                               {"metric": "material_cost", "direction": "min"}]},
}
MODEL_CONS = {
    "cylindrical": [{"metric": "no_lithium_plating", "op": "==", "value": True, "basis": "model"},
                    {"metric": "T_max_C", "op": "<=", "value": 60, "basis": "model"}],
    "pouch_prismatic": [{"metric": "no_lithium_plating", "op": "==", "value": True, "basis": "model"},
                        {"metric": "T_max_C", "op": "<=", "value": 50, "basis": "model"}],
    "lfp_lto": [{"metric": "no_lithium_plating", "op": "==", "value": True, "basis": "model"},
                {"metric": "T_max_C", "op": "<=", "value": 60, "basis": "model"},
                {"metric": "nail_penetration_no_fire", "op": "==", "value": True, "basis": "model"},
                {"metric": "overcharge_no_fire", "op": "==", "value": True, "basis": "model"},
                {"metric": "thermal_runaway_no_fire", "op": "==", "value": True, "basis": "model"}],
}
ABBR = {"cylindrical": "cyl", "pouch_prismatic": "pouch", "lfp_lto": "lfp"}

tasks, review, counter = [], [], {}
for r in RECS:
    k = cls_of(r)
    counter[k] = counter.get(k, 0) + 1
    vals, lost, gap = parse(r)
    tid = f"T-{ABBR[k]}-{counter[k]:02d}"
    cons = []
    if k == "lfp_lto":
        if vals["capacity_ah"]:
            cons.append({"metric": "capacity_ah", "op": ">=", "value": vals["capacity_ah"], "basis": "control_spec"})
        if vals["wh_kg"]:
            cons.append({"metric": "energy_density_wh_kg", "op": ">=", "value": vals["wh_kg"], "basis": "control_spec"})
    else:
        if vals["capacity_ah"]:
            cons.append({"metric": "capacity_ah", "op": ">=", "value": vals["capacity_ah"], "basis": "control_spec"})
        if vals["cycles"] and vals["eol_frac"]:
            cons.append({"metric": "cycle_life_at_eol", "op": ">=", "value": vals["cycles"],
                         "eol_frac": vals["eol_frac"], "basis": "control_spec"})
        if vals["max_discharge_C"]:
            cons.append({"metric": "max_discharge_C", "op": ">=", "value": vals["max_discharge_C"],
                         "basis": "control_spec"})
    cons += MODEL_CONS[k]
    tasks.append({
        "id": tid, "class": k, "scenario": TPL[k]["scenario"],
        "control": {"model": r["model"], "chemistry_as_stated": r["chem"] or None,
                    "spec_reference": r["cite"], "source": r["src_file"], "spec_values": vals},
        "objectives": TPL[k]["objectives"], "constraints": cons,
        "eval": {"lead_margin": 0.10, "budget_sim_calls": None},
        "parse_failed": lost, "spec_gaps": gap,
    })
    if lost or gap:
        review.append((tid, r["model"], lost, gap))

doc = {
    "name": "battery-cell-design-benchmark", "version": "0.1.0", "date": "2026-09-27",
    "description": "66 cell-design tasks. Each takes one real commercial cell as its control; a method "
                   "must beat it on the objectives while staying inside the flagged constraints.",
    "lead_margin": 0.10,
    "lead_margin_reason": "The simulator's electrode-stack mass runs ~8.6% below the datasheet-implied "
                          "value, inflating computed energy density by ~9.5%. Below 10% a win cannot be "
                          "told apart from that bias.",
    "notes": [
        "constraints with basis=control_spec take their threshold from that cell's own spec sheet",
        "constraints with basis=model have no control value and must simply be satisfied",
        "capacity and energy density are on the whole-cell caliber (stack + electrolyte + packaging)",
        "parse_failed = we could not extract it though the spec states it; spec_gaps = the spec does not state it",
        "budget_sim_calls is not set yet",
        "wh_kg_basis: vendor_stated vs derived (derived = computed from vendor mass and energy)",
        "cycles_basis: vendor_stated vs read_off_chart (read off a plotted curve by us, not a vendor number)",
    ],
    "n_tasks": len(tasks), "tasks": tasks,
}
(OUT / "tasks.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"写出 {len(tasks)} 条 -> benchmark/tasks.json")
print("分类:", dict(collections.Counter(t["class"] for t in tasks)))
n_lost = sum(1 for _, _, l, _ in review if l)
n_gap = sum(1 for _, _, _, g in review if g)
print(f"\n解析失败 {n_lost} 条；规格书缺项 {n_gap} 条（可重叠）")
for tid, m, l, g in review:
    print(f"  {tid:12s} {m[:30]:30s} 解析失败={l}  规格书缺={g}")
