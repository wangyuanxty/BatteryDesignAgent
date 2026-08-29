"""Round 7: propose E3/E4 (balanced charge-end via cathode particle radius). t6_r1_singlemodel."""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_singlemodel", "runs/exp")
CELL = ws.path / "cell"
LNMO_BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

E1 = {
    "Separator thickness [m]": 1e-05,
    "Negative electrode thickness [m]": 1e-04,
    "Positive electrode thickness [m]": 6.1e-05,
    "Positive electrode porosity": 0.30,
    "Positive electrode active material volume fraction": 0.70,
    "Negative electrode porosity": 0.27,
    "Negative electrode active material volume fraction": 0.73,
    "Electrolyte conductivity [S.m-1]": 2.0,
    "Cation transference number": 0.65,
    "Electrolyte diffusivity [m2.s-1]": 4e-10,
    "Initial concentration in electrolyte [mol.m-3]": 2500.0,
    "Total heat transfer coefficient [W.m-2.K-1]": 200.0,
    "SEI kinetic rate constant [m.s-1]": 1e-13,
    "SEI reaction exchange current density [A.m-2]": 1.5e-08,
    "Positive particle radius [m]": 1e-07,
    "Negative particle radius [m]": 2e-07,
}
E3 = dict(E1)
E3.update({"Positive particle radius [m]": 1.7e-07})
E4 = dict(E1)
E4.update({"Positive particle radius [m]": 1.5e-07})

propose = {
    "action": "propose",
    "round": 7,
    "candidates": [
        {
            "name": "E3_Rp170_balanced",
            "base": LNMO_BASE,
            "struct": E3,
            "role": (
                "balanced charge-end: E1 trace shows the 4C charge (starts at the discharge-end cathode "
                "bulk 0.994) trips at 4.7 V when the cathode SURFACE strips (bulk = quasi-steady overshoot "
                "jR/(5FDc) + 0.02 = 0.155 at R_p 100 nm -> swing 6.06 mAh/cm2 = 1246 s), which is ~50-100 s "
                "AFTER the anode-full point (5.75 mAh/cm2) -> over-charge tail -> plating. Quasi-steady "
                "model validated on E1 to +/-10 s. Balanced fix: R_p 100 -> 170 nm -> overshoot 0.244 -> "
                "the surface strips when the bulk returns to the initial sto 0.264, i.e., the charge swing "
                "= the discharge swing (5.27 mAh/cm2, 1083 s at 18 A) -> the 4.7 V trip fires with the "
                "anode at bulk 0.92 (surface 0.98, OCP ~0.045 V positive, ~99 s margin to full saturation) "
                "-> no plating. Discharge stays cathode-limited ~5.27-5.31 (E1 measured 5.27) -> "
                "ED ~1130 Wh/L. Note: R_p 170 nm still a nano-LNMO (literature 50-200 nm); the R3 100 nm "
                "choice targeted the transient-pinning theory which R4 superseded with the salt-depletion "
                "diagnosis - the pinning-control rationale is now superseded by the balance rationale."
            ),
        },
        {
            "name": "E4_Rp150_sensitivity",
            "base": LNMO_BASE,
            "struct": E4,
            "role": (
                "sensitivity: R_p 150 nm -> overshoot 0.216 -> trip at the bulk 0.236 -> swing 5.47 "
                "mAh/cm2 (charge over-delivers the 5.27 discharge by 0.2) -> anode bulk 0.954 at the trip, "
                "surface pinned at 1.0 (potential still positive ~0.02-0.04; D1 trace showed the negative "
                "plunge only ~60-95 s past the pin) -> expected still no plating. Tests the margin "
                "sensitivity of the balance point."
            ),
        },
    ],
    "llm_reason": (
        "Bridge listing (deltas vs E1_cathode_61um):\n"
        "  Positive particle radius [m] 1e-7 -> 1.7e-7 (E3) / 1.5e-7 (E4). Radius is the sanctioned "
        "diffusion lever; the quasi-steady surface overshoot jR/(5FDc_max) is the balance knob that "
        "times the 4.7 V trip: ov(E1 100 nm)=0.144 (trip at the bulk 0.155, swing 6.06, 1246 s, too "
        "late), ov(170 nm)=0.244 (trip at the bulk 0.264 = the initial sto -> charge = discharge swing "
        "5.27, 1083 s, anode 0.92, no plating), ov(150 nm)=0.216 (trip at the bulk 0.236, swing 5.47, "
        "anode 0.954 - sensitivity).\n"
        "R6 verdicts: E1 fail (4C charge 1246 s, cap metric 1.384 Ah runner duration-proxy = true "
        "6.06 mAh/cm2, plated min -0.237, T 319.14 PASS, SEI 118.8 PASS, ED 1130.75 PASS, mid 4.2974 "
        "PASS); E2 fail (same mechanism, plated -0.237, T 319.16 PASS, SEI 119.7 PASS, ED 1160.2 PASS, "
        "mid 4.2970 PASS). Quasi-steady trip-time model validated on E1 (+/-10 s). R7 = the balance "
        "fix; R8 = DFN verification of the winner (Stage 4) + closing."
    ),
}

append_entry(ws, propose)
print("propose round 7 appended")

for name, params in (("E3", E3), ("E4", E4)):
    p = CELL / f"r7_{name}_params.json"
    p.write_text(json.dumps(params, indent=2), encoding="utf-8")
    print("wrote", p.name, "->", len(params), "keys")
