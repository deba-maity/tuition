'use strict';
// Short, family-balanced practice; all work stays in the browser and in backups.
window.ICSE_FOCUS=(()=>{
 const E=v=>ICSE_UI.escape(v),$=s=>document.querySelector(s);
 let session=null,index=0,revealed=false;
 const key=()=>`icse27:focus:${state.sid}:${state.pair}`;
 const notesKey=id=>`icse27:working:${state.sid}:${id}`;
 const reviews=()=>read('icse27:review:worked-r2',{});
 function choose(items,records,count,mode,now=Date.now()){
  const rank=q=>{const r=records[state.sid+':'+q.id]||{};return r.status==='wrong'?0:r.due&&r.due<=now?1:!r.attempts?2:3;};
  let candidates=items.filter(q=>mode!=='mistakes'||rank(q)<2);
  candidates=candidates.map((q,i)=>({q,i,rank:rank(q)})).sort((a,b)=>a.rank-b.rank||a.i-b.i);
  const selected=[],families=new Set();
  for(const {q} of candidates){const f=q.family||q.topic;if(!families.has(f)){selected.push(q);families.add(f);}if(selected.length===count)break;}
  if(selected.length<count)for(const {q}of candidates){if(!selected.includes(q))selected.push(q);if(selected.length===count)break;}
  return selected;
 }
 function setup(){
  $('.subject-nav').insertAdjacentHTML('beforeend','<button data-view="focus">Focused practice</button>');
  $('.workspace').insertAdjacentHTML('beforeend','<section id="focus" class="view"><div id="focusOutput"></div></section>');
  $('[data-view="focus"]').addEventListener('click',()=>showView('focus'));
  $('#questionSearch').parentElement.insertAdjacentHTML('afterend','<div><label for="familyFilter">Question family</label><select id="familyFilter"><option value="">All families</option></select></div><label class="family-toggle"><input id="onePerFamily" type="checkbox"> One example per family</label>');
  for(const id of ['familyFilter','onePerFamily'])$('#'+id).addEventListener('change',()=>{state.page=1;renderQuestions();});
  document.addEventListener('input',e=>{if(e.target.id==='focusWorking'||e.target.id==='focusNote'){const q=current();if(q){const record=read(notesKey(q.id),{});record[e.target.id==='focusWorking'?'working':'note']=e.target.value;save(notesKey(q.id),record);$('#workingStatus').textContent='Saved on this device';}}});
  document.addEventListener('click',e=>{
   const b=e.target.closest('[data-focus]');if(!b)return;
   const action=b.dataset.focus;
   if(action==='start'){
    const items=pool().filter(q=>!$('#focusTopic').value||q.topic===$('#focusTopic').value);
    const chosen=choose(items,reviews(),Number($('#focusCount').value),$('#focusMode').value);
    session={ids:chosen.map(q=>q.id),index:0,results:{},started:Date.now()};index=0;save(key(),session);render();
   }else if(action==='retry'){
    showView('focus');session={ids:[b.dataset.id],index:0,results:{},started:Date.now()};index=0;revealed=false;save(key(),session);renderQuestion();
   }else if(action==='resume'){session=read(key(),null);index=session?.index||0;revealed=false;renderQuestion();}
   else if(action==='reveal'){revealed=true;renderQuestion();}
   else if(action==='next'){index++;session.index=index;save(key(),session);revealed=false;renderQuestion();}
   else if(action==='menu'){session=null;render(true);}
   else if(action==='wrong'||action==='correct'){
    const q=current();if(!q||!revealed)return;
    const recs=reviews(),k=state.sid+':'+q.id,old=recs[k]||{};
    // An immediate second click cannot establish delayed recall.
    const delayed=old.last&&Date.now()-old.last>=86400000;
    const status=action==='correct'&&delayed?'mastered':action;
    recs[k]={...old,status,attempts:(old.attempts||0)+1,last:Date.now(),due:Date.now()+({wrong:1,correct:3,mastered:7}[status])*86400000};
    save('icse27:review:worked-r2',recs);ICSE_STUDY.invalidate();session.results[q.id]=status;save(key(),session);renderQuestion();
   }
  });
 }
 function families(){const el=$('#familyFilter');if(!el)return;const old=el.value;const counts=new Map();for(const q of pool()){const f=q.family||q.topic;counts.set(f,(counts.get(f)||0)+1);}el.innerHTML='<option value="">All families</option>'+[...counts].map(([f,n])=>`<option value="${E(f)}">${E(f)} (${n})</option>`).join('');el.value=counts.has(old)?old:'';}
 function filter(qs){const f=$('#familyFilter')?.value;qs=qs.filter(q=>!f||(q.family||q.topic)===f);if($('#onePerFamily')?.checked){const seen=new Set();qs=qs.filter(q=>{const f=q.family||q.topic;if(seen.has(f))return false;seen.add(f);return true;});}return qs;}
 function current(){return session&&pool().find(q=>q.id===session.ids[index]);}
 function render(menu=false){
  if(!state.pack){$('#focusOutput').innerHTML='<p class="panel">Loading questions…</p>';return;}
  if(session&&!menu&&read(key(),null)?.started===session.started){renderQuestion();return;}
  session=null;revealed=false;
  const saved=read(key(),null),r=reviews(),due=pool().filter(q=>{const x=r[state.sid+':'+q.id];return x&&(x.status==='wrong'||x.due<=Date.now());}).length;
  $('#focusOutput').innerHTML=`<section class="panel"><p class="eyebrow">Recall → check → correct → retest</p><h3>A manageable session with different question families</h3><p>Start with mistakes and due reviews, then cover new families. Work on paper or type your answer before opening the solution. This is a practice session, not a board-format paper.</p><div class="focus-settings"><label>Topic<select id="focusTopic"><option value="">All topics</option>${[...new Set(pool().map(q=>q.topic))].map(t=>`<option>${E(t)}</option>`).join('')}</select></label><label>Session size<select id="focusCount"><option>5</option><option selected>10</option><option>20</option></select></label><label>Questions<select id="focusMode"><option value="mixed">Mistakes, due reviews and new skills</option><option value="mistakes">Mistakes and due reviews only (${due})</option></select></label></div><button class="primary-btn" data-focus="start">Start session</button> ${saved?.ids?.length&&saved.index<saved.ids.length?'<button class="secondary-btn" data-focus="resume">Resume saved session</button>':''}<p class="muted">Working and correction notes save automatically and are included in your progress backup. “Correct on retest” requires at least 24 hours since the previous rating.</p></section>`;
 }
 function renderQuestion(){
  const q=current();
  if(!q){const results=Object.values(session?.results||{});$('#focusOutput').innerHTML=`<section class="panel"><h3>Session finished</h3><p>${results.length} checked · ${results.filter(x=>x==='wrong').length} need correction · ${results.filter(x=>x==='mastered').length} correct on a delayed retest.</p><p>Correct your errors now, then return tomorrow and solve them without looking at the model.</p><button class="primary-btn" data-focus="menu">Choose another session</button></section>`;return;}
  const draft=read(notesKey(q.id),{}),rated=session.results[q.id];
  $('#focusOutput').innerHTML=`<section class="panel focus-question"><p class="eyebrow">Question ${index+1} of ${session.ids.length} · ${E(q.topic)} · ${q.marks} marks</p><h3>${E(q.family||q.topic)}</h3><p class="question-text">${E(q.prompt).replace(/\n/g,'<br>')}</p>${ICSE_UI.figures(q)}${ICSE_UI.subquestions(q)}${q.options?'<ol type="a">'+q.options.map(o=>`<li>${E(o)}</li>`).join('')+'</ol>':''}<label for="focusWorking">Your working / answer (or work in your notebook)</label><textarea id="focusWorking" rows="7" maxlength="20000" placeholder="Attempt the question before checking the solution.">${E(draft.working||'')}</textarea><p id="workingStatus" role="status">${draft.working||draft.note?'Saved on this device':''}</p>${revealed?`<div class="focus-solution"><h4>Check your answer</h4>${ICSE_UI.solution(q)}</div><label for="focusNote">What went wrong, and how will you avoid it?</label><textarea id="focusNote" rows="3" maxlength="3000" placeholder="E.g. I used integer division; identify the operand types before calculating.">${E(draft.note||'')}</textarea><div class="focus-actions"><button class="secondary-btn" data-focus="wrong" ${rated?'disabled':''}>Needs work</button><button class="secondary-btn" data-focus="correct" ${rated?'disabled':''}>Correct without help</button><button class="primary-btn" data-focus="next" ${!rated?'disabled':''}>Next question</button></div><p role="status">${rated?'Saved: '+E(rated)+'. This question is scheduled for review.':'Compare every part, including units, evidence and required working. Rate your attempt to continue.'}</p>`:'<button class="primary-btn" data-focus="reveal">I have attempted it — show solution</button>'}<button class="secondary-btn" data-focus="menu">Pause session</button></section>`;
 }
 function notebook(){
  const entries=pool().map(q=>({q,draft:read(notesKey(q.id),{})})).filter(x=>x.draft.note||x.draft.working);
  if(!entries.length)return '<section class="panel"><h3>Your working and corrections</h3><p>Working and correction notes from focused practice will appear here.</p></section>';
  return `<section class="panel"><h3>Your working and corrections (${entries.length})</h3><p>Reattempt without the solution before comparing your earlier working.</p>${entries.map(({q,draft})=>`<details class="answer-checkpoints"><summary>${E(q.topic)} · ${E(q.id)}</summary><p>${E(q.prompt)}</p><h4>Your earlier working</h4><pre class="worked-answer">${E(draft.working||'Worked in notebook')}</pre><h4>Correction to remember</h4><p>${E(draft.note||'No correction note saved.')}</p><button class="secondary-btn" data-focus="retry" data-id="${E(q.id)}">Reattempt this question</button></details>`).join('')}</section>`;
 }
 return {setup,render,families,filter,choose,notebook};
})();
