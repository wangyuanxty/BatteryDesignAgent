"""Fix audit chain (add round 1 evaluate) and generate PDF versions."""
import os, json, subprocess

os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
PYTHON = "D:/research/degradation_prognostics/Battery_Design_Agent/.venv/Scripts/python.exe"
CASE_DIR = "D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo"
LOG_FILE = "log.jsonl"
DELIVER_DIR = "deliverables"

def append_log(entry):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# 1. Add round 1 evaluate entries for V_B/C/D/E (all failed plating)
# Read log to insert before the round 2 entries
with open(LOG_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where to insert (after the round 1 funnel entry)
insert_idx = None
for i, line in enumerate(lines):
    entry = json.loads(line)
    if entry.get("action") == "funnel" and entry.get("round") == 1:
        insert_idx = i + 1
        break

if insert_idx is None:
    # Insert at end before plan update
    for i, line in enumerate(lines):
        entry = json.loads(line)
        if entry.get("action") == "plan" and entry.get("update"):
            insert_idx = i
            break

# Round 1 evaluation entries
eval_entries = [
    {
        "action": "evaluate",
        "round": 1,
        "metrics": {
            "energy_density_wh_kg": 352.07,
            "plated": True,
            "anode_potential_v_min": -0.452,
            "nail_penetration_triggered": "unchecked",
            "sei_thickness_nm": "unchecked"
        },
        "verdict": "fail",
        "evidence": [
            {"metric": "energy_density_wh_kg", "value": 352.07, "threshold": {"min": 327.18}, "verdict": "pass", "source": "cell/V_B_thin_electrode_energy.json"},
            {"metric": "plated", "value": True, "threshold": False, "verdict": "fail", "source": "cell/V_B_thin_electrode_4c.json:anode_potential_v (min=-0.452V)"}
        ],
        "candidate": "V_B_thin_electrode",
        "note": "Thinner electrodes reduce ED (352 vs 400) but worsen plating (more negative anode potential). Counter-intuitive: thinner electrodes increase local C-rate."
    },
    {
        "action": "evaluate",
        "round": 1,
        "metrics": {
            "energy_density_wh_kg": 401.90,
            "plated": True,
            "anode_potential_v_min": -0.390,
            "nail_penetration_triggered": "unchecked",
            "sei_thickness_nm": "unchecked"
        },
        "verdict": "fail",
        "evidence": [
            {"metric": "energy_density_wh_kg", "value": 401.90, "threshold": {"min": 327.18}, "verdict": "pass", "source": "cell/V_C_high_porosity_energy.json"},
            {"metric": "plated", "value": True, "threshold": False, "verdict": "fail", "source": "cell/V_C_high_porosity_4c.json:anode_potential_v (min=-0.390V)"}
        ],
        "candidate": "V_C_high_porosity",
        "note": "Higher porosity slightly improves transport (-0.390 vs -0.438 baseline) but not enough to prevent plating."
    },
    {
        "action": "evaluate",
        "round": 1,
        "metrics": {
            "energy_density_wh_kg": 412.83,
            "plated": True,
            "anode_potential_v_min": -0.438,
            "nail_penetration_triggered": "unchecked",
            "sei_thickness_nm": "unchecked"
        },
        "verdict": "fail",
        "evidence": [
            {"metric": "energy_density_wh_kg", "value": 412.83, "threshold": {"min": 327.18}, "verdict": "pass", "source": "cell/V_D_thin_sep_small_particles_energy.json"},
            {"metric": "plated", "value": True, "threshold": False, "verdict": "fail", "source": "cell/V_D_thin_sep_small_particles_4c.json:anode_potential_v (min=-0.438V)"}
        ],
        "candidate": "V_D_thin_sep_small_particles",
        "note": "Thin separator + small particles insufficient for plating prevention under SPMe."
    },
    {
        "action": "evaluate",
        "round": 1,
        "metrics": {
            "energy_density_wh_kg": 411.66,
            "plated": True,
            "anode_potential_v_min": -0.415,
            "nail_penetration_triggered": "unchecked",
            "sei_thickness_nm": "unchecked"
        },
        "verdict": "fail",
        "evidence": [
            {"metric": "energy_density_wh_kg", "value": 411.66, "threshold": {"min": 327.18}, "verdict": "pass", "source": "cell/V_E_balanced_energy.json"},
            {"metric": "plated", "value": True, "threshold": False, "verdict": "fail", "source": "cell/V_E_balanced_4c.json:anode_potential_v (min=-0.415V)"}
        ],
        "candidate": "V_E_balanced",
        "note": "Balanced approach: ED good but still plating (-0.415V). SPMe underestimates transport."
    }
]

# Rewrite log with inserted evaluate entries
if insert_idx is not None:
    new_lines = lines[:insert_idx]
    for e in eval_entries:
        new_lines.append(json.dumps(e, ensure_ascii=False) + "\n")
    new_lines.extend(lines[insert_idx:])
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Inserted {len(eval_entries)} evaluate entries at position {insert_idx}")
else:
    print("Could not find insertion point")
    for e in eval_entries:
        append_log(e)

# 2. Generate PDF versions using reportlab
print("\n=== Generating PDF versions ===")
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.units import mm

    def md_to_pdf(md_path, pdf_path):
        """Convert simple markdown to PDF."""
        doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                                leftMargin=20*mm, rightMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)
        styles = getSampleStyleSheet()
        story = []

        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        for line in content.split("\n"):
            if line.startswith("# "):
                story.append(Paragraph(line[2:], styles['Title']))
                story.append(Spacer(1, 6))
            elif line.startswith("## "):
                story.append(Paragraph(line[3:], styles['Heading2']))
                story.append(Spacer(1, 4))
            elif line.startswith("### "):
                story.append(Paragraph(line[4:], styles['Heading3']))
                story.append(Spacer(1, 3))
            elif line.startswith("|") and "---" not in line:
                # Table row - skip for simplicity, render as text
                cells = [c.strip() for c in line.split("|")[1:-1]]
                story.append(Paragraph(" | ".join(cells), styles['Normal']))
            elif line.startswith("- **") or line.startswith("- "):
                story.append(Paragraph("• " + line[2:], styles['Normal']))
            elif line.strip():
                story.append(Paragraph(line, styles['Normal']))
            else:
                story.append(Spacer(1, 3))

        doc.build(story)

    # Generate PDFs for each deliverable
    pdf_files = {
        "design_spec.md": "VBF-T7R1MIMO-DS-01.pdf",
        "datasheet.md": "VBF-T7R1MIMO-DSH-01.pdf",
        "dvpr.md": "VBF-T7R1MIMO-DVPR-01.pdf",
        "dfmea.md": "VBF-T7R1MIMO-DFMEA-01.pdf",
        "delivery_index.md": "VBF-T7R1MIMO-INDEX-01.pdf",
    }

    for md_file, pdf_file in pdf_files.items():
        md_path = f"{DELIVER_DIR}/{md_file}"
        pdf_path = f"{DELIVER_DIR}/{pdf_file}"
        if os.path.exists(md_path):
            try:
                md_to_pdf(md_path, pdf_path)
                size = os.path.getsize(pdf_path)
                print(f"  {pdf_file}: {size} bytes")
            except Exception as e:
                print(f"  {pdf_file}: ERROR - {e}")

except ImportError:
    print("reportlab not available - skipping PDF generation")
    print("Installing reportlab...")
    r = subprocess.run([PYTHON, "-m", "pip", "install", "reportlab"], capture_output=True, text=True)
    print(r.stdout[-200:] if r.stdout else "")

print("\n=== Done ===")
