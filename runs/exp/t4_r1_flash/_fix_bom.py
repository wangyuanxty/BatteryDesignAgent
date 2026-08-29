"""Strip BOM and verify UTF-8 integrity of log.jsonl after PS Set-Content round-trip."""
import sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"runs\exp\t4_r1_flash\log.jsonl"
raw = open(p, "rb").read()
print("starts with BOM:", raw.startswith(b"\xef\xbb\xbf"))
try:
    text = raw.decode("utf-8-sig")
    print("UTF-8 decode: OK, chars:", len(text), "lines:", text.count("\n") + 1)
except UnicodeDecodeError as e:
    print("UTF-8 decode FAILED:", e)
    sys.exit(1)

# mojibake check: look for replacement chars or latin-1 double-encoded CJK
bad = 0
for i, line in enumerate(text.splitlines(), 1):
    if "�" in line:
        bad += 1
        print("line", i, "has U+FFFD:", line[:80])
print("lines with replacement chars:", bad)

# write back without BOM (byte-identical apart from BOM)
new_raw = text.encode("utf-8")
open(p, "wb").write(new_raw)
print("rewrote without BOM, bytes:", len(new_raw), "(was", len(raw), ")")
