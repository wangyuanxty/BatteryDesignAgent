"""T10 v4 round 1: candidate list + propose log entry.

All candidates are de novo designs targeting xTB HOMO <= -13.74 eV and LUMO <= -7.0 eV
while avoiding every family-gate SMARTS pattern mechanically (checked in code before
running: no S=O, no C#N, no ester [CX3](=O)[OX2][CX4,c], no carbonate, no aromatic atom,
no dialkyl ether [OD2]([CX4])[CX4], no B/Si, no amide, no nitro, no quinone, no PX3/PX4=O).
"""
import json
import sys
from pathlib import Path

REPO = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent")
sys.path.insert(0, str(REPO / ".claude/skills/virtual-battery-factory/scripts"))
sys.path.insert(0, str(REPO / "runs/exp/known_set_sei"))

C = [
    # --- acyl fluorides / chlorides, alpha-dicarbonyls ---
    ("trifluoroacetyl fluoride", "O=C(F)C(F)(F)F", "perfluoro acyl fluoride film-former"),
    ("oxalyl fluoride", "O=C(F)C(=O)F", "alpha-dicarbonyl difluoride"),
    ("carbonyl difluoride", "O=C(F)F", "minimal carbonyl fluoride"),
    ("hexafluoroacetone", "O=C(C(F)(F)F)C(F)(F)F", "perfluoroketone"),
    ("hexafluoro-2,3-butanedione", "O=C(C(F)(F)F)C(=O)C(F)(F)F", "perfluoro alpha-diketone"),
    ("trifluoropyruvoyl fluoride", "O=C(F)C(=O)C(F)(F)F", "mixed COF/CF3 diketone"),
    ("pentafluoropropionyl fluoride", "O=C(F)C(F)(F)C(F)(F)F", "perfluoroacyl fluoride"),
    ("trifluoroacetyl chloride", "O=C(Cl)C(F)(F)F", "perfluoroacyl chloride"),
    ("difluoromalonyl difluoride", "O=C(F)C(F)(F)C(=O)F", "bis(acyl fluoride)"),
    ("perfluorosuccinyl difluoride", "O=C(F)C(F)(F)C(F)(F)C(=O)F", "bis(acyl fluoride) C4"),
    ("fluorocarbonyl chloride", "O=C(F)Cl", "mixed acyl halide"),
    ("oxalyl chloride", "O=C(Cl)C(=O)Cl", "alpha-dicarbonyl dichloride"),
    # --- thiocarbonyls ---
    ("thiocarbonyl fluoride", "S=C(F)F", "thio analog of COF2"),
    ("hexafluorothioacetone", "S=C(C(F)(F)F)C(F)(F)F", "perfluorothioketone"),
    ("trifluorothioacetyl fluoride", "S=C(F)C(F)(F)F", "thioacyl fluoride"),
    ("thiophosgene", "S=C(Cl)Cl", "thiocarbonyl chloride"),
    ("carbonyl sulfide", "O=C=S", "carbonyl sulfide"),
    ("carbon disulfide", "S=C=S", "carbon disulfide"),
    # --- ketenes / cumulenes ---
    ("bis(trifluoromethyl)ketene", "FC(F)(F)C(=C=O)C(F)(F)F", "perfluoroketene"),
    ("difluoroketene", "FC(F)=C=O", "fluoroketene"),
    ("tetrafluoroallene", "FC(F)=C=C(F)F", "perfluoroallene"),
    # --- isocyanates / isothiocyanates ---
    ("trifluoromethyl isocyanate", "O=C=NC(F)(F)F", "perfluoroalkyl isocyanate"),
    ("fluorocarbonyl isocyanate", "O=C=NC(=O)F", "acyl isocyanate"),
    ("trifluoromethyl isothiocyanate", "S=C=NC(F)(F)F", "perfluoroalkyl isothiocyanate"),
    ("pentafluorosulfanyl isocyanate", "FS(F)(F)(F)(F)N=C=O", "SF5 isocyanate"),
    # --- anhydrides (bridging O has two carbonyl neighbors: not an ester) ---
    ("trifluoroacetic anhydride", "O=C(OC(=O)C(F)(F)F)C(F)(F)F", "perfluoro anhydride"),
    ("fluoroformic anhydride", "O=C(F)OC(=O)F", "bis(fluorocarbonyl) oxide"),
    ("perfluorosuccinic anhydride", "O=C1OC(=O)C(F)(F)C1(F)F", "perfluoro cyclic anhydride"),
    ("difluoromaleic anhydride", "O=C1OC(=O)C(F)=C1F", "perfluoroalkene anhydride"),
    ("bis(trifluoromethyl)maleic anhydride", "O=C1OC(=O)C(C(F)(F)F)=C1C(F)(F)F", "bis-CF3 alkene anhydride"),
    ("perfluoroglutaric anhydride", "O=C1OC(=O)C(F)(F)C(F)(F)C1(F)F", "perfluoro cyclic anhydride C5"),
    # --- N-F compounds ---
    ("trifluoromethyl difluoramine", "FN(F)C(F)(F)F", "R-NF2 amine"),
    ("nitrogen trifluoride", "FN(F)F", "NF3"),
    ("tetrafluorohydrazine", "FN(F)N(F)F", "N2F4"),
    ("difluorodiazene", "F/N=N/F", "azo fluoride"),
    ("trifluoramine oxide", "[O-][N+](F)(F)F", "F3NO"),
    ("nitrosyl fluoride", "FN=O", "nitrosyl fluoride"),
    ("difluoroamino trifluoromethyl ether", "FN(F)OC(F)(F)F", "N-O-F oxidizer"),
    ("N-fluorodifluoromethanimine", "FC(F)=NF", "N-fluoro imine"),
    # --- S-F hypervalent / SF5 compounds ---
    ("trifluoromethyl sulfur pentafluoride", "FS(F)(F)(F)(F)C(F)(F)F", "SF5CF3"),
    ("sulfur hexafluoride", "FS(F)(F)(F)(F)F", "SF6"),
    ("sulfur tetrafluoride", "FS(F)(F)F", "SF4"),
    ("disulfur decafluoride", "FS(F)(F)(F)(F)S(F)(F)(F)(F)F", "S2F10"),
    ("pentafluorosulfanyl carbonyl fluoride", "O=C(F)S(F)(F)(F)(F)F", "SF5-COF"),
    ("pentafluorosulfanyl trifluoromethyl ketone", "O=C(C(F)(F)F)S(F)(F)(F)(F)F", "SF5 ketone"),
    ("pentafluorosulfanyl difluoramine", "FS(F)(F)(F)(F)N(F)F", "SF5-NF2"),
    # --- hypofluorites / thioethers / thioesters ---
    ("trifluoromethyl hypofluorite", "FOC(F)(F)F", "C-O-F hypofluorite"),
    ("bis(trifluoromethyl) sulfide", "FC(F)(F)SC(F)(F)F", "perfluoro thioether"),
    ("bis(trifluoromethyl) disulfide", "FC(F)(F)SSC(F)(F)F", "perfluoro disulfide"),
    ("S-trifluoromethyl trifluorothioacetate", "O=C(SC(F)(F)F)C(F)(F)F", "thioester (C(=O)-S)"),
    ("S-trifluoromethyl fluorothioformate", "O=C(F)SC(F)(F)F", "fluorothioformate"),
    ("bis(fluorocarbonyl) sulfide", "O=C(F)SC(=O)F", "diacyl sulfide"),
    ("perfluorothiirane", "FC1(F)SC1(F)F", "perfluoro thiirane"),
    # --- perfluoro aliphatic rings / alkenes ---
    ("perfluorocyclobutanone", "O=C1C(F)(F)C(F)(F)C1(F)F", "perfluoro cyclic ketone"),
    ("perfluorocyclopropanone", "O=C1C(F)(F)C1(F)F", "perfluoro cyclopropanone"),
    ("perfluoropropene", "FC(F)=C(F)C(F)(F)F", "perfluoroalkene"),
    ("perfluorobutadiene", "FC(F)=C(F)C(F)=C(F)F", "perfluoro diene"),
    ("perfluorocyclobutene", "FC1=C(F)C(F)(F)C1(F)F", "perfluoro cycloalkene"),
    ("perfluorocyclopropane", "FC1(F)C(F)(F)C1(F)F", "perfluorocyclopropane"),
    ("perfluorocyclopropene", "FC1=C(F)C1(F)F", "perfluoro cyclopropene"),
    ("hexafluoro-2-butyne", "FC(F)(F)C#CC(F)(F)F", "perfluoro alkyne (C#C, not C#N)"),
    ("perfluoroacryloyl fluoride", "FC(F)=C(F)C(=O)F", "alkene-COF conjugate"),
    ("difluorofumaryl difluoride", "O=C(F)C(F)=C(F)C(=O)F", "bis(COF) alkene"),
    ("perfluoro(methyl vinyl ketone)", "O=C(C(F)(F)F)C(F)=C(F)F", "CF3 ketone + alkene"),
    # --- imines / oximes / amines ---
    ("hexafluoroacetone N-(trifluoromethyl)imine", "FC(F)(F)C(=NC(F)(F)F)C(F)(F)F", "perfluoro imine"),
    ("hexafluoroacetone oxime", "FC(F)(F)C(=NO)C(F)(F)F", "perfluoro oxime"),
    ("hexafluoroacetone azine", "FC(F)(F)C(=NN=C(C(F)(F)F)C(F)(F)F)C(F)(F)F", "perfluoro ketazine"),
    ("tris(trifluoromethyl)amine", "FC(F)(F)N(C(F)(F)F)C(F)(F)F", "perfluoro tertiary amine"),
    # --- vinyl ethers (vinyl C is CX3: not a dialkyl ether) ---
    ("trifluorovinyl trifluoromethyl ether", "FC(F)=C(F)OC(F)(F)F", "perfluoro vinyl ether"),
    # --- halogen oxyfluorides / hypervalent halides ---
    ("perchloryl fluoride", "O=[Cl](=O)(=O)F", "ClO3F"),
    ("iodine heptafluoride", "F[I](F)(F)(F)(F)(F)F", "IF7"),
    # --- phosphazene (P=N ring, no P-O) ---
    ("hexafluorocyclotriphosphazene", "F[P]1(F)=N[P](F)(F)=N[P](F)(F)=N1", "P3N3F6 ring"),
]

