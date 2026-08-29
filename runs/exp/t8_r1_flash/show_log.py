import json

for line in open("runs/exp/t8_r1_flash/log.jsonl", encoding="utf-8"):
    e = json.loads(line)
    a = e.get("action", "criteria")
    extra = ""
    if a == "propose":
        extra = "[" + ", ".join(c.get("name", "?") for c in e.get("candidates", [])) + "]"
    elif a == "evaluate":
        extra = f"{e.get('candidate')} -> {e.get('verdict')}"
    elif a == "final":
        extra = f"verdict={e.get('verdict')}"
    elif a == "funnel":
        extra = f"passed={e.get('passed')} rejected={e.get('rejected')}"
    elif a == "endorse":
        extra = f"skipped={e.get('skipped')}"
    elif a == "plan":
        extra = "-> design_plan.md"
    print(f"{a:10s} {extra}")
