"""Round-4 audit entries: propose + funnel + eval batch (canonical workspace).

Callers: this session only (run once via .venv python).
Writes: appends 2 entries to runs/exp/c1_t1_r1/log.jsonl via bda.store.append_entry,
        and writes runs/exp/c1_t1_r1_leak/work/eval_batch_r4.json
        (list of {'candidate','outputs','note'} for `bda log-evaluate --batch-file`).
"""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace('exp/c1_t1_r1', 'runs')
LEAK_WORK = Path('D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/c1_t1_r1_leak/work')

append_entry(WS, {
    "action": "propose", "round": 4, "stage": 3,
    "candidates": [
        {"name": "R4-V1-cool", "params": "work/params/r4_v1_cool.json",
         "rationale": "R3-V2-tpt + cooling h 30->100 (fix 4C T_max overshoot)"},
        {"name": "R4-V2-coolfull", "params": "work/params/r4_v2_coolfull.json",
         "rationale": "R3-V3-full + cooling h=100"},
        {"name": "R4-V3-margin", "params": "work/params/r4_v3_margin.json",
         "rationale": "R3-V2-tpt + h=100 + transport margin kit: t+ 0.6->0.7, D_e 1e-9->2e-9, kappa 2.0->3.0, negative radius 4->3um"},
        {"name": "R4-V4-coolmax", "params": "work/params/r4_v4_coolmax.json",
         "rationale": "R3-V3-full + h=150 (test cooling ceiling / kinetics trade-off)"},
    ],
})

append_entry(WS, {
    "action": "funnel", "round": 4, "stage": 4,
    "observations": [
        {"metric": "plated",
         "finding": "h=100 keeps plating suppressed: R4-V1-cool anode_min +0.0247 V, R4-V3-margin +0.0503 V, R4-V2-coolfull +0.0015 V; h=150 (R4-V4-coolmax) drops anode_min to -0.0006 V -> plated again (cooler cell slows kinetics) - cooling-kinetics trade-off confirmed",
         "evidence": "cell/r4_v*_4c45c_spme.json anode_potential_v"},
        {"metric": "T_max_K",
         "finding": "4C T_max: V1 325.08 / V2 324.17 / V3 323.98 / V4 322.38 K, all <= 333.15; h=100 sufficient",
         "evidence": "cell/r4_v*_4c45c_spme.json T_max_K"},
        {"metric": "energy_density_wh_kg",
         "finding": "ED: V1 499.4 / V2 555.9 / V3 502.7 / V4 556.1 Wh/kg, all >= 392.61",
         "evidence": "cell/r4_v*_energy.json"},
        {"metric": "triggered",
         "finding": "overcharge to 4.70 V reached; run-tr coupling: V1 and V3 triggered=false, TR T_max 299.42/299.45 K",
         "evidence": "validation/r4_v*_tr.json"},
    ],
    "conclusion": "R4-V1-cool and R4-V3-margin pass ALL criteria; R4-V3-margin selected as champion (better plating margin +50 mV and lower T_max); R4-V2-coolfull passes but thin plating margin (+1.5 mV) rejected",
})

def rel(p):
    return 'runs/exp/c1_t1_r1/cell/' + p

def relv(p):
    return 'runs/exp/c1_t1_r1/validation/' + p

batch_r4 = [
    {"candidate": "R4-V1-cool",
     "outputs": [rel('r4_v1_cool_1c_spme.json'), rel('r4_v1_cool_energy.json'), rel('r4_v1_cool_4c45c_spme.json'),
                 rel('r4_v1_cool_overcharge_spme.json'), relv('r4_v1_cool_tr.json')],
     "note": "full stage-3+4 evidence; T_max_K last-wins from TR file"},
    {"candidate": "R4-V2-coolfull",
     "outputs": [rel('r4_v2_coolfull_1c_spme.json'), rel('r4_v2_coolfull_energy.json'), rel('r4_v2_coolfull_4c45c_spme.json')],
     "note": "stage-3 evidence; triggered unchecked (TR not run for this variant)"},
    {"candidate": "R4-V3-margin",
     "outputs": [rel('r4_v3_margin_1c_spme.json'), rel('r4_v3_margin_energy.json'), rel('r4_v3_margin_4c45c_spme.json'),
                 rel('r4_v3_margin_overcharge_spme.json'), relv('r4_v3_margin_tr.json')],
     "note": "full stage-3+4 evidence; T_max_K last-wins from TR file"},
    {"candidate": "R4-V4-coolmax",
     "outputs": [rel('r4_v4_coolmax_1c_spme.json'), rel('r4_v4_coolmax_energy.json'), rel('r4_v4_coolmax_4c45c_spme.json')],
     "note": "stage-3 evidence; triggered unchecked (TR not run for this variant)"},
]
(LEAK_WORK / 'eval_batch_r4.json').write_text(json.dumps(batch_r4, ensure_ascii=False, indent=2), encoding='utf-8')
print('appended 2 entries + wrote eval_batch_r4.json')
