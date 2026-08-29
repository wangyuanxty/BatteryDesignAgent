# Correction entries: measurement-setup fix after first baseline run (append-only; entry 0 not overwritten).
from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r1", "runs")

plan_update = {
    "action": "plan",
    "update": True,
    "reason": (
        "Measurement-setup correction: the Chen2020 parameter-set default initial state was found "
        "empirically to be nearly charged (start OCV 4.036 V, 1C SPMe discharge capacity 4.95 Ah). "
        "OCP convention verified by evaluation: OCP_pos(1.0)=3.487 V (fully lithiated = low voltage), "
        "OCP_neg(0.03)=1.011 V. The planned fully-charged initial-concentration override was therefore "
        "unnecessary and is dropped; its first attempt additionally produced an IDA singularity at "
        "c_max and an infeasible-discharge step (V_init 2.48 V < 2.5 V), confirming both the "
        "convention and the edge-state pitfall. All discharge protocols now use the parameter-set "
        "default initial state; 5C retention = 5C capacity / 1C capacity on identical states."
    ),
    "candidate_strategy": "unchanged (round-1 baseline on defaults; round-2 single-lever variants)",
    "budget_allocation": "unchanged",
}

meta_correction = {
    "action": "criteria_meta_correction",
    "reason": "Empirical correction after first baseline run (raw 1C SPMe: V0=4.036 V, capacity 4.95 Ah)",
    "field": "meta.measurement_notes.discharge_initial_state",
    "original": (
        "Chen2020 initial state is discharged (positive electrode 27% lithiated, known artifact). "
        "1C/5C discharge protocols run with initial concentrations overridden to fully-charged state "
        "(pos=63104, neg=994 mol/m3) to measure nominal capacity from 100% SOC."
    ),
    "corrected": (
        "Chen2020 default initial state is nearly charged (positive electrode 27% lithiated = "
        "delithiated = high OCP; measured 1C discharge capacity from this state = 4.95 Ah). "
        "No initial-concentration override is used; all discharge protocols run with parameter-set "
        "defaults. Note: the default state covers cathode x in [0.27, 1.0] during discharge; the "
        "reported nominal capacity is the measured 1C discharge capacity from this state."
    ),
}

for e in (plan_update, meta_correction):
    append_entry(WS, e)
print("correction entries appended")
