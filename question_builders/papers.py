"""Fixed original mocks with explicit offered/attempted marks and section choices."""
import copy
from .common import rng, mcq
from .paper_mcqs import make_mcqs
from .computer_reference import PROGRAMS
from .computer_reference_questions import MCQ, SHORT
from .verb_passages import verb_passage
from . import bio_papers
from .paper_shorts import short_questions

class Picker:
    def __init__(self,bank,seed):self.bank=bank;self.seed=seed;self.used=set();self.n=0;self.topics={}
    def take(self,marks=None,topic=None,section=None,where=None):
        pool=[q for q in self.bank if q['id'] not in self.used and (not topic or q['topic']==topic) and (not section or q.get('section')==section) and (not where or where(q))]
        if not pool:raise ValueError(f'Empty question pool {topic}/{section}')
        minimum=min(self.topics.get(q['topic'],0) for q in pool)
        pool=[q for q in pool if self.topics.get(q['topic'],0)==minimum]
        rng('paper-pick',self.seed*100+self.n).shuffle(pool);self.n+=1
        if marks:
            exact=[q for q in pool if q['marks']==marks]
            if exact:pool=exact
        q=copy.deepcopy(pool[0]);self.used.add(q['id'])
        self.topics[q['topic']]=self.topics.get(q['topic'],0)+1
        if marks:q['marks']=marks
        return q

def group(label,parts,prompt=''):
    return dict(label=label,prompt=prompt,marks=sum(q['marks'] for q in parts),parts=parts)

def section(title,questions,attempt=None,instructions=''):
    required=len(questions) if attempt is None else attempt
    marks=sum(q['marks'] for q in questions) if attempt is None else sum(q['marks'] for q in questions[:attempt])
    assert attempt is None or len(set(q['marks'] for q in questions))==1
    return dict(title=title,questions=questions,attempt=required,marks=marks,instructions=instructions or ('Answer all questions.' if attempt is None else f'Answer any {attempt} questions.'))

