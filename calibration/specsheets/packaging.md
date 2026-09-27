# Packaging / casing mass fraction for Li-ion cells — verified sources

Task: find published, citable mass breakdowns by component, with packaging/casing mass fraction for pouch and prismatic formats.
Verification rule: every number below comes from a source actually fetched. Second-hand numbers are marked as such.
Run started: 2026-09-27T14:34:20+08:00

---

## SOURCE 1 — Lee et al. 2025 (pouch, MEASURED teardown) ✅ VERIFIED

**Format:** pouch (all four cells) | **Cells:** 4 pouch cells, total mass 35–909 g
- LMO: First-generation Nissan Leaf, quality-control reject
- NMC: Second-generation Nissan Leaf, end-of-life
- LFP: A123
- LCO: Apple (consumer electronics)

**Number:** **"The mass percentage of the casing ranged from 3.5% to 5.4%."** (section 3.1 Cell Composition)

Direct quotes from the paper (section 3.1):
> "The total masses of the different cells ranged from 35 to 909 g. The mass percentage of the casing ranged from 3.5% to 5.4%. This value is quite low as the pouch materials are thin and light. This would be significantly higher for prismatic or cylindrical cells with rigid steel or plastics cases. The separators represented between 2.3% and 4.1% of the total mass of the cell. The cathodic and anodic coatings accounted for 33–45% and 18–25% of the total mass, respectively."

**Full breakdown given (as ranges over the 4 cells):**
| Component | wt% of total cell |
|---|---|
| Cathode coating | 33–45% |
| Anode coating | 18–25% |
| Separator | 2.3–4.1% |
| **Casing (pouch material)** | **3.5–5.4%** |
| (remainder = electrolyte + current collectors; given as Sankey diagrams, Figure 6, not as a number table) |

**How measured:** explicit cell teardown. Section 2: "A 'cell teardown' was performed on each cell chemistry... weighed and opened in a fume hood with a ceramic scalpel, and separated into anode, cathode, separator, and pouch material." Method step 4: "The change in weight between the unopened cell and the dried cell components was assumed to be electrolyte."

**Citation:** Lee, H.; Driscoll, E. H.; Waters, K.; Kendrick, E.; Sommerville, R. *Advanced Energy and Sustainability Research* **2025**, *6* (9), 2400366. DOI: 10.1002/aesr.202400366.

