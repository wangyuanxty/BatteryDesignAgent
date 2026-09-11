"""Apply the contract's fixed additive-to-kinetics mapping to each candidate.

Rule (contract, no free parameters):
    k(M) = k0 * 10**((HOMO_xTB(M) + 12.5) / 1.0),  k0 = Chen2020 baseline = 1e-12 m/s
Executed from the funnel xTB outputs. Writes one params file per candidate and a
mapping record (mapping.json) for the audit trail.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
K0 = 1e-12  # Chen2020 "SEI kinetic rate constant [m.s-1]"

CANDIDATES = ["pfta", "pfhex", "pftea", "pfpent", "ncf3"]
recs = []
for k in CANDIDATES:
    xtb = json.loads((HERE.parent / "funnel" / f"{k}_xtb.json").read_text(encoding="utf-8"))
    homo = xtb["candidates"][0]["metrics"]["homo_ev"]
    k_m = K0 * 10 ** ((homo + 12.5) / 1.0)
    params = {"SEI kinetic rate constant [m.s-1]": k_m}
    (HERE / f"params_{k}.json").write_text(json.dumps(params, indent=2), encoding="utf-8")
    recs.append({
        "candidate": k,
        "homo_ev_xtb": homo,
        "exponent": round(homo + 12.5, 6),
        "k_m_s": k_m,
        "k_over_k0": k_m / K0,
        "log10_k_over_k0": round(homo + 12.5, 6),
        "note": "below the 0.1x calibration floor -> extrapolation, flagged in report",
    })
    print(f"{k}: HOMO={homo} eV -> k = {k_m:.4e} m/s ({k_m/K0:.4f} x k0)")

(HERE / "mapping.json").write_text(
    json.dumps({"rule": "k = k0 * 10**((HOMO_xTB + 12.5)/1.0)", "k0_m_s": K0,
                "candidates": recs}, indent=2), encoding="utf-8")
print("wrote mapping.json")
