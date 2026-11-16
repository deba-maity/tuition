"""Worked traces, full intermediate calculations and subject-specific method notes."""
import re, ast, math
from fractions import Fraction as F
from .common import num as N

METHODS={
'GST':('Find the price after discount before calculating tax. For an inclusive bill, divide by 1+GST/100.','CGST and SGST together equal the total GST; their percentages are each half of the total rate.'),
'Banking':('Let monthly deposit=P, number of months=n and annual rate=r. Interest=P×n(n+1)×r/2400; maturity=nP+interest.','An instalment deposited later earns interest for fewer months. Do not apply simple interest to the entire final deposit for the whole term.'),
'Shares and dividend':('Dividend per share=face value×dividend rate/100. Investment=number×market price. Yield=annual dividend/investment×100.','Use face value for dividend and market price for investment; these are different bases.'),
'Quadratic equations':('Write the equation in ax²+bx+c=0 form. Use factorisation or x=(−b±√(b²−4ac))/(2a), then test any domain restrictions.','Keep both algebraic roots until the physical restrictions or original denominator exclude one.'),
'Matrices':('For AB, multiply each row of A by each column of B. The entry (i,j) is the sum of the corresponding products.','Order matters: AB need not equal BA. For unknown entries, equate corresponding positions.'),
'Arithmetic progression':('Tn=a+(n−1)d; Sn=n[2a+(n−1)d]/2. Two known terms give two linear equations in a and d.','The term index contributes n−1 differences, not n.'),
'Geometric progression':('Find r by dividing consecutive terms. Tn=ar^(n−1); Sn=a(r^n−1)/(r−1), for r≠1.','Keep brackets around a negative common ratio when taking powers.'),
'Section formula':('If AP:PB=m:n, P=((nxA+mxB)/(m+n),(nyA+myB)/(m+n)).','The coefficient m multiplies endpoint B. Check that an internal point lies between the endpoints.'),
'Similarity':('Corresponding lengths and perimeters have the same ratio. Areas have the square of that ratio.','An area difference gives the difference of the squared-ratio multiples.'),
'Circles':('Select the property required by the stated geometry: supplementary cyclic opposite angles, radius perpendicular to tangent, or tangent²=external secant×whole secant.','Distinguish the external part of a secant from its complete length.'),
'Mensuration':('Write the appropriate volume or exposed-area formula first. For recasting, equate original and final volumes; for surface area exclude joined faces.','Volume uses cubic units, area uses square units. A radius is half a diameter.'),
'Statistics':('For a frequency distribution calculate Σf and Σfx separately, then mean=Σfx/Σf. For grouped data use class marks or the stated interpolation rule.','Do not take an unweighted average of values with unequal frequencies.'),
'Probability':('List the equally likely outcomes for the single experiment. Probability=favourable outcomes/total outcomes.','The final probability must lie between 0 and 1. Use a complement only for the event actually requested.'),
'Lenses':('Use the Cartesian sign convention: real object u<0, convex f>0 and concave f<0. Apply 1/v−1/u=1/f and magnification m=v/u.','Negative v indicates a virtual image on the object side; it is not automatically an error.'),
'Calorimetry':('Write heat lost=heat gained. Use Q=mcΔT for a temperature change and Q=mL for a change of state. Check whether all ice melts before solving for a final temperature above 0°C.','Use consistent mass and specific-heat units. Include the vessel’s heat capacity only when it is supplied.'),
'Electricity':('Identify series and parallel parts before calculating equivalent resistance. Use V=IR, P=VI=I²R=V²/R and energy=power×time.','Series components share current; parallel branches share potential difference. Convert watts to kilowatts for kWh.'),
'Work, energy and power':('Use work=force×distance in the force direction, GPE=mgh, KE=½mv² and power=energy/time. Efficiency=useful output/input.','Convert efficiency from percent to a fraction before dividing. The SI unit of power is watt.'),
'Mole concept':('n=m/M; gas volume at the stipulated STP=22.4n litres; particles=n×6.022×10²³. Use the balanced-equation ratio when a reaction is involved.','Distinguish atoms, molecules and ions. Equal moles do not imply equal masses.'),
'Chemical calculations':('Balance the equation, convert the known amount into moles, apply the coefficient ratio and convert the required moles into mass or gas volume.','For percentage purity, divide the mass of the pure reactant by the whole impure sample mass.'),
'Electrolysis':('Identify electrolyte and electrodes. At the cathode reduction consumes electrons; at the anode oxidation releases electrons. Write charge-balanced half-equations.','Copper anodes replenish Cu²⁺ in copper refining; inert anodes do not supply replacement copper ions.'),
'Genetics':('Write the parental genotypes, list gametes and combine one allele from each parent. Count genotype and phenotype classes separately.','A predicted ratio describes probabilities; it is not a guaranteed exact count in a small family.'),
'Cell division':('Identify the stage from the chromosome behaviour. Count chromosomes by centromeres; after DNA replication a metaphase chromosome has two chromatids.','Mitosis preserves chromosome number. Do not confuse DNA amount, chromatids and chromosomes.'),
'Topographical interpretation':('Read eastings before northings. A six-figure reference appends tenths within the square to each coordinate. At RF 1:n, ground distance=map distance×n in the same units.','At 1:50,000, 2 cm represents 1 km. A digital image must be printed at the stated size before a ruler measurement is valid.'),
}

