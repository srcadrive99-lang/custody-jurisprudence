# -*- coding: utf-8 -*-
"""Simplified Facebook cards (1080x1350): Arabic text only, large type, no links/QR/English/footnotes."""
import json, re, sys, asyncio, html as H, io, segno
sys.path.insert(0,'/home/claude/work')
from assemble import SEC, mn_plain
from playwright.async_api import async_playwright
import os
REVIEW=os.environ.get('REVIEW')=='1'
J=json.load(open('/home/claude/work/build/review.json' if REVIEW else '/home/claude/work/build/nuqul_7_9.json',encoding='utf8'))
IDS=J['meta']['short_ids'] if REVIEW else json.load(open('/home/claude/work/build/tools/short_ids.json',encoding='utf8'))
SN=J['meta']['sections']
src=open('/home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.html',encoding='utf8').read()
FONTS=''.join(re.findall(r'@font-face\{[^}]*\}',src))
LOGO=re.search(r'<div class="lgw">(<svg.*?</svg>)</div>',src,re.S).group(1)
import base64
WM_SVG=base64.b64encode(('<svg xmlns="http://www.w3.org/2000/svg" width="260" height="120"><text x="130" y="68" text-anchor="middle" transform="rotate(-24 130 60)" font-family="CairoE, Cairo, sans-serif" font-weight="700" font-size="19" fill="#1F2A30" fill-opacity="0.075">'+'نداء من أجل أطفال مصر'+'</text></svg>').encode()).decode()
MN='<span class="mn">بالمناصفة</span>'
PAGE='نداء من أجل أطفال مصر'; PURL='https://www.facebook.com/profile.php?id=61595080592206'
def _qr(u):
    b=io.BytesIO(); segno.make(u,error='m').save(b,kind='svg',xmldecl=False,svgns=True,dark='#1F2A30',light=None,border=1,scale=1)
    t=b.getvalue().decode(); m=re.search(r'width="(\d+)" height="(\d+)"',t); return t.replace(m.group(0),f'viewBox="0 0 {m.group(1)} {m.group(2)}"',1)
PQR=_qr(PURL)
WM=''.join(f'<span>{PAGE}</span>' for _ in range(24))
SEAL=None
def mn(s): return re.sub(r'(?<![ء-ي])((?:و|ف|ب|ل|ك)?الرعاية المشتركة)(?!\s*(?:<span class="mn">)?بالمناصفة)',r'\1 '+MN,s).replace('الرعاية المشتركة بالمناصفة','الرعاية المشتركة '+MN) if 'class="mn"' not in s else s
FIXTXT={'A5-099':'يحتاج الأطفال بعد الانفصال أن يعلموا أن كلا الوالدين يحبهم، وتقرر الجمعية أن أهمية صلة الطفل بكلا والديه ورعايتهما له معا «لا يمكن المبالغة فيها».','A5-052':'مادة تدريبية رسمية لقضاة الأسرة تعرض تقرير وارشاك 2014 ودراسة فابريشيوس 2017، وتنقل أن التحذير من مبيت الطفل عند أبيه في السنوات الثلاث الأولى لا تسنده الأدلة.','A5-032':'تمتع الوالد والطفل بصحبة أحدهما الآخر عنصر أساسي للحياة الأسرية «حتى لو انهارت العلاقة بين الوالدين».'}
def unq(t):
    t=t.strip()
    m=re.fullmatch(r'«([^«»]*)»\s*([.،:؛]?)',t)
    if m: return m.group(1).strip()
    a,b=t.count('«'),t.count('»')
    if a>b: t=t+'»'
    elif b>a: t='«'+t
    return t
def arabic_text(e):
    return FIXTXT.get(e['id']) or unq(_arabic_text(e))
def _arabic_text(e):
    o=e['original']; t=o['text']
    if re.search('[\u0600-\u06FF]',t[:40]): return t.replace('مضمونه: ','').replace('مضمونه:','')
    return (e.get('translation_ar') or '')
def quoted(e):
    return not e['original']['text'].startswith('مضمونه')
def year(e):
    m=re.search(r'(1[0-9]{3}|20[0-9]{2})',e['author'].get('date','') or ''); return m.group(1) if m else (e['author'].get('date') or '')
