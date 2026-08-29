# -*- coding: utf-8 -*-
"""t1_r3 entry 0 — pre-registered criteria + case meta (zero-interaction execution).

Writes log.jsonl entry 0 via bda.store.append_entry (protocol-mandated path).
Idempotent: skips if a criteria entry already exists.
"""
import json
import sys

from bda.store import CaseWorkspace, append_entry

TASK_TEXT = (
    "Design a battery for a next-generation pure electric sedan: "
    "energy density ≥ 392.61 Wh/kg, support 4C fast charge (no lithium plating), "
    "maximum temperature ≤ 60°C, overcharge to 4.7 V without triggering thermal runaway."
)

ENTRY = {
    "criteria": {
        "stage1": {
            # Molecular-level elimination lines (Stage 2 funnel; defaults per protocol).
            "max_energy_ev": {"max": 0.0},
            "max_homo_ev": {"max": -6.0},
        },
        "stage2": {
            # Cell performance. Contract-caliber definition (bda calc-energy):
            # ED = ∫V·I_1C dt / Σ layer thickness×(1−porosity)×density×area (electrolyte excluded).
            "energy_density_wh_kg": {"min": 392.61},
        },
        "stage3": {
            # Safety. T_max_K judged on every cell-thermal scenario output
            # (4C fast charge and overcharge) — strict reading of "maximum temperature ≤ 60°C".
            "T_max_K": {"max": 333.15},
            "plated": False,
            "triggered": False,
        },
        "meta": {
            "task": TASK_TEXT,
            "start_stage": 3,
            "base": "Chen2020",
            "base_reason": (
                "task text names no electrode system → deterministic default Chen2020 "
                "(anchor: NMC811/graphite, no SiOx; verified by parameter dump before first run)"
            ),
            "real_compute": False,
            "ablation": {
                "exploration_force": "on",
                "ceiling_escalation": "on",
                "funnel_voting": "on",
            },
            "freedoms": {
                "electrode_system": (
                    "adjustable (widest interpretation — task declares none locked; "
                    "base parameter-set switch allowed, e.g. OKane2022 NMC811/SiOx)"
                ),
                "electrolyte_formulation": (
                    "adjustable (widest — transport overrides sigma/t+/D allowed per bridge table)"
                ),
                "electrode_modification": (
                    "adjustable (widest — coating/doping allowed; SEI/cracking parameter bridge)"
                ),
                "cell_architecture": (
                    "adjustable (widest — thickness/porosity/N-P/separator/current collector/particle size)"
                ),
                "thermal_management": (
                    "adjustable (widest — Total heat transfer coefficient override allowed)"
                ),
            },
            "overcharge_target": (
                "4.7 V = NMC811 upper cut-off 4.2 V + 0.5 V (overcharge protocol definition); "
                "verbatim match to the task contract"
            ),
            "triggered_judge": (
                "run-tr --sim <overcharge output> --mass-kg <calc-energy mass_kg> → triggered boolean; "
                "mechanical, no intuition"
            ),
            "t_max_criterion_scope": (
                "T_max_K ≤ 333.15 K enforced on 4C_charge_45C and overcharge cell-thermal outputs; "
                "run-tr T_max_K (runaway-trajectory continuation) not separately re-judged"
            ),
            "energy_density_def": (
                "calc-energy contract caliber: electrolyte excluded from mass/volume, "
                "electrodes + current collectors + separator included"
            ),
        },
    }
}


def main() -> int:
    ws = CaseWorkspace("exp/t1_r3")
    log = ws.path / "log.jsonl"
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            if isinstance(e.get("criteria"), dict):
                print("entry 0 already exists; skip")
                return 0
    append_entry(ws, ENTRY)
    print(f"entry 0 written → {log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
