# Append endorse + final entries to log.jsonl via bda.store.append_entry (protocol-mandated write path)
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r3", root=r"D:\research\degradation_prognostics\Battery_Design_Agent\runs")
print("workspace path:", ws.path)

# guard: never append if the closing entries already exist (resume-safe)
existing = [json.loads(l) for l in open(ws.path / "log.jsonl", encoding="utf-8") if l.strip()]
if not any(e.get("action") == "endorse" for e in existing):
    append_entry(ws, {
        "action": "endorse",
        "skipped": True,
        "reason": "real_compute=false (entry-0 meta): Stage-5 true DFT/MD endorsement (run-orca/run-md) not executed; no DFT/MD values fabricated. Design conclusions rest on PyBaMM DFN/SPMe cell-scale outputs (rounds 1-7) per protocol.",
        "candidates": [],
    })
    print("endorse entry appended (skip)")
else:
    print("endorse entry already exists - skipped")

if not any(e.get("action") == "final" for e in existing):
    final = {
        "action": "final",
        "verdict": "achieved",
        "recommendation": (
            "combo-v5-final (Chen2020 base + 8 overrides: pos r 2.5um, neg r 2.0um, sigma 1.7 S/m const, "
            "D 5e-10 m2/s, t+ 0.45, neg porosity 0.40, SEI k x0.2, SEI V_bar x0.5) meets ALL five contract criteria "
            "at DFN precision (round 7): ED 447.12 >= 327.18 Wh/kg; lowT retention 0.9957 >= 0.90; "
            "SEI@100 276.2 <= 500 nm; SEI@500 393.0 <= 550 nm; 4C@45C plating-free (anode_potential_v min +0.0443 V > 0). "
            "Aging kept SPMe per protocol standard (SEI params identical to DFN set). "
            "Deliverables: design_spec.md, bom.xlsx, datasheet.docx, calc.xlsx, dvpr.md, dfmea.md, delivery_index.md "
            "+ PDF releases in deliverables/. True DFT/MD endorsement skipped (real_compute=false, see endorse entry). "
            "Residual risks flagged in DFMEA: aged-cell 4C plating margin (+44 mV fresh), 4C heating at 45C ambient (+29.5 K, h=10), "
            "electrolyte oxidative stability unquantified (no Stage-2 molecules/DFT)."
        ),
    }
    append_entry(ws, final)
    print("final entry appended")
else:
    print("final entry already exists - skipped")
print("log entries now:", sum(1 for l in open(ws.path / "log.jsonl", encoding="utf-8") if l.strip()))