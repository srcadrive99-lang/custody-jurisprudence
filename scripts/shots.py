import asyncio,os,zipfile,shutil,json
from playwright.async_api import async_playwright
H='/home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.html'
NAMES=json.load(open('/home/claude/work/secnames.json'))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':560,'height':1200},device_scale_factor=2)
        await pg.goto('file://'+H); await pg.wait_for_timeout(1500)
        ids=await pg.eval_on_selector_all('section.page','e=>e.map(x=>x.id)')
        cur=None;n=0
        for i in ids:
            if i.startswith('sec-'):
                cur=i[4:]; n=0
            if cur not in NAMES or i in('stats',): 
                if i=='stats': cur=None
                continue
            n+=1; d=f'imgs/{NAMES[cur]}'; os.makedirs(d,exist_ok=True)
            nm=f'{n:03d}_افتتاح.png' if i.startswith('sec-') else f'{n:03d}_بطاقة.png'
            await pg.locator(f'section[id="{i}"]').screenshot(path=f'{d}/{nm}')
        await b.close()
asyncio.run(main())
os.makedirs('build/صور_البطاقات',exist_ok=True)
for k,v in NAMES.items():
    with zipfile.ZipFile(f'build/صور_البطاقات/{v}.zip','w',zipfile.ZIP_STORED) as z:
        for f in sorted(os.listdir(f'imgs/{v}')): z.write(f'imgs/{v}/{f}',f)
    print(v,len(os.listdir(f'imgs/{v}')))
