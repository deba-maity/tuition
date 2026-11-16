import math
from fractions import Fraction as F
from .common import item, num as N, rng, variant_bank, numeric_mcq

GASES=[('H₂',2,'hydrogen','a lighted splint gives a pop'),('O₂',32,'oxygen','a glowing splint rekindles'),('CO₂',44,'carbon dioxide','limewater turns milky'),('NH₃',17,'ammonia','damp red litmus turns blue'),('HCl',36.5,'hydrogen chloride','damp blue litmus turns red; dense white fumes with ammonia'),('SO₂',64,'sulphur dioxide','acidified potassium dichromate changes from orange to green'),('N₂',28,'nitrogen','no support for ordinary combustion')]
SALTS=[('Cu²⁺','pale blue precipitate','insoluble in excess NaOH','deep-blue solution in excess NH₄OH','Cu(OH)₂'),('Fe²⁺','dirty green precipitate','insoluble in excess NaOH','insoluble in excess NH₄OH','Fe(OH)₂'),('Fe³⁺','reddish-brown precipitate','insoluble in excess NaOH','insoluble in excess NH₄OH','Fe(OH)₃'),('Zn²⁺','white gelatinous precipitate','soluble in excess NaOH','soluble in excess NH₄OH','Zn(OH)₂'),('Pb²⁺','white precipitate','soluble in excess NaOH','insoluble in excess NH₄OH','Pb(OH)₂'),('Ca²⁺','white precipitate with sufficient NaOH','insoluble in excess NaOH','no precipitate with ordinary NH₄OH','Ca(OH)₂')]

