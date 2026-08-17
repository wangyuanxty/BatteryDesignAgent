MAPPING = {
    "D_electrolyte_m2_s": "Electrolyte diffusivity [m2.s-1]",
    "conductivity_S_m": "Electrolyte conductivity [S.m-1]",
    "transport_number": "Cation transference number",
}


def map_micro_to_pybamm(props: dict) -> dict:
    out = {}
    for key, value in props.items():
        if key not in MAPPING:
            raise ValueError(
                f"unknown micro property '{key}'; legal keys: {', '.join(sorted(MAPPING))}"
            )
        out[MAPPING[key]] = value
    return out