def source(e):
    a=e['author']['name']; j=e.get('jurisdiction','')
    if re.search('[؀-ۿ]',a): s=a+(' · '+a_date if (a_date:=e['author'].get('date','')) else '')
    else: s=j+(' · '+year(e) if year(e) else '')
    return s
IDN={x['id']:x['card_number'] for x in J['entries'] if x.get('card_number')}
import flags
NCI={x['id']:x.get('icon','') for x in json.load(open('/home/claude/work/new_cards.json',encoding='utf8'))}
NCW={x['id']:x.get('src',{}) for x in json.load(open('/home/claude/work/new_cards.json',encoding='utf8'))}
def fullsrc(e):
    a=e['author']; w=e.get('work') or {}
    parts=[]
    for k in ('title','volume','section','page'):
        v=(w.get(k) or '').strip()
        if v and v not in parts: parts.append(v)
    if not parts:
        sw=re.sub(r'\{N:(A\d-\d{3})\}',lambda m:str(IDN.get(m.group(1),'')),(NCW.get(e['id'],{}).get('sw') or '').strip())
        if sw: parts.append(sw)
    return parts
def locjoin(L):
    out=[];buf=[]
    for x in L:
        if re.search('[\u0600-\u06FF]',x):
            if buf: out.append(bd(' · '.join(buf))); buf=[]
            out.append(bd(x))
        else: buf.append(x)
    if buf: out.append(bd(' · '.join(buf)))
    return ' · '.join(out)
def bd(x):
    x=H.escape(x)
    return f'<bdi dir="ltr">{x}</bdi>' if not re.search('[\u0600-\u06FF]',x) else f'<bdi>{x}</bdi>'
def mainlink(e):
    L=e.get('links') or [{'url':u,'label':'النص في مصدره','site':'','domain':re.sub(r'^https?://([^/]+).*',r'\1',u)} for u in e.get('urls',[])]
    return L[0] if L else None
