from fractions import Fraction as F
from datetime import date, timedelta
from .common import item, num as N, rng, variant_bank, numeric_mcq

TRAITS=[('pea height','T','t','tall','dwarf'),('pea seed shape','R','r','round','wrinkled'),('pea seed colour','Y','y','yellow','green'),('pea flower colour','P','p','purple','white'),('pea pod colour','G','g','green','yellow'),('pea pod shape','I','i','inflated','constricted'),('pea flower position','A','a','axial','terminal')]
def cross_outcomes(a,b):
    outcomes={}
    for x in a:
        for y in b:
            g=''.join(sorted(x+y,key=lambda c:(c.islower(),c)))
            outcomes[g]=outcomes.get(g,0)+1
    return outcomes

def make_bank():
    fs=[]; hard=[]
    def add(name,fn,h=False):(hard if h else fs).append((name,fn))
    def division(v,kind=0):
        r=rng('cell'+str(kind),v); chromosomes=r.choice([4,6,8,12,16,20,24,46]); cells=r.randint(2,25); rounds=r.randint(1,5)
        if kind==0:return item('Cell division',f'{cells} diploid body cells, each containing {chromosomes} chromosomes, undergo {rounds} complete rounds of mitosis. Find the number of daughter cells and chromosomes per daughter cell. Explain the role of mitosis in tissue growth.',f'Cells={cells}×2^{rounds}={cells*2**rounds}. Every daughter cell has {chromosomes} chromosomes. Mitosis preserves chromosome number and produces genetically similar cells for growth/repair.')
        if kind==1:return item('Cell division',f'A diploid cell with {chromosomes} chromosomes is observed at metaphase of mitosis, before centromeres divide. State chromosome number, chromatid number, chromosome arrangement and the structure attaching spindle fibres to chromosomes.',f'{chromosomes} chromosomes, {2*chromosomes} chromatids. Chromosomes align at the equator; spindle fibres attach at the centromere/kinetochore region. Do not double chromosome number merely because each chromosome has two chromatids.',4)
        return item('Cell division',f'An organism has {chromosomes} chromosomes in a normal somatic cell. Compare chromosome number in its gamete, fertilised egg and daughter cells produced by mitosis. Why is reduction division necessary before sexual reproduction?',f'Gamete={chromosomes//2}; zygote={chromosomes}; mitotic daughter cell={chromosomes}. Meiosis halves chromosome number so fertilisation restores it rather than doubling it in each generation.')
    for i,n in enumerate(['Mitotic cell count','Metaphase chromosomes and chromatids','Diploid and haploid restoration']):add(n,lambda v,i=i:division(v,i))
    def division_order(v):
        r=rng('order',v); chrom=r.choice([4,6,8,10,12,16,24,46]); count=r.randint(2,25)
        return item('Cell division',f'In a sample of {count} dividing cells, each with {chrom} chromosomes, one cell has sister chromatids moving to opposite poles and another has chromosomes aligned at the equator. Identify both stages, state the event that starts their separation, and explain why equal distribution matters.',f'Moving chromatids: anaphase; equatorial chromosomes: metaphase. Centromeres divide to separate sister chromatids. Equal distribution gives each daughter nucleus the original {chrom} chromosomes and corresponding genetic information.',4)
    add('Stage identification from verbal observations',division_order)
    def gene(v,kind=0):
        r=rng('gene'+str(kind),v); trait,D,d,dom,rec=r.choice(TRAITS); total=r.randint(8,90)*4
        a,b=([(D+d,D+d),(D+d,d+d),(D+D,d+d),(D+D,D+d),(d+d,d+d)][kind%5]); outcomes=cross_outcomes(a,b); denominator=4; phenotype={dom:0,rec:0}
        for g,n in outcomes.items():phenotype[dom if D in g else rec]+=n
        return item('Genetics',f'For {trait}, {D} ({dom}) is dominant to {d} ({rec}). Cross {a} × {b}. Show the gametes, give the genotype and phenotype proportions, and calculate the expected numbers of each phenotype among {total} offspring.',f'Gamete types: '+', '.join(sorted(set(a)))+' and '+', '.join(sorted(set(b)))+'. Genotypes: '+', '.join(f'{g}: {n}/4' for g,n in sorted(outcomes.items()))+'. Phenotypes: '+', '.join(f'{name}: {n}/4, expected {total*n//4}' for name,n in phenotype.items())+'. Expected counts are theoretical, not a guarantee for a small sample.',4)
    for i,n in enumerate(['Heterozygote self-cross','Test cross','Pure dominant by pure recessive','Pure dominant by heterozygote','Recessive self-cross']):add(n,lambda v,i=i:gene(v,i))
    def testcross(v):
        r=rng('testcross',v); trait,D,d,dom,rec=r.choice(TRAITS); n=r.randint(12,130); total=2*n
        return item('Genetics',f'A {dom} plant of unknown genotype is crossed with a pure {rec} plant. The {total} offspring comprise {n} {dom} and {n} {rec}. With {D} dominant, infer the unknown genotype and explain how this cross differs from a cross between two pure contrasting parents.',f'Unknown parent={D+d}; gametes {D} and {d}. With {d+d}, offspring are ½ {D+d} ({dom}) and ½ {d+d} ({rec}). A pure {D+D}×{d+d} cross would produce only {D+d} offspring. The test-cross result indicates heterozygosity.',4)
    add('Infer a parent from offspring data',testcross)
    def sexlinked(v):
        r=rng('sexlinked',v); children=r.randint(4,60)*4; disease=r.choice(['haemophilia','red-green colour blindness']); case=r.choice([0,1,2]); mother=['XᴺXⁿ','XᴺXᴺ','XⁿXⁿ'][case]; father='XᴺY'
        ratio=[('½ sons affected; no daughters affected; ½ daughters carriers',F(1,4)),('no affected children; no carrier daughters',F(0)),('all sons affected; all daughters carriers',F(1,2))][case]
        return item('Genetics',f'For an X-linked recessive model of {disease}, a mother {mother} and father {father} have children. Show the cross and state risks separately for sons and daughters. If {children} births followed the expected equal sex ratio, how many affected children are expected?',f'Mother gametes='+('Xᴺ, Xⁿ' if case==0 else 'Xᴺ' if case==1 else 'Xⁿ')+'; father gametes Xᴺ, Y. '+ratio[0]+f'. Overall affected fraction={N(ratio[1])}; expected affected={N(children*ratio[1])}. The probability is per birth, not a fixed family outcome.',4)
    add('X-linked recessive inheritance',sexlinked)
    def dihybrid(v):
        r=rng('dihybrid',v); total=r.randint(2,70)*16
        return item('Genetics',f'Assume independent assortment and complete dominance for two pea traits. Two double-heterozygous parents are crossed. Give the F₂ phenotype ratio and expected numbers in each category among {total} plants. Do not calculate all dihybrid genotypes.',f'Phenotypes are 9:3:3:1. Expected categories: both dominant={total*9//16}; first dominant/second recessive={total*3//16}; first recessive/second dominant={total*3//16}; both recessive={total//16}. This phenotype calculation assumes independent assortment.',4)
    add('Dihybrid phenotype ratio only',dihybrid)
    def osmotic(v,kind=0):
        r=rng('osmosis'+str(kind),v); initial=r.randint(20,90)/10; delta=r.randint(1,15)/10; initial=max(initial,delta+1); gain=kind==0; final=initial+delta if gain else initial-delta; concentration=r.randint(4,20)
        return item('Plant water relations',f'A potato strip initially has mass {initial:.1f} g. After immersion in '+('distilled water' if gain else f'{concentration}% sucrose solution')+f' it has mass {final:.1f} g. Calculate percentage mass change and explain the direction of water movement through the cell membrane. Assume no tissue loss.',f'Mass change={delta if gain else -delta:.1f} g; percentage={(final-initial)/initial*100:.2f}%. Water moves '+('into cells by endosmosis from the more dilute external solution, increasing turgidity.' if gain else 'out by exosmosis into the more concentrated external solution; cells lose turgor and may plasmolyse.'),4)
    add('Osmosis: mass gain',osmotic);add('Osmosis: mass loss',lambda v:osmotic(v,1))
    def plasmolysis(v):
        r=rng('plasmolysis',v); minutes=r.randint(5,45); concentration=r.randint(5,20); examples=r.sample(['a root hair','an onion epidermal cell','a leaf epidermal cell','a young stem cell'],2)
        return item('Plant water relations',f'{examples[0].capitalize()} is placed in {concentration}% sucrose for {minutes} minutes and its living contents pull away from the wall. Name the process, state which structure is selectively permeable, and predict the change on transfer to distilled water if the cell is still alive.',f'Process: plasmolysis due to exosmosis. The plasma membrane is selectively permeable; the cell wall is freely permeable. In distilled water, endosmosis can cause deplasmolysis and restore turgidity.',4)
    add('Plasmolysis and reversal',plasmolysis)
    def root(v):
        r=rng('root',v); water=r.randint(20,200); length=r.randint(2,15); salt=r.randint(3,15)
        return item('Plant water relations',f'A seedling root with many root hairs is supplied {water} mL water. After a gardener adds concentrated fertiliser ({salt}% model solute concentration), its young leaves wilt although soil remains wet. Explain the root-hair adaptations, the direction of water movement and why “more water in the soil” does not by itself prove water will enter the roots.',f'Root hairs provide large absorptive surface, thin permeable walls and a selectively permeable membrane. A strongly concentrated external solution can draw water out by exosmosis. Osmotic movement depends on relative solution concentration/water potential, not total water volume alone.',4)
    add('Root absorption in saline conditions',root)
    def potometer(v):
        r=rng('potometer',v); a=r.randint(1,15); distance=r.randint(8,90); t=r.randint(2,15); rate=distance/t; factor=r.choice([2,3,4]); wet=distance/factor
        return item('Transpiration',f'In a potometer, an air bubble moves from {a} mm to {a+distance} mm in {t} minutes. Calculate uptake distance per minute. Under more humid air it moves only {N(wet)} mm in the same time. Explain the difference and why a potometer measures uptake, not transpiration exactly.',f'First uptake rate={distance}/{t}={rate:.2f} mm/min; humid-air rate={wet/t:.2f} mm/min. Humidity reduces the water-vapour diffusion gradient. Some absorbed water is retained or used, so uptake is an estimate of transpiration, not an identical quantity.',4)
    add('Potometer rate and humidity',potometer)
    def potometer_volume(v):
        r=rng('potvol',v); area=r.randint(1,8)/10; dist=r.randint(10,95); time=r.randint(2,12); vol=area*dist
        return item('Transpiration',f'A potometer capillary has internal cross-sectional area {area:.1f} mm². Its bubble moves {dist} mm in {time} minutes. Use volume=area×distance to find uptake volume and rate. Explain why all joints must be airtight.',f'Volume={area}×{dist}={N(vol)} mm³; rate={vol/time:.2f} mm³/min. Leaks can move the bubble or admit air independently of uptake, making the measurement invalid.',4)
    add('Potometer volume from supplied geometry',potometer_volume)
    def leaf(v):
        r=rng('leaf',v); upper=r.randint(15,60); lower=r.randint(80,260); minutes=r.randint(8,45)
        return item('Transpiration',f'A dicot leaf has {upper} stomata per mm² on its upper surface and {lower} on its lower surface. In a {minutes}-minute cobalt-chloride paper test, which surface would normally turn the paper pink sooner? Explain the indicator change, the role of stomata and one control needed.',f'The lower surface would normally act faster because its stomatal density is greater. Dry blue cobalt-chloride paper turns pink on absorbing moisture. Use comparable paper area/dryness, the same leaf conditions and a control against atmospheric moisture.',4)
    add('Stomatal distribution and cobalt chloride',leaf)
    def vaseline(v):
        r=rng('vaseline',v); minutes=r.randint(10,80); control=r.randint(30,100)/10; coated=control/r.choice([2,3,4]); side=r.choice(['lower','both'])
        return item('Transpiration',f'Two similar leafy shoots lose {control:.1f} g and {coated:.2f} g in {minutes} minutes. The second has petroleum jelly on '+('both leaf surfaces' if side=='both' else 'the lower leaf surface')+'. Explain the lower loss, identify two variables to control, and state one function of transpiration.',f'Jelly restricts stomatal/cuticular water loss; coating the more stomata-rich lower surface particularly reduces transpiration. Control leaf area, time, temperature, humidity and air movement (any two). Transpiration supports water/mineral transport and evaporative cooling.',4)
    add('Coated-leaf comparison',vaseline)
    def photosynthesis(v):
        r=rng('photo',v); hours=r.randint(18,48); light=r.randint(2,8); setup=r.choice(['KOH under a sealed bell jar','an opaque cover over part of a leaf','a variegated leaf'])
        answers={'KOH under a sealed bell jar':('carbon dioxide','KOH absorbs carbon dioxide; a sealed jar prevents replacement. An otherwise identical control has no KOH. The test leaf fails to turn blue-black if CO₂ is absent.'),'an opaque cover over part of a leaf':('light','The covered part lacks light and does not form starch, while exposed photosynthetic tissue turns blue-black.'),'a variegated leaf':('chlorophyll','Only originally green exposed regions normally turn blue-black; compare their position with the original green areas.')}
        req,explanation=answers[setup]
        return item('Photosynthesis',f'A plant is kept in darkness for {hours} hours, then used with {setup} and exposed to light for {light} hours. State the aim, explain destarching, predict the iodine-test result and state a relevant control/comparison.',f'Aim: test the requirement for {req}. Darkness uses stored starch, so new starch can be attributed to the test conditions. {explanation}',4)
    add('Photosynthesis requirement experiments',photosynthesis)
    def starchtest(v):
        r=rng('starchtest',v); hours=r.randint(2,10); leaves=r.randint(2,10); condition=r.choice(['light','darkness','absence of CO₂'])
        return item('Photosynthesis',f'{leaves} destarched leaves are kept in {condition} for {hours} hours. Describe the sequence used to test for starch, explaining the purpose of hot water, alcohol, washing and iodine. State the positive result.',f'Hot water kills cells/stops reactions. Alcohol removes chlorophyll and is heated using a water bath, away from a direct flame. Wash to soften/remove alcohol, then add iodine. Blue-black indicates starch. In darkness/absence of CO₂, new starch should not be produced under an otherwise controlled test.',4)
    add('Starch-test sequence and purpose',starchtest)
    def oxygen(v):
        r=rng('oxygen',v); first=r.randint(10,60); second=first+r.randint(10,70); time=r.randint(2,12)
        return item('Photosynthesis',f'A water plant releases {first} bubbles in {time} minutes under one light condition and {second} bubbles in the same time under brighter light. Calculate both rates, infer the effect of light and give one reason bubble count is only an approximate measure of photosynthesis.',f'Rates={first/time:.2f} and {second/time:.2f} bubbles/min. The higher rate is consistent with increased photosynthesis when light was limiting. Bubble sizes vary and some oxygen dissolves; keep plant size, temperature and CO₂ supply controlled.',4)
    add('Photosynthetic oxygen-rate data',oxygen)
    def equation(v):
        r=rng('equation',v); glucose=r.randint(1,30); bottles=r.randint(2,20)
        return item('Photosynthesis',f'A model leaf produces {glucose} molecules of glucose by photosynthesis. Write a balanced overall photosynthesis equation and use it to state the corresponding CO₂ and net O₂ molecule counts. State where light energy is trapped and name the mineral required for chlorophyll.',f'6CO₂+12H₂O → C₆H₁₂O₆+6H₂O+6O₂ in light and chlorophyll (net form also acceptable). CO₂={6*glucose}; O₂={6*glucose}. Chlorophyll in chloroplasts traps light; magnesium is required for chlorophyll.',4)
    add('Photosynthesis equation and molecule ratio',equation)
    def tropism(v):
        r=rng('tropism',v); days=r.randint(2,15); conditions=r.sample(['shoot lit from one side','root placed horizontally','root near moisture on one side','tendril touches a support'],2)
        mapping={'shoot lit from one side':'positive phototropism; unequal auxin-related growth makes the shoot curve towards light','root placed horizontally':'positive geotropism; root growth turns downward in response to gravity','root near moisture on one side':'positive hydrotropism; root grows towards greater moisture','tendril touches a support':'positive thigmotropism; contact-associated growth helps the tendril coil'}
        return item('Plant coordination',f'Over {days} days two observations are recorded: (a) {conditions[0]}; (b) {conditions[1]}. Name and explain the directional response in each. Distinguish a growth response from movement caused simply by wind.',f'(a) {mapping[conditions[0]]}. (b) {mapping[conditions[1]]}. A tropism is directional growth in relation to a stimulus; wind can bend a plant without producing that biological growth response.',4)
    add('Tropic responses from conditions',tropism)
    def hormones(v):
        r=rng('phormone',v); days=r.randint(3,25); a,b=r.sample([('auxin','cell elongation and phototropic bending'),('gibberellin','stem elongation and seed germination'),('cytokinin','cell division and delayed senescence'),('abscisic acid','stress responses such as stomatal closure and dormancy'),('ethylene','fruit ripening')],2)
        return item('Plant coordination',f'In a {days}-day plant-growth study, treatment A is associated with {a[1]}, while treatment B is associated with {b[1]}. Identify the likely hormones and explain why growth promoters and inhibitors both matter for plant survival.',f'A: {a[0]}; B: {b[0]}. Growth must be coordinated with development and environmental resources. For example ABA-mediated closure conserves water under stress, whereas promoters support appropriate growth.',4)
    add('Plant hormone action comparison',hormones)
    def stomata(v):
        r=rng('stomata',v); count=r.randint(20,150); open_=r.randint(1,count-1)
        return item('Plant coordination',f'Of {count} stomata examined before drought, {open_} are open. After water stress, only {open_//2} are open. Find the before/after percentage open and explain the roles of guard-cell turgor and ABA. Give one trade-off of closure.',f'Before={open_/count*100:.2f}%; after={(open_//2)/count*100:.2f}%. Guard-cell turgor controls the pore; ABA promotes closure during stress. Closure conserves water but restricts CO₂ uptake and can reduce photosynthesis.',4)
    add('Stomatal closure from counts',stomata)
    def output(v):
        r=rng('cardiac',v); rate=r.randint(55,105); stroke=r.randint(45,95); exercise=r.randint(110,165); stroke2=stroke+r.randint(5,25)
        return item('Circulatory system',f'A model heart beats {rate} times/min and pumps {stroke} mL/beat at rest. During exercise values become {exercise}/min and {stroke2} mL/beat. Using output=rate×stroke volume, calculate both outputs in L/min and explain the increase.',f'Rest={rate*stroke/1000:.3f} L/min; exercise={exercise*stroke2/1000:.3f} L/min. Active muscles need more oxygen/nutrients and faster removal of CO₂; increased heart output supports these demands.',4)
    add('Cardiac output from supplied relation',output)
    def heartpath(v):
        r=rng('heartpath',v); steps=r.randint(12,90); start=r.choice(['body tissues','lungs','left ventricle','right ventricle'])
        paths={'body tissues':'vena cava → right atrium → right ventricle → pulmonary artery → lungs','lungs':'pulmonary veins → left atrium → left ventricle → aorta → body','left ventricle':'aorta → systemic arteries → body capillaries → veins → vena cava → right atrium','right ventricle':'pulmonary artery → lung capillaries → pulmonary veins → left atrium'}
        return item('Circulatory system',f'After {steps} seconds of a circulation-tracing simulation, a marker is reported at {start}. State the next major route it follows, the oxygenation change across the relevant capillary bed, and why valves are needed.',f'Route: {paths[start]}. Pulmonary capillaries oxygenate blood; systemic capillaries supply tissues and collect CO₂. Valves maintain one-way flow by preventing backflow. Arteries are named by direction away from the heart, not oxygen content.',4)
    add('Blood route and oxygenation',heartpath)
    def vessels(v):
        r=rng('vessels',v); a,b=r.sample([('artery','thick elastic muscular wall; carries blood away from the heart'),('vein','thinner wall, wider lumen, often valves; carries blood towards the heart'),('capillary','one-cell-thick wall for exchange')],2); pressure=r.randint(70,140)
        return item('Circulatory system',f'A tissue model includes a vessel with {a[1]} and another with {b[1]}. Its arterial pressure is recorded as {pressure} arbitrary units. Identify the two vessel types, link their structures to functions and explain why exchange is concentrated in capillary beds.',f'First={a[0]}; second={b[0]}. Their stated structures match transport direction/pressure or exchange. Capillaries have very thin walls, narrow channels and large collective surface area, allowing exchange with tissue fluid.',4)
    add('Vessel structure-function identification',vessels)
    def blood(v):
        r=rng('blood',v); amount=r.randint(2,10); cases=r.sample([('low haemoglobin','reduced oxygen transport by red blood cells'),('low platelet count','impaired clot formation and longer bleeding'),('increased white-cell activity','defence against infection'),('loss of plasma','reduced fluid/transport volume and altered circulation')],2)
        return item('Circulatory system',f'In two fictional samples of {amount} mL blood, A shows {cases[0][0]} and B shows {cases[1][0]}. Link each finding to the affected function. Explain how red cells are adapted for oxygen carriage and why mature human red cells lack a nucleus.',f'A: {cases[0][1]}; B: {cases[1][1]}. Red cells contain haemoglobin and have a biconcave form increasing exchange surface; absence of a nucleus provides more space for haemoglobin. This is a textbook model, not a diagnosis.',4)
    add('Blood components from functional data',blood)
    def filtration(v):
        r=rng('kidney',v); filtrate=r.randint(100,200); urine=r.randint(10,25)/10; reabsorbed=filtrate-urine
        return item('Excretory system',f'A simplified kidney model forms {filtrate} L filtrate per day and produces {urine:.1f} L urine. Calculate the volume and percentage reabsorbed. Name the filtration site and explain why normal urine should not contain large plasma proteins.',f'Reabsorbed={reabsorbed:.1f} L; percentage={reabsorbed/filtrate*100:.2f}%. Ultrafiltration occurs at the glomerulus into Bowman’s capsule. The filtration barrier normally retains blood cells and large proteins.',4)
    add('Filtration versus urine output',filtration)
    def adh(v):
        r=rng('adh',v); before=r.randint(15,30)/10; after=r.randint(5,12)/10; hours=r.randint(2,12)
        return item('Excretory system',f'In a model, urine output changes from {before:.1f} L/day to {after:.1f} L/day after several hours of water shortage. Explain the expected ADH response, its effect on water reabsorption and the change in urine concentration.',f'Water shortage generally increases ADH release from the posterior pituitary. Increased collecting-tubule/duct water permeability increases reabsorption, reducing volume and concentrating urine. Excretion of wastes must continue; the kidney does not merely “stop working”.',4)
    add('ADH response to water shortage',adh)
    def urine(v):
        r=rng('urine',v); volume=r.randint(5,25)/10; pairs=r.sample([('urea','a nitrogenous waste formed mainly in the liver'),('glucose','normally selectively reabsorbed after filtration'),('large plasma proteins','normally retained in blood by the filtration barrier'),('excess water and salts','regulated in the final urine')],2)
        return item('Excretory system',f'A simplified analysis of {volume:.1f} L daily urine considers {pairs[0][0]} and {pairs[1][0]}. Explain their normal handling by the body/kidney and distinguish excretion from egestion.',f'{pairs[0][0].capitalize()}: {pairs[0][1]}. {pairs[1][0].capitalize()}: {pairs[1][1]}. Excretion removes metabolic wastes; egestion removes undigested material from the alimentary canal.',4)
    add('Urine constituents and excretion',urine)
    def reflex(v):
        r=rng('reflex',v); distance=r.randint(30,200)/100; time=r.randint(1,9)/100; object_=r.choice(['a hot pan','a sharp thorn','a hot metal handle','an unexpectedly sharp edge'])
        return item('Nervous system',f'A person quickly withdraws a hand after touching {object_}. In a simplified reflex model, the signal route is {distance:.2f} m and delay {time:.2f} s. Using speed=distance/time, calculate model signal speed, list the reflex-arc sequence and distinguish the immediate response from later conscious pain perception.',f'Model speed={distance/time:.2f} m/s. Receptor → sensory neuron → relay/association neuron in spinal cord → motor neuron → effector muscle. The spinal reflex can initiate withdrawal before the brain completes conscious interpretation; information also reaches the brain.',4)
    add('Reflex arc with supplied timing model',reflex)
    def neurons(v):
        r=rng('neurons',v); synapses=r.randint(2,9); delays=r.randint(1,8); a,b=r.sample([('sensory neuron','carries impulses from a receptor towards the central nervous system'),('motor neuron','carries impulses from the central nervous system to an effector'),('relay neuron','connects neurons within the central nervous system')],2)
        return item('Nervous system',f'A signal pathway has {synapses} synapses. Each contributes a model delay of {delays} ms. Find total synaptic delay. Identify neurons A and B if A {a[1]} and B {b[1]}; explain why chemical synapses usually transmit in one direction.',f'Delay={synapses*delays} ms. A={a[0]}; B={b[0]}. Neurotransmitter is released from the presynaptic ending and acts on receptors on the postsynaptic membrane, producing directional transmission.',4)
    add('Neuron types and synapse direction',neurons)
    def brain(v):
        r=rng('brain',v); trials=r.randint(2,45); a,b=r.sample([('cerebrum','conscious thought, memory and voluntary action'),('cerebellum','balance and coordination of muscle activity'),('medulla oblongata','involuntary functions such as breathing and heartbeat')],2)
        return item('Nervous system',f'Across {trials} observations, subject A has difficulty with {a[1]}, while subject B has difficulty with {b[1]}. Name the associated brain regions and contrast voluntary control with involuntary regulation.',f'A: {a[0]}; B: {b[0]}. Voluntary action involves conscious initiation; involuntary regulation maintains functions without repeated conscious commands. These are functional associations in an educational model.',4)
    add('Brain-region functional comparison',brain)
    def eye(v):
        r=rng('eye',v); a,b=r.sample([('myopia','distant objects blurred; image tends to form in front of the retina','concave lens'),('hyperopia','near objects blurred; image tends to form behind the retina','convex lens'),('presbyopia','age-related loss of accommodation','appropriate reading/bifocal correction as prescribed')],2); distance=r.randint(20,80)
        return item('Sense organs',f'In a textbook vision test at {distance} cm, case A is described as “{a[1]}”, case B as “{b[1]}”. Identify the defects, state their corrective lens types and explain the function of the retina.',f'A: {a[0]}, corrected using a {a[2]}. B: {b[0]}, corrected using a {b[2]}. Retinal rods/cones receive light and initiate signals carried by the optic nerve. Actual correction requires an eye examination.',4)
    add('Vision defects from verbal image positions',eye)
    def accommodation(v):
        r=rng('accom',v); near=r.randint(20,40); far=r.randint(3,30); light=r.choice(['bright','dim'])
        return item('Sense organs',f'A person shifts focus from an object {near} cm away to one {far} m away. Describe changes in ciliary muscle, suspensory ligaments and lens curvature. Separately explain the pupil response to {light} light.',f'For distant focus: ciliary muscles relax, suspensory ligaments become taut and lens becomes thinner/less convex. For near focus these reverse. '+('Bright light causes pupil constriction.' if light=='bright' else 'Dim light causes pupil dilation.')+' Iris controls pupil size; ciliary muscles control accommodation.',4)
    add('Accommodation versus pupil response',accommodation)
    def ear(v):
        r=rng('ear',v); freq=r.randint(2,18)*100; rate=r.randint(2,15); a,b=r.sample([('pinna','collects sound waves'),('tympanic membrane','vibrates with sound'),('ear ossicles','transmit and amplify vibrations'),('cochlea','contains sensory receptors for hearing'),('Eustachian tube','equalises air pressure across the eardrum'),('semicircular canals','detect rotational movement and help balance')],2)
        return item('Sense organs',f'A hearing/balance lesson uses a {freq} Hz sound. Explain the functions of {a[0]} and {b[0]}, then trace the general route from incoming sound to the auditory nerve. Why is a pressure-equalising connection to the throat useful?',f'{a[0]}: {a[1]}; {b[0]}: {b[1]}. Pinna → ear canal → eardrum → ossicles → oval window/cochlear fluid → sensory hair cells → auditory nerve. Eustachian tube equalises pressure so the eardrum can vibrate effectively.',4)
    add('Hearing route and ear functions',ear)
    def endocrine(v):
        r=rng('endocrine',v); time=r.randint(10,180); a,b=r.sample([('insulin','pancreatic beta cells','lowers high blood glucose'),('glucagon','pancreatic alpha cells','raises low blood glucose'),('thyroxine','thyroid','influences metabolic rate'),('adrenaline','adrenal medulla','supports the fight-or-flight response'),('growth hormone','anterior pituitary','supports body growth'),('ADH','released from posterior pituitary','increases water reabsorption')],2)
        return item('Endocrine system',f'In a model observed for {time} minutes, response A {a[2]} and response B {b[2]}. Identify both hormones and source glands. Explain one difference between endocrine signalling and a nerve impulse.',f'A={a[0]}, {a[1]}; B={b[0]}, {b[1]}. Hormones travel in blood to target cells with receptors; nerve impulses travel along neurons and usually act more rapidly and locally.',4)
    add('Hormone source and action',endocrine)
    def glucose(v):
        r=rng('glucose',v); base=r.randint(75,95); high=base+r.randint(40,95); later=base+r.randint(-5,8); minutes=r.randint(60,180)
        return item('Endocrine system',f'A simplified healthy response shows blood glucose changing from {base} to {high} mg/dL after a meal and then to {later} mg/dL after {minutes} minutes. Identify the hormone expected to increase after the meal, explain two of its effects and describe negative feedback.',f'Insulin secretion increases. It promotes glucose uptake and conversion of surplus glucose to glycogen, helping lower the raised concentration. As the stimulus falls, secretion reduces: negative feedback stabilises conditions. These values are supplied for a model, not individual diagnosis.',4)
    add('Glucose data and negative feedback',glucose)
    def thyroid(v):
        r=rng('thyroid',v); population=r.randint(5,80)*100; affected=r.randint(1,20); iodine=r.choice(['adequate','deficient'])
        return item('Endocrine system',f'A school case study follows {population} people; {affected}% have thyroid enlargement in an iodine-deficient region. Calculate the affected number and explain the link between iodine, thyroxine and thyroid enlargement. Why is every goitre not simply a label for excessive thyroxine?',f'Affected={population*affected//100}. Iodine is needed for thyroxine synthesis; deficiency may reduce hormone production and cause compensatory gland enlargement. Enlargement describes structure, not a unique hormone level; the underlying condition matters.',4)
    add('Iodine deficiency and interpretation',thyroid)
    def cycle(v):
        r=rng('cycle',v); length=r.randint(26,32); day=length-14; start=r.randint(1,20)
        first=date(2027,3,start); predicted=first+timedelta(days=day-1)
        return item('Reproductive system',f'A textbook model assumes a regular {length}-day menstrual cycle starting on {first.strftime("%d %B %Y")} (day 1), and ovulation 14 days before the next menstruation. Estimate the cycle day and calendar date of ovulation, identify the hormone surge associated with ovulation, and state the role of progesterone.',f'Estimated cycle day={length}−14={day}; calendar date={predicted.strftime("%d %B %Y")}. LH surge is associated with ovulation. Progesterone helps maintain the endometrium for possible implantation; falling hormone levels allow shedding if pregnancy does not occur. This simplified cycle model does not predict an individual’s fertility.',4)
    add('Menstrual-cycle model and hormones',cycle)
    def embryo(v):
        r=rng('embryo',v); divisions=r.randint(1,6); cells=2**divisions; embryos=r.randint(2,25)
        return item('Reproductive system',f'A development model contains {embryos} independent fertilised human eggs, each undergoing {divisions} ideal mitotic divisions. Find the cell count per embryo and total cell count. Name the usual fertilisation site and implantation site, and distinguish the two processes.',f'Per embryo: 2^{divisions}={cells}; total={embryos}×{cells}={embryos*cells}. Fertilisation normally occurs in the oviduct; implantation occurs in the uterine endometrium. Fertilisation fuses gametes; implantation embeds the developing embryo in the uterine lining.',4)
    add('Fertilisation implantation and cleavage',embryo)
    def placenta(v):
        r=rng('placenta',v); stage=r.randint(8,35); a,b=r.sample(['oxygen','glucose','carbon dioxide','urea'],2)
        directions={'oxygen':'mother to foetus','glucose':'mother to foetus','carbon dioxide':'foetus to mother','urea':'foetus to mother'}
        return item('Reproductive system',f'At week {stage} in a model of human pregnancy, consider placental exchange of {a} and {b}. State the usual direction for each, explain the exchange surface and give two functions of the amniotic fluid/sac.',f'{a}: {directions[a]}; {b}: {directions[b]}. Placental villi provide extensive thin exchange surfaces; maternal and foetal blood do not normally mix directly. Amniotic fluid cushions the foetus, permits movement and helps maintain a stable environment (any two).',4)
    add('Placenta exchange and protection',placenta)
    def gametes(v):
        r=rng('gametes',v); ova=r.randint(1,15); sperm=r.randint(20,100)*1000; route=r.choice(['sperm','ovum'])
        path='seminiferous tubules → epididymis → vas deferens → urethra' if route=='sperm' else 'ovary → oviduct → uterus'
        return item('Reproductive system',f'A human reproduction model shows {ova} ovum/ova and {sperm} sperm cells. Give chromosome number in either gamete, trace the route of a {route}, and explain one structural adaptation of sperm and one of the ovum.',f'Each normal gamete has 23 chromosomes. Route: {path}. Sperm has a flagellum for movement and many mitochondria in the middle piece; the ovum has cytoplasm supporting early development and a protective membrane. Large sperm numbers do not change chromosome number.',4)
    add('Gamete structure and transport',gametes)
    def population(v):
        r=rng('population',v); start=r.randint(10,80)*1000; births=r.randint(200,900); deaths=r.randint(100,500); immigrants=r.randint(40,250); emigrants=r.randint(20,180); end=start+births-deaths+immigrants-emigrants
        return item('Population',f'A town starts a year with {start} people. There are {births} births, {deaths} deaths, {immigrants} immigrants and {emigrants} emigrants. Find population at year-end and natural increase. Explain why natural increase alone does not give the total change.',f'Natural increase={births-deaths}. Total change=births−deaths+immigration−emigration={end-start}; final population={end}. Migration also affects population size.',4)
    add('Population balance with migration',population)
    def birthrate(v):
        r=rng('rates',v); pop=r.randint(10,100)*1000; births=r.randint(15,35)*pop//1000; deaths=r.randint(5,14)*pop//1000
        return item('Population',f'In a population of {pop}, {births} live births and {deaths} deaths occur in one year. Calculate birth and death rates per thousand and natural growth rate per thousand. State one limitation of comparing these rates without age-structure information.',f'Birth rate={births/pop*1000:.1f}‰; death rate={deaths/pop*1000:.1f}‰; natural increase={(births-deaths)/pop*1000:.1f}‰. Different age structures can affect births/deaths and must be considered in interpretation.',4)
    add('Rates per thousand',birthrate)
    def evolution(v):
        r=rng('evolution',v); start=r.randint(100,500); dark=r.randint(10,60); end=r.randint(60,95); generations=r.randint(3,30)
        return item('Evolution',f'A model moth population changes from {dark}% dark forms among {start} moths to {end}% after {generations} generations on darkened tree trunks. Explain natural selection using variation, differential survival and inheritance. Why is “each moth changed colour because it needed to” an incorrect explanation?',f'Pre-existing heritable variation gives some moths better camouflage. Reduced predation increases their survival/reproduction; inherited variants become more frequent. Individuals do not intentionally acquire the needed inherited colour. Selection changes frequencies across generations.',4)
    add('Natural selection from frequency changes',evolution)
    def homology(v):
        r=rng('homology',v); sample=r.randint(8,70); a,b=r.sample([('human arm','whale flipper','homologous: common basic structural origin with different functions'),('bird wing','insect wing','analogous: flight function is similar but basic origin differs'),('human appendix','reduced caecal structure','vestigial: reduced remnant with ancestral significance')],2)
        return item('Evolution',f'A class examines {sample} structural records. Compare pair A ({a[0]} and {a[1]}) with pair B ({b[0]} and {b[1]}). Identify the kind of evolutionary evidence and explain why similar function alone does not prove close ancestry.',f'A: {a[2]}. B: {b[2]}. Functional resemblance can arise independently; structural/developmental relationships and other evidence are needed.',4)
    add('Comparative evolutionary evidence',homology)
    def foodchain(v):
        r=rng('food',v); producer=r.randint(1,80)*1000; transfer=r.choice([5,10,15]); first=producer*transfer/100; second=first*transfer/100
        return item('Ecology and pollution',f'A supplied food-chain model has {producer} kJ at producer level and transfers {transfer}% to each next trophic level. Calculate energy at the next two levels. Explain why the transfer percentage is a model assumption and why energy flow differs from recycling matter.',f'First consumer={N(first)} kJ; second consumer={N(second)} kJ. Transfer varies in real systems; energy is dissipated as heat/metabolism and flows directionally. Matter cycles through organisms and the environment.',4)
    add('Energy transfer with a supplied model',foodchain)
    def pollution(v):
        r=rng('pollution',v); before=r.randint(65,95); after=r.randint(15,55); period=r.randint(2,25)
        return item('Ecology and pollution',f'In a river model, dissolved oxygen falls from {before/10:.1f} to {after/10:.1f} mg/L over {period} days after untreated organic sewage enters. Explain the bacterial process, predict an effect on fish and suggest two measures at the pollution source.',f'Microbes decompose organic matter and consume dissolved oxygen; increased oxygen demand can leave less for fish, causing stress/death. Treat sewage before release and prevent direct organic-waste discharge; monitor effluent and oxygen demand.',4)
    add('Sewage and dissolved-oxygen data',pollution)
    def biomagnification(v):
        r=rng('biomag',v); low=r.randint(1,20)/1000; factor=r.choice([5,10,20]); levels=r.randint(2,4)
        return item('Ecology and pollution',f'A model persistent pesticide has concentration {low:.3f} units at the producer level and rises by factor {factor} at each transfer. Find concentration after {levels} transfers. Explain biomagnification and why a non-biodegradable pollutant poses a food-chain problem.',f'Model concentration={low}×{factor}^{levels}={N(low*factor**levels)} units. Persistent substances accumulate and become more concentrated at higher trophic levels as predators consume many contaminated prey. The numerical factor is supplied, not a universal biological constant.',4)
    add('Biomagnification model',biomagnification)
    def waste(v):
        r=rng('waste',v); organic=r.randint(10,100); batteries=r.randint(2,30); paper=r.randint(5,60)
        return item('Ecology and pollution',f'A school generates {organic} kg food waste, {paper} kg clean paper and {batteries} used batteries. Propose separate management routes and explain why a single compost pit is unsuitable for the whole collection.',f'Food waste: controlled composting/biogas where suitable. Clean paper: reuse/recycling. Batteries: authorised hazardous/e-waste collection. Batteries can introduce toxic materials and paper is better recovered separately; mixed disposal reduces safe resource recovery.',4)
    add('Waste separation with stated materials',waste)
    def h_sample(v):
        q=gene(v+400,0);q['prompt']+=' If actual small-sample results differ from the expected counts, does that alone disprove Mendelian segregation? Explain.';q['answer']+=' No. Random fertilisation causes sampling variation; test larger, well-controlled data before drawing that conclusion.';return q
    add('Twist: expectation versus observation',h_sample,True)
    def h_stomata(v):
        q=stomata(v+400);q['prompt']+=' A student claims that reduced transpiration always increases growth. Evaluate the claim using CO₂ entry and cooling.';q['answer']+=' Not always: reduced CO₂ entry may limit photosynthesis and reduced evaporative cooling may raise leaf temperature, even though water is conserved.';return q
    add('Twist: benefit and trade-off of closure',h_stomata,True)
    def h_osmosis(v):
        q=osmotic(v+400,1);q['prompt']+=' Predict whether a boiled, membrane-damaged strip should be interpreted using the same selectively permeable-cell model.';q['answer']+=' Not without qualification: boiling disrupts living membranes; the selective barrier assumed in the model may no longer function.';return q
    add('Twist: intact versus damaged membrane',h_osmosis,True)
    def h_photo(v):
        q=photosynthesis(v+400);q['prompt']+=' Explain why a positive iodine test in a plant that was not destarched could not by itself prove starch was made during the experiment.';q['answer']+=' Previously stored starch may remain; destarching helps isolate starch formed under the experimental conditions.';return q
    add('Twist: pre-existing starch confound',h_photo,True)
    def h_renal(v):
        q=filtration(v+400);q['prompt']+=' A student calls the entire filtrate volume “water lost from the body”. Correct this claim.';q['answer']+=' Most filtered water is reabsorbed to blood; only the final excreted fraction is lost as urine.';return q
    add('Twist: filtration is not excretion',h_renal,True)
    def h_chromosome(v):
        q=division(v+400,1);q['prompt']+=' Explain how DNA can have replicated even though the chromosome number has not doubled at metaphase.';q['answer']+=' DNA replication forms sister chromatids; chromosome count is based on centromeres until they separate.';return q
    add('Twist: DNA amount versus chromosome count',h_chromosome,True)
    def h_pop(v):
        q=population(v+400);q['prompt']+=' Could this town have positive natural increase yet a falling total population? State the required migration condition.';q['answer']+=' Yes, if net emigration exceeds births minus deaths; total change then becomes negative.';return q
    add('Twist: migration reverses natural growth',h_pop,True)
    def h_evolution(v):
        q=evolution(v+400);q['prompt']+=' If the background becomes light again, must every dark moth disappear immediately? Explain.';q['answer']+=' No. Selection changes reproductive success over generations; surviving frequencies, migration and other conditions matter.';return q
    add('Twist: selection is not immediate transformation',h_evolution,True)
    def h_vessels(v):
        q=heartpath(v+400);q['prompt']+=' Give one artery carrying deoxygenated blood and one vein carrying oxygenated blood in the adult pulmonary circuit.';q['answer']+=' Pulmonary artery carries deoxygenated blood away from the right ventricle; pulmonary veins return oxygenated blood to the left atrium.';return q
    add('Twist: artery does not mean oxygenated',h_vessels,True)
    def h_control(v):
        q=oxygen(v+400);q['prompt']+=' The brighter lamp also warmed the water. Explain why the result cannot isolate light intensity as the only cause.';q['answer']+=' Temperature changed as well and can affect metabolic rate; control it independently before attributing the difference solely to light.';return q
    add('Twist: two changed experimental factors',h_control,True)
    return variant_bank('bio',fs,hard)
