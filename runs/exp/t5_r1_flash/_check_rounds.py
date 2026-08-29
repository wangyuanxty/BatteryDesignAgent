import json, os
ws = os.path.dirname(os.path.abspath(__file__))
entries = [json.loads(ln) for ln in open(os.path.join(ws, "log.jsonl"), encoding="utf-8")]
for e in entries:
    a = e.get("action")
    if a in ("propose", "evaluate"):
        cands = [c.get("name") for c in e.get("candidates", [])] if a == "propose" else e.get("candidate", "")
        print(f"{a:8s} round={e.get('round')}  {cands if isinstance(cands, list) else cands}  {e.get('verdict','')}")
