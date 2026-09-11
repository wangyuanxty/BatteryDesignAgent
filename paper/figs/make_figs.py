"""make_figs.py — generate all matplotlib figures for the paper (paper/figs/*.pdf).

Run from repo root:  D:/anaconda/envs/py312/python.exe paper/figs/make_figs.py
Every number is read from experiment artifacts (runs/, calibration/); the few
constants hardcoded here are copied from the audit records in docs/experiment-design.md.
"""
import json
import glob
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding="utf-8")

# ---------- unified style ----------
plt.rcParams.update({
    "figure.dpi": 120, "font.size": 9, "axes.titlesize": 10,
    "axes.labelsize": 9.5, "legend.fontsize": 8, "xtick.labelsize": 8,
    "ytick.labelsize": 8, "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})
GREEN = "#1a9850"; RED = "#d73027"; GRAY = "#b0b0b0"; BLUE = "#2166ac"; ORANGE = "#e08214"
PRO = "#2166ac"; FLASH = "#e08214"; LUNA = "#6a3d9a"; MIMO = "#00868b"

TASKS = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"]


# ============================================================
# Fig 4 (fig_alignment.pdf): LG M50T BOL 0.1C measured vs simulated
# ============================================================
def fig_alignment():
    import pandas as pd
    csv = glob.glob(str(ROOT / "calibration" / "lgm50t" / "extracted" / "**" / "*.csv"), recursive=True)[0]
    df = pd.read_csv(csv)
    real_chg = df["Charge (mA.h)"].values
    real_v = df["Voltage (V)"].values
    cap_real = real_chg[-1] - real_chg[0]

    sim = json.loads((ROOT / "calibration" / "lgm50t" / "oregan_01C_dfn.json").read_text(encoding="utf-8"))
    t = np.asarray(sim["time_s"]); v = np.asarray(sim["voltage_v"])
    cap_sim = float(sim["capacity_ah"]) * 1000.0

    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.plot((real_chg - real_chg[0]) / cap_real * 100, real_v, color=RED, lw=1.6,
            label=f"Measured LG M50T BOL (0.1C), {cap_real:.0f} mAh")
    ax.plot(t / t[-1] * 100, v, color=BLUE, lw=1.6, ls="--",
            label=f"Simulated ORegan2022 DFN (0.1C), {cap_sim:.0f} mAh")
    ax.set_xlabel("Depth of discharge (%)")
    ax.set_ylabel("Cell voltage (V)")
    ax.set_title("Real-data anchor: BoL 0.1C discharge")
    ax.legend(frameon=False)
    ax.annotate("capacity +0.45%  |  RMSE 20.6 mV (DoD 2–82%)",
                xy=(60, 3.62), fontsize=8, color="k")
    fig.tight_layout(); fig.savefig(OUT / "fig_alignment.pdf"); plt.close(fig)
    print("fig_alignment.pdf")


# ============================================================
# Fig 6 (fig_c1_yardstick.pdf): yardstick-failure panels
# ============================================================
def fig_c1_yardstick():
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.5))
    # (a) threshold shift
    ax = axes[0]
    ax.axvspan(-10, 0, color="#f7dddd", alpha=0.85)          # self-set safety window
    ax.barh([0], [6.9], left=[-6.9], color=RED, height=0.42)  # C1 claim at -6.9 mV
    ax.plot([0, 0], [-0.4, 1.1], color="k", lw=1.2)           # contract line
    ax.plot([-10, -10], [-0.2, 1.1], color=RED, lw=0.8, ls=":")
    ax.text(-3.45, -0.42, "C1 claim: $-6.9$ mV", ha="center", fontsize=6.5, color=RED)
    ax.text(-10, 1.22, "self-set onset −10 mV", ha="center", fontsize=6, color=RED)
    ax.text(0.25, 1.22, "contract:", ha="left", fontsize=6)
    ax.text(0.25, 1.02, "$\eta\\geq 0$", ha="left", fontsize=6)
    ax.set_yticks([0]); ax.set_yticklabels(["C1 claim"], fontsize=7)
    ax.set_xlim(-16, 2); ax.set_ylim(-0.75, 1.5)
    ax.set_xlabel("$\eta$ (mV)", fontsize=8); ax.set_title("(a) threshold shift — T1", fontsize=8, pad=6)
    # (b) model substitution
    ax = axes[1]
    ax.bar(["claimed", "contract model"], [15.1, 818.9],
           color=[GREEN, RED], width=0.55)
    for x, v in zip([0, 1], [15.1, 818.9]):
        ax.text(x, v + 18, f"{v:.1f}", ha="center", fontsize=6.5)
    ax.axhline(550, color="k", lw=1, ls="--"); ax.text(1.42, 565, "limit 550 nm", fontsize=6.5)
    ax.set_ylabel("SEI @500 cyc (nm)", fontsize=8); ax.set_title("(b) model substitution — T2", fontsize=8, pad=6)
    # (c) purchased parameter + caliber shift
    ax = axes[2]
    ax.bar(["claimed", "contract caliber"], [96.7, 94.1],
           color=[GREEN, RED], width=0.55)
    for x, v in zip([0, 1], [96.7, 94.1]):
        ax.text(x, v + 0.6, f"{v:.1f}", ha="center", fontsize=6.5)
    ax.axhline(95, color="k", lw=1, ls="--"); ax.text(1.42, 95.5, "limit 95%", fontsize=6.5)
    ax.set_ylabel("5C retention (%)", fontsize=8); ax.set_ylim(60, 100.5)
    ax.set_title("(c) purchased $D_s$ + caliber — T3", fontsize=8, pad=6)
    fig.suptitle("Yardstick failure modes of the protocol-free agent (mechanical re-adjudication)",
                 y=1.0, fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(OUT / "fig_c1_yardstick.pdf"); plt.close(fig)
    print("fig_c1_yardstick.pdf")


# ============================================================
# Fig 7 (fig_ablation.pdf): mechanism effect decomposition
# ============================================================
def fig_ablation():
    mechs = [
        ("Ceiling escalation\noff", ["T2", "T6"], ["T5"], "2/3 causal"),
        ("Architecture forcing\noff", ["T2"], ["T1", "T3", "T4", "T7", "T8"], "1/6 narrow"),
        ("Funnel voting\noff", [], ["T2", "T5", "T6"], "0/3 null\n(molecular path taken more)"),
    ]
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    y = 0
    for name, flipped, same, label in mechs:
        ax.barh(y, len(flipped), color=RED, height=0.55)
        ax.barh(y, len(same), left=len(flipped), color=GRAY, height=0.55)
        ax.text(len(flipped) + len(same) + 0.12, y, f"{label}  ({'/'.join(flipped) if flipped else 'no flip'})",
                va="center", fontsize=8)
        ax.text(-0.15, y, name, ha="right", va="center", fontsize=8)
        y += 1
    ax.set_xlim(0, 7.6); ax.set_yticks([]); ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax.set_xlabel("tasks (red = verdict flipped when mechanism off; gray = unchanged)")
    ax.set_title("Ablation: what each governance component actually carries")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=RED, label="verdict flipped"), Patch(color=GRAY, label="no change")],
              loc="lower right", frameon=False, fontsize=7.5)
    fig.tight_layout(); fig.savefig(OUT / "fig_ablation.pdf"); plt.close(fig)
    print("fig_ablation.pdf")


