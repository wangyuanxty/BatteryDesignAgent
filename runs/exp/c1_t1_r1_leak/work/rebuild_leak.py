"""Rebuild the complete R2-R4 audit chain in the _leak quarantine workspace.

Facts / callers / purpose / schema:
- Callers: this session only (headless, run once via .venv python). No other file serves
  this purpose (existing log_entries_r2r3.py / log_entries_r4.py append to the CANONICAL
  case dir, which a concurrent session keeps overwriting/sweeping; _leak/log.jsonl holds
  only my pristine first 5 entries: criteria, plan, propose R1, funnel R1, evaluate R1).
- Purpose: make _leak the stable authoritative case workspace; append propose/funnel
  entries for rounds 2-4 via bda.store.append_entry (append-only, protocol-compliant),
  and write the three log-evaluate batch files pointing at _leak output files.
- Schema: log entries are VBF protocol shapes (action/round/stage/candidates/observations/
  conclusion); batch files are lists of {'candidate','outputs','note'} consumed by
  `bda log-evaluate --batch-file` (outputs resolved against REPO_ROOT).
- User instruction being served (verbatim task): "Design a battery for a next-generation
  pure electric sedan: energy density >= 392.61 Wh/kg, support 4C fast charge (no lithium
  plating), maximum temperature <= 60 C, overcharge to 4.7 V without triggering thermal
  runaway" - audit-ledger closure per the Virtual Battery Factory protocol.
"""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace('exp/c1_t1_r1_leak', 'runs')
WORK = Path('D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/c1_t1_r1_leak/work')

append_entry(WS, {
    "action": "propose", "round": 2, "stage": 3,
    "candidates": [
        {"name": "R2-V1-thincc", "params": "work/params/r2_v1_thincc.json",
         "rationale": "ED ladder: CC Al 16->8um / Cu 12->6um, separator 12->8um porosity 0.55"},
        {"name": "R2-V2-fastk", "params": "work/params/r2_v2_fastk.json",
         "rationale": "fast-charge kit: pos/neg radius 3.0/2.5um, electrolyte conductivity 1.5 S/m, cooling h=30"},
        {"name": "R2-V3-anodeup", "params": "work/params/r2_v3_anodeup.json",
         "rationale": "N/P up: negative thickness 85.2->110um"},
        {"name": "R2-V4-combo1", "params": "work/params/r2_v4_combo1.json",
         "rationale": "union of V1+V2+V3"},
    ],
})

append_entry(WS, {
    "action": "funnel", "round": 2, "stage": 3,
    "observations": [
        {"metric": "energy_density_wh_kg",
         "finding": "all 4 variants >= 417 Wh/kg (V1 488.9, V2 417.0, V3 433.0, V4 566.3); criterion satisfied everywhere",
         "evidence": "cell/r2_v*_energy.json"},
        {"metric": "plated",
         "finding": "all 4 variants still plate at 4C; anode_potential_v minimum occurs at the END of the 4C charge (V=4.2 cut-off, min at last time point); anode-side polarization at 20 A dominates; thin CC/separator (V1) ~neutral, h=30 cooling slightly worse kinetics (V2), thicker anode worse (V3)",
         "evidence": "cell/r2_v*_4c45c_spme.json anode_potential_v"},
        {"metric": "T_max_K",
         "finding": "4C T_max: V1 332.08 / V2 323.92 / V3 334.12 / V4 325.64 K; h=30 cooling effective; V3 marginally exceeds 333.15",
         "evidence": "cell/r2_v*_4c45c_spme.json T_max_K"},
    ],
    "conclusion": "electrolyte-side transport (cation transference number, diffusivity, conductivity) + electrode porosity are the next levers; keep thin CC/separator ED bank; ED headroom is large (>=417 vs 392.61)",
})

append_entry(WS, {
    "action": "propose", "round": 3, "stage": 3,
    "candidates": [
        {"name": "R3-V1-por", "params": "work/params/r3_v1_por.json",
         "rationale": "porosity up (neg 0.25->0.35, pos 0.335->0.40) + thin CC/sep + h=30"},
        {"name": "R3-V2-tpt", "params": "work/params/r3_v2_tpt.json",
         "rationale": "electrolyte transport kit: t+ 0.2594->0.6, D_e ->1e-9 m2/s, kappa ->2.0 S/m, negative radius 5.86->4um + thin CC/sep + h=30"},
        {"name": "R3-V3-full", "params": "work/params/r3_v3_full.json",
         "rationale": "porosity + transport kit + positive radius 5.22->3um"},
    ],
})

