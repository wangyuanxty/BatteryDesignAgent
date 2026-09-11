"""Charging-potential gate for AlB55 - checkpointed, ONE state per invocation.

Session constraint: blocking foreground calls only (~10 min each). This script processes the
first incomplete state and exits; completed states persist in comp/gate_state.json. When both
states are done it composes comp/gate_out.json (top-level scalars for log-evaluate).

States:
  full - ONE CHGNet FIRE relaxation of the full-lithium cell; energy from the trajectory
         last frame (relax_energy convention) + density from result['final_structure']
         (profile relaxed_density convention). Identical math to running both separately.
  x04  - relaxation of the x_Li = 0.4 delithiated cell (seeded; nested subset of the
         x = 0.3 removal order, so 0.4 -> 0.3 is one sequential Li-removal step).
         E(x=0.3) is reused from comp/batch3_layered_out.json (same machinery/seed).

charging_potential_v = -[E(0.4) - E(0.3) - 1*e_li] / 1  (last Li removed on charge)
"""
import json
import sys
import traceback
from pathlib import Path

import numpy as np
from pymatgen.core import Composition

from bda.simulators.comp_runner import (
    _li_metal_energy,
    _seed,
    average_voltage,
    build_doped_structure,
    delithiate,
    relax_energy,
)

ROOT = Path(__file__).resolve().parent  # runs/exp/t9_r4/comp
STATE = ROOT / "gate_state.json"
OUT = ROOT / "gate_out.json"
FORMULA = "LiAl0.5B0.5O2"
X_FULL = 1.0
X_DELITH = 0.3

BATCH = json.loads((ROOT / "batch3_layered_out.json").read_text(encoding="utf-8"))
CAND = next(c for c in BATCH["candidates"] if c["name"] == "AlB55")
E_03 = CAND["e_delith_ev"]  # x = 0.3 relaxed energy (sourced from the batch)


def relax_full_once():
    """One FIRE run -> (e_full, converged, density_g_cm3, density_source).

    Energy extraction mirrors relax_energy (trajectory last frame); density extraction
    mirrors profile_voltage.relaxed_density (result final_structure -> relaxed cell)."""
    from chgnet.model import CHGNet
    from chgnet.model.dynamics import AseAtomsAdaptor
    from chgnet.model.dynamics import FIRE
    from chgnet.model.dynamics import StructOptimizer

    struct_full, counts, _ = build_doped_structure(FORMULA)
    atoms = AseAtomsAdaptor().get_atoms(struct_full)
    relaxer = StructOptimizer(model=CHGNet.load(), optimizer_class=FIRE)
    result = relaxer.relax(atoms, fmax=0.1, steps=300, relax_cell=True, verbose=False)
    traj = result.get("trajectory")
    frames = getattr(traj, "trajectory", None) or (traj if isinstance(traj, list) else [])
    e_full, conv = None, False
    if frames:
        last = frames[-1]
        e = last.get("energies", last.get("energy"))
        if isinstance(e, (list, tuple)):
            e = e[-1] if e else None
        f = last.get("forces", last.get("force"))
        if isinstance(f, (list, tuple)):
            f = f[-1] if f else None
        fmax = float(np.abs(np.asarray(f)).max()) if f is not None else None
        if e is not None:
            e_full = float(e)
        conv = bool(e is not None and fmax is not None and fmax <= 0.1)
    if e_full is None:
        e_full = float(atoms.get_potential_energy())
    final = result.get("final_structure")
    dens, src = None, "input-cell"
    if final is not None and hasattr(final, "volume"):
        d = getattr(final, "density", None)
        if d and d > 0:
            dens, src = float(d), "relaxed-final-structure"
    if dens is None:
        if frames:
            cell = frames[-1].get("cell")
            if cell is not None:
                atoms.set_cell(cell)
        dens = float(
            Composition(struct_full.composition.formula).weight
            * len(struct_full)
            / (6.02214076e23 * atoms.get_volume() * 1e-24)
        )
        src = "relaxed-atoms-cell"
    return e_full, conv, dens, src


def relax_x04():
    struct_full, _, _ = build_doped_structure(FORMULA)
    copy = struct_full.copy()
    sub, _ = delithiate(copy, 0.4, _seed(FORMULA))
    return relax_energy(sub)


def main():
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    done = state.get("done", {})
    steps = [("full", relax_full_once), ("x04", relax_x04)]
    for key, fn in steps:
        if key in done:
            continue
        print(f"RUNNING state {key} ...", flush=True)
        try:
            if key == "full":
                e, conv, dens, src = fn()
            else:
                e, conv = fn()
                dens, src = None, None
        except Exception:
            traceback.print_exc()
            sys.exit(2)
        if key == "full":
            done[key] = {"e_full_ev": e, "converged": conv, "density_g_cm3": dens, "density_source": src}
        else:
            done[key] = {"e_04_ev": e, "converged": conv}
        state["done"] = done
        STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        print(f"SAVED {key}: {done[key]}", flush=True)
        return

    # all states done -> compose the gate output
    e_li = _li_metal_energy()
    full, x04 = done["full"], done["x04"]
    v = float(-(x04["e_04_ev"] - E_03 - 1 * e_li) / 1.0)
    n_tot = 12 - round(X_DELITH * 12)
    avg_gate = float(average_voltage(full["e_full_ev"], E_03, n_tot, e_li))
    out = {
        "name": "AlB55",
        "formula": FORMULA,
        "avg_voltage_v": float(CAND["avg_voltage_v"]),
        "avg_voltage_v_from_gate_states": avg_gate,
        "charging_potential_v": v,
        "charging_potential_source": (
            "incremental V(0.4 -> 0.3), the last charge step into the top-of-charge state; "
            "E(0.4) from this gate relaxation, E(0.3) from comp/batch3_layered_out.json "
            "(same machinery/seed, nested removal order)"
        ),
        "n_li_removed_04_03": 1,
        "e_full_ev": full["e_full_ev"],
        "e_04_ev": x04["e_04_ev"],
        "e_03_ev": E_03,
        "e_li_metal_ev": e_li,
        "capacity_mah_g": CAND["capacity_mah_g"],
        "rel_stability_ev_atom": CAND["rel_stability_ev_atom"],
        "density_g_cm3": full["density_g_cm3"],
        "density_source": full["density_source"],
        "converged": bool(full["converged"] and x04["converged"]),
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"COMPLETE: charging_potential_v = {v:.4f} V")
    for k, val in out.items():
        print(f"  {k}: {val}")


if __name__ == "__main__":
    main()