# ============================================================
# Fig 8 (fig_trace_t6.pdf): governed decision trace on T6
# ============================================================
def fig_trace_t6():
    p = ROOT / "runs" / "exp" / "t6_r1" / "log.jsonl"
    es = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    rounds, whl = [], []
    for e in es:
        if e.get("action") == "evaluate" and isinstance(e.get("round"), int):
            m = e.get("metrics", {})
            if isinstance(m.get("energy_density_wh_l"), (int, float)):
                rounds.append(e["round"]); whl.append(m["energy_density_wh_l"])
    # funnel entry position (LNMO switch): first evaluate after the funnel entry
    switch_round = None
    idx_fun = next(i for i, e in enumerate(es) if e.get("action") == "funnel" and e.get("passed") == 1)
    for e in es[idx_fun:]:
        if e.get("action") == "evaluate" and isinstance(e.get("round"), int):
            switch_round = e["round"]; break
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.plot(rounds, whl, "o-", color=BLUE, lw=1.2, ms=4)
    ax.axhline(950, color=RED, lw=1, ls="--"); ax.text(0.3, 960, "contract ≥ 950 Wh/L", fontsize=7, color=RED)
    ax.axhline(854, color=GRAY, lw=1, ls=":"); ax.text(0.3, 862, "baseline ceiling ≈ 854", fontsize=7, color=GRAY)
    if switch_round:
        ax.axvline(switch_round - 0.5, color=GREEN, lw=1, ls=":")
        ax.annotate("LNMO system switch\n(ceiling escalation)", xy=(switch_round, 1005),
                    xytext=(switch_round + 0.6, 980), fontsize=7, color=GREEN,
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.8))
    ax.set_xlabel("Round"); ax.set_ylabel("Volumetric ED (Wh/L)")
    ax.set_xticks(sorted(set(rounds))); ax.set_ylim(800, 1200)
    ax.set_title("Governed decision trace — T6 (smartphone)")
    fig.tight_layout(); fig.savefig(OUT / "fig_trace_t6.pdf"); plt.close(fig)
    print("fig_trace_t6.pdf")


