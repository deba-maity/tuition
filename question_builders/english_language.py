from .common import item

VERBS=[('write','wrote','written','writing','writes','the report'),('repair','repaired','repaired','repairing','repairs','the fence'),('read','read','read','reading','reads','the novel'),('prepare','prepared','prepared','preparing','prepares','the meal'),('complete','completed','completed','completing','completes','the assignment'),('check','checked','checked','checking','checks','the document'),('design','designed','designed','designing','designs','the poster'),('paint','painted','painted','painting','paints','the gate'),('teach','taught','taught','teaching','teaches','the lesson'),('explain','explained','explained','explaining','explains','the rule'),('clean','cleaned','cleaned','cleaning','cleans','the room'),('organise','organised','organised','organising','organises','the event'),('review','reviewed','reviewed','reviewing','reviews','the plan'),('translate','translated','translated','translating','translates','the passage'),('build','built','built','building','builds','the model'),('collect','collected','collected','collecting','collects','the parcel'),('deliver','delivered','delivered','delivering','delivers','the message'),('solve','solved','solved','solving','solves','the problem'),('inspect','inspected','inspected','inspecting','inspects','the machine'),('choose','chose','chosen','choosing','chooses','the material'),('bring','brought','brought','bringing','brings','the equipment'),('arrange','arranged','arranged','arranging','arranges','the display'),('finish','finished','finished','finishing','finishes','the project'),('update','updated','updated','updating','updates','the register'),('record','recorded','recorded','recording','records','the observation')]
NAMES=['Riya','Meera','Anita','Sara','Nisha','Tara','Leela','Asha','Diya','Ira']
PREPOSITIONS=[
 ('was accused ___ damaging','of',['the gate','the desk','the fence','the locker','the bicycle']),
 ('apologised ___ arriving late at','for',['the rehearsal','the meeting','the lesson','the interview','the ceremony']),
 ('is interested ___ studying','in',['astronomy','history','botany','poetry','geology']),
 ('is good ___ solving','at',['puzzles','equations','riddles','logic problems','crosswords']),
 ('was afraid ___ entering','of',['the dark tunnel','the deserted house','the deep cave','the empty warehouse','the abandoned station']),
 ('can depend ___','on',['her sister','the guide','the captain','the librarian','her teacher']),
 ('was congratulated ___ winning','on',['the debate','the scholarship','the medal','the race','the award']),
 ('prefers walking ___ travelling by','to',['bus','car','taxi','train','rickshaw']),
 ('arrived ___','at',['the station','the museum','the airport','the theatre','the school gate']),
 ('arrived ___ the city of','in',['Delhi','Mumbai','Chennai','Kolkata','Pune']),
 ('was deprived ___','of',['a fair hearing','an opportunity','her prize','her rights','a proper education']),
 ('was jealous ___','of',['her cousin’s success','her rival’s award','her friend’s talent','the winner’s popularity','her sister’s achievement']),
 ('was grateful ___','to',['the nurse','her neighbour','the coach','the librarian','her principal']),
 ('remained indifferent ___','to',['the criticism','the warning','the complaint','the suffering','the suggestion']),
 ('insisted ___ paying for','on',['the tickets','the repairs','the meal','the stationery','the transport']),
 ('objected ___','to',['the proposal','the delay','the new rule','the interruption','the unfair decision']),
 ('was fully aware ___','of',['the danger','the deadline','the difficulty','the rule','the responsibility']),
 ('is capable ___ completing','of',['the journey','the task','the investigation','the experiment','the course']),
 ('decided to abstain ___','from',['the vote','the contest','the discussion','the celebration','the meeting']),
 ('agreed to abide ___','by',['the rules','the verdict','the agreement','the regulations','the decision']),
 ('was required to comply ___','with',['the order','the instructions','the safety rule','the regulations','the conditions']),
 ('had to deal ___','with',['the complaint','the problem','the delay','the emergency','the disagreement']),
 ('explained that the parcel belongs ___','to',['the teacher','the captain','the librarian','her sister','the visitor']),
 ('was keen ___ joining','on',['the choir','the club','the expedition','the team','the workshop']),
 ('was engaged ___ writing','in',['a speech','a report','a letter','an article','a review']),
 ('was convinced ___','of',['her innocence','the need for change','the plan’s usefulness','the risk','the value of practice']),
 ('was acquainted ___','with',['the new captain','the local guide','the principal','the organiser','the author']),
 ('was responsible ___','for',['the timetable','the accounts','the equipment','the invitations','the arrangements']),
 ('applied ___','for',['the scholarship','the post','the grant','the permit','the fellowship']),
 ('was tired ___ hearing','of',['the same excuse','the repeated complaint','the endless argument','the false promise','the familiar story']),
 ('was prevented ___ entering','from',['the hall','the laboratory','the office','the stadium','the library']),
 ('was prohibited ___ using','from',['the lift','the shortcut','the machine','the passage','the device']),
 ('succeeded ___ repairing','in',['the radio','the pump','the clock','the engine','the lock']),
 ('was absorbed ___ reading','in',['the novel','the newspaper','the biography','the report','the diary']),
 ('was ashamed ___','of',['her behaviour','the lie','the unfair remark','her carelessness','the rude reply']),
 ('was proud ___','of',['her team','the school','the achievement','her work','the improvement']),
 ('was eligible ___','for',['the scholarship','the award','the position','the examination','the grant']),
 ('was anxious ___ the safety of','about',['her sister','the climber','the child','the passengers','the workers']),
 ('was blamed ___ damaging','for',['the window','the instrument','the lock','the bicycle','the display']),
 ('was praised ___ helping','for',['the visitor','the child','the patient','the elderly woman','the injured player']),
 ('was familiar ___','with',['the route','the procedure','the software','the story','the regulations']),
 ('was eager ___ hear','to',['the result','the announcement','the explanation','the news','the verdict']),
 ('was invited ___ participate in','to',['the debate','the contest','the survey','the programme','the campaign']),
 ('was forbidden ___ enter','to',['the room','the factory','the mine','the compound','the tower']),
 ('was determined ___ complete','to',['the project','the course','the journey','the survey','the experiment']),
 ('was accustomed ___ working in','to',['the heat','the cold','the laboratory','the evening','the open air']),
 ('was opposed ___ closing','to',['the library','the playground','the museum','the clinic','the reading room']),
 ('was devoted ___ caring for','to',['injured animals','young children','elderly residents','abandoned birds','sick patients']),
 ('took pride ___ maintaining','in',['the garden','the archive','the library','the collection','the playground']),
 ('lost faith ___','in',['the promise','the plan','the official account','the proposed remedy','the leadership']),
]

