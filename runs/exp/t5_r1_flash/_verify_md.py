"""MD chain verification: relax + 50-step sanity + Fmax/E diagnostics."""
import time

import numpy as np
from ase import Atoms
from ase.md.langevin import Langevin
from ase.optimize import BFGS

from bda.simulators import md_runner as mr

box = {"molecules": {"EC": 12, "EMC": 16, "PF6": 4, "Li": 4}}
atom_dicts, length_aa, _ = mr._place_molecules(box["molecules"])
pos0 = np.array([a["pos"] for a in atom_dicts])
atoms = Atoms(
    symbols=[a["symbol"] for a in atom_dicts],
    positions=pos0,
    cell=np.identity(3) * length_aa,
    pbc=True,
)
import torch  # noqa: E402
from mace.calculators import mace_mp  # noqa: E402

atoms.calc = mace_mp(
    model="medium", device="cuda" if torch.cuda.is_available() else "cpu"
)
mr._patch_mace_neighborhood()
t0 = time.time()
f0 = np.abs(atoms.get_forces())
print(f"before relax: Fmax = {float(f0.max()):.1f} eV/A", flush=True)
opt = BFGS(atoms, logfile=None)
opt.run(fmax=0.5, steps=120)
print(
    f"relax done in {time.time() - t0:.1f}s | Fmax = "
    f"{float(np.abs(atoms.get_forces()).max()):.3f} | E = {float(atoms.get_potential_energy()):.2f}",
    flush=True,
)
dyn = Langevin(atoms, timestep=1.0, temperature_K=298.15, friction=0.01, fixcm=False)
for step in (25, 50):
    dyn.run(25)
    d = np.linalg.norm(atoms.get_positions() - pos0, axis=1)
    print(f"step {step}: max disp = {float(d.max()):.3f} A", flush=True)
print("VERIFY_OK", flush=True)
