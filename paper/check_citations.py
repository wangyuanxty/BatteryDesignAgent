# Verify every \cite key in body text has a matching bib entry, and list unused entries.
import re
import pathlib

bib = open("paper.bib", encoding="utf-8").read()
bibkeys = set(re.findall(r"@\w+\{([^,]+),", bib))

flatsrc = []
for f in list(pathlib.Path("sections").glob("*.tex")) + [pathlib.Path("main.tex"), pathlib.Path("supplementary.tex")]:
    flatsrc.append(f.read_text(encoding="utf-8"))
txt = "\n".join(flatsrc)

citekeys = set()
for m in re.findall(r"\\cite\{([a-zA-Z0-9_,\s]+)\}", txt):
    for k in m.split(","):
        k = k.strip()
        if k:
            citekeys.add(k)

missing = citekeys - bibkeys
unused = bibkeys - citekeys
print("cite keys used:", len(citekeys))
print("bib keys:", len(bibkeys))
print("MISSING cite->bib:", sorted(missing) if missing else "NONE")
print("unused bib entries:", sorted(unused) if unused else "NONE")
