"""t4_r3: build log-evaluate batch files for rounds 2-6 (one log-evaluate entry per candidate).

Output order per candidate: [lowT, 1C25C, 4C45C, energy, retention-bridge] so that
T_max_K comes from the 4C run (last T_max write) and capacity_ah from the energy file (1C cap).
"""
import json

from bda.store import CaseWorkspace

ws = CaseWorkspace("exp/t4_r3", root="runs")
cell = ws.path / "cell"
bridge = ws.path / "bridge"


def f(rel):
    return (cell / rel).as_posix()


def b(rel):
    return (bridge / rel).as_posix()


rounds = {
    2: [
        ("V1_thin_pack", "r2_V1"),
        ("V2_thin_pack_NP125", "r2_V2"),
        ("V3_thin_pack_both", "r2_V3"),
        ("V4_cold_elx", "r2_V4"),
    ],
    3: [
        ("V5_thin_pack_Rneg35", "r3_V5"),
        ("V6_thin_pack_Rneg30_Rpos35", "r3_V6"),
        ("V7_thin_pack_Rneg25_Rpos30", "r3_V7"),
    ],
    4: [
        ("V8_sys_ORegan2022", "r4_V8"),
        ("V9_sys_OKane2022", "r4_V9"),
    ],
    5: [
        ("V10_ok_thin", "r5_V10"),
        ("V11_ok_thin_h40", "r5_V11"),
        ("V12_ok_thin_h60_Rshrink", "r5_V12"),
        ("V13_ok_thin_h40_Rshrink", "r5_V13"),
    ],
    6: [
        ("V14_sys_LNMO", "r6_V14"),
        ("V16_ok_h60_elx", "r6_V16"),
        ("V17_ok_h60_elx_plus", "r6_V17"),
    ],
}

for rnd, cands in rounds.items():
    batch = []
    for cand, stem in cands:
        batch.append({
            "candidate": cand,
            "round": rnd,
            "outputs": [
                f(f"{stem}_1c_lowT_spme.json"),
                f(f"{stem}_1c_25C_spme.json"),
                f(f"{stem}_4C_45C_spme.json"),
                f(f"{stem}_energy.json"),
                b(f"{stem}_lowT_retention.json"),
            ],
        })
    out = ws.path / f"_batch_eval_r{rnd}.json"
    out.write_text(json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", out.name, "with", len(batch), "records")