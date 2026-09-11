# t9_r4 — Session Notes

Headless design task: grid-storage cell cathode on Chen2020 NMC811/graphite. Window: CHGNet
computed avg voltage >= 4.6 V; charging potential <= 4.8 V; not in the 115-material catalogue;
outside the 102-point hull; six supported families; ED >= 327.18 Wh/kg (calc-energy, contract
convention) on the mapped cell (constant OCP = V_avg, capacity = 0.9 x C, SEI = Chen2020 k0);
no plating at 4C/45C; no TR trigger; SEI <= 500 nm at 100 x 1C; true-voltage guard.

## Key measured facts (tool outputs, this session)

- Baseline Chen2020 1C discharge: 4.948 Ah, 17.39 Wh, mass 0.04345 kg, ED 400.29 Wh/kg,
  midpoint 3.935 V (`cell/baseline_1c_spme.json`, `cell/baseline_1c_energy.json`).
- LNMO.json base discharge (precedent): 5.11 Ah, 4088 s, T_max 309.5 K — anode-limited
  termination with plateau OCP (`cell/lnmo_ref_1c_spme.json`).
- Constant-OCP mapping test (OCP=4.65 scalar via --params): works in PyBaMM; discharge
  5.118 Ah, 3685 s, ends at 2.5 V, mid 4.3995 V, T_max 312.3 K (`cell/constocp_test_1c.json`).
- Chen2020 geometry (dump): pos 75.6 um / eps_am 0.665 / rho 3262, neg 85.2 um / 0.75 / 1657,
  sep 12 um / 0.47 / 397, CC 16/12 um Al/Cu, area 0.1027 m2. Positive active mass
  M_am = 16.84 g; calc-energy mass (porosity-corrected layers, no electrolyte) = 43.45 g.

## ED feasibility analysis (decisive)

- Family capacity bounds (C_comp = 0.7 x F/3.6 / MW): layered 172-285, olivine <= 128,
  spinel <= 113, tavorites <= 111, NASICON <= 46 mAh/g.
- Non-layered ED: even LiNiPO4 at its true 5.1 V gives 0.9 x 116.6 x M_am / 43.45 g
  => ~317 Wh/kg < 327.18. Non-layered families are ED-infeasible under the 0.9 rule.
  => the candidate MUST be layered LiMO2.
- Mapped-cell ED: with plateau OCP the fixed-cell discharge is anode-limited (~5.1 Ah,
  LNMO.json precedent behavior) -> ED ~ 450-500 Wh/kg for any layered at 4.6-4.8 V.
  With candidate crystal density override (precedent), ED >= ~400 Wh/kg. Both readings
  clear 327.18 for layered V in [4.6, 4.8]. The binding constraint is the computed voltage.

## Screening results

- Round 1 (TM-redox layered, 14): band 2.56-3.99 V. Best NiFe55 3.990, LiFeO2 3.943.
  Cu layered computes 3.5-3.8 (CHGNet prices Cu low). LiCuO2 3.707. ALL < 4.6.
- Round 2 (Cr mixes + d0/d10 O-redox, 14): d0/d10 line at the window edge —
  LiAlO2 4.598 (2 mV short!), LiZnO2 4.492, LiGaO2 4.479, LiScO2 4.298; mixes 3.55-4.25.
  Ionic-radius trend: smaller d0 cation -> higher V (Al 0.535 A > Ga 0.62 > Sc 0.745).
- Round 3 (B-Al d0 system, 14, done): **AlB55 (LiAl0.5B0.5O2) 4.6413 V - the first of 42
  candidates to clear the 4.6 V window (margin 41 mV).** LiBO2 4.253: pure B is NOT higher
  than LiAlO2 (4.598) - the radius trend breaks at B; the pass is a sharp 50:50 mixing
  peak (neighbors: BGa55 4.504, GaAl55 4.494, AlB95 4.488, AlB82 4.464, GaAl91 4.454,
  AlB91 4.443, AlB73 4.429, BAl73 4.226, LiBO2 4.253). Peak source: the delithiated x=0.3
  state sits ~1.5 eV off the B-content trend -> sensitivity risk; charging-potential
  profile (comp/profile_voltage.py) is the co-gate.
- Known-set layered reference: LiNiO2 3.890 (max), LiNi0.5Mn0.5O2 3.701, LiCoO2 3.361,
  LiCrO2 3.558 (documented - excluded), LiMnO2 3.143.

- Envelope adjudication (comp_envelope_check.py): PASS on both modes. --formula mode
  independently re-computed AlB55: avg 4.6354 V (6 mV below batch 4.6413 - relaxation
  noise; still >= 4.6), capacity 324.38, stab -2.3901, "PASS (outside envelope)", 115
  catalogue members checked; --point mode (4.6413, 324.38, -2.3912): "PASS (outside
  envelope)". Not in the catalogue, outside the 102-point hull.
- QE pseudopotentials: b_pbe_v1.4.uspp.F.UPF DOES exist in sssp/efficiency (earlier
  "no B pseudo" note was a bad glob). Al.pbe-n-kjpaw_psl.1.0.0.UPF confirmed. Added
  Al + B entries to _PSEUDO_FILES in bda/simulators/qe_runner.py (2-line extension,
  recorded honestly) -> run-qe is feasible for AlB55 (48-atom supercell, ~3 pw.x runs).

