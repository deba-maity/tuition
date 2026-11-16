const assert=require('node:assert/strict');
const {chromium}=require('C:/Users/debajyothi.m/CMS/node_modules/playwright');
const subjects=['english1','english2','hindi','maths','computer','histciv','geo','phy','chem','bio'];
const errors=[];
async function loaded(p,id){await p.waitForFunction(s=>state.sid===s&&state.pack!==null,id);}
async function select(p,id){await p.selectOption('#homeSubjectSelect',id);await loaded(p,id);}
async function run(url){
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});page.on('pageerror',e=>errors.push(e.message));
  await page.goto(url);await page.waitForSelector('#loading[hidden]',{state:'attached'});
  await page.evaluate(()=>localStorage.clear());await page.reload();await loaded(page,'computer');
  for(const sid of subjects){
   await select(page,sid);
   if(sid==='hindi')await page.selectOption('#hindiPair','sahitya-naya');
   await page.click('[data-view="practice"]');assert.equal(await page.locator('.paper-tile').count(),20);
   for(let n=1;n<=20;n++){
    await page.click(`[data-paper="${n}"]`);
    assert.match(await page.locator('.exam-header h2').innerText(),new RegExp('Paper '+String(n).padStart(2,'0')));
    assert.equal(await page.locator('.exam-solution').count(),0);
    assert.equal(await page.locator('#showAnswers').isDisabled(),true);
    assert.ok(await page.locator('.exam-section').count()>=1);
   }
   await page.click('[data-paper="1"]');await page.click('#completePaper');
   assert.equal(await page.locator('#showAnswers').isEnabled(),true);assert.ok(await page.locator('.exam-solution').count()>0);
   await page.click('#showQuestions');assert.equal(await page.locator('.exam-solution').count(),0);
   await page.click('[data-paper="2"]');assert.equal(await page.locator('#showAnswers').isDisabled(),true);
   await page.click('[data-paper="1"]');assert.equal(await page.locator('#showAnswers').isEnabled(),true);
   await page.reload();await loaded(page,sid);await page.click('[data-view="practice"]');assert.equal(await page.locator('#showAnswers').isEnabled(),true);
   await page.click('#resetPaper');assert.equal(await page.locator('#showAnswers').isDisabled(),true);assert.equal(await page.locator('.exam-solution').count(),0);
  }
  await select(page,'maths');await page.click('[data-view="questions"]');assert.match(await page.locator('#questionCount').innerText(),/2,100/);
  await page.selectOption('#sectionFilter','100 exam challenge questions');assert.match(await page.locator('#questionCount').innerText(),/100 matching/);assert.equal(await page.locator('.question-card').count(),40);
  const first=await page.locator('.question-card').first().getAttribute('data-question-id');
  await page.click('#bankPaginationTop [data-page="2"]');assert.notEqual(await page.locator('.question-card').first().getAttribute('data-question-id'),first);
  await page.fill('#questionSearch','NO_MATCH_123456');assert.equal(await page.locator('.question-card').count(),0);
  await select(page,'geo');await page.click('[data-view="overview"]');assert.match(await page.locator('#subjectOverview').innerText(),/Waste management/i);assert.match(await page.locator('#subjectOverview').innerText(),/Agriculture/);
  await page.click('[data-view="practice"]');await page.emulateMedia({media:'print'});assert.equal(await page.locator('.practice-intro').isVisible(),false);assert.equal(await page.locator('.exam-paper').isVisible(),true);assert.equal(await page.locator('#paperControls').isVisible(),false);
  await page.pdf({path:'C:/Users/debajyothi.m/CMS/tmp/tuition-geography-print.pdf',format:'A4',printBackground:true});await page.emulateMedia({media:'screen'});
  await page.setViewportSize({width:390,height:844});
  for(const sid of ['english1','hindi','computer','geo']){
   await select(page,sid);if(sid==='hindi')await page.selectOption('#hindiPair','naya-ekanki');await page.click('[data-view="practice"]');
   const dims=await page.evaluate(()=>({viewport:innerWidth,content:document.documentElement.scrollWidth}));assert.ok(dims.content<=dims.viewport+1,JSON.stringify({sid,...dims}));
  }
  await page.screenshot({path:'C:/Users/debajyothi.m/CMS/tmp/tuition-mobile.png',fullPage:false});
  assert.deepEqual(errors,[]);console.log('PASS',url,'200 papers, answers/persistence/reset, banks, print and mobile');
 }finally{await browser.close();}
}
(async()=>{await run('file:///C:/Users/debajyothi.m/10/tuition/index.html');await run('http://127.0.0.1:8765/');})().catch(e=>{console.error(e);process.exitCode=1;});
