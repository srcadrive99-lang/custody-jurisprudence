import sys,asyncio
from playwright.async_api import async_playwright
html,mode,out=sys.argv[1],sys.argv[2],sys.argv[3]
W=560 if mode=='m' else 1032
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':W,'height':1200})
        await pg.goto('file://'+html); await pg.wait_for_timeout(1500)
        await pg.emulate_media(media='print')
        hs=await pg.eval_on_selector_all('section.page','e=>e.map(x=>[x.id,Math.ceil(Math.max(x.getBoundingClientRect().height,x.scrollHeight))+(x.id=="cover"?24:2)])')
        css=['html,body{margin:0}']
        for k,(i,h) in enumerate(hs):
            if mode=='m': h=max(h,740)
            css.append(f'@page p{k}{{size:{W}px {h}px;margin:0}} section.page[id="{i}"]{{page:p{k};break-after:page}}')
        await pg.add_style_tag(content='\n'.join(css))
        await pg.pdf(path=out,print_background=True,prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
