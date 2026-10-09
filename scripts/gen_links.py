# -*- coding: utf-8 -*-
import re, html as H, json, sys
sys.path.insert(0,'/home/claude/work')
from assemble import SEC, ORDER, mn_plain
s=open('/home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.html',encoding='utf8').read()
def txt(x): return H.unescape(re.sub(r'<[^>]+>',' ',x)).replace('  ',' ').strip()
md=['# روابط النصوص والمصادر','', 'حول سن الحضانة والرعاية المشتركة بالمناصفة — كل رابط في الإصدار، وما دل عليه، وما استفيد منه، ومنزلة المصدر.','']
hh=['<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>روابط النصوص والمصادر</title><style>body{font-family:Calibri,Carlito,sans-serif;font-size:18px;line-height:2;margin:24px auto;max-width:980px;padding:0 18px;color:#182228;background:#fff}h1{color:#C40000}h2{color:#1F5FA8;border-bottom:2px solid #CBD3D6;margin-top:36px}.e{border-bottom:1px solid #E3E7E9;padding:10px 0}.t{font-weight:700}.l a{color:#145C94;word-break:break-all;direction:ltr;unicode-bidi:isolate}.k{color:#637681;font-size:16px}</style></head><body><h1>روابط النصوص والمصادر</h1><p>حول سن الحضانة والرعاية المشتركة بالمناصفة — كل رابط في الإصدار، وما دل عليه، وما استفيد منه، ومنزلة المصدر.</p>']
n=0; nlinks=0; ncards=0; cur=None
for m in re.finditer(r'<section class="page ([^"]*)" id="([^"]+)"[^>]*>(.*?)</section>',s,re.S):
    cls,id_,body=m.groups()
    if id_.startswith('sec-'):
        cur=id_[4:]; name=mn_plain(SEC[cur]['name'])
        md+=[f'## {name}','']; hh.append(f'<h2>{name}</h2>'); continue
    if not re.match(r'A\d-\d{3}',id_): continue
    n+=1
    urls=re.findall(r'<a class="qi" href="([^"]+)"',body)
    if not urls: continue
    ncards+=1; nlinks+=len(urls)
    rt=txt(re.search(r'<div class="rt">(.*?)</div>',body,re.S).group(1))
    ot=txt(re.search(r'<div class="ot[^"]*"[^>]*>(.*?)</div></div>',body,re.S).group(1))
    arg=txt(re.search(r'<div class="argt">(.*?)</div>',body,re.S).group(1))
    ab=re.search(r'<div class="about st">(.*?)</span></div>',body,re.S)
    ab=txt(ab.group(1)).replace('عن المصدر:','').strip() if ab else ''
    labels=re.findall(r'<div class="ql">(.*?)</div>',body)
    md.append(f'### بطاقة {n} — {rt}')
    for u,l in zip(urls,labels): md.append(f'- {l}: [{H.unescape(u)}]({H.unescape(u)})')
    md.append(f'- **ما دل عليه:** {ot}'); md.append(f'- **ما استفيد منه:** {arg}')
    if ab: md.append(f'- **عن المصدر:** {ab}')
    md.append('')
    links=''.join(f'<div class="l">{l}: <a href="{u}" target="_blank" rel="noopener">{H.unescape(u)}</a></div>' for u,l in zip(urls,labels))
    hh.append(f'<div class="e"><div class="t">بطاقة {n} — {rt}</div>{links}<div class="k"><b>ما دل عليه:</b> {ot}</div><div class="k"><b>ما استفيد منه:</b> {arg}</div>'+(f'<div class="k"><b>عن المصدر:</b> {ab}</div>' if ab else '')+'</div>')
hh.append('</body></html>')
open('/home/claude/work/build/روابط_النصوص_والمصادر.md','w',encoding='utf8').write('\n'.join(md))
open('/home/claude/work/build/روابط_النصوص_والمصادر.html','w',encoding='utf8').write(''.join(hh))
print('cards with links',ncards,'links',nlinks,'of',n)