# ============================================================
# Fig 9 (fig_bo_trajectories.pdf): BO convergence per task
# ============================================================
def fig_bo_trajectories():
    dirs = {"T1": "t1_r2", "T2": "t2_r2", "T3": "t3_r1", "T4": "t4_r1",
            "T5": "t5_r1", "T6": "t6_r1", "T7": "t7_r1", "T8": "t8_r1"}
    passed = {"T1", "T4", "T8"}
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    for t, d in dirs.items():
        p = ROOT / "runs" / "c2" / d / "bo_trajectory.json"
        if not p.exists():
            continue
        traj = json.loads(p.read_text(encoding="utf-8"))
        obj = [x["objective"] for x in traj]
        best = np.maximum.accumulate(obj)
        color = GREEN if t in passed else RED
        ax.plot(best, lw=1.2, color=color, alpha=0.85)
        ax.annotate(t, xy=(len(best) - 1, best[-1]), fontsize=7, color=color,
                    xytext=(2, 0), textcoords="offset points")
    ax.set_xlabel("BO evaluation"); ax.set_ylabel("Best objective (ED − penalties)")
    ax.set_title("Bayesian optimization trajectories (Ax, seed 1234, 50 evals)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=GREEN, label="contract achieved (3)"),
                       Patch(color=RED, label="contract failed (5)")], frameon=False, fontsize=7.5)
    fig.tight_layout(); fig.savefig(OUT / "fig_bo_trajectories.pdf"); plt.close(fig)
    print("fig_bo_trajectories.pdf")


# ============================================================
# Fig 10 (fig_cost.pdf): resource cost, two panels
# ============================================================
def fig_cost():
    turns_pro = [303, 380, 263, 327, 350, 468, 371, 261]
    turns_fl = [258, 191, 244, 323, 376, 437, 374, 215]
    tin_pro = [232, 210, 173, 196, 164, 235, 149, 158]
    tout_pro = [176, 202, 136, 139, 169, 234, 148, 147]
    tin_fl = [128, 82, 136, 152, 149, 207, 175, 94]
    tout_fl = [75, 83, 91, 129, 141, 245, 142, 87]
    x = np.arange(8); w = 0.38
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.4, 2.9))
    a1.bar(x - w/2, turns_pro, w, color=PRO, label="pro")
    a1.bar(x + w/2, turns_fl, w, color=FLASH, label="flash")
    a1.set_xticks(x); a1.set_xticklabels(TASKS); a1.set_ylabel("Turns")
    a1.set_title("(a) harness turns"); a1.legend(frameon=False)
    a2.bar(x - w/2, tin_pro, w, color=PRO, label="pro in", alpha=0.85)
    a2.bar(x - w/2, tout_pro, w, bottom=tin_pro, color=PRO, alpha=0.45, label="pro out")
    a2.bar(x + w/2, tin_fl, w, color=FLASH, label="flash in", alpha=0.85)
    a2.bar(x + w/2, tout_fl, w, bottom=tin_fl, color=FLASH, alpha=0.45, label="flash out")
    a2.set_xticks(x); a2.set_xticklabels(TASKS); a2.set_ylabel("Tokens (k)")
    a2.set_title("(b) model tokens (in/out)"); a2.legend(frameon=False, fontsize=6.5)
    fig.tight_layout(); fig.savefig(OUT / "fig_cost.pdf"); plt.close(fig)
    print("fig_cost.pdf")


