# Round-2 propose entry (agent-built input script)
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t1_r1_flash", root="runs")

propose = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
            },
            "name": "ArchA-h150",
            "role": "T_max fix: thin collectors (ED 462.6) + liquid-cooling h=150 W/m2.K (BEV sedan pack-level cooling, thermal-management DOF)",
        },
        {
            "struct": {
                "Positive electrode thickness [m]": 9.5e-5,
                "Negative electrode thickness [m]": 1.07e-4,
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
                "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
            },
            "name": "ArchB-h150",
            "role": "T_max fix on ED champion (492.5) + liquid-cooling h=150; thicker electrodes raise 4C heat so T_max margin expected thinner than ArchA-h150",
        },
    ],
    "llm_reason": "R1 baseline failed only T_max (367.4 K vs 333.15) at h=10 default; ED passes with margin (405.6/462.6/492.5). Root cause = cooling, not chemistry/architecture: hA=0.053 W/K cannot reject ~10-15 W at 4C. Fix at the scale where the cause lives (Stage 3/thermal DOF): liquid-cooling h=150. Both ED-passing architectures get 4C-DFN plating+T_max test; plating margin is the watch item (cooler cell -> slower kinetics -> anode potential may dip below 0 V).",
}
append_entry(ws, propose)
print("propose R2 written")
