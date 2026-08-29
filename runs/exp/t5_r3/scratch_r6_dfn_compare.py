"""Round-6: DFN vs SPMe comparison for finalists."""
import json

base = r"runs\exp\t5_r3\cell"

def ed_of(fname):
    return json.load(open(fr"{base}\{fname}", encoding="utf-8"))

dfs = [
    ("y4", "r6_y4_energy_dfn.json", "r5_y4_energy.json"),
    ("y3", "r6_y3_energy_dfn.json", "r5_y3_energy.json"),
]
for v, df, sp in dfs:
    try:
        d = ed_of(df)
        try:
            s = ed_of(sp)
            print(
                f"{v} DFN: ED={d['energy_density_wh_kg']:.2f} Wh/kg cap={d['capacity_ah']:.3f} Ah mass={d['mass_kg']*1000:.2f} g | "
                f"SPMe: ED={s['energy_density_wh_kg']:.2f} cap={s['capacity_ah']:.3f} | "
                f"dED={d['energy_density_wh_kg']-s['energy_density_wh_kg']:+.2f}"
            )
        except FileNotFoundError:
            print(f"{v} DFN: ED={d['energy_density_wh_kg']:.2f} Wh/kg cap={d['capacity_ah']:.3f} Ah mass={d['mass_kg']*1000:.2f} g | SPMe file missing")
    except FileNotFoundError:
        print(f"{v} DFN file not yet present")