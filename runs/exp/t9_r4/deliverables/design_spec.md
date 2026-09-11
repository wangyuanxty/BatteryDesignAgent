# VBF-T9R4-DS-001 Design Specification

t9_r4 - grid-storage cell cathode on the Chen2020 NMC811/graphite profile
Result: HONEST NEGATIVE (no candidate satisfies the full contract; nothing reported as passing)

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

The specification is therefore recorded as NOT ACHIEVED within the six supported families.