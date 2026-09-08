"""OpenMM smoke test: ECx12 + EMCx16 OPLS-AA, 10 ps NVT (no ions).

Force-field assembly path validation: LigParGen OPLS-AA XML + PDB templates,
deterministic grid box (~34 AA), LangevinMiddle 298 K, 10 ps.
"""
import math

import numpy as np
from openmm import LangevinMiddleIntegrator, unit
from openmm.app import PME, PDBFile, ForceField, StateDataReporter

R = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_flash"
SPECIES = [("EC", 12), ("EMC", 16)]


def load_tmpl(name):
    """Parse ATOM lines of the LigParGen PDB -> (atomnames, symbols, coords)."""
    names, syms, coords = [], [], []
    for line in open(f"{R}/_opls_{name}.pdb"):
        if line.startswith("ATOM"):
            atom_name = line[12:16].strip()
            coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            names.append(atom_name)
            syms.append(atom_name[0])
    return np.array(coords), syms, names


tmpls = {n: load_tmpl(n) for n, _ in SPECIES}
nmol = sum(c for _, c in SPECIES)
grid = max(1, int(math.ceil(nmol ** (1.0 / 3.0))))
gap = 7.0
rng = np.random.default_rng(42)

import re as _re


def xml_bonds(name):
    t = open(f"{R}/_opls_{name}2.xml").read()
    return [(int(a), int(b)) for a, b in _re.findall(r'<Bond from="(\d+)" to="(\d+)"/>', t)]


atom_lines, serial, resid = [], 1, 1
conect_lines = []
for name, count in SPECIES:
    coords, syms, names = tmpls[name]
    bonds = xml_bonds(name)
    center0 = coords.mean(axis=0)
    for slot in range(count):
        s0 = serial
        gi = slot // (grid * grid); rem = slot % (grid * grid)
        gj, gk = rem // grid, rem % grid
        center = np.array([gi + 0.5, gj + 0.5, gk + 0.5]) * gap + rng.uniform(-0.05 * gap, 0.05 * gap, 3)
        for a, sym in enumerate(syms):
            x, y, z = (coords[a] - center0) + center
            atom_lines.append(
                f"ATOM  {serial:5d} {names[a]:4s} {name:>3s} {resid:5d}    "
                f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {sym}"
            )
            serial += 1
        for i, j in bonds:
            conect_lines.append(f"CONECT{s0 + i:5d}{s0 + j:5d}")
        resid += 1

box_len = (grid + 0.5) * gap
cryst = (f"CRYST1{box_len:9.3f}{box_len:9.3f}{box_len:9.3f}  90.00  90.00  90.00 P 1           1")
pdb_path = f"{R}/_box_nions.pdb"
with open(pdb_path, "w") as f:
    f.write("\n".join([cryst] + atom_lines + conect_lines) + "\nEND\n")

ff = ForceField(f"{R}/_opls_ec2.xml", f"{R}/_opls_emc2.xml")
pdb = PDBFile(pdb_path)
system = ff.createSystem(
    pdb.topology,
    nonbondedMethod=PME,
    nonbondedCutoff=1.0 * unit.nanometer,
    constraints=None,
)
integrator = LangevinMiddleIntegrator(298.15 * unit.kelvin, 1.0 / unit.picosecond,
                                      1.0 * unit.femtosecond)
from openmm.app import Simulation  # noqa: E402

sim = Simulation(pdb.topology, system, integrator)
sim.context.setPositions(pdb.positions)
sim.minimizeEnergy()
sim.context.setVelocitiesToTemperature(298.15 * unit.kelvin)
sim.reporters.append(
    StateDataReporter(f"{R}/_smoke.log", 100, step=True, potentialEnergy=True,
                      temperature=True, separator=" ")
)
sim.step(10000)
print("SMOKE OK")