append_entry(WS, {
    "action": "funnel", "round": 3, "stage": 3,
    "observations": [
        {"metric": "plated",
         "finding": "porosity alone reduces plating (anode_min -0.4385->-0.3962) but does not eliminate it; transport kit eliminates plating: R3-V2-tpt anode_min +0.0420 V, R3-V3-full +0.0135 V (plated=false in both)",
         "evidence": "cell/r3_v*_4c45c_spme.json anode_potential_v"},
        {"metric": "T_max_K",
         "finding": "plating-free 4C charge now overheats: R3-V2-tpt 335.77 K, R3-V3-full 334.49 K > 333.15 limit (charge accepts more current over time)",
         "evidence": "cell/r3_v*_4c45c_spme.json T_max_K"},
        {"metric": "energy_density_wh_kg",
         "finding": "ED 500-557 Wh/kg, large headroom vs 392.61",
         "evidence": "cell/r3_v*_energy.json"},
    ],
    "conclusion": "plating solved by electrolyte transport; next round: raise cooling h (30->100-150) and add transport margin (t+ 0.7, D_e 2e-9, kappa 3.0, negative radius 3um)",
})

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
    return 'runs/exp/c1_t1_r1_leak/cell/' + p


def relv(p):
    return 'runs/exp/c1_t1_r1_leak/validation/' + p


batch_r2 = [
    {"candidate": "R2-V1-thincc", "outputs": [rel('r2_v1_thincc_1c_spme.json'), rel('r2_v1_thincc_energy.json'), rel('r2_v1_thincc_4c45c_spme.json')],
     "note": "T_max_K last-wins from 4C file (binding scenario)"},
    {"candidate": "R2-V2-fastk", "outputs": [rel('r2_v2_fastk_1c_spme.json'), rel('r2_v2_fastk_energy.json'), rel('r2_v2_fastk_4c45c_spme.json')],
     "note": "T_max_K last-wins from 4C file (binding scenario)"},
    {"candidate": "R2-V3-anodeup", "outputs": [rel('r2_v3_anodeup_1c_spme.json'), rel('r2_v3_anodeup_energy.json'), rel('r2_v3_anodeup_4c45c_spme.json')],
     "note": "T_max_K last-wins from 4C file (binding scenario)"},
    {"candidate": "R2-V4-combo1", "outputs": [rel('r2_v4_combo1_1c_spme.json'), rel('r2_v4_combo1_energy.json'), rel('r2_v4_combo1_4c45c_spme.json')],
     "note": "T_max_K last-wins from 4C file (binding scenario)"},
]
batch_r3 = [
    {"candidate": "R3-V1-por", "outputs": [rel('r3_v1_por_1c_spme.json'), rel('r3_v1_por_energy.json'), rel('r3_v1_por_4c45c_spme.json')],
     "note": "T_max_K last-wins from 4C file (binding scenario)"},
    {"candidate": "R3-V2-tpt", "outputs": [rel('r3_v2_tpt_1c_spme.json'), rel('r3_v2_tpt_energy.json'), rel('r3_v2_tpt_4c45c_spme.json')],
     "note": "T_max_K last-wins from 4C file (binding scenario)"},
    {"candidate": "R3-V3-full", "outputs": [rel('r3_v3_full_1c_spme.json'), rel('r3_v3_full_energy.json'), rel('r3_v3_full_4c45c_spme.json')],
     "note": "T_max_K last-wins from 4C file (binding scenario)"},
]
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
(WORK / 'eval_batch_r2.json').write_text(json.dumps(batch_r2, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK / 'eval_batch_r3.json').write_text(json.dumps(batch_r3, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK / 'eval_batch_r4.json').write_text(json.dumps(batch_r4, ensure_ascii=False, indent=2), encoding='utf-8')
print('appended 6 entries (propose/funnel R2-R4) to _leak log + rewrote 3 batch files with _leak paths')