def grammar_bank():
    result=[]
    def add(section,family,prompt,answer,**extra):
        result.append(item(section,prompt,answer,1,id=f'english1-grammar-{len(result)+1:04}',section=section,family=family,**extra))
    for vi,(base,past,pp,ing,third,obj) in enumerate(VERBS):
        name=NAMES[vi%10]
        forms=[(f'Every weekday, {name} ___ ({base}) {obj}. Use the simple present.',third,'A singular third-person subject takes the -s/-es form.'),
          (f'Yesterday, {name} ___ ({base}) {obj}. Use the simple past.',past,'The completed past-time expression requires the simple past.'),
          (f'At this moment, {name} ___ ({base}) {obj}. Use the present continuous.','is '+ing,'Use is + present participle for this singular subject.'),
          (f'By the time the visitor arrived, {name} ___ ({base}) {obj}. Use the past perfect and include already.','had already '+pp,'The earlier completed past action takes had + past participle.'),
          (f'Since Monday, {name} ___ ({base}) {obj}. Use the present perfect continuous.','has been '+ing,'An activity continuing from the past uses has been + -ing.'),
          (f'By this time tomorrow, {name} ___ ({base}) {obj}. Use the future perfect.','will have '+pp,'Completion before a future reference point uses will have + past participle.'),
          (f'When the power failed, {name} ___ ({base}) {obj}. Use the past continuous.','was '+ing,'The ongoing background action takes was + -ing.'),
          (f'If she had more time, {name} ___ ({base}) {obj}. Use would and the correct verb form.','would '+base,'A modal takes the base form.'),
          (f'{obj.capitalize()} ___ ({base}) by {name} yesterday. Use the simple-past passive.','was '+pp,'Passive: was + past participle; the stated object is singular.'),
          (f'{name} must ___ ({base}) {obj} before leaving. Supply the verb form.',base,'Use the bare infinitive after must.')]
        for j,(prompt,ans,reason) in enumerate(forms):add('Grammar · verb forms',f'Verb form {j+1}',prompt,ans+'. '+reason,answerText=ans,paperKind='verb')
    for i,(stem,prep,objects) in enumerate(PREPOSITIONS):
        for j,obj in enumerate(objects):
            name=NAMES[(i+j)%10]
            add('Grammar · prepositions','Collocation '+str(i+1),f'Fill the blank with the appropriate word: {name} {stem} {obj}.',prep+'. The construction is '+stem.replace('___',prep)+'.',answerText=prep,paperKind='preposition')
    for j,name in enumerate(NAMES):
        friend=NAMES[(j+3)%10]; task=['report','assignment','article','project','speech','essay','review','proposal','summary','translation'][j]; adjective=['difficult','demanding','lengthy','important','urgent','challenging','complex','unusual','detailed','sensitive'][j]
        cases=[
          ('although',f'{name} was tired. She completed the {task}.',f'Although {name} was tired, she completed the {task}.'),
          ('because',f'{name} missed the bus. She arrived late.',f'{name} arrived late because she missed the bus.'),
          ('unless',f'{name} must finish the {task}. Otherwise, she cannot leave.',f'{name} cannot leave unless she finishes the {task}.'),
          ('as soon as',f'{name} finished the {task}. She called {friend} immediately.',f'As soon as {name} finished the {task}, she called {friend}.'),
          ('who',f'I met {name}. She had won the competition.',f'I met {name}, who had won the competition.'),
          ('whose',f'I thanked {name}. Her advice had helped me.',f'I thanked {name}, whose advice had helped me.'),
          ('where',f'{name} visited the library. She had studied there as a child.',f'{name} visited the library where she had studied as a child.'),
          ('which',f'{name} completed the {task}. It had taken a week.',f'{name} completed the {task}, which had taken a week.'),
          ('in order to',f'{name} went to the library. She wanted to research the {task}.',f'{name} went to the library in order to research the {task}.'),
          ('so that',f'{name} spoke slowly. She wanted everyone to understand the {task}.',f'{name} spoke slowly so that everyone could understand the {task}.'),
          ('so ... that',f'The {task} was very {adjective}. {name} needed help.',f'The {task} was so {adjective} that {name} needed help.'),
          ('too ... to',f'The bag was very heavy. {name} could not lift it.',f'The bag was too heavy for {name} to lift.'),
          ('enough to',f'{name} was strong. She could carry the suitcase.',f'{name} was strong enough to carry the suitcase.'),
          ('as well as',f'{name} submitted the {task}. {friend} submitted it too.',f'{name} as well as {friend} submitted the {task}.'),
          ('not only ... but also',f'{name} prepared the {task}. She presented it.',f'{name} not only prepared the {task} but also presented it.'),
          ('neither ... nor',f'{name} did not attend the meeting. {friend} did not attend it.',f'Neither {name} nor {friend} attended the meeting.'),
          ('either ... or',f'{name} may present the {task}. Alternatively, {friend} may present it.',f'Either {name} or {friend} may present the {task}.'),
          ('in spite of',f'{name} was exhausted. She completed the {task}.',f'In spite of being exhausted, {name} completed the {task}.'),
          ('instead of',f'{name} did not abandon the {task}. She revised it.',f'Instead of abandoning the {task}, {name} revised it.'),
          ('while',f'{name} was writing the {task}. At the same time, {friend} was checking the figures.',f'While {name} was writing the {task}, {friend} was checking the figures.'),
          ('having',f'{name} completed the {task}. Then she went home.',f'Having completed the {task}, {name} went home.'),
          ('before',f'{name} checked the {task}. Then she submitted it.',f'{name} checked the {task} before she submitted it.'),
          ('after',f'{name} explained the {task}. Then the discussion began.',f'After {name} explained the {task}, the discussion began.'),
          ('if',f'{name} did not practise. Therefore, she was not confident. Express an unreal past condition.',f'If {name} had practised, she would have been confident.'),
          ('since',f'{name} had lost the original {task}. She used a copy.',f'Since {name} had lost the original {task}, she used a copy.')]
        for connector,pair,ans in cases:
            add('Grammar · sentence joining','Join with '+connector,f'Join the sentences using {connector}, preserving the meaning: {pair}',ans+' Equivalent grammatical wording preserving the stated relationship is acceptable.',answerText=ans,paperKind='join',paperJoin=connector not in ['not only ... but also','as well as'])
    for j,name in enumerate(NAMES):
        n=j+2; task=['report','assignment','article','project','speech','essay','review','proposal','summary','translation'][j]
        cases=[
          (f'{name} wrote the {task}. Begin: The {task} ...',f'The {task} was written by {name}.','Past passive'),
          (f'The {task} was completed by {name}. Begin: {name} ...',f'{name} completed the {task}.','Passive to active'),
          (f'{name} said yesterday, "I am ready now." Report her words today, beginning: {name} said ...',f'{name} said that she was ready then.','Reported statement'),
          (f'{name} asked me, "Are you ready?" Begin: {name} asked me whether ...',f'{name} asked me whether I was ready.','Reported question'),
          (f'As soon as {name} entered the hall, the lights went out. Begin: No sooner ...',f'No sooner had {name} entered the hall than the lights went out.','No sooner inversion'),
          (f'As soon as {name} finished the {task}, the bell rang. Begin: Hardly ...',f'Hardly had {name} finished the {task} when the bell rang.','Hardly inversion'),
          (f'{name} is intelligent and hardworking. Use: not only ... but also.',f'{name} is not only intelligent but also hardworking.','Correlative conjunction'),
          (f'{name} is too tired to continue. Use: so ... that.',f'{name} is so tired that she cannot continue.','Too to to so that'),
          (f'The box is so heavy that {name} cannot lift it. Use: too ... to.',f'The box is too heavy for {name} to lift.','So that to too to'),
          (f'{name} is taller than her sister. Begin: Her sister ...',f'Her sister is not as tall as {name}.','Comparative transformation'),
          (f'{name} is the tallest student in the class. Begin: No other ...',f'No other student in the class is as tall as {name}.','Superlative transformation'),
          (f'Unless {name} apologises, she will not be forgiven. Begin: If ...',f'If {name} does not apologise, she will not be forgiven.','Unless to if'),
          (f'If {name} does not hurry, she will miss the train. Begin: Unless ...',f'Unless {name} hurries, she will miss the train.','If to unless'),
          (f'Despite being ill, {name} completed the {task}. Begin: Although ...',f'Although {name} was ill, she completed the {task}.','Despite to although'),
          (f'Although {name} was tired, she continued. Begin: In spite of ...',f'In spite of being tired, {name} continued.','Although to in spite'),
          (f'Only {name} knew the answer. Begin: None but ...',f'None but {name} knew the answer.','Only to none but'),
          (f'Immediately after {name} opened the door, the dog ran out. Begin: The moment ...',f'The moment {name} opened the door, the dog ran out.','Immediate sequence'),
          (f'{name} has not visited us for {n} years. Begin: It is ...',f'It is {n} years since {name} last visited us.','Since and for'),
          (f'Very few students in the class are as diligent as {name}. Use: one of the ...',f'{name} is one of the most diligent students in the class.','Very few to one of'),
          (f'What a remarkable {task} {name} has written! Change to an assertive sentence.',f'{name} has written a very remarkable {task}.','Exclamatory to assertive'),
          (f'The {task} was so clear that everyone understood it. Use: such ... that.',f'It was such a clear {task} that everyone understood it.','So to such'),
          (f'{name} is presenting the {task}, ___? Supply the question tag.',"isn't she?",'Question tag'),
          (f'{name} did not study, so she failed the test. Begin: If {name} had ...',f'If {name} had studied, she would not have failed the test.','Unreal past condition'),
          (f'{name} did complete the {task}. Remove the emphatic did without changing the tense.',f'{name} completed the {task}.','Emphatic auxiliary'),
          (f'{name} as well as her sister speaks French. Begin: Both ...',f'Both {name} and her sister speak French.','Agreement with both')]
        for prompt,ans,family in cases:add('Grammar · transformations',family,'Rewrite as directed without changing the meaning: '+prompt,ans+' Accept an equivalent correct construction that obeys the instruction.',answerText=ans,paperKind='transform')
    assert len(result)==1000 and len({q['prompt'] for q in result})==1000
    return result

