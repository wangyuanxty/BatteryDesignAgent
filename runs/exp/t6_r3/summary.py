"""Summarize one candidate's full suite (1C energy + 4C + aging) across the five t6_r3 criteria.

Usage: python summary.py <candidate-tag> [file-pattern]
Default pattern: cell/r3_<tag>_{energy,4c,aging}.json under this workspace.
"""
import json
import sys

WS = "runs/exp/t6_r3/cell"


def summarize(tag, pat):
    def load(sfx):
        with open(f"{WS}/{pat.format(tag, sfx)}", encoding="utf-8") as f:
            return json.load(f)

    e = load("energy")
    c = load("4c")
    a = load("aging")
    ap = c["anode_potential_v"]
    caps = a["capacity_ah_per_cycle"]
    print(
        f"{tag}: wh_l={e['energy_density_wh_l']:.1f} (>=950) mid={e['midpoint_voltage_v']:.4f} (>=4.1)"
        f" | 4C: Tmax={c['T_max_K']:.2f}K (<=323.15) amin={min(ap):+.4f} plated={min(ap) < 0} q4c={c['capacity_ah']:.3f}Ah"
        f" | SEI={a['sei_thickness_nm_end']:.1f}nm (<=500) cap1={caps[0]:.3f} cap100={caps[-1]:.3f}"
    )


if __name__ == "__main__":
    tag = sys.argv[1]
    pat = sys.argv[2] if len(sys.argv) > 2 else "r3_{0}_{1}.json"
    summarize(tag, pat)