**Verified how:** PDF fetched (Heriot-Watt research portal, publisher's version of record) and text-extracted locally; the casing sentence read verbatim in section 3.1. Note: Table 2's columns are scrambled by the text extractor — chemistry/row assignment in that table should not be trusted from my extraction, but the casing sentence is unambiguous prose.

*CAVEAT for the user:* the 3.5–5.4% is a **measured teardown range**, not a single number, and it is for consumer/automotive pouch cells of 35–909 g. Note that the 909 g and 35 g cells span a 26x mass range, so the range is real spread, not measurement noise.

---

## SOURCE 2 — Jethwa PhD thesis 2024, Table 6-2 (pouch, MEASURED teardown) ✅ VERIFIED

**Format:** pouch, single cell type | **Cell:** Nissan Leaf (gen 1) QCR (quality-control reject) pouch cell, ~792 g
**Number:** m_casing = **38.4 / 38.0 / 39.9 g** on totals of **792.4 / 792.0 / 793.2 g** → **4.85% / 4.80% / 5.03%** (mean **4.9%**)

**Exact table as read from the rendered PDF page 215 (Table 6-2, "Mass breakdown of dissembled Nissan Leaf (gen 1) QCR pouch cell by components"):**

| Reference code | m_total | m_cathode | m_anode | m_separator | m_electrolyte | **m_casing** | m_unrecovered |
|---|---|---|---|---|---|---|---|
| PC 0203 | 792.4 | 412.2 | 255.5 | 44.3 | 7.4 | **38.4** | 34.6 |
| PC 2604 | 792.0 | 412.9 | 257.5 | 42.9 | 8.3 | **38.0** | 32.4 |
| PC 1406 | 793.2 | 410.4 | 258.7 | 47.6 | 6.3 | **39.9** | 30.3 |

(all in g; footnote: "m_i denotes the mass of each component, measured in g. Standard uncertainty, u(m) = 0.01 g.")
Each row sums to m_total exactly.

Definitions given in the thesis, verbatim: "m_total represents the total weight of the pouch cell before the disassembly, m_electrolyte is the electrolyte in its free liquid form captured on the surface of the electrode stack, and m_unrecovered represents the losses due to electrolyte vapourisation."

Important caveats stated in the thesis itself, verbatim: "the electrodes and separator components are 'wetted', meaning that their overall mass, as presented in Table 6-2, includes a fraction of the electrolyte. Consequentially, these recorded values do not solely denote the pure form of these components." And: "The estimated mass loss due to electrolyte vaporisation during the tear downs was between 3-5% of the total weight of the LIB pouch cells."

So m_cathode/m_anode/m_separator here are NOT pure component masses — they carry electrolyte. m_casing (38-40 g) is an aluminium laminate pouch, so it is a clean dry mass. Total electrolyte is larger than the 7.4 g "free liquid" figure; the rest is inside the wetted components plus the ~30-35 g vaporised.

**Citation:** Jethwa, S. *Recovery and Characterisation of LIB Electrolyte from Electric Vehicles* (PhD thesis). University of Birmingham, 2024, Chapter 6, Table 6-2, p. 215. Available at: https://etheses.bham.ac.uk/id/eprint/15175/7/Jethwa2024PhD.pdf

**Verified how:** PDF fetched, text-extracted, table header did not survive text extraction, so the page was rendered to an image at 220 dpi and the table read visually — column header `m_casing` is unambiguous.

*CAVEAT:* this is a **doctoral thesis**, not a peer-reviewed paper. The measurement itself is careful (three cells, u = 0.01 g) but it is grey literature and only one cell model.

---

## SOURCE 3 — Fischer et al. 2026, Recycling (peer-reviewed, MEASURED teardowns, BOTH pouch and prismatic) ✅ VERIFIED

**This is the single best source found for your question: it gives casing fraction for pouch AND prismatic AND cylindrical from one consistent teardown methodology, peer-reviewed, open access.**

**Citation:** Fischer, S.; Born, J. G.; Wolke, M.; Hölter, T.; Dröder, K.; Scholl, S.; Zetzener, H.; Kwade, A. Comprehensive End-of-Life-Battery Composition Analysis from Module to Electrode Level to Assist More Efficient Recycling. *Recycling* **2026**, *11* (1), 11. DOI: 10.3390/recycling11010011.

**Method (verbatim):** "In this investigation, a 30.2 kg battery module ... and its pouch cells (PouchZ) were dismantled and subjected to detailed analysis. ... Four additional industrial cells with unknown composition were examined in this study: one with a cylindrical format (Cylind), two with a prismatic format (PrismaS and PrismaB), and a pouch cell (PouchS). **For each experiment, three cells of each format were analyzed, and the average value was calculated.**" → this is a **measured teardown**, not a modelling assumption. Categories: "housing, conductor, plastic, electrolyte, Al foil, Cu foil, separator, anode coating, and cathode coating"; "The shavings produced by opening the cell were added to the housing."

### Cell identity (Table 6, verbatim)

| Sample | Format | Dimensions (L × W/D × H/T mm) | Case material | Case/foil thickness | Cell weight |
|---|---|---|---|---|---|
| Cylind | cylindrical | no length column value; 21 dia × 70 height → **21700 format** | Ni-coated steel | 0.45–0.5 mm | 68.3 ± 0.6 g |
| **PrismaB** | **prismatic** | 147 × 90 × 24 | **Al** | 1.0 mm | 684.8 ± 0.6 g |
| **PrismaS** | **prismatic** | 235 × 130 × 36 | **Al** | 0.8–1.0 mm | 2255.3 ± 3.7 g |
| PouchS | pouch | 352.5 × 100 × 16.1 | Plastic-Al | 0.16 mm | 1159.7 ± 3.1 g |
| PouchZ | pouch | 503 × 98 × 8.5 | Plastic-Al | 0.15 mm | 1055.3 ± 0.5 g |

Electrode assembly: Cylind wound, PrismaB wound, PrismaS Z-folded, PouchS stack, PouchZ laminated. PrismaS is from a stationary application; PrismaB/PouchZ/PouchS from electric transportation; Cylind are test cells. Electrode count for PrismaS: 88 anodes / 86 cathodes.

### THE NUMBERS — casing (housing) mass fraction

**Figure 3a**, "Mass fraction of various cell formats" (stacked bar, wt.%), read directly from the rendered figure:

| Cell | Format | **Housing wt%** | Conductor | Plastic | Housing+Conductor+Plastic (+Discharge plate) |
|---|---|---|---|---|---|
| Cylind | cylindrical | **17.88** | (panel b pie: 0.4) | (panel b pie: 0.8) | ≈ 19.1 |
| **PrismaB** | **prismatic, Al can, NMC** | **13.31** | 2.8 | 1.1 | **≈ 17.2** |
| **PrismaS** | **prismatic, Al can, LFP** | **7.61** | 1.2 | 0.8 | **≈ 10.8** (+1.2 discharge plate) |
| PouchS | pouch (stationary) | **≈ 1.8** | 0.5 | 0.1 | ≈ 2.4 |
| PouchZ | pouch (NCA) | **≈ 2.6** | 0.5 | 0.1 | ≈ 3.2 |

Whole-cell breakdown, read from the Appendix pies (each pie's inner ring sums to ~100%; the outer ring decomposes only the cathode coating into Li/Ni/Co/Mn/binder+bound oxygen):

| Component | PrismaB (Fig. A1) | PrismaS (Fig. A2) | PouchZ (Fig. A4) | PouchS (Fig. A3) |
|---|---|---|---|---|
| **Housing** | **13.3** | **7.6** | **2.6** | **1.8** |
| Conductor | 2.8 | 1.2 | 0.5 | 0.5 |
| Plastic | 1.1 | 0.8 | 0.1 | 0.1 |
| Electrolyte | 13.8 | 10.0 | 9.4 | 10.0 |
| Anode coating | 19.0 | 22.6 | 31.1 | 25.1 |
| Al-foil | 4.2 | 2.2 | 3.4 | 9.2 |
| Cu-foil | 8.6 | 5.5 | 5.7 | 5.2 |
| Separator | 3.4 | 4.3 | 3.7 | 6.8 |
| Cathode coating | 33.8 | 44.5 | 43.4 | 41.3 |
| Discharge plate | – | 1.2 | – | – |
| **Sum** | **100.0** | **99.9** | **99.9** | **100.0** |

(Values from the pies; the Figure 3a bars agree with these to within reading precision — e.g. PrismaB cathode 33.80, anode 19.01, housing 13.31, electrolyte 13.79; PrismaS cathode 44.68, anode 22.59, housing 7.61, electrolyte 10.00, Cu-foil 5.30, separator 4.42.)

**Verified how:** PDF downloaded from the MDPI article-deploy endpoint (mdpi-res.com) and opened locally; every number above was read from pages 5, 20, and 21 rendered at 500–900 dpi. Cross-checks that passed: (i) panel (b) pie (cylindrical, NCA) exactly reproduces the Cylind bar values 17.9 / 23.6 / 36.8 / 10.2; (ii) every Appendix pie's components sum to 100.0 ± 0.1 as the figure note allows ("Totals may differ from 100% due to rounding"); (iii) bar and pie agree for every cell on the housing value.

**Important definitional caveat for your model:** this source counts the **metal/laminate case only** as "Housing". Tabs/busbars/bus-plates ("Conductor"), seals/insulators ("Plastic") and the "Discharge plate" are separate categories. Your LG M50 "packaging = 17.60 g" residual almost certainly lumps all of those together. So the directly comparable quantity is **Housing + Conductor + Plastic** (last column of the table above), not Housing alone.

**Second caveat:** PrismaS is a **stationary-storage** LFP cell (2255 g), not an automotive traction cell, and its 7.6% housing reflects a large cell with a favourable surface-to-volume ratio. PrismaB (685 g, automotive) is the more representative automotive prismatic.

---

## SOURCE 4 — BatPaC v3 manual (MODELLING ASSUMPTION — and it is NOT a hard prismatic can) ✅ VERIFIED

**Citation:** Nelson, P. A.; Ahmed, S.; Gallagher, K. G.; Dees, D. W. *Modeling the Performance and Cost of Lithium-Ion Batteries for Electric-Drive Vehicles, Third Edition*; ANL/CSE-19/2; Argonne National Laboratory, 2019.
(Author list verified from the PDF itself: "Paul A. Nelson, Shabbir Ahmed, Kevin G. Gallagher, and Dennis W. Dees".)

**Verified how:** PDF read directly (130 pages, text-extracted). The copy was obtained from a public mirror at
`https://static.nhtsa.gov/nhtsa/downloads/CAFE/2021-NPRM-LD-2024-2026/Argonne+Databases/Documentations/BatPac+Model+Documentation+Third+Edition150624.pdf`
(3.0 MB, ANL/CSE-19/2 title page confirmed in the file). OSTI itself is unreachable from this network, so the OSTI/purl route could not be used.

**FINDING — the important one for you:** BatPaC's cell is **not a hard-cased prismatic**. Verbatim:
> "To provide a specific design for the calculations, **a prismatic cell in a stiff-pouch container was selected.**"

and
> "The stiff-pouch containment for the cell and the terminal seal is illustrated in Fig. 2.3. ... The cell housing material is a tri-layer consisting of an outer layer of polyethylene terephthalate (PEP) for strength, a **middle layer of 0.1-mm aluminum** for stiffness and impermeability to moisture and electrolyte solvent vapors and an inner layer of polypropylene (PP) for sealing by heating [21,22]."

and, from the manufacturing cost chapter (§8.3.11 "Enclosing Cell in Container"):
> "The aluminum foil layer in the pouch container is sufficiently thick (**100 microns default thickness**) to permit the use of stiff, pre-shaped pouch halves."

So **BatPaC is a pouch-format model**, even though the manual calls the design "prismatic". A casing fraction taken from BatPaC is a *pouch* number, not a hard-can prismatic number. Do not use BatPaC to justify a prismatic casing fraction.

**FINDING 2:** the manual **does not tabulate a cell-level component mass breakdown or a casing mass fraction anywhere**. I searched the full extracted text for "cell mass", "container" + "mass", and all table captions (Table 3.1 … Table 8.4). The tables in Chapters 4–7 report pack-level parameters (range, energy, power, price, pack mass in kg) and electrode thicknesses; the per-component cell masses are computed inside the Excel model and are not printed in the manual. The only pack-level mass statement reachable is a single "Pack mass, kg" label in a template table.

**Consequence:** BatPaC can be cited for *how a pouch container is modelled* (tri-layer PET/0.1 mm Al/PP), and for the general statement that it computes a mass breakdown — but **there is no citable BatPaC number for the casing mass fraction** in the manual. Anyone quoting one is quoting the spreadsheet's output, not the report.

---

## CROSS-CHECK against your LG M50 cylindrical derivation

Fischer et al. (Source 3) also tore down a cylindrical cell: **Cylind, 21 mm dia × 70 mm (i.e. a 21700), 68.3 g, Ni-coated steel can 0.45–0.5 mm** — essentially the same format and mass as your LG M50 (21 × 70 mm, 67.5 g).

| | your LG M50 | Fischer 2026 Cylind |
|---|---|---|
| total cell | 67.5 g | 68.3 g |
| case/housing | (inside your 17.60 g residual) | **17.88 wt%** |
| + conductor + plastic | – | +0.4 + 0.8 wt% = **19.1 wt%** |
| your whole packaging residual | **17.60 g = 26.1 %** | **≈ 19.1 %** |

So a measured teardown of a same-format, same-mass 21700 cell puts the *complete* non-stack hardware at **≈ 19 wt%**, about 7 points below your 26.1% residual. Two plausible explanations, both worth checking on your side: (i) your "electrode stack 43.45 g" may exclude the uncoated foil overhang / tab region, which this study counts under "Conductor"; (ii) the LG M50 can/cap is genuinely heavier. Either way, your 26.1% is *not* out of line with a bigger picture where cylindrical hard-case cells run 19–26%, and the same study's pouch and prismatic numbers show the format ordering you would expect (pouch ≪ prismatic < cylindrical).

---

## BOTTOM LINE — what fraction to use

**Pouch: use ≈ 4 % (range 2–5 %).**
Three independent measured teardowns of pouch cells agree on the order of a few percent: Lee 2025 (peer-reviewed, 4 pouch cells incl. two automotive Nissan Leaf) gives **3.5–5.4 %**; Jethwa 2024 (Nissan Leaf gen 1 QCR) gives **4.80–5.03 %** on three cells; Fischer 2026 gives **1.8 % and 2.6 %** on two larger (~1.1 kg) pouch cells. The two automotive-pouch studies cluster at **4–5 %**; the two large-format cells sit at **~2 %** because the laminate area scales worse than the volume as cells get bigger. If your pouch cells are ~0.5–1 kg automotive cells, **4 %** is the best single number; the whole defensible band is 2–5 %.

**Prismatic: use ≈ 13 % for the can alone, ≈ 15–17 % for all non-stack hardware — but scale it with cell size.**
The only measured, peer-reviewed prismatic numbers found are from Fischer 2026, both aluminium hard-case cells:
- **PrismaB** (automotive, 685 g, NMC, wound, 147 × 90 × 24 mm, 1.0 mm Al can): **housing 13.31 wt%**; housing + conductor + plastic = **17.2 wt%**.
- **PrismaS** (stationary, 2255 g, LFP, Z-folded, 235 × 130 × 36 mm, 0.8–1.0 mm Al can): **housing 7.61 wt%**; housing + conductor + plastic + discharge plate = **10.8 wt%**.

Note the spread is driven by cell size, not chemistry: the 0.69 kg cell gives 13.3 %, the 2.26 kg cell gives 7.6 %. If your simulated prismatic cell is a several-hundred-gram automotive cell, **13 % (can) / 17 % (all hardware)** is the right end; if it is a large multi-kg cell, use **8 % / 11 %**.

**Do not use BatPaC for the prismatic number.** BatPaC's cell is explicitly "a prismatic cell in a stiff-pouch container" with a PET/0.1 mm Al/PP laminate — it is a pouch, and the manual contains no casing mass fraction at all.

**Definitional warning that matters for your model.** In the measured studies, "housing" is the *case only*. Tabs, busbars, seals, gaskets and insulators are separate categories ("conductor", "plastic"). Your LG M50 residual of 17.60 g is "total − stack − electrolyte", which is the *sum* of those. So when you calibrate a pouch or prismatic equivalent, compare like with like: use **housing + conductor + plastic** (the second number in each row above), not housing alone, if your "packaging" term is meant to absorb everything that is not stack or electrolyte.

---

## COULD NOT VERIFY (do not cite these as checked)

1. **Stock, S. et al., "Cell teardown and characterization of an automotive prismatic LFP battery", *Electrochimica Acta* 2023, 471, 143341, DOI: 10.1016/j.electacta.2023.143341.** Identified and confirmed as a genuine open-access (CC BY) **prismatic hard-case LFP teardown** — a Tesla Model 3 SR pack cell, 161.5 Ah, 163 Wh/kg, separated into "can, two jelly rolls, and cap". This would be the ideal second prismatic source. **I could not read it:** ScienceDirect, Cell Press, SSRN and Scribd all returned HTTP 403 to this network, and Unpaywall/OpenAlex show no repository copy (publisher-hosted only). Its numeric mass breakdown is therefore **unverified** — a search snippet said the teardown separated can / jelly rolls / cap but no result I saw stated the casing mass or percentage. Worth retrieving from a network that can reach Elsevier.

2. **BatPaC v5.0 manual (Knehr, Kubal, Nelson, Ahmed; ANL/CSE-22/1, 2022, DOI 10.2172/1877590).** Could not be fetched — **osti.gov is unreachable from this machine** (connections return HTTP 000) and publications.anl.gov returns 403. All BatPaC statements above come from the **Third Edition (ANL/CSE-19/2)**, which I did read in full. There is some chance v5.0 added a printed mass-breakdown table that the third edition lacks; unverified.

3. **The prismatic-vs-pouch BOM attributed to a PEFCR/Stellantis dataset** (prismatic Al 17.4 % vs pouch Al 6.2 %) surfaced in a search snippet sourced to a Politecnico di Torino thesis. Not fetched, so **second-hand and unverified** — and note that its "Al" column merges the casing with the cathode current-collector foil, so it is not a casing fraction at all.

4. **HNEI report Table A7 "outer case wt%"** (Diekman 2017 29.4 %, Kochhar & Johnston 2018 18.4 %, Zhu 2021 30 %, etc.). These are literature compilations of secondary sources, not measurements; I did not fetch the report, so they are **second-hand and unverified**, and several of them clearly refer to the *module/pack* enclosure rather than the cell casing. Do not use without checking each upstream reference.

5. **Günter & Wassiliadis 2022 JES pouch teardown (DOI 10.1149/1945-7111/ac4e11).** Confirmed to exist as an open-access teardown of a 78 Ah VW ID.3 pouch cell, reporting component masses (cathode foil 30.5 g, separator 41.3 g, evaporated electrolyte 75.1 g) and that ">75 % of cell mass ... contributes active material". A search snippet reports these; I did not fetch the paper, and **the snippet did not include the packaging mass**, so no pouch casing fraction from this source is verified here. It is a good candidate for a stronger automotive-pouch number if you can reach IOPscience.

---

*Summary of what is actually verified in this file: pouch casing 3.5–5.4 % (Lee 2025, peer-reviewed, measured); pouch casing 4.80–5.03 % (Jethwa 2024 thesis, measured); pouch casing 1.8 % and 2.6 % (Fischer 2026, peer-reviewed, measured); prismatic casing 13.31 % and 7.61 % (Fischer 2026, peer-reviewed, measured); BatPaC models a stiff pouch and publishes no casing fraction.*
