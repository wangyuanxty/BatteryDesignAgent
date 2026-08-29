"""Scan log.jsonl for CJK content and mojibake artifacts after PS round-trip."""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
p = r"runs\exp\t4_r1_flash\log.jsonl"
lines = open(p, encoding="utf-8").read().splitlines()
print("lines:", len(lines))

cjk_re = re.compile(r"[一-鿿]")
moji_re = re.compile(r"Ã[\x80-\xbf]|â€|Â[\x80-\xbf]")
for i, line in enumerate(lines, 1):
    cjk = cjk_re.findall(line)
    moji = moji_re.findall(line)
    if cjk or moji:
        flag = "CJK" if cjk else ""
        flag += ("MOJI:" + "".join(moji)) if moji else ""
        print(f"line {i} [{flag}] {line[:120]}")

# parse every line as JSON to confirm structural integrity
for i, line in enumerate(lines, 1):
    try:
        json.loads(line)
    except Exception as e:
        print(f"line {i} JSON ERROR: {e}")
print("JSON parse check done")
