import json,zipfile,os,shutil,sys
sys.path.insert(0,'/home/claude/work')
d=json.load(open('build/nuqul_7_9.json'));m=d['meta'];O=m['section_order'];S=m['sections']
E={int(x['card_number']):x for x in d['entries'] if x.get('card_number')}
PNAME={1:'الطب_وجسد_الطفل_وعلم_النفس',2:'المدرسة_والمجتمع_وأضرار_غياب_الأب',3:'دراسات_الرعاية_المشتركة_بالمناصفة',4:'المواثيق_والتشريعات_وسن_التمييز_والقضاء',5:'فتاوى_الأزهر_ودار_الإفتاء_المصرية',6:'فقه_مصر_والقرآن_والسنة_والفقه_الحنفي',7:'الفقه_المالكي_والشافعي_والحنبلي_والمقارن',8:'الأدلة_المتضافرة'}
PART={'med':1,'body':1,'psy':1,'school':2,'soc':2,'harm':2,'study':3,'intl':4,'law':4,'tamyiz':4,'court':4,'azhar':5,'eg':6,'f1':6,'f2':6,'f3':7,'f4':7,'f5':7,'f6':7,'hujaj':8}
def zname(lab,p):
    ns=[n for n,e in E.items() if PART[e['section']]==p]
    return f'صور_نمط_{lab}_الجزء_{p}_{PNAME[p]}_بطاقات_{min(ns)}-{max(ns)}.zip'
def folder(sec): return f"{O.index(sec)+1:02d}_{S[sec].replace(':','').replace(' ','_')}"
OUT='/mnt/user-data/outputs/البطاقات_المختصرة'
for st,src,lab in (('A','/tmp/claude-0/sp/simA','أ'),('B','/tmp/claude-0/sp/simB','ب')):
    zs={p:zipfile.ZipFile(f'{OUT}/'+zname(lab,p),'w',zipfile.ZIP_STORED) for p in range(1,9)}
    for n,e in sorted(E.items()):
        zs[PART[e['section']]].write(f'{src}/img_{st}/{n:03d}.png',f"{folder(e['section'])}/بطاقة_{n:03d}.png")
    for z in zs.values(): z.close()
shutil.copy('/tmp/claude-0/sp/simA/A.pdf',f'{OUT}/البطاقات_المختصرة_نمط_أ_بالدلالة.pdf')
shutil.copy('/tmp/claude-0/sp/simB/B.pdf',f'{OUT}/البطاقات_المختصرة_نمط_ب_النص_وحده.pdf')
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f'{OUT}/{f}')//1048576,'MB')
