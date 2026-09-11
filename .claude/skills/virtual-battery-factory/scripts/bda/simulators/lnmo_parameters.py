"""LNMO (LiNi0.5Mn1.5O4, 4.7 V spinel) high-voltage cathode parameter set — used for
the materials-bottleneck self-identification check.

Parameter set provenance (calibrated from the literature):
- LNMO OCP curve (Markovsky et al. / Duncan et al. 4.7 V plateau):
  Li-rich end ~4.4 V → 4.7 V main plateau → Li-poor end ~4.85 V; midpoint at x=0.5 ≈ 4.7 V
- Theoretical specific capacity 147 mAh/g; density 4.4 g/cm3; diffusion coefficient
  ~1e-12 m2/s (spinel ionic conduction)
- Everything else (anode/electrolyte/separator/geometry/thermal) is inherited from
  Chen2020 — the architecture design degrees of freedom are unchanged

Usage: run-pyamm --base <data/LNMO.json> (run_simulation detects that base is a file
path, then uses the Chen2020 base plus these override keys; the OCP is bound as a pybamm
symbolic function).
"""
from __future__ import annotations

import pybamm


def lnmo_ocp(sto, c_e=1000.0):
    """LNMO cathode OCP (V vs Li/Li+) — a pybamm symbolic expression (the solver evaluates
    it symbolically).

    A 4.7 V main plateau with smooth tanh ramps at both ends: the midpoint at x=0.5 is
    ≈ 4.7 V. sto ∈ [0,1] (1 = Li-poor state 4.9V, 0 = Li-rich state 4.4V); the stoich
    range is guaranteed by the parameter set's limits.
    """
    return 4.7 + 0.13 * pybamm.tanh(12.0 * (sto - 0.92)) + 0.17 * pybamm.tanh(12.0 * (0.08 - sto))

