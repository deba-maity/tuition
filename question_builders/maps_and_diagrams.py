from .common import item
from build_visuals import FEATURES,paper_features
SOI='https://surveyofindia.gov.in/pages/educational-map-series'

def figure(src,caption,source='',credit=''):
    return dict(src=src,caption=caption,source=source,credit=credit)

def topo_question(n):
    sheet='G43S7' if n%2 else 'G43S10';east=(25 if n%2 else 52)+n%5;north=(2 if n%2 else 30)+n%3;ew=3+n%3;nh=3+n%2;cm=2+n*.3;te=2+n%7;tn=1+n%8
    bounds=f'Eastings {east}–{east+ew}; Northings {north:02}–{north+nh:02}'
    questions=[
      ('State the representative fraction printed on the supplied Survey of India sheet.','RF=1:50,000. One map unit represents 50,000 of the same ground units.'),
      (f'A direct distance measures {cm:.1f} cm on a correctly scaled print of this sheet. Calculate the ground distance in km.',f'1 cm=50,000 cm=0.5 km. Distance={cm:.1f}×0.5={cm*.5:.2f} km. Do not measure a resized screen preview with a physical ruler.'),
      (f'Calculate the area between the grid limits {bounds}. Each full grid square is 1 km by 1 km.',f'East–west extent={ew} km; north–south extent={nh} km; area={ew}×{nh}={ew*nh} km².'),
      ('Read the contour interval from the sheet’s scale/legend panel.','Contour interval=20 metres. It is the vertical difference between consecutive contour lines.'),
      (f'A point is {te} tenths east of easting {east} and {tn} tenths north of northing {north:02}. Give its six-figure reference.',f'Easting component={east}{te}; northing component={north:02}{tn}. Six-figure reference={east}{te}{north:02}{tn}. Read eastings first.'),
      ('What does the yellow tint in the map represent?','Cultivated land. Use the sheet’s conventional-symbol legend to distinguish it from green forest/open scrub.'),
      ('What does the abbreviation P.F. indicate on these educational sheets?','Protected Forest, not permanent forest. R.F. denotes Reserved Forest.'),
      ('What does a spot-height number printed in black beside a dot indicate?','The elevation of that particular surveyed point in metres above mean sea level; it is not the height relative to an adjacent valley.'),
      ('What does r following a height/depth value indicate?','Relative height/depth in metres: a local difference between top and bottom, rather than absolute elevation above sea level.'),
      (f'Give the compass direction of grid square {east+2}{north+2:02} from grid square {east}{north:02}.','Northeast: the destination has both a higher easting and a higher northing.')]
    q=item('Topo map · '+sheet,'Use Survey of India educational sheet '+sheet+' ('+('45D/7' if n%2 else '45D/10')+'). '+bounds+'. Use the supplied complete sheet and its legend; these are original skill questions rather than claims about an unseen school extract.', '\n\n'.join(f'({i+1}) {answer}' for i,(_,answer) in enumerate(questions)),10,id=f'geo-topo-{n:02}',section='Topographical maps · real sheets',family='Survey of India map skills',parts=[dict(prompt=p,answer=a,marks=1) for p,a in questions],sheet=sheet,gridBounds=bounds)
    q['figures']=[figure(f'assets/maps/{sheet}-overview.png','Survey of India '+sheet+' · overview; open the full PDF to read symbols and grid references.',SOI,'Survey of India. Original map and legend retained.')]
    q['resourcePdf']=f'assets/maps/{sheet}.pdf'
    return q

def india_question(n):
    marking,ident=paper_features(n)
    questions=[]
    for name,kind,coords in marking:questions.append(dict(prompt=('Mark and label ' if kind=='point' else 'Shade/trace and label ')+name+'.',answer=f'{name}: see the annotated map. '+('Use a clear dot and a leader line; labels alone without the correct location do not earn the location mark.' if kind=='point' else 'The overlay shows the broad route/region. Keep shading/lines within the appropriate geographical area and attach the label clearly.'),marks=1))
    for letter,(name,kind,coords) in zip('ABCD',ident):questions.append(dict(prompt=f'Identify the feature marked {letter} on the supplied map.',answer=f'{letter}: {name}.',marks=1))
    q=item('India map work','On the supplied outline of India, attempt the following six marking tasks and identify four marked features. Use arrows where needed to keep labels readable.', 'Compare your completed map with the answer map. Credit a location only when the point, route or shaded region is correctly placed; the name alone is insufficient.',10,id=f'geo-india-map-{n:02}',section='India maps · mark and identify',family='India outline map',parts=questions)
    q['figures']=[figure(f'assets/diagrams/india-paper-{n:02}.svg','Question map: only A–D are pre-marked. Boundary derived from Survey of India’s outline vector.','https://surveyofindia.gov.in/pages/outline-maps-of-india','Survey of India boundary; original schematic exercise overlays.')]
    q['answerFigures']=[figure(f'assets/diagrams/india-answer-{n:02}.svg','Answer map: schematic placements for comparison. Rivers, relief belts and soil regions are broad study overlays; use your teacher’s map marking conventions.')]
    return q

def enrich(sid,bank):
    if sid=='geo':
        bank=[q for q in bank if q.get('section')!='Text-only topography']
        bank.extend(topo_question(n) for n in range(1,21));bank.extend(india_question(n) for n in range(1,21))
    if sid=='phy':
        for q in bank:
            if q.get('family')=='Parallel resistance and branch current':q['figures']=[figure('assets/diagrams/series-parallel.svg','Two parallel branches. R₁, R₂ and V take the values specified in the question; diagram not to scale.')]
            elif q.get('family')=='Beam equilibrium and support reaction':q['figures']=[figure('assets/diagrams/lever.svg','Light beam with a pivot, load and effort. Use the distances in the question; diagram not to scale.')]
        # Replace a handful of numerical duplicates-in-spirit with genuine ray construction.
        for n,index in enumerate(range(12,2000,100)):
            f=10+n;u=2*f;q=bank[index]
            q.update(topic='Lenses',family='Ray construction at twice focal distance',prompt=f'A convex lens has focal length {f} cm. An object of height {2+n%4} cm is placed {u} cm from the lens, at 2F₁. Complete the two principal rays, locate the image, and calculate image distance and height. State its nature.',answer=f'1. Draw one ray parallel to the principal axis; after refraction it passes through F₂. Draw a second through O, undeviated. Their intersection is at 2F₂.\n2. u=−{u} cm, f=+{f} cm. Lens formula gives 1/v=1/{f}−1/{u}=1/{u}; v=+{u} cm.\n3. Magnification=v/u=−1. Image height=−{2+n%4} cm: equal magnitude and inverted.\n4. The image is real, inverted and the same size as the object.',marks=4)
            for key in ['shortAnswer','distractors','mcqPrompt']:q.pop(key,None)
            q['figures']=[figure('assets/diagrams/convex-lens-question.svg','Complete the rays on this diagram; the displayed geometry is at 2F₁. Use the numerical values in the question.')]
            q['answerFigures']=[figure('assets/diagrams/convex-lens-answer.svg','Completed construction: rays meet at 2F₂, with equal image magnitude and inversion.')]
    return bank
