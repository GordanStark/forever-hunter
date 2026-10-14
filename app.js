const SPN=Object.keys(window.SPELLS||{}).filter(k=>SPELLS[k].u).sort((a,b)=>b.length-a.length);
const SPRX=new RegExp("(?<![\\w'])("+SPN.map(n=>n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+")(?![\\w'])","g");
function spLink(n){const v=SPELLS[n];return `<a class="sp" href="${v.u}" target="_blank" rel="noopener"><img class="ic" src="icons/spells/${v.i}.jpg" alt="">${n}</a>`}
function linkHTML(h){return h.split(/(<[^>]+>)/).map(p=>p.startsWith('<')?p:p.replace(SPRX,m=>spLink(m))).join('')}
const S={get:(k,d)=>{try{return JSON.parse(localStorage.getItem('hq:'+k))??d}catch(e){return d}},set:(k,v)=>localStorage.setItem('hq:'+k,JSON.stringify(v))};
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
// tabs
function showTab(){const id=(location.hash||'#guide').slice(1);const t=$('#t-'+id)?id:'guide';
$$('.tab').forEach(x=>x.classList.toggle('on',x.id==='t-'+t));$$('.tabs a').forEach(a=>a.classList.toggle('on',a.hash==='#'+t));window.scrollTo(0,0)}
addEventListener('hashchange',showTab);showTab();
// level picker
const sel=$('#lvSel');for(let i=1;i<=60;i++)sel.add(new Option(i,i));
function rotFor(l){const a=[];
 if(l>=10)a.push('<b>Aspect of the Hawk</b> on for fights'+(l>=20?' · Aspect of the Cheetah for travel only':''));else if(l>=4)a.push('<b>Aspect of the Monkey</b> on (Hawk comes at 10)');
 if(l>=6)a.push("<b>Hunter's Mark</b> (key 3) before the pull");
 if(l>=10)a.push('Send the pet in first, let it build threat');else a.push('Before 10: back up between Auto Shots, <b>Raptor Strike</b> in melee');
 a.push('<b>Auto Shot</b> (key 4) the whole fight');
 if(l>=4)a.push('<b>Serpent Sting</b> (key 2)'+(l>=10?' once the pet has hit it':''));
 if(l>=26)a.push('<b>Summon Hawk</b> (key 1) on CD, keep 2 up');else if(l>=6)a.push('<b>Arcane Shot</b> (key 1) when mana allows');
 if(l>=20)a.push('<b>Aimed Shot</b> (key 7) on CD'+(l>=18?' · Multi-Shot (Top 4) on groups':''));else if(l>=18)a.push('Multi-Shot (Top 4) on groups');
 if(l>=26)a.push('Arcane Shot (Top 7) only near full mana with 2 hawks up');
 if(l>=8)a.push('Concussive Shot (key 5) to slow runners');
 if(l>=12)a.push('Mend Pet (key 6) between pulls or when it gets low');
 if(l>=20)a.push('Pulled aggro: Disengage (Top 3)'+(l>=30?' · Bad pull: Feign Death (Top 6)':''));
 if(l>=30)a.push('Intimidation (Top 1) to stun a caster or runner');
 return `<ol>${a.map(x=>'<li>'+x+'</li>').join('')}</ol><span class="src">Icy Veins Forever BM · slots = draft bars</span>`}
function setLv(l){l=Math.max(1,Math.min(60,l));S.set('lv',l);sel.value=l;$('#curLv').textContent=l;$('#rotTag').textContent='· Lv '+l;$('#rot').innerHTML=linkHTML(rotFor(l));
 $$('.row').forEach(r=>{const c=+r.dataset.lv===l;r.classList.toggle('cur',c);r.classList.toggle('open',c)})}
sel.onchange=()=>setLv(+sel.value);$('#lvUp').onclick=()=>setLv(+sel.value+1);$('#lvDown').onclick=()=>setLv(+sel.value-1);
$('#rotBtn').onclick=e=>{const r=$('#rot');r.hidden=!r.hidden;e.currentTarget.setAttribute('aria-expanded',!r.hidden)};
// rows
const done=S.get('done',{});
$$('.row').forEach(r=>{const k=r.id;if(done[k])r.classList.add('done');
 r.querySelector('.row-head').onclick=e=>{if(e.target.classList.contains('chk')){r.classList.toggle('done');done[k]=r.classList.contains('done');S.set('done',done);
   if(done[k]&&+r.dataset.lv===+sel.value)setLv(+sel.value+1);return}r.classList.toggle('open')}});
const hd=$('#hideDone');hd.checked=S.get('hideDone',false);document.body.classList.toggle('hidedone',hd.checked);hd.onchange=()=>{S.set('hideDone',hd.checked);document.body.classList.toggle('hidedone',hd.checked)};
// checkboxes
const cb=S.get('cb',{});function wire(i){if(!i.dataset.k)return;i.checked=!!cb[i.dataset.k];i.onchange=()=>{cb[i.dataset.k]=i.checked;S.set('cb',cb)}}
// custom bags
function renderBags(){const list=S.get('bags',[]);$('#customBags').innerHTML=list.map((t,i)=>`<label class="ci"><input type="checkbox" data-k="cb${i}_${t}"><span>${t.replace(/</g,'&lt;')}</span></label>`).join('');$$('input[type=checkbox][data-k]').forEach(wire)}
$('#bagAdd').onclick=()=>{const v=$('#bagNew').value.trim();if(!v)return;const l=S.get('bags',[]);l.push(v);S.set('bags',l);$('#bagNew').value='';renderBags()};
$('#resetBags').onclick=()=>{Object.keys(cb).filter(k=>/^b|^cb/.test(k)).forEach(k=>delete cb[k]);S.set('cb',cb);renderBags()};
renderBags();
const n=$('#notes');n.value=S.get('notes','');n.oninput=()=>S.set('notes',n.value);
setLv(S.get('lv',1));
// my character
fetch('data.json',{cache:'no-cache'}).then(r=>r.json()).then(d=>{const esc=s=>String(s).replace(/</g,'&lt;');
 const g=d.gold||{};const tbl=(o)=>'<table>'+Object.entries(o).map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join('')+'</table>';
 $('#meBox').innerHTML=(d.example?'<div class="example">⚠ EXAMPLE DATA — not your real character. This fills in once the addon sync is set up.</div>':'')+
 `<div class="card"><h3>${esc(d.name)} · Lv ${d.level}</h3><p>${esc(d.race)} ${esc(d.class)} · ${g.g||0}g ${g.s||0}s ${g.c||0}c<br><span class="src">Last synced: ${esc(d.lastSynced)}</span></p></div>`+
 `<div class="card"><h3>Gear</h3>${tbl(Object.fromEntries(d.gear.map(x=>[x.slot,x.item+(x.ilvl?' (ilvl '+x.ilvl+')':'')])))}</div>`+
 `<div class="card"><h3>Professions</h3>${tbl(Object.fromEntries(d.professions.map(p=>[p.name,p.skill+'/'+p.max])))}</div>`+
 `<div class="card"><h3>Bags</h3>${tbl(Object.fromEntries(d.bags.map(b=>[b.item,'×'+b.count])))}</div>`+
 `<div class="card"><h3>Mounts</h3>${d.mounts.length?d.mounts.map(esc).join('<br>'):'None yet'}<span class="src">Mount lookup in Forever's addon API not yet confirmed.</span></div>`
}).catch(()=>{$('#meBox').textContent='No synced data yet.'});
if('serviceWorker' in navigator){navigator.serviceWorker.register('sw.js',{updateViaCache:'none'}).then(r=>r.update());let rl=0;navigator.serviceWorker.addEventListener('controllerchange',()=>{if(!rl){rl=1;location.reload()}})}
(()=>{const q=new URLSearchParams(location.search);if(q.get('lv'))setLv(+q.get('lv'));if(q.get('rot'))$('#rotBtn').click()})();

setTimeout(()=>{if(!location.search.includes('noscroll')&&(location.hash||'#guide')==='#guide'){const r=$('.row.cur');if(r)window.scrollTo(0,r.offsetTop-$('.bar').offsetHeight-8)}},50);
const SH={"Hunter's Mark":"Hunter's Mark",'Serpent Sting':'Serpent Sting','Concussive Shot':'Concus. Shot','Raptor Strike':'Raptor Strike','Arcane Shot':'Arcane Shot','Summon Hawk':'Summon Hawk','Aimed Shot':'Aimed Shot','Auto Shot':'Auto Shot','Mend Pet':'Mend Pet','Wing Clip':'Wing Clip','Disengage':'Disen-gage','Multi-Shot':'Multi-Shot','Freezing Trap':'Freezing Trap','Feign Death':'Feign Death','Intimidation':'Intimi-dation','Feed Pet':'Feed Pet','Revive Pet':'Revive Pet','Call Pet':'Call Pet','Hearthstone':'Hearth-stone','Aspect of the Monkey':'Monkey','Aspect of the Hawk':'Hawk','Aspect of the Cheetah':'Cheetah','Aspect of the Beast':'Beast','Aspect of the Pack':'Pack','Aspect of the Wild':'Wild','Track Beasts':'Track Beasts'};
const IT={Food:'inv_misc_food_11',Water:'inv_drink_07',Hearthstone:'inv_misc_rune_01',Mount:'ability_mount_mountainram'};
function renderBars(l){const b=window.BARS[l],p=window.BARS[l-1];const lab={top:['Top','click · cooldowns & escapes'],mid:['Middle','keys 1-7 · pressed constantly'],bot:['Bottom','out of combat · pet care'],asp:['Aspect bar','aspects + tracking']};
 $('#barLv').textContent=l;
 $('#barsBox').innerHTML=['top','mid','bot','asp'].map(r=>`<div class="brow${r==='asp'?' aur':''}"><div class="blab"><b>${lab[r][0]}</b> ${lab[r][1]}</div><div class="bslots">`+b[r].map((s,i)=>{if(!s)return`<div class="bs empty">${r==='mid'?i+1:''}</div>`;
  const nw=!p||JSON.stringify(p[r][i])!==JSON.stringify(s);const v=IT[s.n]?{i:IT[s.n]}:(SPELLS[s.n]||{});const tag=v.u?'a':'div';return`<${tag} class="bs${nw?' new':''}${s.u?' unc':''}"${v.u?` href="${v.u}" target="_blank" rel="noopener"`:''} title="${s.n}">${v.i?`<img src="icons/spells/${v.i}.jpg" alt="">`:''}${r==='mid'?`<i>${i+1}</i>`:''}<span>${SH[s.n]||s.n}</span>${nw?'<em>NEW</em>':''}</${tag}>`}).join('')+'</div></div>').join('')}
const _setLv=setLv;setLv=function(l){_setLv(l);renderBars(+sel.value)};renderBars(+sel.value);
(()=>{const o=new URLSearchParams(location.search).get('only');if(o)$$('.row').forEach(r=>{if(r.dataset.lv!==o)r.style.display='none'})})();

