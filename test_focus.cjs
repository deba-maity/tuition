const assert=require('node:assert/strict');
const {chromium}=require('C:/Users/debajyothi.m/CMS/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch();
 try{
  const p=await browser.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto('file:///'+__dirname.replaceAll('\\','/')+'/index.html');await p.waitForFunction(()=>state.pack);
  await p.evaluate(()=>localStorage.clear());await p.reload();await p.waitForFunction(()=>state.pack);
  await p.click('[data-view="focus"]');await p.selectOption('#focusCount','5');await p.click('[data-focus="start"]');
  assert.equal(await p.locator('.focus-solution').count(),0);
  await p.fill('#focusWorking','My independent working');await p.click('[data-focus="reveal"]');
  assert.ok(await p.locator('.worked-answer').isVisible());await p.fill('#focusNote','Check operator precedence.');
  await p.click('[data-focus="wrong"]');await p.click('[data-focus="next"]');
  await p.reload();await p.waitForFunction(()=>state.pack);await p.click('[data-view="focus"]');await p.click('[data-focus="resume"]');
  assert.match(await p.locator('.focus-question .eyebrow').innerText(),/Question 2 of 5/i);
  await p.click('[data-focus="menu"]');await p.selectOption('#focusMode','mistakes');await p.click('[data-focus="start"]');
  assert.equal(await p.inputValue('#focusWorking'),'My independent working');await p.click('[data-focus="reveal"]');
  assert.equal(await p.inputValue('#focusNote'),'Check operator precedence.');await p.click('[data-focus="correct"]');
  let r=await p.evaluate(()=>Object.values(JSON.parse(localStorage.getItem('icse27:review:worked-r2')))[0]);assert.equal(r.status,'correct');
  await p.evaluate(()=>{const k='icse27:review:worked-r2',r=JSON.parse(localStorage.getItem(k));Object.values(r).forEach(x=>{x.last-=2*86400000;x.due=Date.now()-1000;});localStorage.setItem(k,JSON.stringify(r));ICSE_STUDY.invalidate();});
  await p.click('[data-focus="menu"]');await p.selectOption('#focusMode','mistakes');await p.click('[data-focus="start"]');await p.click('[data-focus="reveal"]');await p.click('[data-focus="correct"]');
  r=await p.evaluate(()=>Object.values(JSON.parse(localStorage.getItem('icse27:review:worked-r2')))[0]);assert.equal(r.status,'mastered');
  await p.click('[data-view="questions"]');await p.check('#onePerFamily');
  assert.match(await p.locator('#questionCount').innerText(),/40 matching questions in 40 families/);
  for(const sid of ['english1','english2','hindi','maths','histciv','geo','phy','chem','bio']){
   await p.selectOption('#homeSubjectSelect',sid);await p.waitForFunction(s=>state.sid===s&&state.pack,sid);
   await p.click('[data-view="focus"]');await p.click('[data-focus="start"]');assert.equal(await p.locator('.focus-question').count(),1);
  }
  await p.setViewportSize({width:390,height:844});assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  assert.deepEqual(errors,[]);console.log('PASS all-subject focused practice, saved drafts, resume, mistakes, delayed mastery and family browsing');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
