"""Plan-update: D_ec iterative correction (trigger: simulation overturned estimate)."""
import json
from pathlib import Path

CASE = Path("runs/exp/t2_r1_singlemodel")
LOG = CASE / "log.jsonl"

update = {
    "action": "plan",
    "update": True,
    "reason": (
        "simulation overturns the R3 propose D_ec estimate twice (trigger 3, "
        "key assumption vs measurement): R3 propose shipped D_ec 1e-18 m2/s "
        "(predicted SEI500 ~550 nm from baseline scaling); DFN aging measured "
        "585.18 nm @100cyc and 1083.29 nm @500cyc -> FAIL. Correction to "
        "2e-19 (10x denser film) measured 272.64 nm @100cyc (PASS, <=500) but "
        "611.79 nm @500cyc (FAIL, 11% over 550). Measured sensitivity exponent "
        "ln(1083.29/611.79)/ln(5) = 0.355 at 500cyc (transitional regime, "
        "k-mixing), ln(585.18/272.64)/ln(5) = 0.475 at 100cyc (~diffusion-"
        "limited). Final correction D_ec 2e-19 -> 8e-20 m2/s (denser additive-"
        "derived SEI, solvent permeation cut 25x vs baseline 2e-18); predicted "
        "SEI500 465-509 nm by exponent bounds 0.2-0.3 (worst-case still under "
        "550), SEI100 ~180-200 nm. D_ec is only used by the SEI-growth model "
        "(ec reaction limited), so 1C/4C/lowT/energy results are unchanged "
        "(verified identical across the two edits)."
    ),
    "candidate_strategy": (
        "unchanged R3 final design (neg 250 um / pos 100 um / radii 3.5/3.0 um "
        "/ neg i0 2.0 A/m2 / SEI pack k 3e-13 + i0 7.5e-8) with the only "
        "revision: EC diffusivity 8e-20 m2/s (film-property extension of the "
        "SEI-suppression bridge, honest estimate, recorded)."
    ),
    "budget_allocation": (
        "one more aging rerun (100+500, D_ec=8e-20, DFN) in background; "
        "meanwhile Stage 4 safety: overcharge + run-tr on the final design, "
        "then R3 evaluate (all criteria), then closing."
    ),
}

with LOG.open("a", encoding="utf-8") as f:
    f.write(json.dumps(update, ensure_ascii=False) + "\n")
print("appended plan-update (D_ec correction)")

# design_plan.md revision history
plan = CASE / "design_plan.md"
rev = (
    "\n\n## Revision history\n"
    "- R3 (post-evaluate): D_ec estimate 1e-18 -> 2e-19 -> final 8e-20 m2/s; "
    "DFN aging measured 585.18/1083.29 nm (1e-18) and 272.64/611.79 nm (2e-19); "
    "500cyc still over -> final 8e-20 with measured-exponent-bounded prediction "
    "465-509 nm @500cyc. All non-aging results unchanged.\n"
    "- R3 (pre-evaluate): SPMe unphysical c_e for thick anodes -> DFN adopted; "
    "neg i0 = 2.0 A/m2 decisive for 4C plating; SEI growth diffusion-limited "
    "-> D_ec is the SEI500 lever.\n"
)
with plan.open("a", encoding="utf-8") as f:
    f.write(rev)
print("appended design_plan.md revision history")
