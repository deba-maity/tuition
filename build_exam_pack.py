"""Build the original banks, twenty fixed papers per subject, and research folders.

Run after build_icse_2027.py, or independently against its checked metadata file.
All exports work from file://; no network or browser PDF service is required.
"""
import csv, html, json, shutil, base64
from pathlib import Path
from question_builders import maths,physics,chemistry,biology,english_language,readings,literature,humanities,computer,hindi
from question_builders.papers import build_papers
from question_builders.plans import make_plan
from question_builders import challenge_bank,editorial,worked_solutions,english_models,hindi_models,maps_and_diagrams,literature_models

ROOT=Path(__file__).resolve().parent
ASSET_CACHE={}
def embedded_asset(src):
    if src not in ASSET_CACHE:
        path=ROOT/src;mime='image/svg+xml' if path.suffix=='.svg' else 'image/png'
        ASSET_CACHE[src]='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
    return ASSET_CACHE[src]
def dump(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text('\n'.join(line.rstrip() for line in text.split('\n')),encoding='utf-8')

def render_question(q,answers=False,label=''):
    esc=lambda s:html.escape(str(s))
    title=f'<b>{esc(q.get("label",label))}</b>' if q.get('label',label) else ''
    out=f'<article class="exam-question">{title} <span class="marks">[{q["marks"]}]</span><div class="prompt">{esc(q.get("prompt",""))}</div>'
    for f in q.get('figures',[]):out+=f'<figure><img style="max-width:100%;max-height:650px" src="{embedded_asset(f["src"])}" alt="{esc(f["caption"])}"><figcaption>{esc(f["caption"])}</figcaption></figure>'
    if q.get('resourcePdf'):
        sheet=Path(q['resourcePdf']).stem
        url='https://surveyofindia.gov.in/files/'+('45D10.pdf' if sheet=='G43S10' else '45d7education%20map.pdf')
        out+=f'<p><a href="{url}">Open the complete original sheet PDF</a></p>'
    if q.get('options') and '\n(a)' not in q.get('prompt',''):out+='<ol type="a">'+''.join(f'<li>{esc(o)}</li>' for o in q['options'])+'</ol>'
    if answers and q.get('answer'):
        out+='<div class="solution"><b>Worked solution / model answer</b>'+('<p>'+esc(q['method'])+'</p>' if q.get('method') else '')+'<pre>'+esc(q['answer'])+'</pre>'
        if q.get('solutionTable'):out+='<table>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in [q['solutionTable']['headers']]+q['solutionTable']['rows'])+'</table>'
        for f in q.get('answerFigures',[]):out+=f'<figure><img style="max-width:100%" src="{embedded_asset(f["src"])}" alt="{esc(f["caption"])}"><figcaption>{esc(f["caption"])}</figcaption></figure>'
        out+='</div>'
    if q.get('choices'):
        out+='<p><em>Choose one:</em></p>'+''.join(render_question(x,answers,f'Option {i+1}') for i,x in enumerate(q['choices']))
    if q.get('parts') and isinstance(q['parts'][0],dict):out+=''.join(render_question(x,answers,f'({i+1})') for i,x in enumerate(q['parts']))
    return out+'</article>'

def paper_html(p,answers=False):
    esc=lambda s:html.escape(str(s))
    body=f'<header><p>ICSE 2027 · Original practice</p><h1>{esc(p["title"])}</h1><p>{p["marks"]} marks · {esc(p["time"])}</p><h2>{"Answer sheet — model answers and marking points" if answers else "Question paper"}</h2></header>'
    body+=''.join('<p>'+esc(x)+'</p>' for x in p['instructions'])
    if p['adaptation']:body+='<p class="adaptation">'+esc(p['adaptation'])+'</p>'
    for s in p['sections']:
        body+=f'<section><h2>{esc(s["title"])}</h2><p>{esc(s["instructions"])}</p>'+''.join(render_question(q,answers) for q in s['questions'])+'</section>'
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+esc(p['title'])+'</title><style>body{font:16px/1.65 Georgia,"Nirmala UI",serif;max-width:900px;margin:40px auto;padding:0 24px;color:#18232d}h1{font-size:28px}h2{font-size:21px}.exam-question{padding:14px 0;border-bottom:1px solid #ddd;break-inside:avoid}.exam-question .exam-question{margin-left:18px}.marks{float:right}.prompt,pre{white-space:pre-wrap;overflow-wrap:anywhere}pre{font:14px/1.6 Consolas,"Nirmala UI",monospace}.solution{background:#edf5ef;padding:12px;margin-top:12px}.adaptation{font-size:14px;color:#53636b}@media print{body{margin:0;max-width:none;padding:0}h2{break-after:avoid}}</style><body>'+body+'</body></html>'

def validate_bank(sid,bank):
    assert len({q['id'] for q in bank})==len(bank),(sid,'duplicate IDs')
    def signature(q):return json.dumps([q['prompt'],[p.get('prompt') for p in q.get('parts',[]) if isinstance(p,dict)],[f['src'] for f in q.get('figures',[])]],ensure_ascii=False)
    assert len({signature(q) for q in bank})==len(bank),(sid,'duplicate questions')
    assert all(q['answer'].strip() and q['marks']>0 for q in bank)
    if sid in ('maths','phy','chem','bio'):
        assert len(bank)==2100 and all(not q.get('options') for q in bank)
        assert sum(bool(q.get('challenge')) for q in bank)==100
        assert all(q.get('challenge') for q in bank[-100:])
    if sid=='computer':
        assert len(bank)==1100
        assert all(sum(q.get('priority')==rank for q in bank)==5 for rank in range(1,21))
    if sid=='english1':assert sum(bool(q.get('paperKind')) for q in bank)==1000

def main():
    raw=(ROOT/'icse_2027_data.js').read_text(encoding='utf-8');data=json.loads(raw[raw.index('=')+1:].strip().rstrip(';'))
    builders={'maths':maths.make_bank,'phy':physics.make_bank,'chem':chemistry.make_bank,'bio':biology.make_bank,'english1':lambda:english_language.make_bank(readings.make_bank()),'english2':literature.make_bank,'computer':computer.make_bank,'histciv':humanities.history_bank,'geo':humanities.geography_bank}
    catalogue={};totals={}
    for meta in data['subjects']:
        sid=meta['id'];bank=hindi.make_bank(meta['practice']) if sid=='hindi' else builders[sid]()
        if sid in ('maths','phy','chem','bio'):bank=challenge_bank.rebuild_challenges(sid,bank)
        bank=editorial.revise(sid,bank)
        if sid in ('maths','phy','chem','bio'):bank=challenge_bank.repair_duplicates(sid,bank)
        if sid=='english1':bank=english_models.enrich(bank)
        if sid=='hindi':bank=literature_models.enrich(hindi_models.enrich(bank))
        bank=maps_and_diagrams.enrich(sid,bank)
        bank=worked_solutions.enrich(sid,bank)
        validate_bank(sid,bank);papers=build_papers(sid,bank,meta);plan=make_plan(sid)
        for paper in papers:
            if sid in ('maths','phy','chem','bio'):paper['adaptation']='Original syllabus-scoped practice. Diagrams, where included, are schematic; use the numerical values specified in the question.'
        payload=dict(bank=bank,papers=papers,plan=plan,edition='2026-11-16-worked')
        dump(ROOT/'practice_data'/f'{sid}.js',f'window.ICSE_PRACTICE=window.ICSE_PRACTICE||{{}};window.ICSE_PRACTICE[{json.dumps(sid)}]='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n')
        catalogue[sid]=dict(bankCount=len(bank),paperCount=len(papers),families=len({q.get('family',q['topic']) for q in bank}),plan=plan)
        destination=ROOT/'subjects'/sid
        for paper in papers:
            dump(destination/'practice'/f'paper-{paper["number"]:02}.html',paper_html(paper))
            dump(destination/'practice'/f'answers-{paper["number"]:02}.html',paper_html(paper,True))
        evidence=['# '+meta['name']+' — evidence and study choices','Reviewed main-paper metadata: 2023–2026. The 2027 syllabus/specimen is the format reference. This is not an all-subject ten-year frequency audit.','## Study route',plan['strategy'],plan['rationale']]
        for key,title in [('core','Full long-answer preparation'),('backup','Backup preparation'),('light','Lighter compulsory review')]:
            if plan[key]:evidence+=['## '+title]+['- '+x for x in plan[key]]
        evidence+=['## Evidence anchors']+[f'- {year} {q}: {description}' for year,q,description in meta['evidence']]
        evidence+=['## Sources',f'- [Syllabus]({meta["syllabus"]})']+[f'- [{p["year"]} actual paper]({p["url"]})' for p in meta['sources']]
        if plan['source']:evidence+=[f'- [Official 2027 specimen]({plan["source"]})']
        evidence+=['## Practice content',f'{len(bank)} original questions/variants across {catalogue[sid]["families"]} named families. Twenty fixed papers. These are practice selections, not calibrated forecasts. Numerical variants are not copied from Selina, Goyal or another textbook.','The practice folder has question-only HTML files and separate worked-solution/model-answer HTML files. Images are embedded so a downloaded HTML file remains usable away from the site. Both versions print to PDF. On the website answers unlock only after marking the paper complete.','Geography uses original Survey of India sheets and an India outline derived from its authoritative vector. Location overlays are schematic study guides. Physics includes labelled circuit, lever and ray-construction diagrams. Full writing models are supplied; they illustrate one valid response rather than compulsory wording.']
        dump(destination/'research'/'README.md','\n\n'.join(evidence)+'\n')
        with (destination/'research'/'paper-evidence.csv').open('w',encoding='utf-8-sig',newline='') as stream:
            writer=csv.writer(stream);writer.writerow(['Year','Question','Observed family']);writer.writerows(meta['evidence'])
        totals[sid]=len(bank)
    # Retain the previously requested Computer mock as Paper 01's PDF attachment.
    downloads=Path.home()/'Downloads'
    for name in ['ICSE_2027_Computer_Applications_100_Mark_Mock.pdf','ICSE_2027_Computer_Applications_Research_and_Practice.pdf']:
        source=downloads/name;target=ROOT/'assets'/name
        if source.exists():target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    dump(ROOT/'exam_catalog.js','window.ICSE_EXAM_CATALOG='+json.dumps(catalogue,ensure_ascii=False,separators=(',',':'))+';\n')
    geography_sources=next(s for s in data['subjects'] if s['id']=='geo')['sources'];urls={str(s['year']):s['url'] for s in geography_sources}
    topo_rows=[['2016 (context)','45D/7','Board paper','https://cdn1.byjus.com/wp-content/uploads/2020/07/ICSE-Class-10-Geography-Question-Paper-2016.pdf'],['2017','45D/10','Board paper','https://cdn1.byjus.com/wp-content/uploads/2020/06/ICSE-Class-10-Geography-Question-Paper-2017.pdf'],['2018','45D/7','Board paper','https://cdn1.byjus.com/wp-content/uploads/2020/06/ICSE-Class-10-Geography-Question-Paper-2018.pdf'],['2019','45D/10','Board paper','https://cdn1.byjus.com/wp-content/uploads/2020/06/ICSE-Class-10-Geography-Question-Paper-2019.pdf'],['2020','Excluded','Pandemic cancellation; not a held-paper recurrence','https://api.sci.gov.in/supremecourt/2020/12580/12580_2020_32_1_22694_Order_26-Jun-2020.pdf'],['2021','Excluded','CISCE cancelled examinations','https://cisce.org/wp-content/uploads/2025/04/CISCE-SCHEME-ICSE-and-ISC.pdf'],['2022','Not compared','Split-semester format; no normal-paper sheet frequency asserted','https://meritbatch.com/icse-2022-geography-question-paper-solved-semester-2/']]+[[str(y),sheet,'Board paper; header checked',urls[str(y)]] for y,sheet in [(2023,'G43S7'),(2024,'G43S7'),(2025,'G43S10'),(2026,'G43S7')]]+[['2027 specimen','G43S10','Specimen; excluded from past-board frequency','https://cisce.org/wp-content/uploads/2026/08/ICSE-2027-SPECIMEN-502-GEOGRAPHY-QP-MS.pdf']]
    with (ROOT/'subjects'/'geo'/'research'/'topo-sheet-audit.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['Year','Sheet','Status','Source']);writer.writerows(topo_rows)
    dump(ROOT/'EXAM_PACK_README.txt','ICSE 2027 study pack — worked-answer edition\nOpen index.html directly, or run node serve_icse_site.js.\nEach subject has subjects/<subject>/research and subjects/<subject>/practice.\nTwenty fixed papers per subject; answers unlock after marking a paper complete. Revised-paper completion is tracked separately from the earlier edition.\nQuestion banks now show worked calculations, Java traces/tables, model writing and part-by-part literature answers. Short one-mark answers remain concise.\nThe writing repertoire includes ten English compositions and letters, and ten Hindi compositions and letters, with complete original models. Weak Hindi writing templates were removed instead of padding their answers.\nGeography: open Maps & topo sheets for 70 location exercises and original Survey of India PDFs G43S7 and G43S10. Grid limits/editions matter; match an exercise to its supplied sheet. Keep assets/maps with the pack for offline access to the complete sheets.\nDownloaded HTML papers embed their images; Print / Save PDF waits for question images to load. Physics includes schematic circuits, levers and completed ray constructions.\nUse Needs work / Got it / Correct on retest to build a mistake notebook and spaced review queue. Progress & mistakes shows family coverage and saved paper scores. The writing timer survives navigation/reload; self-mark after completion, then save your score and revision note. Backups can be exported/restored as JSON.\nA 95% target is tracked through timed practice, coverage and error correction; it is not a guaranteed examination result. Scores and mastery labels are self-recorded.\nAll practice text is original. Numerical variants are grouped by family, not presented as thousands of distinct concepts.\nEvidence: 2023–2026 all-subject inventory and 2027 syllabus/specimen, plus Geography sheet audit for 2017–2026 with 2016 context. Cancelled and split-semester years are labelled separately. Evergreen publisher listing was checked; the full book was not publicly available to audit.\nBuild: python -X utf8 build_exam_pack.py\nVisuals: python -X utf8 build_visuals.py\nChecks: python -X utf8 test_exam_pack.py; node test_browser.cjs; node test_study_features.cjs\n')
    print(json.dumps({'questions':totals,'papers':20*len(totals),'questions_total':sum(totals.values())}))

if __name__=='__main__':main()
