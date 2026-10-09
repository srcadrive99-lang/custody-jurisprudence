# -*- coding: utf-8 -*-
import json,re,sys
sys.path.insert(0,'/home/claude/work')
from assemble import SEC, ORDER, mn_plain
J=json.load(open('/home/claude/work/build/nuqul_7_9.json',encoding='utf8'))
css=open('/home/claude/work/fav_css.txt',encoding='utf8').read()
ents=[e for e in J['entries'] if e['axis']!=6 and 'counter' not in e['supports'] and e.get('card_number')]
data={'meta':{'version':J['meta']['version'],'date':J['meta']['date'],'legend':J['meta']['legend'],'sections':J['meta']['sections'],'order':J['meta']['section_order']},
      'entries':[{k:e.get(k) for k in ('section','card_number','supports','author','work','original','translation_ar','urls','links','strength','argument','jurisdiction','title','source_standing','evidence_level')} for e in ents]}
html=f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>حول سن الحضانة والرعاية المشتركة بالمناصفة — النصوص والمصادر</title>
<style>{css}
.sec-blurb{{color:var(--soft);font-size:16px;margin:-4px 0 10px}}
.about{{font-size:15px;color:var(--soft);background:#F7F4EC;border-radius:8px;padding:6px 12px;margin:6px 0}} .about b{{color:var(--gold)}}
.ttl{{font-weight:700;font-size:20px;color:var(--wine)}}
.num{{font-family:var(--mono);font-size:13px;color:var(--muted);direction:ltr;text-decoration:none}}
.sel{{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}} .sel select{{font:inherit;font-size:15px;padding:4px 8px;border:1px solid #D9D2C3;border-radius:8px;background:#fff;max-width:260px}}
.acts{{display:flex;gap:8px;align-items:center;margin-top:8px;flex-wrap:wrap}} .acts button,.tools button{{font:inherit;font-size:14px;padding:4px 12px;border-radius:8px;border:1px solid #CFC6B3;background:#FBF8F1;cursor:pointer}}
.acts label{{font-size:14px;color:var(--soft)}} .tools{{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}}
.card:target{{outline:3px solid #C40000;outline-offset:3px}}
@media print{{header.top,nav.bar,footer,.acts,.tools{{display:none!important}} body.selonly article.card:not(.picked){{display:none}} body.selonly h2.ax{{display:none}} article.card{{break-inside:avoid}}}}
</style>
</head>
<body>
<header class="top">
  <h1>حول سن الحضانة والرعاية المشتركة بالمناصفة</h1><p class="sub" style="font-size:21px;color:var(--wine)">النصوص والمصادر · السابعة والتاسعة · انتهاء الطفولة بالبلوغ · الرعاية المشتركة بالمناصفة · صلة الرحم</p>
  <p class="sub">ما بين معقوفين [ ] إيضاح لمرجع الضمير، وليس من لفظ المصدر.</p>
  <div class="stats" id="stats"></div>
</header>
<nav class="bar"><div class="bar-in">
  <div class="grp" id="axF"></div>
  <div class="grp" id="supF"></div>
  <div class="sel"><select id="lvF"><option value="">كل درجات الدليل</option></select><select id="juF"><option value="">كل الدول والجهات</option></select><select id="yrF"><option value="">كل السنوات</option></select></div>
  <div class="tools"><button id="prAll">طباعة المعروض</button><button id="prSel">طباعة المحدد فقط</button><button id="clrSel">إلغاء التحديد</button></div>
  <input type="search" id="q" placeholder="ابحث في النصوص والمصادر، أو اكتب رقم البطاقة…">
  <span class="count" id="cnt"></span>
</div></nav>
<main id="list"></main>
<footer>
  <div>تعاد صناعة هذه الصفحة مع كل تحديث للموسوعة</div>
</footer>
<script id="data" type="application/json">{json.dumps(data,ensure_ascii=False)}</script>
<script>
(function(){{
const D=JSON.parse(document.getElementById('data').textContent);
const L=D.meta.legend, E=D.entries, SN=D.meta.sections, ORDER=D.meta.order;
const SUPS=['7','9','childhood_ends_at_puberty','shared_parenting','silat_al_rahim'];
const st={{sec:'',sup:null,q:'',lv:'',ju:'',yr:''}};
const picked=new Set();
const jur=e=>String(e.jurisdiction||'').split('—')[0].split('؛')[0].trim();
const yearOf=e=>{{const m=String((e.author||{{}}).date||'').match(/(1[0-9]{{3}}|20[0-9]{{2}})/);return m?+m[1]:null;}};
const decade=e=>{{const y=yearOf(e);if(!y)return '';if(y<1900)return 'قبل 1900';return (Math.floor(y/10)*10)+'–'+(Math.floor(y/10)*10+9);}};
function fillSel(id,vals){{const el=document.getElementById(id);[...new Set(vals.filter(Boolean))].sort().forEach(v=>{{const o=document.createElement('option');o.value=v;o.textContent=v;el.appendChild(o);}});el.onchange=()=>{{st[id.slice(0,2)]=el.value;draw();}};}}
const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
const n=k=>E.filter(e=>e.supports.includes(k)).length;
document.getElementById('stats').innerHTML=`<div class="stat"><b>${{E.length}}</b>نصا ومصدرا</div>`+SUPS.map(k=>`<div class="stat"><b>${{n(k)}}</b>${{L.supports[k]}}</div>`).join('');
const axF=document.getElementById('axF');
axF.innerHTML=`<button class="chip on" data-sec="">كل الأقسام</button>`+ORDER.map(k=>`<button class="chip" data-sec="${{k}}">${{esc(SN[k])}}</button>`).join('');
const supF=document.getElementById('supF');
supF.innerHTML=SUPS.map(k=>`<button class="chip" data-sup="${{k}}">${{L.supports[k]}}</button>`).join('');
axF.onclick=e=>{{const b=e.target.closest('[data-sec]');if(!b)return;st.sec=b.dataset.sec;axF.querySelectorAll('.chip').forEach(c=>c.classList.toggle('on',c===b));draw();}};
supF.onclick=e=>{{const b=e.target.closest('[data-sup]');if(!b)return;st.sup=st.sup===b.dataset.sup?null:b.dataset.sup;supF.querySelectorAll('.chip').forEach(c=>c.classList.toggle('on',c.dataset.sup===st.sup));draw();}};
fillSel('lvF',E.map(e=>e.evidence_level));fillSel('juF',E.map(jur));fillSel('yrF',E.map(decade));
document.getElementById('prAll').onclick=()=>{{document.body.classList.remove('selonly');window.print();}};
document.getElementById('prSel').onclick=()=>{{if(!picked.size){{alert('حدد بطاقة واحدة على الأقل');return;}}document.body.classList.add('selonly');window.print();setTimeout(()=>document.body.classList.remove('selonly'),500);}};
document.getElementById('clrSel').onclick=()=>{{picked.clear();draw();}};
function cite(e){{const w=e.work||{{}};return [e.author.name+(e.author.date?' ('+e.author.date+')':''),e.title,[w.title,w.section,w.volume,w.page,w.edition].filter(Boolean).join('، '),e.jurisdiction,((e.links&&e.links[0]&&e.links[0].url)||(e.urls||[])[0]||''),'بطاقة '+e.card_number+' — حول سن الحضانة والرعاية المشتركة بالمناصفة'].filter(Boolean).join(' · ');}}
document.getElementById('list').addEventListener('click',ev=>{{const b=ev.target.closest('[data-cite]');if(b){{const e=E.find(x=>x.card_number==b.dataset.cite);const t=cite(e);(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{{b.textContent='تم النسخ ✓';setTimeout(()=>b.textContent='نسخ التوثيق',1500);}}).catch(()=>{{prompt('انسخ التوثيق:',t);}});}}}});
document.getElementById('list').addEventListener('change',ev=>{{const c=ev.target.closest('[data-pick]');if(c){{const n=+c.dataset.pick;c.checked?picked.add(n):picked.delete(n);c.closest('article').classList.toggle('picked',c.checked);}}}});
document.getElementById('q').oninput=e=>{{st.q=e.target.value.trim().toLowerCase();draw();}};
const SL={{explicit_7:'نص في السابعة',explicit_9:'نص في التاسعة',explicit:'دلالة صريحة',indirect:'دلالة بالاستنباط',contextual:'شاهد'}};
function card(e){{
  const w=e.work||{{}}, ref=[w.title,w.section,w.volume,w.page,w.edition].filter(Boolean).map(esc).join('، ');
  const ltr=e.original.lang!=='ar';
  const links=(e.links&&e.links.length)?e.links.map(l=>`<a href="${{esc(l.url)}}" target="_blank" rel="noopener">${{esc(l.label)}} — ${{esc(l.url)}}</a>`).join(''):(e.urls||[]).map(u=>`<a href="${{esc(u)}}" target="_blank" rel="noopener">${{esc(u)}}</a>`).join('');
  return `<article class="card ver${{picked.has(e.card_number)?' picked':''}}" id="b${{e.card_number}}">
   <div class="head"><a class="num" href="#b${{e.card_number}}">بطاقة ${{e.card_number}}</a><span class="ttl">${{esc(e.title)}}</span></div>
   <div class="head"><span class="who">${{esc(e.author.name)}}</span>${{e.author.date?`<span class="date">${{esc(e.author.date)}}</span>`:''}}</div>
   <div class="src"><b style="color:var(--blue)">${{esc(e.jurisdiction)}}</b>${{ref?' · '+ref:''}}</div>
   <div class="tags">${{e.supports.map(s=>`<span class="tag s">${{L.supports[s]}}</span>`).join('')}}<span class="tag">${{SL[e.strength]||''}}</span>${{e.evidence_level?`<span class="tag v">${{esc(e.evidence_level)}}</span>`:''}}</div>
   <blockquote class="${{ltr&&e.original.verbatim?'ltr':''}}">${{esc(e.original.text)}}</blockquote>
   ${{e.translation_ar?`<div class="tr"><b>الترجمة:</b> ${{esc(e.translation_ar)}}</div>`:''}}
   ${{e.argument?`<p class="arg"><b>المضمون: الاستدلال به:</b> ${{esc(e.argument)}}</p>`:''}}
   ${{e.source_standing?`<div class="about"><b>عن المصدر:</b> ${{esc(e.source_standing)}}</div>`:''}}
   ${{links?`<div class="links">${{links}}</div>`:''}}
   <div class="acts"><button data-cite="${{e.card_number}}">نسخ التوثيق</button><label><input type="checkbox" data-pick="${{e.card_number}}" ${{picked.has(e.card_number)?'checked':''}}> تحديد للطباعة</label></div>
  </article>`;}}
function draw(){{
  const qn=/^\d+$/.test(st.q)?+st.q:null;
  let f=E.filter(e=>(!st.sec||e.section===st.sec)&&(!st.sup||e.supports.includes(st.sup))&&(!st.lv||e.evidence_level===st.lv)&&(!st.ju||jur(e)===st.ju)&&(!st.yr||decade(e)===st.yr)&&(!st.q||(qn!==null?e.card_number===qn:JSON.stringify(e).toLowerCase().includes(st.q))));
  document.getElementById('cnt').innerHTML=`عرض <b>${{f.length}}</b> من <b>${{E.length}}</b>`;
  const out=[];
  ORDER.forEach(k=>{{const g=f.filter(e=>e.section===k).sort((x,y)=>x.card_number-y.card_number);
    if(g.length) out.push(`<h2 class="ax"><span>${{g.length}} نصا</span>${{esc(SN[k])}}</h2>`+g.map(card).join(''));}});
  document.getElementById('list').innerHTML=out.join('')||'<div class="empty">لا نتائج بهذه المرشحات.</div>';
}}
draw();
if(location.hash){{const el=document.querySelector(location.hash);if(el)el.scrollIntoView();}}
window.addEventListener('hashchange',()=>{{const el=document.querySelector(location.hash);if(el)el.scrollIntoView();}});
}})();
</script>
</body>
</html>'''
open('/home/claude/work/build/nuqul_7_9_favorable.html','w',encoding='utf8').write(html)
print('favorable entries',len(ents), 'bytes',len(html.encode('utf8')))
