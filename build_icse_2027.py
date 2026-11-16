"""Build the student pack, evidence guide and browser data from reviewed content.

Run: python -X utf8 build_icse_2027.py
No downloads or external writes. OCR classifications stay explicitly provisional.
"""
import csv, hashlib, json, re
from pathlib import Path
from icse_2027_content import *

ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT / 'research'
RESEARCH.mkdir(exist_ok=True)
CORPUS = RESEARCH / 'corpus'
SEEDS = json.loads((ROOT / 'icse_hindi_seed_data.json').read_text(encoding='utf-8'))
MANIFEST = json.loads((CORPUS / 'manifest.json').read_text(encoding='utf-8'))
SYLLABUSES = json.loads((CORPUS / 'syllabus_manifest.json').read_text(encoding='utf-8'))
SPECIMENS = json.loads((CORPUS / 'specimen_manifest.json').read_text(encoding='utf-8'))

# Start pages inspected in the scanned images after OCR damaged headings.
# This confirms location only; it does not certify all subparts or their marking.
PAGE_CORRECTIONS = {
 'board_bio_2023': {5:8,6:9},
 'board_chem_2023': {3:6,8:10},
 'board_chem_2025': {3:9,4:10,5:11,6:13,7:14},
 'board_computer_2025': {4:11,5:11,7:12,8:12},
 'board_geo_2023': {5:6,7:7,11:9},
 'board_geo_2024': {8:8,11:9},
 'board_geo_2025': {5:7,7:9},
 'board_histciv_2024': {6:7},
 'board_histciv_2025': {4:9,6:10,7:11,10:12},
 'board_maths_2025': {8:13,9:14,10:15},
 'board_phy_2023': {9:10},
 'board_phy_2024': {5:8,7:9,9:12},
 'board_phy_2025': {4:10,5:11,9:16},
}

def save(name, value):
    (ROOT / name).write_text(value, encoding='utf-8')

def table(headers, rows):
    clean=lambda x: str(x).replace('|','/').replace('\n','<br>')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(clean,r))+' |' for r in rows])+'\n'

def add(bank, subject, topic, marks, difficulty, prompt, answer, **extra):
    q=dict(id=f'{subject}-{len(bank[subject])+1:03}',topic=topic,marks=int(marks),difficulty=difficulty,prompt=prompt,answer=answer,**extra)
    bank[subject].append(q)
    return q

BANK={key:[] for key in SUBJECTS}
for key, text in PRACTICE_TEXT.items():
    for line in text.strip().splitlines():
        add(BANK,key,*line.split('|',4))
for title, kind, prompt, answer in ENGLISH_TEXTS:
    add(BANK,'english2',title,8,'Medium',prompt,answer,book=kind)

# Hindi original writing prompts retained where useful; count each only once.
for kind, prompts in SEEDS['compositionTypes']:
    for prompt in prompts:
        add(BANK,'hindi','रचना: '+kind,15,'Medium',prompt+' लगभग 250 शब्द लिखिए।','विषय से स्पष्ट संबंध, क्रमबद्ध विचार/घटनाएँ, उपयुक्त अनुच्छेद, भाषा और शुद्ध वर्तनी।',category='writing')
for difficulty,prompt in SEEDS['letters']:
    add(BANK,'hindi','पत्र',7,difficulty,prompt+' लगभग 120 शब्द लिखिए।','पता, तिथि, उपयुक्त संबोधन, उद्देश्य, आवश्यक विवरण, विनम्र भाषा और समापन।',category='writing')

# Short-answer grammar avoids ambiguous automatic distractors. No last-year blacklist.
LABELS={'vilom':'विलोम','paryay':'पर्यायवाची','bhav':'भाववाचक संज्ञा','visheshan':'विशेषण','muhavara':'मुहावरे का अर्थ','oneword':'एक शब्द','vakya':'वाक्य-शुद्धि'}
for kind,label in LABELS.items():
    for source,answer in SEEDS['grammarData'][kind]:
        if kind=='paryay' and source=='दिन': answer='दिवस / वासर'
        if kind=='vilom' and source=='साहस': answer='कायरता'
        if kind=='paryay' and source=='बालक': continue
        if kind=='bhav' and source=='धनी': continue
        if kind=='oneword' and source=='जो देखा न गया हो': source='जो दिखाई न दे'
        if kind=='oneword' and source=='जो सबके लिए समान हो': source='जो सब लोगों के लिए हो'
        if kind=='vakya' and (source==answer or source in ('यह काम मेरे द्वारा किया गया।','मैंने पुस्तक को पढ़ा।')): continue
        if kind=='vakya' and source=='सीता ने आम खाया और वह मीठी थी।': source='यह आम बहुत मीठी है।'; answer='यह आम बहुत मीठा है।'
        prompt=f'{label}: {source}'
        add(BANK,'hindi','व्याकरण: '+label,1,'Normal',prompt,answer,category='grammar')

