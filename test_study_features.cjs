const assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {chromium}=require('C:/Users/debajyothi.m/CMS/node_modules/playwright');
async function select(p,sid){await p.selectOption('#homeSubjectSelect',sid);await p.waitForFunction(s=>state.sid===s&&state.pack,sid);}
(async()=>{
 const browser=await chromium.launch();const errors=[];
 try{
  const p=await browser.newPage({viewport:{width:1440,height:1000}});p.on('pageerror',e=>errors.push(e.message));
  await p.goto('file:///C:/Users/debajyothi.m/10/tuition/index.html');await p.waitForSelector('#loading[hidden]',{state:'attached'});await p.evaluate(()=>localStorage.clear());await p.reload();await p.waitForFunction(()=>state.pack);
  await p.click('[data-view="questions"]');const first=p.locator('.question-card').first();
  await first.locator('summary').click();assert.match(await first.locator('.worked-answer').innerText(),/Multiply before adding/);
  await first.locator('[data-rating="wrong"]').click();assert.match(await first.locator('.review-status').innerText(),/Wrong/i);assert.equal(await first.locator('details').getAttribute('open'),'');
  await p.selectOption('#reviewFilter','wrong');assert.equal(await p.locator('.question-card').count(),1);
  await p.reload();await p.waitForFunction(()=>state.pack);await p.click('[data-view="progress"]');assert.match(await p.locator('#progressOutput').innerText(),/1 questions need work/);
  await p.click('[data-view="practice"]');await p.click('[data-timer="start"]');
  await p.evaluate(()=>{const key='icse27:timer:worked-r2:computer:1:';localStorage.setItem(key,JSON.stringify({used:35*60000,running:false}));});
  await p.click('#completePaper');await p.fill('#paperScore','96');await p.fill('#paperErrorNote','Recheck binary search bounds.');await p.click('#paperScoreForm button');assert.match(await p.locator('#scoreStatus').innerText(),/Saved/);
  await p.click('[data-view="progress"]');assert.match(await p.locator('#progressOutput').innerText(),/1 timed papers at 95%/);assert.match(await p.locator('#progressOutput').innerText(),/96\/100/);
  const downloadPromise=p.waitForEvent('download');await p.click('#exportStudy');const download=await downloadPromise;const backup=JSON.parse(fs.readFileSync(await download.path(),'utf8'));assert.equal(backup.version,1);assert.ok(Object.keys(backup.data).some(k=>k.includes('review:worked-r2')));
  await p.setInputFiles('#importStudy',{name:'invalid.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({version:1,data:{'icse27:subject':'"maths"','icse27:bad':'not JSON'}}))});await p.waitForFunction(()=>document.querySelector('#backupStatus').textContent);assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('icse27:subject'))),'computer');
  await select(p,'geo');await p.click('[data-view="maps"]');assert.equal(await p.locator('#mapFeature option').count(),70);await p.click('#mapShowKey');assert.ok(await p.locator('#indiaCanvas text').count()>0);
  await p.click('#indiaCanvas',{position:{x:250,y:250}});assert.match(await p.locator('#mapFeedback').innerText(),/location|overlay/);
  await p.selectOption('#topoSheet','G43S10');await p.waitForFunction(()=>document.querySelector('#topoImage').complete&&document.querySelector('#topoImage').naturalWidth>0);await p.click('#topoZoomIn');assert.equal(await p.locator('#topoImage').getAttribute('style'),'width: 150%;');
  await p.click('[data-view="practice"]');assert.equal(await p.locator('#paperOutput img[src*="india-answer"]').count(),0);assert.equal(await p.locator('#paperOutput img[src*="india-paper"]').count(),1);await p.click('#completePaper');assert.equal(await p.locator('#paperOutput img[src*="india-answer"]').count(),1);
  await p.emulateMedia({media:'print'});assert.equal(await p.locator('#paperStudyTools').isVisible(),false);await p.emulateMedia({media:'screen'});
  await select(p,'phy');await p.click('[data-view="questions"]');await p.selectOption('#topicFilter','Lenses');assert.ok(await p.locator('#subjectTopics img[src*="convex-lens-question"]').count()>0);
  await p.setViewportSize({width:390,height:844});await select(p,'geo');await p.click('[data-view="maps"]');assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  // A downloaded HTML paper must keep its maps outside the original directory.
  const target=path.join(os.tmpdir(),'icse-standalone-map-paper.html');fs.copyFileSync(path.join(__dirname,'subjects/geo/practice/paper-01.html'),target);const standalone=await browser.newPage();standalone.on('pageerror',e=>errors.push(e.message));await standalone.goto('file:///'+target.replaceAll('\\','/'));await standalone.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));assert.equal(await standalone.locator('.solution').count(),0);fs.unlinkSync(target);
  assert.deepEqual(errors,[]);console.log('PASS worked traces, mistake persistence, timed scores, atomic backup validation, maps/zoom, diagram keys, print and standalone export');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