## Cell mapping design (for the finalist)

Mirror LNMO.json precedent + the contract's fixed rule:
- "Positive electrode OCP [V]": V_avg (scalar, verified working), entropic change 0.0
- cutoffs: lower 2.5 V, upper 4.8 V (the declared charging-potential limit)
- "Nominal cell capacity [A.h]": 0.9 x C_comp x M_am(candidate density)
- "Positive electrode density [kg.m-3]": candidate density from the profile script
  (CHGNet-relaxed cell; sourced)
- "Positive electrode molar mass [kg.mol-1]": candidate MW (sourced from run-comp C)
- "Positive electrode maximum concentration [mol.m-3]": density / MW (consistent)
- "Initial concentration in positive electrode [mol.m-3]": 0.3 x c_max (top-of-charge x=0.3)
- stoich limits [1.0, 0.3]; electrons transferred 1.0
- SEI keys: untouched (baseline k0, per rule)
- transport/conductivity: inherited from Chen2020 (same family, no fabricated values)

Anode-limited discharge with plateau OCP (cathode over-lithiation beyond the 0.7-Li window
at the tail) = fixed-cell signature, same as the LNMO.json precedent; label honestly in the
report; report delivered capacity AND the rule capacity 0.9 x C_comp x M_am and
ED_active = V x C x 0.9.

## Charging-potential plan

Profile script `comp/profile_voltage.py` reuses run-comp machinery: relaxes x = 1.0 and
0.9..0.3 (nested seeded subsets), charging_potential_v = incremental V(0.4 -> 0.3) (the
last charge step into the top-of-charge state). Co-gate with the window: for d0 O-redox
the top-end could exceed 4.8 V. Also outputs the relaxed-cell density for the mapping.

## True-voltage guard plan

- Primary: run-qe (own QE, Li-metal reference) on the finalist if budget allows.
- Secondary: literature-consistent evidence. For the d0 O-redox line: Li-rich layered
  oxides (Li2MnO3-class) activate O redox at a 4.4-4.7 V plateau — the mechanism basis.
  Honest caveat: no direct experimental LiAlO2/LiBO2 cathode data; the guard will say so.
- Layered is not an overestimate-prone family (NMC811 self-calibrates 3.80 vs 3.8).

## Risks

- If B-Al caps below 4.6: layered envelope documented at ~2.5-4.6 V -> window infeasible in
  all six families -> honest negative result with escalation questioning (three layers).
- If a finalist passes 4.6 but charging_potential_v > 4.8: compositional adjustment or next.
- Plateau-OCP artifacts (over-lithiation tail, zero entropic heat): labeled, not hidden.

## Closing (2026-09-10) — HONEST NEGATIVE RESULT

- Charging-potential gate (comp/gate_charging.py, checkpointed: one CHGNet relaxation per
  blocking call): AlB55 **charging_potential_v = 7.410 V** (V(0.4->0.3); E(0.4) -295.256 eV,
  E(0.3) -285.968 eV, n=1) — 2.6 V above the 4.8 V electrolyte limit. FAIL, decisive.
- Diagnosis: the round-3 window pass was the signature of a pathological x=0.3 endpoint
  (~9 eV off its composition neighbors); the final Li removal costs 7.4 V. Fatal for the
  whole d0/d10 O-redox layered line — any avg >= 4.6 in that family comes from the same
  diseased endpoint. LiAlO2 (4.598) fails the window regardless.
- Two decisive walls: (i) TM-redox layered caps ~4.0 V; (ii) the only >4.6 V layered
  mechanism fails the 4.8 V charging gate. Plus (iii) non-layered families are
  ED-infeasible under the 0.9-capacity rule. Over-determined negative.
- Round 4: propose4 -> funnel4 (0 passed / 2 rejected) -> mechanical evaluate (AlB55 fail
  checked=2, LiAlO2 fail checked=1) -> final entry (verdict: negative) — LAST log entry.
- Close loop: envelope --formula mode re-computed AlB55 independently (4.6354 V, 6 mV from
  the batch) PASS outside envelope; public-catalogue search: no results for LiAlO2 /
  LiAl0.5B0.5O2 cathodes ("not found in the searched scope"); run-qe not performed (no
  survivor to Stage 5; Al/B pseudopotentials were added to _PSEUDO_FILES in preparation).
- Deliverables: 7 documents (md + PDF) in deliverables/; verify-deliverables ALL PASS;
  report.html rendered.

## Files

- design_plan.md, log.jsonl (entry 0 criteria + plan + rounds 1-3 propose/funnel +
  mechanical evaluate entries r1/r2), NOTES.md (this file)
- comp/batch{1,2,3}_layered{,_out}.json, comp/eval/*.json (per-candidate scalars),
  comp/make_eval_files.py, comp/make_eval_r4.py, comp/profile_voltage.py,
  comp/gate_charging.py + gate_state.json + gate_out.json (charging gate, checkpointed)
- cell/: baseline_1c_spme.json, baseline_1c_energy.json, lnmo_ref_1c_spme.json,
  constocp_test_1c.json, params_constocp_test.json, params_empty.json
- dump_chen2020.py, log_setup.py, followup_log.py, propose4_log.py, closing_log.py,
  final_log.py, make_deliverables.py
- deliverables/ (7 documents md+PDF, VBF-T9R4 numbering), report.html
