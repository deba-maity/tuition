"""Syllabus-scoped multi-step examination problems, with fully worked solutions.

These replace the previous 'find the flaw in a classmate's reasoning' padding.
Science give-reason tasks remain where the specimen actually uses that skill.
"""
from fractions import Fraction as F
from math import sqrt
from .common import item, rng, num as N

def maths(v):
    k=v%10;r=rng('new-maths-challenge',v)
    if k==0:
        price=r.randrange(30,130)*100;d=r.choice([10,15,20,25]);tax=r.choice([5,12,18]);net=price*(100-d)/100;paid=net*(100+tax)/100
        q=f'An article is marked ₹{price}. After a discount, an intra-state customer pays ₹{N(paid)}, including {tax}% GST. Find (i) the taxable value, (ii) the discount percentage and (iii) CGST and SGST.'
        a=f'1. Let the taxable value be x. GST-inclusive amount=x(1+{tax}/100).\n2. x={N(paid)}×100/{100+tax}=₹{N(net)}.\n3. Discount={price}−{N(net)}=₹{N(price-net)}. Discount percentage=({N(price-net)}/{price})×100={d}%.\n4. Total GST={N(net)}×{tax}/100=₹{N(paid-net)}.\n5. For an intra-state sale, CGST=SGST=half the total GST=₹{N((paid-net)/2)} each.';t='GST: recover discount and split tax'
    elif k==1:
        P=r.randrange(8,31)*100;n=r.choice([12,18,24,30]);rate=r.choice([5,6,7,8]);I=P*n*(n+1)*rate/2400;M=P*n+I
        q=f'A recurring deposit pays maturity value ₹{N(M)} after {n} monthly instalments, at {rate}% p.a. Find the monthly instalment and total interest using the ICSE recurring-deposit convention.'
        a=f'1. Let each monthly instalment be ₹P. Principal deposited={n}P.\n2. Interest=P×{n}×{n+1}×{rate}/2400={N(n*(n+1)*rate/2400)}P.\n3. Maturity=principal+interest: {N(M)}=({n}+{N(n*(n+1)*rate/2400)})P.\n4. P={N(M)}/{N(n+n*(n+1)*rate/2400)}=₹{P}.\n5. Total interest={N(M)}−{n}×{P}=₹{N(I)}.';t='Recurring deposit: reverse maturity'
    elif k==2:
        b=r.randint(8,23);delta=r.randint(3,11);area=b*(b+delta)
        q=f'The length of a rectangle exceeds its breadth by {delta} cm and its area is {area} cm². Form and solve a quadratic equation. Hence find its perimeter.'
        a=f'1. Let breadth=x cm, so length=(x+{delta}) cm.\n2. x(x+{delta})={area}, giving x²+{delta}x−{area}=0.\n3. Factorise: (x−{b})(x+{b+delta})=0.\n4. x={b} or x=−{b+delta}. A length is positive, so breadth={b} cm and length={b+delta} cm.\n5. Perimeter=2({b}+{b+delta})={4*b+2*delta} cm.';t='Quadratic equations: dimensions from area'
    elif k==3:
        m=r.randint(2,6);n=m+r.randint(1,5);scale=r.randint(4,15);diff=scale*(n*n-m*m)
        q=f'Two similar triangles have corresponding sides in the ratio {m}:{n}. Their areas differ by {diff} cm². Find both areas. If the smaller perimeter is {3*m*scale} cm, find the larger perimeter.'
        a=f'1. Similar triangles have area ratio {m*m}:{n*n}, the square of the side ratio.\n2. Write their areas as {m*m}k and {n*n}k. Then ({n*n}−{m*m})k={diff}, so k={scale}.\n3. Smaller area={m*m}×{scale}={m*m*scale} cm²; larger area={n*n}×{scale}={n*n*scale} cm².\n4. Perimeters are in the side ratio {m}:{n}. Larger perimeter={3*m*scale}×{n}/{m}={3*n*scale} cm.';t='Similarity: area difference and perimeter'
    elif k==4:
        b=r.randint(2,9);mult=r.randint(2,5);tan=b*mult;whole=b*mult*mult
        q=f'From external point P, tangent PA to a circle is {tan} cm. A secant meets the circle first at B and then C, with PB={b} cm. Calculate PC and BC.'
        a=f'1. By the tangent–secant theorem, PA²=PB×PC.\n2. {tan}²={b}×PC, so PC={tan*tan}/{b}={whole} cm. PC is the whole secant from P.\n3. BC=PC−PB={whole}−{b}={whole-b} cm.\nCheck: {b}×{whole}={tan*tan}=PA².';t='Circles: tangent and complete secant'
    elif k==5:
        xs=[r.randint(2,6)*5,r.randint(7,10)*5,r.randint(11,15)*5];f1=r.randint(2,7);f3=r.randint(8,15);unknown=r.randint(3,12);mean=F(f1*xs[0]+unknown*xs[1]+f3*xs[2],f1+unknown+f3)
        if mean==xs[1]:return maths(v+10)
        q=f'The values {xs[0]}, {xs[1]}, {xs[2]} have frequencies {f1}, k, {f3}, respectively. Their mean is {N(mean)}. Find k and the total frequency.'
        c=f1*xs[0]+f3*xs[2];f=f1+f3
        a=f'1. Mean=Σfx/Σf=({c}+{xs[1]}k)/({f}+k).\n2. Put this equal to {N(mean)} and cross-multiply: {N(mean)}({f}+k)={c}+{xs[1]}k.\n3. Collect k terms: ({N(mean)}−{xs[1]})k={c}−{N(mean)}×{f}.\n4. k={unknown}; total frequency={f1}+{unknown}+{f3}={f+unknown}.\n5. Substitution gives ({c}+{xs[1]}×{unknown})/({f}+{unknown})={N(mean)}, confirming the stated mean.';t='Statistics: missing frequency'
    elif k==6:
        x=r.randint(-8,5);y=r.randint(-5,8);dx=r.randint(2,6);dy=r.randint(2,6);m=r.randint(1,4);n=r.randint(2,5);xx=F(n*x+m*(x+dx),m+n);yy=F(n*y+m*(y+dy),m+n)
        q=f'P divides A({x},{y}) and B({x+dx},{y+dy}) internally in the ratio AP:PB={m}:{n}. Find P and the equation of the line through P perpendicular to AB.'
        slope=F(dy,dx);perp=-1/slope
        a=f'1. Section formula: P=((nx₁+mx₂)/(m+n),(ny₁+my₂)/(m+n)).\n2. xP=({n}×{x}+{m}×{x+dx})/{m+n}={N(xx)}; yP=({n}×{y}+{m}×{y+dy})/{m+n}={N(yy)}.\n3. Slope AB=({y+dy}−({y}))/({x+dx}−({x}))={N(slope)}.\n4. Perpendicular slope=−1/({N(slope)})={N(perp)}.\n5. Required line: y−({N(yy)})=({N(perp)})(x−({N(xx)})). This point-slope form is a complete equation.';t='Coordinate geometry: section point and perpendicular'
    elif k==7:
        red=r.randint(4,12);blue=r.randint(3,10);green=r.randint(2,9);total=red+blue+green;prob=F(red,total)
        q=f'A bag contains {red} red balls, {blue} blue balls and k green balls. Every ball is equally likely to be selected. On a single draw, P(red)={N(prob)}. Find k and P(not blue).'
        a=f'1. Total balls={red+blue}+k. Thus {red}/({red+blue}+k)={N(prob)}.\n2. Cross-multiply and solve: total={total}; k={total}−{red}−{blue}={green}.\n3. Not blue means red or green, so favourable balls={red}+{green}={red+green}.\n4. P(not blue)={red+green}/{total}={N(F(red+green,total))}.';t='Probability: recover bag composition'
    elif k==8:
        small=r.randint(2,6);factor=r.choice([2,3,4]);R=small*factor;h=small*factor;count=2*factor**2
        q=f'A solid hemisphere of radius {R} cm is melted and recast into identical solid cones of radius {small} cm and height {h} cm, with no metal loss. Find the number of cones and the curved surface area of one cone. Leave the area in terms of π.'
        l=sqrt(small*small+h*h)
        a=f'1. Hemisphere volume=(2/3)πR³=(2/3)π×{R}³.\n2. One cone volume=(1/3)πr²h=(1/3)π×{small}²×{h}.\n3. Number=hemisphere volume/cone volume=2×{R}³/({small}²×{h})={count}.\n4. Slant height l=√(r²+h²)=√({small*small+h*h})={small}√{1+factor*factor} cm.\n5. Curved surface area=πrl={small*small}π√{1+factor*factor} cm² (approximately {N(small*l)}π cm²).';t='Mensuration: recasting and slant height'
    else:
        d=r.randint(10,50)*2;eye=r.choice([1.5,1.6,1.8]);height=d*sqrt(3)/2+eye
        q=f'An observer’s eye is {eye} m above level ground. The elevation of a tower top is 30°. After moving {d} m directly towards its base, the elevation is 60°. Find the tower’s height, correct to two decimal places.'
        a=f'1. Let the nearer horizontal distance be x m and height above eye level be H m.\n2. From the nearer position, tan60°=H/x, so H=x√3.\n3. From the farther position, tan30°=H/(x+{d}), so H=(x+{d})/√3.\n4. Equate: 3x=x+{d}; x={d/2:g} m. H={d/2:g}√3 m.\n5. Tower height=H+eye height={d/2:g}√3+{eye}={height:.2f} m.';t='Heights: two observations and eye level'
    return item(t,q,a,4)

