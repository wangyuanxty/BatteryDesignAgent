"""t9_r4 closing deliverables: 7 document types (md source + PDF), honest negative result.

Files land in runs/exp/t9_r4/deliverables/ with names starting with the type key
(verify-deliverables: prefix match + VBF numbering in the index).
"""
import json
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent  # runs/exp/t9_r4
DLV = ROOT / "deliverables"

TITLE = "t9_r4 - grid-storage cell cathode on the Chen2020 NMC811/graphite profile"
STATUS = "Result: HONEST NEGATIVE (no candidate satisfies the full contract; nothing reported as passing)"

DOCS = {
    "design_spec": f"""# VBF-T9R4-DS-001 Design Specification

{TITLE}
{STATUS}

Objective: design a cathode composition (the only free variable) for a grid-storage cell on the
Chen2020 NMC811/graphite profile. Electrolyte (EC/EMC + LiPF6, anodic limit 4.8 V) and cell
architecture are fixed. Contract criteria (pre-registered in log.jsonl entry 0):

- stage1: CHGNet-computed average voltage >= 4.6 V (run-comp)
- stage1: charging potential <= 4.8 V (computed incremental profile into the top-of-charge state)
- stage1: not in the 115-material catalogue; outside the 102-point hull (comp_envelope_check.py)
- stage1: one of the six supported families (layered/olivine/spinel/tavorite-P/tavorite-S/NASICON)
- stage2: energy density >= 327.18 Wh/kg at 1C (calc-energy convention); report ED_active = V x C x 0.9
- stage3: no Li plating at 4C/45C; no thermal-runaway trigger; SEI <= 500 nm after 100 x 1C
- guard: true voltage >= 4.6 V beyond the screening proxy (experimental/QE/literature-consistent)

Mapping rule (fixed): constant OCP = computed average voltage; capacity = 0.9 x computed capacity;
SEI kinetics = Chen2020 baseline k0.

Design evolution: rounds 1-2 mapped the layered voltage envelope (TM-redox band 2.56-3.99 V;
d0/d10 O-redox line 4.25-4.60 V). Round 3 found the only window pass in 42 candidates:
AlB55 (LiAl0.5B0.5O2) at 4.6413 V. Round 4 (charging-potential gate) rejected it: the last
charge step (x: 0.4 -> 0.3) costs 7.410 V - incompatible with the 4.8 V electrolyte. The window
pass was an artifact of a pathological x=0.3 endpoint, fatal for the whole d0/d10 line.

Decisive negative walls:
(i) TM-redox layered voltage caps at ~4.0 V (NiFe55 3.990; known-set max ~4.03 V).
(ii) The only >4.6 V layered mechanism (d0 O-redox) intrinsically ends with a >4.8 V final
    charge step (measured 7.41 V).
(iii) Non-layered families are ED-infeasible under the 0.9-capacity rule (<= ~322 Wh/kg even
    at 4.8 V; LiNiPO4 at true 5.1 V ~ 317 Wh/kg < 327.18).

The specification is therefore recorded as NOT ACHIEVED within the six supported families.""",
    "bom": f"""# VBF-T9R4-BOM-001 Bill of Materials

{TITLE}
{STATUS}

Fixed cell stack (Chen2020 baseline, unchanged by design - the cathode composition is the only
free variable):

| Item | Specification | Source |
|---|---|---|
| Positive current collector | Al, 16 um | Chen2020 |
| Negative current collector | Cu, 12 um | Chen2020 |
| Positive electrode coating | 75.6 um, eps_am 0.665, rho 3262 kg/m3 (NMC811 baseline) | Chen2020 |
| Negative electrode | 85.2 um, eps_am 0.75, graphite rho 1657 kg/m3 | Chen2020 |
| Separator | 12 um, porosity 0.47 | Chen2020 |
| Electrolyte | EC/EMC + LiPF6 (anodic limit 4.8 V) - FIXED | contract |
| Cathode active material | NOT RESOLVED - no candidate passed; screening space: 42 layered LiMO2 compositions | negative result |
| Electrode area | 0.1027 m2 (0.065 x 1.58 m); nominal 5.0 Ah | Chen2020 |

Screened cathode-active candidates (3 run-comp batches, all layered LiMO2 prototypes):
round 1: LiCuO2, LiFeO2, CuNi55, CuMn55, CuFe55, CuCo55, NiFe55, CoFe55, FeMn55, LiVO2,
CuAl91, CuZr91, CuMn73, CuNi82; round 2: LiScO2, LiAlO2, LiGaO2, LiZnO2, FeNi73, FeNi37,
CrFe55, CrNi55, CrCo55, FeCo91, NiFe91, FeNi91, ZnNi55, ScFe55; round 3: LiBO2, AlB55, AlB73,
AlB91, BAl73, BAl91, AlB82, AlB64, AlB95, GaAl55, AlSc55, BGa55, BSc55, GaAl91.
All rejected (window, compatibility, or both).""",
    "datasheet": f"""# VBF-T9R4-DSH-001 Datasheet (Target vs Measured)

{TITLE}
{STATUS}

| Criterion | Threshold | Best measured | Verdict |
|---|---|---|---|
| Computed avg voltage | >= 4.6 V | 4.6413 V (AlB55) | window pass, then REJECTED on compatibility |
| Charging potential | <= 4.8 V | 7.410 V (AlB55, V(0.4->0.3)) | FAIL - decisive |
| Catalogue exclusion | not of 115 | PASS (outside envelope) | pass |
| Hull exclusion | outside 102-point hull | PASS (outside envelope) | pass |
| Supported family | six families | layered LiMO2 | pass |
| Energy density 1C | >= 327.18 Wh/kg | not reached (no survivor to stage 3) | n/a |
| ED_active report | V x C x 0.9 | AlB55: 4.6413 x 324.38 x 0.9 = 1355 (Wh/kg-active, informative only) | n/a |
| 4C/45C plating | none | not reached | n/a |
| Thermal runaway | no trigger | not reached | n/a |
| SEI @100 x 1C | <= 500 nm | not reached (baseline Chen2020 ~449 nm signal) | n/a |
| True-voltage guard | >= 4.6 beyond proxy | envelope re-computation 4.6354 V (independent run) | informative |

Overall: NOT ACHIEVED. The only window-passer fails the electrolyte compatibility limit by
2.6 V; no candidate passes both stage-1 co-gates, so stages 2-4 were never reached.""",
    "calc": f"""# VBF-T9R4-CALC-001 Calculation Record (decisive numbers)

{TITLE}

ED feasibility (binds the family choice):
- Chen2020 positive active mass M_am = 75.6e-6 x 0.1027 x 0.665 x 3262 = 16.84 g.
- calc-energy total mass = 43.45 g (porosity-corrected layers, no electrolyte).
- Baseline 1C discharge measured 4.948 Ah / 17.39 Wh -> ED 400.29 Wh/kg.
- Family capacity bounds (C = 0.7 x F/3.6 / MW): layered 180-285, olivine <= 128, spinel <= 113,
  tavorites <= 111, NASICON <= 46 mAh/g.
- Non-layered ED under the 0.9 rule: olivine at 4.8 V/128 mAh/g ~ 322 Wh/kg; LiNiPO4 at its
  true 5.1 V ~ 317 Wh/kg - both < 327.18 -> only layered LiMO2 can pass (ED ~ 445-465 Wh/kg).
- Plateau-OCP mapped discharge is anode-limited (~5.1 Ah, LNMO.json precedent): ED ~ 450-500
  Wh/kg for any layered at 4.6-4.8 V -> the binding constraint is the computed voltage itself.

Voltage screening (run-comp CHGNet, bcc Li reference e_li = -1.87848 eV):
- TM-redox layered band: 2.56-3.99 V (42-candidate sweep + known set; NiFe55 3.990 max).
- d0/d10 O-redox line: LiScO2 4.298, LiGaO2 4.479, LiZnO2 4.492, LiAlO2 4.598, AlB55 4.641,
  BGa55 4.504, GaAl55 4.494, LiBO2 4.253.

Charging-potential gate (comp/gate_charging.py, same machinery/seed; nested removal order):
- V(0.4 -> 0.3) = -(E(0.4) - E(0.3) - 1 x e_li) / 1
- E(0.4) = -295.256 eV (gate relaxation), E(0.3) = -285.968 eV (batch3), e_li = -1.878 eV
- charging_potential_v = 7.410 V >> 4.8 V -> FAIL. The x=0.3 endpoint sits ~9 eV off its
  composition neighbors; the 50:50 avg peak was this artifact's signature.

Capacity proxy: C = 0.7 x 26801.481 / MW. AlB55: MW 82.57 -> 324.38 mAh/g.
Relaxed-cell density (gate full state): 2.836 g/cm3 (relaxed-final-structure).""",
    "dvpr": f"""# VBF-T9R4-DVPR-001 Design Verification Plan & Results

{TITLE}
{STATUS}

| # | Requirement | Method | Result | Verdict |
|---|---|---|---|---|
| 1 | avg voltage >= 4.6 V | run-comp x3 batches (42 layered) | max 4.6413 V (AlB55) | pass for AlB55 only |
| 2 | charging potential <= 4.8 V | gate_charging.py incremental profile | 7.410 V | FAIL (decisive) |
| 3 | catalogue/hull exclusion | comp_envelope_check.py --formula/--point | PASS (outside envelope) | pass |
| 4 | supported family | run-comp strict dispatch | layered LiMO2 | pass |
| 5 | ED >= 327.18 Wh/kg | run-pyamm 1C + calc-energy | not reached (no survivor) | n/a |
| 6 | no plating 4C/45C | run-pyamm 4C_charge_45C --plating | not reached | n/a |
| 7 | no TR trigger | run-tr | not reached | n/a |
| 8 | SEI <= 500 nm @100cyc | run-pyamm aging_1C_100cyc | not reached | n/a |
| 9 | true voltage >= 4.6 V | envelope re-compute + literature | 4.6354 V independent re-compute | informative |

Verification closure: the mechanical audit chain is complete (log.jsonl: entry 0 criteria,
plan, 4 propose rounds each with same-round evaluate entries, 4 funnels, final entry).
close-loop: run-comp replay (envelope --formula re-computation, 4.6354 V) + public-catalogue
search (no results for LiAl0.5B0.5O2 / LiAlO2 cathodes - 'not found in the searched scope').
run-qe not performed: no candidate survived to Stage 5 (Al/B pseudopotentials were added to
the QE map in preparation; recorded honestly).""",
    "dfmea": f"""# VBF-T9R4-DFMEA-001 Failure Modes & Effects (design phase)

{TITLE}
{STATUS}

| Failure mode | Effect | Cause | S | O | D | Mitigation / outcome |
|---|---|---|---|---|---|---|
| d0/d10 O-redox top-of-charge pathology | charging potential far above the electrolyte anodic limit | pathological x=0.3 endpoint (last Li in a deep trap; ~9 eV off-trend) | 10 | 8 | 3 | MEASURED: AlB55 7.410 V -> line abandoned |
| Avg-voltage artifact (sharp 50:50 peak) | false window pass | unstable delithiated state inflates the average | 8 | 6 | 3 | Detected by the incremental-profile co-gate before any cell work |
| TM-redox layered voltage cap ~4.0 V | window unreachable | 3d redox levels of the family | 8 | 8 | 2 | Envelope documented across 42 candidates |
| Non-layered ED infeasibility | ED < 327.18 under the 0.9-capacity rule | capacity bounds of olivine/spinel/tavorite/NASICON | 8 | 7 | 2 | Decisive calc: only layered can pass |
| Relaxation non-convergence (fmax 0.1/300 steps) | mV-level noise in voltages | FIRE step budget; universal in this machinery | 2 | 8 | 1 | Reproducibility checked: independent re-compute within 6 mV |
| Overestimate-prone family claims | guard failure | Ni-rich olivine inflation (LiNiPO4 7.016 vs 5.1) | 6 | 5 | 2 | Not used; layered family self-calibrates (NMC811 3.80 vs 3.8) |
| Session/background loss | compute lost | harness kills background tasks at turn end | 4 | 6 | 2 | Checkpointed gate script (one state per blocking call) |

Residual risk accepted: none - the negative result is over-determined by walls (i) and (ii),
independent of relaxation noise.""",
    "delivery_index": f"""# VBF-T9R4-IDX-001 Delivery Index

{TITLE}
{STATUS}

VBF numbering list:
- VBF-T9R4-DS-001 design_spec (design specification, negative result)
- VBF-T9R4-BOM-001 bom (bill of materials, fixed stack + screening space)
- VBF-T9R4-DSH-001 datasheet (target vs measured, NOT ACHIEVED)
- VBF-T9R4-CALC-001 calc (decisive calculations)
- VBF-T9R4-DVPR-001 dvpr (verification plan & results)
- VBF-T9R4-DFMEA-001 dfmea (failure modes & effects)
- VBF-T9R4-IDX-001 delivery_index (this file)

Audit trail: runs/exp/t9_r4/log.jsonl (entry 0 criteria; plan; rounds 1-4 propose/funnel/
evaluate; final entry, verdict: negative). Simulation outputs under comp/ and cell/.
Report: runs/exp/t9_r4/report.html.""",
}


def md_to_pdf(md_path: Path, pdf_path: Path) -> None:
    styles = getSampleStyleSheet()
    body = styles["Normal"]
    body.fontSize = 8.5
    body.leading = 11
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm)
    story = []
    for line in Path(md_path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            story.append(Spacer(1, 4))
            continue
        text = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if line.startswith("#"):
            story.append(Paragraph(f"<b>{text.lstrip('# ')}</b>", body))
        else:
            story.append(Paragraph(text, body))
    doc.build(story)


def main():
    for key, content in DOCS.items():
        md_path = DLV / f"{key}.md"
        pdf_path = DLV / f"{key}.pdf"
        md_path.write_text(content, encoding="utf-8")
        md_to_pdf(md_path, pdf_path)
        print(f"wrote {key}.md ({len(content)} chars) + {key}.pdf ({pdf_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
