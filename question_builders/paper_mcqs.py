"""Original conceptual distractors; answer order is shuffled per paper."""
from .common import item, rng

ROWS={
'chem':'''Across a period, atomic size generally|decreases|increases uniformly|remains exactly constant|becomes zero
Down a group, metallic character generally|increases|decreases|is absent in every element|has no relation to electron loss
A covalent bond involves|sharing of electron pairs|transfer of protons|sharing of neutrons|loss of every electron
Molten lead bromide conducts because it contains|mobile ions|free neutral molecules only|moving protons in nuclei|solid metal particles only
During electrolysis of molten lead bromide, the cathode product is|lead|bromine|oxygen|hydrogen
In copper electrorefining, the impure copper is used as the|anode|cathode|electrolyte solvent|insulator
An ammonium salt warmed with alkali releases|ammonia|chlorine|oxygen|nitrogen dioxide
A blue precipitate with sodium hydroxide suggests|copper(II) ions|iron(III) ions|calcium ions|ammonium ions
A reddish-brown precipitate with sodium hydroxide suggests|iron(III) ions|zinc ions|lead(II) ions|ammonium ions
The catalyst in the Haber process is|finely divided iron|vanadium(V) oxide|manganese dioxide|platinum gauze
The catalyst in the Contact process is|vanadium(V) oxide|iron filings|nickel|copper turnings
Concentrated sulphuric acid chars sugar mainly through|dehydration|neutralisation|simple dilution|precipitation
Hydrogen chloride is collected by upward displacement of air because it is|denser than air and very soluble in water|lighter than air and insoluble|a solid|less dense than hydrogen
The brown gas from copper and concentrated nitric acid is|nitrogen dioxide|nitrogen monoxide|hydrogen|ammonia
The functional group of an alcohol is|hydroxyl|carboxyl|aldehyde|ketone
Ethene decolourises bromine solution mainly through|addition|neutralisation|sublimation|fermentation
Oxidation of ethanol under suitable conditions can produce|ethanoic acid|methane|sodium ethoxide only|ethyne
The two structural isomers of C4H10 differ in|carbon-chain arrangement|molecular formula|number of carbon atoms|relative molecular mass
An amphoteric oxide reacts with|both acids and suitable bases|neither acids nor bases|only water|only oxygen
Aluminium is extracted by electrolysis rather than carbon reduction because|its oxide is too stable for ordinary carbon reduction|it is less reactive than copper|it is liquid at room temperature|its ore contains no oxygen''',
'phy':'''The turning effect of a force depends on its|perpendicular distance from the pivot|distance along its own line alone|speed alone|temperature alone
A couple has|zero resultant force and a turning effect|zero moment in every case|one force only|two unequal parallel forces by definition
In a series circuit the same quantity through each resistor is|current|potential difference in every case|resistance|electrical power in every case
For resistors in parallel the same quantity across each branch is|potential difference|current in every case|resistance|power in every case
A fuse is connected in the|live wire in series with the appliance|earth wire only|neutral wire in parallel with the appliance|insulated casing only
For a given potential difference, an appliance with greater rated power draws|greater current|less current in every case|zero current|the same current irrespective of power
An ideal transformer requires|changing magnetic flux|steady DC flux only|no primary current|a permanent open secondary with no induction
Total internal reflection requires travel from|optically denser to rarer medium above critical angle|rarer to denser medium at any angle|vacuum to glass above any angle|any medium at normal incidence
The power of a concave lens is|negative|positive|always zero|measured in amperes
The frequency of a sound wave chiefly determines|pitch|loudness alone|speed in a fixed medium alone|echo distance
The minimum total travel distance for an echo is based on|the outward and return path|only the outward path|only the obstacle thickness|the wavelength alone
During melting of pure ice at constant pressure, heat supplied ideally changes|state without increasing temperature|temperature only|mass into charge|the freezing point continuously
The most penetrating of alpha, beta and gamma radiations is|gamma|alpha|beta in every material|all are identical
Alpha emission reduces mass number by|4|2|1|0
Electrical energy in the commercial unit is measured in|kilowatt-hour|kilowatt per hour|ampere per second|volt per metre
Efficiency of an ordinary real machine is|less than 100 percent|greater than 100 percent|always exactly 100 percent|unrelated to input energy''',
'bio':'''The site of ultrafiltration is|glomerulus into Bowman’s capsule|collecting duct into ureter|loop of Henle into pelvis|renal vein into bladder
An increase in ADH normally causes|greater water reabsorption|less water reabsorption|more glucose filtration|cessation of filtration
The valve between the left atrium and left ventricle is|bicuspid valve|tricuspid valve|pulmonary valve|aortic valve
The vessel carrying oxygenated blood from the lungs is|pulmonary vein|pulmonary artery|vena cava|hepatic portal vein
Which blood component is primarily responsible for clotting?|platelets|erythrocytes|plasma water|lymphocytes
The organelle associated directly with aerobic ATP production is|mitochondrion|ribosome|lysosome|Golgi apparatus
Opening of stomata is associated with|turgid guard cells|flaccid guard cells|loss of chlorophyll|death of epidermis
Which process requires a selectively permeable membrane?|osmosis|evaporation|simple mixing of gases|burning
A destarched plant is used in a photosynthesis test to|remove previously stored starch|remove chlorophyll|kill its leaves|stop all respiration permanently
The chemical used to remove carbon dioxide in a photosynthesis experiment is|potassium hydroxide|iodine solution|ethanol|dilute starch solution
Growth of a shoot towards unilateral light is|positive phototropism|negative phototropism|positive geotropism|negative hydrotropism
The plant hormone that promotes cell division is|cytokinin|adrenaline|thyroxine|insulin
The hormone that lowers blood glucose is|insulin|glucagon|adrenaline|thyroxine
The gland producing thyroxine is|thyroid|adrenal medulla|pituitary posterior lobe|pancreatic exocrine tissue
The part of the brain chiefly coordinating balance is|cerebellum|cerebrum|hypothalamus|spinal nerve
The sensory cells of the retina are|rods and cones|cilia and villi|nephrons and axons|platelets and fibres
The usual site of fertilisation in humans is|oviduct|uterine wall|vagina|ovary surface
The placenta mainly provides|exchange between maternal and fetal circulations|direct mixing of all maternal and fetal blood|formation of eggs|storage of urine
Meiosis produces cells with|half the parental chromosome number|twice the parental chromosome number|no chromosomes|unchanged number in all cases
The phenotypic ratio in an independently assorting dihybrid F2 is|9:3:3:1|1:2:1:2|3:1:3:1|1:1:1:1 in every cross
Which is a biodegradable waste?|vegetable peel|glass shard|plastic wrapper|aluminium foil
The sequence carrying an impulse away from a sensory receptor begins with|sensory neuron|motor end plate|effector muscle|motor neuron
Which human activity directly promotes eutrophication?|fertiliser runoff into a lake|segregating dry paper|rainwater storage|planting a shelter belt
An allele that expresses in the heterozygous condition is|dominant|always lethal|necessarily sex-linked|recessive by definition''',
'histciv':'''A no-confidence motion against the Union government is moved in the|Lok Sabha|Rajya Sabha alone|Supreme Court|Election Commission
The normal term of the Lok Sabha is|five years|six years|four years|permanent with retiring thirds
A Money Bill can be introduced only in the|Lok Sabha|Rajya Sabha|Supreme Court|State High Court
The ex-officio Chairman of the Rajya Sabha is the|Vice-President|Prime Minister|President|Lok Sabha Speaker
The formal head of the Union executive is the|President|Chief Justice|Cabinet Secretary|Speaker
The Council of Ministers is collectively responsible to the|Lok Sabha|Supreme Court|President’s electoral college|Rajya Sabha alone
Habeas corpus is chiefly a protection against|unlawful detention|unpaid income tax|defeat in an election|loss in a civil contract
Judicial review examines the|constitutional validity of law or executive action|profitability of companies|membership of political parties only|merits of every parliamentary speech
The immediate military grievance associated with the 1857 uprising concerned|greased cartridges|the Salt Law|the Vernacular Press Act|the Rowlatt Act
The Doctrine of Lapse was associated with|Dalhousie|Mountbatten|Ripon|Wavell
The Government of India Act 1858 transferred rule to the|British Crown|Indian National Congress|United Nations|French government
The Indian National Congress was founded in|1885|1857|1905|1919
The partition of Bengal in 1905 is associated with|Curzon|Ripon|Mountbatten|Dalhousie
The Muslim League was founded in|1906|1885|1916|1942
The Non-Cooperation Movement was withdrawn after|Chauri Chaura|Dandi March|Cabinet Mission|Mountbatten Plan
The Salt March began in|1930|1919|1922|1942
The Quit India resolution was adopted in|1942|1930|1920|1947
The Indian Independence Act provided for|two independent dominions|continued Company rule|a permanent single British province|a new League of Nations
The assassination at Sarajevo was the immediate trigger of|First World War|Second World War|Cold War|Korean War
The Treaty of Versailles was imposed principally upon|Germany|Japan|Italy alone|the United States
The invasion of Poland in 1939 triggered|Second World War in Europe|First World War|Russian Revolution|formation of the Congress
The permanent organ primarily responsible for international peace and security is the|UN Security Council|UNESCO executive office|World Health Assembly|NAM secretariat
The UN agency chiefly concerned with world health is|WHO|UNESCO|ILO|FAO
Non-alignment implies|independent judgement outside military power blocs|isolation from all world affairs|automatic support for one bloc|refusal to join the UN''',
'geo':'''Black soil retains moisture mainly because it is|clayey|coarse gravel|pure sand|solid granite
The newer alluvium is known as|Khadar|Bhangar|Regur|Laterite
Laterite develops most strongly under|heavy rain and leaching|permanent ice|no rainfall|marine salinity alone
Contour ploughing helps to|reduce runoff on slopes|increase gully erosion|remove soil cover|eliminate all rainfall
Mangrove vegetation is associated with|tidal coastal areas|alpine snowfields|hot bare deserts|deep ocean floors
Tropical evergreen forests are generally|dense and multi-layered|leafless in every month|pure stands of a single tree everywhere|confined to cold deserts
Deep roots in desert plants help them to|reach scarce water|increase water loss|prevent all growth|avoid minerals
Drip irrigation supplies water|near the root zone in small quantities|only by complete field flooding|only through river canals|as seawater spray
Rainwater recharge pits help to|replenish groundwater|create coal deposits|stop evaporation entirely|increase marine tides
Canal irrigation is favoured in much of the northern plains by|level land and perennial rivers|steep rocky slopes alone|absence of rivers|permanent frost
The main June–September rain-bearing winds are the|southwest monsoon|polar easterlies|land breeze only|western disturbances only
Chennai receives important rainfall during|retreating/northeast monsoon months|only the hottest pre-monsoon week|the snowfall season|no season
The Deccan rain-shadow lies chiefly to the|east of the Western Ghats|west of the Western Ghats in the sea|north of the Himalayas|centre of the Bay of Bengal
A kharif crop is commonly sown with the onset of|summer monsoon|winter frost|spring snowmelt alone|retreating trade winds in April
Tea is damaged by|stagnant water around roots|well-distributed rain|a moist climate|well-drained slopes
Cotton textile centres near Mumbai historically benefited from|port access and a humid climate|permanent ice|absence of markets|lack of labour
The most flexible door-to-door transport mode is|road|rail|ocean shipping|air trunk routes
Large regular long-distance bulk loads are often suited to|rail transport|bicycle courier only|helicopter only|hand carriage
Inland waterways are limited by|navigable depth and route availability|an inability to carry any heavy cargo|a need for mountain rails|the absence of terminals everywhere
The best route for clean segregated vegetable waste is|composting or suitable biogas processing|open burning with batteries|mixing with medical sharps|dumping in a stream
Used batteries should be sent to|authorised separate recovery channels|a food compost heap|an open playground fire|a riverbank
The first step in effective waste recovery is|segregation at source|mixing all waste|adding drain water|removing collection bins
An example of renewable energy is|solar energy|coal|petroleum|natural gas
An example of a ferrous mineral is|iron ore|bauxite|limestone|mica''',
'english2':'''Who permits Antony to speak at Caesar’s funeral under conditions?|Brutus|Portia|Pindarus|Strato
Who interprets Titinius’s reception by soldiers incorrectly?|Pindarus|Cinna the poet|Lucius|Octavius
Who holds the sword for Brutus at the end?|Strato|Titinius|Caesar|Metellus Cimber
The dispute over Lucius Pella chiefly concerns|bribery|a marriage proposal|a lost crown|a forged will
Caesar’s ghost promises another meeting at|Philippi|Athens|Sardinia|Alexandria
Which character defends Brutus’s honour after his death?|Antony|Portia|Pindarus|Calpurnia
The photographer and narrator disagree chiefly about|likeness versus imposed improvement|the price of a train ticket|a missing letter|ownership of a camera
Martin’s central fear concerns|the elevator and its disturbing encounters|a forest expedition|a school election|a sea voyage
Adjoa’s achievement is in|running|painting portraits|playing the violin|writing a newspaper
Nana initially judges Adjoa’s legs by|traditional expectations of a woman’s body|a medical examination described in detail|a race already won|the cost of shoes
Leonard Mead is detained while|walking at night|driving a racing car|robbing a bank|repairing a television
The police vehicle in The Pedestrian is|automated|drawn by horses|driven by Mead|a private taxi
Franz’s unprepared school exercise concerns|participles|fractions|Roman history|musical scales
The official order in The Last Lesson ends the teaching of|French|Latin everywhere|all subjects|German
The title Haunted Houses chiefly develops the idea of|continuity of past lives in familiar places|a detective’s murder investigation|a war at sea|the invention of a machine
In The Glove and the Lions, the lady seeks a public|test of her lover’s devotion|vote for a new king|lesson in medicine|proof of the king’s poverty
The lover’s final rejection chiefly asserts|self-respect over a vain demand|fear preventing any action|hatred of all spectators|ignorance of danger
The great trees metaphorically suggest|influential lives whose loss affects others|a forestry instruction manual|only a change in weather|a comic musical performance
The speck’s movement makes the speaker recognise|apparently purposeful intelligence|a chemical formula|a printed correction|a mechanical clock
Who ends the singer’s performance in The Power of Music?|a goat|a royal judge|Martin’s father|a photographer'''
}

def make_mcqs(sid,seed,count,extra=()):
    pool=[]
    for i,line in enumerate(ROWS.get(sid,'').splitlines()):
        if not line:continue
        prompt,*opts=line.split('|');correct=opts[0];order=opts[:];rng(f'{sid}-options-{i}',seed).shuffle(order)
        pool.append(item('Compulsory MCQ',prompt,correct,1,id=f'{sid}-mcq-{i}',options=order,correct=order.index(correct)))
    pool+=list(extra);rng(sid+'mcqs',seed).shuffle(pool)
    assert len(pool)>=count,(sid,len(pool),count)
    return pool[:count]