def build_papers(sid,bank,meta):
    result=[]
    for n in range(1,21):
        p=Picker(bank,n);sections=[];adaptation=''
        def get(m,**kwargs):return p.take(m,**kwargs)
        def grouped(label,weights,topic=None):return group(str(label),[get(m,topic=topic) for m in weights])
        def numeric_mcqs(count):
            # Each topic appears before a second question of that topic.
            pool=[mcq(q,n) for q in bank if q.get('shortAnswer') is not None and not q.get('challenge')];pool=[q for q in pool if q]
            rng(sid+'numerical-mcq',n).shuffle(pool);chosen=[];seen=set()
            for q in pool:
                if q['topic'] not in seen:chosen.append(q);seen.add(q['topic'])
                if len(chosen)==count:break
            for q in pool:
                if len(chosen)==count:break
                if q not in chosen:chosen.append(q)
            assert len(chosen)==count,(sid,len(chosen));return chosen
        if sid=='english1':
            comps=[q for q in bank if q['section'].startswith('Composition')];letters=[q for q in bank if q['section'].startswith('Letters')]
            comp=group('1',[], 'Write 300–350 words on ONE of the following.');comp.update(marks=20,choices=[copy.deepcopy(comps[(n-1+i*2)%10]) for i in range(5)])
            # Alternate starts avoid a five-paper-only composition rotation.
            lett=group('2',[],'Write ONE of the following letters.');lett.update(marks=10,choices=[copy.deepcopy(letters[(n-1)%5]),copy.deepcopy(letters[5+(n+1)%5])])
            notice=next(q for q in bank if q.get('event')==(n-1)%10 and q['section'].startswith('Notices'))
            email=next(q for q in bank if q.get('event')==(n-1)%10 and q['section'].startswith('Emails'))
            read=copy.deepcopy(next(q for q in bank if q['id']==f'english1-reading-{(n-1)%10+1:02}'));read['label']='4'
            grammar=[]
            for kind,num,mark in [('verb',8,.5),('preposition',8,.5),('join',4,1),('transform',8,1)]:
                if kind=='verb':grammar.append({**verb_passage(n),'label':'(a)'});continue
                parts=[get(mark,where=lambda q,k=kind:q.get('paperKind')==k and (k!='join' or q.get('paperJoin',True))) for _ in range(num)]
                grammar.append(group({'verb':'(a)','preposition':'(b)','join':'(c)','transform':'(d)'}[kind],parts,{'verb':'Supply the correct verb forms.','preposition':'Fill each blank with an appropriate preposition.','join':'Join each pair without using and, but or so.','transform':'Rewrite as directed without changing the meaning.'}[kind]))
            sections=[section('English Language — 80 marks',[comp,lett,group('3',[notice,email]),read,group('5',grammar)])]
            adaptation='Original reading passages and verbal situational composition choices; no picture-composition item.'
        elif sid=='english2':
            sections=[section('Section A — compulsory',[group('1',make_mcqs(sid,n,16),'Choose the correct answers.')])]
            sets=[('Section B — Drama',['Julius Caesar Act III','Julius Caesar Act IV','Julius Caesar Act V']),('Section C — Prose',['With the Photographer','The Elevator','The Girl Who Can','The Pedestrian','The Last Lesson']),('Section D — Poetry',['Haunted Houses','The Glove and the Lions','When Great Trees Fall','A Considerable Speck','The Power of Music'])]
            label=2
            for title,texts in sets:
                qs=[]
                for offset in [0,1]:
                    text=texts[(n-1+offset*2)%len(texts)];available=[q for q in bank if q['topic']==text];rng(text,n).shuffle(available)
                    threes=[q for q in available if q['marks']==3][:4];four=next(q for q in available if q['marks']==4)
                    qs.append(group(str(label),copy.deepcopy(threes+[four]),text+'\nContext summary: '+available[0]['context']));label+=1
                sections.append(section(title,qs,1,'Answer at least ONE question from this section. Across Sections B–D, answer FOUR questions in total. Each is 16 marks.'))
            # Three required sections plus one extra, rather than a misleading sum of offered marks.
            adaptation='Close-reading mocks use original context summaries instead of reproducing copyrighted Treasure Chest extracts. Use the prescribed texts while checking literary evidence.'
        elif sid in ('maths','phy','chem','bio'):
            if sid=='bio':mcqs=make_mcqs('bio',n,15)
            elif sid in ('phy','chem'):
                mcqs=numeric_mcqs(7)+make_mcqs(sid,n,8);rng(sid+'mixed-mcqs',n).shuffle(mcqs)
            else:mcqs=numeric_mcqs(15)
            for q in mcqs:p.used.add(q['id'])
            if sid=='maths':
                compulsory=[group('1',mcqs,'Choose the correct answers.'),grouped(2,[4,4,4]),group('3',[get(4),get(4),get(5,where=lambda q:q['marks']>=4)])]
                options=[grouped(i,[3,3,4]) for i in range(4,11)]
            elif sid=='phy':
                shorts=short_questions('phy',n,11)
                compulsory=[group('1',mcqs,'Choose the correct answers.'),group('2',shorts[:5],'Answer all subparts.'),group('3',shorts[5:]+[get(3)],'Answer all subparts.')]
                options=[grouped(i,[3,3,4]) for i in range(4,10)]
            else:
                compulsory=[group('1',mcqs,'Choose the correct answers.'),grouped(2,[5]*5)]
                options=[grouped(i,[3,3,4]) for i in range(3,9)]
            if sid=='bio':
                options=bio_papers.long_choices(n)
            sections=[section('Section A — 40 marks; compulsory',compulsory),section('Section B — 40 marks; choice',options,4)]
            adaptation='Original text/data-based mock. Drawing and diagram-interpretation tasks are replaced with verbal or numerical applications; this does not practise the board’s diagram skills.'
        elif sid=='histciv':
            sections=[section('Part I — compulsory; 30 marks',[group('1',make_mcqs(sid,n,16),'Choose the correct answers.'),group('2',short_questions('histciv',n,7),'Answer all subparts.')]),
              section('Part II A — Civics; 20 marks',[grouped(i,[3,3,4],t) for i,t in zip(range(3,6),['Parliament','Executive','Judiciary'])],2),
              section('Part II B — History; 30 marks',[grouped(i,[3,3,4],t) for i,t in zip(range(6,11),['1857','Nationalism' if n%2 else 'Gandhian movements','Independence and Partition','Wars and dictatorships','UN and NAM'])],3)]
        elif sid=='geo':
            topo=copy.deepcopy(next(q for q in bank if q['id']==f'geo-topo-{n:02}'));topo['label']='1'
            india=copy.deepcopy(next(q for q in bank if q['id']==f'geo-india-map-{n:02}'));india['label']='2'
            sections=[section('Part I — compulsory; 30 marks',[topo,india,group('3',make_mcqs(sid,n,10),'Choose the correct answers.')]),
              section('Part II — theory; 50 marks',[grouped(i,[2,2,3,3],t) for i,t in zip(range(4,13),['Climate','Soils','Natural vegetation','Water resources','Minerals and energy','Agriculture','Manufacturing','Transport','Waste management'])],5)]
            adaptation='Use the supplied Survey of India sheet and India outline. A resized preview is for viewing; use the full PDF or a correctly scaled print for ruler measurements. India answer overlays are schematic study guides.'
        elif sid=='computer':
            if n==1:
                ms=[dict(prompt=t,options=opts,correct='ABCD'.index(key),answer=key+'. '+ans,marks=1) for t,opts,key,ans in MCQ]
                shorts=[dict(prompt=t,answer=ans+'\n'+rubric,marks=2) for t,hint,ans,rubric in SHORT]
                progs=[next(q for q in bank if q['id']==f'computer-program-{i+1:02}-1') for i in [0,4,3,6,7,1]]
            else:
                concepts=[dict(prompt=t,options=opts,correct='ABCD'.index(key),answer=key+'. '+ans,marks=1) for t,opts,key,ans in MCQ]
                rng('computer-concepts',n).shuffle(concepts)
                ms=numeric_mcqs(10)+concepts[:10];rng('computer-mixed',n).shuffle(ms)
                shorts=[get(2,where=lambda q:q.get('category')=='short') for _ in range(10)]
                indices=[0,1,2+(n-2)%3,5+(n-2)%5,10+(n-2)%5,15+(n-2)%5]
                progs=[next(q for q in bank if q['id']==f'computer-program-{i+1:02}-{(n-1)%5+1}') for i in indices]
            sections=[section('Section A — compulsory; 40 marks',[group('1',ms,'Choose the correct answers.'),group('2',shorts,'Answer all subparts.')]),section('Section B — programming; 60 marks',[{**copy.deepcopy(q),'label':str(i+3)} for i,q in enumerate(progs)],4,'Answer any FOUR programs. Write complete Java classes. Use meaningful variable names and explain the algorithm; library sorting/searching is not a substitute where an algorithm is specified.')]
        elif sid=='hindi':
            composition=[q for q in bank if q.get('category')=='writing' and q['marks']==15];letters=[q for q in bank if q.get('category')=='writing' and q['marks']==7]
            qs=[]
            for label,ls,m,count in [('1',composition,15,5),('2',letters,7,2)]:
                choices=[copy.deepcopy(ls[(n*3+i*7)%len(ls)]) for i in range(count)];qs.append(dict(label=label,prompt='किसी एक विषय पर लिखिए।',marks=m,choices=choices))
            read=get(10,where=lambda q:q.get('category')=='reading');read['label']='3';qs.append(read)
            qs.append(group('4',[get(1,where=lambda q:q.get('category')=='grammar' and q['marks']==1) for _ in range(8)],'निर्देशानुसार उत्तर दीजिए।'))
            literature=[q for q in bank if q.get('category')=='literature'];lit=[]
            for book in ['साहित्य सागर','नया रास्ता','एकांकी संचय']:
                candidates=[q for q in literature if q['book']==book];rng(book,n).shuffle(candidates)
                if book=='साहित्य सागर':
                    poems={'सूर के पद','विनय के पद','भिक्षुक','चलना हमारा काम है','मातृ मंदिर की ओर'}
                    candidates=[q for q in candidates if q['topic'] not in poems][:3]+[q for q in candidates if q['topic'] in poems][:3]
                for q in candidates[:(6 if book=='साहित्य सागर' else 3)]:lit.append({**copy.deepcopy(q),'label':str(5+len(lit))})
            sections=[section('खंड अ — अनिवार्य; 40 अंक',qs),section('खंड ब — साहित्य; 40 अंक',lit,4,'अपने विद्यालय की दो निर्धारित पुस्तकों से चार प्रश्न कीजिए। प्रत्येक पुस्तक से कम-से-कम एक उत्तर अनिवार्य है।')]
            adaptation='मौलिक अभ्यास-प्रश्न; साहित्य में प्रसंग-आधारित प्रश्न हैं, पाठ से गढ़े हुए उद्धरण नहीं। चित्र-रचना के स्थान पर शब्दों में दी गई परिस्थिति है।'
        else:raise ValueError(sid)
        extra_choice=16 if sid=='english2' else 0
        attempted=sum(s['marks'] for s in sections)+extra_choice
        assert attempted==meta['marks'],(sid,n,attempted)
        instructions=['Spend 15 minutes reading before starting the writing time.','Follow the choices printed in each section. Marks in brackets are the intended marks for this original practice paper.']
        if sid=='english2':instructions+=['Answer all of Section A. Answer FOUR questions from Sections B–D: at least one Drama, one Prose and one Poetry, plus one additional question from any of these sections.']
        result.append(dict(id=f'{sid}-paper-{n:02}',number=n,title=f'{meta["name"]} — Paper {n:02}',marks=attempted,time=meta['time'],sections=sections,additionalChoiceMarks=extra_choice,adaptation=adaptation,instructions=instructions,**({'sourcePdf':'assets/ICSE_2027_Computer_Applications_100_Mark_Mock.pdf'} if sid=='computer' and n==1 else {})))
    return result
