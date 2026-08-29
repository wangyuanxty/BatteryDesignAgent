"""t4_r3: propose entry round 6 — strong-transport OKane combos + LNMO system switch."""
from pathlib import Path

from bda.store import CaseWorkspace, append_entry, REPO_ROOT

ws = CaseWorkspace("exp/t4_r3", root="runs")
lnmo = (
    REPO_ROOT / ".claude/skills/virtual-battery-factory/scripts/bda/simulators/data/LNMO.json"
).as_posix()
# verify path exists before proposing
assert Path(lnmo).exists(), lnmo

propose_r6 = {
    "action": "propose",
    "round": 6,
    "candidates": [
        {
            "base": lnmo,
            "name": "V14_sys_LNMO",
            "role": "system switch: high-voltage LNMO spinel cathode set (4.7 V cut-off; library data/LNMO.json on Chen2020 base) with empty overrides — higher cathode voltage shifts 4C charge cutoff to lower anode depth (plating margin) and raises energy per Ah",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 60,
                "Negative particle radius [m]": 2.5e-6,
                "Positive particle radius [m]": 3.0e-6,
                "Electrolyte conductivity [S.m-1]": 1.6,
                "Electrolyte diffusivity [m2.s-1]": 4.0e-10,
                "Cation transference number": 0.45,
            },
            "name": "V16_ok_h60_elx",
            "role": "OKane2022 + thin pack + h=60 cold-plate + particle shrink + strong electrolyte (T-independent sigma=1.6 S/m, D=4e-10, t+=0.45): max transport attack on the plating gate at cooled 4C charge; T_max ~325 K",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-6,
                "Negative current collector thickness [m]": 6e-6,
                "Separator thickness [m]": 8e-6,
                "Total heat transfer coefficient [W.m-2.K-1]": 60,
                "Negative particle radius [m]": 2.0e-6,
                "Positive particle radius [m]": 2.5e-6,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Electrolyte diffusivity [m2.s-1]": 6.0e-10,
                "Cation transference number": 0.5,
            },
            "name": "V17_ok_h60_elx_plus",
            "role": "V16 escalated: sigma=2.2/D=6e-10/t+=0.5, radii 2.0/2.5 um — upper bound of the formulation+architecture attack within sanctioned levers",
        },
    ],
    "llm_reason": (
        "Round 5 verdict: V13 (h40+R2.5/3.0) passes retention (95.65) and densities (506.6 Wh/kg, "
        "961.3 Wh/L) but T_max 339.97 (needs h>=~58 -> T~325 K) and anode min -0.417 V at cooled 4C. "
        "The plating pass of V10 (+0.0088 V) existed only at T_max 368 K — hot-cell artifact; the cooled "
        "charge (V12: -0.435) shows the chemistry's true 4C margin. Round 6 pushes the two remaining "
        "levers: (1) electrolyte transport attack (sigma/D/t+ scalars, T-independent = wide-temperature "
        "formulation, ESTIMATE values listed; record that gaining only ohmic/concentration share bounds "
        "the anode-surface lift), (2) the sanctioned system-switch row for high-voltage LNMO (4.7 V "
        "cut-off => 4C charge terminates at lower anode depth). Retention lowT runs keep identical "
        "params to their 1C runs (entry-0 derivation contract); no initial-temperature overrides — "
        "warm-start is a known runner artifact and is annotated, not exploited."
    ),
}
append_entry(ws, propose_r6)
print("propose r6 written; LNMO path =", lnmo)