# Board-style grammar: explicit single correct option and a balanced answer position.
MCQS = [
 ('विलोम','“उन्नति” का विलोम चुनिए।',['प्रगति','अवनति','सफलता','विकास'],1),
 ('विलोम','“स्थायी” का विलोम चुनिए।',['अस्थायी','स्थिर','नियमित','निश्चित'],0),
 ('पर्यायवाची','“वर्षा” का पर्याय चुनिए।',['पवन','प्रभात','वृष्टि','पर्वत'],2),
 ('पर्यायवाची','“वस्त्र” का पर्याय चुनिए।',['पात्र','पथ','पत्र','परिधान'],3),
 ('भाववाचक संज्ञा','“कमाना” की भाववाचक संज्ञा चुनिए।',['कम','कमाना','कमाई','कमल'],2),
 ('भाववाचक संज्ञा','“मूर्ख” की भाववाचक संज्ञा चुनिए।',['मूर्खता','मूर्खतापूर्ण','मूर्ख व्यक्ति','मूर्खों'],0),
 ('विशेषण','“पत्थर” से बना विशेषण चुनिए।',['पत्थरशिला','पथरीला','पत्थरपन','पत्थरीकरण'],1),
 ('विशेषण','“नीति” से बना विशेषण चुनिए।',['नियति','नियम','नेता','नैतिक'],3),
 ('शुद्ध वर्तनी','शुद्ध वर्तनी चुनिए।',['आवस्यकता','आवश्यकता','आवशकता','आवशक्यता'],1),
 ('शुद्ध वर्तनी','शुद्ध वर्तनी चुनिए।',['कृतग्य','कृत्तज्ञ','कृतज्ञ','कृतज्ञय'],2),
 ('शुद्ध वर्तनी','शुद्ध वर्तनी चुनिए।',['श्रेष्ठ','श्रेष्ट','श्रेषठ','श्रेठ'],0),
 ('शुद्ध वर्तनी','शुद्ध वर्तनी चुनिए।',['पतीव्रता','पतिवर्ता','पतिब्रता','पतिव्रता'],3),
 ('मुहावरे','“उन्नीस-बीस का अंतर” का अर्थ चुनिए।',['बहुत बड़ा अंतर','बहुत कम अंतर','पूरी समानता','गिनती भूलना'],1),
 ('मुहावरे','“आग में घी डालना” का अर्थ चुनिए।',['शांत करना','भोजन पकाना','विवाद और बढ़ाना','सहायता देना'],2),
 ('मुहावरे','“आँखों का तारा” का अर्थ चुनिए।',['बहुत प्रिय व्यक्ति','दृष्टि की कमजोरी','आकाश का तारा','क्रोधित व्यक्ति'],0),
 ('मुहावरे','“हाथ मलना” का अर्थ चुनिए।',['सफाई करना','तैयार होना','बधाई देना','पछताना'],3),
 ('एक शब्द','“जिसे गुप्त रखा जाना आवश्यक हो” के लिए एक शब्द चुनिए।',['गुप्तचर','गोपनीय','रहस्यमयी','अदृश्य'],1),
 ('एक शब्द','“जो देखने योग्य हो” के लिए एक शब्द चुनिए।',['पठनीय','श्रवणीय','दर्शनीय','स्मरणीय'],2),
 ('वाक्य-शुद्धि','संदर्भानुसार सही शब्द चुनिए: रोगी की ___ ठीक नहीं है।',['दशा','दिशा','दया','दूरी'],0),
 ('वाक्य-शुद्धि','शुद्ध वाक्य चुनिए।',['राम और श्याम गया।','राम और श्याम जाती है।','राम और श्याम जाते हूँ।','राम और श्याम गए।'],3),
]
for label,prompt,options,correct in MCQS:
    add(BANK,'hindi','व्याकरण MCQ: '+label,1,'Normal',prompt+'\n'+'\n'.join(f'({chr(97+i)}) {x}' for i,x in enumerate(options)),f'({chr(97+correct)}) {options[correct]}',category='grammar',options=options,correct=correct)

for book,title,cue,check in HINDI_TEXTS:
    # No invented textbook quotations. These are whole-text revision exercises.
    questions=[f'पाठ के मुख्य पात्र/वक्ता या काव्य-स्थिति का परिचय दीजिए। [2]',f'इस विषय का पाठ में संदर्भ स्पष्ट कीजिए: {cue}। [2]',f'इसी विषय को विकसित करने वाले दो उदाहरण पाठ से देकर समझाइए। [3]',f'पाठ के शीर्षक अथवा मुख्य संदेश से इस विषय का संबंध तर्क सहित स्पष्ट कीजिए। [3]']
    add(BANK,'hindi',title,10,'Medium','\n'.join(questions),'उत्तर-जाँच: '+check,category='literature',book=book,parts=[2,2,3,3],cue=cue)
for start,end in [(14,17),(18,21),(22,26)]:
    add(BANK,'hindi',f'नया रास्ता: अध्याय {start}–{end}',10,'Medium',f'अपने पाठ्यपुस्तक के अध्याय {start}–{end} से एक निर्णायक घटना चुनिए।\n(i) पात्र और परिस्थिति का परिचय दीजिए। [2]\n(ii) घटना का कारण समझाइए। [2]\n(iii) निर्णय और उसके परिणाम को दो पाठ-आधारित बिंदुओं से समझाइए। [3]\n(iv) इस घटना का पात्र-विकास या उपन्यास के संदेश में योगदान बताइए। [3]','शिक्षक चुनी घटना और अध्याय की जाँच करें। नाम, क्रम, कारण और परिणाम पाठ से मिलाएँ। यह किसी विशिष्ट सर्ग में गढ़ी हुई घटना या उद्धरण नहीं है।',category='literature',book='नया रास्ता',parts=[2,2,3,3])

