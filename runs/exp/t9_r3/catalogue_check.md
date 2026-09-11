# T9 run 3 — public catalogue check (criterion 6, close the loop)

Date: 2026-09-10. Queries executed from this workspace machine.

## 1. Crystallography Open Database (COD, crystallography.net)

- Query A (exact finalist): `https://www.crystallography.net/cod/result?formula=Ni0.75Mg0.25PO4F&format=json`
  -> **0 entries**.
- Query B (finalist element set): `https://www.crystallography.net/cod/result?formula=Li1 Ni1 P1 O4 F1&format=json`
  -> **0 entries** (the whole Li-Ni-P-O-F fluorophosphate family is absent from COD — scope characterization).

## 2. Open Quantum Materials Database (OQMD, oqmd.org)

- Query: OPTIMADE endpoint
  `https://oqmd.org/optimade/v1/structures?filter=elements HAS ALL "Li","Ni","Mg","P","O","F"`
  -> **data_returned = 0 of 1,407,395 total entries**.
- (OQMD does contain the parent binaries/phosphates, e.g. LiNiPO4 and LiMgPO4 entries — but
  no Li-Ni-Mg-P-O-F quinary fluorophosphate.)

## Verdict

The finalist composition LiNi0.75Mg0.25PO4F was **not found in the searched scope**
(COD + OQMD). It is absent from the 115-formula documented-cathode membership layer of
known_set_v3.json as well (membership_check.py: raw and whitespace-normalized, clean).