import os
CSS=FONTS+'''
*{box-sizing:border-box;margin:0;padding:0}
body{--wmo:__WMO__;--slo:__SLO__;background:#fff;font-family:'NotoArE','NotoArL',sans-serif;direction:rtl}
.c{width:540px;height:675px;position:relative;overflow:hidden;background:linear-gradient(180deg,var(--t1) 0%,#fff 22%,#fff 100%);display:flex;flex-direction:column;padding:14px 18px 12px;border-top:9px solid var(--a)}
.hd{display:flex;align-items:center;gap:10px}
.hd svg{width:58px;height:58px;flex:0 0 58px}
.hd .nm{flex:1}
.hd .sec{font-family:'CairoE',sans-serif;font-weight:700;color:var(--a);font-size:15px;line-height:1.3}
.hd .ttl{font-family:'CairoE',sans-serif;color:#4A5A61;font-size:11.5px;line-height:1.3}
.hd .no{font-family:'CairoE',sans-serif;font-weight:700;background:var(--a);color:#fff;border-radius:14px;padding:2px 12px;font-size:15px}
.rt{font-family:'CairoE',sans-serif;font-weight:700;color:var(--ad);font-size:calc(var(--k)*1.08);line-height:1.38;margin:10px 0 8px}
.tx{flex:1;display:flex;align-items:center}
.tx .q{width:100%;background-color:#fff;position:relative;overflow:hidden;border:2px solid var(--a);border-radius:16px;padding:12px 16px;font-size:var(--k);line-height:1.75;color:#182228;box-shadow:0 4px 14px rgba(0,0,0,.06)}
.tx .q.ar{font-family:'AmiriE','NotoArE',serif;font-size:calc(var(--k)*1.12);line-height:1.8}
.sr{margin-top:8px;font-family:'CairoE',sans-serif;font-weight:700;color:var(--a);font-size:calc(var(--k)*.66);line-height:1.45}
.sw{margin-top:1px;font-size:calc(var(--k)*.56);line-height:1.45;color:#2E3B42}
a.lk{text-decoration:none;color:inherit}
.lk{display:flex;align-items:center;gap:6px;min-width:0}.lk svg{width:40px;height:40px;flex:0 0 40px}.lk .lt{min-width:0;font-size:10px;line-height:1.35;color:#4A5A61}.lk .lt b{display:block;color:var(--ad);font-size:11.5px}.lk .lt small{display:block;direction:ltr;text-align:right;font-size:8.6px;color:#1F5FA8;word-break:break-all;max-width:250px}
.id{margin-top:2px;font-size:calc(var(--k)*.62);line-height:1.45;color:#4A5A61}
.ag{margin-top:8px;background:var(--t1);border-right:6px solid var(--a);border-radius:10px;padding:7px 12px;font-size:calc(var(--k)*.74);line-height:1.6;color:#20303A}
.ag b{font-family:'CairoE',sans-serif;color:var(--ad)}
.slog{flex:0 0 auto;margin-top:5px;padding-top:4px;border-top:0.5px solid #D5DADC;text-align:center;white-space:nowrap;overflow:hidden;font-family:'NotoArL','NotoArE',sans-serif;font-weight:300;font-size:9.6px;line-height:1.6;color:#8A949A}
.slog i{display:inline-block;width:3.5px;height:3.5px;border-radius:50%;margin:0 6px;vertical-align:middle;background:radial-gradient(circle at 35% 30%,#9aa3a8 0%,#2b2f32 45%,#0b0c0d 100%)}
.ft{flex:0 0 auto;margin-top:8px;display:flex;justify-content:space-between;align-items:center;gap:8px;font-family:'CairoE',sans-serif;font-size:10.5px;color:#7A868C;border-top:1px solid #E3DDD0;padding-top:5px}
.pg{display:flex;align-items:center;gap:6px;color:var(--ad);font-weight:700;font-size:12px;white-space:nowrap}.pg svg{width:34px;height:34px}.pg small{display:block;font-weight:400;font-size:8.5px;color:#4A5A61;direction:ltr}
.tx .q .sl{position:absolute;left:10px;bottom:8px;width:70px;height:70px;opacity:var(--slo,.13);pointer-events:none}.tx .q .sl svg{width:70px!important;height:70px!important}
.tx .q .wm{position:absolute;inset:-40px;display:flex;flex-wrap:wrap;align-content:space-around;justify-content:space-around;transform:rotate(-22deg);pointer-events:none;z-index:0}.tx .q .wm span{font-family:'CairoE',sans-serif;font-weight:700;font-size:15px;color:rgba(31,42,48,var(--wmo,.075));white-space:nowrap;padding:14px 18px}
.tx .q .qt{position:relative;z-index:1}
.flg{display:inline-flex;align-items:center;gap:4px;margin-left:6px;vertical-align:middle}.flg svg{width:24px;height:16px;display:block;filter:drop-shadow(0 1px 1px rgba(0,0,0,.18))}.flg .fn{font-family:'CairoE',sans-serif;font-weight:700;font-size:.95em;color:inherit}.flg .fn:after{content:' ·'}
.hq{padding:0 0 .35em;margin:0 0 .35em;border-bottom:1px dashed #E2C3D4}.hq:last-child{border-bottom:0;margin-bottom:0;padding-bottom:0}.hs{display:block;font-family:'CairoE',sans-serif;font-weight:700;font-size:.6em;line-height:1.4;color:var(--ad)}
.mn{font-family:'AmiriE','CairoE',serif;font-weight:700;color:#C40000;font-size:1.08em}
.B .ag{display:none}.B .tx .q{font-size:calc(var(--k)*1.1)}
'''
CSS=CSS.replace('__WMO__',os.environ.get('WMO','.125')).replace('__SLO__',os.environ.get('SLO','.21'))
def linkblk(e,n):
    l=mainlink(e)
    if not l: return f'<span>النص الكامل في البطاقة {n} من الطبعة الكاملة</span>'
    u=l['url']; short=re.sub(r'^https?://(www\.)?','',u)
    if len(short)>70: short=short[:67]+'…'
    return f'<a class="lk" href="{H.escape(u)}">{_qr(u)}<span class="lt"><b>رابط المصدر: {H.escape(l.get("label") or "الرابط")}</b>{H.escape(l.get("site") or "")}<small>{H.escape(short)}</small></span></a>'
