"""Round-1 close-out driver: append the funnel entry, compute k-rule rate
constants, and write bridge params files for the 5 funnel-passing candidates.

- Importers/callers: invoked manually from this workspace (headless session); no module imports it.
- Affected API: none. Appends one JSONL entry to log.jsonl; writes params JSON
  under cell/; prints a summary.
- Data schemas: log.jsonl entries are the bda append_entry schema (one JSON
  object per line). params files = {"SEI kinetic rate constant [m.s-1]": float}.
- Verbatim instruction: "k(M) = k0 * 10^((HOMO_xtb(M)+12.5)/1.0), k0=1.0e-12 m/s"
  and "write criteria to log.jsonl entry 0 then execute automatically".
"""
import json
from pathlib import Path

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t10_r2")
LOG = WS / "log.jsonl"
K0 = 1.0e-12

# HOMO values (xTB GFN2) for the 5 candidates that pass the full stage-1 funnel
# (both ML legs converged AND HOMO <= -13.74 eV). Source: candidates/round1_xtb.json.
passers = [
    ("bis(trifluoromethyl)sulfone", "FC(F)(F)S(=O)(=O)C(F)(F)F", -14.2961),
    ("pentafluoroethylsulfonyl fluoride", "FC(F)(F)C(F)(F)S(=O)(=O)F", -14.2697),
    ("trifluoronitromethane", "FC(F)(F)[N+](=O)[O-]", -14.1208),
    ("sulfuryl fluoride", "O=S(=O)(F)F", -13.8919),
    ("trifluoroacetonitrile", "FC(F)(F)C#N", -13.8447),
]

rows = []
for name, smi, homo in passers:
    k = K0 * 10 ** ((homo + 12.5) / 1.0)
    rows.append({"name": name, "smiles": smi, "homo_ev": homo, "k_ms": k})

# Write params files (bridge input) for each passer.
for r in rows:
    slug = r["name"].replace("(", "").replace(")", "").replace(" ", "_").replace(",", "")
    slug = slug.replace("[", "").replace("]", "").replace("+", "").replace("-", "")
    p = WS / "cell" / f"params_{slug}.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps({"SEI kinetic rate constant [m.s-1]": r["k_ms"]}, indent=2), encoding="utf-8")

funnel = {
    "action": "funnel",
    "round": 1,
    "passed": 5,
    "rejected": 5,
    "disputed": 0,
    "detail": (
        "Stage-1 molecular funnel over 10 novel perfluoro/hypervalent-sulfur candidates "
        "(mace relax + chgnet relax + xtb GFN2 HOMO, then envelope_check.py Delaunay). "
        "Envelope adjudicator sanity: 82/82 of the hull's own points test inside their "
        "own Delaunay (find_simplex>=0), so the outside-test is well-conditioned and the "
        "verdicts are reliable (no degeneracy). All 10 candidates adjudicated in_envelope=false "
        "(outside). Funnel hard lines: HOMO<=-6.0 eV (all 10 pass), total energy<=0 eV "
        "(all 10 negative MACE energies), ML convergence both legs. Rejected(3): CF3-SF5, "
        "fluorosulfonyl isocyanate, thionyl tetrafluoride (ML not converged in >=1 leg). "
        "Rejected(2): cyanosulfonyl fluoride (HOMO -13.06) and sulfuryl chloride fluoride "
        "(HOMO -13.39) pass the -6.0 hard line but miss the -13.74 eV property window. "
        "Passed(5) advance to cell-level: bis(trifluoromethyl)sulfone HOMO -14.2961 (deepest, "
        "beats documented triflyl fluoride -14.1428), pentafluoroethylsulfonyl fluoride "
        "-14.2697, trifluoronitromethane -14.1208, sulfuryl fluoride -13.8919, "
        "trifluoroacetonitrile -13.8447. The two -14.27/-14.30 candidates exit the hull on "
        "the HOMO axis unambiguously (deeper than every one of the 82 documented points)."
    ),
}

with open(LOG, "a", encoding="utf-8") as f:
    f.write(json.dumps(funnel, ensure_ascii=False) + "\n")
    f.flush()

for r in rows:
    print(f"{r['name']:35s} HOMO {r['homo_ev']:8.4f}  k = {r['k_ms']:.6e} m/s")