# ============================================================
# Fig 11 (fig_model_robustness.pdf): four-model design diversity
# ============================================================
def fig_model_robustness():
    def last_metric(run, key):
        for p in (ROOT / "runs" / "exp" / run / "log.jsonl", ROOT / "runs" / run / "log.jsonl"):
            if p.exists():
                es = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
                break
        for e in reversed(es):
            m = e.get("metrics", {}) if e.get("action") == "evaluate" else {}
            if isinstance(m.get(key), (int, float)):
                return m[key]
        return None
    t1 = {"pro": 553.98, "flash": 459.4,
          "luna": last_metric("t1_r1_luna", "energy_density_wh_kg"),
          "mimo": last_metric("t1_r1_mimo", "energy_density_wh_kg")}        # ED Wh/kg
    t5 = {"pro": last_metric("t5_r1", "energy_density_wh_kg"),
          "flash": last_metric("t5_r1_flash", "energy_density_wh_kg"),
          "luna": last_metric("t5_r1_luna", "energy_density_wh_kg"),
          "mimo": last_metric("t5_r1_mimo", "energy_density_wh_kg")}
    t6 = {"pro": 1135.8, "flash": last_metric("t6_r1_flash", "energy_density_wh_l"),
          "luna": last_metric("t6_r1_luna", "energy_density_wh_l"),
          "mimo": last_metric("t6_r1_mimo", "energy_density_wh_l")}
    fails = {"T1": {"luna", "mimo"}, "T5": {"luna"}, "T6": {"luna", "mimo"}}
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=False)
    specs = [("T1 sedan\nED (Wh/kg)", t1, 392.61, "luna & mimo: ED clears,\nplating line fails"),
             ("T5 flagship\nED (Wh/kg)", t5, 500.94, "luna stalls below contract\n(ceiling); mimo clears"),
             ("T6 phone\nWh/L", t6, 950, "both foreign-vendor legs\nbelow contract (plateau)")]
    for ax, (title, vals, thresh, note) in zip(axes, specs):
        keys = list(vals.keys())
        vv = [vals[k] if vals[k] else 0 for k in keys]
        cols = [PRO, FLASH, LUNA, MIMO]
        bar = ax.bar(keys, vv, color=cols, width=0.55)
        for b, k in zip(bar, keys):
            if k in fails[title[:2]]:
                b.set_edgecolor(RED); b.set_linewidth(1.6)
        ax.axhline(thresh, color=RED, ls="--", lw=1)
        ax.text(0.5, thresh * 1.002, f"contract {thresh}", fontsize=6, color=RED, ha="center")
        ax.set_title(title, fontsize=8.5); ax.set_ylim(0, max(vv) * 1.15)
        ax.text(0.5, max(vv) * 1.05, note, fontsize=6, ha="center", va="top")
    fig.suptitle("Same contracts, different designs — 8/8 under primary models, 4/8 under each foreign-vendor leg",
                 y=1.04, fontsize=8.5)
    fig.tight_layout(); fig.savefig(OUT / "fig_model_robustness.pdf"); plt.close(fig)
    print("fig_model_robustness.pdf (check None values:", {k: v for k, v in t5.items()}, {k: v for k, v in t6.items()}, ")")


