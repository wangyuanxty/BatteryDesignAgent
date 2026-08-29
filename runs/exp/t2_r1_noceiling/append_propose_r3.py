import sys
sys.path.insert(0, r".claude/skills/virtual-battery-factory/scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1_noceiling", "runs")
entry = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {"struct": {"Positive current collector thickness [m]": 1e-05,
                    "Negative current collector thickness [m]": 8e-06,
                    "Negative electrode thickness [m]": 1.1e-04},
         "name": "E ThickNeg",
         "role": "N/P 1.16->1.5 (anode capacity +29%): raises anode OCP at every charge throughput (4C plating margin) and shrinks the per-cycle anode stoichiometry swing in 1C cycling (SEI500 relief); ED cost offset by stacked thin collectors"},
        {"struct": {"Positive current collector thickness [m]": 1e-05,
                    "Negative current collector thickness [m]": 8e-06,
                    "Separator thickness [m]": 9e-06,
                    "Separator porosity": 0.55},
         "name": "F ThinSep",
         "role": "separator 12->9 um + porosity 0.47->0.55: relieve the electrolyte transport bottleneck at the highest-flux region (diagnostic: phi_e collapse across the separator during 4C charge)"},
        {"struct": {"Positive current collector thickness [m]": 1e-05,
                    "Negative current collector thickness [m]": 8e-06,
                    "Negative electrode thickness [m]": 1.1e-04,
                    "Separator thickness [m]": 9e-06,
                    "Separator porosity": 0.55},
         "name": "G ThickNeg+ThinSep",
         "role": "combined anode-headroom (E) + separator-transport (F) levers"},
        {"struct": {"Positive current collector thickness [m]": 1e-05,
                    "Negative current collector thickness [m]": 8e-06,
                    "Negative electrode thickness [m]": 1.3e-04},
         "name": "H ThickNeg2",
         "role": "N/P 1.16->1.77 dose-response: quantifies the anode-headroom lever scaling for 4C plating margin and SEI500"},
    ],
    "llm_reason": "R2: all four single-factor candidates still plate at 4C (min -0.4494..-0.4067 V) and fail SEI500 (771-837 nm); B (transport-up) and D (lower loading) WORSENED SEI500. Tool-run diagnostics (cell/diag_*.py, this case): at the 4C abort (V=4.2, ~33 s) the anode representative-particle surface stoichiometry has rocketed to ~0.8 (surface OCP 0.092 V) while the bulk is at ~0.06 - the 4C excursion is a surface-response/transport race pinned by the abort trajectory, which single levers barely move (measured deltas: B -0.011, C +0.002, D +0.032). Remaining structural levers in the allowed architecture space: (1) N/P up via thicker negative electrode - raises the anode OCP at every charge throughput and shrinks the per-cycle anode swing (empirically test whether the 4.2 V charge-end pinning cancels the SEI benefit); (2) separator thinning + porosity to relieve the electrolyte bottleneck at the highest-flux region. H is the N/P dose-response. All candidates stack A's thin-collector ED bank (measured inert w.r.t. plating/SEI). Bookkeeping: nominal capacity re-measured at 1C per candidate before the 4C runs (honest C-rate, D precedent). Sources: mechanisms from this case's tool-run diagnostics; lever directions from domain experience + Chen2020 parameterization (dump-verified keys: Negative electrode thickness, Separator thickness, Separator porosity).",
}
append_entry(ws, entry)
print("propose r3 appended")
