import hashlib, math, random
from fractions import Fraction

def rng(family, variant):
    return random.Random(int(hashlib.sha256(f'{family}:{variant}'.encode()).hexdigest()[:16],16))

def num(x, digits=3):
    if isinstance(x,Fraction):
        return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
    if isinstance(x,float):
        if math.isclose(x,round(x),abs_tol=1e-9): return str(round(x))
        return f'{x:.{digits}f}'.rstrip('0').rstrip('.')
    return str(x)

def item(topic,prompt,answer,marks=3,**extra):
    return dict(topic=topic,prompt=prompt,answer=answer,marks=marks,difficulty='Standard',**extra)

def variant_bank(subject, families, challenge_families, standard=2000, challenge=100):
    result=[]; seen=set(); counts={}
    for section,fs,total in [('Chapter practice',families,standard),('100 twist problems',challenge_families,challenge)]:
        active=list(fs); i=0; added=0
        while added<total:
            if not active: raise ValueError(f'Insufficient distinct content: {subject}/{section}')
            family,fn=active[i%len(active)]; v=i//len(active)
            i+=1
            for attempt in range(150):
                q=fn(v+attempt*97)
                key=' '.join(q['prompt'].split()).casefold()
                if key not in seen: break
            else:
                active=[(name,f) for name,f in active if name!=family]
                continue
            seen.add(key)
            q.update(id=f'{subject}-{len(result)+1:04}',section=section,family=family,variant=v+1,
                     difficulty='Challenge' if section=='100 twist problems' else q.get('difficulty','Standard'))
            if section=='100 twist problems':
                q['challenge']=True
                q['marks']=max(4,q['marks'])
            result.append(q); counts[family]=counts.get(family,0)+1
            added+=1
    assert len(result)==standard+challenge
    return result

def mcq(q, seed=0):
    """Make a separate paper-only MCQ; never insert MCQs in quantitative banks."""
    if q.get('options'):
        return {**q,'marks':1}
    value=q.get('shortAnswer')
    distractors=q.get('distractors')
    if value is None or not distractors: return None
    options=list(dict.fromkeys([str(value)]+[str(x) for x in distractors]))[:4]
    if len(options)!=4: return None
    rng(q.get('id',q['topic']),seed).shuffle(options)
    return {**q,'prompt':q.get('mcqPrompt',q['prompt']), 'options':options,
            'correct':options.index(str(value)),'marks':1,
            'answer':f'{"ABCD"[options.index(str(value))]}. {value}\n{q["answer"]}'}

def numeric_mcq(q,value,unit='',prompt=None):
    q['shortAnswer']=f'{num(value)}{unit}'
    scale=max(1,abs(value)*0.15)
    q['distractors']=[f'{num(value+scale)}{unit}',f'{num(value-scale)}{unit}',f'{num(value+2*scale)}{unit}']
    if prompt: q['mcqPrompt']=prompt
    return q
