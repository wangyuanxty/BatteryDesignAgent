"""Thermal runaway sub-model: three side-reaction heat releases (SEI decomposition /
anode-electrolyte / cathode-electrolyte) plus Newtonian cooling.

Conventions (reproducible from the paper's methods section):
- zero-dimensional lumped thermal balance: m·Cp·dT/dt = Σ(Q_i·r_i) − hA(T − T_amb) + Q_nail
- three side-reaction kinetics (standard Arrhenius form, Kim et al. 2019 / Coman et al. 2016):
  R1 SEI decomposition:   r1 = A1·exp(−E1/RT)·x          (x = SEI coverage, initially 1)
  R2 anode-electrolyte:   r2 = A2·exp(−E2/RT)·exp(−a/x)  (as x→0 the SEI protection fails and the reaction runs away)
  R3 cathode-electrolyte: r3 = A3·exp(−E3/RT)·(1−y)·z    (y = cathode decomposition degree; z = electrolyte availability)
- side-reaction consumption: dx/dt = −r1; a simplification of dy/dt = r3·y (keeping the
  two states x/y)
- stiff ODE → scipy solve_ivp(method="BDF", rtol=1e-8, atol=1e-10)
- trigger test: dT/dt > 1 K/s (temperature-rise inflection) or T ≥ 573 K (300 °C engineering red line)
- nail penetration: Q_nail = I_sc²·R_short (local short-circuit heating), injected as a
  constant heat source term
- overcharge coupling: the T_max_K of the run-pyamm overcharge protocol is fed in as the
  initial temperature

Parameters (Kim et al. 2019 thermal-runaway calibration for lithium-ion cells, J/kg basis):
  R1: A=1.667e15 s⁻¹  Ea=1.3508e5 J/mol  ΔH=2.57e5 J/kg
  R2: A=2.5e13 s⁻¹    Ea=1.3508e5 J/mol  ΔH=1.714e6 J/kg
  R3: A=1.75e14 s⁻¹   Ea=1.65e5 J/mol   ΔH=1.13e5 J/kg
  coverage factor a = 0.05 (R2's sensitivity to the residual SEI)
  the cell heat capacity m·Cp and the cooling hA are passed in by the caller (defaults
  1 kg·Cp≈1000 J/K, hA=0.05 W/K as an adiabatic approximation)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

# ---- three side-reaction parameters (literature calibration, J/kg basis; m = active material mass in kg) ----
R1 = {"A": 1.667e15, "Ea": 1.3508e5, "dH": 2.57e5}
R2 = {"A": 2.5e13, "Ea": 1.3508e5, "dH": 1.714e6}
R3 = {"A": 1.75e14, "Ea": 1.65e5, "dH": 1.13e5}
COVERAGE_FACTOR = 0.05  # retained (historical parameter name); the R2 coverage factor now uses the (1-x) form
R_GAS = 8.314
# Active material mass as a fraction of the whole cell: dH is on an active-material basis
# (J/kg) while the whole-cell heat capacity mcp includes inert components (current
# collectors/separator/casing), so the energy released into the whole cell must be scaled by
# this fraction — otherwise ΔT is overestimated by ~3x.
ACTIVE_MASS_FRAC = 0.3

# Trigger test
TRIGGER_DTDT = 1.0   # K/s: temperature-rise inflection
TRIGGER_T_K = 573.0  # 300 ℃ engineering red line


def _rhs(t: float, y: np.ndarray, mcp: float, hA: float, t_amb: float, q_nail: float) -> np.ndarray:
    """y = [T_K, x_sei, y_cath, u_anode]; returns [dT/dt, dx/dt, dy/dt, du/dt].

    Reactant depletion guarantees energy conservation (the temperature stays bounded):
    - x (SEI amount) is consumed by R1; R3 saturates via (1-y) (it stops as y→1);
    - u (anode combustibles) is consumed by R2 — earlier versions lacked this depletion
      term, which made the temperature blow up numerically (10^15 K).
    """
    t_k, x, yc, u = y
    # State clamp: x/y/u ∈ [0,1] (solver numerical out-of-range protection, physical domain)
    x = min(max(x, 0.0), 1.0)
    yc = min(max(yc, 0.0), 1.0)
    u = min(max(u, 0.0), 1.0)
    inv_rt = 1.0 / (R_GAS * t_k)
    # Rate clamp (mass-transport limitation): the Arrhenius pre-exponential factor has no
    # physical upper bound at high temperature (10^15 s⁻¹), and without a cap the
    # instantaneous power becomes infinite and energy is not conserved (T_max explodes to
    # the 10^8 K range). Reactant conversion is transport-limited, so an engineering cap of
    # 100 s⁻¹ is used (corresponding to ms-scale depletion, capping energy conservation).
    RATE_CAP = 1e2
    # Note: x gets no floor — at x=0 r1 must truly be 0 (SEI exhaustion stops it).
    # The earlier max(x, 1e-12) made r1 = A1·exp·1e-12 ≈ 1.6e3 > cap at high temperature →
    # R1 burns at full power forever (T blows up).
    r1 = min(R1["A"] * np.exp(-R1["Ea"] * inv_rt) * x, RATE_CAP)
    # R2 coverage factor = (1-x): with intact SEI (x=1) the anode-electrolyte reaction is
    # suppressed (factor=0), and it runs away (factor→1) after the SEI decomposes (x→0);
    # it is limited by the consumption of u (anode combustibles), so the energy is bounded.
    r2 = min(R2["A"] * np.exp(-R2["Ea"] * inv_rt) * (1.0 - x) * u, RATE_CAP)
    r3 = min(R3["A"] * np.exp(-R3["Ea"] * inv_rt) * (1.0 - yc), RATE_CAP)
    q_gen = (R1["dH"] * r1 + R2["dH"] * r2 + R3["dH"] * r3) * ACTIVE_MASS_FRAC
    dtdt = (q_gen - hA * (t_k - t_amb) + q_nail) / mcp
    # First-order reactant consumption (∫r dt = amount consumed = 1, energy conserved):
    # the second-order form (-r2·u) makes u approach 0 asymptotically and never reach it,
    # so ∫r dt diverges logarithmically → excess energy (T_max blows up).
    dxdt = -r1
    dydt = r3  # r3 already contains the (1-yc) saturation factor
    dudt = -r2  # r2 already contains the u reactant factor
    return np.asarray([dtdt, dxdt, dydt, dudt])


def run_thermal_runaway(
    t_init_k: float = 298.15,
    x_sei_init: float = 1.0,
    t_max_s: float = 3600.0,
    mcp_j_k: float = 1000.0,
    hA_w_k: float = 0.05,
    t_amb_k: float = 298.15,
    q_nail_w: float = 0.0,
    mass_kg: float | None = None,
) -> dict:
    """Integrate the thermal runaway ODE. Returns the temperature curve and the trigger verdict.

    Note: dH is in J/kg (on an active-material mass basis). This implementation sums the
    three side-reaction heat releases as dH·r_i (r_i is a rate of order s⁻¹) and normalizes
    by mcp — when mcp is the whole-cell heat capacity (about 1 kg × 1000 J/kg/K), dH must be
    read as the "whole-cell equivalent heat of release" (J). To preserve the literature
    magnitude, the caller should pass mcp ≈ cell mass × specific heat, and be aware that
    under this simplification the trigger temperature boundary agrees with the literature
    (verified by the sanity tests).
    **mass_kg takes precedence**: when provided, mcp = mass_kg × 900 (approximate cell
    specific heat in J/kg/K), overriding the mcp parameter — nail penetration/thermal
    runaway must pass the cell's actual mass (taken mechanically from calc-energy mass_kg),
    otherwise mcp defaults to 1000 (≈ a 1 kg reference cell) and dT/dt is systematically
    underestimated for small cells.
    """
    if mass_kg is not None:
        mcp_j_k = mass_kg * 900.0
    y0 = np.asarray([t_init_k, x_sei_init, 0.0, 1.0])
    sol = solve_ivp(
        _rhs,
        (0.0, t_max_s),
        y0,
        method="BDF",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.2,  # reaction depletion happens on the ms~0.1s scale, so the step cap must be below that
        args=(mcp_j_k, hA_w_k, t_amb_k, q_nail_w),
        dense_output=True,
    )
    t_grid = np.linspace(0.0, t_max_s, 2001)
    y_grid = sol.sol(t_grid)
    t_k = y_grid[0]
    dtdt = np.gradient(t_k, t_grid)
    trigger_idx = int(np.argmax(dtdt > TRIGGER_DTDT)) if np.any(dtdt > TRIGGER_DTDT) else -1
    if trigger_idx < 0 and np.any(t_k >= TRIGGER_T_K):
        trigger_idx = int(np.argmax(t_k >= TRIGGER_T_K))
    triggered = trigger_idx >= 0
    return {
        "triggered": bool(triggered),
        "trigger_time_s": float(t_grid[trigger_idx]) if triggered else None,
        "T_max_K": float(t_k.max()),
        "T_final_K": float(t_k[-1]),
        "dTdt_max_K_s": float(dtdt.max()),
        "T_series_K": [round(float(v), 2) for v in t_k[::20]],
        "t_series_s": [round(float(v), 2) for v in t_grid[::20]],
        "params": {
            "t_init_K": t_init_k,
            "mcp_J_K": mcp_j_k,
            "hA_W_K": hA_w_k,
            "t_amb_K": t_amb_k,
            "q_nail_W": q_nail_w,
            "source": "Kim et al. 2019 / Coman et al. 2016 Arrhenius three side reactions, zero-dimensional lumped thermal balance",
        },
    }


def cmd_run_thermal_runaway(args) -> int:
    try:
        t_init_k = args.t_init
        if args.sim:
            # Overcharge/discharge simulation output coupling: read its T_max_K as the
            # thermal runaway initial temperature (automatic chaining)
            sim = json.loads(Path(args.sim).read_text(encoding="utf-8-sig"))
            if "T_max_K" not in sim:
                raise ValueError(f"--sim file is missing the T_max_K key (expected a run-pyamm output): {args.sim}")
            t_init_k = float(sim["T_max_K"])
        out = run_thermal_runaway(
            t_init_k=t_init_k,
            x_sei_init=args.x0,
            t_max_s=args.t_max,
            mcp_j_k=args.mcp,
            hA_w_k=args.hA,
            t_amb_k=args.t_amb,
            q_nail_w=args.q_nail,
            mass_kg=getattr(args, "mass_kg", None),
        )
    except (ValueError, RuntimeError) as e:
        print(f"bda error: {e}", file=sys.stderr)
        return 1
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0
