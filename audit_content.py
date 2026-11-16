"""Snapshot generated question quality before and after editorial improvements."""
import json, re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
def main():
    report={}
    for path in (ROOT/'practice_data').glob('*.js'):
        data=json.loads(path.read_text(encoding='utf-8').split(']=',1)[1].strip().rstrip(';'))
        bank=data['bank'];seen=set();samples=[]
        for q in bank:
            if q.get('challenge') and q['family'] not in seen:samples.append(q);seen.add(q['family'])
        report[path.stem]={'count':len(bank),'short_answers':sum(len(q['answer'].split())<20 for q in bank),'generic_answers':sum(bool(re.search(r'give.*example.*text|marking guide|correct.*context|use.*evidence|अपेक्षित',q['answer'],re.I)) for q in bank),'challenge_families':samples,'families':dict(Counter(q.get('family',q['topic']) for q in bank))}
    destination=ROOT/'research'/'content_quality_audit.json'
    destination.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    for sid,d in report.items():
        print(sid,d['count'],'short answers:',d['short_answers'],'generic answers:',d['generic_answers'])
        for q in d['challenge_families']:print(q['family'],'::',q['prompt'],'\nANSWER:',q['answer'])
if __name__=='__main__':main()
