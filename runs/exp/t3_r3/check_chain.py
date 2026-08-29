"""Closing self-check helper: print the log action chain for t3_r3."""
import json

actions = []
for line in open("runs/exp/t3_r3/log.jsonl", encoding="utf-8"):
    e = json.loads(line)
    a = e.get("action", "criteria-meta")
    if a == "propose":
        actions.append(f"propose_r{e['round']}")
    elif a == "evaluate":
        verdict = e.get("verdict", "?")
        cand = e.get("candidate", "")
        actions.append(f"evaluate_r{e['round']}_{cand}={verdict}")
    else:
        actions.append(a)
print(" | ".join(actions))
print("total entries:", len(actions))