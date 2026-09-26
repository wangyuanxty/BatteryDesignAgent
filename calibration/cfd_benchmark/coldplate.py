# -*- coding: utf-8 -*-
"""Cold-plate CFD benchmark (FiPy): steady laminar incompressible flow + conjugate heat transfer.

Adapted from FiPy's own examples/flow/stokesCavity.py (SIMPLE + Rhie-Chow on a
collocated grid); inertia (ConvectionTerm) and a solid region (viscosity
penalisation) added here.

Domain (2D, x along flow, y across), metres:
    y in [0, Hf]       water channel
    y in [Hf, Hf+Hs]   aluminium plate
BCs:
    inlet  x=0   u = U_IN in the channel, 0 in the plate ; T = T_IN in the channel
    outlet x=L   p' = 0
    top    y=H   q = Q_TOP (heat flux from the cell footprint)
    bottom y=0   adiabatic (default zero-gradient)
Outputs: max/mean plate temperature, wall heat transfer coefficient h, wall time.

Usage: python coldplate.py <nx> <ny> [<sweeps>]
"""
import sys, time
import numpy as np
from fipy import (CellVariable, FaceVariable, Grid2D, DiffusionTerm,
                  ConvectionTerm, numerix)
from fipy.variables.faceGradVariable import _FaceGradVariable

L, Hf, Hs = 0.050, 0.002, 0.003
H = Hf + Hs
RHO_F, MU_F, K_F, CP_F = 1000.0, 1.0e-3, 0.60, 4180.0
K_S = 200.0
U_IN, T_IN, Q_TOP = 0.2, 298.15, 5000.0
MU_SOLID = 1.0e-0                       # 1000x water: penalisation keeping the matrix well conditioned
U_REL, P_REL = 0.7, 0.1
STOKES = True

def solve(nx, ny, sweeps=400):
    t0 = time.time()
    mesh = Grid2D(nx=nx, ny=ny, dx=L/nx, dy=H/ny)
    X, Y = mesh.faceCenters
    yc = np.asarray(mesh.cellCenters[1].value)

    fluid_cell = CellVariable(mesh=mesh, value=(yc < Hf).astype(float))
    fluid_face = fluid_cell.arithmeticFaceValue
    mu = CellVariable(mesh=mesh, value=np.where(yc < Hf, MU_F, MU_SOLID))
    kk = CellVariable(mesh=mesh, value=np.where(yc < Hf, K_F, K_S))

    pressure = CellVariable(mesh=mesh, name='p')
    pressureCorrection = CellVariable(mesh=mesh)
    u = CellVariable(mesh=mesh, name='u', value=np.where(yc < Hf, U_IN, 0.0))
    v = CellVariable(mesh=mesh, name='v')
    velocity = FaceVariable(mesh=mesh, rank=1)
    T = CellVariable(mesh=mesh, name='T', value=T_IN)

    # --- equations ---------------------------------------------------------
    convCoeff = FaceVariable(mesh=mesh, rank=1)
    xEq = (ConvectionTerm(coeff=convCoeff, var=u)
           == DiffusionTerm(coeff=mu, var=u) - pressure.grad.dot([1., 0.]))
    yEq = (ConvectionTerm(coeff=convCoeff, var=v)
           == DiffusionTerm(coeff=mu, var=v) - pressure.grad.dot([0., 1.]))
    Teq = (ConvectionTerm(coeff=(RHO_F * CP_F * fluid_face * velocity), var=T)
           == DiffusionTerm(coeff=kk, var=T))

    # --- boundary conditions ----------------------------------------------
    inlet_fluid = mesh.facesLeft & (Y < Hf)
    inlet_solid = mesh.facesLeft & (Y >= Hf)
    u.constrain(U_IN, inlet_fluid); u.constrain(0., inlet_solid)
    u.constrain(0., mesh.facesTop | mesh.facesBottom)
    v.constrain(0., mesh.exteriorFaces)
    pressureCorrection.constrain(0., mesh.facesRight)
    T.constrain(T_IN, inlet_fluid)
    T.faceGrad.constrain(Q_TOP / K_S * mesh.faceNormals, where=mesh.facesTop)

    volume = CellVariable(mesh=mesh, value=mesh.cellVolumes)
    contrvolume = volume.arithmeticFaceValue
    ap = CellVariable(mesh=mesh, value=1.)

    coeff = 1. / ap.arithmeticFaceValue * mesh._faceAreas * mesh._cellDistances
    pCorrEq = DiffusionTerm(coeff=coeff) - velocity.divergence
    psolver = pCorrEq.getDefaultSolver(tolerance=1e-10, iterations=2000)

    velocity[0] = np.where(np.asarray(fluid_face.value) > 0.5, U_IN, 0.0)
    warmup = sweeps // 3
    for sweep in range(sweeps):
        convCoeff[:] = 0.0 if STOKES else RHO_F * fluid_face * velocity
        xEq.cacheMatrix()
        xres = xEq.sweep(var=u, underRelaxation=U_REL)
        xmat = xEq.matrix
        yres = yEq.sweep(var=v, underRelaxation=U_REL)
        ap[:] = numerix.maximum(-numerix.asarray(xmat.takeDiagonal()), 1e-16)

        presgrad = pressure.grad
        facepresgrad = _FaceGradVariable(pressure)
        velocity[0] = (u.arithmeticFaceValue
                       + contrvolume / ap.arithmeticFaceValue
                       * (presgrad[0].arithmeticFaceValue - facepresgrad[0]))
        velocity[1] = (v.arithmeticFaceValue
                       + contrvolume / ap.arithmeticFaceValue
                       * (presgrad[1].arithmeticFaceValue - facepresgrad[1]))
        velocity[..., mesh.exteriorFaces.value] = 0.
        velocity[0, (mesh.facesLeft & (Y < Hf)).value] = U_IN

        pCorrEq.cacheRHSvector()
        pres = pCorrEq.sweep(var=pressureCorrection, solver=psolver)
        rhs = pCorrEq.RHSvector

        pressure.setValue(pressure + P_REL * pressureCorrection)
        u.setValue(u - pressureCorrection.grad[0] / ap * mesh.cellVolumes)
        v.setValue(v - pressureCorrection.grad[1] / ap * mesh.cellVolumes)

        if sweep % 50 == 0 or sweep == sweeps - 1:
            print(f"   sweep {sweep:4d}  |xres|={float(abs(xres)):.3e} "
                  f"|yres|={float(abs(yres)):.3e} |pres|={float(abs(pres)):.3e} "
                  f"cont={float(np.max(np.abs(np.asarray(rhs)))):.3e}", flush=True)

    for _ in range(20):
        Teq.sweep(var=T, underRelaxation=0.9)
    wall = time.time() - t0

    Tv = T.value
    Tw_top = float(np.mean(Tv.reshape(ny, nx)[-1, :]))       # top row (cell centres)
    T_bulk = float(Tv.reshape(ny, nx)[int(ny*(Hf/H)*0.5), -1])  # channel centre, outlet
    h = Q_TOP / (Tw_top - T_bulk)
    return dict(nx=nx, ny=ny, cells=nx * ny, sweeps=sweeps, wall_s=wall,
                T_top_mean=Tw_top, T_out_bulk=T_bulk, h_W_m2K=h,
                T_max=float(Tv.max()))

if __name__ == "__main__":
    nx, ny = int(sys.argv[1]), int(sys.argv[2])
    sw = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    print(f"== cold plate {nx}x{ny} = {nx*ny} cells, {sw} sweeps ==", flush=True)
    r = solve(nx, ny, sw)
    print(f"RESULT {r}")
