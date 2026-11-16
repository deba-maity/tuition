"""Original coherent biology cases with the five-part 1+2+2+2+3 mark split."""
from .common import rng
CASES=[
('A destarched plant has one leaf partly covered with opaque paper. After sunlight exposure, the leaf is tested for starch.',[
('Name the starch-testing reagent.','Iodine solution.'),
('Why must the plant be destarched first?','Previously stored starch must be removed so the result can be attributed to starch formed during the experiment.'),
('Why is alcohol heated in a water bath during the test?','Alcohol removes chlorophyll so the colour change can be seen; a water bath avoids direct flame near flammable alcohol.'),
('State the results expected in exposed and covered regions.','Exposed: blue-black. Covered: yellow-brown, provided destarching and light exclusion were effective.'),
('State the conclusion and explain why the experiment does not establish the need for carbon dioxide.','It supports a requirement for light in starch formation under these conditions. Carbon dioxide was not independently changed between the two regions; its role needs a separate controlled experiment.')]),
('A kidney model filters blood and returns useful substances to the circulation. Its ADH concentration then rises.',[
('Name the functional unit of the kidney.','Nephron.'),
('Explain ultrafiltration in the glomerulus.','High blood pressure drives water and small dissolved substances into Bowman’s capsule; blood cells and most large proteins remain in the circulation.'),
('Why is glucose in the filtrate normally absent from final urine?','It is small enough to be filtered, then normally selectively reabsorbed, chiefly in the proximal convoluted tubule.'),
('Predict two changes in final urine when ADH increases.','Water reabsorption increases; urine volume decreases and it becomes more concentrated.'),
('Distinguish excretion, egestion and secretion with one example each.','Excretion removes metabolic waste, e.g. urea; egestion removes undigested food from the alimentary canal; secretion releases a useful substance, e.g. a digestive enzyme or hormone.')]),
('A person withdraws a hand from a hot surface. Separately, the person walks from a dim room into bright light.',[
('Name the junction between communicating neurons.','Synapse.'),
('State the impulse directions in sensory and motor neurons.','Sensory: from receptor towards CNS. Motor: from CNS towards effector.'),
('Why can withdrawal begin before conscious awareness of pain?','A spinal reflex pathway can coordinate the response without waiting for conscious cerebral interpretation; impulses also travel to the brain.'),
('State two changes in the iris during pupil constriction.','Circular muscles contract; radial muscles relax.'),
('Trace the withdrawal reflex and distinguish receptor and effector.','Skin receptor → sensory neuron → relay neuron in spinal cord → motor neuron → muscle. Receptor detects the stimulus; effector performs the response.')]),
('Compare control of blood glucose after a carbohydrate-rich meal with the response to sudden danger.',[
('Name the endocrine region of the pancreas.','Islets of Langerhans.'),
('State the source and effect of insulin.','Beta cells secrete insulin; it promotes glucose utilisation/storage and lowers blood glucose.'),
('Why are glucagon and insulin described as antagonistic?','Glucagon raises blood glucose, including by glycogen breakdown; insulin lowers it. Their effects on this regulated quantity oppose each other.'),
('Give two physiological effects of adrenaline.','Increased heart rate; increased blood glucose. Accept appropriate increased breathing or redirected blood supply to skeletal muscles.'),
('Distinguish endocrine and exocrine glands and give an example of each.','Endocrine glands are ductless and release hormones into blood, e.g. thyroid. Exocrine glands release products through ducts, e.g. salivary glands. The pancreas has both functions.')]),
('Consider the normal human sequence from ovulation to implantation and placental exchange.',[
('Name the usual site of fertilisation.','Oviduct/fallopian tube.'),
('Distinguish ovulation from implantation.','Ovulation releases an ovum from an ovary; implantation embeds the early embryo in the uterine lining.'),
('State two functions of amniotic fluid.','Cushions against mechanical shock; permits fetal movement in a protected fluid environment. Accept suitable temperature/protection points.'),
('Explain the directions of oxygen and carbon dioxide exchange at the placenta.','Oxygen passes from maternal towards fetal blood; carbon dioxide passes from fetal towards maternal blood across placental surfaces. Direct mixing is not required.'),
('Give one function each of testes, scrotum and sperm duct.','Testes produce sperm/testosterone; scrotum helps maintain a lower temperature for sperm production; sperm duct carries sperm towards the urethra.')]),
('Fertiliser runoff enters a lake. An algal bloom is followed by falling dissolved oxygen. A nearby school generates peels, paper and used batteries.',[
('Name excessive nutrient enrichment of a water body.','Eutrophication.'),
('Explain why oxygen falls after the bloom.','Dead organic material is decomposed by microorganisms; their aerobic respiration consumes dissolved oxygen.'),
('Distinguish biodegradable and non-biodegradable waste with examples.','Peels are broken down biologically; plastic wrappers persist under ordinary conditions and are non-biodegradable.'),
('Suggest two measures to reduce fertiliser runoff.','Controlled quantity/timing of fertiliser; vegetated buffers or runoff interception before it enters the lake.'),
('Give separate management routes for peels, paper and batteries.','Peels: compost/appropriate biogas process. Clean paper: reuse/recycle. Batteries: authorised separate collection/recovery. Segregation avoids contamination and improves recovery.')]),
]