HINDI_PASSAGES = [
 {'title':'पुस्तकालय का नया प्रयोग','text':'विद्यालय के पुस्तकालय में कई पुस्तकें वर्षों से बंद अलमारियों में रखी थीं। बच्चों को डर था कि पुरानी पुस्तक को छूने से उसके पन्ने टूट जाएँगे। पुस्तकालयाध्यक्ष ने एक दिन छोटा समूह बुलाया और सावधानी से पुस्तक पकड़ने का तरीका सिखाया। समूह ने पुरानी यात्रा-कथाओं में अपने शहर के वर्णन खोजे। उन्हें पता चला कि जिस सड़क पर आज दुकानें हैं, वहाँ कभी पेड़ों की लंबी कतार थी। बच्चों ने अपने दादा-दादी से उन पेड़ों के बारे में पूछा और उनकी यादें लिखीं। कुछ बातें पुस्तक से मिलती थीं, कुछ अलग थीं। अध्यापिका ने समझाया कि किसी एक स्मृति को अंतिम सत्य मानना उचित नहीं; दूसरे प्रमाण भी खोजने चाहिए। बच्चों ने पुस्तक के चित्रों, परिवारों की यादों और वर्तमान तस्वीरों की एक प्रदर्शनी बनाई। इस काम से उन्हें पढ़ने के साथ प्रश्न पूछना भी आया। अब वे पुरानी पुस्तक को बेकार वस्तु नहीं, समय को समझने का साधन मानते थे। पुस्तकालयाध्यक्ष ने भी निश्चय किया कि संरक्षण का अर्थ हर पुस्तक को बंद रखना नहीं, उसके सुरक्षित उपयोग की व्यवस्था करना है।',
 'tasks':[('बच्चे पुरानी पुस्तकें छूने से क्यों डरते थे?','पन्ने टूटने की आशंका थी।'),('समूह ने पुस्तक में क्या खोजा और क्या परिवर्तन जाना?','शहर का वर्णन; पेड़ों की कतार के स्थान पर दुकानें।'),('अध्यापिका ने स्मृतियों की जाँच के विषय में क्या सलाह दी?','एक स्मृति को अंतिम सत्य न मानें; अन्य प्रमाण खोजें।'),('प्रदर्शनी में किन तीन प्रकार की सामग्री का उपयोग हुआ?','पुस्तक के चित्र, परिवारों की यादें और वर्तमान तस्वीरें।'),('गद्यांश का उपयुक्त शीर्षक लिखिए तथा उसका कारण बताइए।','सार्थक शीर्षक और सुरक्षित उपयोग/अतीत को समझने से स्पष्ट संबंध; अन्य उचित उत्तर स्वीकारें।')]},
 {'title':'जल बचाने की समझ','text':'गर्मी में नगर के एक विद्यालय को हर दोपहर पानी की कमी का सामना करना पड़ता था। पहले बच्चों ने सोचा कि बड़ी टंकी खरीद लेने से समस्या समाप्त हो जाएगी। विज्ञान अध्यापक ने कहा कि समाधान चुनने से पहले पानी का उपयोग समझना जरूरी है। एक सप्ताह तक बच्चों ने रसोई, शौचालय और बगीचे में पानी के उपयोग का लेखा रखा। उन्हें तीन खराब नल मिले, जिनसे लगातार बूंदें गिरती थीं। माली पौधों को दोपहर में पानी देता था, जब तेज धूप के कारण काफी पानी जल्दी सूख जाता था। मरम्मत के बाद नलों से रिसाव बंद हुआ और बगीचे में पानी देने का समय सुबह कर दिया गया। विद्यालय ने छत से बहने वाले वर्षा-जल को एक टंकी में एकत्र करने की योजना भी बनाई। बच्चों ने स्पष्ट किया कि यह पानी बिना उचित उपचार के पीने के लिए उपयोग नहीं होगा। अगले महीने पानी की खपत घटी। इससे बच्चों ने सीखा कि संसाधन बचाने के लिए केवल नारा पर्याप्त नहीं होता; सही जानकारी, छोटा सुधार और नियमित जाँच भी आवश्यक हैं।',
 'tasks':[('बच्चों ने आरंभ में कौन-सा समाधान सोचा?','बड़ी टंकी खरीदना।'),('अध्यापक ने समाधान चुनने से पहले क्या करने को कहा?','पानी का उपयोग समझना/लेखा रखना।'),('जाँच में कौन-सी दो समस्याएँ मिलीं?','तीन रिसते नल; तेज धूप में बगीचे को पानी देना।'),('वर्षा-जल के उपयोग में कौन-सी सावधानी बताई गई?','उचित उपचार के बिना पीने के लिए उपयोग नहीं।'),('अंतिम वाक्य के आधार पर संसाधन-संरक्षण के तीन आवश्यक उपाय लिखिए।','सही जानकारी, छोटा सुधार और नियमित जाँच।')]},
 {'title':'सच्ची टीम','text':'विद्यालय की नाटक प्रतियोगिता में रिया को मुख्य भूमिका मिली थी। उसने संवाद याद कर लिए, पर अभ्यास के समय दूसरे पात्रों की बातें ध्यान से नहीं सुनती थी। उसे लगता था कि उसके बोलते ही दर्शक प्रभावित हो जाएँगे। एक दिन मंच पर साथी अपना संवाद भूल गया। रिया ने तुरंत अगला संवाद बोल दिया, जिससे कहानी का क्रम बिगड़ गया। निर्देशक ने किसी को डाँटने के बजाय सबको बताया कि नाटक केवल अलग-अलग अच्छे संवादों का संग्रह नहीं है। हर पात्र को दूसरे की बात सुनकर सही समय पर प्रतिक्रिया देनी होती है। अगले अभ्यास में रिया ने साथियों के संवाद भी समझे और संकेतों पर ध्यान दिया। मंच-सज्जा करने वाले बच्चों के काम को भी उसने पहली बार गंभीरता से देखा। प्रतियोगिता के दिन एक पर्दा अटक गया, लेकिन कलाकारों ने थोड़ी देर सहज बातचीत जारी रखी और दर्शकों का ध्यान भटकने नहीं दिया। दल को दूसरा पुरस्कार मिला। रिया पहले स्थान से अधिक इस बात पर प्रसन्न थी कि उन्होंने कठिनाई को मिलकर संभाला। उसे समझ आया कि सफलता में दिखाई देने वाली भूमिका के साथ अनेक अनदेखे प्रयास भी शामिल होते हैं।',
 'tasks':[('रिया आरंभ में किस बात की उपेक्षा करती थी?','दूसरे पात्रों के संवाद सुनने/समझने की।'),('उसके तुरंत अगला संवाद बोलने से क्या हुआ?','कहानी का क्रम बिगड़ा।'),('निर्देशक ने अच्छे नाटक की कौन-सी शर्त बताई?','एक-दूसरे को सुनकर सही समय पर प्रतिक्रिया।'),('प्रतियोगिता में पर्दा अटकने पर दल ने क्या किया?','सहज बातचीत जारी रखकर दर्शकों का ध्यान बनाए रखा।'),('रिया को पुरस्कार से अधिक किस बात की खुशी थी और क्यों?','कठिनाई मिलकर संभालने की; सहयोग व अनदेखे प्रयासों का महत्व समझा।')]},
]
for passage in HINDI_PASSAGES:
    add(BANK,'hindi','अपठित गद्यांश',10,'Medium',passage['text']+'\n\n'+'\n'.join(f'({i+1}) {q} [2]' for i,(q,a) in enumerate(passage['tasks'])),'\n'.join(f'({i+1}) {a}' for i,(q,a) in enumerate(passage['tasks'])),category='reading',parts=[2]*5)
