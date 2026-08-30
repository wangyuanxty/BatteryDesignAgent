# Global table shrinking patch for main.tex and supplementary.tex
for f in ["main.tex", "supplementary.tex"]:
    s = open(f, encoding="utf-8").read()
    probe = "% ---- global table shrinking ----"
    if probe in s:
        print(f, "already patched")
        continue
    anchor = "\\usepackage{longtable}\n"
    if anchor not in s:
        anchor = "\\usepackage{booktabs}\n"
    patch = ("\\usepackage{longtable}\n"
             "\\setlength{\\tabcolsep}{3.4pt}\n"
             "\\let\\origtable\\table\n"
             "\\renewcommand*{\\table}{\\footnotesize\\origtable}\n"
             "% ---- global table shrinking ----\n")
    assert anchor in s, f
    s = s.replace(anchor, patch, 1)
    open(f, "w", encoding="utf-8").write(s)
    print(f, "patched")
