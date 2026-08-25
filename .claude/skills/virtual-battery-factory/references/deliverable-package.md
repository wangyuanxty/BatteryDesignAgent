# Deliverable Format: Delivery Package Index `delivery_index.md` (Required at close-out; also output a PDF release version)

> Read on demand per SKILL.md Section 1, Step 7 at close-out. The index is the "cover + controlled list" of all deliverables, organizing the scattered deliverables into a controlled design package; the index registers only **actually generated** files (first list the directory to confirm, then write one row per file); it must not register files that are planned but not produced.

- **Cover information (field list, none missing)**:
  - Case name (e.g. `ed300_4c`)
  - Numbering scheme: `VBF-<CASE-ID-UPPERCASE>-<DOC-CODE>-<SEQ-NO>` (for the uppercase case ID, remove non-alphanumeric characters, e.g. `ed300_4c` → `ED3004C`; the SEQ-NO is a two-digit serial number under that document code, starting from `01`)
  - Generation date (`YYYY-MM-DD`)
  - Signature block: prepared / reviewed / approved three fields, **left blank** (for manual signing)
- **Document code reference table (fixed by protocol)**:

  | Document code | Meaning | Corresponding file |
  |--------|------|---------|
  | DS | Specification | `design_spec.md` |
  | BOM | Bill of Materials | `bom.xlsx` |
  | DSH | Datasheet technical parameter sheet | `datasheet.docx` |
  | CALC | Calculation sheet | `calc.xlsx` |
  | DVPR | Design verification report | `dvpr.md` |
  | DFMEA | Failure analysis | `dfmea.md` |
  | CAD | Structure model | `cell_model.stl` |

- **File list table format** (one row per deliverable, four columns: file name / number / format / source description):
  - Number: in the form `VBF-ED3004C-DS-01`; the editable source and the PDF release version of the same file share **the same number**, distinguished in the file name and format columns
  - Format: the actual extension, e.g. `md` / `pdf` / `xlsx` / `docx` / `stl` / `png` / `html`
  - Source description: which step/tool produced the file (e.g. "design_spec.md generated per the deliverable-design-spec spec", "xlsx→pdf exported by openpyxl/reportlab")
  - Ancillary files (preview images, legends, reports, etc.) also each occupy one row, numbered with their owning document code (e.g. `cell_model_preview.png` belongs to CAD, `report.html` belongs to DS)
- **PDF release version**: use reportlab (installed in `.venv`) with a one-off script to generate `delivery_index.pdf`; the cover colors follow the engineering blueprint style `#14283C` (deep blue background)/`#1E5A8A` (medium blue)/`#C97B3D` (copper orange accent), may be simplified; the inner file list table is row-by-row identical to the md version
