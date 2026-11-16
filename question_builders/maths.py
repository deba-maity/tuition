import math
from fractions import Fraction as F
from .common import item, num as N, rng, variant_bank, numeric_mcq

def make_bank():
    families=[]; hard=[]
    def add(name,fn,challenge=False): (hard if challenge else families).append((name,fn))
    def gst(v):
        r=rng('gst',v); price=r.randrange(15,100)*100; rate=r.choice([5,12,18]); disc=r.choice([5,10,15,20])
        taxable=price*(100-disc)/100; tax=taxable*rate/100
        q=item('GST',f'A shop marks an article at ₹{price} and allows {disc}% discount before charging {rate}% GST. The sale is intra-state. Calculate the taxable value, CGST, SGST and final invoice amount.',f'Taxable value = {price} × {100-disc}/100 = ₹{N(taxable)}. Total GST = ₹{N(tax)}; CGST = SGST = ₹{N(tax/2)}. Invoice = taxable value + GST = ₹{N(taxable+tax)}.',4)
        return numeric_mcq(q,taxable+tax,' rupees',f'An article marked ₹{price} is discounted by {disc}% before {rate}% GST. What is the final invoice amount?')
    add('GST: discount then tax',gst)
    def reverse_gst(v):
        r=rng('reversegst',v); base=r.randrange(20,160)*50; rate=r.choice([5,12,18,28]); total=base*(1+rate/100)
        return numeric_mcq(item('GST',f'A GST-inclusive invoice is ₹{N(total)} at {rate}%. Recover the taxable price and the GST component. Explain why subtracting {rate}% of the invoice gives the wrong taxable price.',f'Taxable price = {N(total)} × 100/{100+rate} = ₹{base}. GST = ₹{N(total-base)}. GST is a percentage of the pre-tax value, not of the inclusive amount.'),base,' rupees',f'An invoice of ₹{N(total)} includes {rate}% GST. What is its taxable value?')
    add('GST: inclusive price',reverse_gst)
    def bank(v,inverse=False):
        r=rng('bank'+str(inverse),v); p=r.randrange(3,30)*100; n=r.choice([12,15,18,20,24,30]); rate=r.choice([5,6,7,8]); interest=F(p*n*(n+1)*rate,2400); maturity=p*n+interest
        if inverse: prompt=f'A recurring deposit runs for {n} months at {rate}% p.a. Its maturity is ₹{N(maturity)}. Find the fixed monthly instalment and the total interest.'
        else: prompt=f'₹{p} is deposited at the beginning of each month for {n} months in a recurring deposit earning {rate}% p.a. Use the standard ICSE RD formula to find interest and maturity.'
        return numeric_mcq(item('Banking',prompt,f'I = Pn(n+1)r/2400. Here I = ₹{N(interest)}. M = nP + I = ₹{N(maturity)}. For the inverse problem, P = M/[n + n(n+1)r/2400] = ₹{p}.'),float(interest),' rupees',f'Find the interest on monthly RD instalments ₹{p} for {n} months at {rate}% p.a. using I = Pn(n+1)r/2400.')
    add('RD maturity',bank); add('RD inverse instalment',lambda v:bank(v,True))
    def shares(v,inverse=False):
        r=rng('shares'+str(inverse),v); face=r.choice([10,20,50,100]); market=face+r.choice([5,10,15,20]); count=r.randrange(20,121); rate=r.choice([8,10,12,15,18]); income=F(face*count*rate,100); invest=count*market; yieldp=F(face*rate,market)
        prompt=(f'An investor receives ₹{N(income)} annual dividend from ₹{face} shares paying {rate}%. If each share costs ₹{market}, find the number of shares, investment and percentage yield.' if inverse else f'{count} shares of face value ₹{face} are bought at ₹{market} each. The dividend rate is {rate}%. Find the investment, annual income and percentage yield (to 2 decimal places).')
        return numeric_mcq(item('Shares and dividend',prompt,f'Dividend per share = ₹{N(F(face*rate,100))}. Number = {count}; investment = {count} × {market} = ₹{invest}. Annual income = ₹{N(income)}. Yield = income/investment × 100 = {float(yieldp):.2f}%. Face value determines dividend; market price determines investment.'),float(income),' rupees',f'{count} shares of face value ₹{face} pay {rate}% dividend. What is the annual dividend?')
    add('Shares: income and yield',shares); add('Shares: recover investment',lambda v:shares(v,True))
    def inequality(v):
        r=rng('ineq',v); a=r.randint(2,9); low=r.randint(-8,2); high=low+r.randint(3,7); b=r.randint(-9,9)
        return item('Linear inequations',f'Solve {a*low+b} < {a}x {b:+} ≤ {a*high+b}, where x is an integer. List the solution set and state which boundary is excluded.',f'Subtract {b} throughout and divide by positive {a}: {low} < x ≤ {high}. Integers: '+', '.join(map(str,range(low+1,high+1)))+f'. The lower endpoint {low} is excluded; {high} is included.')
    add('Double inequations',inequality)
    def negative_ineq(v):
        r=rng('negineq',v); k=r.randint(2,8); b=r.randint(1,15); root=r.randint(-5,10); rhs=b-k*root
        return numeric_mcq(item('Linear inequations',f'Solve {b} − {k}x > {rhs} for real x. Explain what happens to the inequality sign when dividing by −{k}.',f'−{k}x > {rhs-b}; division by a negative number reverses > to <: x < {root}.'),root,'',f'When {b} − {k}x > {rhs} is written x < k, find k.')
    add('Inequality: negative divisor',negative_ineq)
    def quad(v,kind=0):
        r=rng('quad'+str(kind),v); a=r.randint(1,9); b=r.randint(2,13)
        if a==b:b+=1
        if kind==0: return item('Quadratic equations',f'Solve x² − {a+b}x + {a*b} = 0 by factorisation. Verify both roots by stating their sum and product.',f'(x − {a})(x − {b}) = 0; x = {a} or {b}. Sum {a+b}; product {a*b}.')
        if kind==1:
            c=r.randint(1,7); rad=math.sqrt(a*a+4*c)
            return item('Quadratic equations',f'Solve x² + {a}x − {c} = 0. Give both roots correct to 3 significant figures.',f'x = [−{a} ± √({a*a+4*c})]/2. Roots: {(-a+rad)/2:.3g}, {(-a-rad)/2:.3g}. Retain unrounded values until the final step.',4)
        return item('Quadratic equations',f'A rectangle has breadth x cm, length {b} cm more than its breadth, and area {a*(a+b)} cm². Form a quadratic equation and find its perimeter.',f'x(x+{b}) = {a*(a+b)}. The positive root is x={a}; length={a+b}. Reject x=−{a+b}. Perimeter = 2({a}+{a+b}) = {4*a+2*b} cm.',4)
    for i,n in enumerate(['Quadratic factorisation','Quadratic formula accuracy','Quadratic modelling']):add(n,lambda v,i=i:quad(v,i))
    def discriminant(v):
        r=rng('disc',v); a=r.randint(2,10); b=r.randint(2,8); k=a*a*b
        return item('Quadratic equations',f'For the equation {b}x² − {2*a*b}x + k = 0 to have equal real roots, find k and the repeated root. State the condition used.',f'Equal roots require b²−4ac=0. ({2*a*b})²−4({b})k=0, giving k={k}. Repeated root = {2*a*b}/(2×{b}) = {a}.')
    add('Equal-root parameter',discriminant)
    def factor(v):
        r=rng('factor',v); a=r.randint(1,7); b=r.randint(2,9); c=r.randint(3,11)
        return item('Factor and remainder theorem',f'P(x)=x³−{a+b+c}x²+{a*b+a*c+b*c}x−{a*b*c}. Use the factor theorem to verify that x−{a} is a factor and factorise P(x) completely.',f'P({a})=0. Dividing gives (x−{a})[x²−{b+c}x+{b*c}] = (x−{a})(x−{b})(x−{c}).',4)
    add('Cubic factor theorem',factor)
    def remainder(v):
        r=rng('remainder',v); a=r.randint(2,8); b=r.randint(1,10); c=r.randint(-9,9); x=r.randint(-4,6); result=a*x**3-b*x+c
        return numeric_mcq(item('Factor and remainder theorem',f'Find the remainder when {a}x³−{b}x {c:+} is divided by x−({x}). Name the theorem that avoids polynomial long division.',f'Remainder theorem: remainder=P({x})={a}({x})³−{b}({x})+({c})={result}.'),result)
    add('Remainder evaluation',remainder)
    def matrix(v,kind=0):
        r=rng('matrix'+str(kind),v); a,b,c,d,e,f,g,h=[r.randint(-5,8) for _ in range(8)]; ab=[[a*e+b*g,a*f+b*h],[c*e+d*g,c*f+d*h]]
        if kind==0:return item('Matrices',f'A=[[{a},{b}],[{c},{d}]], B=[[{e},{f}],[{g},{h}]]. Calculate AB, showing the row-by-column calculation for its top-right element.',f'AB={ab}. The top-right element is {a}×{f}+{b}×{h}={a*f+b*h}.',4)
        if kind==1:return item('Matrices',f'If 2[[x,{b}],[{c},y]] + [[{e},0],[0,{h}]] = [[{2*a+e},{2*b}],[{2*c},{2*d+h}]], find x and y. Show the two corresponding-entry equations.',f'2x+{e}={2*a+e}, so x={a}; 2y+{h}={2*d+h}, so y={d}.')
        ba=[[e*a+f*c,e*b+f*d],[g*a+h*c,g*b+h*d]]
        return item('Matrices',f'For A=[[{a},{b}],[{c},{d}]] and B=[[{e},{f}],[{g},{h}]], calculate AB and BA. Decide whether these particular matrices commute.',f'AB={ab}; BA={ba}. '+('They commute for these entries.' if ab==ba else 'They do not commute because AB≠BA.'),4)
    for i,n in enumerate(['Matrix product','Matrix unknown entries','Matrix noncommutativity']):add(n,lambda v,i=i:matrix(v,i))
    def ap(v,inverse=False):
        r=rng('ap'+str(inverse),v); a=r.randint(-6,18); d=r.randint(2,12); n=r.randint(12,45); k=r.randint(3,8); m=k+r.randint(3,9); term=a+(n-1)*d; total=n*(2*a+(n-1)*d)//2
        prompt=(f'The {k}th and {m}th terms of an AP are {a+(k-1)*d} and {a+(m-1)*d}. Find its first term, common difference and sum of the first {n} terms.' if inverse else f'An AP has first term {a} and common difference {d}. Find its {n}th term and the sum of its first {n} terms.')
        return item('Arithmetic progression',prompt,f'a={a}, d={d}; a{n}=a+({n}−1)d={term}. S{n}={n}/2[2a+({n}−1)d]={total}. For an inverse question, subtract the two term equations first.')
    add('AP term and sum',ap);add('AP recover a and d',lambda v:ap(v,True))
    def gp(v):
        r=rng('gp',v); a=r.randint(2,20); ratio=r.choice([2,3,-2]); n=r.randint(4,7); term=a*ratio**(n-1); total=a*(ratio**n-1)//(ratio-1)
        return item('Geometric progression',f'A GP begins {a}, {a*ratio}, {a*ratio*ratio}, ... . Find its common ratio, {n}th term and sum of the first {n} terms.',f'r={ratio}; T{n}={a}×({ratio})^{n-1}={term}; S{n}={a}[({ratio})^{n}−1]/({ratio}−1)={total}.')
    add('GP finite term and sum',gp)
    def ratio(v):
        r=rng('ratio',v); x=r.randint(5,35); a=r.randint(1,4); p=F(x+a,x-a)
        return item('Ratio and proportion',f'If (x+{a})/(x−{a}) = {N(p)}, find x. State the excluded value of x before cross-multiplying.',f'x≠{a}. {p.denominator}(x+{a})={p.numerator}(x−{a}); solve to get x={x}.')
    add('Ratio: excluded value',ratio)
    def reflect(v):
        r=rng('reflect',v); x=r.choice([i for i in range(-15,16) if i]); y=r.choice([i for i in range(-15,16) if i])
        return item('Reflection',f'Point P is ({x},{y}). State its image in the x-axis, in the y-axis and in the origin. Which coordinate changes sign in reflection in the x-axis?',f'x-axis: ({x},{-y}); y-axis: ({-x},{y}); origin: ({-x},{-y}). Only the y-coordinate changes in reflection in the x-axis.')
    add('Coordinate reflection',reflect)
    def section(v):
        r=rng('section',v); x=r.randint(-10,10); y=r.randint(-10,10); dx=r.randint(2,6); dy=r.randint(2,6); m=r.randint(1,5); n=r.randint(1,5); bx=x+(m+n)*dx; by=y+(m+n)*dy
        return item('Section formula',f'A({x},{y}) and B({bx},{by}) are divided internally by P in ratio AP:PB={m}:{n}. Find P and verify the ratio using the change in x-coordinates.',f'P=(({n}×{x}+{m}×{bx})/{m+n},({n}×{y}+{m}×{by})/{m+n})=({x+m*dx},{y+m*dy}). The x-distances are {m*dx} and {n*dx}, ratio {m}:{n}.')
    add('Internal division',section)
    def line(v,perp=False):
        r=rng('line'+str(perp),v); a=r.randint(1,8); b=r.randint(2,9); x=r.randint(-7,9); y=r.randint(-8,9); slope=F(-b,a) if perp else F(a,b)
        return item('Equation of a line',f'Find the equation of the line through ({x},{y}) '+(f'perpendicular to a line of slope {a}/{b}.' if perp else f'parallel to a line of slope {a}/{b}.')+' Give the equation in point-slope form.',f'Required slope={N(slope)}. The equation is y−({y})=({N(slope)})(x−({x})). '+('The product of the slopes is −1.' if perp else 'Parallel lines have the same slope.'))
    add('Parallel line equation',line);add('Perpendicular line equation',lambda v:line(v,True))
    def midpoint(v):
        r=rng('mid',v); x,y=[r.randint(-12,12) for _ in range(2)]; mx,my=[r.randint(-5,9) for _ in range(2)]
        return item('Coordinate geometry',f'A is ({x},{y}) and the midpoint of AB is M({mx},{my}). Find B and the length AM, correct to 2 decimal places.',f'B=(2×{mx}−({x}),2×{my}−({y}))=({2*mx-x},{2*my-y}). AM=√[({mx-x})²+({my-y})²]={math.hypot(mx-x,my-y):.2f} units.')
    add('Midpoint and distance',midpoint)
    def similarity(v):
        r=rng('sim',v); m=r.randint(2,5); n=m+r.randint(1,4); k=r.randint(2,15); diff=(n*n-m*m)*k
        return item('Similarity',f'The corresponding sides of two similar triangles are in ratio {m}:{n}. Their areas differ by {diff} cm². Find both areas and the ratio of corresponding altitudes.',f'Areas are {m*m}k and {n*n}k. Difference gives k={k}; areas {m*m*k} cm² and {n*n*k} cm². Altitudes have the same linear ratio {m}:{n}.')
    add('Similarity: area difference',similarity)
    def cyclic(v):
        r=rng('cyclic',v); x=r.randint(15,35); a=r.randint(2,4); b=r.randint(2,4); c=r.randint(-10,15); d=180-(a+b)*x-c
        return item('Circles',f'ABCD is cyclic. Opposite angles A and C are ({a}x {c:+})° and ({b}x {d:+})°. Find x and both angles; state the circle property used.',f'Opposite angles of a cyclic quadrilateral are supplementary. ({a+b})x+({c+d})=180, so x={x}. A={a*x+c}°, C={b*x+d}°.')
    add('Cyclic opposite angles',cyclic)
    def tangent(v):
        r=rng('tangent',v); tangent=r.randint(6,30); pb=r.randint(2,6); pc=F(tangent*tangent,pb)
        return item('Circles',f'From an external point P a tangent PA has length {tangent} cm. A secant through P meets the circle first at B and then C; PB={pb} cm. Find PC and BC. All lengths are measured along the same secant.',f'Tangent-secant theorem: PA²=PB×PC. PC={tangent*tangent}/{pb}={N(pc)} cm. BC=PC−PB={N(pc-pb)} cm.')
    add('Tangent and secant lengths',tangent)
    def tangentangle(v):
        r=rng('tanangle',v); angle=r.randint(24,75)
        return numeric_mcq(item('Circles',f'PA and PB touch a circle at A and B, with O as centre. If ∠APB={angle}°, find ∠AOB and explain why angles OAP and OBP are right angles.',f'A radius is perpendicular to the tangent at contact. Quadrilateral OAPB has two right angles; ∠AOB=360−180−{angle}={180-angle}°.'),180-angle,' degrees',f'Two tangents PA and PB enclose {angle}°. What angle do OA and OB enclose at the centre?')
    add('Angle between tangents',tangentangle)
    def cone(v):
        r=rng('cone',v); radius=r.randint(2,10); height=r.randint(2,12)*3; small=r.choice([1,2]); count=F(radius*radius*height,4*small**3)
        return item('Mensuration',f'A solid cone of radius {radius} cm and height {height} cm is melted without loss into spheres of radius {small} cm. Find the ratio of the cone volume to one sphere volume. Can an exact whole number of complete spheres be obtained with no material left? Explain.',f'Cone volume=π×{radius}²×{height}/3. Sphere volume=4π×{small}³/3. Ratio={N(count)}:1. '+(f'Exactly {count.numerator} spheres can be made.' if count.denominator==1 else f'No: the ratio is not an integer; {count.numerator//count.denominator} complete spheres leave some material.'),4)
    add('Recasting solids',cone)
    def cylinder(v):
        r=rng('cyl',v); radius=r.randint(3,15); height=r.randint(5,30)
        return item('Mensuration',f'A closed cylindrical tin has radius {radius} cm and height {height} cm. Find its total surface area and capacity using π=22/7. Give answers to 2 decimal places.',f'TSA=2πr(r+h)=2×22/7×{radius}×{radius+height}={2*22/7*radius*(radius+height):.2f} cm². Volume=πr²h={22/7*radius**2*height:.2f} cm³.')
    add('Cylinder area and volume',cylinder)
    def hemisphere(v):
        r=rng('hemi',v); radius=r.randint(3,14); h=r.randint(6,24)
        return item('Mensuration',f'A solid consists of a cylinder of radius {radius} cm and height {h} cm surmounted by a hemisphere of the same radius. Its bottom circular face is exposed. Find the external surface area in terms of π.',f'External area=cylinder CSA+hemisphere CSA+bottom circle = 2πrh+2πr²+πr² = {2*radius*h+3*radius**2}π cm². Do not count the joined circular surfaces.',4)
    add('Combined solid external area',hemisphere)
    def trig(v,kind=0):
        r=rng('trig'+str(kind),v); triple=r.choice([(3,4,5),(5,12,13),(8,15,17),(7,24,25)]); a,b,c=triple; k=r.randint(2,25)
        if kind==0:return item('Trigonometry',f'For acute θ, sin θ={a}/{c}. Find cos θ, tan θ and ({k}sin θ + cos θ).',f'Using a right triangle, adjacent side={b}. cos θ={b}/{c}; tan θ={a}/{b}; required expression=({k}×{a}+{b})/{c}={N(F(k*a+b,c))}.')
        d=r.randint(5,50); angle=r.choice([30,45,60]); h=d*math.tan(math.radians(angle))
        return item('Heights and distances',f'An observer whose eye is {k/10:.1f} m above level ground stands {d} m from a vertical tower. The angle of elevation of its top is {angle}°. Find the tower height to 2 decimal places.',f'Height above eye level={d}tan {angle}°={h:.3f} m. Add eye height: tower={h+k/10:.2f} m. Horizontal ground distance is the adjacent side.',4)
    add('Acute-angle ratios',trig);add('Tower with observer height',lambda v:trig(v,1))
    def identity(v):
        r=rng('ident',v); k=r.randint(2,150)
        return item('Trigonometric identities',f'For acute θ, simplify {k}[(1−cos²θ)/sin²θ] + (sec²θ−tan²θ). State the identities used.',f'1−cos²θ=sin²θ, so the bracket is 1. sec²θ−tan²θ=1. Result={k+1}.')
    add('Identity simplification',identity)
    def mean(v):
        r=rng('mean',v); vals=sorted(r.sample(range(5,70,5),4)); freqs=[r.randint(2,12) for _ in vals]; total=sum(freqs); fx=sum(a*b for a,b in zip(vals,freqs))
        return item('Statistics',f'Values x: {vals}; corresponding frequencies f: {freqs}. Find Σf, Σfx and the mean, correct to 2 decimal places.',f'Σf={total}; Σfx={fx}; mean=Σfx/Σf={fx}/{total}={fx/total:.2f}. A simple unweighted mean would ignore frequencies.')
    add('Weighted mean',mean)
    def missing_mean(v):
        r=rng('missmean',v); a=r.randint(3,12); f=r.randint(2,9); k=r.randint(2,10); x=[a,2*a,3*a]; target=F(a*f+2*a*k+3*a*f,2*f+k)
        return item('Statistics',f'The values {x} have frequencies {f}, k, {f} respectively. Their mean is {2*a}. Can k be determined uniquely? Justify your answer, assuming k is a positive integer.',f'Σfx={4*a*f}+{2*a}k; Σf={2*f}+k. The mean simplifies to {2*a} for every positive k. The information does not determine k uniquely.',4)
    add('Mean: sufficiency of information',missing_mean)
    def grouped_median(v):
        r=rng('median',v); start=r.randrange(0,30,5); width=r.choice([5,10]); fs=[r.randint(3,10),r.randint(10,20),r.randint(12,24),r.randint(3,10)]; total=sum(fs); cum=0; index=0
        for i,f in enumerate(fs):
            if cum+f>=total/2:index=i;break
            cum+=f
        val=start+index*width+(total/2-cum)/fs[index]*width
        classes=[f'{start+i*width}–{start+(i+1)*width}' for i in range(4)]
        return item('Statistics',f'Continuous classes: {classes}; frequencies: {fs}. Form the less-than cumulative frequencies and use linear interpolation within the median class to estimate the median. No graph is required.',f'Cumulative frequencies='+str([sum(fs[:i+1]) for i in range(4)])+f'. N={total}; N/2={total/2}. Median class={classes[index]}. Median=L+[(N/2−cf)/f]h={val:.2f}.',4)
    add('Median from cumulative data',grouped_median)
    def density(v):
        r=rng('density',v); k=r.randint(2,12); f=[r.randint(2,20),r.randint(3,18),2*k]; a=r.randint(0,20)
        return item('Statistics',f'Class intervals {a}–{a+10}, {a+10}–{a+20}, {a+20}–{a+40} have frequencies {f}. Without drawing, state the three histogram heights when a 10-unit class width is used as standard. Explain why the last raw frequency is not its height.',f'Adjusted height=f×10/class width. Heights={f[0]}, {f[1]}, {k}. The last class has double width; its area, not height alone, must represent frequency.')
    add('Histogram density without drawing',density)
    def probability(v):
        r=rng('prob',v); red=r.randint(3,15); blue=r.randint(2,12); green=r.randint(2,10); total=red+blue+green
        return item('Probability',f'A bag contains {red} red, {blue} blue and {green} green balls, identical except for colour. One ball is selected at random. Find P(red), P(not blue) and P(blue or green).',f'Total={total}; P(red)={N(F(red,total))}; P(not blue)={N(F(red+green,total))}; P(blue or green)={N(F(blue+green,total))}. This is a single draw.')
    add('Single-event colour probabilities',probability)
    def numbered_cards(v):
        r=rng('cards',v); n=r.randint(15,90); d=r.choice([2,3,4,5,6,7]); multiples=n//d; odds=(n+1)//2
        return item('Probability',f'Cards numbered 1 to {n} are thoroughly mixed and one is drawn. Find the probability that its number is divisible by {d}; also find the probability that it is odd.',f'Favourable multiples={multiples}; probability={N(F(multiples,n))}. Odd numbers={odds}; probability={N(F(odds,n))}.')
    add('Numbered-card events',numbered_cards)
    # Twists stay within the syllabus: reverse calculations, competing interpretations,
    # sign choices and missing information, not an unrelated olympiad extension.
    def h_gst(v):
        r=rng('hgst',v); marked=r.randrange(20,100)*100; disc=r.choice([5,10,15,20,25]); rate=r.choice([5,12,18]); paid=marked*(100-disc)/100*(100+rate)/100
        return item('GST',f'A customer has exactly ₹{N(paid)}. An article is marked ₹{marked}, and GST at {rate}% is payable after discount. What minimum percentage discount makes the invoice exactly equal to the money available? Show why applying the discount after GST gives the same numerical invoice here.',f'Let discount=d%. {marked}(1−d/100)({100+rate}/100)={N(paid)} gives d={disc}%. Percentage factors multiply commutatively when both are applied to the same price chain; tax itself is calculated on the discounted value.',4)
    add('Twist: reverse GST discount',h_gst,True)
    def h_roots(v):
        r=rng('hroots',v); a=r.randint(2,12); b=r.randint(2,15)
        return item('Quadratic equations',f'A student obtains x={a} and x=−{b} while solving a rectangle problem with breadth x. The rectangle has length x{b-a:+} and area {a*b}. Explain which root is physically admissible and find the actual dimensions. Explain why an algebraically valid root may be rejected.',f'Positive root x={a} is the breadth; length={b}. Root −{b} makes the breadth negative and is inadmissible. Dimensions {a} by {b}; area={a*b}. The model imposes positive lengths.',4)
    add('Twist: algebraic versus admissible roots',h_roots,True)
    def h_inverse(v):
        r=rng('hinverse',v); m=r.randint(2,8); n=m+r.randint(1,6); area=r.randint(3,18)*m*m
        return item('Similarity',f'Two similar triangles have corresponding side ratio {m}:{n}. A student multiplies the smaller area {area} cm² by {n}/{m} to obtain the larger area. Correct the method, calculate the larger area, and find the scale factor for perimeters.',f'Areas scale by the square of the side factor. Larger area={area}×({n}/{m})²={N(F(area*n*n,m*m))} cm². Perimeters scale by {n}:{m}. The student used a linear factor on an area.',4)
    add('Twist: linear and area scale',h_inverse,True)
    def h_tangent(v):
        q=tangent(v+300);q['prompt']+=' A student treats the supplied PB as BC. Explain the difference and identify the first point at which the secant meets the circle.';q['answer']+=' PB is the outside segment and BC lies inside the circle; B is the nearer intersection.';return q
    add('Twist: external versus whole secant',h_tangent,True)
    def h_weight(v):
        r=rng('hweight',v); a=r.randint(10,35); b=a+r.randint(10,30); f=r.randint(2,6); g=f+r.randint(3,9)
        return item('Statistics',f'A class records {f} students scoring {a} and {g} students scoring {b}. A student reports the mean as ({a}+{b})/2. Find the correct mean and show when that shortcut would be valid.',f'Weighted mean=({f}×{a}+{g}×{b})/{f+g}={(f*a+g*b)/(f+g):.2f}. The shortcut is valid if frequencies are equal (or if the two scores coincide). Here the frequencies differ.',4)
    add('Twist: unweighted-mean trap',h_weight,True)
    add('Twist: symmetric-frequency indeterminacy',lambda v:missing_mean(v+500),True)
    def h_section(v):
        q=section(v+300);q['prompt']+=' A student reverses the weights m and n in the formula. State which endpoint must receive the coefficient m when AP:PB=m:n.';q['answer']+=' Endpoint B receives m; endpoint A receives n.';return q
    add('Twist: section-formula weights',h_section,True)
    def h_prob(v):
        r=rng('hprob',v); a=r.randint(3,12); b=r.randint(2,9); c=r.randint(2,8); total=a+b+c
        return item('Probability',f'A bag has {a} red, {b} blue and {c} green balls. One ball is drawn. A student adds P(not red)+P(not blue) to calculate P(red or blue). Find both quantities and explain the overcounting.',f'P(red or blue)={N(F(a+b,total))}. P(not red)+P(not blue)={N(F(a+b+2*c,total))}. Green belongs to both complement events and is counted twice; the sum is not the requested union.',4)
    add('Twist: overlapping events on a single draw',h_prob,True)
    def h_rd(v):
        q=bank(v+300);q['prompt']+=' A classmate uses simple interest on nP for the whole n-month term. Explain why this overestimates the interest.';q['answer']+=' Later instalments earn for fewer months; the balances do not all remain deposited for n months.';return q
    add('Twist: RD time-weighting',h_rd,True)
    def h_heights(v):
        r=rng('hheight',v); dist=r.randint(10,70); eye=r.choice([1.2,1.4,1.5,1.6,1.8]); angle=r.choice([30,45,60]); value=dist*math.tan(math.radians(angle))+eye
        return item('Heights and distances',f'A surveyor’s eye is {eye} m above horizontal ground. The tower base is {dist} m away and the elevation of the top is {angle}°. A solution gives {dist}tan({angle}°) as the tower height. Identify the missing term and calculate the height to 2 decimal places.',f'The triangle gives height above the eye, not above ground. Add {eye} m: h={dist}tan({angle}°)+{eye}={value:.2f} m.',4)
    add('Twist: reference level in elevation',h_heights,True)
    return variant_bank('maths',families,hard)
