"""Round-1 propose entry: six electrolyte additive candidates (Stage 2)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t2_r1_singlemodel", root="runs/exp")

entry = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {"smiles": "FC1COC(=O)O1", "name": "FEC",
         "role": "fluoroethylene carbonate film-forming additive: suppresses SEI growth and 4C plating"},
        {"smiles": "O=C1OC=CO1", "name": "VC",
         "role": "vinylene carbonate film-forming additive: SEI stabilization"},
        {"smiles": "O=S1(=O)CCCO1", "name": "PS",
         "role": "1,3-propane sultone SEI film former: graphite surface protection"},
        {"smiles": "CCC(=O)OCC", "name": "EP",
         "role": "ethyl propionate low-viscosity ester co-solvent: -20C electrolyte conductivity"},
        {"smiles": "[B-]1(OC(=O)C(=O)O1)(F)F", "name": "LiDFOB-anion",
         "role": "difluoro(oxalato)borate anion: SEI/CEI film former, low-T interfacial impedance reduction"},
        {"smiles": "[O-]P(=O)(F)F", "name": "LiDFP-anion",
         "role": "difluorophosphate anion: interfacial film former, low-T impedance reduction"},
    ],
    "llm_reason": "Grid storage targets map to three failure modes: SEI growth "
    "(500 nm@100 cyc / 550 nm@500 cyc) -> film-forming additives FEC/VC/PS; "
    "4C plating -> robust fluorinated SEI (FEC, LiDFOB); -20 C retention >=90% "
    "-> low-viscosity ester co-solvent EP and low-impedance interfacial anions "
    "LiDFOB/LiDFP. Anions screened as isolated anions (mace on charged species "
    "is screening-grade only; their cell-level benefit is judged via the "
    "parameter bridge at Stage 3, not via the molecular funnel).",
}

append_entry(ws, entry)
print("propose R1 written")
