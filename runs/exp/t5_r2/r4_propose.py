"""Round-4 propose entry (t5_r2): thermal management candidates on the e2 (plating-free) platform.

Parameter list BEFORE running (units + sources):
  - Total heat transfer coefficient [W.m-2.K-1] = 40 / 50 / 80 (baseline contract default 10).
    Design choice in the thermal-management freedom; value range anchored to liquid-cooled EV pack
    channel/immersion heat-transfer coefficients (domain experience, no precise source).
  - t4 additionally: Positive electrode porosity 0.40->0.43, Negative 0.35->0.40 (further ohmic-heat
    relief + mass cut; watched for capacity delivery).

Reasoned-out lever (recorded, no sim wasted): electrode-area scaling was rejected - contract ED mass
scales with area at fixed areal loading, so spreading the same 6.5 Ah over a larger area halves ED.
"""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

append_entry(ws, {
    "action": "propose",
    "round": 4,
    "candidates": [
        {"name": "e2_h40", "role": "e2 platform + cooling h 40 W/m2K (liquid-channel class); steady-state rise estimate ~12 K (est) - first T_max pass attempt"},
        {"name": "e2_h50", "role": "e2 platform + cooling h 50 W/m2K; more margin on the 15 K budget"},
        {"name": "e2_h80", "role": "e2 platform + cooling h 80 W/m2K (immersion-class); high-margin arm"},
        {"name": "e2_por43_h50", "role": "e2 + porosity pos 0.43 / neg 0.40 + h 50; cuts ohmic heat at source AND boosts ED margin"},
    ],
    "llm_reason": (
        "Round-3 e2 = first plating-free variant (ap_min +0.0138 V, ED 571.82); only failing metric is "
        "T_max 367.45 K = 49.3 K rise at contract-default h=10 (evidence: round-3 evaluate). "
        "Fallback routing: failure lives at Stage 3 thermal scale -> thermal-management lever (h), "
        "with one heat-source-reduction variant. All four are measured as full triads."
    ),
})
print("propose round 4 appended")