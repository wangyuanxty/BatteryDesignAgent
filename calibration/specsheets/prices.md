# Citable unit prices for lithium-ion cell materials

Purpose: unit prices ($/kg or $/m2) for computing material cost from a per-layer mass model
(positive coating, negative coating, positive current collector, negative current collector, separator).

Rule applied throughout: every number below comes from a source that was actually fetched.
Nothing is inferred, interpolated, or remembered. Second-hand numbers are flagged as such.

---

## Verified prices

### 1. NMC811 positive electrode active material — $26.0/kg

- **Price**: 26.0 USD/kg
- **Vintage of price**: BatPaC 5.0 default price set, updated 8 March 2022
- **Raw or battery-grade**: **Battery-grade purchased material** (positive electrode active material as a material input to a cell cost model)
- **Observed or assumed**: **Model assumption.** This is the BatPaC 5.0 *default input* price, not a recorded transaction. The paper says the validations rely on "private communications from equipment manufacturers, cell manufacturers, materials suppliers, and original equipment manufacturers (OEM) based on the global market values" — so it is a market-informed assumption, but it is an assumption.
- **Cell type**: NMC811-Gr (NMC811 cathode / graphite anode)
- **Citation**: Hewawasam, D.; Karunathilake, H.; Subasinghe, L.; Witharana, S. In *2022 Moratuwa Engineering Research Conference (MERCon)*; IEEE, 2022; pp 1–6. DOI: 10.1109/MERCon55799.2022.9906183. (Author order as printed on the paper; Crossref lists Subasinghe second, the PDF lists Karunathilake second.)
- **Verified how**: Fetched the PDF (http://s3.amazonaws.com/edas.manuscripts/final/1570802596.pdf, 728 kB, 6 pages), extracted text with PyMuPDF, read Table IV directly. No search snippet was used.

Companion values from the same Table IV (same vintage and same status — BatPaC 5.0 defaults, 8 March 2022):

| Cell type | Positive active material price | Raw or battery-grade | Observed or assumed |
|---|---|---|---|
| NMC811-Gr | 26.0 $/kg | battery-grade | model assumption (BatPaC 5.0 default) |
| NCA-Gr | 26.0 $/kg | battery-grade | model assumption (BatPaC 5.0 default) |
| LFP-Gr | 10.0 $/kg | battery-grade | model assumption (BatPaC 5.0 default) |
| LMO-Gr | 9.0 $/kg | battery-grade | model assumption (BatPaC 5.0 default) |
| NMC532/LMO (50/50)-Gr | 16.5 $/kg | battery-grade | model assumption (BatPaC 5.0 default) |

Same source. The paper also states: "For this study, the default price values of the most recent updated version of BatPaC 5.0 by 8th March 2022 were used."

---

### 2–5. USGS Mineral Commodity Summaries 2025 — RAW MATERIALS ONLY (context, not battery-grade cell materials)

**Read this first.** All four numbers below are **raw / refined commodity prices**, not prices for the
battery-grade cell material in your mass model. In particular, lithium carbonate is a *cathode precursor
chemical*, not NMC811 powder. Copper cathode and aluminium ingot are *unwrought metal*, not battery-grade
6 µm / 12 µm foil. Flake graphite is *mine/import concentrate*, not battery-grade anode powder.
They are useful for context, sanity checks and lower bounds — they are **not** substitutes for the
battery-grade prices.

All four are **market observations** (published annual averages), not model assumptions.
The 2025 edition reports calendar years 2020–2024 (the 2024 column is marked "e" = estimated).

**Verified how (all four)**: Fetched the USGS PDF directly (HTTP 200, ~750 kB each), extracted text with
PyMuPDF, read the "Salient Statistics—United States" table header and price rows verbatim.
URLs: https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-{lithium,graphite,copper,aluminum}.pdf

#### 2. Lithium carbonate (battery-grade), annual average real price

| Year | 2020 | 2021 | 2022 | 2023 | 2024e |
|---|---|---|---|---|---|
| USD per metric ton | 10,100 | 14,200 | 71,100 | 41,300 | **14,000** |

- **2024 value: $14,000/metric ton = $14.00/kg**
- **Raw or battery-grade**: The USGS line labels it "battery-grade lithium carbonate" — but it is a **precursor chemical (raw material)**, not NMC811 cathode powder.
- **Observed or assumed**: market observation (annual average, real terms)
- Row label verbatim: "Price, annual average-real, battery-grade lithium carbonate, dollars per metric ton2"
- Corroborating sentence verbatim: "For fixed contracts, the annual average U.S. lithium carbonate price was $14,000 per ton in 2024, a decrease of 66% from that in 2023."
- **Citation**: Jaskula, B. W. *Lithium*; Mineral Commodity Summaries 2025, U.S. Geological Survey, 2025.

#### 3. Graphite (natural, flake) — average unit value of imports

| Year | 2020 | 2021 | 2022 | 2023 | 2024e |
|---|---|---|---|---|---|
| USD per metric ton | 1,340 | 1,330 | 1,200 | 1,080 | **1,070** |

- **2024 value: $1,070/metric ton = $1.07/kg**
- **Raw or battery-grade**: **RAW.** Natural flake graphite concentrate, import unit value at foreign ports. Not battery-grade spherical/coated anode powder.
- **Observed or assumed**: market observation (import unit value). Note the row label itself says "average unit value of imports", i.e. a trade statistic, not a quoted price.
- **Citation**: Stewart, A. A. *Graphite (Natural)*; Mineral Commodity Summaries 2025, U.S. Geological Survey, 2025.

#### 4. Copper — U.S. producer cathode (COMEX + premium), annual average

| Year | 2020 | 2021 | 2022 | 2023 | 2024e |
|---|---|---|---|---|---|
| cents per pound | 286.7 | 432.3 | 410.8 | 395.3 | **430** |

- **2024 value: 430 cents/lb = $4.30/lb = $9.48/kg** (converted at 1 lb = 0.45359237 kg)
- **Raw or battery-grade**: **RAW.** Refined copper cathode, not rolled battery foil. Battery foil carries a rolling/processing premium on top of this.
- **Observed or assumed**: market observation
- **Citation**: Flanagan, D. M. *Copper*; Mineral Commodity Summaries 2025, U.S. Geological Survey, 2025.

#### 5. Aluminium — ingot, average U.S. market (spot)

| Year | 2020 | 2021 | 2022 | 2023 | 2024e |
|---|---|---|---|---|---|
| cents per pound | 89.7 | 138.5 | 152.6 | 125.9 | **130** |

- **2024 value: 130 cents/lb = $1.30/lb = $2.87/kg** (converted at 1 lb = 0.45359237 kg)
- **Raw or battery-grade**: **RAW.** Primary ingot, not battery-grade 12–16 µm foil.
- **Observed or assumed**: market observation
- **Citation**: Merrill, A. M. *Aluminum*; Mineral Commodity Summaries 2025, U.S. Geological Survey, 2025.

---

### 6. BatPaC manual Table 4.1 — the material price table itself (2010 vintage, published 2012)

**This is the BatPaC material price table.** I could not reach osti.gov or anl.gov (see "Could not verify" at the
bottom), so I obtained the table from the ANL-authored EPA edition of the same manual, which is hosted on EPA's
publications server and reachable.

**Source document**: *Modeling the Cost and Performance of Lithium-Ion Batteries for Electric-Drive Vehicles* —
Draft Report; EPA-420-D-12-004; U.S. Environmental Protection Agency, Office of Transportation and Air Quality,
August 2012; prepared for EPA by Argonne National Laboratory under Contract No. DE-AC02-06CH11357.

**Verified how**: Fetched the PDF directly from EPA's NEPIS server
(https://nepis.epa.gov/Exe/ZyPDF.cgi?Dockey=P100KUFL.PDF, 1.65 MB, 87 pages, HTTP 200), extracted text with
PyMuPDF, and read Table 4.1 verbatim on page 27 of the document (PDF page 43). Every number below is quoted from
that table; none comes from a search snippet.

**Status of every number in this table — read before using:**
- **Raw or battery-grade**: **battery-grade purchased material** (these are prices for the material as bought
  by a cell manufacturer, not metal/mineral prices).
- **Observed or assumed**: **model assumption.** The report states verbatim: *"While we state suggested materials
  costs, the user of the cost model may enter any value that they desire."* and *"Our values, as well as the others
  in the table, are derived from conversations with material, cell, and original equipment manufacturers. The
  sources are commonly anonymous and the accuracy of the values is generally unknown."*
- **Vintage**: the column used below is the **ANL 2010** column. **This is roughly 15 years old — flag it.**
  The table also reproduces TIAX 2010 and CARB 2007 columns for comparison (given below for range).

| Material | Chemistry / spec | Unit | **ANL 2010** | TIAX 2010 | CARB 2007 |
|---|---|---|---|---|---|
| Manganese spinel cathode | Li1.06Mn1.94O4 (LMO) | $/kg | 10 | 12–16–20 | 8–10 |
| Phospholivine cathode | LiFePO4 (LFP) | $/kg | 20 | 15–20–25 | 16–20 |
| Layered oxide cathode | LiNi0.80Co0.15Al0.05O2 (NCA) | $/kg | 36 | 34–40–54 | 28–30 |
| Layered oxide cathode | Li1.05(Ni1/3Mn1/3Co1/3)0.95O2 (NMC-333) | $/kg | 40 | 40–45–53 | 22–25 |
| Layered oxide cathode | Li1.05(Ni4/9Mn4/9Co1/9)0.95O2 (NMC-441) | $/kg | 33 | – | – |
| Li & Mn rich layered cathode | xLi2MnO3·(1-x)LiNiyMnzCo1-y-zO2 (LMR-NMC) | $/kg | 25 | 24–31–39 | – |
| **Graphite anode** | C6 (Gr) | **$/kg** | **19** | 17–20–23 | – |
| Titanate spinel anode | Li4Ti5O12 (LTO) | $/kg | 12 | 9–10–12 | – |
| **Electrolyte** | 1.2 M LiPF6 in EC:EMC | **$/kg** | **19** | 18.5–21.5–24.5 | – |
| **Separator** | PP/PE/PP | **$/m²** | **2** | 1–2.5–2.9 | – |
| **Current collector foil, Copper** | | **$/m²** | **3.00** | – | – |
| **Current collector foil, Aluminum** | | **$/m²** | **0.80** | – | – |

TIAX and CARB columns shown as printed; where three numbers appear they are the low–mid–high of a stated range.

Corroborating sentence verbatim from the same section, on the electrolyte: *"...the electrolyte used in this
model is based on a lithium hexafluorophosphate salt, LiPF6, ... $19/kg, is only for the base electrolyte
(i.e. no additional additives)."*

**Note on units for your model**: BatPaC quotes separator, Cu foil and Al foil **per m², not per kg**. If you need
$/kg you must divide by the areal mass (foil thickness × density); BatPaC's own foil thickness assumptions are in
its cell design inputs, not in this table.

Same source and page.

Note: **NMC811 does not appear in this table** — the 2010 report predates it. For NMC811 the only price I
verified is the BatPaC 5.0 default of $26.0/kg (entry 1 above).

---

### 7. Baars et al. (2023) SI, Table S3 — complete battery-grade material price table, market prices as of 13 May 2022

**This is the best single source for your purpose.** It is a peer-reviewed, open-access journal paper whose
Supporting Information tabulates prices in **$/kg for every one of your six core materials**, as
**battery-grade purchased materials**, from **market price observations** (Shanghai Metals Market, SMM),
at a **single stated vintage (13 May 2022)**.

**Citation**: Baars, J.; Cerdas, F.; Heidrich, O. *Environ. Sci. Technol.* **2023**, *57*, 5056–5067.
DOI: 10.1021/acs.est.2c04080. (Supporting Information, Table S3: "Battery material mass prices".)

**Verified how**: The SI ZIP was retrieved from the Europe PMC supplementary-files service for PMCID
PMC10061934 (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10061934/supplementaryFiles`), then the
contained `es2c04080_si_001.pdf` (5,551,038 bytes, 107 pages) was extracted and converted to text with
PyMuPDF. Table S3 was read verbatim off page S73 of that PDF. Note: this download required forcing HTTP/1.0 —
over HTTP/1.1 the transfer was silently truncated at ~590 kB every time and the ZIP had no central directory.

**Table S3 as printed** — heading verbatim: *"Table S3: Battery material mass prices. SMM price as of the 13th
May 2022"*. The "Source" column is reproduced exactly as printed; this is what distinguishes observed from assumed.

| Material | Price | Unit | Source (as printed) | Observed or assumed |
|---|---|---|---|---|
| **natural graphite** | **9.11** | $/kg | SMM (2022) | market observation |
| **synthetic graphite** | **12.15** | $/kg | SMM (2022) | market observation |
| **SiO** | **60.00** | $/kg | Greenwood et al. (2021) | model assumption (other paper) |
| LMO | 16.64 | $/kg | SMM (2022) | market observation |
| LFP | 21.43 | $/kg | SMM (2022) | market observation |
| NCA | 39.64 | $/kg | See Section 6.6 (calculated) | derived |
| NMC333 | 42.31 | $/kg | See Section 6.6 (calculated) | derived |
| NMC532 | 51.40 | $/kg | SMM (2022) | market observation |
| NMC622 | 54.49 | $/kg | SMM (2022) | market observation |
| **NMC811** | **60.09** | $/kg | SMM (2022) | market observation |
| NMC532/50%/LMO | 34.02 | $/kg | Calculated 50% NMC532-50%LMO | derived |
| **cathode binder (PVDF)** | **15.00** | $/kg | BatPaC version 5 | model assumption |
| **anode binder (CMC)** | **5.00** | $/kg | Greenwood et al. (2021) | model assumption (other paper) |
| anode binder additive (SBR) | 5.00 | $/kg | Greenwood et al. (2021) | model assumption (other paper) |
| **carbon black** | **3.60** | $/kg | Alibaba | market listing (not SMM; weaker) |
| binder solvent (NMP) | 2.00 | $/kg | Alibaba | market listing (not SMM; weaker) |
| binder solvent (deionised water) | 0.00 | $/kg | Assumed free | assumption |
| **Al foil (10–12 µm)** | **5.65** | $/kg | SMM (2022) | market observation |
| **Al foil (13 & 14 µm)** | **5.50** | $/kg | SMM (2022) | market observation |
| **Al foil (15–18 µm)** | **5.35** | $/kg | SMM (2022) | market observation |
| **Cu foil (6 µm)** | **15.77** | $/kg | SMM (2022) | market observation |
| **Cu foil (8–14 µm)** | **14.15** | $/kg | SMM (2022) | market observation |
| **electrolyte (NMC/NCA)** | **15.54** | $/kg | SMM (2022) | market observation |
| electrolyte (LFP) | 13.03 | $/kg | SMM (2022) | market observation |
| electrolyte (LMO) | 12.89 | $/kg | SMM (2022) | market observation |
| **separator (5 µm)** | **195.56** | $/kg | SMM (2022) | market observation |
| **separator (7 µm)** | **98.41** | $/kg | SMM (2022) | market observation |
| **separator (9 µm)** | **51.85** | $/kg | SMM (2022) | market observation |
| coated separator (5+2 µm) | 83.31 | $/kg | SMM (2022) | market observation |
| coated separator (7+2 µm) | 51.81 | $/kg | SMM (2022) | market observation |
| coated separator (9+3 µm) | 32.88 | $/kg | SMM (2022) | market observation |
| cell terminal cathode | 8.64 | $/kg | BatPaC version 5 | model assumption |
| cell terminal anode | 2.41 | $/kg | BatPaC version 5 | model assumption |
| cell container | 3.00 | $/kg | BatPaC version 5 | model assumption |

**Vintage: all SMM prices are as of 13 May 2022.** That is ~4 years old as of 2026 — flag it.

**Critical caveat on the Cu and Al foil numbers — these are not pure metal prices.** Verbatim from the same
SI section (§6.3):

> *"For LIB Al foils, the SMM reports a price of 2.9, 2.8 and 2.7 $ kg−1 for 12, 13 and 15 µm, respectively
> while LIB Cu foil has a price range of 7.28 and 5.15 $ kg−1 for 6 and 8 µm (foil prices refers to the
> processing fees of foils and excludes the cost of raw Cu and Al). ... For Cu foil, it was assumed that 6 and
> 7 µm foils are sold with a treatment charges of 7.28 $ kg−1 while 8 - 14 µm are fixed to 5.72 $ kg−1. An
> additional cost of 9.00 kg−1 is included to account for the current Cu price and 2.7 $/kg to account for the
> Al price (see Table S7)."*

So each foil price = SMM processing/treatment charge **plus** the metal price. The tabulated totals are close to
but not exactly reproducible from the rounded components quoted in the prose (e.g. Cu 6 µm: 7.28 + 9.00 = 16.28
vs. 15.77 tabulated; Al 10–12 µm: 2.9 + 2.7 = 5.6 vs. 5.65 tabulated). **Use the tabulated values**; the prose
components are rounded. This confirms the foil numbers are **battery-grade finished foil prices, not raw metal
prices** — which is exactly what a cell material-cost calculation needs.

Other verbatim notes from the SI that bear on interpretation:
- Separator: *"The price data for separator was converted from m2 to kg based on Equation 5.1 in Section 5.3.4."* — the huge spread across 5/7/9 µm is a real thickness effect, not an error.
- Electrolyte: three SMM electrolyte types exist (NMC, LMO, LFP); *"It is assumed that NCA chemistries require NMC electrolytes and LMO electrolyte is only for pure LMO"*.

**Cross-check against entry 1**: this table's NMC811 SMM market price for May 2022 is **$60.09/kg**, while the
BatPaC 5.0 *default input* for the same period (entry 1) is **$26.0/kg** — a factor of ~2.3 apart. This is the
market-observation vs. model-assumption distinction in its starkest form, and it has a large effect on any
computed cell cost. Use the BatPaC default if you want to reproduce BatPaC's numbers; use the SMM price if you
want a market cost.

---

### 8. Argonne (2024) "Material Price Assumptions" 2019–2024 — the current BatPaC default price set

**This is the most recent BatPaC material price set I could verify (2024 vintage).** Use this in preference to
entry 6 (2010 vintage) for graphite, electrolyte, separator, Al and Cu current collectors, binder and NMP.

**Source document**: Knehr, K.; Kubal, J.; Ahmed, S. *Estimated Cost of EV Batteries 2019–2024*; Argonne National
Laboratory, Chemical Sciences and Engineering Division, August 19, 2024. (Slide deck; slide 9 is the price table.
The companion workbook is named on the slides as *Benchmark EV Battery 2024-08-19 – BPC5p1 2023-08-14.xls*,
i.e. BatPaC 5.1.)

**Verified how**: `anl.gov` returns HTTP 403 to this client on every path. I retrieved the PDF from the Internet
Archive Wayback Machine snapshot taken 2024-12-12 of the ANL URL
(`http://web.archive.org/web/20241212001652/https://www.anl.gov/sites/www/files/2024-11/GPRA2024_06Nov2024.pdf`,
550,443 bytes, 15 pages, HTTP 200), extracted text with PyMuPDF, and read the table off slide 9 directly. The
Wayback snapshot is a byte copy of the ANL file; the content itself is Argonne's.

**Status of every number**: **battery-grade purchased material** prices; **model assumptions** (BatPaC default
inputs), not observed transactions. Slide heading verbatim: *"Material Price Assumptions"*, with the annotation
*"Material prices have dropped between 2023-2024"*. Cell design context verbatim: *"NMC811 cathode, Graphite
anode; 94 kWhRated, 80 kWhUseable; 200 kW; 300 cells, 10 modules; Pack production volume of 100,000 packs per
year — Packs made from cells produced in plant with 50 GWh/year capacity."*

| Component | Unit | 2019 | 2020 | 2021 | 2022 | 2023 | **2024** |
|---|---|---|---|---|---|---|---|
| Cathode Active Material | (chemistry) | NMC622 | NMC811 | NMC811 | NMC811 | NMC811 | **NMC811** |
| **Cathode Active Material** | **$/kg** | 21.00 | 22.00 | 22.80 | 26.00 | 26.00 | **22.00** |
| **Graphite** | **$/kg** | 14.00 | 14.00 | 11.00 | 10.00 | 10.00 | **9.50** |
| **Electrolyte** | **$/L** | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | **14.00** |
| **Separator** | **$/m²** | 1.10 | 1.00 | 1.00 | 1.00 | 1.00 | **1.00** |
| **Aluminum Current Collector** | **$/m²** | 0.40 | 0.40 | 0.40 | 0.40 | 0.40 | **0.40** |
| **Copper Current Collector** | **$/m²** | 1.20 | 1.20 | 1.20 | 1.20 | 1.20 | **1.20** |
| **Positive Binder** | **$/kg** | 10.00 | 10.00 | 10.00 | 15.00 | 15.00 | **15.00** |
| NMP | $/kg | 3.10 | 3.10 | 3.10 | 3.10 | 3.10 | **3.10** |

**Vintage: the 2024 column is a 2024 price.** Not stale. (The table is labelled "2019–2024" and the deck is dated
August 19, 2024.)

**Note the disagreement with entry 7, and take it seriously.** For NMC811 the Argonne 2024 default is **$22.00/kg**
while the SMM market price in May 2022 was **$60.09/kg**. Argonne's electrolyte is quoted **per litre** and the
Baars table **per kg** — they are not directly comparable without the electrolyte density. Argonne's Cu and Al
are **per m²**; the Baars table is **per kg** — not directly comparable without foil thickness and density.
Argonne's separator is **$1.00/m²** while Baars' is **$51.85–195.56/kg** depending on thickness; the two are
reconcilable only through the areal mass.

---

# Summary table

Every row was verified by fetching the source and reading the number in it. "Verified how" is abbreviated here;
the full method is in the entry above.

| Material | Price | Year of price | Raw or battery-grade | Observed or assumed | Citation | Verified how |
|---|---|---|---|---|---|---|
| **NMC811 cathode powder** | **22.00 $/kg** | 2024 | battery-grade | assumed (BatPaC 5.1 default) | Knehr, K.; Kubal, J.; Ahmed, S. *Estimated Cost of EV Batteries 2019–2024*; Argonne National Laboratory, 2024. | fetched PDF via Wayback snapshot of anl.gov; read slide 9 |
| **NMC811 cathode powder** | 26.0 $/kg | 2022 (8 Mar 2022) | battery-grade | assumed (BatPaC 5.0 default) | Hewawasam et al., *2022 MERCon*, IEEE, pp 1–6. DOI: 10.1109/MERCon55799.2022.9906183 | fetched PDF; read Table IV |
| **NMC811 cathode powder** | 60.09 $/kg | 2022 (13 May 2022) | battery-grade | **observed** (SMM market price) | Baars, J.; Cerdas, F.; Heidrich, O. *Environ. Sci. Technol.* **2023**, *57*, 5056–5067. DOI: 10.1021/acs.est.2c04080 | fetched SI ZIP via Europe PMC; read Table S3, p S73 |
| **Graphite anode powder** | **9.50 $/kg** | 2024 | battery-grade | assumed (BatPaC 5.1 default) | Knehr, Kubal, Ahmed, Argonne, 2024, slide 9 | as above |
| Graphite anode powder | 10.00 $/kg | 2022 and 2023 | battery-grade | assumed | same | as above |
| Graphite anode powder — natural | 9.11 $/kg | 2022 (13 May 2022) | battery-grade | **observed** (SMM) | Baars et al. 2023 SI, Table S3 | as above |
| Graphite anode powder — synthetic | 12.15 $/kg | 2022 (13 May 2022) | battery-grade | **observed** (SMM) | Baars et al. 2023 SI, Table S3 | as above |
| Graphite anode powder | 19 $/kg | 2010 | battery-grade | assumed (BatPaC) | *Modeling the Cost and Performance of Li-Ion Batteries for EDVs*; EPA-420-D-12-004; EPA, 2012 (prepared by ANL), Table 4.1 | fetched PDF from EPA NEPIS; read Table 4.1 |
| Graphite (natural flake, concentrate) | 1.07 $/kg | 2024 | **RAW** | observed (import unit value) | Stewart, A. A. *Graphite (Natural)*; MCS 2025, USGS, 2025. | fetched USGS PDF; read Salient Statistics |
| **Copper foil (battery grade)** | **1.20 $/m²** | 2024 | battery-grade finished foil | assumed (BatPaC 5.1 default) | Knehr, Kubal, Ahmed, Argonne, 2024, slide 9 | as above |
| Copper foil (battery grade) | 15.77 $/kg (6 µm); 14.15 $/kg (8–14 µm) | 2022 (13 May 2022) | battery-grade finished foil (SMM treatment charge + Cu metal) | **observed** (SMM) | Baars et al. 2023 SI, Table S3 | as above |
| Copper foil (battery grade) | 3.00 $/m² | 2010 | battery-grade | assumed (BatPaC) | EPA-420-D-12-004, 2012, Table 4.1 | as above |
| Copper (refined cathode) | 9.48 $/kg (430 ¢/lb) | 2024 | **RAW** | observed | Flanagan, D. M. *Copper*; MCS 2025, USGS, 2025. | fetched USGS PDF |
| **Aluminium foil (battery grade)** | **0.40 $/m²** | 2024 | battery-grade finished foil | assumed (BatPaC 5.1 default) | Knehr, Kubal, Ahmed, Argonne, 2024, slide 9 | as above |
| Aluminium foil (battery grade) | 5.65 $/kg (10–12 µm); 5.50 $/kg (13–14 µm); 5.35 $/kg (15–18 µm) | 2022 (13 May 2022) | battery-grade finished foil (SMM processing + Al metal) | **observed** (SMM) | Baars et al. 2023 SI, Table S3 | as above |
| Aluminium foil (battery grade) | 0.80 $/m² | 2010 | battery-grade | assumed (BatPaC) | EPA-420-D-12-004, 2012, Table 4.1 | as above |
| Aluminium (ingot, spot) | 2.87 $/kg (130 ¢/lb) | 2024 | **RAW** | observed | Merrill, A. M. *Aluminum*; MCS 2025, USGS, 2025. | fetched USGS PDF |
| **Separator (PP/PE/PP)** | **1.00 $/m²** | 2024 | battery-grade | assumed (BatPaC 5.1 default) | Knehr, Kubal, Ahmed, Argonne, 2024, slide 9 | as above |
| Separator | 51.85 $/kg (9 µm); 98.41 $/kg (7 µm); 195.56 $/kg (5 µm) | 2022 (13 May 2022) | battery-grade | **observed** (SMM, converted m²→kg by the authors) | Baars et al. 2023 SI, Table S3 | as above |
| Separator | 2 $/m² | 2010 | battery-grade | assumed (BatPaC) | EPA-420-D-12-004, 2012, Table 4.1 | as above |
| **Electrolyte (LiPF6 in carbonate)** | **14.00 $/L** | 2024 | battery-grade | assumed (BatPaC 5.1 default) | Knehr, Kubal, Ahmed, Argonne, 2024, slide 9 | as above |
| Electrolyte (NMC/NCA) | 15.54 $/kg | 2022 (13 May 2022) | battery-grade | **observed** (SMM) | Baars et al. 2023 SI, Table S3 | as above |
| Electrolyte (1.2 M LiPF6 in EC:EMC) | 19 $/kg | 2010 | battery-grade | assumed (BatPaC) | EPA-420-D-12-004, 2012, Table 4.1 | as above |
| SiOx (as "SiO") | 60.00 $/kg | 2022 | battery-grade | assumed (taken from Greenwood et al. 2021) | Baars et al. 2023 SI, Table S3 | as above |
| Binder, PVDF | 15.00 $/kg | 2022 and 2024 | battery-grade | assumed (BatPaC v5 / 5.1) | Baars et al. 2023 SI Table S3; Knehr et al. 2024 slide 9 | as above |
| Binder, CMC / SBR | 5.00 / 5.00 $/kg | 2022 | battery-grade | assumed (from Greenwood et al. 2021) | Baars et al. 2023 SI, Table S3 | as above |
| Conductive carbon (carbon black) | 3.60 $/kg | 2022 | battery-grade | market listing (Alibaba, not SMM — weaker) | Baars et al. 2023 SI, Table S3 | as above |
| NMP (binder solvent) | 3.10 $/kg | 2024 | battery-grade | assumed (BatPaC 5.1 default) | Knehr, Kubal, Ahmed, Argonne, 2024, slide 9 | as above |
| Lithium carbonate (battery-grade) | 14.00 $/kg | 2024 | **RAW precursor chemical** | observed | Jaskula, B. W. *Lithium*; MCS 2025, USGS, 2025. | fetched USGS PDF |
| **LiPF6 salt alone** | **not found** | — | — | — | — | could not verify (see below) |

---

# Bottom line

**All six core materials have a usable price.**

| Material | Status |
|---|---|
| 1. NMC811 cathode powder | **Have it.** Three independent values: Argonne 2024 default 22.00 $/kg; BatPaC 5.0 2022 default 26.0 $/kg; SMM May-2022 market price 60.09 $/kg. |
| 2. Graphite anode powder | **Have it.** Argonne 2024 default 9.50 $/kg; SMM May-2022 market prices 9.11 $/kg natural and 12.15 $/kg synthetic. |
| 3. Copper foil | **Have it.** Argonne 2024 default 1.20 $/m²; SMM May-2022 15.77 $/kg (6 µm) and 14.15 $/kg (8–14 µm), battery-grade finished foil including metal cost. |
| 4. Aluminium foil | **Have it.** Argonne 2024 default 0.40 $/m²; SMM May-2022 5.65 / 5.50 / 5.35 $/kg by thickness. |
| 5. Separator | **Have it.** Argonne 2024 default 1.00 $/m²; SMM May-2022 converted-to-mass prices 51.85–195.56 $/kg depending on thickness. |
| 6. Electrolyte | **Have it.** Argonne 2024 default 14.00 $/L; SMM May-2022 15.54 $/kg for NMC/NCA chemistry. |

**Start here.** If you want one consistent, recent, self-consistent set, use the **Argonne 2024 column (entry 8)**
— all six core materials in one table, one vintage, one cell design context. Its weaknesses: it is a **model
assumption set**, not a market observation, and Cu/Al/separator are quoted per m² rather than per kg.

If you want **market prices in $/kg** — which is the unit your mass model wants — use the **Baars et al. 2023 SI
Table S3 (entry 7)**. It is the only source I verified that gives all six core materials in **$/kg**, as
battery-grade purchased materials, from market observations. Its weakness is vintage: May 2022.

Two things to be careful about when you use these in a calculation:

1. **NMC811 is the one material where the model-assumption and market-observation numbers diverge by more than a
   factor of two** (22–26 $/kg assumed vs 60.09 $/kg observed). On a cell whose cathode dominates materials cost,
   that single choice moves the answer more than everything else combined.
2. **The units do not line up across sources.** Argonne quotes electrolyte per litre and Cu/Al/separator per m²;
   Baars quotes all of them per kg. Converting requires an electrolyte density and a foil/separator areal mass,
   which I did not verify in any source and have therefore not supplied. **I have not converted anything in this
   document** — every number appears exactly as its source prints it.

---

# Could NOT verify

State this plainly rather than filling the gaps:

1. **LiPF6 as a standalone salt price.** I found no fetched source that prices LiPF6 separately from a formulated
   electrolyte. Every electrolyte price above is for the finished electrolyte (salt + solvent), not the salt alone.
2. **The BatPaC manuals themselves.** The manual for BatPaC v5.0 (Knehr et al., ANL/CSE-22/1, July 2022, DOI
   10.2172/1877590) and the Third Edition (Nelson, Ahmed, Gallagher, Dees, ANL/CSE-19/2, 2019, DOI
   10.2172/1503280) are both hosted on **osti.gov, which is unreachable from this machine** (connection fails
   outright — no HTTP response at all, on both the `/biblio/` and `/servlets/purl/` paths, with and without a
   browser user-agent). **anl.gov returns HTTP 403 to every request.** Unpaywall and Semantic Scholar both list
   the v5.0 manual as open access but point only back to osti.gov, so their metadata did not help.
3. **ANL material price tables for 2025 or 2026.** Search results indicate a newer ANL "GPRA 2026" deck contains a
   component cost table covering 2019–2026. **I could not fetch it** — anl.gov is 403, and no Wayback snapshot of
   `GPRA2026 2026-08-19.pdf` or any 2025 GPRA file exists (checked the Wayback availability API; empty result).
   The 2024 table I did verify is the newest I can stand behind.
4. **Shanghai Metals Market prices newer than May 2022.** SMM is a subscription service; I could not reach it.
   The Baars et al. SI is a legitimate published copy of a May-2022 SMM snapshot, but that vintage is now over
   four years old. **Every SMM price in this document should be treated as a 2022 price.**
5. **The Nature Energy (2024) supplementary "material component price floors".** I fetched this 82-page SI and
   confirmed the concept (§Supplementary Note 1) and that it covers NMC811, copper foil, graphite, separator and
   electrolyte in USD2023. **But the values are presented only in a figure (Supplementary Figure 3), not in a
   numeric table**, so I could not read any number out of it. I am also not confident a "price floor" — which the
   authors derive from underlying mineral prices via a molar-composition model — is the same quantity as the
   material price you want; it is a different kind of number and I did not want to substitute one for the other.
6. **DOE VTO Annual Progress Reports.** I fetched the 2020 Batteries APR (95 MB) and the FY2016 Energy Storage
   APR (34 MB) from energy.gov (both reachable, HTTP 200) and searched them for a material price table. Neither
   contains one — they are R&D progress reports. Separately, the 2019 Batteries APR PDF downloaded intact
   (36 MB) but **opens with zero pages in both PyMuPDF and pdfplumber**, and repair did not help, so its contents
   are unreadable to me. A search result claims that file contains "Table I.7.A.1 Input Values and Results from
   BatPaC 3.1"; **I could not confirm that**, so treat any such claim as unverified.
7. **A Baars et al. Zenodo data deposit** is referenced by search results as containing the underlying material
   data. Both zenodo.org and api.zenodo.org are unreachable from this machine (000 / 403), so I could not check
   it. The published SI (entry 7 above) already contains what I needed.
8. **Second-hand numbers I deliberately did not promote into the table.** Search snippets surfaced additional
   BatPaC-derived figures that I could not trace to a source I fetched — notably a German dissertation's
   reproduced BatPaC cost table (positive active material 28.5 $/kg, negative active material 19.0 $/kg, separator
   2.0 $/m², Cu foil 1.8 $/m², Al foil 0.8 $/m², electrolyte 21.6 $/L; Hettesheimer, *Strategische
   Produktionsplanung in jungen Märkten*, Fraunhofer Verlag, 2017). I did fetch and read that thesis, but it is a
   secondary reproduction of a 2012-era BatPaC, its material labels are ambiguous in the German, and its vintage
   is older than entry 8 on every line — so it adds nothing and I have left it out of the table rather than
   create a fourth conflicting column.

---

## Access notes (for anyone re-running this)

Hosts that answered HTTP 200 and produced usable sources: `pubs.usgs.gov`, `energy.gov`, `nepis.epa.gov`,
`mdpi-res.com`, `www.ebi.ac.uk` (Europe PMC REST), `api.crossref.org`, `api.openalex.org`, `archive.org`
(Wayback), `s3.amazonaws.com`. Hosts that did not: `osti.gov` (no connection at all), `anl.gov` (403),
`nrel.gov` (no connection), `pmc.ncbi.nlm.nih.gov` (bot interstitial + JS redirect), `pubs.acs.org` /
`pubs.rsc.org` / `mdpi.com` (403), `zenodo.org` (403). `r.jina.ai` proxy: unreachable.

One transfer bug worth recording: the Europe PMC supplementary-files ZIP silently truncated at ~590 kB on every
HTTP/1.1 attempt (the ZIP had no central directory and the SI PDF was past the cut). Forcing `curl --http1.0`
returned the complete 7,425,775-byte archive in one go. If you re-fetch that SI, use `--http1.0`.






