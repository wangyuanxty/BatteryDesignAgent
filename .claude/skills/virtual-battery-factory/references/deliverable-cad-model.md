# Deliverable Format: Cell Structure Model `cell_model.stl` + Preview Images (Optional, delegate to cad-skill)

> Read on demand per SKILL.md Section 1, Step 7. Produce when the user clarifies the request.

- **Tool**: use **cad-skill** (CadQuery parametric modeling + headless rendering preview), following its progressive preview workflow (Phase 1 base shape → user feedback → Phase 2 details → Phase 3 delivery). **Dependency declaration**: cad-skill is an external skill and must be installed (`.claude/skills/cad-skill/`, not part of this repository) and CadQuery must be installable via pip; if unavailable, this optional deliverable shall be honestly marked as skipped.
- **Parameter source**: all dimensions/layer thicknesses are taken from the parameter set (the same set of values as `deliverable-design-spec.md`), annotated line by line in the PARAMETERS section of the script; no numbers are written from memory.
- **Clarifications already covered (interaction mode, Section 0, Item 7)**: structural form (21700 wound / pouch stacked / other) and expression style (exploded diagram with real thickness annotations / proportionally exaggerated / print parts) — execute per the user's choice, do not change without authorization.
- **Real thickness annotation**: µm-level layer thicknesses are not visible in mm-level models; a companion layer-thickness annotation table (layer name ↔ real thickness ↔ parameter set source) must be delivered together with the model.
- **Deliverables**: `cell_model.stl` + multi-view preview PNGs + layer thickness annotation table.
- **Boundary**: this model is a structural illustration (paper figure / demonstration), **not** a tolerance-bearing engineering manufacturing drawing — state this honestly at delivery.