def make_bank():
    fs=[]; hard=[]
    def add(name,fn,h=False):(hard if h else fs).append((name,fn))
    def mole(v,kind=0):
        r=rng('mole'+str(kind),v); symbol,mass,name,test=r.choice(GASES); n=r.randint(2,120)/20; grams=n*mass; volume=n*22.4; molecules=n*6.022e23
        if kind==0: prompt=f'A sample contains {N(grams)} g of {name}, {symbol}. Its molar mass is {mass} g/mol. Find its amount in moles and volume at STP. Use molar volume 22.4 L/mol.'
        elif kind==1:prompt=f'{N(volume)} L of {name} is measured at STP. Find its number of moles and mass. Use molar mass {mass} g/mol and molar volume 22.4 L/mol.'
        else:prompt=f'A sample contains {n:.2f} mol of {name}. Find the number of molecules and mass. Use NA=6.022×10²³ mol⁻¹ and molar mass {mass} g/mol.'
        return numeric_mcq(item('Mole concept',prompt,f'n=m/M=V/22.4={N(n)} mol. Mass={N(grams)} g; STP volume={N(volume)} L; number of molecules=nNA={molecules:.4e}.',3),n,' mol',f'Find moles in {N(grams)} g of {name}, molar mass {mass} g/mol.')
    for i,n in enumerate(['Mass to moles and gas volume','STP volume to mass','Molecules and amount']):add(n,lambda v,i=i:mole(v,i))
    def equalvolume(v):
        r=rng('equalvol',v); a,b=r.sample(GASES,2); vol=r.randint(2,120)*.56; moles=vol/22.4
        return item('Mole concept',f'Equal volumes ({N(vol)} L each) of {a[2]} and {b[2]} are measured at the same STP conditions. Compare their numbers of molecules and calculate their masses. Molar masses: {a[1]} and {b[1]} g/mol.',f'By Avogadro’s law equal volumes at the same temperature and pressure contain equal numbers of molecules. Each contains {N(moles)} mol. Masses={N(moles*a[1])} g and {N(moles*b[1])} g. Equal volume does not imply equal mass.',4)
    add('Avogadro equal-volume comparison',equalvolume)
    def vd(v):
        r=rng('vd',v); gas=r.choice(GASES); amount=r.randint(2,100)/10
        return item('Mole concept',f'A gas sample has mass {N(amount*gas[1])} g and occupies {N(amount*22.4)} L at STP. Determine its relative molecular mass and vapour density relative to hydrogen.',f'Moles=V/22.4={N(amount)}. Relative molecular mass=m/n={gas[1]}. Vapour density=M/2={gas[1]/2}.')
    add('Gas molar mass and vapour density',vd)
    def empirical(v):
        r=rng('emp',v); a,b=r.choice([(1,2),(2,3),(1,1),(3,2)]); factor=r.randint(2,8); molmass=(12*a+16*b)*factor; sample=r.randint(2,20); total=12*a+16*b
        return item('Empirical and molecular formula',f'A carbon-oxygen compound contains {12*a/total*100:.4f}% carbon and the remainder oxygen. Relative molecular mass is {molmass}. Find its empirical and molecular formula. Use C=12, O=16; allow rounding of the percentages.',f'Mole ratio C:O=({12*a/total*100:.4f}/12):({16*b/total*100:.4f}/16)={a}:{b}. Empirical formula=C{a if a>1 else ""}O{b if b>1 else ""}; empirical mass={total}. Factor={molmass}/{total}={factor}; molecular formula=C{a*factor}O{b*factor}.',4)
    # Percent/mass factor gives a finite formula domain; include an analysis mass
    # and ask actual element masses to create additional substantive data.
    def empirical_mass(v):
        r=rng('emass',v); pairs=[(1,2),(2,3),(1,1),(3,2)]; a,b=r.choice(pairs); k=r.randint(2,80)/10; factor=r.randint(1,6); total=12*a+16*b
        return item('Empirical and molecular formula',f'Analysis of {N(k*total)} g of a C/O compound gives {N(k*12*a)} g carbon and {N(k*16*b)} g oxygen. Its relative molecular mass is {factor*total}. Find empirical and molecular formulae. C=12, O=16.',f'Moles C={N(k*a)}, O={N(k*b)}. Divide by {N(k)}: C:O={a}:{b}. Empirical formula C{a if a>1 else ""}O{b if b>1 else ""}, mass {total}. Molecular multiplier={factor}; formula C{a*factor}O{b*factor}.',4)
    add('Element analysis to formula',empirical_mass)
    def combustion(v):
        r=rng('combust',v); c=r.randint(1,5); h=2*c+2; mol=r.randint(1,30)/10; oxygen=(c+h/4)*mol; dioxide=c*mol; water=h/2*mol
        return item('Chemical calculations',f'{N(mol)} mol of alkane C{c}H{h} burns completely. Write a balanced combustion equation and calculate moles of oxygen used, carbon dioxide formed and water formed.',f'C{c}H{h} + {N(c+h/4)}O₂ → {c}CO₂ + {h//2}H₂O (multiply every coefficient by 2 if whole-number coefficients are required). O₂={N(oxygen)} mol; CO₂={N(dioxide)} mol; H₂O={N(water)} mol.',4)
    add('Alkane combustion stoichiometry',combustion)
    def carbonate(v):
        r=rng('carbonate',v); mass=r.randint(2,80)*5; n=mass/100; vol=n*22.4
        return numeric_mcq(item('Chemical calculations',f'{mass} g pure CaCO₃ is heated until decomposition is complete. Write the equation, calculate the CaO mass and CO₂ volume at STP, and state a confirmatory test for the gas. Ca=40, C=12, O=16.',f'CaCO₃ → CaO + CO₂. Molar masses 100, 56 and 44. CaO={N(n*56)} g; CO₂={N(vol)} L at STP. CO₂ turns limewater milky (CaCO₃ precipitate).',4),vol,' L',f'{mass} g CaCO₃ decomposes completely. M(CaCO₃)=100 g/mol. Find CO₂ volume at STP, 22.4 L/mol.')
    add('Carbonate thermal decomposition',carbonate)
    def zincacid(v):
        r=rng('zincacid',v); mass=r.randint(1,70)*1.3; moles=mass/65
        return item('Hydrogen chloride and salts',f'{N(mass)} g zinc reacts completely with excess dilute HCl. Calculate the mass of ZnCl₂ and the hydrogen volume at STP. Include the equation and a gas test. Zn=65, Cl=35.5, H=1.',f'Zn+2HCl→ZnCl₂+H₂. Zn moles={N(moles)}; ZnCl₂ mass={N(moles*136)} g; H₂ volume={N(moles*22.4)} L. A lighted splint produces a pop.',4)
    add('Metal acid reaction and gas test',zincacid)
    def ammonia(v):
        r=rng('ammonia',v); mass=r.randint(2,75)*1.4; n=mass/28
        return item('Ammonia',f'In the reaction N₂+3H₂⇌2NH₃, {N(mass)} g N₂ is fully converted with excess H₂. Calculate the H₂ volume used at STP and NH₃ mass formed. State the industrial catalyst. N=14, H=1.',f'n(N₂)={N(n)} mol. H₂ required=3n={N(3*n)} mol={N(3*n*22.4)} L at STP. NH₃=2n mol, mass={N(2*n*17)} g. Haber catalyst: finely divided iron.',4)
    add('Haber reaction quantities',ammonia)
    def purity(v):
        r=rng('purity',v); sample=r.randint(5,40)*10; purity=r.choice([60,70,75,80,85,90,95]); pure=sample*purity/100; vol=pure/100*22.4
        return item('Chemical calculations',f'A {sample} g limestone sample contains {purity}% CaCO₃; the rest does not react with dilute HCl. Find the mass of CaCO₃ and CO₂ volume at STP when acid is in excess. M(CaCO₃)=100 g/mol.',f'CaCO₃ mass={sample}×{purity}/100={N(pure)} g. CaCO₃+2HCl→CaCl₂+H₂O+CO₂. CO₂ moles={N(pure/100)}; volume={N(vol)} L.',4)
    add('Purity in carbonate stoichiometry',purity)
    def acidbase(v):
        r=rng('acidbase',v); mol=r.randint(1,40)/10; which=r.choice(['NaOH','Ca(OH)₂']); ratio=1 if which=='NaOH' else 2; mm=40 if which=='NaOH' else 74
        return item('Acids, bases and salts',f'{N(mol*mm)} g {which} is exactly neutralised by HCl. Write the balanced equation, calculate HCl mass needed and name the type of reaction. Na=23, Ca=40, O=16, H=1, Cl=35.5.',f'{which}+'+('HCl→NaCl+H₂O' if ratio==1 else '2HCl→CaCl₂+2H₂O')+f'. Base moles={N(mol)}; HCl moles={N(mol*ratio)}; HCl mass={N(mol*ratio*36.5)} g. This is neutralisation.',4)
    add('Neutralisation with one or two OH groups',acidbase)
    def hydrate(v):
        r=rng('hydrate',v); n=r.randint(1,150)/10
        return item('Water of crystallisation',f'A sample of hydrated copper sulphate loses {N(90*n)} g water and leaves {N(160*n)} g anhydrous CuSO₄ on heating. Find x in CuSO₄·xH₂O and describe the colour change. Cu=64, S=32, O=16, H=1.',f'Moles CuSO₄={N(n)}; water={N(5*n)} mol. Ratio=1:5, so x=5. Blue hydrated crystals become white anhydrous copper sulphate; adding water restores blue.',4)
    add('Water of crystallisation formula',hydrate)
    def volume_ratio(v):
        r=rng('volratio',v); gas=r.choice(['hydrogen','ammonia','carbon monoxide']); volume=r.randint(2,120)/2
        if gas=='hydrogen':eq='2H₂+O₂→2H₂O(g)';react=volume/2;product=volume
        elif gas=='ammonia':eq='4NH₃+3O₂→2N₂+6H₂O(g)';react=volume*.75;product=volume*.5
        else:eq='2CO+O₂→2CO₂';react=volume*.5;product=volume
        pname='steam' if gas=='hydrogen' else ('nitrogen' if gas=='ammonia' else 'carbon dioxide')
        return item('Gas volume calculations',f'{N(volume)} L {gas} reacts according to {eq}. All gas volumes are compared at the same temperature and pressure. Find oxygen volume required and volume of {pname} formed.',f'Gas volumes follow equation coefficients at common temperature and pressure. Oxygen={N(react)} L; {pname}={N(product)} L. Products listed as gases remain gaseous for this comparison.')
    add('Gay-Lussac volume coefficients',volume_ratio)
    def shells(v):
        r=rng('shells',v); z=r.choice([3,4,5,6,7,8,9,11,12,13,14,15,16,17,19,20]); shells=([2,z-2] if z<=10 else [2,8,z-10] if z<=18 else [2,8,8,z-18]); outer=shells[-1]; val=outer if outer<=4 else 8-outer; other=r.randint(1,50)
        return item('Periodic table',f'An atom X has atomic number {z} and mass number {z+other}. Write its shell configuration, identify its period, give valence electrons and predict its usual valency. Does changing its mass number alone change its group?',f'Shells={shells}. Period={len(shells)}; valence electrons={outer}; usual valency={val}. Mass number alone does not change electron configuration or group; isotopes have the same atomic number.',4)
    add('Electronic configuration and position',shells)
    def pair_periodic(v):
        r=rng('pairperiod',v); period=r.choice([2,3]); pairs=[(1,7),(1,2),(2,6),(3,7),(4,7)]; x,y=r.choice(pairs); zbase=2 if period==2 else 10; isotope=r.randint(1,40)
        return item('Periodic table',f'Atoms X and Y are in period {period}, with {x} and {y} valence electrons respectively. X has mass number {zbase+x+isotope}. Compare their metallic character, atomic size and electronegativity. Justify each trend across a period.',f'X is to the left of Y. Across a period effective nuclear attraction generally rises: atomic size decreases, electronegativity increases and metallic character decreases. Thus X is generally larger and more metallic, Y more electronegative. The supplied mass number does not reverse periodic position.',4)
    add('Across-period comparison',pair_periodic)
    def isotopeions(v):
        r=rng('ions',v); z=r.choice([11,12,13,17,19,20]); charge={11:1,12:2,13:3,17:-1,19:1,20:2}[z]; a=z+r.randint(z,z+20); elec=z-charge
        return numeric_mcq(item('Chemical bonding',f'X has atomic number {z}, mass number {a}, and forms an ion with charge {charge:+}. Find protons, neutrons and electrons in the ion. Explain whether ion formation changes the nucleus.',f'p={z}; n={a-z}; electrons=Z−charge={elec}. Forming the ion changes electrons only, not protons or neutrons.'),elec,' electrons',f'An ion has atomic number {z}, mass number {a}, and charge {charge:+}. How many electrons does it have?')
    add('Subatomic particles in ions',isotopeions)
    def ionic(v):
        r=rng('ionic',v); c,cv,cname=r.choice([('Na',1,'sodium'),('Mg',2,'magnesium'),('Al',3,'aluminium'),('Ca',2,'calcium')]); a,av,aname=r.choice([('Cl',1,'chlorine'),('O',2,'oxygen'),('S',2,'sulphur')]); g=math.gcd(cv,av); cn=av//g; an=cv//g; formula=c+(str(cn) if cn>1 else '')+a+(str(an) if an>1 else ''); amount=r.randint(1,60)/10
        return item('Chemical bonding',f'{cname.capitalize()} forms {cv}+ ions and {aname} forms {av}− ions. Derive the formula of their ionic compound and calculate moles of each ion in {N(amount)} mol of the compound. Explain why the solid does not conduct electricity.',f'Charge balance gives {formula}. Ion amounts: {cname}={N(amount*cn)} mol; {aname}={N(amount*an)} mol. Ions are fixed in the solid lattice and cannot move freely; in molten/aqueous form mobile ions can conduct.',4)
    add('Ionic formula and ion ratio',ionic)
    def covalent(v):
        r=rng('covalent',v); form,shared,lone,shape=r.choice([('H₂O',2,2,'bent'),('NH₃',3,1,'pyramidal'),('CH₄',4,0,'tetrahedral'),('HCl',1,3,'a diatomic molecule')]); count=r.randint(2,70)/10
        return item('Chemical bonding',f'Consider {N(count)} mol of {form}. State the number of shared electron pairs in one molecule and lone pairs on its O/N/C/Cl atom as appropriate. Explain the covalent bond in terms of electron sharing. How many moles of shared pairs are represented?',f'One molecule has {shared} shared pairs and {lone} lone pairs on the stated non-hydrogen central/bonded atom. A shared pair is attracted to both bonded nuclei. Shared-pair amount={N(count*shared)} mol. This is sharing, not complete electron transfer.',4)
    add('Covalent shared and lone pairs',covalent)
    def conduct(v):
        r=rng('conduct',v); volts=r.randint(2,15); volume=r.randint(20,250); sample=r.choice(['solid NaCl','molten NaCl','aqueous glucose','dilute HCl','aqueous NaCl'])
        answers={'solid NaCl':'It does not conduct: its ions are fixed in the lattice.','molten NaCl':'It conducts: its ions are mobile.','aqueous glucose':'It does not conduct appreciably: glucose dissolves as molecules, not ions.','dilute HCl':'It conducts: ionisation gives mobile ions.','aqueous NaCl':'It conducts: dissolved ions are mobile.'}
        return item('Electrolytes and bonding',f'A {volts} V test circuit is connected to a cell containing {volume} cm³ of {sample}. Predict whether it conducts and explain the charge carriers. Why is merely dissolving a substance insufficient to guarantee conduction?',answers[sample]+' Conduction requires mobile charged particles; a molecular solute can dissolve without producing ions.')
    add('Conductivity with stated physical state',conduct)
    def hydroxide(v):
        r=rng('hydroxide',v); ion,colour,na,nh,formula=r.choice(SALTS); sample=r.randint(1,80)/10; excess=r.choice(['NaOH','NH₄OH'])
        return item('Analytical chemistry',f'A {sample:.1f} cm³ sample containing {ion} ions is tested by adding {excess} dropwise, then in excess. Describe the observations, name/formulate the precipitate, and explain why “white precipitate” alone is not a unique identification.',f'Precipitate: {colour}; formula {formula}. In excess: '+(na if excess=='NaOH' else nh)+'. More than one cation can form a white precipitate; excess-reagent behaviour and a second test are required.',4)
    add('Hydroxide precipitation and excess',hydroxide)
    def distinguish(v):
        r=rng('distinguish',v); first,second=r.sample(SALTS,2); quantity=r.randint(2,100)
        return item('Analytical chemistry',f'Two labelled {quantity} cm³ solutions contain {first[0]} and {second[0]} respectively. Give a stepwise NaOH/NH₄OH test to distinguish them. State observations separately for both and include the excess-reagent result where useful.',f'{first[0]}: {first[1]}, {first[2]}, {first[3]}. {second[0]}: {second[1]}, {second[2]}, {second[3]}. Test separate small portions and compare the full pattern, not just the presence of a precipitate.',4)
    add('Distinguish cations by observation pattern',distinguish)
    def ammonium(v):
        r=rng('ammonium',v); mass=r.randint(1,70)*.535; n=mass/53.5
        return item('Analytical chemistry',f'{N(mass)} g NH₄Cl is warmed with excess NaOH. Identify the gas by two observations, give the equation, and calculate its volume at STP. NH₄Cl=53.5 g/mol.',f'NH₄Cl+NaOH→NaCl+NH₃+H₂O. Ammonia has a pungent smell and turns damp red litmus blue; with HCl it gives dense white fumes. n={N(n)} mol; V={N(n*22.4)} L at STP. Do not deliberately inhale the gas.',4)
    add('Ammonium salt test and quantity',ammonium)
    def acidgas(v):
        r=rng('acidgas',v); case=r.choice([('sodium carbonate','Na₂CO₃',106,'CO₂','Na₂CO₃+2HCl→2NaCl+H₂O+CO₂','turns limewater milky'),('sodium sulphite','Na₂SO₃',126,'SO₂','Na₂SO₃+2HCl→2NaCl+H₂O+SO₂','turns acidified dichromate orange to green'),('iron sulphide','FeS',88,'H₂S','FeS+2HCl→FeCl₂+H₂S','blackens moist lead acetate paper')]); mass=r.randint(1,60)*case[2]/20; n=mass/case[2]
        return item('Acids, bases and salts',f'{N(mass)} g {case[0]} reacts completely with excess dilute HCl. Identify the evolved gas, give a confirmatory test and balanced equation, and calculate STP gas volume. M({case[1]})={case[2]} g/mol.',f'Gas={case[3]}; test: {case[5]}. {case[4]}. One mole salt gives one mole gas: n={N(n)}; V={N(n*22.4)} L.',4)
    add('Acid reaction: gas identification and volume',acidgas)
    def electrolysis(v,kind=0):
        r=rng('electrolysis'+str(kind),v); volume=r.randint(10,200)*2
        if kind==0:return item('Electrolysis',f'Acidulated water is electrolysed with inert electrodes. {volume} cm³ hydrogen is collected at one electrode. Name both electrode products, calculate oxygen volume at the same conditions, write a cathode equation and explain why acid is added.',f'Cathode H₂; anode O₂. H₂:O₂=2:1, so oxygen={volume//2} cm³. Cathode: 2H⁺+2e⁻→H₂. Dilute sulphuric acid supplies ions and improves conductivity; it is not the intended decomposition product.',5)
        if kind==1:return item('Electrolysis',f'A cell contains {volume} cm³ aqueous CuSO₄ and pure copper electrodes. State changes at both electrodes, write both electrode equations and explain whether the blue colour should fade substantially during ideal operation.',f'Anode copper dissolves: Cu→Cu²⁺+2e⁻. Cathode copper deposits: Cu²⁺+2e⁻→Cu. Copper ions used at the cathode are replenished at the anode, so blue colour remains approximately constant.',4)
        if kind==2:return item('Electrolysis',f'{volume} cm³ aqueous copper sulphate is electrolysed using platinum electrodes. State both products, the expected colour change and why the answer differs from copper-electrode electrolysis.',f'Cathode: Cu²⁺+2e⁻→Cu. Anode: oxygen from water/OH⁻ discharge, not copper dissolution. Blue colour fades as Cu²⁺ is removed without replacement. Platinum is inert.',4)
        return item('Electrolysis',f'A cell contains {volume} g lead bromide, first solid and then molten. Explain the conductivity change; state both products of electrolysis and write the electrode half-equations.',f'The solid has immobile ions; melting allows ions to move. Cathode: Pb²⁺+2e⁻→Pb. Anode: 2Br⁻→Br₂+2e⁻. Products are lead and bromine.',4)
    for k,name in enumerate(['Acidulated-water electrolysis','Copper electrodes in copper sulphate','Inert electrodes in copper sulphate','Molten lead bromide']):add(name,lambda v,k=k:electrolysis(v,k))
    def metal(v):
        r=rng('aluminium',v); mass=r.randint(1,80)*5.1; n=mass/102
        return item('Metallurgy',f'{N(mass)} g pure Al₂O₃ is completely electrolysed in the Hall-Héroult process. Calculate the theoretical aluminium mass. State the purpose of cryolite and why carbon anodes need replacement. Al=27, O=16.',f'One mole Al₂O₃ (102 g) supplies two mol Al (54 g). Aluminium mass={N(n*54)} g. Cryolite lowers the working melting temperature and improves conductivity of the bath. Oxygen formed at the anode reacts with carbon, consuming the anode.',4)
    add('Aluminium extraction calculation and roles',metal)
    def refining(v):
        r=rng('refine',v); mass=r.randint(10,90)*10; purity=r.choice([95,96,97,98,99]); copper=mass*purity/100
        return item('Metallurgy',f'A {mass} g impure copper anode contains {purity}% copper. In electrolytic refining identify the anode, cathode and electrolyte, give the copper half-reactions, and find the maximum copper mass supplied by that anode if all its copper is transferred.',f'Anode: impure copper; cathode: thin pure copper; electrolyte: acidified CuSO₄. Anode Cu→Cu²⁺+2e⁻; cathode Cu²⁺+2e⁻→Cu. Maximum transferable copper={N(copper)} g; suitable insoluble impurities form anode mud.',4)
    add('Copper refining setup and yield',refining)
    def hcl(v):
        r=rng('hclprep',v); mass=r.randint(1,80)*5.85; n=mass/58.5
        return item('Hydrogen chloride',f'NaCl is treated with concentrated H₂SO₄ below 200°C to prepare HCl. For {N(mass)} g NaCl, write the laboratory equation and find the theoretical HCl mass. Explain why the gas is not collected over water. NaCl=58.5, HCl=36.5 g/mol.',f'NaCl+H₂SO₄→NaHSO₄+HCl. n(NaCl)={N(n)}; HCl mass={N(n*36.5)} g. HCl is extremely soluble in water, so water collection would absorb it.',4)
    add('HCl preparation: condition and solubility',hcl)
    def ammonia_lab(v):
        r=rng('nh3lab',v); mass=r.randint(1,80)*5.35; n=mass/53.5
        return item('Ammonia',f'{N(mass)} g NH₄Cl is heated with excess Ca(OH)₂. Give the equation, calculate NH₃ mass and explain the choice of a drying agent. NH₄Cl=53.5, NH₃=17 g/mol.',f'2NH₄Cl+Ca(OH)₂→CaCl₂+2NH₃+2H₂O. NH₃ moles={N(n)}; mass={N(n*17)} g. Dry with quicklime (CaO); concentrated H₂SO₄ would react with ammonia and anhydrous CaCl₂ absorbs it.',4)
    add('Laboratory ammonia and drying',ammonia_lab)
    def nitric(v):
        r=rng('nitric',v); mass=r.randint(1,70)*6.4; n=mass/64; conc=r.choice([True,False])
        eq='Cu+4HNO₃→Cu(NO₃)₂+2NO₂+2H₂O' if conc else '3Cu+8HNO₃→3Cu(NO₃)₂+2NO+4H₂O'; gas=n*(2 if conc else F(2,3))
        return item('Nitric acid',f'{N(mass)} g copper reacts with excess '+('concentrated' if conc else 'dilute')+' nitric acid. Write the equation, identify the main nitrogen oxide, describe its appearance and calculate its amount in moles. Cu=64 g/mol.',f'{eq}. Copper moles={N(n)}; gas moles={N(gas)}. '+('NO₂ is reddish-brown.' if conc else 'NO is colourless and turns brown in air as it forms NO₂.'),4)
    add('Nitric-acid concentration and product',nitric)
    def sulphuric(v):
        r=rng('sulphuric',v); mass=r.randint(1,65)*6.4; n=mass/64
        return item('Sulphuric acid',f'{N(mass)} g copper is heated with excess concentrated H₂SO₄. Give the balanced equation, state the acid’s role, identify the gas by a chemical test and calculate its mass. Cu=64, SO₂=64 g/mol.',f'Cu+2H₂SO₄→CuSO₄+SO₂+2H₂O. Concentrated hot sulphuric acid acts as an oxidising agent. SO₂ changes acidified dichromate orange to green. Gas moles={N(n)}; mass={N(n*64)} g.',4)
    add('Hot concentrated sulphuric acid as oxidant',sulphuric)
    def alkane(v):
        r=rng('alkane',v); n=r.randint(1,5); mol=r.randint(2,100)/10; molmass=14*n+2
        return item('Organic chemistry',f'A saturated acyclic hydrocarbon contains {n} carbon atom(s) per molecule. Write its molecular formula, name the homologous series and calculate the mass of {N(mol)} mol. C=12, H=1. State the change in formula between successive members.',f'General formula CnH2n+2 gives C{n if n>1 else ""}H{2*n+2}. Series: alkanes. M={molmass} g/mol; mass={N(mol*molmass)} g. Successive members differ by CH₂ (14 u).')
    add('Alkane formula and homologous difference',alkane)
    def unsaturation(v):
        r=rng('unsat',v); carbon=r.randint(2,5); triple=r.choice([True,False]); hydrogen=2*carbon-2 if triple else 2*carbon; mol=r.randint(1,70)/10
        return item('Organic chemistry',f'A hydrocarbon is an acyclic '+('alkyne with one triple bond' if triple else 'alkene with one double bond')+f' and has {carbon} carbon atoms. Write its formula, calculate the H₂ moles needed to fully hydrogenate {N(mol)} mol, and name a suitable catalyst.',f'Formula C{carbon}H{hydrogen}. '+('Each triple bond takes 2 mol H₂ per mol' if triple else 'Each double bond takes 1 mol H₂ per mol')+f', so H₂ needed={N(mol*(2 if triple else 1))} mol. Use nickel under suitable heating conditions.',4)
    add('Unsaturation and hydrogenation',unsaturation)
    def ethanol(v):
        r=rng('ethanol',v); mass=r.randint(1,90)*2.3; n=mass/46
        return item('Organic chemistry',f'{N(mass)} g ethanol is dehydrated with concentrated H₂SO₄ at about 170°C. Write the product equation, find the gas volume at STP and state one chemical test that distinguishes the gas from ethane. Ethanol=46 g/mol.',f'C₂H₅OH→C₂H₄+H₂O. n={N(n)}; ethene volume={N(n*22.4)} L. Ethene decolourises bromine water by addition under ordinary test conditions; ethane does not without a substitution condition such as UV.',4)
    add('Ethanol dehydration and unsaturation test',ethanol)
    def ester(v):
        r=rng('ester',v); mass=r.randint(1,70)*3; n=mass/60
        return item('Organic chemistry',f'{mass} g ethanoic acid reacts completely with excess ethanol in esterification. Give the ester name, balanced equation, catalyst/condition and theoretical ester mass. Ethanoic acid=60, ester=88 g/mol.',f'CH₃COOH+C₂H₅OH⇌CH₃COOC₂H₅+H₂O. Ester: ethyl ethanoate. Warm with concentrated H₂SO₄ catalyst. Acid moles={N(n)}; theoretical ester mass={N(n*88)} g, assuming complete conversion as stated.',4)
    add('Esterification and theoretical product',ester)
    def oxidation(v):
        r=rng('oxidation',v); mass=r.randint(1,60)*2.3; n=mass/46
        return item('Organic chemistry',f'{N(mass)} g ethanol is completely oxidised to ethanoic acid. Name a suitable oxidising reagent, write the equation using [O], calculate the acid mass and name its functional group. Ethanol=46, ethanoic acid=60 g/mol.',f'C₂H₅OH+2[O]→CH₃COOH+H₂O. Use acidified potassium dichromate (or suitable acidified KMnO₄). Acid moles={N(n)}; mass={N(n*60)} g. Functional group: carboxyl, −COOH.',4)
    add('Alcohol to carboxylic acid',oxidation)
    # Additional mixed tasks develop observations and conditions rather than
    # introducing unlisted kinetics, thermodynamics or electrochemical formulae.
    def observations(v):
        r=rng('observation',v); sample=r.randint(10,150); gas=r.choice(GASES[:6])
        if gas[0]=='N₂':
            return item('Observation and inference',f'A {sample} cm³ gas sample is suspected to be nitrogen. A burning splint is extinguished. Explain why this observation alone does not identify nitrogen, and give its formula and relative molecular mass.', 'Other gases also fail to support ordinary combustion, so extinction alone does not confirm nitrogen. Nitrogen is N₂; relative molecular mass=28. Additional evidence is required.')
        return item('Observation and inference',f'You are given {sample} cm³ of a gas believed to be {gas[2]}. State the expected confirmatory test result and explain why a change in litmus alone is insufficient to distinguish every gas. Give its formula and relative molecular mass.',f'{gas[2].capitalize()}: {gas[3]}. Formula {gas[0]}, relative molecular mass {gas[1]}. Several acidic gases turn blue litmus red, so a more specific reaction/test is needed for identification.')
    add('Gas test: observation versus inference',observations)
    def oxide(v):
        r=rng('oxide',v); mass=r.randint(1,80)*4; n=mass/80
        return item('Acids, bases and salts',f'{mass} g CuO reacts completely with excess dilute H₂SO₄. Write the equation, describe the visible change and find the mass of anhydrous CuSO₄ formed. CuO=80 and CuSO₄=160 g/mol.',f'CuO+H₂SO₄→CuSO₄+H₂O. Black copper oxide dissolves to give a blue copper sulphate solution. n={N(n)}; salt mass={N(n*160)} g. CuO behaves as a basic oxide.',4)
    add('Basic oxide and acid',oxide)
    def precipitation(v):
        r=rng('precip',v); mass=r.randint(1,50)*2.34; n=mass/234
        return item('Preparation of salts',f'{N(mass)} g NaCl reacts with excess AgNO₃ solution. Write the molecular and ionic equations, describe the precipitate and calculate its mass. NaCl=58.5, AgCl=143.5 g/mol.',f'NaCl+AgNO₃→AgCl↓+NaNO₃; Ag⁺+Cl⁻→AgCl↓. White curdy precipitate of silver chloride. n(NaCl)={N(mass/58.5)}; AgCl mass={N(mass/58.5*143.5)} g.',4)
    add('Precipitation and ionic equation',precipitation)
    def sulphate_test(v):
        r=rng('sulphate',v); mass=r.randint(1,80)*7.1; n=mass/142
        return item('Preparation of salts',f'{N(mass)} g Na₂SO₄ reacts completely with excess BaCl₂. Write the equation, state the precipitate colour and calculate its mass. Explain the role of acidification in a confirmatory sulphate test. Na₂SO₄=142, BaSO₄=233 g/mol.',f'Na₂SO₄+BaCl₂→BaSO₄↓+2NaCl. White BaSO₄; n={N(n)}; mass={N(n*233)} g. Dilute HCl removes interference from carbonate/sulphite; BaSO₄ remains insoluble in dilute HCl.',4)
    add('Sulphate precipitate and interference',sulphate_test)
    def h_purity(v):
        r=rng('hpure',v); sample=r.randint(5,30)*10; percent=r.choice([60,70,75,80,90]); mass=sample*percent/100; volume=mass/100*22.4
        return item('Chemical calculations',f'{sample} g limestone yields {N(volume)} L CO₂ at STP on complete reaction with excess HCl. Find its CaCO₃ percentage purity. A pupil divides CO₂ mass directly by sample mass to report purity. Explain the mistake. CaCO₃=100, CO₂=44 g/mol.',f'n(CO₂)={N(volume)}/22.4={N(mass/100)}; same moles CaCO₃, mass={N(mass)} g. Purity={percent}%. CO₂ mass is not CaCO₃ mass; convert with the stoichiometric molar-mass ratio.',4)
    add('Twist: recover purity from gas',h_purity,True)
    def h_copper(v):
        q=electrolysis(v+500,1);q['prompt']+=' A student says the copper cathode gains mass because negative electrons are deposited as metal. Correct the explanation.';q['answer']+=' Copper ions gain electrons and become neutral copper atoms; electrons alone do not supply the metal mass.';return q
    add('Twist: ions versus electrons at a cathode',h_copper,True)
    def h_solution(v):
        q=conduct(v+500);q['prompt']+=' Distinguish ionisation from simple physical dissolution in your explanation.';q['answer']+=' Ionic dissociation separates pre-existing ions; ionisation forms ions from molecules. Mere dissolution can leave neutral molecules.';return q
    add('Twist: dissolution does not guarantee ions',h_solution,True)
    def h_atom(v):
        q=isotopeions(v+500);q['prompt']+=' Another sample has the same atomic number and two more neutrons. Will its usual valency differ? Justify.';q['answer']+=' It is an isotope with the same electron configuration (for the same charge), so its usual chemical valency is unchanged.';return q
    add('Twist: isotope versus ion',h_atom,True)
    def h_formula(v):
        q=empirical_mass(v+500);q['prompt']+=' State why percentage composition alone could not have fixed the molecular formula.';q['answer']+=' The empirical ratio can be multiplied by an integer; molecular mass is needed to select the multiplier.';return q
    add('Twist: empirical versus molecular information',h_formula,True)
    def h_litmus(v):
        q=observations(v+500);q['prompt']+=' A dry litmus paper shows no change with dry HCl. Does that disprove the gas identity? Explain the role of moisture.';q['answer']+=' No. HCl needs water to ionise and display its acidic effect on litmus; damp paper is required.';return q
    add('Twist: dry gas and dry indicator',h_litmus,True)
    def h_nitric(v):
        q=nitric(v+500);q['prompt']+=' Explain why using the ordinary metal+dilute-acid rule to predict hydrogen here would fail.';q['answer']+=' Nitric acid is an oxidising acid; for copper the supplied concentration determines the nitrogen oxide product, rather than liberation of hydrogen.';return q
    add('Twist: oxidising acid exception',h_nitric,True)
    def h_alkane(v):
        q=unsaturation(v+500);q['prompt']+=' Both the original and fully hydrogenated products are colourless gases in this description. Why is appearance not a sufficient test for unsaturation?';q['answer']+=' A specific addition reaction such as bromine decolourisation tests bonding; colourless appearance alone reveals no bond multiplicity.';return q
    add('Twist: chemical evidence for unsaturation',h_alkane,True)
    def h_colour(v):
        q=hydroxide(v+500);q['prompt']+=' Explain why adding the reagent in excess must be recorded as a separate observation from its initial addition.';q['answer']+=' Some initially similar precipitates dissolve in excess reagent; initial colour alone can miss the distinguishing behaviour.';return q
    add('Twist: sequence of analytical observations',h_colour,True)
    def h_gas(v):
        q=equalvolume(v+500);q['prompt']+=' A classmate says equal molecules require equal total atoms. Is that necessarily true?';q['answer']+=' No: molecular atomicity can differ (for example two atoms in H₂ and three in CO₂), so count atoms per molecule as well.';return q
    add('Twist: molecules versus total atoms',h_gas,True)
    return variant_bank('chem',fs,hard)
