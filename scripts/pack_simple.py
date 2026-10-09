import json,zipfile,os,shutil,sys
sys.path.insert(0,'/home/claude/work')
d=json.load(open('build/nuqul_7_9.json'));m=d['meta'];O=m['section_order'];S=m['sections']
E={int(x['card_number']):x for x in d['entries'] if x.get('card_number')}
PART={'med':1,'psy':1,'soc':2,'harm':2,'study':3,'intl':4,'law':4,'court':4,'eg':5,'f1':5,'f2':5,'f3':6,'f4':6,'f5':6,'f6':6}
def folder(sec): return f"{O.index(sec)+1:02d}_{S[sec].replace(':','').replace(' ','_')}"
OUT='/mnt/user-data/outputs/البطاقات_المختصرة'
for st,src,lab in (('A','/tmp/claude-0/sp/simA','أ'),('B','/tmp/claude-0/sp/simB','ب')):
    zs={p:zipfile.ZipFile(f'{OUT}/صور_نمط_{lab}_الجزء_{p}.zip','w',zipfile.ZIP_STORED) for p in range(1,7)}
    for n,e in sorted(E.items()):
        zs[PART[e['section']]].write(f'{src}/img_{st}/{n:03d}.png',f"{folder(e['section'])}/بطاقة_{n:03d}.png")
    for z in zs.values(): z.close()
shutil.copy('/tmp/claude-0/sp/simA/A.pdf',f'{OUT}/البطاقات_المختصرة_نمط_أ_بالدلالة.pdf')
shutil.copy('/tmp/claude-0/sp/simB/B.pdf',f'{OUT}/البطاقات_المختصرة_نمط_ب_النص_وحده.pdf')
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f'{OUT}/{f}')//1048576,'MB')