COMPOSITIONS=[
('Narrative','Write a story beginning: “The envelope had been lying on the classroom floor all morning.” Develop a convincing conflict and an ending that follows from the events.'),
('Narrative','An ordinary journey became an experience you still remember. Describe the incident, your response and how it affected your judgement of another person.'),
('Narrative','Write an original story ending: “For the first time, I was glad that things had not gone according to plan.”'),
('Descriptive','Describe a familiar market just before a festival. Use selected sights, sounds and interactions to convey its atmosphere rather than merely listing shops.'),
('Descriptive','Describe a place that changes noticeably between early morning and late evening. Convey the contrast through details and your response to it.'),
('Descriptive','Describe the moment before, during and immediately after an important school performance, using a consistent viewpoint.'),
('Argumentative','“Competition brings out the best in students.” Present a reasoned argument for or against the statement, considering a serious opposing view.'),
('Argumentative','“Every school should reserve one afternoon a week for practical community work.” Give your views, supported by reasons and examples.'),
('Reflective','Describe a situation in which listening carefully changed your first impression. Explain what you learned without turning the composition into a list of advice.'),
('Situational','A school library closes temporarily and pupils must find another way to keep its activities going. Write a story or description centred on the situation. No picture is required.')]

LETTERS=[
('Formal','Write to the Municipal Commissioner about unsafe traffic outside your school. Describe the problem with specific examples, explain the risks, and suggest realistic measures without making unsupported accusations.'),
('Formal','Write to the Director of a local museum requesting a visit for your class. State the educational purpose, propose a date and group size, and ask about arrangements and access requirements.'),
('Formal','Write to the manager of a sports shop about equipment delivered in a damaged condition. Give the order details, describe the fault and request an appropriate remedy.'),
('Formal','Write to the editor of a newspaper about the declining use of a public library in your area. Explain its value and suggest measures to attract young readers.'),
('Formal','Write to the principal requesting permission to organise a student-run reading event. Explain its purpose, proposed arrangements and how normal school work will be protected.'),
('Informal','Write to your grandfather about a skill you learned from him and recently used. Describe the situation, the outcome and why the experience mattered to you.'),
('Informal','A friend is disappointed after not being selected for a team. Write a letter acknowledging the disappointment, sharing a relevant experience and suggesting a constructive way forward.'),
('Informal','Write to a cousin who is moving to a new city. Describe the difficulties you faced during a similar change and offer specific, considerate advice.'),
('Informal','Write to a friend describing an unexpected responsibility you handled during a school event. Explain what happened, how you managed it and what you would do differently.'),
('Informal','Write to an older sibling about a book or experience that changed your opinion. Explain your earlier view, the change and why you want to discuss it with them.')]

