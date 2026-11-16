"""Code-native diagrams and a map derived from Survey of India's outline vector."""
import struct, zipfile, math, json, html
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets'/'diagrams';OUT.mkdir(parents=True,exist_ok=True)
SOURCE='https://surveyofindia.gov.in/documents/Outline_of_India.zip'
def svg(body,width=640,height=430):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img"><defs><marker id="rayArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#147d9c"/></marker></defs><style>text{{font:16px Arial;fill:#142b3e}}.wire{{fill:none;stroke:#142b3e;stroke-width:3}}.ray{{fill:none;stroke:#147d9c;stroke-width:2.4;marker-end:url(#rayArrow)}}.dash{{stroke-dasharray:6 5}}.key{{fill:#b63d36}}</style><rect width="100%" height="100%" fill="white"/>'+body+'</svg>'
def save(name,body,w=640,h=430):(OUT/name).write_text(svg(body,w,h),encoding='utf-8')
def simplify(points,tolerance=.15):
    """Subpixel display generalisation; preserve each island/ring separately."""
    if len(points)<12:return points
    clean=[]
    for point in points:
        p=(round(point[0],2),round(point[1],2))
        if not clean or clean[-1]!=p:clean.append(p)
    if len(clean)<5:return clean
    keep={0,len(clean)-1};stack=[(0,len(clean)-1)]
    while stack:
        start,end=stack.pop();ax,ay=clean[start];bx,by=clean[end];dx=bx-ax;dy=by-ay;den=dx*dx+dy*dy;best=-1;idx=None
        for j in range(start+1,end):
            x,y=clean[j]
            if den:
                t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/den));distance=(x-ax-t*dx)**2+(y-ay-t*dy)**2
            else:distance=(x-ax)**2+(y-ay)**2
            if distance>best:best=distance;idx=j
        if idx is not None and best>tolerance*tolerance:keep.add(idx);stack.extend([(start,idx),(idx,end)])
    result=[clean[i] for i in sorted(keep)]
    return result if len(result)>=4 else clean
def project(lon,lat):
    # Exact forward LCC parameters from Outline_of_India.prj (WGS84 ellipsoid).
    e=math.sqrt(0.00669437999014);a=6378137.;rad=math.radians
    def m(p):return math.cos(p)/math.sqrt(1-e*e*math.sin(p)**2)
    def t(p):return math.tan(math.pi/4-p/2)/((1-e*math.sin(p))/(1+e*math.sin(p)))**(e/2)
    p1,p2=rad(12.472944),rad(35.172806);n=math.log(m(p1)/m(p2))/math.log(t(p1)/t(p2));F=m(p1)/(n*t(p1)**n)
    rho=a*F*t(rad(lat))**n;rho0=a*F*t(rad(24))**n;theta=n*rad(lon-80)
    return 4000000+rho*math.sin(theta),4000000+rho0-rho*math.cos(theta)

