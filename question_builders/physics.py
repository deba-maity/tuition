import math
from fractions import Fraction as F
from .common import item, num as N, rng, variant_bank, numeric_mcq

def make_bank():
    families=[]; hard=[]
    def add(name,fn,h=False):(hard if h else families).append((name,fn))
    def moment(v,inverse=False):
        r=rng('moment'+str(inverse),v); force=r.randint(12,90); arm=r.randint(5,45)/100; torque=force*arm
        text=(f'A perpendicular force produces a moment of {N(torque)} N m about a pivot. Its line of action is {arm*100:.0f} cm from the pivot. Calculate the force and explain why applying it through the pivot would produce no moment.' if inverse else f'A force of {force} N acts at right angles to a spanner {arm*100:.0f} cm from its pivot. Find the turning moment. If the same force acts at half this perpendicular distance, what is the new moment?')
        q=item('Forces and moments',text,f'Perpendicular distance={N(arm)} m. Moment=force×distance={force}×{N(arm)}={N(torque)} N m. At half the distance the moment is {N(torque/2)} N m. In the inverse calculation force={N(torque)}/{N(arm)}={force} N; through the pivot the arm is zero.')
        return numeric_mcq(q,torque,' N m',f'A perpendicular force {force} N has a moment arm {arm*100:.0f} cm. Find its moment.')
    add('Moment from perpendicular arm',moment);add('Moment: recover force',lambda v:moment(v,True))
    def beam(v):
        r=rng('beam',v); m=r.randint(1,9)*10; left=r.randint(2,9)*5; right=r.randint(2,9)*5; other=F(m*left,right)
        return item('Forces and moments',f'A light horizontal beam is supported at a pivot. A {m} N load is {left} cm to the left. What downward force at {right} cm to the right balances it? Find the upward reaction at the pivot.',f'Clockwise moment=anticlockwise moment: F×{right}={m}×{left}. F={N(other)} N. Vertical balance gives reaction={m}+{N(other)}={N(m+other)} N. The beam weight is neglected.',4)
    add('Beam equilibrium and support reaction',beam)
    def couple(v):
        r=rng('couple',v); force=r.randint(5,60); distance=r.randint(8,80)/100
        return numeric_mcq(item('Forces and moments',f'Two equal, opposite, parallel forces of {force} N act along lines {N(distance)} m apart. Find their resultant force and couple moment. Does choosing another moment point change the couple moment?',f'Resultant force=0. Couple moment=one force×perpendicular separation={force}×{N(distance)}={N(force*distance)} N m. It is independent of the moment point.'),force*distance,' N m',f'A couple consists of two {force} N forces whose lines of action are {N(distance)} m apart. Find the couple moment.')
    add('Couple moment',couple)
    def work(v):
        r=rng('work',v); force=r.randint(10,90); displacement=r.randint(3,35); angle=r.choice([0,90,180]); val=force*displacement*{0:1,90:0,180:-1}[angle]
        return numeric_mcq(item('Work, energy and power',f'A constant {force} N force acts while an object is displaced {displacement} m. The angle between force and displacement is {angle}°. Find the work and interpret its sign.',f'W=Fs cosθ={force}×{displacement}×cos {angle}°={val} J. '+({0:'Force transfers energy to the object.',90:'The force is perpendicular to displacement and does no work.',180:'The force opposes motion and removes mechanical energy.'}[angle])),val,' J',f'Find the work by a {force} N force over {displacement} m when the force and displacement enclose {angle}°.')
    add('Work and direction',work)
    def lifting(v):
        r=rng('lifting',v); mass=r.randint(8,75); h=r.randint(2,22); t=r.randint(5,45); e=mass*10*h
        return numeric_mcq(item('Work, energy and power',f'A motor raises a {mass} kg load vertically through {h} m in {t} s at steady speed. Take g=10 m/s². Find useful work and average useful power.',f'Work against gravity=mgh={mass}×10×{h}={e} J. Useful power=W/t={e}/{t}={e/t:.2f} W.'),e,' J',f'Find the gain in gravitational potential energy when {mass} kg is lifted by {h} m. Take g=10 m/s².')
    add('Lifting work and power',lifting)
    def kinetic(v):
        r=rng('kinetic',v); m=r.randint(2,45); u=r.randint(2,12); speed=r.randint(13,26); delta=.5*m*(speed*speed-u*u)
        return item('Work, energy and power',f'A {m} kg body increases its speed from {u} m/s to {speed} m/s. Find the increase in kinetic energy and the net work done. State the principle connecting the two.',f'ΔKE=½m(v²−u²)=½×{m}×({speed}²−{u}²)={N(delta)} J. Net work equals the change in kinetic energy (work-energy theorem).')
    add('Kinetic energy change',kinetic)
    def energy_ratio(v):
        r=rng('eratio',v); m=r.randint(2,12); speed=r.randint(2,7); original=r.randint(20,250)
        return item('Work, energy and power',f'A body initially has kinetic energy {original} J. Its mass is multiplied by {m} and speed by {speed}. Find the new kinetic energy and explain why multiplying by {m*speed} is incorrect.',f'KE is proportional to mv². Multiplier={m}×{speed}²={m*speed*speed}. New KE={original*m*speed*speed} J. Speed enters quadratically, not linearly.')
    add('Energy proportionality',energy_ratio)
    def falling(v):
        r=rng('fall',v); h=r.randint(8,100); mass=r.randint(1,25); mid=r.randint(1,h-1)
        return item('Conservation of energy',f'A {mass} kg stone falls from rest from height {h} m. Neglect air resistance and use g=10 m/s². Find its potential and kinetic energies at height {mid} m above ground and its speed there.',f'Total energy={mass*10*h} J. PE={mass*10*mid} J; KE=mg({h}−{mid})={mass*10*(h-mid)} J. v=√[2g({h}−{mid})]={math.sqrt(20*(h-mid)):.2f} m/s.',4)
    add('Falling-body energy at intermediate height',falling)
    def machine(v):
        r=rng('machine',v); vr=r.randint(2,8); eff=r.choice([40,50,60,75,80,90]); effort=r.randint(20,100); ma=vr*eff/100; load=ma*effort
        return item('Machines',f'A machine has velocity ratio {vr} and efficiency {eff}%. It is operated with effort {effort} N. Find mechanical advantage and the load it can raise steadily. Why can its MA be less than its VR?',f'η=MA/VR×100, so MA={vr}×{eff}/100={N(ma)}. Load=MA×effort={N(load)} N. Friction and other dissipative losses reduce useful output work.')
    add('Machine efficiency and load',machine)
    def pulley(v):
        r=rng('pulley',v); strands=r.randint(2,7); load=r.randint(12,80)*10; effort=r.choice([1.1,1.2,1.25,1.5])*load/strands
        return item('Machines',f'A pulley system has {strands} supporting rope segments. A {load} N load is raised by effort {N(effort)} N. Take VR equal to the number of supporting segments. Find MA and efficiency, to 2 decimal places.',f'MA=L/E={load}/{N(effort)}={load/effort:.2f}; VR={strands}; η=MA/VR×100={load/effort/strands*100:.2f}%.')
    add('Pulley MA VR efficiency',pulley)
    def lever(v):
        r=rng('lever',v); effort_arm=r.randint(3,12)*10; load_arm=r.randint(1,3)*5; load=r.randint(15,90)*10
        return item('Machines',f'In an ideal lever the effort arm is {effort_arm} cm and load arm is {load_arm} cm. The load is {load} N. Find the required effort and velocity ratio. Can arm lengths alone identify the class of lever? Explain.',f'E×{effort_arm}=L×{load_arm}; E={N(F(load*load_arm,effort_arm))} N. VR={N(F(effort_arm,load_arm))}. No: class depends on the relative positions of load, fulcrum and effort.',4)
    add('Lever arms and classification information',lever)
    def refraction(v):
        r=rng('refract',v); mu=r.choice([1.25,1.4,1.5,1.6,1.8]); sini=r.randint(30,85)/100
        return item('Refraction at plane surfaces',f'A ray travels from air into a medium of refractive index {mu}. If sin i={sini}, find sin r and the speed of light in the medium. Use c=3×10⁸ m/s.',f'Snell’s law gives sin r=sin i/μ={sini}/{mu}={sini/mu:.3f}. v=c/μ={3e8/mu:.3e} m/s. The ray bends towards the normal.')
    add('Snell law and speed',refraction)
    def apparent(v):
        r=rng('apparent',v); depth=r.randint(10,70); mu=r.choice([1.25,1.5,1.6,2]); apparent=depth/mu
        return item('Refraction at plane surfaces',f'A coin is {depth} cm below the surface of a transparent liquid of refractive index {mu}. Viewed nearly normally from air, find its apparent depth and apparent upward shift.',f'Apparent depth=real depth/μ={depth}/{mu}={N(apparent)} cm. Shift=real−apparent={N(depth-apparent)} cm. The relation assumes near-normal viewing.')
    add('Real and apparent depth',apparent)
    def relative(v):
        r=rng('relative',v); a=r.choice([1.2,1.25,1.3,1.4]); b=r.choice([1.5,1.6,1.7,1.8]); i=r.randint(20,60)
        return item('Refraction at plane surfaces',f'Media A and B have absolute refractive indices {a} and {b}. A ray passes from A into B at incidence {i}°. Calculate the relative refractive index of B with respect to A and sin r. State the bending direction.',f'μBA=μB/μA={b/a:.3f}. sin r=μA sin i/μB={a*math.sin(math.radians(i))/b:.3f}. B is optically denser, so it bends towards the normal.')
    add('Relative optical density',relative)
    def critical(v):
        r=rng('critical',v); mu=r.choice([1.25,1.3,1.4,1.5,1.6,1.7,1.8,2]); angle=r.randint(20,80); crit=math.degrees(math.asin(1/mu)); status='total internal reflection' if angle>crit else 'refraction into air'
        return item('Total internal reflection',f'Light travels from a medium of refractive index {mu} into air at incidence {angle}°. Calculate the critical angle to 1 decimal place and decide whether total internal reflection occurs.',f'sin C=1/μ=1/{mu}, so C={crit:.1f}°. Since i is '+('greater' if angle>crit else 'less')+f' than C, the ray undergoes {status}. The dense-to-rare condition is satisfied.')
    add('Critical-angle condition',critical)
    def lens(v,kind=0):
        r=rng('lens'+str(kind),v); f=r.randint(4,24); factor=r.choice([1.5,2,3,4,5]); u=-f*factor
        if kind==1:u=-f/r.choice([1.25,1.5,2,2.5,3,4])
        if kind==2:f=-f
        value=1/(1/f+1/u); mag=value/u
        nature='real, inverted' if value>0 else 'virtual, erect'
        return item('Lenses',f'An object is {N(abs(u))} cm to the left of a '+('concave' if f<0 else 'convex')+f' lens of focal length magnitude {abs(f)} cm. Light travels left to right. Use Cartesian signs to find image distance, magnification and image nature.',f'u={N(u)} cm, f={f} cm. 1/v−1/u=1/f gives v={value:.2f} cm. m=v/u={mag:.2f}. Image is {nature}. '+('A negative v places it on the object side.' if value<0 else 'A positive v places it on the far side.'),4)
    for i,n in enumerate(['Convex lens real image','Convex lens virtual image','Concave lens sign convention']):add(n,lambda v,i=i:lens(v,i))
    def power(v):
        r=rng('power',v); f=r.choice([-50,-40,-25,-20,10,12.5,20,25,40,50]); p=100/f
        return numeric_mcq(item('Lenses',f'A lens has focal length {f} cm. Find its power in dioptres, identify the lens type and explain the sign.',f'f={f/100} m; P=1/f={N(p)} D. '+('Positive power: converging convex lens.' if p>0 else 'Negative power: diverging concave lens.')),p,' D',f'What is the power of a lens with focal length {f} cm?')
    # Varying focal lengths above has a finite useful domain; add object distance
    # to retain meaningful distinctness for all requested practice variants.
    def power_expanded(v):
        r=rng('powerx',v); f=r.randint(5,95)*(1 if v%2 else -1); p=100/f; obj=r.randint(10,90)
        return numeric_mcq(item('Lenses',f'A lens labelled with focal length {f} cm is used with an object {obj} cm away. Calculate its power. Does changing the object position change this power?',f'P=100/{f}={p:.3f} D. Power is a property of the lens in its surrounding medium, not of the object position.'),p,' D',f'A lens has focal length {f} cm, irrespective of object position {obj} cm. Find power to 3 decimal places.')
    add('Lens power in metres',power_expanded)
    def echo(v):
        r=rng('echo',v); speed=r.choice([320,330,340,350]); t=r.randint(15,200)/100; distance=speed*t/2
        return numeric_mcq(item('Sound',f'A sound pulse returns as an echo after {t:.2f} s. The speed of sound is {speed} m/s. Find the reflector distance and explain the factor 2 in your formula.',f'The time includes outward and return journeys. 2d=vt; d={speed}×{t:.2f}/2={N(distance)} m.'),distance,' m',f'An echo returns after {t:.2f} s at sound speed {speed} m/s. Find the reflector distance.')
    add('Echo round-trip distance',echo)
    def wavelength(v):
        r=rng('wavelength',v); speed=r.choice([320,330,340]); freq=r.randrange(100,1200,25)
        return item('Sound',f'A source produces sound of frequency {freq} Hz in air where speed is {speed} m/s. Find the wavelength. When the source enters a medium in which sound travels twice as fast, what happens to frequency and wavelength?',f'λ=v/f={speed}/{freq}={speed/freq:.3f} m. Frequency is fixed by the source and remains {freq} Hz. At twice the speed, wavelength doubles to {2*speed/freq:.3f} m.')
    add('Wave speed frequency wavelength',wavelength)
    def waves(v):
        r=rng('waves',v); fa=r.randint(2,12)*100; amp=r.randint(1,8); k=r.randint(2,5)
        return item('Sound',f'Two sound waves A and B have the same frequency {fa} Hz and the same waveform. B has amplitude {k} times A, whose amplitude is {amp} arbitrary units. Compare pitch, quality and intensity.',f'Pitch is the same because frequency is the same. Quality is the same because waveform is the same. Intensity ratio IB:IA={k*k}:1 since intensity is proportional to amplitude squared.')
    add('Sound-wave property comparison',waves)
    def resistance(v):
        r=rng('resistance',v); voltage=r.randint(3,30); current=r.randint(2,15)/10; length=r.choice([2,3,4]); radius=r.choice([2,3])
        return item('Current electricity',f'A wire takes {current:.1f} A at {voltage} V. Find its resistance. A second wire of the same material and temperature has {length} times its length and {radius} times its radius. Find its resistance relative to the first.',f'R=V/I={voltage/current:.3f} Ω. R∝L/A and A∝r², so R2/R1={length}/{radius**2}={N(F(length,radius**2))}; R2={voltage/current*length/radius**2:.3f} Ω.')
    add('Ohm law and geometry',resistance)
    def series(v):
        r=rng('series',v); a=r.randint(2,20); b=r.randint(2,20); volts=r.randint(2,12)*(a+b); cur=volts/(a+b)
        return numeric_mcq(item('Current electricity',f'Resistors {a} Ω and {b} Ω are in series across {volts} V. Find equivalent resistance, current and voltage across each resistor.',f'Req={a+b} Ω. I=V/Req={N(cur)} A. Drops: V1={N(cur*a)} V, V2={N(cur*b)} V; their sum is {volts} V.'),a+b,' ohms',f'Find equivalent resistance of {a} Ω and {b} Ω connected in series.')
    add('Series resistance and voltage division',series)
    def parallel(v):
        r=rng('parallel',v); a=r.randint(2,24); b=r.randint(2,24); volts=r.randint(4,30); eq=F(a*b,a+b)
        return item('Current electricity',f'Resistors {a} Ω and {b} Ω are connected in parallel across {volts} V. Find equivalent resistance, current in each branch and total current.',f'Req=R1R2/(R1+R2)={N(eq)} Ω. I1={volts/a:.3f} A; I2={volts/b:.3f} A; total={volts/a+volts/b:.3f} A. Each branch has the full {volts} V supply.',4)
    add('Parallel resistance and branch current',parallel)
    def mixed(v):
        r=rng('mixed',v); a=r.randint(2,15); b=r.randint(2,15); c=r.randint(2,10); volts=r.randint(6,36); para=F(a*b,a+b); eq=para+c; cur=F(volts,1)/eq
        return item('Current electricity',f'A {a} Ω resistor and a {b} Ω resistor form a parallel pair. This pair is connected in series with {c} Ω across {volts} V. Find total resistance, total current and the voltage across the parallel pair.',f'Parallel resistance={N(para)} Ω. Total={N(eq)} Ω. I={float(cur):.3f} A. Voltage across pair=I×Rp={float(cur*para):.3f} V.',4)
    add('Text-described mixed circuit',mixed)
    def rating(v):
        r=rng('rating',v); volts=r.choice([110,220,230,240]); power=r.randrange(2,25)*100; actual=volts/2
        return item('Electrical power',f'A heater is rated {power} W, {volts} V. Calculate its rated current and resistance. Assuming resistance is constant, find its power when operated at {N(actual)} V.',f'I=P/V={power/volts:.3f} A. R=V²/P={volts**2/power:.3f} Ω. At half voltage, P′=V′²/R=P/4={power/4:.1f} W. This assumes unchanged resistance.',4)
    add('Appliance rating and changed voltage',rating)
    def energy(v):
        r=rng('energy',v); watts=r.randrange(2,22)*100; hours=r.choice([1.5,2,2.5,3,4,5]); days=r.randint(12,31); rate=r.randint(4,11); kwh=watts/1000*hours*days
        return numeric_mcq(item('Household electricity',f'A {watts} W appliance runs for {hours} hours daily for {days} days. Electricity costs ₹{rate} per kWh. Find energy used and the energy charge, excluding fixed fees.',f'Power={watts/1000} kW. E=Pt={watts/1000}×{hours}×{days}={N(kwh)} kWh. Charge={N(kwh)}×{rate}=₹{N(kwh*rate)}.'),kwh,' kWh',f'A {watts} W appliance runs {hours} hours per day for {days} days. Find electrical energy used.')
    add('Energy consumption and billing',energy)
    def meter(v):
        r=rng('meter',v); start=r.randint(1000,8000); diff=r.randint(20,180); kw=r.choice([.5,1,1.5,2,2.5]); hours=diff/kw
        return item('Household electricity',f'A meter reads {start} kWh initially and {start+diff} kWh later. A single {N(kw*1000)} W appliance is the only load and operates continuously between readings. Find the operating time. Explain why dividing the readings themselves would be meaningless.',f'Energy change={diff} kWh; power={kw} kW. Time=E/P={diff}/{kw}={N(hours)} h. Readings are cumulative; use their difference, not their ratio.')
    add('Meter difference to time',meter)
    def fuse(v):
        r=rng('fuse',v); volts=r.choice([220,230,240]); powers=[r.randrange(1,8)*100,r.randrange(5,16)*100,r.randrange(1,5)*100]; current=sum(powers)/volts; ratings=[3,5,10,13,15,20]; selected=next((x for x in ratings if x>current),25)
        return item('Household electricity',f'Appliances rated {powers} W operate simultaneously on a {volts} V supply. Find their total current. Select the smallest suitable fuse from 3 A, 5 A, 10 A, 13 A, 15 A, 20 A, 25 A, taking a rating strictly above normal current. State which wire contains it.',f'Ptotal={sum(powers)} W; I=P/V={current:.2f} A. Select {selected} A under the stated rule. The fuse must be in the live wire so that melting disconnects the appliance from the live supply.',4)
    add('Fuse choice with supplied ratings',fuse)
    def joule(v):
        r=rng('joule',v); current=r.randint(2,12)/2; resistance=r.randint(2,30); seconds=r.randrange(30,301,15); heat=current**2*resistance*seconds
        return numeric_mcq(item('Heating effect of current',f'A current of {current} A passes through {resistance} Ω for {seconds} s. Calculate the heat produced and the heat produced if the current is doubled for the same time.',f'H=I²Rt={N(heat)} J. At double current, heat is four times as large: {N(4*heat)} J.'),heat,' J',f'Find I²Rt for I={current} A, R={resistance} Ω, t={seconds} s.')
    add('Joule heating and squared current',joule)
    def induction(v):
        r=rng('induction',v); initial=r.randint(1,9); final=initial+r.randint(1,8); turns=r.randint(20,120); changes=r.sample(['double the turns','reverse the magnet motion','keep the magnet stationary','move the magnet faster'],2)
        answers={'double the turns':'For the same flux change per turn, the induced emf increases.','reverse the magnet motion':'The direction of induced current reverses.','keep the magnet stationary':'No flux change occurs, so no induced emf is produced.','move the magnet faster':'A larger rate of change of magnetic flux produces a larger induced emf.'}
        return item('Electromagnetism',f'A {turns}-turn coil gives a deflection while a bar magnet approaches it. In one trial speed rises from {initial} to {final} cm/s. Predict the effect on induced emf. Explain the effect of each further change: (a) {changes[0]}; (b) {changes[1]}.',f'Faster approach increases the rate of flux change and induced emf. (a) {answers[changes[0]]} (b) {answers[changes[1]]}',4)
    add('Electromagnetic induction scenarios',induction)
    def emf_direction(v):
        r=rng('motor',v); machine=r.choice(['motor','generator']); cur=r.randint(1,20); pole=r.choice(['N above and S below','N to the left and S to the right']); changes=r.sample(['reverse current only','interchange the magnetic poles only','reverse current and interchange poles'],2)
        answer={'reverse current only':'The force reverses.','interchange the magnetic poles only':'The force reverses.','reverse current and interchange poles':'Both changes reverse their factors, so the force direction remains unchanged.'}
        return item('Electromagnetism',f'A straight current-carrying wire carries {cur} A in a magnetic field ({pole}). Explain the change in force direction if you (a) {changes[0]}, (b) {changes[1]}. Name the hand rule for the motor effect.',f'(a) {answer[changes[0]]} (b) {answer[changes[1]]} Use Fleming’s left-hand rule for force on a current-carrying conductor.')
    add('Motor effect reversals without a diagram',emf_direction)
    def heat(v):
        r=rng('heat',v); mass=r.randint(2,20)*50; c=r.choice([.4,.5,.9,2.1,4.2]); start=r.randint(10,40); end=start+r.randint(15,60); energy=mass*c*(end-start)
        return item('Calorimetry',f'A {mass} g sample with specific heat capacity {c} J g⁻¹ °C⁻¹ is heated from {start}°C to {end}°C without a change of state. Find heat supplied and the sample’s heat capacity.',f'Q=mcΔT={mass}×{c}×{end-start}={N(energy)} J. Heat capacity=mc={N(mass*c)} J/°C. Specific heat capacity is per unit mass, whereas heat capacity is for the entire sample.')
    add('Specific heat and heat capacity',heat)
    def mixing(v):
        r=rng('mix',v); hot=r.randint(60,95); cold=r.randint(10,30); mh=r.randint(1,6)*50; mc=r.randint(2,8)*50; final=(mh*hot+mc*cold)/(mh+mc)
        return item('Calorimetry',f'{mh} g of water at {hot}°C is mixed with {mc} g of water at {cold}°C in an insulated container of negligible heat capacity. Find the final temperature. State the heat-balance equation.',f'Heat lost=heat gained: {mh}c({hot}−T)={mc}c(T−{cold}). T=({mh}×{hot}+{mc}×{cold})/{mh+mc}={final:.2f}°C. The result lies between the starting temperatures.',4)
    add('Water mixture heat balance',mixing)
    def unknown_c(v):
        r=rng('unknownc',v); water=r.randint(1,5)*100; metal=r.randint(1,6)*100; cold=r.randint(10,25); final=cold+r.randint(2,8); hot=r.randint(70,100); c=water*4.2*(final-cold)/(metal*(hot-final))
        return item('Calorimetry',f'A {metal} g metal block at {hot}°C is put in {water} g water at {cold}°C. The final temperature is {final}°C. Ignore the vessel and heat loss. Find the metal’s specific heat capacity; cwater=4.2 J g⁻¹ °C⁻¹.',f'{metal}c({hot}−{final})={water}×4.2×({final}−{cold}). c={c:.3f} J g⁻¹ °C⁻¹. Use the metal’s cooling interval, not its original temperature.',4)
    add('Recover specific heat capacity',unknown_c)
    def melt(v):
        r=rng('melt',v); ice=r.randint(1,15)*10; final=r.randint(5,35); energy=ice*336+ice*4.2*final
        return item('Change of state',f'{ice} g ice at 0°C is completely melted and the water is then warmed to {final}°C. Calculate total heat required. Use Lfusion=336 J/g and cwater=4.2 J g⁻¹ °C⁻¹.',f'Melting heat=mL={ice*336} J; warming heat=mcΔT={N(ice*4.2*final)} J. Total={N(energy)} J. Do not assign a temperature increase to the melting stage.')
    add('Latent heat followed by warming',melt)
    def cooling(v):
        r=rng('cooling',v); mass=r.randint(1,10)*100; c=r.choice([.4,.9,2.1,4.2]); delta=r.randint(10,60); power=r.randint(2,20)*20; seconds=mass*c*delta/power
        return item('Calorimetry',f'A heater supplies {power} W entirely to {mass} g material of specific heat {c} J g⁻¹ °C⁻¹. How long does a temperature rise of {delta}°C take, if no phase change occurs?',f'Q=mcΔT={N(mass*c*delta)} J. Since P=Q/t, t=Q/P={seconds:.2f} s. Watt is joule per second.')
    add('Electrical heating time',cooling)
    def radiation(v):
        r=rng('nuclear',v); z=r.randint(20,90); a=2*z+r.randint(5,50); alpha=r.randint(1,3); beta=r.randint(1,4); az=a-4*alpha; zz=z-2*alpha+beta
        return item('Radioactivity',f'A nucleus has mass number {a} and atomic number {z}. It emits {alpha} alpha particle(s) and then {beta} beta-minus particle(s). Find the final mass and atomic numbers and explain whether a following gamma emission changes either.',f'Each α reduces A by 4 and Z by 2; each β⁻ leaves A unchanged and increases Z by 1. Final A={az}; Z={zz}. Gamma emission changes neither A nor Z.')
    add('Nuclear emission bookkeeping',radiation)
    def nuclear_safety(v):
        r=rng('safety',v); a=r.randint(15,150); source=r.choice(['alpha','beta','gamma']); layer=r.choice(['paper','thin aluminium','thick lead or concrete']); identity={'alpha':'strong ionisation, low penetration; especially hazardous if inhaled or ingested','beta':'moderate penetration; can be stopped by suitable aluminium shielding','gamma':'high penetration; needs substantial lead or concrete shielding'}
        return item('Radioactivity',f'A labelled {source}-emitting sealed source is handled remotely from {a} cm away in a school demonstration. State its ionising/penetrating character, recommend a suitable shield, and explain why increasing distance and reducing exposure time help.',f'{source.capitalize()}: {identity[source]}. Use '+{'alpha':'paper or an appropriate sealed enclosure','beta':'appropriate aluminium shielding','gamma':'thick lead/concrete shielding'}[source]+'. Distance reduces received intensity; shorter exposure reduces accumulated dose. Never handle or open the source directly.',4)
    # Only finite source names are used; distance supplies a genuine safety scenario.
    add('Radiation properties and safe handling',nuclear_safety)
    # Challenge questions test interpretation, inverse reasoning and assumptions.
    def h_parallel(v):
        r=rng('hparallel',v); a=r.randint(3,20); b=r.randint(3,20); volts=r.randint(6,30); req=F(a*b,a+b)
        return item('Current electricity',f'A student claims that replacing series resistors {a} Ω and {b} Ω with a parallel connection across the SAME ideal {volts} V battery reduces current because “current divides”. Calculate total current in both cases and evaluate the claim.',f'Series current={volts/(a+b):.3f} A. Parallel current=V(1/R1+1/R2)={volts/a+volts/b:.3f} A. Current divides between branches, but total current increases because equivalent resistance falls from {a+b} to {N(req)} Ω.',4)
    add('Twist: total versus branch current',h_parallel,True)
    def h_lens(v):
        q=lens(v+400,1);q['prompt']+=' A student rejects a negative image distance as impossible. Evaluate the objection.';q['answer']+=' A negative v is valid: it indicates a virtual image on the object side.';return q
    add('Twist: meaningful negative lens result',h_lens,True)
    def h_ice(v):
        r=rng('hice',v); water=r.randint(1,4)*100; temp=r.randint(10,30); ice=r.randint(3,8)*100; q=water*4.2*temp; melted=q/336
        return item('Calorimetry',f'{water} g water at {temp}°C is mixed with {ice} g ice at 0°C in an insulated vessel. With cwater=4.2 J g⁻¹ °C⁻¹ and L=336 J/g, determine whether all the ice melts, the final temperature, and the mass of ice remaining.',f'Water cooling to 0°C supplies {N(q)} J. This melts {melted:.2f} g, less than {ice} g. Ice remains, so equilibrium temperature is 0°C. Remaining ice={ice-melted:.2f} g. Do not use a liquid-only average-temperature formula.',4)
    add('Twist: incomplete melting',h_ice,True)
    def h_rating(v):
        q=rating(v+400);q['prompt']+=' Explain why doubling voltage does not merely double power under the stated assumption.';q['answer']+=' Since P=V²/R and R is fixed, doubling voltage multiplies power by four.';return q
    add('Twist: squared-voltage dependence',h_rating,True)
    def h_energy(v):
        r=rng('heff',v); mass=r.randint(10,80); h=r.randint(3,25); t=r.randint(6,40); eta=r.choice([40,50,60,75,80]); output=mass*10*h/t; inp=output*100/eta
        return item('Work, energy and power',f'A motor consuming electrical power raises {mass} kg through {h} m in {t} s. Its efficiency is {eta}%. Find the minimum electrical input power. A student divides the output by {eta}; identify the unit error.',f'Useful output=mgh/t={output:.3f} W. Fractional efficiency={eta/100}. Input=output/({eta}/100)={inp:.3f} W. Efficiency percent must be converted to a fraction before dividing.',4)
    add('Twist: input versus useful power',h_energy,True)
    def h_wave(v):
        r=rng('hvoice',v); freq=r.randrange(150,600,10); amp=r.randint(2,8); speed=r.choice([320,330,340]); other=speed*4
        return item('Sound',f'A tuning fork of frequency {freq} Hz sends a wave from air (speed {speed} m/s) into water (speed {other} m/s). A pupil says both pitch and wavelength become four times as large. Correct both statements and calculate both wavelengths.',f'Frequency and therefore pitch remain unchanged at the boundary. λair={speed/freq:.3f} m; λwater={other/freq:.3f} m. Wavelength alone becomes four times as large.',4)
    add('Twist: frequency at a boundary',h_wave,True)
    def h_moment(v):
        q=beam(v+400);q['prompt']+=' Now a downward {0} N beam weight acts exactly through the pivot. State what changes and what does not.'.format(20+v);q['answer']+=' The added weight has no moment about the pivot, so the balancing force is unchanged; the upward reaction increases by '+str(20+v)+' N.';return q
    add('Twist: force through a pivot',h_moment,True)
    def h_alpha(v):
        q=radiation(v+400);q['prompt']+=' A pupil concludes that unchanged mass number after beta emission means no change of element. Explain the mistake.';q['answer']+=' Element identity is set by atomic number, which changes during beta-minus emission.';return q
    add('Twist: element identity in beta decay',h_alpha,True)
    def h_fuse(v):
        q=fuse(v+400);q['prompt']+=' Explain why putting the fuse in the neutral wire can leave a hazard even after it melts.';q['answer']+=' The appliance may remain connected to the live conductor even when the neutral path opens.';return q
    add('Twist: fuse placement versus rating',h_fuse,True)
    def h_balance(v):
        q=mixing(v+400);q['prompt']+=' Would a real vessel initially at the colder temperature make the final temperature higher or lower than your ideal result? Give a reason.';q['answer']+=' Lower: the vessel also gains heat, so less is available to warm the colder water.';return q
    add('Twist: neglected calorimeter capacity',h_balance,True)
    return variant_bank('phy',families,hard)