def case(topic,n,label):
    r=rng('structured-bio',n+topic*100);x=r.randint(12,40);rate=r.randint(60,90);volume=r.randint(60,85);rounds=r.randint(3,7);chrom=r.choice([8,12,16,24])
    if topic==6:
        context=f'Tallness T is dominant over dwarfness t in a pea-plant model. Two heterozygotes are crossed. Use Mendelian segregation and a large population.'
        rows=[('Name the alternative form of a gene.','Allele.'),('Write parental genotypes and their gametes.','Tt×Tt; each parent produces T and t.'),('Give genotypic and phenotypic ratios.','TT:Tt:tt=1:2:1; tall:dwarf=3:1.'),(f'Calculate the expected dwarf number among {4*x} offspring. Explain whether this number is guaranteed.',f'{4*x}/4={x}. It is an expectation; random segregation can give a different actual count.'),('Explain a test cross distinguishing TT and Tt, including what an all-tall small sample can establish.','Cross with tt. TT gives all Tt; Tt gives expected 1:1 tall:dwarf. A dwarf demonstrates a t allele in the tall parent; an all-tall small sample does not conclusively establish TT.')]
    elif topic==7:
        context=f'A model heart beats {rate} times/min with stroke volume {volume} mL.'
        rows=[('Name the natural pacemaker.','Sinoatrial node.'),('Distinguish pulmonary artery and pulmonary veins.','Artery: deoxygenated blood from right ventricle to lungs. Veins: oxygenated blood from lungs to left atrium.'),('Why is the left ventricle more muscular than the right?','It generates greater pressure for the systemic circuit; the right pumps through the shorter lower-pressure pulmonary circuit.'),('Calculate cardiac output in L/min.',f'{rate}×{volume}={rate*volume} mL/min={rate*volume/1000} L/min.'),('Trace blood from the venae cavae to the aorta, naming the chambers in order.','Venae cavae → right atrium → tricuspid valve → right ventricle → pulmonary artery → lungs → pulmonary veins → left atrium → bicuspid valve → left ventricle → aorta. Credit chamber order, lung circuit and systemic exit.')]
    elif topic==8:
        context=f'One diploid cell with {chrom} chromosomes completes {rounds} successive rounds of mitosis. Every cell divides and none dies.'
        rows=[('Name the stage with chromosomes at the equator.','Metaphase.'),('Calculate cell number and chromosome number in each daughter cell.',f'2^{rounds}={2**rounds} cells; each retains {chrom} chromosomes.'),('Distinguish chromosome and chromatid at metaphase.','One replicated chromosome has two sister chromatids joined at a centromere; while joined they count as one chromosome.'),('Give two functions of mitosis in a multicellular organism.','Growth by increasing cell number; repair/replacement of damaged or worn-out cells.'),('Compare mitosis and meiosis using divisions, products and chromosome number.','Mitosis: one division, usually two cells, parental chromosome number maintained. Meiosis: two divisions, usually four haploid products, half the diploid chromosome number.')]
    elif topic==9:
        start=r.randint(10,25);end=start+r.randint(2,6);context=f'A potato strip increases from {start} g to {end} g in dilute solution. An identical strip loses mass in concentrated sugar solution. Both are blotted before weighing.'
        rows=[('Name the main process causing the changes.','Osmosis.'),('Explain the first strip’s mass gain.','Water enters cells from the more dilute external solution across selectively permeable membranes, down the water-potential gradient.'),('Describe water movement and the cell-state change in concentrated solution.','Water leaves the cells; turgor decreases. Sufficient water loss produces plasmolysis, with protoplast withdrawal from the wall.'),('Calculate percentage mass gain and explain blotting.',f'Gain=({end}−{start})/{start}×100={(end-start)/start*100:.2f}%. Blotting removes adhering solution that would alter measured mass.'),('Give three controls for a fair comparison.','Comparable tissue and equal initial dimensions; same duration; same temperature. Accept equal solution volume and consistent blotting. Concentration is the variable changed.')]
    else:context,rows=CASES[topic]
    return dict(label=str(label),prompt=context,marks=10,parts=[dict(prompt=q,answer=a,marks=m) for (q,a),m in zip(rows,[1,2,2,2,3])])

def long_choices(n):return [case((n-1+i)%10,n,3+i) for i in range(6)]
def compulsory(n):
    result=[]
    for i in range(5):
        full=case((n+2*i)%10,n,'');result.append(dict(prompt=full['prompt'],marks=5,parts=[full['parts'][2],full['parts'][4]]))
    return result
