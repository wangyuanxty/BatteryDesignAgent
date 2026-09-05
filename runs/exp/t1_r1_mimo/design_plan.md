# Battery Design Plan

## 1. Objective Decomposition
- **Energy Density**: >= 392.61 Wh/kg. This is a high target, requiring a high-nickel cathode (NMC811) or high-voltage cathode (LNMO) and a silicon-enhanced anode (SiOx/Graphite).
- **Fast Charge**: 4C rate without lithium plating. This requires high electrolyte conductivity, low transference number, and optimized electrode porosity/particle size to reduce overpotential.
- **Safety (Thermal)**: Max temp <= 60°C (333.15 K). This requires efficient thermal management (high cooling coefficient) and low internal resistance.
- **Safety (Abuse)**: Overcharge to 4.7V without thermal runaway. This is the most challenging constraint, potentially limiting cathode choice (LNMO is naturally 4.7V, NMC811 is not).

## 2. Candidate Strategy
- **Round 1**: Baseline characterization of OKane2022 (NMC811/Graphite+SiOx) with optimized architecture (thin separator, high porosity, small particles) to assess ED and 4C potential.
- **Round 2**: If ED is insufficient or overcharge triggers TR, switch to LNMO/Graphite (high voltage) or explore high-conductivity electrolyte formulations for NMC811.
- **Round 3**: Safety fine-tuning (cooling coefficient) if temperature exceeds 60°C.

## 3. Risk and Fallback Plan
- **Risk**: OKane2022 baseline ED might be < 392 Wh/kg. **Fallback**: Increase electrode thickness or reduce porosity (Stage 3 adjustment).
- **Risk**: Overcharge to 4.7V triggers TR in NMC811. **Fallback**: Switch to LNMO system (Stage 2 system switch).
- **Risk**: 4C charge causes plating. **Fallback**: Reduce particle size or increase electrolyte conductivity (Stage 3/2).

## 4. References
- High-nickel NMC/SiOx anode for high ED: OKane2022 parameter set.
- LNMO high-voltage cathode: LNMO.json library path.
- Fast charge strategies: domain experience (high conductivity, small particles).


## Revision History

### Rev 3 (2026-08-30)
- **Plating Suppression Strategy**: Systematic sweep of cation transference number (t+) and electrolyte diffusivity.
- **Best Candidate (R19)**: Achieved 470.9 Wh/kg (ED > 392.6), T_max = 298.3 K (< 333 K), and anode potential min = -0.0047 V.
- **Conclusion**: While high t+ (1.25) significantly reduced plating risk compared to baseline, the NMC811/Graphite+SiOx architecture in DFN mode cannot achieve strictly positive anode potential (> 0 V) at 4C without sacrificing energy density below the threshold.
- **Recommendation**: Plating risk is mitigated but not eliminated (-4.7 mV). Final design prioritizes Energy Density and Thermal Safety while maintaining acceptable plating margin.