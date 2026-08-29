"""t5_r3 round-3 propose via append_entry."""
from bda.store import CaseWorkspace, append_entry
ws = CaseWorkspace("t5_r3", "runs/exp")
propose = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Separator thickness [m]": 9e-06,
                "Positive electrode thickness [m]": 100e-06,
                "Negative electrode thickness [m]": 112e-06,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Cation transference number": 0.5,
                "Electrolyte diffusivity [m2.s-1]": 6e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 30.0,
            },
            "name": "W1 arch+transport+h30",
            "role": "V2 ED architecture + strong transport upgrade (isoC recipe) + liquid cooling h=30",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Separator thickness [m]": 9e-06,
                "Positive electrode thickness [m]": 100e-06,
                "Negative electrode thickness [m]": 112e-06,
                "Electrolyte conductivity [S.m-1]": 3.2,
                "Cation transference number": 0.42,
                "Electrolyte diffusivity [m2.s-1]": 4e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 30.0,
            },
            "name": "W2 arch+transport-mod",
            "role": "same architecture, moderated transport upgrade (probe minimum formulation ask)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Separator thickness [m]": 9e-06,
                "Positive electrode thickness [m]": 100e-06,
                "Negative electrode thickness [m]": 112e-06,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Cation transference number": 0.5,
                "Electrolyte diffusivity [m2.s-1]": 6e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 50.0,
            },
            "name": "W3 arch+transport+h50",
            "role": "W1 with h=50 (stronger liquid cooling; probe T_max headroom)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Separator thickness [m]": 9e-06,
                "Positive electrode thickness [m]": 100e-06,
                "Negative electrode thickness [m]": 112e-06,
                "Electrolyte conductivity [S.m-1]": 5.0,
                "Cation transference number": 0.5,
                "Electrolyte diffusivity [m2.s-1]": 6e-10,
                "Total heat transfer coefficient [W.m-2.K-1]": 30.0,
            },
            "name": "W4 okane+arch+transport",
            "role": "system-switch candidate: OKane2022 base (native plating kinetic function) + same architecture/transport/cooling",
        },
    ],
    "llm_reason": (
        "Round-2 diagnostics isolated the plating cause to ELECTROLYTE SALT TRANSPORT (isoC sigma=5+t+=0.5+De=6e-10 "
        "lifts min anode potential -0.438->+0.034V; anode/cathode particle size inert; thin anode alone insufficient). "
        "isoC at h=10 ran hotter (348.8K) because the 4C charge actually proceeds -> must pair transport with cooling. "
        "W1 pairs the V2 ED architecture (518.9 Wh/kg) with the isoC transport recipe at h=30. W2 probes the minimum "
        "formulation ask. W3 probes T_max headroom at h=50. W4 = OKane2022 system switch: its native plating "
        "exchange-current FUNCTION cleared plating at baseline but overheated (368.3K); combine with arch+transport+cooling. "
        "Note (honest): local pybamm-26.7.1 OKane2022 = graphite anode + Ai2020 cracking (no SiOx keys), so W4 is a "
        "kinetics/cracking-model system switch, not a chemistry switch. Transport overrides are estimates marked as such "
        "(high-conductivity/single-ion-class electrolyte formulation); ED from calc-energy contract."
    ),
}
append_entry(ws, propose)
print("round-3 propose appended")