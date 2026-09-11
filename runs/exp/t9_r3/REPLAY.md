# T9 run 3 — reviewer replay guide

All commands run from `D:\research\degradation_prognostics\Battery_Design_Agent` with the
single environment `D:/anaconda/envs/py312/python.exe` (CUDA torch; required for run-comp).
`bda` CLI lives in `.claude/skills/virtual-battery-factory/scripts` (run `python -m bda`
from that directory).

## 1. Screening (run-comp)
```
cd .claude/skills/virtual-battery-factory/scripts
D:/anaconda/envs/py312/python.exe -m bda run-comp --in D:\...\runs\exp\t9_r3\in_batch1.json --out D:\...\runs\exp\t9_r3\out_batch1.json
D:/anaconda/envs/py312/python.exe -m bda run-comp --in D:\...\runs\exp\t9_r3\in_batch2.json --out D:\...\runs\exp\t9_r3\out_batch2.json
```
Finalist in batch 2: LiNi0.75Mg0.25PO4F -> realized {Ni: 6, Mg: 2},
avg_voltage_v = 5.51902, capacity_mah_g = 109.709, rel_stability = -1.2274.

## 2. Envelope adjudication (criterion 1+2, with fresh recompute)
```
cd D:\research\degradation_prognostics\Battery_Design_Agent
D:/anaconda/envs/py312/python.exe comp_envelope_check.py --known-set runs/exp/known_set_comp/known_set_v3.json --formula "LiNi0.75Mg0.25PO4F"
D:/anaconda/envs/py312/python.exe comp_envelope_check.py --known-set runs/exp/known_set_comp/known_set_v3.json --formula "LiNi0.875Mg0.125PO4F"
```
Outputs recorded verbatim in replay_envelope_finalist.json / replay_envelope_backup.json:
both `PASS (outside envelope)`. Batch-1 triples: adjudication_batch1.json.
Membership layer A0: `D:/anaconda/envs/py312/python.exe runs/exp/t9_r3/membership_check.py`.

## 3. Cell mapping (criterion 5)
```
D:/anaconda/envs/py312/python.exe runs/exp/t9_r3/cell_mapping.py
```
Constant OCP = 5.5190 V; capacity = 0.9 x computed = 98.738 mAh/g; SEI k0 = 1e-12 m/s
baseline; delivered 0.6194 Ah (expected 0.6194); terminal voltage 5.378-5.385 V;
ED_active = 544.9 mWh/g.

## 4. Public catalogues (criterion 6)
See catalogue_check.md: COD exact formula -> 0 entries; OQMD OPTIMADE HAS ALL
{Li,Ni,Mg,P,O,F} -> 0 of 1,407,395. Outcome: "not found in the searched scope".

## 5. QE endorsement (criterion 6, attempt)
```
cd .claude/skills/virtual-battery-factory/scripts
D:/anaconda/envs/py312/python.exe -m bda run-qe --in D:\...\runs\exp\t9_r3\in_qe_finalist.json --out D:\...\runs\exp\t9_r3\out_qe_finalist.json
```
(finalist only; Li-metal reference; SSSP efficiency pseudos; ecutwfc 50 Ry; nspin 2
ferromagnetic guess; full vc-relax + delithiated fixed-cell relax.)
Result recorded in out_qe_finalist.json on completion.

## 6. Report
FINAL_REPORT.md (this directory) and notes.md (working log).
