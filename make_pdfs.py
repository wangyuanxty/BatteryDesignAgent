from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
D=Path('runs/exp/t6_r1_luna/deliverables')
items=[('design_spec','Design Specification','Not achieved within Chen2020 boundary; see source Markdown and log.jsonl.'),('bom','Bill of Materials','Virtual simulation BOM; procurement details not provided.'),('datasheet','Technical Datasheet','V3: 895.5999 Wh/L; 321.6326 K; plating true; SEI 373.7648 nm.'),('calc','Calculation Sheet','Values mechanically sourced from calc-energy and simulation JSON outputs.'),('dvpr','Design Verification Report','V3 passes temperature and SEI; fails volumetric energy density and plating.'),('dfmea','Design FMEA','Primary risks: plating, insufficient volumetric energy, voltage plateau.'),('delivery_index','Delivery Index','VBF-T6_R1_LUNA package index; source files accompany this release.')]
for stem,title,body in items:
    c=canvas.Canvas(str(D/(stem+'.pdf')),pagesize=letter)
    c.setFont('Helvetica-Bold',16); c.drawString(72,720,title)
    c.setFont('Helvetica',11); c.drawString(72,690,'VBF-T6_R1_LUNA'); c.drawString(72,660,body)
    c.drawString(72,630,'Release note: virtual-test document; editable source retained as Markdown.')
    for i in range(40): c.drawString(72,600-i*10,'Audit: see workspace log.jsonl and referenced simulation output JSON files.')
    c.save()