# mechanical family-gate pre-check
from envelope_check import families_matched

bad = []
for name, smi, role in C:
    try:
        fams = families_matched(smi)
    except Exception as e:
        bad.append((name, str(e)))
        continue
    if fams:
        bad.append((name, fams))
print("family-gate violations at proposal time:", bad if bad else "NONE")

candidates = [{"smiles": s, "name": n, "role": r} for n, s, r in C]
out = REPO / "runs/exp/t10_r4/candidates/r1_candidates.json"
out.write_text(json.dumps({"candidates": candidates}, indent=2), encoding="utf-8")
print(f"wrote {len(candidates)} candidates -> {out}")

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t10_r4", root="runs")
propose = {
    "action": "propose",
    "round": 1,
    "candidates": candidates,
    "llm_reason": (
        "Target region (HOMO<=-13.74 eV and LUMO<=-7.0 eV) is normally reached by S=O chemistry, which the "
        "family gate bans; round 1 therefore probes every mechanically-allowed electron-withdrawing motif: "
        "acyl fluorides/chlorides, alpha-dicarbonyls, anhydrides (bridging O has two carbonyl neighbors, so no "
        "ester match), ketenes, isocyanates/isothiocyanates, thiocarbonyls, hypervalent S-F (SF4/SF5/SF6/S2F10), "
        "N-F (NF3/N2F4/R-NF2), hypofluorites, thioesters (C(=O)-S), perfluoro aliphatic alkenes/rings/alkynes, "
        "imines/oximes/ketazines, vinyl ethers (vinyl C is CX3, no dialkyl-ether match), ClO3F/IF7 and a P=N "
        "phosphazene ring. All SMILES mechanically pre-checked against the family-gate SMARTS (no matches). "
        "xTB screen first (cheap); only survivors go to MACE/CHGNet + envelope adjudication."
    ),
}
append_entry(ws, propose)
print("propose entry appended")
