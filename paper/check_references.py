# Every figure/table defined in paper must be referenced at least once in body text.
# (This is a standard journal requirement: no orphan floats.)
import re
import pathlib

files = list(pathlib.Path("sections").glob("*.tex")) + [
    pathlib.Path("main.tex"),
    pathlib.Path("supplementary.tex"),
]

tabs = re.compile(r"\\label\{(tab:[a-z0-9]+)\}")
figs = re.compile(r"\\label\{(fig:[a-z0-9]+)\}")
ref = re.compile(r"\\ref\s*\{((?:tab|fig):[a-z0-9]+)\}")

labels, refs = set(), set()
for f in files:
    if not f.exists():
        continue
    txt = f.read_text(encoding="utf-8")
    labels |= set(tabs.findall(txt))
    labels |= set(figs.findall(txt))
    refs |= set(ref.findall(txt))

orphans = sorted(labels - refs)
print("floats defined:", len(labels))
print("floats referenced:", len(refs))
print("ORPHAN floats (never referenced):", orphans if orphans else "NONE")