# Marking overlays are schematic study guides on the authoritative boundary.
# The underlying national outline is neither hand-invented nor taken from a
# generic country dataset with different boundaries.
FEATURES=[
('Delhi','point',[(77.21,28.61)]),('Mumbai','point',[(72.88,19.08)]),('Kolkata','point',[(88.36,22.57)]),('Chennai','point',[(80.27,13.08)]),('Hyderabad','point',[(78.49,17.39)]),('Bengaluru','point',[(77.59,12.97)]),('Kochi','point',[(76.27,9.97)]),('Allahabad / Prayagraj','point',[(81.85,25.44)]),
('Mumbai High','point',[(71.3,19.4)]),('Digboi','point',[(95.62,27.39)]),('Singhbhum','point',[(85.8,22.5)]),('Jharia','point',[(86.41,23.75)]),('Wular Lake','point',[(74.6,34.36)]),('Karakoram Pass','point',[(78.0,35.5)]),('Mount Godwin Austin / K2','point',[(76.51,35.88)]),('Kanchenjunga','point',[(88.15,27.7)]),
('Himalayas','line',[(74.6,34.6),(78.0,31.7),(82.0,29.8),(86.0,28.0),(89,27.7),(93,28)]),('Karakoram','line',[(74.5,36),(77,35.5),(78.5,35)]),('Aravali','line',[(73.1,24.5),(74.5,26.4),(76.3,28)]),('Vindhyas','line',[(74.5,22.6),(77,23.4),(80,24.4)]),('Satpura','line',[(74.5,21.5),(77,22),(80.5,22.5)]),('Western Ghats','line',[(73.7,20.5),(74.4,17),(75.3,14),(76.6,11),(77.3,8.5)]),('Eastern Ghats','line',[(84,19),(82.3,17),(79.5,14),(78,11.8)]),('Nilgiris','point',[(76.7,11.4)]),('Khasi Hills','point',[(91.7,25.45)]),
('Deccan Plateau','region',[(74,19),(79,20),(81,16),(78,11),(75,14),(74,19)]),('Chota Nagpur Plateau','region',[(84,22),(87,22),(87,24.5),(84,24.5),(84,22)]),('Gangetic Plains','region',[(77,29),(80,28),(87,26),(88,23.5),(83,24),(78,26),(77,29)]),('Thar Desert','region',[(69.8,25.5),(71,28.8),(73,29),(73.6,26.5),(71.5,24.5),(69.8,25.5)]),
('Konkan Coast','line',[(72.8,20),(73,18),(73.7,16)]),('Malabar Coast','line',[(75.3,12.3),(76.1,10.5),(76.7,8.6)]),('Coromandel Coast','line',[(80.3,13),(80,11.8),(79.9,10.8)]),('Northern Circars','line',[(85,19),(83.3,17.8),(81.7,16.5)]),
('Gulf of Kutch','point',[(69.4,22.6)]),('Gulf of Khambhat','point',[(72.5,21.5)]),('Gulf of Mannar','point',[(79,8.7)]),('Palk Strait','point',[(79.7,9.9)]),('Andaman Sea','point',[(94,11)]),
('Indus','line',[(79.5,32.5),(77.5,34),(75,35)]),('Jhelum','line',[(75.3,33.4),(74.7,34.2),(73.7,34)]),('Chenab','line',[(77,32.5),(75.6,33.2),(74.5,32.8)]),('Ravi','line',[(76.5,32.4),(75.7,32.3),(74.7,31.5)]),('Beas','line',[(77.1,32.3),(76.2,31.8),(75.1,31.2)]),('Satluj','line',[(80,31),(78.4,31.5),(76.5,31.3),(75,31)]),
('Ganga','line',[(79,30.9),(78.2,29.9),(80,27.4),(81.8,25.5),(85.1,25.6),(87.9,24.3),(88.2,22.2)]),('Yamuna','line',[(78.5,31),(77.2,28.6),(78.5,27.2),(80,25.8),(81.8,25.4)]),('Ghaghra','line',[(81,29.2),(81.5,27.3),(83,26.2),(84.7,25.7)]),('Gomti','line',[(80.1,28.5),(80.9,26.8),(82.2,25.8),(83.2,25.5)]),('Gandak','line',[(83.5,28.2),(84,26.7),(85.1,25.7)]),('Kosi','line',[(87,27.8),(86.8,26.3),(87.2,25.4)]),('Chambal','line',[(75.7,22.5),(75.8,25.2),(77.4,26.5),(79.2,26.5)]),('Betwa','line',[(77.6,23),(78.5,25),(80.2,25.9)]),('Brahmaputra','line',[(94,28.5),(95,27.8),(92.7,26.8),(90.1,26.1),(89.8,25.5)]),('Narmada','line',[(81.7,22.7),(79.9,23.1),(77,22),(74,21.8),(72.6,21.6)]),('Tapti / Tapi','line',[(78.3,21.7),(76,21.1),(74,21.1),(72.6,21)]),('Mahanadi','line',[(81.8,20.1),(83.2,21.5),(85,20.8),(86.7,20.3)]),('Godavari','line',[(73.5,20),(76,19.2),(79,18.8),(81,17.4),(82.3,16.7)]),('Krishna','line',[(73.7,18),(75,16.5),(78,16),(80,16.3),(81,15.8)]),('Cauveri / Kaveri','line',[(75.5,12.4),(77,12.3),(78.2,11.3),(79.8,10.9)]),
('Alluvial soil','region',[(77.5,29),(81,28),(87,25.7),(86,24.2),(80,25.5),(77.5,29)]),('Black soil','region',[(73.5,21),(77,22.2),(79,19),(77,16.8),(74,18),(73.5,21)]),('Red soil','region',[(77,14),(80,14),(79,11),(77,11.5),(77,14)]),('Dense population: Gangetic Plain','region',[(80,27),(85,27),(86,24.5),(81,25),(80,27)]),('Sparse population: Thar','region',[(70,26),(71,28.5),(73,28),(72,25.5),(70,26)]),
('Tropic of Cancer','line',[(68.5,23.5),(89.8,23.5)]),('Standard Meridian 82°30′E','line',[(82.5,17),(82.5,28)]),('SW monsoon: Arabian Sea branch','arrow',[(66,10),(71,16),(74,19)]),('SW monsoon: Bay of Bengal branch','arrow',[(88,16),(89,20),(91,24)]),('Northeast monsoon','arrow',[(83.5,16),(81.5,12),(79,9)]),('Western Disturbances','arrow',[(67,32),(72,32.5),(76,32)])
]
def paper_features(n):
    marking=[FEATURES[(n*3+i*7)%len(FEATURES)] for i in range(6)]
    names={f[0] for f in marking};points=[f for f in FEATURES if f[1]=='point' and f[0] not in names]
    ident=[points[(n+i*3)%len(points)] for i in range(4)]
    assert len({f[0] for f in marking+ident})==10
    return marking,ident