def computer_trace(q):
    k=int(q['family']);idx=int(q['id'].rsplit('-',1)[1])-1;n=idx//20;a=7+3*n;b=n+2 if k==19 else 2+n%8
    old=q['answer'];steps=[];table=None
    if k==0:
        steps=[f'Initial values: a={a}, b={b}.',f'a++ supplies {a} to the expression, then a becomes {a+1}.',f'--b changes b to {b-1} first and supplies {b-1}.',f'Multiply before adding: c=({a}×2)+{b-1}={2*a}+{b-1}={2*a+b-1}.',f'Final values: c={2*a+b-1}, a={a+1}, b={b-1}.']
    elif k==1:steps=[f'Both operands are int values, so / performs integer division: {a}/{b}={a//b}.',f'The remainder is {a}%{b}={a%b}, since {a}={b}×{a//b}+{a%b}.',f'Add the two results: {a//b}+{a%b}={a//b+a%b}.']
    elif k==2:
        word,lo,hi=re.search(r'"([A-Z]+)"\.substring\((\d+),(\d+)\)',q['prompt']).groups();lo=int(lo);hi=int(hi)
        steps=[f'Java indexes the first character at 0. The start index {lo} is included; the end index {hi} is excluded.',f'Selected indices: '+', '.join(str(i) for i in range(lo,hi))+'.',f'Their characters form "{word[lo:hi]}". Length=end−start={hi}−{lo}={hi-lo}.']
        table={'headers':['Index','Character','Selected'],'rows':[[i,c,'yes' if lo<=i<hi else ''] for i,c in enumerate(word)]}
    elif k==3:
        total=a;rows=[]
        for i in range(1,b+1):rows.append([i,total,i,total+i]);total+=i
        table={'headers':['i','s before','Added','s after'],'rows':rows};steps=[f'Initial s={a}. The loop uses i=1 through {b}, inclusive.',f'It executes {b} times. Sum added=1+…+{b}={b*(b+1)//2}.',f'Final s={a}+{b*(b+1)//2}={total}.']
    elif k==4:steps=[f'The parentheses are evaluated numerically: ({a}+{b})={a+b}.',f'The first operand "{a}" is a String. The following + operators therefore concatenate left to right.',f'"{a}"+{b} becomes "{a}{b}"; appending {a+b} gives "{a}{b}{a+b}".']
    elif k==5:steps=[f'The array has {a} rows and {b} columns, hence {a*b} int elements.',f'Every int array element is initially 0, so m[0][0]=0.',f'Each int value uses 4 bytes. Element-value storage={a}×{b}×4={a*b*4} bytes; object and row-array overhead is excluded as requested.']
    elif k==6:
        exponent=(b//2)//2;steps=[f'The exponent expression contains int division: {b//2}/2={exponent}.',f'Math.pow receives {a} and {exponent}; result={float(a**exponent)}.', 'Math.pow returns double even when its numerical value is a whole number.']
    elif k==7:steps=[f'The cast (char){65+n%26} yields the character {chr(65+n%26)}.',f'The separate parenthesised integer addition is {65+n%26}+{b}={65+n%26+b}.','The intervening String " " makes the final + operations concatenations. Output: '+chr(65+n%26)+' '+str(65+n%26+b)+'.']
    elif k==8:steps=['toLowerCase() returns a new String value; it does not mutate s.','Because that result is not assigned to s, s still contains the uppercase original.','charAt uses the supplied zero-based index. '+old]
    elif k==9:
        x=a;rows=[]
        while True:
            before=x;x-=b;rows.append([len(rows)+1,before,x,x>0])
            if x<=0:break
        table={'headers':['Execution','x before','x after subtraction','x > 0'],'rows':rows};steps=['A do-while loop executes the body before testing its condition.',f'Subtract {b} repeatedly until x≤0. The last subtraction is not undone.',f'Final x={x}; body executions={len(rows)}.']
    elif k==10:steps=[f'The first multiple is {b}. Initialise i={b}.',f'The last multiple {a*b} is included, so use i<={a*b}.',f'Increase by the common step {b} each time.\n'+old,f'The body prints {a} multiples.']
    elif k==11:steps=['Integer.parseInt converts a valid decimal String to int; assigning the String directly to int would be a type error.',old,'Math.sqrt returns double, so store the square root in a double variable.']
    elif k==12:
        steps=['Start with low=0 and high=4.',f'mid=(0+4)/2=2, a[mid]={a+2*b}, key={a+3*b}. Since key>a[mid], set low=3.',f'mid=(3+4)/2=3. a[3]={a+3*b}, so the search succeeds at index 3.','The visited mid indices are 2 and 3.']
    elif k==13:
        values=[a+b,a,a+2*b,a-b];rows=[]
        for j in range(3):
            pair=f'{values[j]} and {values[j+1]}';swap=values[j]>values[j+1]
            if swap:values[j],values[j+1]=values[j+1],values[j]
            rows.append([j,pair,'swap' if swap else 'keep',str(values[:])])
        table={'headers':['j','Compared','Action','Array after comparison'],'rows':rows};steps=['An ascending bubble pass compares adjacent pairs left to right and swaps when the left value is larger.',f'After 3 comparisons the array is {values}.','This is one pass, not the complete sort.']
    elif k==14:steps=[f'Return type first: boolean. Method name: check{n+1}. Parameter types: int and char.',f'Header: boolean check{n+1}(int number, char code)', 'Overloading requires a different parameter list (number, order or types). Changing only the return type does not produce a valid overload.']
    elif k==15:steps=[f'Valid data indices are 0 through {a-1}; therefore the traversal must test i<data.length.',f'Integer.parseInt requires a String, so use "{b}" rather than the int literal {b}.','Correct loop:\n'+old.split('\n')[0]]
    elif k==16:
        word,ch=re.search(r'"([A-Z]+)"\.indexOf\(\'([A-Z])\'\)',q['prompt']).groups();indices=[i for i,c in enumerate(word) if c==ch]
        steps=[f'Number the characters of {word} from zero.',f'Occurrences of {ch} are at indices '+', '.join(map(str,indices))+'.',f'indexOf returns the first occurrence, {indices[0]}; lastIndexOf returns the last, {indices[-1]}.']
    elif k==17:steps=['A new object’s int field is default-initialised to 0.','The constructor parameter amount shadows the field. In amount=amount both names refer to that parameter, leaving the field unchanged.','Use this.amount=amount; this.amount refers to the field, while the right-hand amount is the argument. '+f'For the given call the corrected field becomes {a}.']
    elif k==18:steps=[f'Test age<{b+8}. If true, choose 0; otherwise choose {a*10}.',old,'The conditional operator is condition ? valueIfTrue : valueIfFalse. Both selected values here are int.']
    else:steps=[f'For i=1 the inner loop has {b} iterations; for i=2 it has {b-1}; for i={b} it has one.',f'Total=1+2+…+{b}={b}({b}+1)/2={b*(b+1)//2}.',f'count starts at zero and increases once per inner execution, so final count={b*(b+1)//2}.']
    q['answer']='\n\n'.join(f'{i+1}. {s}' for i,s in enumerate(steps));q['solutionSteps']=steps
    if table:q['solutionTable']=table

def expand_maths(q):
    p=q['prompt'];family=q.get('family','')
    if family in ['Matrix product','Matrix noncommutativity']:
        matrices=re.findall(r'\[\[-?\d+,-?\d+\],\[-?\d+,-?\d+\]\]',p)
        if len(matrices)==2:
            A,B=map(ast.literal_eval,matrices);steps=[]
            for name,X,Y in [('AB',A,B)]+([('BA',B,A)] if family=='Matrix noncommutativity' else []):
                vals=[]
                for i in range(2):
                    vals.append([])
                    for j in range(2):
                        value=X[i][0]*Y[0][j]+X[i][1]*Y[1][j];vals[-1].append(value)
                        steps.append(f'{name}[{i+1},{j+1}]={X[i][0]}×({Y[0][j]})+({X[i][1]})×({Y[1][j]})={value}.')
                steps.append(f'{name}={vals}.')
            if family=='Matrix noncommutativity':steps.append(q['answer'].split('. ')[-1])
            q['answer']='\n'.join(steps)
    elif family=='AP recover a and d':
        match=re.search(r'The (\d+)th and (\d+)th terms of an AP are (-?\d+) and (-?\d+).*first (\d+) terms',p)
        if match:
            k,m,tk,tm,n=map(int,match.groups());d=F(tm-tk,m-k);a=tk-(k-1)*d;total=F(n,2)*(2*a+(n-1)*d)
            q['answer']=f'1. The two term equations are a+{k-1}d={tk} and a+{m-1}d={tm}.\n2. Subtract: {m-k}d={tm-tk}, so d={N(d)}.\n3. Substitute: a={tk}−{k-1}×({N(d)})={N(a)}.\n4. S{n}={n}/2[2({N(a)})+{n-1}({N(d)})]={N(total)}.'
    elif family=='Weighted mean':
        lists=re.findall(r'\[[\d, ]+\]',p)
        if len(lists)==2:
            xs,fs=map(ast.literal_eval,lists);total=sum(fs);fx=sum(x*f for x,f in zip(xs,fs));q['solutionTable']={'headers':['x','f','fx'],'rows':[[x,f,x*f] for x,f in zip(xs,fs)]+[['Total',total,fx]]}
            q['answer']=f'1. Multiply each value by its frequency, as shown in the table.\n2. Σf={total}; Σfx={fx}.\n3. Mean=Σfx/Σf={fx}/{total}={fx/total:.2f}. Frequencies weight the observations; averaging the four listed values directly would be incorrect.'

def enrich(sid,bank):
    for q in bank:
        if sid=='computer' and q.get('category')=='short':computer_trace(q)
        if sid=='maths':expand_maths(q)
        if sid=='bio' and q['topic']=='Genetics':
            cross=re.search(r'Cross ([A-Za-z]{2}) × ([A-Za-z]{2})',q['prompt'])
            if cross:
                a,b=cross.groups()
                genotype=lambda x,y:''.join(sorted(x+y,key=lambda c:(c.islower(),c)))
                q['solutionTable']={'headers':['Gametes',a[0],a[1]],'rows':[[b[0],genotype(a[0],b[0]),genotype(a[1],b[0])],[b[1],genotype(a[0],b[1]),genotype(a[1],b[1])]]}
        if sid=='bio' and q.get('family')=='Vessel structure-function identification':
            match=re.search(r'First=(\w+); second=(\w+)',q['answer'])
            if match:
                explanations={'artery':'The thick muscular, elastic wall withstands and smooths the high-pressure pulses of blood moving away from the heart.','vein':'The thinner wall and wider lumen suit lower-pressure return; valves prevent backflow and help maintain movement towards the heart.','capillary':'Its wall is one cell thick, providing a short diffusion distance for exchange with tissue fluid.'}
                a,b=match.groups();q['answer']=f'1. First vessel: {a}. {explanations[a]}\n2. Second vessel: {b}. {explanations[b]}\n3. Exchange is concentrated in capillary beds because their thin walls, extensive network and close contact with cells favour diffusion. Large arteries and veins chiefly transport blood rather than forming the exchange surface.'
        if sid=='bio' and q.get('family')=='Light requirement and starch test':
            q['answer']+=' The uncovered green region of the same destarched leaf is the comparison: it receives light while plant, water supply, exposure time and surrounding conditions are otherwise shared. Use a water bath to heat alcohol safely during chlorophyll removal, then iodine to test starch.'
        if sid=='english1' and q.get('paperKind'):
            if q['paperKind'] in ['verb','preposition']:
                sentence=q['prompt'].split(': ',1)[-1] if ': ' in q['prompt'] else q['prompt']
                sentence=re.sub(r'\s*\([^)]*\)', '',sentence)
                sentence=sentence.replace('___',q['answerText'])
                sentence=re.split(r' Use | Supply ',sentence)[0]
                q['answer']='Answer: '+q['answerText']+'\n\nCompleted sentence: '+sentence+'\n\nRule: '+q['answer'].split('. ',1)[-1]
            else:
                q['answer']='Complete answer: '+q.get('answerText',q['answer'])+'\n\n'+{'join':'Construction: combine the two clauses using the requested connector; preserve the time order, subject and stated relationship.','transform':'Construction: '+q.get('family','Sentence transformation')+'. Preserve the original tense, agent and meaning while obeying the supplied opening or keyword.'}[q['paperKind']]
        method=METHODS.get(q['topic'])
        if not method:
            if sid=='phy' and any(x in q['topic'].lower() for x in ['circuit','rating','resist','electric','fuse']):method=METHODS['Electricity']
            if sid=='chem' and any(x in q['topic'].lower() for x in ['stoich','gas volume','purity','mole','calculation']):method=METHODS['Chemical calculations']
        if method:q['method'],q['check']=method
        if not q.get('solutionSteps'):
            # Preserve existing calculations and sentences, rather than inventing a
            # longer answer by adding generic instructions or unsupported facts.
            chunks=re.split(r'(?<=[.;])\s+(?=[A-Z₹Σ0-9])',q['answer'])
            q['solutionSteps']=[c.strip() for c in chunks if c.strip()]
    return bank