def flag_key(e):
    k=NCI.get(e['id']) if e['id'] in NCI else None
    if not k: k=flags.key_for(e.get('jurisdiction',''),e.get('category',''))
    return k
COUNTRY_SKIP=flags.FIQH_KEYS|{'book','egbook'}
def flag_span(k,txt=''):
    if not k or k not in flags.F: return ''
    nm=flags.NAMES.get(k,'')
    lab='' if (k in COUNTRY_SKIP or not nm or nm in txt) else f'<b class="fn">{nm}</b>'
    return f'<span class="flg">{flags.icon(k)}{lab}</span>'
IDE={x['card_number']:x for x in J['entries'] if x.get('card_number')}
def hujaj_html(e):
    parts=[x.strip() for x in arabic_text(e).split('◆') if x.strip()]
    out=[]
    for x in parts:
        m=re.match(r'^([«﴿].*[»﴾])\s*\((.*)\)\s*$',x,re.S)
        q,sname=(m.group(1),m.group(2)) if m else (x,'')
        mm=re.search(r'بطاقة (\d+)',sname); se=IDE.get(int(mm.group(1))) if mm else None
        fs=flag_span(flag_key(se),sname) if se else ''
        out.append(f'<div class="hq">{mn(H.escape(q))}<span class="hs">{fs}{H.escape(sname)}</span></div>')
    return ''.join(out)