EVENTS=[('Reading Relay','reading-aloud competition','12 January 2027','10:00 a.m.–12:00 noon','school auditorium','Classes IX and X','a guest judge','the librarian'),('Science in Action','science demonstration day','16 January 2027','9:30 a.m.–12:30 p.m.','science block','Classes VIII–X','a guest demonstrator','the laboratory coordinator'),('Green Steps','campus waste-segregation drive','20 January 2027','8:30–10:30 a.m.','school courtyard','Classes IX and X','recycling collection support','the eco-club teacher'),('Words that Matter','inter-house debate','23 January 2027','11:00 a.m.–1:00 p.m.','school hall','Classes IX and X','a judge','the English teacher'),('Local Stories','oral-history workshop','27 January 2027','10:00 a.m.–12:00 noon','library reading room','Class X','a resource speaker','the history teacher'),('Play Fair','friendly sports meet','30 January 2027','8:00–11:00 a.m.','school playground','Classes VIII–X','a referee','the sports teacher'),('Safety First','road-safety session','3 February 2027','9:00–10:30 a.m.','school auditorium','Classes IX and X','a traffic-police speaker','the activity coordinator'),('Share a Skill','peer-learning workshop','6 February 2027','10:00 a.m.–12:00 noon','multipurpose room','Classes IX and X','a guest trainer','the student council'),('Listen and Learn','storytelling session','10 February 2027','11:00 a.m.–12:30 p.m.','library','Classes VII–IX','a storyteller','the librarian'),('Our Common Space','school neighbourhood clean-up','13 February 2027','8:30–10:30 a.m.','school front gate','Classes IX and X','waste-collection assistance','the community coordinator')]