for q in BANK['english1']:
    if q['topic']=='Reading and summary':
        q['prompt']=ENGLISH_READING+'\n\n'+'\n'.join(f'({i+1}) {p} [{m}]' for i,(p,m,a) in enumerate(ENGLISH_READING_TASKS))
        q['answer']='\n'.join(f'({i+1}) {a}' for i,(p,m,a) in enumerate(ENGLISH_READING_TASKS))

# Question-level evidence overrides: descriptive families, not copied questions.
COMP = {
 2023:['Theory/MCQ','Theory/output','Student class','Bubble sort','Method overloading','String character classification','Linear search','Array/digit-size sums'],
 2024:['Theory/MCQ','Theory/output','BookFair class','Method overloading','EvenPal digit logic','2D diagonal sums','Selection sort','String email validation'],
 2025:['Theory/MCQ','Theory/output','CloudStorage slab class','2D matrix norm','Upper/lowercase string','Binary search','Method overloading','Digit extrema/parity'],
 2026:['Theory/MCQ','Theory/output','StepTracker class','1D designation frequency scan','2D sparse matrix','Digit Mark test','Method overloading','String word rotation'],
}
ENG2={2023:['MCQs','Old drama','Old drama','Old prose','Old prose','Old poetry','Old poetry'],2024:['MCQs','Old drama','Old drama','Old prose','Old prose','Old poetry','Old poetry'],2025:['MCQs','Julius Caesar III.2','Julius Caesar V.1','The Elevator','The Last Lesson','The Glove and the Lions','A Considerable Speck'],2026:['MCQs','Julius Caesar III.1','Julius Caesar V.3','The Girl Who Can','The Pedestrian','When Great Trees Fall','The Power of Music']}
HINDI_TITLES={
 2023:{5:'Netaji Ka Chashma',6:'Sandeh',7:'Bheden Aur Bhediye',8:'Vah Janmabhumi Meri',9:'Sur Ke Pad',10:'Bhikshuk',11:'Naya Raasta',12:'Naya Raasta',13:'Naya Raasta',14:'Bahu Ki Vida',15:'Matribhoomi Ka Maan',16:'Deepdan'},
 2024:{5:'Apna Apna Bhagya',6:'Bade Ghar Ki Beti',7:'Bheed Me Khoya Aadmi',8:'Chalna Hamara Kaam Hai',9:'Vinay Ke Pad',10:'Megh Aaye',11:'Naya Raasta',12:'Naya Raasta',13:'Naya Raasta',14:'Sanskar Aur Bhavana',15:'Mahabharat Ki Ek Saanjh',16:'Sookhi Dali'},
 2025:{5:'Baat Athanni Ki',6:'Do Kalakar',7:'Kaki',8:'Sakhi',9:'Swarg Bana Sakte Hain',10:'Matri Mandir Ki Or',11:'Bahu Ki Vida',12:'Matribhoomi Ka Maan',13:'Deepdan',14:'Naya Raasta',15:'Naya Raasta',16:'Naya Raasta'},
 2026:{5:'Mahayagya Ka Puraskar',6:'Sandeh',7:'Bheden Aur Bhediye',8:'Vah Janmabhumi Meri',9:'Giridhar Ki Kundaliyan',10:'Sur Ke Pad',11:'Sookhi Dali',12:'Mahabharat Ki Ek Saanjh',13:'Sanskar Aur Bhavana',14:'Naya Raasta',15:'Naya Raasta',16:'Naya Raasta'}
}
KEYWORDS = {
 'maths':{'Commercial':['gst','dividend','recurring','deposit','shares'],'Algebra':['matrix','matrices','quadratic','polynomial','progression','inequation'],'Coordinates':['coordinate','slope','reflect','midpoint'],'Geometry':['circle','tangent','triangle','similar','construct'],'Mensuration':['cone','sphere','cylinder'],'Trigonometry':['elevation','depression','trigonometric','tan','cos','sin'],'Statistics/probability':['histogram','ogive','mean','median','probability','frequency']},
 'phy':{'Mechanics':['moment','couple','pulley','lever','kinetic','potential','efficiency'],'Optics':['lens','refraction','prism','spectrum','radiation','image'],'Sound':['echo','resonance','sound','frequency','vibration'],'Electricity/magnetism':['current','resistance','fuse','circuit','magnetic','generator','transformer'],'Heat':['heat','calorimetry','latent','temperature','capacity'],'Nuclear':['alpha','beta','nuclear','radioactive','fission','fusion']},
 'chem':{'Trends/bonding':['period','electronegativity','covalent','electrovalent','coordinate bond'],'Acids/analysis':['acid','precipitate','hydroxide','ammonium','salt'],'Moles':['mole','molar','stp','empirical','stoichiometry'],'Electrolysis/metallurgy':['electrolysis','electroplating','electrode','bauxite','alloy','ore'],'Compounds':['ammonia','hydrogen chloride','nitric','sulphuric','contact process'],'Organic':['ethanol','ethene','ethyne','alkane','ester','ethanoic','organic']},
 'bio':{'Cell/genetics':['mitosis','meiosis','chromosome','mendel','genotype','allele'],'Plant processes':['transpiration','photosynthesis','stoma','root hair','plasmolysis','turgid'],'Plant coordination':['auxin','gibberellin','cytokinin','tropism','ethylene'],'Human systems':['blood','heart','kidney','nephron','neuron','brain','spinal','hormone','eye','ear','placenta','sperm'],'Evolution':['darwin','lamarck','evolution','homin','melanism','australopithecus'],'Environment/population':['pollution','population','waste','birth rate']},
 'histciv':{'Parliament':['parliament','lok sabha','rajya sabha','speaker'],'Executive':['president','cabinet','prime minister','vice-president'],'Judiciary':['supreme court','high court','jurisdiction','writ'],'Nationalism':['1857','nationalist','congress','gandhi','league','bose','independence','partition'],'World history':['world war','versailles','nazi','fascis','united nations','unesco','unicef','non-aligned']},
 'geo':{'Map work':['grid','contour','topographical','outline map','scale'],'Climate':['monsoon','rainfall','temperature','climate'],'Soils':['soil','erosion'],'Vegetation':['forest','vegetation'],'Water':['irrigation','water','canal'],'Minerals/energy':['coal','petroleum','energy','mineral'],'Agriculture':['crop','rice','wheat','cotton','tea','agriculture'],'Industry':['industry','manufactur','steel','sugar mill'],'Transport':['transport','road','railway','waterway'],'Waste':['waste','compost','recycl']},
 'english1':{'Writing':['composition','letter','notice','email','e-mail'],'Reading':['passage','summary','comprehension'],'Grammar':['verb','preposition','rewrite','join','sentence']},
}

