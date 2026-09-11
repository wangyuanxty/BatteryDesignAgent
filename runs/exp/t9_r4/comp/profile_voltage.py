"""Voltage profile over the delithiation window for layered LiMO2 candidates.

Reuses the run-comp machinery EXACTLY (same prototype builder, same seeded delithiation,
same CHGNet FIRE relaxation, same bcc Li metal reference) and additionally:
- relaxes the delithiated states at x = 0.9 ... 0.3 (nested seeded subsets -> each x is a
  consistent prefix of the removal order, so the incremental voltages are sequential
  Li-removal steps);
- charging_potential_v = incremental voltage of the LAST removal step (0.4 -> 0.3), i.e.
  the potential at which charging finishes into the top-of-charge state x = 0.3;
- avg_voltage_v re-derived from the endpoints (sanity check against the run-comp batch);
- density_g_cm3 from the CHGNet-relaxed full-lithium cell (used by the cell mapping).

IN: JSON {"candidates": [{"formula": ..., "name": ...}]}  OUT: {"profiles": [...]}
"""
import json
import sys
from pathlib import Path

import numpy as np
from pymatgen.core import Composition

from bda.simulators.comp_runner import (
    _X_DELITH,
    _seed,
    average_voltage,
    build_doped_structure,
    delithiate,
    relax_energy,
)
from bda.simulators.comp_runner import _li_metal_energy

X_VALUES = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]


def relaxed_density(struct):
    """CHGNet-relaxed cell density (g/cm3). The relaxer returns the final structure via
    result['final_structure'] (pymatgen) when available; otherwise falls back to the
    last trajectory frame's cell or the input cell (labeled in the output)."""
    from chgnet.model import CHGNet
    from chgnet.model.dynamics import AseAtomsAdaptor
    from chgnet.model.dynamics import FIRE
    from chgnet.model.dynamics import StructOptimizer

    atoms = AseAtomsAdaptor().get_atoms(struct)
    relaxer = StructOptimizer(model=CHGNet.load(), optimizer_class=FIRE)
    result = relaxer.relax(atoms, fmax=0.1, steps=300, relax_cell=True, verbose=False)
    final = result.get("final_structure")
    if final is not None and hasattr(final, "volume"):
        d = final.density
        if d is not None and d > 0:
            return float(d), "relaxed-final-structure"
    traj = result.get("trajectory")
    frames = getattr(traj, "trajectory", None) or (traj if isinstance(traj, list) else [])
    if frames:
        cell = frames[-1].get("cell")
        if cell is not None:
            atoms.set_cell(cell)
    d = float(Composition(struct.composition.formula).weight * len(struct) / (6.02214076e23 * atoms.get_volume() * 1e-24))
    return d, "relaxed-atoms-cell"


def profile_candidate(formula: str, e_li: float):
    struct_full, counts, _ = build_doped_structure(formula)
    seed = _seed(formula)
    e_full, conv_full = relax_energy(struct_full)
    n_li_full = sum(1 for s in struct_full if s.specie.symbol == "Li")

    energies = {1.0: (e_full, conv_full)}
    for x in X_VALUES:
        copy = struct_full.copy()
        sub, _ = delithiate(copy, x, seed)
        e_x, conv_x = relax_energy(sub)
        energies[x] = (e_x, conv_x)

    def n_removed(x_from, x_to):
        return round(x_from * n_li_full) - round(x_to * n_li_full)

    def incr_v(x_from, x_to):
        n = n_removed(x_from, x_to)
        e_hi, _ = energies[x_from]
        e_lo, _ = energies[x_to]
        return float(-(e_hi - e_lo - n * e_li) / n), n

    profile = {}
    steps = [(1.0, 0.9), (0.9, 0.8), (0.8, 0.7), (0.7, 0.6), (0.6, 0.5), (0.5, 0.4), (0.4, 0.3)]
    for hi, lo in steps:
        v, n = incr_v(hi, lo)
        profile[f"{lo:.1f}_to_{hi:.1f}"] = {"v": v, "n_li_removed": n}

    n_tot = n_removed(1.0, _X_DELITH)
    avg_v = average_voltage(e_full, energies[_X_DELITH][0], n_tot, e_li)
    charging_v = profile["0.3_to_0.4"]["v"]
    max_incr = max(p["v"] for p in profile.values())
    dens, dens_src = relaxed_density(struct_full)
    all_conv = conv_full and all(c for _, c in energies.values())

    return {
        "formula": formula,
        "realized_tm_counts": counts,
        "avg_voltage_v": float(avg_v),
        "charging_potential_v": charging_v,
        "max_incremental_v": max_incr,
        "incremental_voltage_v": profile,
        "e_full_ev": e_full,
        "e_delith_ev": energies[_X_DELITH][0],
        "e_li_metal_ev": e_li,
        "density_g_cm3": dens,
        "density_source": dens_src,
        "converged": bool(all_conv),
    }


def main(in_path, out_path):
    data = json.loads(Path(in_path).read_text(encoding="utf-8"))
    e_li = _li_metal_energy()
    out = []
    for c in data["candidates"]:
        try:
            p = profile_candidate(str(c["formula"]), e_li)
            p["name"] = c.get("name", c["formula"])
            out.append(p)
        except ValueError as exc:
            out.append({"name": c.get("name"), "formula": c.get("formula"), "error": str(exc)})
    Path(out_path).write_text(json.dumps({"profiles": out}, indent=2), encoding="utf-8")
    for p in out:
        if "error" not in p:
            print(f"{p['name']}: avg={p['avg_voltage_v']:.4f} V charging={p['charging_potential_v']:.4f} V "
                  f"max_incr={p['max_incremental_v']:.4f} V density={p['density_g_cm3']:.3f} g/cm3 ({p['density_source']}) "
                  f"conv={p['converged']}")
        else:
            print(f"{p['name']}: ERROR {p['error']}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