# ============================================================
# Supp figs
# ============================================================
def fig_case_t6_curves():
    """Case-study figure (T6): (a) 1C discharge curves, Chen2020 baseline vs the
    final LNMO design, against the 4.1 V plateau contract line; (b) the final
    design's 4C fast-charge anode potential with the 0 V plating criterion."""
    cell = ROOT / "runs" / "exp" / "t6_r1" / "cell"
    base = json.loads((cell / "r1_chen2020_1c_spme.json").read_text(encoding="utf-8"))
    fin1c = json.loads((cell / "r8_d6_1c_dfn.json").read_text(encoding="utf-8"))
    fin4c = json.loads((cell / "r8_d6_4c_dfn.json").read_text(encoding="utf-8"))

    def midpoint_v(d):
        t = np.asarray(d["time_s"]); v = np.asarray(d["voltage_v"])
        return float(v[int(len(t) * 0.5)])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.9))
    # (a) discharge curves vs DoD
    for d, lab, c in ((base, "Chen2020 baseline", GRAY), (fin1c, "final LNMO design", BLUE)):
        t = np.asarray(d["time_s"]); v = np.asarray(d["voltage_v"])
        a1.plot(t / t[-1] * 100, v, lw=1.3, color=c, label=lab)
    a1.axhline(4.1, color=RED, ls="--", lw=1)
    a1.text(1, 4.115, "contract plateau ≥ 4.1 V", fontsize=6.5, color=RED)
    a1.annotate(f"midpoint {midpoint_v(base):.3f} V", xy=(50, midpoint_v(base)),
                xytext=(8, 3.55), fontsize=6.5, color=GRAY)
    a1.annotate(f"midpoint {midpoint_v(fin1c):.4f} V", xy=(50, midpoint_v(fin1c)),
                xytext=(55, 4.22), fontsize=6.5, color=BLUE)
    a1.set_xlabel("Depth of discharge (%)"); a1.set_ylabel("Voltage (V)")
    a1.set_title("(a) why the system switch was necessary", fontsize=8.5)
    a1.legend(frameon=False, fontsize=7)
    # (b) 4C anode potential
    t = np.asarray(fin4c["time_s"]) / 60.0
    v = np.asarray(fin4c["anode_potential_v"]) * 1000.0
    a2.plot(t, v, lw=1.1, color=BLUE)
    a2.axhline(0, color=RED, ls="--", lw=1)
    a2.text(0.5, 6, "plating criterion: min ≥ 0 V", fontsize=6.5, color=RED)
    a2.annotate(f"min {v.min():+.1f} mV", xy=(t[np.argmin(v)], v.min()),
                xytext=(t[np.argmin(v)] + 1, v.min() - 45), fontsize=6.5, color=BLUE,
                arrowprops=dict(arrowstyle="->", lw=0.7, color=BLUE))
    a2.set_xlabel("Time (min)"); a2.set_ylabel("Anode potential (mV)")
    a2.set_title("(b) mechanical plating criterion, 4C charge", fontsize=8.5)
    fig.tight_layout(); fig.savefig(OUT / "fig_case_t6_curves.pdf"); plt.close(fig)
    print("fig_case_t6_curves.pdf")