def keyword_tags(subject,text):
    low=text.lower()
    return '; '.join(k for k,words in KEYWORDS.get(subject,{}).items() if any(re.search(r'\b'+re.escape(w),low) for w in words))

LEDGER=[]
coverage=[]
for paper in sorted(MANIFEST,key=lambda x:(x['subject'],x['year'])):
    sid,year=paper['subject'],int(paper['year'])
    raw=(CORPUS/(paper['id']+'.txt')).read_text(encoding='utf-8')
    # Retain marker positions, but never hide unrecoverable headings behind a guessed count.
    matches=list(re.finditer(r'(?im)^\s*(?:Question|auestion|Questio[®n]?|Questiqn)\s*([0-9Il|]+)\b[^\n]*',raw))
    found={}
    last=0
    for match in matches:
        token=match.group(1).replace('I','1').replace('l','1').replace('|','1')
        try: number=int(token)
        except ValueError: continue
        if sid=='hindi' and number==0 and last==9: number=10
        if sid=='hindi' and number<last and 10<=last<16: number+=10
        if 1<=number<=SUBJECTS[sid]['questions'] and number>last:
            found[number]=match
            last=number
    # A complete ordered header sequence can recover damaged numeric glyphs.
    # Reject prose/instruction lines; never fill a partial sequence by guessing.
    candidates=[]
    for match in re.finditer(r'(?m)^\s*(?:Question\w*|auestion|Questiqn|Questi|Quesnel|Questfon|Questios)\b[^\n]*',raw):
        heading=match.group().strip()
        if len(heading)<=30 and not heading.endswith(':'): candidates.append(match)
    expected=SUBJECTS[sid]['questions']
    if sid=='english1' and len(candidates)==expected+1 and '2' in candidates[0].group(): candidates=candidates[1:]
    sequence_complete=len(candidates)==expected
    if sequence_complete: found={n:m for n,m in enumerate(candidates,1)}
    page_markers=list(re.finditer(r'--- PAGE (\d+) ---',raw))
    recovered_pages={}
    for folder in [CORPUS/'ocr'/sid,CORPUS/'recovery']:
        for file in sorted(folder.glob(paper['id']+'_p*.txt')):
            page_num=int(re.search(r'_p(\d+)',file.name).group(1))
            text=file.read_text(encoding='utf-8-sig')
            for match in re.finditer(r'(?im)^\s*(?:Question|auestion|Questio[n®]?|Questiqn)\s*([0-9Il|]+)(?=\s|\[|\(|$)',text):
                token=match.group(1).replace('I','1').replace('l','1').replace('|','1')
                number=int(token)
                if 1<=number<=SUBJECTS[sid]['questions']:
                    recovered_pages.setdefault(number,(page_num,text))
    for n in range(1,SUBJECTS[sid]['questions']+1):
        marker=found.get(n)
        body=''
        page=''
        if marker:
            nexts=[m.start() for num,m in found.items() if num>n]
            body=raw[marker.end():min(nexts) if nexts else len(raw)]
            earlier=[p for p in page_markers if p.start()<=marker.start()]
            page=earlier[-1].group(1) if earlier else ''
        method=('Complete ordered heading sequence; numeric OCR may be corrected' if sequence_complete else 'Primary OCR heading') if marker else 'Unresolved heading'
        if not marker and n in recovered_pages:
            page,body=recovered_pages[n]
            page=str(page)
            method='Alternate OCR heading; page-level tag fallback'
        if n in PAGE_CORRECTIONS.get(paper['id'],{}):
            page=str(PAGE_CORRECTIONS[paper['id']][n])
            body=(CORPUS/'recovery'/f'{paper["id"]}_p{int(page):02}.txt').read_text(encoding='utf-8')
            method='Start page checked in scan; page-level tags provisional'
            if paper['id']=='board_phy_2024' and n==9:
                method='Start page checked by Q8 ending and Q9 subpart sequence; heading cropped'
        tags=keyword_tags(sid,body)
        status='OCR heading recovered; tags provisional' if page else 'OCR heading unresolved; inspect PDF'
        if method.startswith('Start page'): status='Start page checked; page-level tags provisional'
        if sid=='computer': tags=COMP[year][n-1]; status='Program family reviewed; theory not item-by-item verified' if n>2 else status
        if sid=='english2': tags=ENG2[year][n-1]; status='Long-selection reviewed' if n>1 else status
        if sid=='hindi' and n>=5: tags=HINDI_TITLES[year][n];status='Literature title reviewed; subparts not independently marked'
        row={'paper_id':paper['id'],'subject':sid,'year':year,'question':n,'pdf_page':page,'family':tags,'status':status,'extraction_method':method,'url':paper['url']}
        LEDGER.append(row)
    coverage.append({**paper,'status':'downloaded; OCR completed','ocr_chars':len(raw),'expected_main_questions':SUBJECTS[sid]['questions'],'main_questions_located':sum(bool(r['pdf_page']) for r in LEDGER if r['paper_id']==paper['id']),'ocr_headings_recovered':sum(bool(r['pdf_page']) and not r['extraction_method'].startswith('Start page') for r in LEDGER if r['paper_id']==paper['id']),'text_sha256':hashlib.sha256(raw.encode()).hexdigest()})