def rebuild_challenges(sid,bank):
    if sid=='maths':
        new=[maths(v) for v in range(100)]
    else:
        # Keep the numerical/experimental core of each verified in-scope family;
        # remove appended debates about imaginary pupils and model philosophy.
        cuts=[' If actual small-sample',' A student claims',' Predict whether a boiled',' Explain why a positive iodine',' A student calls',' Explain how DNA can',' Could this town',' If the background',' Give one artery',' The brighter lamp',' A pupil divides',' A student says',' Distinguish ionisation',' Another sample',' State why percentage',' A dry litmus',' Explain why using',' Both the original',' Explain why adding',' A classmate says',' A student rejects',' Explain why doubling',' A student divides',' Now a downward',' A pupil concludes',' Explain why putting',' Would a real vessel']
        new=[]
        for old in bank[-100:]:
            q=dict(old)
            for cut in cuts:
                if cut in q['prompt']:q['prompt']=q['prompt'].split(cut)[0]
            q['family']=q['family'].replace('Twist:','Exam application:')
            # Questions retain scientific give-reason parts which occur in the specimen.
            new.append(q)
    for i,q in enumerate(new):
        q.update(id=f'{sid}-{2001+i:04}',section='100 exam challenge questions',challenge=True,difficulty='Challenge',family=q.get('family',q['topic']))
    return bank[:-100]+new

