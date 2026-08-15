import pybamm

PROTOCOLS = {
    "1C_discharge": {"kind": "discharge", "C_rate": 1.0, "t_end_s": 3600.0, "T_amb_K": 298.15},
    "4C_charge_45C": {"kind": "charge", "C_rate": 4.0, "t_end_s": 900.0, "T_amb_K": 318.15},
}


def run_simulation(params: dict, protocol: str, base: str = "Chen2020", mode: str = "spme") -> dict:
    if protocol not in PROTOCOLS:
        raise ValueError(f"unknown protocol '{protocol}'; legal: {sorted(PROTOCOLS)}")
    if mode not in ("spme", "dfn"):
        raise ValueError(f"unknown mode '{mode}'; legal: spme, dfn")
    p = PROTOCOLS[protocol]
    parameter_values = pybamm.ParameterValues(base)
    unknown_params = sorted(name for name in params if name not in parameter_values)
    if unknown_params:
        raise ValueError(f"unknown parameter name(s): {unknown_params}")
    parameter_values.update(params)
    model = pybamm.lithium_ion.SPMe() if mode == "spme" else pybamm.lithium_ion.DFN()
    sim = pybamm.Simulation(model, parameter_values=parameter_values)
    sim.solve([0, p["t_end_s"]])
    sol = sim.solution
    return {
        "model_used": "SPMe" if mode == "spme" else "DFN",
        "time_s": sol["Time [s]"].entries.tolist(),
        "voltage_v": sol["Terminal voltage [V]"].entries.tolist(),
        "capacity_ah": float(sol["Discharge capacity [A.h]"].entries[-1])
        if p["kind"] == "discharge" else float(sol["Time [s]"].entries[-1]) * p["C_rate"] / 3600.0,
    }
