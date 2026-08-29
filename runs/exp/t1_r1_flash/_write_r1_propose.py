# Round-1 propose entry (agent-built input script)
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t1_r1_flash", root="runs")

propose = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "base": "OKane2022",
            "name": "Baseline-OKane2022",
            "role": "baseline system: NMC811/graphite+SiOx next-gen BEV chemistry, complete thermal/geometry, SEI+cracking; 4.2 V cutoff so overcharge +0.5 V = task 4.7 V",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
            },
            "name": "Arch-A",
            "role": "ED boost via thin collectors (16/12 um -> 10/8 um): no electrochemical side effects, inactive-mass reduction",
        },
        {
            "struct": {
                "Positive electrode thickness [m]": 9.5e-5,
                "Negative electrode thickness [m]": 1.07e-4,
                "Positive current collector thickness [m]": 1.0e-5,
                "Negative current collector thickness [m]": 0.8e-5,
            },
            "name": "Arch-B",
            "role": "ED push: thick positive (75.6->95 um) + matched negative (N/P preserved ~1.13) + thin collectors",
        },
    ],
    "llm_reason": "Task names no electrode system; anchor-table default Chen2020 lacks complete thermal/geometry (T_max would be approximate) so the adjustable electrode-system DOF selects OKane2022 (recorded in entry-0 meta). Round 1 = baseline full characterization + 2 ED probes to size the ED/4C trade-off before targeting fixes.",
}
append_entry(ws, propose)
print("propose R1 written")