def repair_duplicates(sid,bank):
    """Replace collisions with fresh substantive values, never serial-number padding."""
    import importlib
    module=importlib.import_module('question_builders.'+{'phy':'physics','chem':'chemistry','bio':'biology','maths':'maths'}[sid])
    source_rng=module.rng
    try:
        module.rng=lambda family,v:source_rng(family,v+30000)
        alternatives=module.make_bank()[:2000]
    finally:module.rng=source_rng
    used=set()
    for q in bank:
        key=' '.join(q['prompt'].split())
        if key in used:
            candidates=[x for x in alternatives if x['topic']==q['topic'] and ' '.join(x['prompt'].split()) not in used]
            if sid=='maths' and q.get('challenge'):
                candidates=[maths(20000+10*j+(int(q['id'].split('-')[-1])%10)) for j in range(100)]
                candidates=[x for x in candidates if ' '.join(x['prompt'].split()) not in used]
            if not candidates:raise ValueError('No legitimate replacement for '+q['id'])
            chosen=candidates[0];q.update(prompt=chosen['prompt'],answer=chosen['answer'],topic=chosen['topic'],family=chosen.get('family',chosen['topic']))
            for key in ['shortAnswer','distractors','mcqPrompt']:
                q.pop(key,None)
                if key in chosen:q[key]=chosen[key]
            key=' '.join(q['prompt'].split())
        used.add(key)
    return bank