def writing_bank():
    result=[]
    def add(section,prompt,answer,marks,**extra):result.append(item(section,prompt,answer,marks,id=f'english1-writing-{len(result)+1:03}',section=section,**extra))
    for genre,prompt in COMPOSITIONS:
        add('Composition · 10 prompts',prompt+' Write 300–350 words.',f'Marking guide (20): content/organisation 10; expression, vocabulary and sentence control 10. For this {genre.lower()} task, develop relevant detail and a clear progression; sustain viewpoint and tense. A strong response must answer the particular situation. Many different original responses are valid.',20,genre=genre)
    for kind,prompt in LETTERS:
        add('Letters · 10 prompts',prompt,f'Marking guide (10): appropriate format 2½; task-specific content 2½; expression 5. Use a consistent {kind.lower()} register, include every requested detail and a purposeful ending. Effective original responses can differ in wording and examples.',10,genre=kind)
    for i,(title,event,date,time,venue,audience,help,contact) in enumerate(EVENTS):
        notice=f'You are the secretary of the relevant club of Sunrise School. Write a notice inviting {audience} to {event} titled “{title}” on {date}, {time}, at the {venue}. Ask interested pupils to register with {contact} at least three days before the event.'
        key=f'{title}\n{event.title()}\nDate: {date}\nTime: {time}\nVenue: {venue}\n{audience} are invited. Register with {contact} at least three days beforehand.\nClub Secretary, Sunrise School.\nMarking (5): clear heading/purpose; correct date, time, venue; audience and action; concise appropriate format.'
        add('Notices · 10 prompts',notice,key,5,event=i)
        email=f'For the same {event} at Sunrise School ({date}, {time}, {venue}), write an email to a suitable external organisation requesting {help}. State the purpose and audience, give the arrangements, explain the assistance required and request confirmation. Use a suitable subject and salutation.'
        answer=f'To: coordinator@example.org\nSubject: Request for {help} — {date}\nDear Sir/Madam,\nSunrise School is organising {event} for {audience} on {date}, {time}, at the {venue}. We request your organisation to provide {help} to support the programme. Kindly confirm availability and inform us of any arrangements you require. We will coordinate the details in advance.\nYours faithfully,\nClub Secretary\nSunrise School\nMarking (5): format/register and subject; purpose; correct arrangements; precise request and confirmation.'
        add('Emails · 10 prompts',email,answer,5,event=i)
    assert len(result)==40
    return result

def make_bank(readings):
    return writing_bank()+readings+grammar_bank()
