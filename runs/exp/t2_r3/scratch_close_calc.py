# Mechanical derivation of all BOM/calc/spec numbers for t2_r3 deliverables.
# Inputs read from tool outputs / pybamm Chen2020 parameter dump (audit-sourced), not memory.
import sys
sys.stdout.reconfigure(encoding="utf-8")

F = 96485.0
KWH = None

# geometry / composition (pybamm Chen2020 dump, scratch_close_dump.py)
H, W = 0.065, 1.58
area = H * W
L_pos, L_neg, L_sep = 75.6e-6, 85.2e-6, 12e-6
L_al, L_cu = 16e-6, 12e-6
por_pos, por_neg, por_sep = 0.335, 0.40, 0.47   # neg porosity = final design 0.40
rho_pos, rho_neg, rho_al, rho_cu = 3262.0, 1657.0, 2700.0, 8960.0
amvf_pos, amvf_neg = 0.665, 0.75
c_max_pos, c_max_neg = 63104.0, 33133.0
r_pos, r_neg = 2.5e-6, 2.0e-6
nom_cap = 5.0
t_total = L_pos + L_neg + L_sep + L_al + L_cu

# simulation results
cap_1c = 5.064843296941604          # r7_final_1c_dfn.json:capacity_ah
energy_wh = 18.457182518897156       # r7_final_energy_dfn.json:energy_wh
mass_kg = 0.04127970507960001        # r7_final_energy_dfn.json:mass_kg
ed_wh_kg = 447.12486398112617
ed_wh_l = 895.0169390062512
vol_m3 = 2.0622160000000005e-05
mid_v = 3.911774309748794
dcr = 0.0026124512480850013
pw = 39080.64160851274
layer = {"pos": 0.163993788, "neg": 0.08470583999999999, "al": 0.043199999999999995,
         "cu": 0.10752, "sep": 0.00252492}   # r7_final_energy_dfn.json:layer_kg_m2
tmax4c = 347.69959453332905
anode_min = 0.044321
lowt = 0.995697
sei100, sei500 = 276.21554418266214, 393.00464365647116

kwh = energy_wh / 1000.0
KWH = kwh
print("area m2 =", area)
print("total stack thickness um =", t_total * 1e6)
print("kWh =", kwh)

print("\n--- layer masses (g) ---")
g = {k: v * area * 1000 for k, v in layer.items()}
for k, v in g.items():
    print(f"  {k}: {v:.4f} g ;  kg/kWh = {v/1000/kwh:.5f}")

tot_ex = sum(g.values())
print("total (contract, no electrolyte) g =", tot_ex)

# electrolyte (estimate: pore volume x 1.2 g/cm3)
v_pore = area * (L_pos*por_pos + L_neg*por_neg + L_sep*por_sep)
m_elec = v_pore * 1200.0 * 1000
print("pore volume m3 =", v_pore, " electrolyte g (est) =", m_elec, " kg/kWh =", m_elec/1000/kwh)
tot_incl = tot_ex + m_elec
print("total incl electrolyte g =", tot_incl, " ED incl elec =", energy_wh/(tot_incl/1000))

print("\n--- BOM rows (split 96/2/2 estimate) ---")
for nm, mass_tot in [("pos coating", g["pos"]), ("neg coating", g["neg"])]:
    for frac, lab in [(0.96, "AM"), (0.02, "binder"), (0.02, "conductive additive")]:
        m = mass_tot * frac
        print(f"  {nm} {lab}: {m:.4f} g ; kg/kWh = {m/1000/kwh:.5f}")

print("\n--- process params ---")
for nm, rho, L, por in [("pos", rho_pos, L_pos, por_pos), ("neg", rho_neg, L_neg, por_neg)]:
    areal = rho * L * (1 - por)          # kg/m2
    comp_kg = rho * (1 - por)            # kg/m3
    print(f"  {nm}: areal {areal*1000:.2f} g/m2 ; compaction {comp_kg:.2f} kg/m3 = {comp_kg/1000:.4f} g/cm3")

print("\n--- N/P ---")
pos_areal_full = c_max_pos * amvf_pos * L_pos * F / 3600    # Ah/m2
neg_areal_full = c_max_neg * amvf_neg * L_neg * F / 3600
print(f"  pos areal full-range {pos_areal_full:.3f} Ah/m2 ; neg {neg_areal_full:.3f} Ah/m2")
print(f"  N/P full-range = {neg_areal_full/pos_areal_full:.4f}")
pos_cell_full = pos_areal_full * area
dof_usable = nom_cap / pos_cell_full
print(f"  pos cell full-range {pos_cell_full:.4f} Ah ; usable-window fraction ~ {dof_usable:.4f}")
print(f"  N/P usable-window basis = {neg_areal_full/(pos_areal_full*dof_usable):.4f}")

print("\n--- perf summary vs criteria ---")
print(f"  ED {ed_wh_kg} >= 327.18 : {ed_wh_kg>=327.18}")
print(f"  lowT {lowt} >= 0.9 : {lowt>=0.9}")
print(f"  SEI100 {sei100} <= 500 : {sei100<=500}")
print(f"  SEI500 {sei500} <= 550 : {sei500<=550}")
print(f"  plated={anode_min < 0} (anode min {anode_min})")
print(f"  1C capacity {cap_1c} Ah ; 1C current {nom_cap} A ; 4C {nom_cap*4} A")
print(f"  T_max 4C {tmax4c} K = {tmax4c-273.15:.2f} C ; rise over 45C ambient = {tmax4c-318.15:.2f} K")
print(f"  1C DFN T_max 304.3123 K = {304.3123-273.15:.2f} C (info)")
print(f"  midpoint {mid_v} V ; DCR {dcr*1000:.3f} mohm ; power density {pw:.1f} W/kg")
print(f"  agent environment check marker")