import sys,asyncio
from playwright.async_api import async_playwright
async def main(html,ids,prefix,w):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':1000},device_scale_factor=1.5)
        await pg.goto('file://'+html); await pg.wait_for_timeout(1500)
        for i in ids:
            await pg.locator(f'section[id="{i}"]').screenshot(path=f'{prefix}{i}.png')
        await b.close()
asyncio.run(main(sys.argv[1],sys.argv[4].split(','),sys.argv[2],int(sys.argv[3])))
