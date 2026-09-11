"""Regenerate the paper's schematic figures with matplotlib (vector PDF, journal style).

Replaces the AI-generated raster figures used by the paper:
  figs/fig_overview_b.png  -> figs/fig_overview_b.pdf   (Fig. 1a: governance idea)
  figs/fig_overview_c.png  -> figs/fig_overview_c.pdf   (Fig. 1b: five fidelity rungs)
  figs/fig_arch_v6.png     -> figs/fig_arch.pdf         (Fig. 2: system architecture)
  figs/fig_protocol_v2.png -> figs/fig_protocol.pdf     (Fig. 3: protocolized loop)

Style: thin black/gray strokes, near-square corners, white fills with at most a faint
gray tint, one muted accent colour for the items that carry consequence (the contract,
the true-compute stage, the adjudication layer's verdicts), one muted slate for the
agent. No shadows, no gradients, no saturated fills.

Run:  D:/anaconda/envs/py312/python.exe paper/figs/make_overview_figs.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).resolve().parent

INK = "#1a1a1a"        # strokes and primary text
GRAY = "#5f5f5f"       # secondary text
LIGHT = "#b9b9b9"      # tertiary strokes
ACCENT = "#8a3b2e"     # contract / criteria / true compute (muted brick)
SLATE = "#2b4a63"      # the agent (muted slate blue)
TINT_NEUTRAL = "#f6f6f6"
TINT_ACCENT = "#faf4f2"
TINT_SLATE = "#f4f6f8"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.linewidth": 0,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})


def _blank(w: float, h: float):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def _box(ax, x, y, w, h, text, *, fc="white", ec=INK, lw=0.8, fs=8.0, weight="normal",
         ls="-", tc=INK, zorder=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.006",
                                linewidth=lw, edgecolor=ec, facecolor=fc, linestyle=ls,
                                zorder=zorder))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
            weight=weight, zorder=zorder + 1, linespacing=1.5)


def _arrow(ax, p0, p1, *, color=INK, lw=0.8, style="-|>", ls="-", zorder=2):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=7, linewidth=lw,
                                 color=color, linestyle=ls, zorder=zorder,
                                 connectionstyle="arc3,rad=0"))


def _elbow(ax, p0, p1, *, color=INK, lw=0.8, ls="-", via_y=None, zorder=2):
    """Three-segment orthogonal connector p0 -> across at via_y -> p1."""
    (x0, y0), (x1, y1) = p0, p1
    yv = via_y if via_y is not None else (y0 + y1) / 2
    ax.plot([x0, x0], [y0, yv], color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle="round")
    ax.plot([x0, x1], [yv, yv], color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle="round")
    ax.plot([x1, x1], [yv, y1], color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle="round")
    _arrow(ax, (x1, yv), (x1, y1), color=color, lw=lw, ls=ls, zorder=zorder + 1)


def _elbow_h(ax, p0, p1, *, color=INK, lw=0.8, ls="-", via_x=None, zorder=2):
    """Three-segment orthogonal connector p0 -> across at via_x -> p1 (for side returns)."""
    (x0, y0), (x1, y1) = p0, p1
    xv = via_x if via_x is not None else (x0 + x1) / 2
    ax.plot([x0, xv], [y0, y0], color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle="round")
    ax.plot([xv, xv], [y0, y1], color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle="round")
    ax.plot([xv, x1], [y1, y1], color=color, lw=lw, ls=ls, zorder=zorder, solid_capstyle="round")
    _arrow(ax, (xv, y1), (x1, y1), color=color, lw=lw, ls=ls, zorder=zorder + 1)


def _label(ax, x, y, text, *, fs=7.5, color=INK, weight="normal", ha="center", va="center",
           style="normal"):
    ax.text(x, y, text, fontsize=fs, color=color, weight=weight, ha=ha, va=va, style=style,
            zorder=6, linespacing=1.4)


# ------------------------------------------------------------------- Fig. 1a: the governance idea
def fig_overview_b() -> None:
    fig, ax = _blank(4.4, 3.2)

    # --- agent (left), holding the five lever families
    ax.add_patch(FancyBboxPatch((0.030, 0.215), 0.430, 0.725,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=0.9, edgecolor=SLATE, facecolor=TINT_SLATE, zorder=1))
    _label(ax, 0.245, 0.895, "governed agent", fs=9.5, weight="bold", color=SLATE)
    families = ["electrode system", "electrolyte formulation", "electrode modification",
                "cell architecture", "thermal management"]
    for i, fam in enumerate(families):
        y = 0.775 - i * 0.108
        _box(ax, 0.065, y - 0.035, 0.300, 0.070, fam, fc="white", ec=LIGHT, lw=0.7, fs=7.4)
        if i < len(families) - 1:
            _arrow(ax, (0.215, y - 0.035), (0.215, y - 0.073), color=LIGHT, lw=0.7)
    # design loop: orthogonal return path from the last family back to the first
    _elbow_h(ax, (0.365, 0.308), (0.365, 0.740), color=SLATE, lw=0.7, ls=(0, (2.5, 1.8)),
             via_x=0.420)
    _label(ax, 0.393, 0.822, "design loop", fs=6.6, color=SLATE, style="italic")

    # --- contract (right, top of the downward flow)
    _box(ax, 0.520, 0.760, 0.450, 0.180, "contract\ncriteria, fixed before the run",
         fc=TINT_ACCENT, ec=ACCENT, lw=1.0, fs=8.2, weight="bold")
    _arrow(ax, (0.460, 0.850), (0.520, 0.850), color=ACCENT, lw=1.0)

    # --- adjudication layer (below the contract) and the ledger (below that)
    ax.add_patch(FancyBboxPatch((0.520, 0.430), 0.450, 0.245,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=0.9, edgecolor=INK, facecolor="white",
                                linestyle=(0, (3.5, 2)), zorder=1))
    _label(ax, 0.745, 0.625, "adjudication layer (code)", fs=8.2, weight="bold", color=INK)
    _label(ax, 0.745, 0.545, "outside the agent;\nissues the verdict, refuses\nincomplete audit chains",
           fs=6.7, color=GRAY)
    _arrow(ax, (0.745, 0.760), (0.745, 0.675), color=ACCENT, lw=1.0)
    _label(ax, 0.760, 0.717, "criteria", fs=6.2, color=ACCENT, ha="left")

    _box(ax, 0.520, 0.180, 0.450, 0.150, "audit ledger\nlog.jsonl: criteria, verdict,\nevidence",
         fc="white", ec=INK, lw=0.9, fs=6.8)
    _arrow(ax, (0.745, 0.430), (0.745, 0.330), color=INK, lw=0.9)
    _label(ax, 0.760, 0.380, "writes", fs=6.4, color=GRAY, ha="left")

    # --- verdict feeds back to the agent
    _arrow(ax, (0.520, 0.600), (0.460, 0.600), color=INK, lw=0.9)
    _label(ax, 0.490, 0.632, "verdict", fs=6.2, color=INK)

    fig.savefig(HERE / "fig_overview_b.pdf")
    plt.close(fig)


# ------------------------------------------------------------------- Fig. 1b: the five fidelity rungs
def fig_overview_c() -> None:
    fig, ax = _blank(4.8, 2.8)
    rungs = [
        ("planning", "no simulation", "0"),
        ("screening", "MLP + xTB", "ms"),
        ("cell design", "SPMe / DFN", "s"),
        ("safety", "4C / 45 $^\\circ$C", "min"),
        ("endorsement", "DFT / MD", "hours"),
    ]
    n = len(rungs)
    margin, gap = 0.085, 0.020
    w = (1 - 2 * margin - (n - 1) * gap) / n
    for i, (stage, method, cost) in enumerate(rungs):
        x = margin + i * (w + gap)
        h = 0.20 + i * 0.118
        last = i == n - 1
        ax.add_patch(FancyBboxPatch((x, 0.215), w, h,
                                    boxstyle="round,pad=0,rounding_size=0.006",
                                    facecolor=TINT_ACCENT if last else "white",
                                    edgecolor=ACCENT if last else INK,
                                    linewidth=1.0 if last else 0.8, zorder=2))
        _label(ax, x + w / 2, 0.215 + h - 0.065, stage, fs=7.0, weight="bold",
               color=ACCENT if last else INK)
        _label(ax, x + w / 2, 0.215 + h - 0.140, method, fs=6.4, color=GRAY)
        _label(ax, x + w / 2, 0.125, cost, fs=8.4, weight="bold", color=INK)
        if i:
            _arrow(ax, (x - gap + 0.002, 0.250), (x - 0.004, 0.250), color=LIGHT, lw=0.8)
    _label(ax, 0.5, 0.050, "computational cost rises left to right", fs=7.2, color=GRAY)
    fig.savefig(HERE / "fig_overview_c.pdf")
    plt.close(fig)


# ------------------------------------------------------------------- Fig. 2: system architecture
def fig_arch() -> None:
    fig, ax = _blank(6.8, 3.4)

    _box(ax, 0.015, 0.80, 0.19, 0.14, "natural-language\ncontract\n(sole input)",
         fc=TINT_ACCENT, ec=ACCENT, lw=1.0, fs=8.2, weight="bold")
    _arrow(ax, (0.205, 0.87), (0.27, 0.87), color=ACCENT, lw=1.0)

    ax.add_patch(FancyBboxPatch((0.27, 0.365), 0.475, 0.575,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=0.9, edgecolor=SLATE, facecolor=TINT_SLATE, zorder=1))
    _label(ax, 0.5075, 0.895, "governed agent: five-stage loop", fs=8.8, weight="bold", color=SLATE)
    stages = ["1  planning", "2  molecular screening", "3  cell design",
              "4  safety assessment", "5  endorsement (DFT/MD)"]
    top, dy, bh = 0.815, 0.086, 0.060
    for i, s in enumerate(stages):
        y = top - i * dy
        _box(ax, 0.295, y - bh, 0.245, bh, s, fc="white", ec=LIGHT, lw=0.7, fs=7.0)
        if i < len(stages) - 1:
            _arrow(ax, (0.4175, y - bh), (0.4175, y - dy + 0.002), color=LIGHT, lw=0.7)
    _elbow_h(ax, (0.540, top - 4 * dy - bh / 2), (0.540, top - 1 * dy - bh / 2), color=ACCENT,
             lw=0.8, ls=(0, (2.5, 1.8)), via_x=0.615)
    _label(ax, 0.625, 0.655, "diagnosed failure\n$\\rightarrow$ back to the\nscale of its cause",
           fs=6.1, color=ACCENT, ha="left")

    _box(ax, 0.27, 0.175, 0.475, 0.115, "command-line tool library (bda)\nsimulation / screening instruments",
         fc=TINT_NEUTRAL, ec=GRAY, lw=0.8, fs=7.3, tc=INK)
    _arrow(ax, (0.44, 0.365), (0.44, 0.29), color=GRAY, lw=0.8, style="<|-|>")
    _label(ax, 0.455, 0.327, "calls", fs=6.5, color=GRAY, ha="left")

    ax.add_patch(FancyBboxPatch((0.785, 0.365), 0.20, 0.575,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=0.9, edgecolor=INK, facecolor="white",
                                linestyle=(0, (3.5, 2)), zorder=1))
    _label(ax, 0.885, 0.885, "adjudication\nlayer (code)", fs=8.0, weight="bold", color=INK)
    _label(ax, 0.885, 0.785, "outside the agent", fs=6.7, color=GRAY, style="italic")
    _arrow(ax, (0.745, 0.845), (0.785, 0.845), color=INK, lw=0.9)
    _arrow(ax, (0.785, 0.70), (0.745, 0.70), color=INK, lw=0.9)
    _label(ax, 0.885, 0.62, "mechanical verdict,\nper-criterion evidence,\nrefuses incomplete\nchains",
           fs=6.1, color=GRAY)

    _box(ax, 0.785, 0.175, 0.20, 0.115, "audit ledger\nlog.jsonl", fc="white", ec=INK, lw=0.9, fs=6.9)
    _arrow(ax, (0.885, 0.365), (0.885, 0.29), color=INK, lw=0.9)
    _label(ax, 0.90, 0.327, "writes", fs=6.3, color=GRAY, ha="left")

    fig.savefig(HERE / "fig_arch.pdf")
    plt.close(fig)


# ------------------------------------------------------------------- Fig. 3: protocolized loop
def fig_protocol() -> None:
    fig, ax = _blank(7.0, 3.5)

    _box(ax, 0.020, 0.795, 0.190, 0.140, "contract\n(sole input)", fc=TINT_ACCENT, ec=ACCENT,
         lw=1.0, fs=8.6, weight="bold")
    _arrow(ax, (0.210, 0.865), (0.255, 0.865), color=ACCENT, lw=1.0)

    ax.add_patch(FancyBboxPatch((0.255, 0.470), 0.470, 0.465,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=0.9, edgecolor=SLATE, facecolor=TINT_SLATE, zorder=1))
    _label(ax, 0.490, 0.885, "one round of the governed loop", fs=8.8, weight="bold", color=SLATE)
    steps = [("propose", 0.275), ("screen\n(if the bottleneck\nis molecular)", 0.420),
             ("simulate\n(cell / safety)", 0.565)]
    for label, x in steps:
        _box(ax, x, 0.640, 0.135, 0.195, label, fc="white", ec=LIGHT, lw=0.7, fs=7.0)
    _arrow(ax, (0.410, 0.7375), (0.420, 0.7375), color=LIGHT, lw=0.8)
    _arrow(ax, (0.555, 0.7375), (0.565, 0.7375), color=LIGHT, lw=0.8)
    _elbow(ax, (0.6325, 0.640), (0.3425, 0.640), color=ACCENT, lw=0.8, ls=(0, (2.5, 1.8)),
           via_y=0.565)
    _label(ax, 0.4875, 0.605, "diagnosed failure $\\rightarrow$ back to the\nscale of its cause",
           fs=6.5, color=ACCENT)
    _arrow(ax, (0.360, 0.470), (0.360, 0.335), color=INK, lw=1.0)
    _label(ax, 0.373, 0.405, "pass", fs=7.0, color=INK, ha="left")

    _box(ax, 0.020, 0.490, 0.190, 0.135, "ceiling reached:\nescalate to a\nsystem switch",
         fc=TINT_ACCENT, ec=ACCENT, lw=0.9, fs=7.0)
    _arrow(ax, (0.210, 0.5575), (0.255, 0.585), color=ACCENT, lw=0.9)

    ax.add_patch(FancyBboxPatch((0.775, 0.470), 0.205, 0.310,
                                boxstyle="round,pad=0,rounding_size=0.008",
                                linewidth=0.9, edgecolor=INK, facecolor="white",
                                linestyle=(0, (3.5, 2)), zorder=1))
    _label(ax, 0.8775, 0.735, "adjudication layer", fs=8.0, weight="bold", color=INK)
    _label(ax, 0.8775, 0.690, "code, outside the agent", fs=6.7, color=GRAY)
    _label(ax, 0.8775, 0.620, "issues the verdict;\nrefuses incomplete\nchains", fs=6.6, color=GRAY)
    _arrow(ax, (0.725, 0.700), (0.775, 0.700), color=INK, lw=0.9)
    _label(ax, 0.750, 0.732, "criteria", fs=6.1, color=ACCENT)
    _arrow(ax, (0.775, 0.580), (0.725, 0.580), color=INK, lw=0.9)
    _label(ax, 0.750, 0.548, "verdict", fs=6.1, color=INK)

    _box(ax, 0.775, 0.100, 0.205, 0.155, "audit ledger\nlog.jsonl:\ncriteria, verdict,\nevidence",
         fc="white", ec=INK, lw=0.9, fs=6.4)
    _arrow(ax, (0.8775, 0.470), (0.8775, 0.255), color=INK, lw=0.9)
    _label(ax, 0.890, 0.365, "writes", fs=6.4, color=GRAY, ha="left")

    _box(ax, 0.255, 0.115, 0.215, 0.130, "endorsement\n(true DFT / MD\non the finalists)",
         fc=TINT_ACCENT, ec=ACCENT, lw=0.9, fs=7.0)
    _box(ax, 0.500, 0.115, 0.225, 0.130, "deliverable package\nspec, BOM, datasheet,\ncalc, DVPR, DFMEA",
         fc="white", ec=INK, lw=0.9, fs=6.7)
    _arrow(ax, (0.470, 0.180), (0.500, 0.180), color=INK, lw=0.9)

    fig.savefig(HERE / "fig_protocol.pdf")
    plt.close(fig)


def main() -> int:
    fig_overview_b()
    fig_overview_c()
    fig_arch()
    fig_protocol()
    for name in ("fig_overview_b.pdf", "fig_overview_c.pdf", "fig_arch.pdf", "fig_protocol.pdf"):
        p = HERE / name
        print(f"wrote {p.name}  ({p.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
