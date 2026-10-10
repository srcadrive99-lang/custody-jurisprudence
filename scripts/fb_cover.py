import asyncio
from playwright.async_api import async_playwright
from PIL import Image
CW,CH,M=1080,1350,44
def fit_one(img):
    sc=min((CW-2*M)/img.width,(CH-2*M)/img.height)
    im=img.resize((round(img.width*sc),round(img.height*sc)),Image.LANCZOS)
    c=Image.new('RGB',(CW,CH),'white'); c.paste(im,((CW-im.width)//2,(CH-im.height)//2)); return c
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':600,'height':1400},device_scale_factor=3)
        await pg.goto('file:///home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate('()=>document.querySelectorAll("body>section.page").forEach(s=>s.style.display=s.id=="cover"?"block":"none")')
        el=await pg.query_selector('section[id="cover"]'); await el.screenshot(path='/tmp/claude-0/blk.png')
        fit_one(Image.open('/tmp/claude-0/blk.png').convert('RGB')).save('fbimg/000_cover_0.png')
        await b.close()
asyncio.run(main())
