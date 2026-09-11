"""T9_R2: initialize log (entry 0 criteria + plan entry) and verify batch-1 formulas
against the known-set membership layer (A0 pre-check)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t9_r2", "runs")

entry0 = {
    "criteria": {
        "stage1": {
            "in_known": False,                      # A0: membership (comp_envelope_check --formula)
            "in_envelope": False,                   # A1: outside Delaunay hull of 96 sealed points
            "avg_voltage_v": {"min": 5.3},          # B: computed average voltage window (run-comp)
            "true_voltage_v": {"min": 5.3},         # B': true voltage (run-qe / literature), not computed-only
        },
        "stage2": {},                                # C: bridge rule - ED_active reported, not a criterion
        "stage3": {},
        "meta": {
            "task": "t9_r2 positive-electrode composition, Chen2020 NMC811/anode profile (cathode replaced, all else fixed)",
            "known_set": "runs/exp/known_set_comp/known_set_v2.json",
            "envelope_tool": "comp_envelope_check.py",
            "real_compute": True,                    # (D) requires run-qe at closing
            "frameworks_computable": ["layered LiMO2", "olivine LiMPO4", "spinel LiM2O4",
                                       "tavorite LiM(PO4)F", "tavorite LiM(SO4)F", "NASICON Li3M2(PO4)3"],
            "qe_elements": ["Li", "Ni", "Mn", "Co", "O", "P", "Si", "Mg"],
            "bridge_rule": "C: OCP=computed avg V (constant); capacity=0.90 x computed; SEI k0 baseline; ED_active=V*C*0.9 (reported)",
            "freedoms": "electrode composition ONLY (all other cell choices fixed)",
            "budget": "up to 3 run-comp batches (~24 candidates each); run-qe only for closing finalist",
        },
    }
}
if not (ws.path / "log.jsonl").exists():
    append_entry(ws, entry0)
    print("entry 0 written")
else:
    print("log.jsonl already exists - skipping entry 0 (resume)")

append_entry(ws, {
    "action": "plan",
    "objective_breakdown": "Single-criterion composition contract: A0 not documented; A1 outside hull; B computed avg V >= 5.3; B' true V >= 5.3 (QE-level or literature); C bridge (OCP=computed V, cap=0.9xC, k0 SEI, ED_active=V*C*0.9 reported); D closed-loop replay + run-qe + catalog check.",
    "candidate_strategy": "B-gate reachable only via CHGNet-inflated Ni environments or unvalidated templates: Ni-olivines (overestimate family; QE-able, B' via run-qe), tavorite-P Ni/Co/Mn/Cr/Cu (unvalidated template; B' literature-only - domain limit: no F pseudo in run-qe), plus spinel/NASICON completeness checks.",
    "budget_allocation": "3 run-comp batches; 1 run-qe closing finalist; web literature search for B' on tavorite-P; MP/catalog check at (D).",
    "risk_and_fallback": "R1 nothing computes >=5.3 -> honest negative; R2 only Ni-olivines compute >=5.3 and QE < 5.3 -> negative on B' with QE evidence; R3 QE overnight exceeds budget -> background run, record; R4 converged=false known screening behavior -> energies usable, annotate.",
    "detail": "design_plan.md",
})
print("plan entry written")

# A0 pre-check: membership layer
ks = json.loads(Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\known_set_comp\known_set_v2.json").read_text(encoding="utf-8"))
members = {c["formula"] for c in ks["membership"]}
print("membership size:", len(members), "n_points:", ks["n_points"])

batch1 = [
    # tavorite-P exploration (unvalidated template)
    "LiNiPO4F", "LiNi0.75Co0.25PO4F", "LiNi0.5Co0.5PO4F", "LiCoPO4F", "LiMnPO4F",
    "LiCrPO4F", "LiNi0.5Mn0.5PO4F", "LiNi0.5V0.5PO4F", "LiCuPO4F",
    # tavorite-S bound
    "LiNi0.75Co0.25SO4F", "LiNi0.5Co0.5SO4F", "LiCuSO4F",
    # olivine Ni-rich (overestimate family; QE-able)
    "LiNi0.8Co0.2PO4", "LiNi0.75Co0.25PO4", "LiNi0.6Co0.4PO4", "LiNi0.4Co0.6PO4",
    # spinel (QE-able; compute-low family - completeness)
    "LiCo2O4", "LiNi0.5Co1.5O4", "LiNiCoO4", "LiNi0.75Co1.25O4",
    # NASICON (QE-able but slow QE; unvalidated Ni template)
    "Li3Ni2(PO4)3", "Li3NiCo(PO4)3", "Li3Co2(PO4)3", "Li3Mn2(PO4)3",
]
print("batch1 size:", len(batch1))
bad = [f for f in batch1 if f in members]
print("A0 hits (documented, must drop):", bad if bad else "NONE - all clear")

# also check framework dispatch for every candidate
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent")
from comp_envelope_check import _resolve  # noqa: E402  (unused; keep import side-effect-free)
from bda.simulators.comp_runner import _framework
for f in batch1:
    print(f"  {f} -> {_framework(f)}")
