"""T9 run 3 — cell mapping for the finalist cathode (standalone script).

Criterion (5), no free parameters:
  - constant OCP = computed average voltage of the finalist
  - capacity = 0.9 x computed capacity (LNMO-anchored utilization)
  - SEI kinetics = baseline k0 (Chen2020 untouched)
  - ED_active = V x C x 0.9 (reported, not a criterion)

Why standalone: pybamm_runner.run_simulation hardcodes any string OCP override to
lnmo_ocp, so a custom constant OCP cannot be injected through the run-pyamm JSON
path. This script builds the Chen2020 base directly and overrides only the cathode
OCP/concentration keys plus the LNMO-template anchors.

Window mechanics: the computed capacity already assumes the x in [0.3, 1] window
(0.7 of one Li per formula unit). The LNMO-anchored utilization 0.9 gives a usable
window fraction of 0.63. This pybamm version's model has no stoichiometry-limit
parameters, so the window is encoded by (a) maximum concentration = rho/MW (one Li
per f.u.), (b) initial (fully charged) concentration = 0.37 x c_max, and (c) a
time-bounded 1C discharge of 0.63 h whose delivered charge is exactly the mapped
capacity. rho = 4400 kg/m3 is the LNMO-template anchor (the skill's own precedent
for a custom high-voltage cathode).
"""
import pybamm

# ---- run-comp values (batch 2; replay-verified by comp_envelope_check --formula) ----
V_COMP = 5.519024610519409     # computed average voltage, V (envelope recompute)
C_COMP = 109.70913206456218    # computed capacity, mAh/g
UTIL = 0.9                     # LNMO-anchored utilization (criterion 5)
WINDOW_COMP = 0.7              # run-comp x window (x in [0.3, 1])
RHO_ANCHOR = 4400.0            # kg/m3, LNMO-template density anchor

MW = 171.0071                  # kg/kmol -> g/mol of LiNi0.75Mg0.25PO4F
                               # Li 6.941 + 0.75Ni 44.0201 + 0.25Mg 6.0763
                               # + P 30.9738 + 4O 63.9976 + F 18.9984
WINDOW = WINDOW_COMP * UTIL    # 0.63 usable fraction of one Li per f.u.
C_USABLE = C_COMP * UTIL       # mAh/g usable in the cell
ED_ACTIVE = V_COMP * C_COMP * UTIL  # mWh/g active (reported)

C_MAX = RHO_ANCHOR / (MW / 1000.0)  # mol/m3, one Li per f.u. at rho anchor
INIT_CONC = (1.0 - WINDOW) * C_MAX  # charged state: x = 0.37 (Li-poor end)

# Chen2020 geometry (unchanged) -> full-range cathode capacity (Ah)
H, W_, L_POS = 0.137, 0.207, 7.56e-5
EPS_AM = 0.665
V_EL = H * W_ * L_POS
FULL_AH = C_MAX * V_EL * EPS_AM * pybamm.constants.F.value / 3600.0
NOMINAL_AH = FULL_AH                     # 1C = full-range capacity per hour
DELIVER_AH = NOMINAL_AH * WINDOW         # = 0.9 x C_COMP x active mass
MASS_ACTIVE_G = RHO_ANCHOR * V_EL * EPS_AM * 1000.0
MAH_PER_G = DELIVER_AH * 1000.0 / MASS_ACTIVE_G


def const_ocp(sto):
    """Flat OCP = computed average voltage (constant-OCP approximation)."""
    return pybamm.Scalar(V_COMP)


parameter_values = pybamm.ParameterValues("Chen2020")
parameter_values.update(
    {
        # criterion 5: constant OCP = computed average voltage
        "Positive electrode OCP [V]": const_ocp,
        "Positive electrode OCP entropic change [V.K-1]": 0.0,
        # criterion 5: capacity = 0.9 x computed (window 0.63, c_max from rho/MW)
        "Maximum concentration in positive electrode [mol.m-3]": C_MAX,
        "Initial concentration in positive electrode [mol.m-3]": INIT_CONC,
        "Nominal cell capacity [A.h]": NOMINAL_AH,
        "Positive electrode density [kg.m-3]": RHO_ANCHOR,
        # LNMO-template anchors for an unknown cathode's transport (skill precedent)
        "Positive electrode conductivity [S.m-1]": 1.0,
        "Positive particle diffusivity [m2.s-1]": 1e-12,
        # voltage cut-offs: lower = Chen2020 baseline; upper above the flat OCP
        "Lower voltage cut-off [V]": 2.5,
        "Upper voltage cut-off [V]": 5.6,
    },
    check_already_exists=False,
)
# criterion 5: SEI kinetics = baseline k0 -> untouched (read back for the record)
SEI_K0 = parameter_values["SEI kinetic rate constant [m.s-1]"]

exp = pybamm.Experiment([f"Discharge at 1C for {WINDOW:g} hours"])
model = pybamm.lithium_ion.SPMe()
sol = pybamm.Simulation(model, experiment=exp, parameter_values=parameter_values).solve()

t = sol["Time [s]"].entries
v = sol["Terminal voltage [V]"].entries
q = sol["Discharge capacity [A.h]"].entries
print("=== cell mapping (criterion 5) ===")
print(f"finalist                : LiNi0.75Mg0.25PO4F (tavorite, 6Ni/2Mg realized)")
print(f"OCP (constant)          : {V_COMP:.4f} V")
print(f"computed capacity       : {C_COMP:.3f} mAh/g")
print(f"mapped capacity         : {C_USABLE:.3f} mAh/g (= 0.9 x computed)")
print(f"ED_active               : {ED_ACTIVE:.1f} mWh/g = V x C x 0.9 (reported)")
print(f"SEI kinetic rate const  : {SEI_K0:.3e} m/s (baseline k0, untouched)")
print(f"density anchor          : {RHO_ANCHOR:.0f} kg/m3 (LNMO template)")
print(f"c_max / initial conc    : {C_MAX:.0f} / {INIT_CONC:.0f} mol/m3 (window {WINDOW:.2f})")
print(f"nominal capacity        : {NOMINAL_AH:.4f} Ah (full-range, 1C basis)")
print(f"delivered (1C x {WINDOW:g}h)  : {q[-1]:.4f} Ah")
print(f"expected delivered      : {DELIVER_AH:.4f} Ah")
print(f"mAh/g active delivered  : {q[-1] * 1000.0 / MASS_ACTIVE_G:.3f} (expect {MAH_PER_G:.3f})")
print(f"terminal voltage        : mean {v.mean():.3f} V, min {v.min():.3f} V, max {v.max():.3f} V")
print(f"mean - OCP              : {(v.mean() - (V_COMP - 0.1)):+.4f} V (anode/ohmic offset vs ~0.1 V)")
