"""T10 v4 (t10_r4): write round-1 funnel entry into runs/exp/t10_r4/log.jsonl.

Mechanically rebuilt from r1_xtb.json (70 valid SMILES) + adjudication_r1.jsonl (16 both-window
passers adjudicated with envelope_check v2 pipeline) + the 2 SMILES dropped at RDKit validation.
Uses bda.store.append_entry (protocol-mandated log writer).
"""
import json
import sys
from pathlib import Path

REPO = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent")
sys.path.insert(0, str(REPO / ".claude/skills/virtual-battery-factory/scripts"))
sys.path.insert(0, str(REPO / "runs/exp/known_set_sei"))
from bda.store import CaseWorkspace, append_entry
from envelope_check import families_matched

WS = REPO / "runs/exp/t10_r4"
HOMO_MAX = -13.74
LUMO_MAX = -7.0

xtb = json.loads((WS / "candidates/r1_xtb.json").read_text(encoding="utf-8"))
adjud = [json.loads(l) for l in (WS / "adjudication_r1.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
adjud_ok = {r["smiles"]: r for r in adjud if "error" not in r}

DROPPED = [
    ("ClO3F", "chloryl fluoride", "dropped at SMILES validation: RDKit rejects (explicit valence for Cl, 7, exceeds permitted)"),
    ("IF7", "iodine heptafluoride", "dropped at SMILES validation: RDKit rejects (explicit valence for I, 7, exceeds permitted)"),
]

dispositions = []
n_pass = n_rej = 0
for c in xtb["candidates"]:
    smi = c["smiles"]
    m = c["metrics"]
    gate = families_matched(smi)
    if smi in adjud_ok:
        rec = adjud_ok[smi]
        status = "passed"
        n_pass += 1
        reason = ("adjudicated (envelope_check v2): in_envelope=%s families_matched=%s "
                  "mace_converged=%s chgnet_converged=%s" % (
                      rec["in_envelope"], rec["families_matched"],
                      rec["mace"]["converged"], rec["chgnet"]["converged"]))
    else:
        status = "rejected"
        n_rej += 1
        if gate:
            reason = "family gate matched: %s" % gate
        elif m["homo_ev"] > HOMO_MAX and m["lumo_ev"] > LUMO_MAX:
            reason = "xTB HOMO %.3f > %s and LUMO %.3f > %s" % (m["homo_ev"], HOMO_MAX, m["lumo_ev"], LUMO_MAX)
        elif m["homo_ev"] > HOMO_MAX:
            reason = "xTB HOMO %.3f > %s" % (m["homo_ev"], HOMO_MAX)
        else:
            reason = "xTB LUMO %.3f > %s (not reduction-first)" % (m["lumo_ev"], LUMO_MAX)
    dispositions.append({"smiles": smi, "status": status, "reason": reason})

for smi, name, why in DROPPED:
    dispositions.append({"smiles": smi, "name": name, "status": "rejected", "reason": why})
    n_rej += 1

entry = {
    "action": "funnel",
    "round": 1,
    "passed": n_pass,
    "rejected": n_rej,
    "disputed": 0,
    "detail": (
        "72 proposed; 2 dropped at RDKit SMILES validation (ClO3F, IF7 - explicit valence). 70 xTB-screened "
        "(GFN2-xTB, family gate + HOMO<=-13.74 + LUMO<=-7.0): 16 gate-clean passers of both windows; all 16 "
        "adjudicated with envelope_check v2 (MACE-MP medium + CHGNet + Delaunay hull over the 87-point known set + "
        "family gate): all converged, in_envelope=false, families_matched=[] -> 16 stage-1 passers. Finalist selected "
        "among them by cell margin + practicality: trifluoroacetic anhydride (TFAA, CAS 407-25-0)."
    ),
    "dispositions": dispositions,
}
append_entry(CaseWorkspace("exp/t10_r4", root="runs"), entry)
print("funnel entry appended: passed=%d rejected=%d dispositions=%d" % (n_pass, n_rej, len(dispositions)))
