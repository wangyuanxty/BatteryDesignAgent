# -*- coding: utf-8 -*-
import json

es = [json.loads(l) for l in open("runs/exp/t1_r3/log.jsonl", encoding="utf-8-sig") if l.strip()]
print("entries:", len(es))
for e in es:
    a = e.get("action", "?")
    r = e.get("round", "-")
    extra = ""
    if a == "evaluate":
        extra = f"verdict={e.get('verdict')} cand={e.get('candidate','?')}"
    if a == "final":
        extra = f"verdict={e.get('verdict')}"
    if a == "endorse":
        extra = f"skipped={e.get('skipped')}"
    print(f"{a:>9} round={str(r):<3} {extra}")
