"""Production OPLS-AA electrolyte MD: EC12/EMC16/LiPF6(4) box, 0.1 ns NVT.

Ion parameters from the ILFF library (il.ff: Li Aqvist; P/FP JCS Perkin2 1999).
D_Li from unwrapped MSD fit (last 500 points, Einstein relation).
Outputs: df_endorse_md_out_opls.json
"""
import json
import math

import numpy as np
from openmm import LangevinMiddleIntegrator, Vec3, unit
from openmm.app import (ForceField, PME, PDBFile, Simulation,
                        StateDataReporter)

R = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_flash"
LJ_EC = [1.0, 1.0, 1.0]  # placeholder unused
SPECIES = [("EC", 12), ("EMC", 16), ("PF6", 4), ("LI", 4)]


def parse_pdb_tmpl(name):
    names, syms, coords = [], [], []
    for line in open(f"{R}/_opls_{name}.pdb"):
        if line.startswith("ATOM"):
            an = line[12:16].strip()
            coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            names.append(an)
            syms.append(an[0])
    return np.array(coords), syms, names


def pf6_geom():
    """Octahedron from ILFF zmat: r(P-F)=1.606 A."""
    p = np.zeros(3)
    fs = [np.array([1.606, 0.0, 0.0]), np.array([-1.606, 0.0, 0.0]),
          np.array([0.0, 1.606, 0.0]), np.array([0.0, -1.606, 0.0]),
          np.array([0.0, 0.0, 1.606]), np.array([0.0, 0.0, -1.606])]
    return np.vstack([p] + fs), ["P1", "F2", "F3", "F4", "F5", "F6", "F7"]


tmpls = {}
for n, _ in SPECIES:
    if n in ("EC", "EMC"):
        tmpls[n] = parse_pdb_tmpl(n)
    elif n == "PF6":
        g, an = pf6_geom()
        tmpls[n] = (g, [a[0] for a in an], an)
    else:
        tmpls[n] = (np.zeros((1, 3)), ["Li"], ["LI1"])

nmol = sum(c for _, c in SPECIES)
grid = max(1, int(math.ceil(nmol ** (1.0 / 3.0))))
gap = 5.45
rng = np.random.default_rng(42)

atom_lines, conect_lines, serial, resid = [], [], 1, 1
for name, count in SPECIES:
    coords, syms, names = tmpls[name]
    bonds = []
    if name in ("EC", "EMC"):
        import re as _re
        t = open(f"{R}/_opls_{name}2.xml").read()
        bonds = [(int(a), int(b)) for a, b in _re.findall(r'<Bond from="(\d+)" to="(\d+)"/>', t)]
    elif name == "PF6":
        bonds = [(0, i) for i in range(1, 7)]
    center0 = coords.mean(axis=0)
    for slot in range(count):
        s0 = serial
        gi = slot // (grid * grid); rem = slot % (grid * grid)
        gj, gk = rem // grid, rem % grid
        center = np.array([gi + 0.5, gj + 0.5, gk + 0.5]) * gap + rng.uniform(-0.05 * gap, 0.05 * gap, 3)
        for a in range(len(coords)):
            x, y, z = (coords[a] - center0) + center
            atom_lines.append(
                f"ATOM  {serial:5d} {names[a]:4s} {name:>3s} {resid:5d}    "
                f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {syms[a]}"
            )
            serial += 1
        if bonds:
            for i, j in bonds:
                conect_lines.append(f"CONECT{s0 + i:5d}{s0 + j:5d}")
        resid += 1

box_len = (grid + 0.5) * gap
pdb_path = f"{R}/_box_full.pdb"
with open(pdb_path, "w") as f:
    f.write(f"CRYST1{box_len:9.3f}{box_len:9.3f}{box_len:9.3f}  90.00  90.00  90.00 P 1           1\n")
    f.write("\n".join(atom_lines + conect_lines) + "\n")
    f.write("END\n")

ff = ForceField(f"{R}/_opls_ec2.xml", f"{R}/_opls_emc2.xml", f"{R}/_opls_ions.xml")
pdb = PDBFile(pdb_path)
system = ff.createSystem(pdb.topology, nonbondedMethod=PME,
                         nonbondedCutoff=1.0 * unit.nanometer, constraints=None)
integrator = LangevinMiddleIntegrator(298.15 * unit.kelvin, 1.0 / unit.picosecond,
                                      1.0 * unit.femtosecond)
sim = Simulation(pdb.topology, system, integrator)
sim.context.setPositions(pdb.positions)
sim.minimizeEnergy()
sim.context.setVelocitiesToTemperature(298.15 * unit.kelvin)
sim.reporters.append(
    StateDataReporter(f"{R}/_prod.log", 500, step=True, potentialEnergy=True,
                      temperature=True, separator=" ")
)
li_idx = [i for i, a in enumerate(pdb.topology.atoms()) if a.residue.name == "LI"]
print("LI atoms:", len(li_idx), flush=True)
# trajectory sampling: 500 x 2000 steps -> 501 frames at 2 ps cadence (1 ns)
frames = []
for k in range(500):
    sim.step(2000)
    st = sim.context.getState(getPositions=True)
    fr = np.array([[v.value_in_unit(unit.angstrom) for v in r]
                   for r in st.getPositions(asNumpy=True)])
    frames.append(fr)
    if (k + 1) % 100 == 0:
        np.save(f"{R}/_frames_{k+1}.npy", np.array(frames))
frames.append(frames[-1])
p0 = frames[0]
ts = np.arange(len(frames)) * 2000.0  # fs
# PBC unwrap: cumulative minimum-image displacement from frame 0
box = np.array([box_len] * 3)
disp = np.cumsum(np.clip((np.diff(frames, axis=0) + box / 2) % box - box / 2,
                         -box / 2, box / 2), axis=0)
msd_d = disp[:, li_idx, :]  # [T, nLi, 3]
msd = np.mean(np.sum(msd_d**2, axis=2), axis=1)  # [T]
arr = np.column_stack([ts[1:], msd])
half = len(ts[1:]) // 2
slope = np.polyfit(arr[half:, 0], arr[half:, 1], 1)[0]
D = slope * 1e-5 / 6.0  # A^2/fs -> m^2/s
traj_ok = bool(np.all(np.isfinite(msd)))
drifter = float(np.nanmax(np.abs(frames[-1] - p0))) if traj_ok else float("nan")
out = {"D_Li_m2_s": float(D), "trajectory_ok": traj_ok,
       "drift_check": f"max_disp_A={drifter:.1f}", "engine": "openmm-opls"}
json.dump(out, open(f"{R}/df_endorse_md_out_opls.json", "w"), indent=2)
print("PROD DONE:", out, flush=True)
