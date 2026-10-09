import asyncio,json,sys,os,shutil,zipfile
from playwright.async_api import async_playwright
from PIL import Image
H='/home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.html'
ONLY=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1] else None
CW,CH,M=1080,1350,44
def canvas(): return Image.new('RGB',(CW,CH),'white')
def fit_one(img):
    sc=min((CW-2*M)/img.width,(CH-2*M)/img.height,1.0)
    im=img.resize((round(img.width*sc),round(img.height*sc)),Image.LANCZOS)
    c=canvas(); c.paste(im,((CW-im.width)//2,(CH-im.height)//2)); return c
def pack(blocks):
    mw=max(b.width for b in blocks); sc=min(1.0,(CW-2*M)/mw)
    bl=[b.resize((round(b.width*sc),round(b.height*sc)),Image.LANCZOS) for b in blocks]
    pages=[];cur=[];h=0
    for b in bl:
        if cur and h+b.height>CH-2*M: pages.append(cur);cur=[];h=0
        cur.append(b);h+=b.height
    if cur: pages.append(cur)
    out=[]
    for pg in pages:
        c=canvas(); tot=sum(b.height for b in pg); y=max(M,(CH-tot)//2)
        for b in pg: c.paste(b,((CW-b.width)//2,y)); y+=b.height
        out.append(c)
    return out
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':600,'height':800},device_scale_factor=2)
        await pg.goto('file://'+H); await pg.wait_for_timeout(1500)
        await pg.add_style_tag(content=open('fb.css').read())
        if ONLY:
            await pg.evaluate('(ids)=>document.querySelectorAll("section.page").forEach(s=>{if(!ids.includes(s.id)) s.remove()})',ONLY)
        res=await pg.evaluate(open('fb.js').read())
        json.dump(res,open('fb_res.json','w'),ensure_ascii=False)
        # cover tweak
        await pg.evaluate('''()=>{const c=document.getElementById('cover'); if(!c) return; const g=c.querySelector('div[style*="flex-direction:column;gap:9px"]'); if(g){g.style.display='grid';g.style.gridTemplateColumns='1fr 1fr';g.style.gap='8px';} c.style.width='700px'; const d=c.firstElementChild; if(d) d.style.width='700px';}''')
        shutil.rmtree('fbimg',ignore_errors=True); os.makedirs('fbimg')
        seq=[]
        await pg.evaluate('()=>{window.__fb=[...document.querySelectorAll(".fbp")];document.getElementById("fbroot").replaceChildren();document.querySelectorAll("body>section.page").forEach(s=>s.style.display="none")}')
        cards={}
        for k,e in enumerate(await pg.query_selector_all('.fbp')): pass
        ids=await pg.evaluate('()=>window.__fb.map(x=>x.dataset.id)')
        for k,i in enumerate(ids): cards.setdefault(i,[]).append(k)
        n=0
        for id_,part,_ in res:
            if part=='1' or part=='0' and id_ in cards and len(cards[id_])>=1 and part!='W':
                if part in('0','1'):
                    for k,ix in enumerate(cards[id_]):
                        await pg.evaluate('(ix)=>{const r=document.getElementById("fbroot");r.replaceChildren(window.__fb[ix]);window.scrollTo(0,0)}',ix); e=await pg.query_selector('.fbp')
                        f=f'fbimg/{n:03d}_{id_}_{k}.png'; await e.screenshot(path=f); im=Image.open(f); print('SIZE',f,im.size) if im.width!=CW or abs(im.height-CH)>3 else None; im.crop((0,0,CW,CH)).save(f) if im.size!=(CW,CH) else None; seq.append((id_,f)); n+=1
                continue
            if part!='W': continue
            await pg.evaluate('(i)=>{document.getElementById("fbroot").replaceChildren();document.querySelectorAll("body>section.page").forEach(s=>s.style.display=s.id==i?"block":"none");window.scrollTo(0,0)}',id_)
            el=await pg.query_selector(f'section[id="{id_}"]')
            if id_ in('toc','stats'):
                kids=await el.query_selector_all(':scope > *')
                blocks=[]
                for kd in kids:
                    tag=await kd.evaluate('e=>e.tagName')
                    sub=await kd.query_selector_all(':scope > a')
                    cls=await kd.evaluate('e=>e.className||""')
                    if 'foot2' in cls: continue
                    for x in (sub if sub else [kd]):
                        await x.screenshot(path='/tmp/claude-0/blk.png'); blocks.append(Image.open('/tmp/claude-0/blk.png').copy())
                imgs=pack(blocks)
            else:
                await el.screenshot(path='/tmp/claude-0/blk.png'); imgs=[fit_one(Image.open('/tmp/claude-0/blk.png').convert('RGB'))]
            for k,im in enumerate(imgs):
                f=f'fbimg/{n:03d}_{id_}_{k}.png'; im.save(f); seq.append((id_,f)); n+=1
        json.dump(seq,open('fb_seq.json','w'),ensure_ascii=False)
        await b.close()
asyncio.run(main())
