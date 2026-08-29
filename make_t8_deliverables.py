from pathlib import Path
import json
import openpyxl
from reportlab.pdfgen import canvas
root=Path(r'D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t8_r1_luna'); d=root/'deliverables'; d.mkdir(exist_ok=True)
energy=json.loads((root/'cell/v5_energy.json').read_text(encoding='utf-8')); der=json.loads((root/'cell/v5_derived.json').read_text(encoding='utf-8')); base=json.loads((root/'cell/baseline_energy.json').read_text(encoding='utf-8'))
texts={
'design_spec':f'''# Cell Design Specification\n\n## Basic specification\n- System: Chen2020 baseline parameter set; architecture candidate TinySeparatorParticles.\n- Contract targets: energy density >=446.18 Wh/kg; 5C retention >=90%; cell mass <=0.040 kg.\n- Result: **not achieved**.\n\n## Performance verification\n| Metric | Value | Source | Result |\n|---|---:|---|---|\n| Energy density | {der["energy_density_wh_kg"]:.6f} Wh/kg | cell/v5_derived.json | FAIL |\n| Cell mass | {der["cell_mass_kg"]:.9f} kg | cell/v5_derived.json | FAIL |\n| 5C retention | {der["rate_retention_5C"]:.6f} | cell/v5_derived.json | FAIL |\n\nArchitecture parameters: separator 1 um; positive/negative particle radius 1 um. Electrolyte excluded from contract mass per calc-energy output. Dimensions and casing: Not provided.\n''',
'datasheet':f'''# Technical Datasheet\n\n| Field | Value | Source |\n|---|---|---|\n| Parameter set | Chen2020 | design_plan.md |\n| Rated 1C capacity | {energy["capacity_ah"]:.6f} Ah | cell/v5_energy.json |\n| Discharge energy | {energy["energy_wh"]:.6f} Wh | cell/v5_energy.json |\n| Energy density | {der["energy_density_wh_kg"]:.6f} Wh/kg | cell/v5_derived.json |\n| Contract mass | {der["cell_mass_kg"]:.9f} kg | cell/v5_derived.json |\n| 5C capacity retention | {der["rate_retention_5C"]:.6f} | cell/v5_derived.json |\n| Cycle life | Not simulated | protocol scope |\n| Safety threshold | Not supplied | task text |\n\nStatus: not achieved.\n''',
'dvpr':'''# Design Verification Plan and Report\n\nThe baseline and architecture candidates were run with DFN 1C and 5C protocols. `calc-energy` supplied contract mass and gravimetric energy. 5C retention was derived as same-parameter 5C capacity divided by 1C capacity. All three contractual criteria failed for the best tested candidate. The audit trail is `log.jsonl`; every proposed round has same-round mechanical evaluation entries.\n''',
'dfmea':'''# Design FMEA\n\n| Failure mode | Effect | Evidence/risk | Mitigation |\n|---|---|---|---|\n| High-rate polarization | 5C capacity loss | v5 retention 0.335044 | redesign chemistry/electrolyte and validate DFN |\n| Excess inactive mass | ED and mass failure | v5 mass 43.2168 g | higher-specific-energy system and packaging redesign |\n| Thin separator robustness | safety/manufacturing risk | 1 um is simulation candidate only | mechanical, short-circuit and process validation required |\n\nThis virtual FMEA is qualitative; abuse and manufacturing tests were not performed.\n'''
}
for n,t in texts.items():
 (d/(n+'.md')).write_text(t,encoding='utf-8')
 c=canvas.Canvas(str(d/(n+'.pdf')),pagesize=(612,792)); c.setFont('Helvetica',10); y=760
 for line in t.splitlines():
  if y<50: c.showPage(); y=760
  c.drawString(40,y,line[:105]); y-=13
 c.save()
for n,rows in {'bom':[('System','Chen2020','design_plan.md'),('Separator thickness',1e-6,'cell/v5_params.json'),('Positive particle radius',1e-6,'cell/v5_params.json'),('Negative particle radius',1e-6,'cell/v5_params.json'),('Status','Not achieved','log.jsonl')],'calc':[('Energy density Wh/kg',der['energy_density_wh_kg'],'cell/v5_derived.json'),('Mass kg',der['cell_mass_kg'],'cell/v5_derived.json'),('5C retention',der['rate_retention_5C'],'cell/v5_derived.json'),('1C energy Wh',energy['energy_wh'],'cell/v5_energy.json'),('Baseline ED Wh/kg',base['energy_density_wh_kg'],'cell/baseline_energy.json')]}.items():
 w=openpyxl.Workbook(); s=w.active; s.title='Source values'; s.append(['Item','Value','Source']); [s.append(list(r)) for r in rows]; w.save(d/(n+'.xlsx'))
 c=canvas.Canvas(str(d/(n+'.pdf')),pagesize=(612,792)); c.setFont('Helvetica',10); c.drawString(40,760,n+' — editable source retained as '+n+'.xlsx'); y=735
 for r in rows: c.drawString(40,y,str(r)[:110]); y-=14
 c.save()
idx='''# Delivery Index\n\n| File | Number | Format | Source note |\n|---|---|---|---|\n| design_spec.md/pdf | VBF-T8_R1_LUNA-DS-001 | Markdown/PDF | simulation outputs and log |\n| bom.xlsx/pdf | VBF-T8_R1_LUNA-BOM-001 | XLSX/PDF | parameter inputs |\n| datasheet.md/pdf | VBF-T8_R1_LUNA-DSH-001 | Markdown/PDF | simulation outputs |\n| calc.xlsx/pdf | VBF-T8_R1_LUNA-CALC-001 | XLSX/PDF | calc-energy and derived retention |\n| dvpr.md/pdf | VBF-T8_R1_LUNA-DVPR-001 | Markdown/PDF | audit trail |\n| dfmea.md/pdf | VBF-T8_R1_LUNA-DFMEA-001 | Markdown/PDF | qualitative engineering analysis |\n\nStatus: negative result; no CAD model requested.\n'''
(d/'delivery_index.md').write_text(idx,encoding='utf-8'); c=canvas.Canvas(str(d/'delivery_index.pdf')); c.setFont('Helvetica',10); c.drawString(40,760,'VBF-T8_R1_LUNA delivery index'); c.drawString(40,740,'Negative result; source files and PDF releases listed in delivery_index.md'); c.save()
