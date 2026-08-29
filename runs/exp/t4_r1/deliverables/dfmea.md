# Design FMEA (qualitative version) — VBF-T4R1-DFMEA-01

Qualitative version, based on simulation signals; severity/occurrence rated high/medium/low from the magnitude of the simulated value vs threshold. RPN = qualitative S×O matrix.

| Failure mode | Failure cause | Simulation signal (detectability basis) | Severity | Occurrence | Design-side mitigation |
|---|---|---|---|---|---|
| Negative electrode lithium plating (fast charge) | Electrolyte salt depletion → local conductivity/diffusivity collapse at anode end-of-charge | anode_potential_v min: baseline −184.8 mV → final design +20.5 mV | high (dendrite → internal short) | low (positive margin in final design; was high in rounds 3–5) | LHCE transport profile (κ 1.1 flat, D_e 3e-10 flat, t⁺ 0.6), fine graphite (2.5 µm) exchange area, h = 80 keeps 45 °C charge cool enough |
| Thermal runaway risk (temperature rise exceeds limit) | Polarization heat at 4C/45 °C charge | T_max_K 327.70 K vs 333.15 K limit (margin 5.4 K) | high (thermal runaway) | low | Immersion cooling h = 80 W/m²/K; lower polarization heat via transport fixes |
| Electrolyte oxidative decomposition (voltage window) | Electrolyte HOMO vs cathode potential | Not quantified — real_compute=false, no DFT HOMO/IE-EA endorsement ran | medium | low | Standard window 2.5–4.2 V below typical EC-class oxidation onset (domain experience); recommend DFT endorsement before production |
| Insufficient capacity | Active material / geometry shortfall | 1C capacity 5.0368 Ah vs nominal 5.0 Ah (100.7 %) | medium | low | Verified at 1C; 4C charge voltage-limited (4.2 V after 0.419 Ah runner-scale) — acceptable per criteria |
| −20 °C power/capacity loss (extreme-cold mission) | Electrolyte transport freeze-out | retention 0.99267 (cold-soak, no self-heating) — but computed under flat-transport idealization | medium | medium (model optimism: real LHCE κ(−20 °C) ≈ 0.3 S/m estimate; margin 4.27 pt) | Confirm electrolyte −20 °C conductivity by measurement; keep self-heating margin if h reduced |

## Conclusion

Highest-risk items: −20 °C electrolyte transport optimism (occurrence medium — the only item without a comfortable simulation margin once real transport properties are considered) and electrolyte oxidation stability (not quantified without true-compute endorsement). Both have mitigations recorded; the plating and thermal items that dominated the design effort (rounds 3–6) are mitigated in the final design with positive margins. Complete FMEA including process/supplier failures: N/A (beyond pure simulation boundary).
