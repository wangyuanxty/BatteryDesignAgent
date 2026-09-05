import json, os
repo = r'D:\research\degradation_prognostics\Battery_Design_Agent'
p = os.path.join(repo, 'runs', 't5_r1_mimo', 'log.jsonl')
entry = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {"name": "Candidate E", "struct": {}, "role": "tighter transport geometry with smaller particles/higher porosity and increased cooling relative to round 2 high-energy baseline"},
        {"name": "Candidate E2", "struct": {}, "role": "thermal-limit probe with further cooling increase to test whether 60C ceiling is reachable while preserving high-energy geometry"}
    ],
    "llm_reason": "Round 3 reuses the round 2 high-energy geometry but tightens transport and raises cooling to address the thermal breach seen in Candidate C/D. Candidate E is the main thermal-mitigation step; Candidate E2 probes whether additional cooling can close the remaining thermal gap without destabilizing plating margins."
}
with open(p, 'a', encoding='utf-8') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
print('appended round 3 propose entry')
