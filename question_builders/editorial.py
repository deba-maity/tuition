"""Remove weak mathematical diversions and meaningless quantitative padding."""
import re
from fractions import Fraction as F
from .common import item, num as N
from .challenge_bank import maths as challenge_math

def revise(sid,bank):
    for i,q in enumerate(bank):
        if sid=='english2' and q['id']=='english2-072':
            q['answer']='The quiet movement of former inhabitants through familiar rooms makes the past part of ordinary domestic life. These presences do not attack the living; they suggest that a place retains the lives once lived there. The image of unseen guests extends the same idea into a social gathering: visible people are not its only company, because memory and earlier lives also occupy the space. Both images make past and present coexist. The calm, reflective tone turns haunting into continuity rather than a conventional supernatural threat.'
        if sid=='english2' and q['id']=='english2-103':
            q['answer']='The lively rhythm carries the performance forward with a force out of proportion to its musical worth. Repeated distress among listeners makes the song sound relentless rather than pleasurable. Their appeals to stop contrast with the singer’s persistence, so each continuing disturbance increases the comic tension. The goat’s abrupt physical intervention supplies a decisive change: action silences a voice that ordinary requests could not restrain. Sound, narrative pace and the sudden ending together expose the singer’s self-importance.'
        if sid=='english2' and q['id']=='english2-083':
            q['answer']='The death changes the survivors’ experience of their surroundings: even breathing and seeing become strained, conveying how thoroughly grief disturbs ordinary perception. Memory then becomes painfully sharp, dwelling on kind words left unsaid and shared experiences that will never occur. This combines a diminished present with a heightened awareness of missed possibilities. The loss is therefore intellectual and emotional as well as physical; the person who once helped give the world meaning is absent.'
        if sid=='phy' and q['topic']=='Work, energy and power' and ('raises' in q['prompt'] or 'gravitational' in q['prompt']) and 'g=' not in q['prompt'] and 'g =' not in q['prompt']:
            q['prompt']+=' Take g=10 m/s².'
        if sid=='phy' and q.get('challenge') and 'A student claims that replacing series resistors' in q['prompt']:
            match=re.search(r'resistors (\d+) Ω and (\d+) Ω.*ideal (\d+) V',q['prompt'])
            if match:
                r1,r2,V=map(int,match.groups());series=r1+r2;parallel=F(r1*r2,series)
                q['prompt']=f'Two resistors of {r1} Ω and {r2} Ω are connected first in series and then in parallel across the same ideal {V} V battery. Calculate equivalent resistance and total current in both arrangements. Find the current through each parallel branch.'
                q['answer']=f'1. Series resistance={r1}+{r2}={series} Ω.\n2. Series current=V/R={V}/{series}={V/series:.3f} A.\n3. Parallel resistance=R₁R₂/(R₁+R₂)={r1*r2}/{series}={N(parallel)} Ω.\n4. Parallel total current={V}/({N(parallel)})={float(V/parallel):.3f} A.\n5. Branch currents: I₁={V}/{r1}={V/r1:.3f} A and I₂={V}/{r2}={V/r2:.3f} A. Their sum equals the total parallel current.'
        if sid=='phy' and q.get('challenge') and 'A pupil says both pitch' in q['prompt']:
            q['prompt']=q['prompt'].split(' A pupil says')[0]+' State the frequency in each medium, calculate both wavelengths and compare the pitch in the two media.'
        if sid=='maths' and 'Can k be determined uniquely?' in q['prompt']:
            replacement=challenge_math(10005+i*10)
            q.update(topic='Statistics',prompt=replacement['prompt'],answer=replacement['answer'],family='Missing frequency: solvable equation')
        if sid=='maths' and q.get('family')=='Recasting solids':
            match=re.search(r'radius (\d+) cm and height (\d+) cm.*spheres of radius (\d+) cm',q['prompt'])
            if match:
                R,h,r=map(int,match.groups());ratio=F(R*R*h,4*r**3);count=ratio.numerator//ratio.denominator;remaining=F(R*R*h,3)-count*F(4*r**3,3)
                q['prompt']=f'A solid cone of radius {R} cm and height {h} cm is melted into spheres of radius {r} cm. Find the maximum number of complete spheres and the volume of metal remaining, in terms of π.'
                q['answer']=f'1. Cone volume=(1/3)π×{R}²×{h}={N(F(R*R*h,3))}π cm³.\n2. One sphere volume=(4/3)π×{r}³={N(F(4*r**3,3))}π cm³.\n3. Volume ratio={N(ratio)}, so the maximum complete spheres={count}.\n4. Remaining volume=original volume−{count}×sphere volume={N(remaining)}π cm³.'
        if sid=='bio' and q.get('family') in ['Energy transfer with a supplied model','Biomagnification model']:
            count=(i+8)*4
            q.update(topic='Genetics',family='Monohybrid offspring and parent inference',prompt=f'A tall pea plant is crossed with a dwarf plant. Among {count} offspring, {count//2} are tall and {count//2} dwarf. T is dominant to t. Determine the tall parent’s genotype, show the cross and state the expected offspring if this tall parent were instead crossed with a pure tall plant.',answer=f'1. The dwarf parent is tt. Dwarf offspring must receive t from both parents, so the tall parent is Tt, not TT.\n2. First cross: Tt×tt. Gametes are T,t and t. Offspring: ½Tt (tall), ½tt (dwarf), matching {count//2} of each phenotype.\n3. Alternative cross: Tt×TT. Gametes are T,t and T. Offspring: ½TT and ½Tt.\n4. All offspring in the alternative cross are tall; the genotype ratio is 1:1 and the phenotype is 100% tall.')
        if sid=='bio':
            if 'seconds of a circulation-tracing' in q['prompt']:
                rate=60+i%31;stroke=60+(i//31)%26
                q['prompt']=re.sub(r'After \d+ seconds of a circulation-tracing simulation, a marker is reported at ',f'A heart beats {rate} times per minute with stroke volume {stroke} mL. A blood marker is at ',q['prompt'])+' Calculate cardiac output in L/min.'
                q['answer']+=f' Cardiac output=heart rate×stroke volume={rate}×{stroke}={rate*stroke} mL/min={rate*stroke/1000} L/min.'
        if sid=='english1' and q.get('paperKind')=='join' and any(s in q.get('family','') for s in ['so that','so ... that']):q['paperJoin']=False
    return bank
