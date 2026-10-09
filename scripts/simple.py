# -*- coding: utf-8 -*-
"""Simplified Facebook cards (1080x1350): Arabic text only, large type, no links/QR/English/footnotes."""
import json, re, sys, asyncio, html as H
sys.path.insert(0,'/home/claude/work')
from assemble import SEC, mn_plain
from playwright.async_api import async_playwright
IDS=json.load(open('/home/claude/work/build/tools/short_ids.json',encoding='utf8'))
J=json.load(open('/home/claude/work/build/nuqul_7_9.json',encoding='utf8'))
SN=J['meta']['sections']
src=open('/home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.html',encoding='utf8').read()
FONTS=''.join(re.findall(r'@font-face\{[^}]*\}',src))
LOGO=re.search(r'<div class="lgw">(<svg.*?</svg>)</div>',src,re.S).group(1)
MN='<span class="mn">بالمناصفة</span>'
def mn(s): return re.sub(r'(?<![ء-ي])((?:و|ف|ب|ل|ك)?الرعاية المشتركة)(?!\s*(?:<span class="mn">)?بالمناصفة)',r'\1 '+MN,s).replace('الرعاية المشتركة بالمناصفة','الرعاية المشتركة '+MN) if 'class="mn"' not in s else s
def arabic_text(e):
    o=e['original']; t=o['text']
    if re.search('[\u0600-\u06FF]',t[:40]): return t.strip('«»').replace('مضمونه: ','').replace('مضمونه:','')
    return (e.get('translation_ar') or '').strip('«»')
def quoted(e):
    return not e['original']['text'].startswith('مضمونه')
def year(e):
    m=re.search(r'(1[0-9]{3}|20[0-9]{2})',e['author'].get('date','') or ''); return m.group(1) if m else (e['author'].get('date') or '')
def source(e):
    a=e['author']['name']; j=e.get('jurisdiction','')
    if re.search('[؀-ۿ]',a): s=a+(' · '+a_date if (a_date:=e['author'].get('date','')) else '')
    else: s=j+(' · '+year(e) if year(e) else '')
    return s
CSS=FONTS+'''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;font-family:'NotoArE','NotoArL',sans-serif;direction:rtl}
.c{width:540px;height:675px;position:relative;overflow:hidden;background:linear-gradient(180deg,var(--t1) 0%,#fff 22%,#fff 100%);display:flex;flex-direction:column;padding:14px 18px 12px;border-top:9px solid var(--a)}
.hd{display:flex;align-items:center;gap:10px}
.hd svg{width:58px;height:58px;flex:0 0 58px}
.hd .nm{flex:1}
.hd .sec{font-family:'CairoE',sans-serif;font-weight:700;color:var(--a);font-size:15px;line-height:1.3}
.hd .ttl{font-family:'CairoE',sans-serif;color:#4A5A61;font-size:11.5px;line-height:1.3}
.hd .no{font-family:'CairoE',sans-serif;font-weight:700;background:var(--a);color:#fff;border-radius:14px;padding:2px 12px;font-size:15px}
.rt{font-family:'CairoE',sans-serif;font-weight:700;color:var(--ad);font-size:calc(var(--k)*1.08);line-height:1.38;margin:10px 0 8px}
.tx{flex:1;display:flex;align-items:center}
.tx .q{width:100%;background:#fff;border:2px solid var(--a);border-radius:16px;padding:12px 16px;font-size:var(--k);line-height:1.75;color:#182228;box-shadow:0 4px 14px rgba(0,0,0,.06)}
.tx .q.ar{font-family:'AmiriE','NotoArE',serif;font-size:calc(var(--k)*1.12);line-height:1.8}
.sr{margin-top:8px;font-family:'CairoE',sans-serif;font-weight:700;color:var(--a);font-size:calc(var(--k)*.66);line-height:1.45}
.id{margin-top:2px;font-size:calc(var(--k)*.62);line-height:1.45;color:#4A5A61}
.ag{margin-top:8px;background:var(--t1);border-right:6px solid var(--a);border-radius:10px;padding:7px 12px;font-size:calc(var(--k)*.74);line-height:1.6;color:#20303A}
.ag b{font-family:'CairoE',sans-serif;color:var(--ad)}
.ft{margin-top:8px;display:flex;justify-content:space-between;align-items:center;font-family:'CairoE',sans-serif;font-size:10.5px;color:#7A868C;border-top:1px solid #E3DDD0;padding-top:5px}
.mn{font-family:'AmiriE','CairoE',serif;font-weight:700;color:#C40000;font-size:1.08em}
.B .ag{display:none}.B .tx .q{font-size:calc(var(--k)*1.1)}
'''
def card(e,style):
    s=SEC[e['section']]; n=e['card_number']
    ar=e['original']['lang']=='ar'
    return f'''<div class="c {style}" data-n="{n}" style="--a:{s['acc']};--ad:{s['accd']};--t1:{s['g'][0]};--k:24px">
<div class="hd">{LOGO}<div class="nm"><div class="sec">{mn(H.escape(SN[e['section']]))}</div><div class="ttl">حول سن الحضانة والرعاية المشتركة {MN}</div></div><div class="no">بطاقة {n}</div></div>
<div class="rt">{mn(H.escape(e['title']))}</div>
<div class="tx"><div class="q{' ar' if ar else ''}">{('«' if quoted(e) else '')+mn(H.escape(arabic_text(e)))+('»' if quoted(e) else '')}</div></div>
<div class="sr">{H.escape(source(e))}</div>{('<div class="id">'+H.escape(IDS.get(str(n),''))+'</div>') if IDS.get(str(n)) else ''}
<div class="ag"><b>الدلالة: </b>{mn(H.escape(e['argument']))}</div>
<div class="ft"><span>النص الكامل ومصدره ورابطه في البطاقة {n} من الطبعة الكاملة</span><span>صلة الأرحام</span></div></div>'''
FIT='''()=>{for(const c of document.querySelectorAll('.c')){let lo=13,hi=30;for(let i=0;i<14;i++){const m=(lo+hi)/2;c.style.setProperty('--k',m+'px');const over=c.scrollHeight>c.clientHeight+1||[...c.children].some(x=>x.scrollWidth>x.clientWidth+2);if(over)hi=m;else lo=m;}c.style.setProperty('--k',lo+'px');c.dataset.k=lo.toFixed(1);}}'''
async def render(ns,style,outdir):
    E={e['card_number']:e for e in J['entries'] if e.get('card_number')}
    body=''.join(card(E[n],style) for n in ns)
    html=f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div id="r" style="display:flex;flex-direction:column;gap:20px;padding:0">{body}</div></body></html>'
    open(f'{outdir}/simple_{style}.html','w',encoding='utf8').write(html)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':560,'height':800},device_scale_factor=2)
        await pg.goto(f'file://{outdir}/simple_{style}.html'); await pg.wait_for_timeout(1200)
        await pg.evaluate(FIT)
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