def build_india():
    z=zipfile.ZipFile(ROOT/'assets'/'maps'/'India-outline.zip');data=z.read('Outline_of_India.shp');_,xmin,ymin,xmax,ymax=struct.unpack('<i4d',data[32:68]);scale=min(540/(xmax-xmin),640/(ymax-ymin));W,H=600,710
    def xy(x,y):return 30+(x-xmin)*scale,25+(ymax-y)*scale
    paths=[];pos=100
    while pos<len(data):
        _,words=struct.unpack('>2i',data[pos:pos+8]);record=data[pos+8:pos+8+words*2];pos+=8+words*2
        if struct.unpack('<i',record[:4])[0] not in [5,15,25]:continue
        nparts,npoints=struct.unpack('<2i',record[36:44]);parts=list(struct.unpack('<'+str(nparts)+'i',record[44:44+4*nparts]))+[npoints];offset=44+4*nparts
        points=[xy(*struct.unpack('<2d',record[offset+i*16:offset+i*16+16])) for i in range(npoints)]
        for start,end in zip(parts,parts[1:]):paths.append('M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in simplify(points[start:end]))+' Z')
    outline=f'<path d="{" ".join(paths)}" fill="#fffdf4" fill-rule="evenodd" stroke="#263a45" stroke-width="1.5"/>'
    foot='<text x="20" y="690" style="font-size:10px">Boundary: Survey of India · study overlays are schematic</text>'
    def feature(f,label=True):
        name,kind,coords=f;pts=[xy(*project(lon,lat)) for lon,lat in coords]
        x,y=pts[len(pts)//2];labeltext=f'<text x="{x+5:.2f}" y="{y-6:.2f}" style="font-size:11px">{html.escape(name)}</text>' if label else ''
        if kind=='point':return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.3" fill="#b63d36"/>'+labeltext
        points=' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)
        if kind=='region':return f'<polygon points="{points}" fill="#f2bc52" fill-opacity=".35" stroke="#ab6a13" stroke-width="1.5"/>'+labeltext
        return f'<polyline points="{points}" fill="none" stroke="{"#206a9e" if kind=="line" else "#b63d36"}" stroke-width="2"/>'+labeltext
    save('india-blank.svg',outline+foot,W,H)
    records=[]
    for i,f in enumerate(FEATURES):
        name,kind,coords=f;target=xy(*project(*coords[len(coords)//2]));records.append(dict(id=i,name=name,kind=kind,target=list(target),svg=feature(f),instruction=('Mark and label ' if kind=='point' else 'Shade/trace and label ')+name+'.'))
        save(f'india-feature-{i:02}.svg',outline+feature(f)+foot,W,H)
    for n in range(1,21):
        marking,ident=paper_features(n)
        dots=''
        for letter,f in zip('ABCD',ident):
            x,y=xy(*project(*f[2][0]));dots+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#142b3e"/><text x="{x+7:.2f}" y="{y-5:.2f}">{letter}</text>'
        save(f'india-paper-{n:02}.svg',outline+dots+foot,W,H)
        save(f'india-answer-{n:02}.svg',outline+''.join(feature(f) for f in marking+ident)+foot,W,H)
    (ROOT/'map_catalog.js').write_text('window.ICSE_MAPS='+json.dumps(dict(source=SOURCE,width=W,height=H,outline='assets/diagrams/india-blank.svg',features=records),ensure_ascii=False)+';',encoding='utf-8')
    return FEATURES

def build_physics():
    save('series-parallel.svg','<path class="wire" d="M100 100H250V70H440V100H520V300H300 M280 300H100V100 M250 100V170H440V100"/><rect x="285" y="55" width="110" height="30" fill="white" stroke="#142b3e" stroke-width="2"/><rect x="285" y="155" width="110" height="30" fill="white" stroke="#142b3e" stroke-width="2"/><path d="M280 278V322M300 286V314" stroke="#142b3e" stroke-width="3"/><text x="315" y="45">R₁</text><text x="315" y="215">R₂</text><text x="268" y="355">V</text><text x="130" y="80">A</text><text x="470" y="80">B</text><text x="125" y="390">Both resistors connect between the same two nodes.</text>')
    save('lever.svg','<path d="M65 180H565" class="wire"/><polygon points="315,183 292,225 338,225" fill="#91aba9"/><path d="M120 75V175M500 75V175" class="wire"/><path d="M112 163L120 176L128 163M492 163L500 176L508 163" class="wire"/><text x="90" y="60">Load</text><text x="465" y="60">Effort</text><text x="295" y="252">Pivot</text><text x="153" y="160">Load arm</text><text x="365" y="160">Effort arm</text><text x="85" y="315">Distances are perpendicular distances from the pivot.</text>')
    axis='<path d="M30 215H610M320 50V370" stroke="#344a57" stroke-width="1.5"/><path d="M320 60Q280 215 320 365Q360 215 320 60Z" fill="#d8f0f2" fill-opacity=".6" stroke="#344a57"/><text x="325" y="240">O</text><text x="190" y="238">F₁</text><text x="435" y="238">F₂</text><path d="M80 215V105" stroke="#b63d36" stroke-width="3"/><text x="50" y="93">Object</text>'
    save('convex-lens-question.svg',axis)
    save('convex-lens-answer.svg',axis+'<path d="M80 105H320L560 325M80 105L560 325" class="ray"/><path d="M560 215V325" stroke="#b63d36" stroke-width="3"/><text x="425" y="355">Real, inverted, same size</text>')
    save('refraction.svg','<rect x="50" y="215" width="540" height="175" fill="#e3f1f5"/><path d="M40 215H600" stroke="#142b3e" stroke-width="2"/><path d="M320 45V385" class="wire dash"/><path d="M120 55L320 215L405 360" class="ray"/><text x="350" y="90">Air</text><text x="450" y="300">Glass</text><text x="285" y="140">i</text><text x="338" y="282">r</text><text x="70" y="414">Angles i and r are measured from the normal.</text>')
    save('cooling-curve.svg','<path d="M80 40V350H590" class="wire"/><path d="M100 75L220 145H340L470 265H560" class="ray"/><text x="10" y="34">T (°C)</text><text x="538" y="385">Time</text><text x="220" y="130">B</text><text x="338" y="130">C</text><text x="112" y="65">A</text><text x="475" y="290">D</text><text x="130" y="408">A plateau indicates a change of state at constant pressure.</text>')

if __name__=='__main__':
    build_india();build_physics();print('Built authoritative outline, feature overlays, 20 paper maps and physics diagrams.')