def card(e,style):
    s=SEC[e['section']]; n=e['card_number']
    ar=e['original']['lang']=='ar'
    return f'''<div class="c {style}" data-n="{n}" style="--a:{s['acc']};--ad:{s['accd']};--t1:{s['g'][0]};--k:24px">
<div class="hd">{LOGO}<div class="nm"><div class="sec">{('للمراجعة · ' if REVIEW else '')+mn(H.escape(SN[e['section']]))}</div><div class="ttl">{PAGE} · حول سن الحضانة والرعاية المشتركة {MN}</div></div><div class="no">{'للمراجعة' if REVIEW else 'بطاقة'} {n}</div></div>
<div class="rt">{mn(H.escape(e['title']))}</div>
<div class="tx"><div class="q{' ar' if ar else ''}"><div class="wm">{WM}</div><div class="sl">{LOGO}</div><div class="qt">{hujaj_html(e) if e['section']=='hujaj' else (lambda _t,_w:('«' if _w else '')+mn(H.escape(_t))+('»' if _w else ''))(arabic_text(e),quoted(e) and '«' not in arabic_text(e) and '﴿' not in arabic_text(e))}</div></div></div>
<div class="sr">{"" if e["section"]=="hujaj" else flag_span(flag_key(e),source(e))}{H.escape(source(e))}</div>{('<div class="sw"><b>الموضع:</b> '+locjoin(fullsrc(e))+'</div>') if fullsrc(e) else ''}{('<div class="id">'+H.escape(IDS.get(str(n),''))+'</div>') if IDS.get(str(n)) else ''}
<div class="ag"><b>الدلالة: </b>{mn(H.escape(e['argument']))}</div>{('<div class="ag" style="background:#FFF4E5;border-color:#E07B00"><b>سبب المراجعة: </b>'+H.escape(e.get('review_reason',''))+' · رقمها في الإصدار 1.26.0: '+str(e.get('old_card_number',''))+'</div>') if REVIEW else ''}
<div class="ft">{linkblk(e,n)}<span class="pg">{PQR}<span>{PAGE}<small>facebook.com/profile.php?id=61595080592206</small></span></span></div><div class="slog">لا للمظاهرات والثورات<i></i>لا لسيداو، ولا لتمييز المرأة على الرجل في الإجراءات والقرارات والقوانين<i></i>نعم لصلة الأرحام</div></div>'''
FIT='''()=>{for(const c of document.querySelectorAll('.c')){let lo=13,hi=30;for(let i=0;i<14;i++){const m=(lo+hi)/2;c.style.setProperty('--k',m+'px');const over=c.scrollHeight>c.clientHeight+1||[...c.children].some(x=>!x.classList.contains('slog')&&x.scrollWidth>x.clientWidth+2);if(over)hi=m;else lo=m;}c.style.setProperty('--k',lo+'px');c.dataset.k=lo.toFixed(1);}}'''
async def render(ns,style,outdir):
    E={e['card_number']:e for e in J['entries'] if e.get('card_number')}
    body=''.join(card(E[n],style) for n in ns)
    html=f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div id="r" style="display:flex;flex-direction:column;gap:20px;padding:0">{body}</div></body></html>'
    open(f'{outdir}/simple_{style}.html','w',encoding='utf8').write(html)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':560,'height':800},device_scale_factor=2)
        await pg.goto(f'file://{outdir}/simple_{style}.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate(FIT)
        _bad=await pg.evaluate("()=>[...document.querySelectorAll('.c')].filter(c=>{const s=c.querySelector('.slog');if(!s)return true;const r=s.getBoundingClientRect(),q=c.getBoundingClientRect();return r.height<8||r.bottom>q.bottom+1}).length")
        assert _bad==0, f'المادة 34: تذييل البطاقة غائب أو مقصوص في {_bad} بطاقة'
        _nos=await pg.evaluate("()=>[...document.querySelectorAll('.c')].filter(c=>!c.querySelector('.sr')||!(c.querySelector('.lk')||c.textContent.includes('النص الكامل في البطاقة'))).length")
        assert _nos==0, f'المادة 35: المصدر أو رابطه غائب في {_nos} بطاقة'
        for el in await pg.query_selector_all('.c'):
            n=await el.get_attribute('data-n'); k=await el.get_attribute('data-k')
            await el.screenshot(path=f'{outdir}/{style}_{int(n):03d}.png'); print(style,n,k)
        await b.close()
async def render_all(style,outdir,pdf):
    import os,collections
    E=sorted([e for e in J['entries'] if e.get('card_number')],key=lambda e:e['card_number'])
    body=''.join(card(e,style) for e in E)
    css_print='@page{size:540px 675px;margin:0} @media print{#r{gap:0!important} .c{break-after:page}}'
    html=f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>البطاقات المختصرة</title><style>{CSS}{css_print}</style></head><body><div id="r" style="display:flex;flex-direction:column;gap:20px">{body}</div></body></html>'
    hp=f'{outdir}/all_{style}.html'; open(hp,'w',encoding='utf8').write(html)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':560,'height':800},device_scale_factor=2)
        await pg.goto('file://'+hp); await pg.wait_for_timeout(2000)
        await pg.evaluate(FIT)
        _bad=await pg.evaluate("()=>[...document.querySelectorAll('.c')].filter(c=>{const s=c.querySelector('.slog');if(!s)return true;const r=s.getBoundingClientRect(),q=c.getBoundingClientRect();return r.height<8||r.bottom>q.bottom+1}).length")
        assert _bad==0, f'المادة 34: تذييل البطاقة غائب أو مقصوص في {_bad} بطاقة'
        _nos=await pg.evaluate("()=>[...document.querySelectorAll('.c')].filter(c=>!c.querySelector('.sr')||!(c.querySelector('.lk')||c.textContent.includes('النص الكامل في البطاقة'))).length")
        assert _nos==0, f'المادة 35: المصدر أو رابطه غائب في {_nos} بطاقة'
        ks=await pg.evaluate('()=>[...document.querySelectorAll(".c")].map(c=>[+c.dataset.n,+c.dataset.k])')
        json.dump(ks,open(f'{outdir}/fit_{style}.json','w'))
        os.makedirs(f'{outdir}/img_{style}',exist_ok=True)
        for el in await pg.query_selector_all('.c'):
            n=int(await el.get_attribute('data-n'))
            await el.screenshot(path=f'{outdir}/img_{style}/{n:03d}.png')
        await pg.emulate_media(media='print')
        await pg.pdf(path=pdf,width='540px',height='675px',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
        await b.close()
if __name__=='__main__' and sys.argv[1]=='ALL':
    asyncio.run(render_all(sys.argv[2],sys.argv[3],sys.argv[4])); sys.exit()
if __name__=='__main__':
    ns=[int(x) for x in sys.argv[1].split(',')]; style=sys.argv[2]; out=sys.argv[3]
    asyncio.run(render(ns,style,out))
