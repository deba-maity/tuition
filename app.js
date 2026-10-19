/* Reviewed ICSE 2027 revision dashboard. */
'use strict';
const DATA=window.ICSE_AUDIT;
const $=selector=>document.querySelector(selector);
const escapeHtml=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const paragraphs=value=>escapeHtml(value).replace(/\n/g,'<br>');
function readStorage(key,fallback){try{return JSON.parse(localStorage.getItem(key))??fallback;}catch{return fallback;}}
function writeStorage(key,value){try{localStorage.setItem(key,JSON.stringify(value));}catch{/* Storage is optional. */}}
const state={subject:DATA.subjects.find(s=>s.id===readStorage('icse27:subject','computer'))||DATA.subjects[0],view:'overview',topic:'',search:'',worksheet:[],completed:new Set(readStorage('icse27:completed',[])),pair:readStorage('icse27:hindi-pair','')};
const BOOK_PAIRS={'sahitya-naya':['साहित्य सागर','नया रास्ता'],'sahitya-ekanki':['साहित्य सागर','एकांकी संचय'],'naya-ekanki':['नया रास्ता','एकांकी संचय']};
function subjectPool(){return state.subject.practice.filter(q=>state.subject.id!=='hindi'||!q.book||!BOOK_PAIRS[state.pair]||BOOK_PAIRS[state.pair].includes(q.book));}
function filteredPool(){const search=state.search.toLocaleLowerCase();return subjectPool().filter(q=>(!state.topic||q.topic===state.topic)&&(!search||`${q.topic} ${q.prompt}`.toLocaleLowerCase().includes(search)));}
function sourceLink(url,label){return `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)}</a>`;}
function showView(view){
  state.view=view;
  document.querySelectorAll('.view').forEach(node=>node.classList.toggle('active',node.id===view));
  document.querySelectorAll('[data-view]').forEach(node=>{const active=node.dataset.view===view;node.classList.toggle('active',active);if(active)node.setAttribute('aria-current','page');else node.removeAttribute('aria-current');});
  $('#viewTitle').textContent=`${state.subject.name} · ${{overview:'Revision plan',evidence:'Paper evidence',questions:'Question bank',practice:'Practice worksheet'}[view]}`;
}
function questionCard(q,index,worksheet=false){return `<article class="question-card" data-question-id="${q.id}"><div class="card-head"><h3>${worksheet?`${index+1}. `:''}${escapeHtml(q.topic)}</h3><span class="tag">${q.marks} practice marks</span></div><p class="muted">${escapeHtml(q.id)} · ${escapeHtml(q.difficulty)}${q.book?' · '+escapeHtml(q.book):''}</p><p class="question-text">${paragraphs(q.prompt)}</p><details class="answer-checkpoints"><summary>Answer checkpoints</summary><p>${paragraphs(q.answer)}</p></details>${worksheet?'':`<label class="completion"><input type="checkbox" data-complete="${q.id}" ${state.completed.has(q.id)?'checked':''}> Practised and checked</label>`}</article>`;}
function renderOverview(){
  const s=state.subject;
  $('#subjectOverview').innerHTML=`<div class="hero-copy panel"><p class="eyebrow">2027 revision · checked ${DATA.date}</p><h3>${escapeHtml(s.name)}</h3><p>${escapeHtml(s.focus)}</p><p>${sourceLink(s.syllabus,'Official syllabus / prescribed books')}${s.syllabusMirror?' · '+sourceLink(s.syllabusMirror,'CISCE document text on mirror'):''}</p></div>
  <div class="audit-grid"><section class="panel"><h3>Prepare first</h3><p>${escapeHtml(s.focus)}</p><p class="muted">Core coverage and your own errors determine priority.</p></section><section class="panel"><h3>Extra practice candidates</h3><p>${escapeHtml(s.candidate)}</p><p class="muted">Study-order advice. No calibrated next-paper probability.</p></section><section class="panel"><h3>What to omit or reduce — and why</h3><p>${escapeHtml(s.skip)}</p></section><section class="panel"><h3>Observed exam format</h3><p>${escapeHtml(s.format)}</p><p class="muted">${s.marks} marks · ${s.time}. ${escapeHtml(s.formatBasis)}</p>${s.specimen?'<p>'+sourceLink(s.specimen.url,'2027 CISCE specimen text on mirror')+'</p>':''}</section></div>
  <section class="panel"><h3>Revision checklist</h3><p>${subjectPool().length} original drills; ${subjectPool().filter(q=>state.completed.has(q.id)).length} checked. This bank samples skills; it does not replace the complete syllabus.</p><div class="topic-chips">${[...new Set(subjectPool().map(q=>q.topic))].map(topic=>`<button type="button" data-topic="${escapeHtml(topic)}" class="secondary-btn">${escapeHtml(topic)}</button>`).join('')}</div></section>`;
}
function renderEvidence(){
  const s=state.subject;
  $('#previousPapers').innerHTML=`<section class="panel"><p class="eyebrow">Sources and concise decision rationale</p><h3>${escapeHtml(s.name)}: 2023–2026</h3><p>${escapeHtml(DATA.notes[0])}</p><p>${escapeHtml(DATA.notes[1])}</p><p>${escapeHtml(DATA.notes[3])}</p><p>${sourceLink('ICSE_2027_Evidence_and_Revision_Guide.md','Full evidence and revision guide')} · <a href="research/question_inventory.csv" download>Question inventory CSV</a> · ${sourceLink('research/source_manifest.json','Source manifest')}</p></section>
  <section class="panel"><h3>Reviewed evidence anchors</h3><div class="table-scroll"><table><thead><tr><th>Year</th><th>Question</th><th>Observed family or text</th></tr></thead><tbody>${s.evidence.map(([year,ref,description])=>`<tr><td>${escapeHtml(year)}</td><td>${escapeHtml(ref)}</td><td>${escapeHtml(description)}</td></tr>`).join('')}</tbody></table></div></section>
  <section class="panel"><h3>What follows from the evidence</h3><p>${escapeHtml(s.candidate)}</p><p>${escapeHtml(s.skip)}</p><p>For example, Computer Applications had both bubble sort and linear search in 2023. Matrix programs occur in 2024, 2025 and 2026. That contradicts a rule that last year’s program family can be omitted.</p></section>
  <section class="panel"><h3>2027 specimen check</h3><p>${escapeHtml(s.formatBasis)}</p><p>${s.specimen?sourceLink(s.specimen.url,'Open mirrored CISCE specimen text'):'No verified 2027 specimen link is attached for this subject.'}</p><p>Specimens demonstrate scope and question style. Their selections do not establish which chapters will appear in the actual paper. Diagrams and full draft marking schemes have not been independently checked.</p></section>
  <section class="panel"><h3>Open the actual main papers</h3><p>These are CISCE papers on an independent mirror. Improvement papers are excluded. Question locations combine OCR with manual page checks; they are not prediction probabilities.</p><div class="source-cards">${s.sources.map(p=>`<article><h4>${sourceLink(p.url,`${p.year} main paper`)}</h4><p>${p.pages} pages · ${p.recovered}/${p.expected} main questions located</p></article>`).join('')}</div></section>
  <section class="panel"><h3>Question-level inventory</h3><p>${s.inventory.length} expected main-question slots; ${s.inventory.filter(r=>!r.pdf_page).length} have unresolved page/heading extraction. Tags may be incomplete and are not marks-weighted frequency estimates. Title/program reviews are labelled separately.</p><div class="table-scroll"><table><thead><tr><th>Year / Q</th><th>PDF page</th><th>Family</th><th>Review status</th></tr></thead><tbody>${s.inventory.map(r=>`<tr><td>${sourceLink(r.url+(r.pdf_page?'#page='+Number(r.pdf_page):''),`${r.year} Q${r.question}`)}</td><td>${r.pdf_page||'Unresolved'}</td><td>${escapeHtml(r.family||'Inspect original PDF')}</td><td>${escapeHtml(r.status)}</td></tr>`).join('')}</tbody></table></div></section>`;
}
function renderQuestions(){const pool=filteredPool();$('#questionCount').textContent=`${pool.length} drills shown · answer checkpoints available`;$('#subjectTopics').innerHTML=pool.length?pool.map((q,i)=>questionCard(q,i)).join(''):'<p class="panel">No questions match these filters. Clear the topic or search.</p>';}
function renderTopicOptions(){
  const topics=[...new Set(subjectPool().map(q=>q.topic))];if(!topics.includes(state.topic))state.topic='';
  $('#topicFilter').innerHTML='<option value="">All topics</option>'+topics.map(t=>`<option value="${escapeHtml(t)}">${escapeHtml(t)}</option>`).join('');$('#topicFilter').value=state.topic;
  $('#worksheetTopic').innerHTML=$('#topicFilter').innerHTML;$('#worksheetTopic').value='';
  const levels=new Set(subjectPool().map(q=>q.difficulty));[...$('#difficultySelect').options].forEach(o=>{o.disabled=o.value!=='Balanced'&&!levels.has(o.value);});$('#difficultySelect').value='Balanced';
}
function render(){
  $('#hindiBookControl').hidden=state.subject.id!=='hindi';$('#hindiPair').value=state.pair;
  $('#practiceIntro').textContent='Generate a short revision worksheet from the reviewed bank. Its marks are the sum of the selected drills. For a full timed board mock, use a linked actual paper and its printed section choices.';
  $('#hindiPairNote').textContent=BOOK_PAIRS[state.pair]?'Literature is filtered to these two school books.':'Choose the school’s two books to include Hindi literature in generated sets. All prescribed books remain visible for reference.';
  renderOverview();renderEvidence();renderQuestions();showView(state.view);
}
function clearWorksheet(){state.worksheet=[];$('#paperOutput').innerHTML='<p class="panel">Choose topic, difficulty and set size, then generate a worksheet.</p>';$('#downloadPaperBtn').disabled=true;$('#downloadTextBtn').disabled=true;}
function selectSubject(id){state.subject=DATA.subjects.find(s=>s.id===id)||DATA.subjects[0];state.topic='';state.search='';$('#questionSearch').value='';writeStorage('icse27:subject',state.subject.id);$('#homeSubjectSelect').value=state.subject.id;clearWorksheet();renderTopicOptions();render();}
function shuffled(items){const copy=[...items];for(let i=copy.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[copy[i],copy[j]]=[copy[j],copy[i]];}return copy;}
function chooseWorksheet(pool,count,recent=[]){
  // Prefer unused IDs and breadth. Never mutate wording to manufacture novelty.
  const order=[...shuffled(pool.filter(q=>!recent.includes(q.id))),...shuffled(pool.filter(q=>recent.includes(q.id)))],picked=[],topics=new Set();
  for(const q of order)if(!topics.has(q.topic)&&picked.length<count){picked.push(q);topics.add(q.topic);}
  for(const q of order)if(picked.length<count&&!picked.some(p=>p.id===q.id))picked.push(q);
  return picked;
}
function generateWorksheet(){
  const difficulty=$('#difficultySelect').value,topic=$('#worksheetTopic').value,count=Number($('#setSize').value);
  let pool=subjectPool().filter(q=>(!topic||q.topic===topic)&&(difficulty==='Balanced'||q.difficulty===difficulty));
  if(state.subject.id==='hindi'&&!BOOK_PAIRS[state.pair])pool=pool.filter(q=>!q.book);
  if(!pool.length){clearWorksheet();$('#paperOutput').innerHTML='<p class="panel" role="status">No drills match this combination. Choose Balanced or another topic. Hindi literature needs the school’s two-book selection.</p>';return;}
  const key='icse27:recent:'+state.subject.id,recent=readStorage(key,[]);state.worksheet=chooseWorksheet(pool,count,recent);
  writeStorage(key,[...new Set([...state.worksheet.map(q=>q.id),...recent])].slice(0,40));renderWorksheet();$('#downloadPaperBtn').disabled=false;$('#downloadTextBtn').disabled=false;
}
function renderWorksheet(){
  const total=state.worksheet.reduce((sum,q)=>sum+q.marks,0);
  $('#paperOutput').innerHTML=`<div class="worksheet-heading"><p class="eyebrow">Original revision worksheet · 2027 preparation</p><h3>${escapeHtml(state.subject.name)} · ${total} practice marks</h3><p>Answer all ${state.worksheet.length} drills below. This set is not a complete board paper.${state.worksheet.length<Number($('#setSize').value)?' The filtered bank contains fewer items than requested.':''}</p>${state.worksheet.some(q=>q.topic==='India outline map')?'<p>Teacher must supply the outline map and choose prescribed locations for the map template.</p>':''}</div>`+state.worksheet.map((q,i)=>questionCard(q,i,true)).join('');
  $('#paperOutput').classList.toggle('include-key',$('#includeKey').checked);
  if($('#includeKey').checked)$('#paperOutput').querySelectorAll('.answer-checkpoints').forEach(details=>{details.open=true;});
}
function downloadWorksheet(){
  const total=state.worksheet.reduce((sum,q)=>sum+q.marks,0);
  let content=`# ${state.subject.name} — revision worksheet\n\n${total} practice marks. Answer all drills. Not a complete board paper.\n\n`;
  content+=state.worksheet.map((q,i)=>`## ${i+1}. ${q.topic} [${q.marks}]\n\n${q.prompt}\n`).join('\n');
  if($('#includeKey').checked)content+='\n# Teacher answer checkpoints\n\n'+state.worksheet.map((q,i)=>`${i+1}. ${q.answer}`).join('\n\n');
  const url=URL.createObjectURL(new Blob([content],{type:'text/markdown;charset=utf-8'})),anchor=document.createElement('a');anchor.href=url;anchor.download=`ICSE_2027_${state.subject.id}_worksheet.md`;document.body.append(anchor);anchor.click();anchor.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function init(){
  if(!DATA||DATA.subjects.length!==10)throw new Error('Reviewed subject data is missing.');
  $('#homeSubjectSelect').innerHTML=DATA.subjects.map(s=>`<option value="${s.id}">${escapeHtml(s.name)}</option>`).join('');$('#homeSubjectSelect').value=state.subject.id;
  $('#patternNotes').innerHTML=DATA.notes.map(n=>`<li>${escapeHtml(n)}</li>`).join('');
  $('#homeStatsGrid').innerHTML=`<article class="stat-card"><strong>40</strong><span>Main papers collected</span></article><article class="stat-card"><strong>10</strong><span>Confirmed subjects</span></article><article class="stat-card"><strong>${DATA.subjects.reduce((n,s)=>n+s.practice.length,0)}</strong><span>Original revision drills</span></article>`;
  $('#homeSubjectSelect').addEventListener('change',e=>selectSubject(e.target.value));document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>showView(button.dataset.view)));
  $('#hindiPair').addEventListener('change',e=>{state.pair=e.target.value;writeStorage('icse27:hindi-pair',state.pair);clearWorksheet();renderTopicOptions();render();});
  $('#topicFilter').addEventListener('change',e=>{state.topic=e.target.value;renderQuestions();});$('#questionSearch').addEventListener('input',e=>{state.search=e.target.value;renderQuestions();});
  $('#subjectOverview').addEventListener('click',e=>{const button=e.target.closest('[data-topic]');if(button){state.topic=button.dataset.topic;$('#topicFilter').value=state.topic;renderQuestions();showView('questions');}});
  $('#subjectTopics').addEventListener('change',e=>{if(e.target.dataset.complete){if(e.target.checked)state.completed.add(e.target.dataset.complete);else state.completed.delete(e.target.dataset.complete);writeStorage('icse27:completed',[...state.completed]);renderOverview();}});
  $('#generatePaperBtn').addEventListener('click',generateWorksheet);$('#downloadPaperBtn').addEventListener('click',()=>window.print());$('#downloadTextBtn').addEventListener('click',downloadWorksheet);$('#includeKey').addEventListener('change',()=>{if(state.worksheet.length)renderWorksheet();});
  clearWorksheet();renderTopicOptions();render();$('#loading').hidden=true;
}
try{init();}catch(error){$('#loading').textContent='Unable to load reviewed data. Start the local server and reload.';console.error(error);}