def fig_endorse_levels():
    """Fig: HOMO/LUMO level diagram for the four endorsed molecules vs the
    -6.0 eV elimination line (data: df_endorse_out.json, ORCA r2SCAN-3c)."""
    import json as _json
    p = ROOT / "runs" / "exp" / "t5_r1_flash" / "df_endorse_out.json"
    data = _json.loads(p.read_text(encoding="utf-8"))
    names = {"C1OC(=O)OC1F": "FEC", "C1=COC(=O)O1": "VC",
             "C1CCS(=O)(=O)O1": "PES", "C1COS(=O)(=O)O1": "DTD"}
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    for i, c in enumerate(data["candidates"]):
        e = c["endorsement"]
        x = i
        ax.plot([x - 0.22, x + 0.22], [e["homo_ev"]] * 2, color=BLUE, lw=2.4)
        ax.plot([x - 0.22, x + 0.22], [e["lumo_ev"]] * 2, color=ORANGE, lw=2.4)
        ax.annotate("", xy=(x, e["lumo_ev"] + 0.05), xytext=(x, e["homo_ev"] - 0.05),
                    arrowprops=dict(arrowstyle="<->", lw=0.7, color="gray"))
        ax.text(x + 0.26, (e["homo_ev"] + e["lumo_ev"]) / 2, f"{e['homo_ev']-e['lumo_ev']:.1f}",
                fontsize=7, va="center", color="gray")
        ax.text(x, e["homo_ev"] - 0.35, f"{e['homo_ev']:.2f}", ha="center", fontsize=7.5, color=BLUE)
        ax.text(x, e["lumo_ev"] + 0.30, f"{e['lumo_ev']:.2f}", ha="center", fontsize=7.5, color=ORANGE)
    ax.axhline(-6.0, color=RED, ls="--", lw=1.1)
    ax.text(3.55, -5.85, "elimination\nline −6.0 eV", fontsize=6.5, color=RED, ha="right", va="bottom")
    ax.set_xticks(range(4)); ax.set_xticklabels([names[c["smiles"]] for c in data["candidates"]])
    ax.set_ylabel("Orbital energy (eV)")
    ax.set_ylim(-8.2, 1.6)
    ax.set_title("True DFT endorsement: HOMO/LUMO (ORCA r2SCAN-3c)")
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([0], [0], color=BLUE, lw=2.4, label="HOMO"),
                       Line2D([0], [0], color=ORANGE, lw=2.4, label="LUMO")],
              loc="lower right", frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(OUT / "fig_endorse_levels.pdf"); plt.close(fig)
    print("fig_endorse_levels.pdf")


def supp_plating():
    cands = glob.glob(str(ROOT / "runs" / "exp" / "t2_r1" / "**" / "*.json"), recursive=True)
    src = None
    for c in cands:
        try:
            d = json.loads(open(c, encoding="utf-8").read())
        except Exception:
            continue
        if "anode_potential_v" in d and isinstance(d.get("time_s"), (list,)) and len(d.get("anode_potential_v", [])) > 100:
            src = c; break
    if src is None:
        print("supp_plating: no anode-potential series found under t2_r1; skipped")
        return
    d = json.loads(open(src, encoding="utf-8").read())
    t = np.asarray(d["time_s"]); v = np.asarray(d["anode_potential_v"]) * 1000  # mV
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.plot(t / 60, v, color=BLUE, lw=1.2)
    ax.axhline(0, color=RED, lw=1, ls="--")
    ax.text(0.02, 8, "plating criterion: min ≥ 0 V", fontsize=7, color=RED)
    ax.set_xlabel("Time (min)"); ax.set_ylabel("Anode potential (mV)")
    ax.set_title("Governed T2 design, 4C charge — mechanical plating criterion")
    fig.tight_layout(); fig.savefig(OUT / "fig_supp_plating.pdf"); plt.close(fig)
    print("fig_supp_plating.pdf from", os.path.basename(src))


def supp_sei():
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.bar(["Chen2020 baseline\n(standard SEI)", "Governed T2\n(SEI bridge)"], [449.1, 9.09],
           color=[GRAY, GREEN], width=0.5)
    ax.axhline(500, color=RED, ls="--", lw=1); ax.text(1.45, 505, "contract ≤ 500 nm", fontsize=7, color=RED)
    ax.set_ylabel("SEI @100 cycles (nm)")
    ax.set_title("SEI-kinetics bridge effect — T2")
    fig.tight_layout(); fig.savefig(OUT / "fig_supp_sei.pdf"); plt.close(fig)
    print("fig_supp_sei.pdf")


if __name__ == "__main__":
    fig_alignment()
    fig_c1_yardstick()
    fig_ablation()
    fig_trace_t6()
    fig_bo_trajectories()
    fig_cost()
    fig_model_robustness()
    fig_case_t6_curves()
    fig_endorse_levels()
    supp_plating()
    supp_sei()
    print("ALL DONE")
