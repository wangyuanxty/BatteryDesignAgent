"""make_fig_arch.py — native redraw of Figure 2 (architecture schematic).

Faithful to figs/prompts/fig_arch_v2.md: four regions + example-trace strip
+ legend. Vector-safe geometry (paths only), exported as 4K PNG and PDF.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, RegularPolygon, Circle

INK = "#14283C"
COPPER = "#C97B3D"
BLUE = "#1E5A8A"
BG = "#F4F7FA"
GREEN = "#2E7D4F"
RED = "#B3402A"
PANEL = "#FFFFFF"
GRID = "#D8E2EC"
SAGE = "#7FC79B"

W, H = 16.72, 9.41  # inches at 230 dpi -> 3846x2164 (4K)
fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, 100); ax.set_ylim(0, 56.3); ax.axis("off")
fig.patch.set_facecolor(BG)


def box(x, y, w, h, fc=PANEL, ec=GRID, lw=1.2, r=1.2, ls="-", z=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=z)
    ax.add_patch(p)
    return p


def hexagon(x, y, r_eff=4.2, fc="#FFFFFF", ec=BLUE, lw=1.4, z=2):
    p = RegularPolygon((x, y), numVertices=6, radius=r_eff,
                       fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(p)
    return p


def txt(x, y, s, size=9, color=INK, weight="normal", ha="center", va="center",
        z=5, style="normal"):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight, ha=ha, va=va,
            zorder=z, fontstyle=style)


def marker(x, y, n, color=COPPER):
    c = Circle((x, y), 1.0, fc=color, ec="white", lw=1.0, zorder=6)
    ax.add_patch(c)
    txt(x, y, n, size=7.5, color="white", weight="bold", z=7)


def arrow(x1, y1, x2, y2, color=INK, lw=1.6, ls="-", style="-|>", z=4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, color=color,
                        lw=lw, linestyle=ls, mutation_scale=14, zorder=z,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)


# ---- Title ----
txt(50, 54.2, "Protocolized governance of an LLM design agent", size=20, weight="bold")
txt(50, 51.6, "five-stage funnel, fallback routing, mechanized verdicts, evidence-chain audit",
    size=11.5, color="#44586C")

# ---- Region 1: Contract input ----
marker(4.2, 48.6, "①")
txt(8.0, 48.6, "Contract input", size=11.5, weight="bold")
box(3, 38.2, 21.5, 9.2, fc=PANEL)
txt(5.2, 45.4, "User", size=10.5, weight="bold", ha="left")
txt(5.2, 42.6, "design a battery for a sedan:\nenergy density ≥ 392.61 Wh/kg,\n4C fast charge without\nlithium plating, T_max ≤ 60 °C",
    size=8.8, ha="left", va="center")
txt(5.2, 39.0, "natural language only —\nno config files", size=7.8, color="#5E768C", ha="left", style="italic")

# ---- Region 2: Governed agent loop ----
marker(30.0, 48.9, "②")
txt(34.0, 48.9, "Governed agent loop", size=11.5, weight="bold")
hexagon(31.5, 35.4, r_eff=6.6, fc="#FDF6EC", ec=COPPER, lw=2.0)
txt(31.5, 38.2, "Governed", size=10.5, weight="bold")
txt(31.5, 35.8, "LLM agent", size=10.5, weight="bold")
txt(31.5, 32.6, "verdicts computed,\nnot asserted", size=7.6, color=COPPER)
for dx, dy, lab in [(0, 10.8, "five-stage\nfunnel"), (-12.6, 1.2, "fallback\nrouting"), (12.6, -1.4, "ceiling\nassessment")]:
    box(31.5 + dx - 6.0, 35.4 + dy - 2.2, 12.0, 4.4, fc="#EEF3F8", lw=1.0)
    txt(31.5 + dx, 35.4 + dy, lab, size=8.0)
arrow(31.5, 42.0, 31.5, 45.2, color="#9FB7CC", lw=1.0, style="-")
arrow(31.5, 28.8, 31.5, 25.0, color=INK, lw=1.8)
arrow(37.6, 35.0, 39.5, 34.6, color="#9FB7CC", lw=1.0, style="-")
arrow(25.4, 35.0, 27.2, 35.4, color="#9FB7CC", lw=1.0, style="-")
arrow(31.5, 44.0, 29.5, 44.9, color="#9FB7CC", lw=1.0, style="-")

# ---- Region 3: Design levers ----
marker(49.5, 48.6, "③")
txt(54.0, 48.6, "Design levers", size=11.5, weight="bold")
lever = [(52.5, 42.2, "Materials", "molecule, coating"), (63.5, 42.2, "Formulation", "solvent, salt"),
         (52.5, 31.2, "Cell architecture", "thickness, N:P"), (63.5, 31.2, "Thermal management", "h-coeff, cooling")]
for x, y, name, sub in lever:
    hexagon(x, y, r_eff=6.0)
    txt(x, y + 1.4, name, size=9.2, weight="bold")
    txt(x, y - 2.0, sub, size=6.4, color="#5E768C")
    c = Circle((x + 2.2, y - 2.4), 0.7, fc=SAGE, ec="none", zorder=6)
    ax.add_patch(c)
arrow(38.1, 35.4, 46.5, 38.6, color=BLUE, lw=1.6)
arrow(58.5, 39.2, 52.6, 38.9, color="#9FB7CC", lw=1.0, style="-")
arrow(69.5, 39.2, 63.6, 38.9, color="#9FB7CC", lw=1.0, style="-")
arrow(58.5, 31.0, 52.6, 30.7, color="#9FB7CC", lw=1.0, style="-")
arrow(69.5, 31.0, 63.6, 30.7, color="#9FB7CC", lw=1.0, style="-")

# ---- Region 4: Tools & adjudication ----
marker(73.8, 48.6, "④")
txt(77.5, 48.6, "Tools & adjudication", size=11.5, weight="bold")
box(71.5, 37.5, 12.8, 9.6, lw=1.0)
txt(75.0, 45.3, "(a) Tool library (CLI)", size=8.2, weight="bold")
for i, t in enumerate(["run-pyamm ×N", "calc-energy", "run-mlp", "run-xtb", "run-orca"]):
    txt(78.2, 43.7 - i * 1.5, t, size=7.6, ha="center")
box(85.0, 37.5, 11.8, 9.6, lw=1.0, fc="#F2F8F2")
txt(89.0, 45.3, "(b) Audit ledger", size=8.2, weight="bold")
txt(89.0, 43.0, "log.jsonl — entry-0 criteria", size=7.4)
ell = FancyBboxPatch((86.4, 39.0), 5.6, 2.6, boxstyle="round,pad=0,rounding_size=1.2",
                     fc="#FFFFFF", ec="#7FC79B", lw=1.2, zorder=2)
ax.add_patch(ell)
txt(89.2, 40.3, "evidence chain — file:key per criterion", size=6.4)
arrow(84.3, 42.3, 85.0, 42.3, color=GREEN, lw=1.6)
box(71.5, 25.8, 25.3, 8.0, fc="#FEF5F3", ec=RED, lw=1.6, ls=(0, (4, 3)), r=1.4)
txt(84.1, 32.0, "adjudication layer — outside the agent", size=9.2, weight="bold", color=RED)
box(75.5, 27.2, 7.8, 3.4, lw=1.0)
txt(79.4, 28.9, "log-evaluate:\nmechanical verdicts", size=6.8)
box(85.0, 27.2, 7.8, 3.4, lw=1.0)
txt(88.9, 28.9, "verify:\naudit-chain checks", size=6.8)
arrow(92.9, 31.5, 93.5, 37.5, color=RED, lw=1.4, ls=(0, (3, 2)))
arrow(78.5, 31.5, 79.0, 36.9, color=RED, lw=1.4, ls=(0, (3, 2)))

# ---- Example trace ----
txt(3, 21.2, "Example trace (one design iteration)", size=10.5, weight="bold", ha="left")
trace = [("contract stated", "user intent captured,\nconstraints parsed"),
         ("entry-0 pre-registration", "measurable targets\nregistered,\nevaluation plan locked"),
         ("ceiling assessment", "theoretical / empirical\nupper bounds estimated,\nfeasibility check"),
         ("material switch (LNMO)", "candidate screened,\nprops logged,\ndecision recorded"),
         ("simulate (run-pyamm)", "simulate scenarios,\ncollect metrics,\nstore outputs"),
         ("evaluate (fail ×N)", "compare to criteria,\nfail reasons logged,\nevidence linked"),
         ("re-plan", "adjust levers,\nupdate plan,\nroute fallback if needed"),
         ("final achieved", "criteria met,\nevidence packaged,\ndeliverables generated")]
for i, (head, body) in enumerate(trace):
    x = 3 + i * 11.9
    box(x, 9.5, 10.8, 9.4, fc=PANEL, lw=1.0)
    txt(x + 1.6, 17.3, str(i + 1), size=7.5, weight="bold", color=COPPER, ha="center")
    txt(x + 5.4, 17.3, head, size=7.2, weight="bold")
    txt(x + 5.4, 13.6, body, size=6.2, color="#44586C")
    if i < len(trace) - 1:
        arrow(x + 10.85, 14.2, x + 11.9, 14.2, color="#9FB7CC", lw=1.0)
arrow(45.0, 9.5, 45.0, 5.6, color=BLUE, lw=1.4, ls=(0, (3, 2)))
arrow(45.0, 5.6, 33.0, 5.6, color=BLUE, lw=1.4)
arrow(33.0, 5.6, 33.0, 9.5, color=BLUE, lw=1.4, style="-|>")

# ---- Legend ----
leg = [("inputs / governance", PANEL), ("design levers", "#EEF3F8"), ("tools", PANEL),
       ("evidence / ledger", "#F2F8F2"), ("outside-agent adjudication", "#FEF5F3")]
txt(3, 3.2, "Legend", size=8.5, weight="bold", ha="left")
for i, (lab, fc) in enumerate(leg):
    x = 11 + i * 14.2
    box(x, 1.4, 13.4, 3.2, fc=fc, lw=1.0, ec=BLUE if fc == PANEL and i == 0 else GRID)
    txt(x + 6.7, 3.0, lab, size=7.0)
txt(86.5, 4.0, "status:", size=7.0, weight="bold", ha="left")
for i, (lab, col) in enumerate([("healthy", SAGE), ("at-risk", COPPER), ("fail", RED)]):
    x = 91.0 + i * 3.2
    c = Circle((x, 3.0), 0.8, fc=col, ec="none", zorder=6)
    ax.add_patch(c)
    txt(x + 1.2, 3.0, lab, size=6.4, ha="left")

fig.tight_layout(pad=0.4)
fig.savefig("fig_arch_4k.png", dpi=230, facecolor=BG)
fig.savefig("fig_arch_vector.pdf", facecolor=BG)
print("saved fig_arch_4k.png + fig_arch_vector.pdf")
