"""Cache publicly available primary map documents for offline study."""
import urllib.request, json
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parent
SOURCES={
'G43S10':'https://surveyofindia.gov.in/files/45D10.pdf',
'G43S7':'https://surveyofindia.gov.in/files/45d7education%20map.pdf',
'India-outline':'https://surveyofindia.gov.in/webroot/UserFiles/files/1_16%282%29.pdf',
'geography-2027-specimen':'https://cisce.org/wp-content/uploads/2026/08/ICSE-2027-SPECIMEN-502-GEOGRAPHY-QP-MS.pdf',
}
def main():
    result=[]
    for name,url in SOURCES.items():
        target=ROOT/'assets'/'maps'/(name+'.pdf');target.parent.mkdir(parents=True,exist_ok=True)
        try:
            if not target.exists():
                request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
                with urllib.request.urlopen(request,timeout=40) as response:data=response.read()
                if not data.startswith(b'%PDF'):raise ValueError('Response is not a PDF')
                target.write_bytes(data)
            document=pymupdf.open(target)
            print(name,document.page_count,document[0].rect)
            result.append(dict(name=name,url=url,path=str(target.relative_to(ROOT)).replace('\\','/'),pages=document.page_count))
            if name.startswith('G43'):
                page=document[0];page.get_pixmap(matrix=pymupdf.Matrix(.45,.45)).save(ROOT/'assets'/'maps'/(name+'-overview.png'))
            elif name=='geography-2027-specimen':
                for i,page in enumerate(document):
                    text=page.get_text()
                    if 'outline' in text.lower() or i in [12,13]:print('page',i+1,text[:120].replace('\n',' '))
        except Exception as error:print(name,type(error).__name__,str(error))
    (ROOT/'assets'/'maps'/'sources.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if __name__=='__main__':main()
