"""Content invariants and executable Java checks for the generated exam pack."""
import json, re, subprocess, tempfile, unittest, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def read_pack(sid):
    text=(ROOT/'practice_data'/f'{sid}.js').read_text(encoding='utf-8')
    return json.loads(text.split(']=',1)[1].strip().rstrip(';'))

class ExamPackTests(unittest.TestCase):
    def test_revised_challenges_and_complete_writing_models(self):
        eng=read_pack('english1')['bank']
        models=[q for q in eng if q.get('modelWords')]
        self.assertEqual(len(models),10);self.assertTrue(all(300<=q['modelWords']<=350 for q in models))
        letters=[q for q in eng if q['section'].startswith('Letters')]
        self.assertTrue(all('One complete model letter' in q['answer'] and len(q['answer'].split())>120 for q in letters))
        hindi=read_pack('hindi')['bank'];writing=[q for q in hindi if q.get('category')=='writing']
        self.assertEqual(len(writing),20)
        self.assertTrue(all(len(q['answer'].split())>100 for q in writing))
        self.assertTrue(all(len(q['answer'].split())>90 for q in hindi if q.get('category')=='literature'))
        for q in read_pack('maths')['bank'][-100:]:
            self.assertNotRegex(q['prompt'],r'(?i)explain why|student|classmate|pupil|can k be determined')
            self.assertGreaterEqual(len(q['answer'].splitlines()),3)
        geo=read_pack('geo')['bank'];self.assertEqual(sum(q['id'].startswith('geo-india-map-') for q in geo),20)
        self.assertEqual(sum(q['id'].startswith('geo-topo-') for q in geo),20)
        from build_visuals import paper_features,project
        for n in range(1,21):
            marking,ident=paper_features(n);self.assertEqual(len({x[0] for x in marking+ident}),10)
        # The supplied LCC projection must place Delhi east of Mumbai and north of it.
        dx,dy=project(77.21,28.61);mx,my=project(72.88,19.08)
        self.assertGreater(dx,mx);self.assertGreater(dy,my)
    def test_bank_counts_and_unique_prompts(self):
        for path in (ROOT/'practice_data').glob('*.js'):
            sid=path.stem;bank=read_pack(sid)['bank']
            self.assertEqual(len(bank),len({q['id'] for q in bank}),sid)
            signatures=[json.dumps([q['prompt'],[p.get('prompt') for p in q.get('parts',[]) if isinstance(p,dict)],[f['src'] for f in q.get('figures',[])]],ensure_ascii=False) for q in bank]
            self.assertEqual(len(bank),len(set(signatures)),sid)
            self.assertTrue(all(q['answer'] and q['marks']>0 for q in bank))
            if sid in ['maths','phy','chem','bio']:
                self.assertEqual(len(bank),2100);self.assertFalse(any(q.get('options') for q in bank))
                self.assertEqual(sum(bool(q.get('challenge')) for q in bank),100)
                self.assertTrue(all(q.get('challenge') for q in bank[-100:]))
        comp=read_pack('computer')['bank']
        self.assertEqual(collections.Counter(q['priority'] for q in comp if q.get('priority')),dict.fromkeys(range(1,21),5))
        eng=read_pack('english1')['bank']
        self.assertEqual(collections.Counter(q['paperKind'] for q in eng if q.get('paperKind')),dict.fromkeys(['verb','preposition','join','transform'],250))

    def test_twenty_papers_marks_and_complete_answers(self):
        def check(q):
            self.assertGreater(q['marks'],0)
            if q.get('parts') and isinstance(q['parts'][0],dict):
                self.assertEqual(q['marks'],sum(x['marks'] for x in q['parts']))
                for part in q['parts']:check(part)
            elif q.get('choices'):
                self.assertTrue(all(x['marks']==q['marks'] for x in q['choices']))
                for part in q['choices']:check(part)
            else:self.assertTrue(q.get('answer'),q.get('id'))
            if q.get('options'):
                self.assertEqual(len(q['options']),4);self.assertEqual(len(set(q['options'])),4)
                self.assertIn(q['correct'],range(4))
            self.assertFalse(re.search(r'\b(teacher must supply|see the missing diagram)\b',q.get('prompt',''),re.I))
            for f in q.get('figures',[])+q.get('answerFigures',[]):self.assertTrue((ROOT/f['src']).is_file(),f['src'])
        total=0
        for path in (ROOT/'practice_data').glob('*.js'):
            sid=path.stem;papers=read_pack(sid)['papers'];self.assertEqual(len(papers),20)
            self.assertEqual(len({json.dumps(p['sections'],ensure_ascii=False) for p in papers}),20,sid)
            for p in papers:
                total+=1;self.assertEqual(p['marks'],100 if sid=='computer' else 80)
                self.assertEqual(sum(s['marks'] for s in p['sections'])+p.get('additionalChoiceMarks',0),p['marks'])
                for s in p['sections']:
                    self.assertTrue(s['questions']);self.assertLessEqual(s['attempt'],len(s['questions']))
                    self.assertEqual(sum(q['marks'] for q in s['questions'][:s['attempt']]),s['marks'])
                    for q in s['questions']:check(q)
                name=f'paper-{p["number"]:02}.html';text=(ROOT/'subjects'/sid/'practice'/name).read_text(encoding='utf-8')
                self.assertNotIn('class="solution"',text)
        self.assertEqual(total,200)

    def test_java_programs_compile_and_execute(self):
        javac=Path.home()/'.jdks'/'jdk-21.0.12+8'/'bin'/'javac.exe';java=javac.with_name('java.exe')
        if not javac.exists():self.skipTest('JDK 21 not available at configured local path')
        from question_builders.computer import program_variant
        from question_builders.computer_reference import PROGRAMS
        with tempfile.TemporaryDirectory(prefix='icse-java-') as directory:
            out=Path(directory);sources=[];cases=[]
            for i,p in enumerate(PROGRAMS):
                for v in range(5):
                    q=program_variant(p,i,v);name=p['name']+str(v);source=out/(name+'.java');source.write_text(q['code'].replace(p['name'],name),encoding='utf-8');sources.append(str(source))
                    if v==0:cases.extend((name,inp,expected) for inp,expected in p['cases'])
            compiled=subprocess.run([str(javac),'-encoding','UTF-8','-d',str(out)]+sources,capture_output=True,text=True)
            self.assertEqual(compiled.returncode,0,compiled.stderr)
            # Variant boundary and changed-specification cases, independent of the Java answer.
            cases.extend([
                ('WaterBill4','Riya\n101\n','Riya\n957.6'),
                ('CharAudit1','AbC_29!\n','2 2 1 2'),
                ('BubbleChars1','a g e d b f c\n','a g e d b f c\ng f e d c b a'),
                ('SelectionNames1','f a c b e d\n','A\nB\nC\nD\nE\nF'),
                ('BalancedDigits4','126\n','Not balanced'),
                ('TitleCase2','ONE TWO THREE FOUR\n','oNE tWO tHREE FOUR'),
                ('PronicCheck3','12\n','Matches'),
                ('ProductLookup3','3 pen 4 PEN 9 box 1 PEN\n','9.0'),
                ('WordFilter1','aba cat blue ice\n','CAT\nCount = 1'),
            ])
            norm=lambda x:'\n'.join(line.rstrip() for line in x.strip().splitlines())
            for name,inp,expected in cases:
                run=subprocess.run([str(java),'-cp',str(out),name],input=inp,text=True,capture_output=True,timeout=8)
                self.assertEqual(run.returncode,0,name+run.stderr)
                self.assertEqual(norm(run.stdout),norm(expected),name)
            # Execute the 350 generated numeric Section A traces in one JVM.
            statements=[];expected=[]
            for q in read_pack('computer')['bank']:
                k=q.get('family')
                if q.get('category')!='short' or k not in ['0','1','3','5','6','9','19']:continue
                prompt=q['prompt'];expr=q['shortAnswer']
                if k=='0':code=prompt.split(' State ')[0]+' System.out.println(c);'
                elif k=='1':code='System.out.println('+prompt[len('Evaluate '):].split(' in Java')[0]+');'
                elif k=='3':code=prompt.split(' Give ')[0]+' System.out.println(s);'
                elif k=='5':
                    a,b=map(int,re.search(r'new int\[(\d+)\]\[(\d+)\]',prompt).groups());code=f'System.out.println({a}*{b}*4);'
                elif k=='6':code='System.out.println('+re.search(r'Math.pow\([^;]+?\)',prompt).group()+');'
                elif k=='9':code=prompt.split(' State ')[0]+' System.out.println(x);'
                else:code=prompt.split(' Give ')[0]+' System.out.println(count);'
                statements.append('{'+code+'}');expected.append(float(expr))
            trace=out/'TraceCheck.java';trace.write_text('public class TraceCheck{public static void main(String[]args){'+''.join(statements)+'}}',encoding='utf-8')
            compiled=subprocess.run([str(javac),'-d',str(out),str(trace)],capture_output=True,text=True);self.assertEqual(compiled.returncode,0,compiled.stderr)
            run=subprocess.run([str(java),'-cp',str(out),'TraceCheck'],capture_output=True,text=True,timeout=8)
            actual=[float(x) for x in run.stdout.splitlines()];self.assertEqual(actual,expected)

if __name__=='__main__':unittest.main(verbosity=2)