with (RESEARCH/'question_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(LEDGER[0]));writer.writeheader();writer.writerows(LEDGER)
(RESEARCH/'source_manifest.json').write_text(json.dumps({'review_date':DATE,'papers':coverage,'syllabuses':SYLLABUSES,'prescribed_books':{'url':BOOKS,'status':'2027 Class X list read via browser; April 2026 revision','local_pdf_available':False},'specimens_2027':SPECIMENS,'specimen_limits':'Eight documents have an internal ICSE 2027 / T27 header. Instructions and selected question styles reviewed from mirrored text; diagrams and complete draft mark schemes not independently checked. Hindi and Computer Applications 2027 specimens not verified; their cards use 2026 main papers.'},ensure_ascii=False,indent=2),encoding='utf-8')

for sid,subject in SUBJECTS.items():
    subject['id']=sid
    subject['practice']=BANK[sid]
    subject['topics']=list(dict.fromkeys(q['topic'] for q in BANK[sid]))
    subject['sources']=[{'year':p['year'],'url':p['url'],'pages':p['pages'],'status':p['status'],'recovered':p['main_questions_located'],'expected':p['expected_main_questions']} for p in coverage if p['subject']==sid]
    subject['syllabusMirror']=next((p['url'] for p in SYLLABUSES if p['subject']==sid),'')
    subject['inventory']=[r for r in LEDGER if r['subject']==sid]
    subject['specimen']=next((p for p in SPECIMENS if p['subject']==sid),None)
    subject['formatBasis']='2027 specimen instructions read on a mirror and cross-checked against 2026 main paper.' if subject['specimen'] else '2026 main-paper instructions; a document internally labelled 2027 was not verified for this subject.'

NOTES=[
 '40 main examination papers: ten project subjects × 2023–2026. Improvement papers and the exceptional 2022 semester exams are not pooled.',
 '372 MAIN question slots are inventoried and their start pages located by OCR or scan checks. Family tags remain provisional where indicated; every subpart, diagram and answer has not been manually verified.',
 'Evidence confidence is different from prediction confidence. No exact-question percentages, fixed rotations or “last year means skip” rules are used.',
 'English Literature title comparisons use only 2025–2026 because the prescribed texts changed. Hindi 2027 scope is filtered through the revised Class X list.',
 'Generated sets are revision worksheets with actual totals, not complete official board mocks. For full timed mocks, open a source paper and follow its printed choices/maps.',
 'Eight internally labelled CISCE 2027 specimens were read through mirrored text. Hindi and Computer Applications 2027 specimens remain unverified. Diagrams and entire draft marking schemes were not independently checked.',
]
DATA={'date':DATE,'notes':NOTES,'syllabusHub':SYLLABUS_HUB,'booksUrl':BOOKS,'subjects':list(SUBJECTS.values()),'reading':ENGLISH_READING}
save('icse_2027_data.js','/* Generated by build_icse_2027.py. */\nwindow.ICSE_AUDIT = '+json.dumps(DATA,ensure_ascii=False,indent=2)+';\n')

guide=['# ICSE 2027 Evidence and Revision Guide',f'Updated {DATE}. For the ten subjects confirmed by the teacher.','\n## How to use this guide','Read the Focus section first, then practise the original drills and inspect the answer checkpoints. Extra-practice candidates get additional attention only after core coverage. “Skip” means a defensible syllabus boundary or unnecessary extension, never a ban on last year’s topic.','\n## Evidence and limits',*['- '+n for n in NOTES],f'\nOfficial reference: [2027 syllabus hub]({SYLLABUS_HUB}) and [revised prescribed books, April 2026]({BOOKS}). Past-paper files are CISCE papers hosted by an independent mirror; that mirror is not the Council. Syllabus document text was read through mirrored CISCE documents when official downloads were blocked. Read the document’s CLASS X section, not the mirror’s marketing summary.','\nThe manifest records links, page counts, PDF hashes, extraction status and unresolved headings. See [source manifest](research/source_manifest.json) and [question inventory](research/question_inventory.csv). Missing OCR headings and ambiguous diagrams have not been converted into precise frequency statistics.','\n## How priorities were decided','1. Filter to the 2027 Class X scope and the school’s prescribed books.','2. Separate compulsory breadth from choice questions: appearing as an offered question does not mean every candidate answered it.','3. Record question family, year and question reference; separate the old and new literature cohorts.','4. Treat repeated assessed skills as core practice. A gap can suggest an extra drill but supplies no calibrated probability.','5. Allocate more time to the student’s mistakes; rotate form/data/diagrams without fabricating question variants.','6. Do not infer a rotation from three unrelated algorithm examples. Check the whole programming section first.','\n## Test of the proposed “skip last year” rule','Computer matrix programs appeared in 2024 Q6 (diagonals), 2025 Q4 (norm), and 2026 Q5 (sparse matrix). Omitting matrices after either of the first two years would leave a blind spot in the next paper. Class applications and method overloading likewise occur in every reviewed programming section. This is a concrete counterexample, not a claimed statistical backtest of all subjects.','\nEnglish 2026 MCQs include texts that were not long-question selections that year. Geography offers the same theory families. Recent appearance is insufficient evidence for exclusion.','\n## Computer Applications: the actual algorithm sequence',table(['Year','Sorting program','Search/scan program','What it means'],[['2023','Q4 bubble sort','Q7 linear search','Both appeared in the same paper.'],['2024','Q7 selection sort','Other array/string tasks','Different program families coexist.'],['2025','No full sorting program','Q6 binary search','A paper can omit a full sorting program.'],['2026','No full sorting program','Q4 designation frequency scan','Frequency counting is not a named sort.']]),'Practical recommendation: timed bubble and selection sort drills, both searches, a class/slab application, overloading, strings, digits and 2D arrays. No evidence supports “selection followed linear, so X must come next”.','\n## Planning revision time','A workable teacher starting plan is 60% core skills and error correction, 25% mixed timed practice using real papers, and 15% extra variations/candidates. These are time allocations, not probabilities. Adjust using each student’s errors.','For choice sections, prepare enough families for spare choices while retaining short-question coverage of the entire scope. In Geography, prepare at least six or seven theory units well; in Computer, practise at least five program families well and trace all listed theory skills. Neither strategy guarantees an easy set of choices.']
guide += ['\n## Recurring Computer Applications families',
 'The denominator below is four complete main-paper programming sections, not four independent chances for a specific future question. Families overlap: a single program can use both arrays and digit logic. Counts describe what was offered, not what every student answered.',
 table(['Family','Offered in reviewed years','Question references','Revision implication'],[
 ['Class application','4/4','2023 Q3; 2024 Q3; 2025 Q3; 2026 Q3','Core: fields, constructor/methods, input, calculation and display.'],
 ['Method overloading','4/4','2023 Q5; 2024 Q4; 2025 Q7; 2026 Q7','Core: signatures, loops/calculation and return values.'],
 ['String/character program','4/4','2023 Q6; 2024 Q8; 2025 Q5; 2026 Q8','Core: conditions and Character/String methods; the task changes.'],
 ['Digit processing','4/4','2023 Q8 (inside array task); 2024 Q5; 2025 Q8; 2026 Q6','Core: extraction, saved original, accumulation and explicit conditions.'],
 ['Two-dimensional array','3/4','2024 Q6; 2025 Q4; 2026 Q5','Core despite consecutive appearances; practise several operations.'],
 ['Named sorting program','2/4','2023 Q4 bubble; 2024 Q7 selection','Extra drill for both listed sorts; two omissions do not prove a return.'],
 ['Named searching program','2/4','2023 Q7 linear; 2025 Q6 binary','Keep both. The 2026 frequency scan is useful array practice, counted separately.']]),
 '\n## Why the Hindi title gaps need extra caution',
 'The 2023–2026 papers drew literature selections from the earlier whole-book scope. The revised 2027 Class X list changes which texts are eligible. A title’s frequency in those four old papers therefore cannot be converted into its 2027 probability. The useful output is an eligible-text checklist, recent examples of task style, and extra practice for less recently selected eligible texts.']

for sid,s in SUBJECTS.items():
    guide += [f'\n## {s["name"]}',f'**Observed paper format:** {s["format"]}',f'**Format basis:** {s["formatBasis"]}',f'\n**Focus:** {s["focus"]}',f'\n**Extra practice / confidence:** {s["candidate"]}',f'\n**What to omit or reduce:** {s["skip"]}','\n**Reviewed anchors:**',table(['Year','Question reference','Observed family/text'],s['evidence']), '\n**Sources:** '+', '.join(f'[{p["year"]} main paper]({p["url"]})' for p in s['sources'])+f'; [official syllabus/books]({s["syllabus"]})'+(f'; [mirrored CISCE syllabus text]({s["syllabusMirror"]})' if s['syllabusMirror'] else '')+(f'; [2027 CISCE specimen text on mirror]({s["specimen"]["url"]})' if s['specimen'] else ''), '\n**Original practice questions and checkpoints**']
    for q in BANK[sid]:
        if sid=='hindi' and q.get('category') not in ('literature',): continue
        guide += [f'\n### {q["id"]} — {q["topic"]} [{q["marks"]} practice marks]',q['prompt'], '\nAnswer checkpoints: '+q['answer']]
guide += ['\n## Verification before setting a final mock','Use the latest Council specimen, confirm the school’s two Hindi books, attach actual topo/outline maps and literature passages where required, and check every offered question’s part totals and section choices. This project’s worksheets are intentionally identified as worksheets; they should not be sold to students as the next board paper.']
save('ICSE_2027_Evidence_and_Revision_Guide.md','\n\n'.join(guide)+'\n')

hindi=['# ICSE Hindi 2027 Practice and Evidence Pack',f'संशोधित: {DATE}। यह अभ्यास-संग्रह है; किसी प्रश्न के निश्चित आने का दावा नहीं।', '\n## Pattern Notes',SUBJECTS['hindi']['format'],SUBJECTS['hindi']['focus'],'पिछले वर्ष आया था, इसलिए पाठ छोड़ दें — यह नियम हटाया गया है। संदर्भ, पात्र, कारण, परिणाम, शब्दार्थ और शीर्षक पर पाठ-आधारित उत्तर तैयार करें।',f'[आधिकारिक संशोधित निर्धारित पुस्तक-सूची]({BOOKS})। पूरी [दस-विषय मार्गदर्शिका](ICSE_2027_Evidence_and_Revision_Guide.md) में कारण, प्रश्न-संदर्भ और सीमाएँ उपलब्ध हैं।','\n## 2027 Class X scope',table(['पुस्तक','कक्षा X में निर्धारित भाग'],[['साहित्य सागर — कहानी','बड़े घर की बेटी; संदेह; भीड़ में खोया आदमी; भेड़ें और भेड़िए; दो कलाकार'],['साहित्य सागर — कविता','सूर के पद; विनय के पद; भिक्षुक; चलना हमारा काम है; मातृ मंदिर की ओर'],['नया रास्ता','अध्याय 14–26'],['एकांकी संचय','सूखी डाली; महाभारत की एक साँझ; दीपदान']]),'स्कूल में पढ़ी गई केवल दो पुस्तकों से चार प्रश्न कीजिए, प्रत्येक पुस्तक से कम-से-कम एक। साहित्य सागर की कहानियाँ और कविताएँ एक ही पुस्तक के दो भाग हैं। वेबसाइट में शिक्षक अपने स्कूल की पुस्तक-जोड़ चुन सकते हैं।','\n### बोर्ड अभ्यास में किन पुराने भागों को छोड़ सकते हैं और क्यों','संशोधित कक्षा X सूची के कारण: बात अठन्नी की, काकी, महायज्ञ का पुरस्कार, नेताजी का चश्मा, अपना-अपना भाग्य; साखी, गिरिधर की कुंडलियाँ, स्वर्ग बना सकते हैं, वह जन्मभूमि मेरी, मेघ आए; संस्कार और भावना, बहू की विदा, मातृभूमि का मान; नया रास्ता अध्याय 1–13। स्कूल के आंतरिक कार्य/परीक्षण का निर्देश अलग हो सकता है। कारण पाठ्यक्रम है, पिछली परीक्षा में आना नहीं।','\n### हाल में आए पाठ जिन्हें बनाए रखना है','संदेह, भेड़ें और भेड़िए, सूर के पद, सूखी डाली, महाभारत की एक साँझ — ये 2026 में भी थे और 2027 कक्षा X सूची में भी हैं।',table(['वर्ष','प्रश्न','2027 सूची से संबंधित देखे गए पाठ'],SUBJECTS['hindi']['evidence'][:-1]),'नया रास्ता के पुराने अवतरण पूरे उपन्यास से हैं। किसी घटना को अनुमान से अध्याय 14–26 का न बताइए; अपने संस्करण में जाँचिए।', '\n## 1. Composition Bank — original writing drills','लगभग 250 शब्द। विषय कोई संभाव्यता-क्रम नहीं है। चित्र वाले कार्यों के लिए [स्थानीय चित्र-पत्रक](assets/hindi-picture-composition-sheet.png) में उपयुक्त पैनल चुनें।',table(['ID','प्रकार','प्रश्न'],[[q['id'],q['topic'],q['prompt']] for q in BANK['hindi'] if q['marks']==15]),'\n## 2. Letter Writing Bank',table(['ID','प्रश्न'],[[q['id'],q['prompt']] for q in BANK['hindi'] if q['topic']=='पत्र']), '\n## 3. Unseen Passage Bank','प्रत्येक प्रश्न-समूह 5 × 2 = 10 अभ्यास अंक। ये मौलिक छोटे अभ्यास गद्यांश हैं; वास्तविक बोर्ड गद्यांश की लंबाई का दावा नहीं।']
for p in HINDI_PASSAGES:
    hindi += ['\n### '+p['title'],p['text'], '\n'.join(f'{i+1}. {q} [2]' for i,(q,a) in enumerate(p['tasks'])), '**उत्तर-जाँच:** '+'; '.join(f'{i+1}. {a}' for i,(q,a) in enumerate(p['tasks']))]
hindi += ['\n## 4. Grammar Practice — unique drills and checked MCQs','एक ही शब्द को बार-बार घुमाकर 1000 प्रश्न बनाने का दावा हटाया गया है। 2024–26 में पूछे शब्द भी उपयोगी पुनरावृत्ति हैं। पहले उत्तर स्वयं दीजिए, फिर उत्तर-जाँच देखिए।',table(['ID','प्रकार','प्रश्न','उत्तर'],[[q['id'],q['topic'],q['prompt'],q['answer']] for q in BANK['hindi'] if q.get('category')=='grammar']), '\n## 5. Section B Literature Revision Sets','प्रत्येक समूह 2 + 2 + 3 + 3 = 10 अभ्यास अंक। नीचे पूरे पाठ पर पुनरावृत्ति-प्रश्न हैं, असली उद्धरण-आधारित बोर्ड प्रश्न नहीं। अवतरण-अभ्यास के लिए शिक्षक निर्धारित पाठ से सही अवतरण दें और वक्ता/श्रोता तथा प्रसंग वाले प्रश्न उससे जोड़ें। नकली उद्धरण या सर्ग-संख्या नहीं बनाई गई है।']
for q in BANK['hindi']:
    if q.get('category')=='literature': hindi += [f'\n### {q["id"]} — {q["book"]}: {q["topic"]}',q['prompt'],q['answer']]
hindi += ['\n## Quick Revision Strategy','पहले स्कूल की दो पुस्तकें और कक्षा X भाग की पुष्टि करें। हर निर्धारित पाठ के लिए पात्र/वक्ता, प्रसंग, मुख्य घटनाओं/बिंबों, कठिन शब्दों तथा शीर्षक/संदेश का एक पृष्ठ तैयार करें। चार उत्तरों में दोनों चुनी पुस्तकों का प्रतिनिधित्व रखें। रचना, पत्र, अपठित गद्यांश और सभी व्याकरण कौशल का अभ्यास जारी रखें।', '\n## English reading appendix (original practice)', ENGLISH_READING,'\n'.join(f'{i+1}. {p} [{m}]' for i,(p,m,a) in enumerate(ENGLISH_READING_TASKS)), '\n## Sources',', '.join(f'[{p["year"]} मुख्य प्रश्नपत्र]({p["url"]})' for p in SUBJECTS['hindi']['sources']),f'[संशोधित पुस्तक-सूची]({BOOKS}); [2027 पाठ्यक्रम]({SYLLABUS_HUB})। दस्तावेज़ तथा OCR की सीमाएँ पूरी मार्गदर्शिका और स्रोत-सूची में दी गई हैं।']
save('ICSE_Hindi_2027_Practice_and_Prediction_Pack.md','\n\n'.join(hindi)+'\n')

# Validation guards prevent a return to padded or malformed question banks.
assert len(coverage)==40 and len(LEDGER)==372
for sid,bank in BANK.items():
    prompts=[q['prompt'] for q in bank]
    assert len(prompts)==len(set(prompts)),f'Duplicate prompt in {sid}'
    assert all(q['answer'] and q['marks']>0 for q in bank)
    for q in bank:
        if 'parts' in q: assert sum(q['parts'])==q['marks']
        if 'options' in q: assert len(set(q['options']))==4 and 0<=q['correct']<4
assert {q['topic'] for q in BANK['hindi'] if q.get('category')=='literature'} >= {'संदेह','भेड़ें और भेड़िए','सूर के पद','सूखी डाली','महाभारत की एक साँझ'}
print(json.dumps({'papers':len(coverage),'main_question_slots':len(LEDGER),'main_questions_located':sum(p['main_questions_located'] for p in coverage),'OCR_headings_recovered':sum(p['ocr_headings_recovered'] for p in coverage),'practice_questions':{k:len(v) for k,v in BANK.items()}},ensure_ascii=False))

# The website consumes the expanded, fixed-paper pack, not the small seed bank.
from build_exam_pack import main as build_exam_pack
build_exam_pack()
