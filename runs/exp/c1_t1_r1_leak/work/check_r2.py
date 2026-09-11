import json

L = 'D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/c1_t1_r1/log.jsonl'
for i, line in enumerate(open(L, encoding='utf-8-sig')):
    line = line.strip()
    if not line:
        continue
    e = json.loads(line)
    a = e.get('action')
    r = e.get('round')
    c = e.get('candidate', '')
    v = e.get('verdict', '')
    cr = 'CRITERIA' if 'criteria' in e else ''
    print(i, a, r, c, v, cr)
