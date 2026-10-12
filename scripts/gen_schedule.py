import json,datetime
d=json.load(open('build/nuqul_7_9.json'));m=d['meta'];O=m['section_order'];S=m['sections']
E={int(x['card_number']):x for x in d['entries'] if x.get('card_number')}
T='build/tools/'
top=[r['n'] for r in json.load(open(T+'top50.json'))]
cap={x['n']:x for x in json.load(open(T+'fb_captions.json'))}
PNAME={1:'الطب_وجسد_الطفل_وعلم_النفس',2:'المدرسة_والمجتمع_وأضرار_غياب_الأب_والتخويف',3:'دراسات_الرعاية_المشتركة_بالمناصفة',4:'المواثيق_والتشريعات_وحماية_اللقاء_وسن_التمييز_والقضاء',5:'فتاوى_الأزهر_ودار_الإفتاء_المصرية',6:'فقه_مصر_والقرآن_والسنة_والفقه_الحنفي',7:'الفقه_المالكي_والشافعي_والحنبلي_والمقارن',8:'الأدلة_المتضافرة'}
PART={'med':1,'body':1,'psy':1,'school':2,'soc':2,'harm':2,'military':2,'fear':2,'study':3,'intl':4,'law':4,'enforce':4,'tamyiz':4,'court':4,'azhar':5,'eg':6,'f1':6,'f2':6,'f3':7,'f4':7,'f5':7,'f6':7,'hujaj':8}
def zname(lab,p):
    ns=[n for n,e in E.items() if PART[e['section']]==p]
    return f'صور_نمط_{lab}_الجزء_{p}_{PNAME[p]}_بطاقات_{min(ns)}-{max(ns)}.zip'
def folder(sec): return f"{O.index(sec)+1:02d}_{S[sec].replace(':','').replace(' ','_')}"
def img(n): s=E[n]['section']; return f"البطاقات_المختصرة/{zname('أ',PART[s])} ← {folder(s)}/بطاقة_{n:03d}.png"
mahdi=[n for n in sorted(E) if E[n]['section']=='azhar']
hj=[n for n in sorted(E) if E[n]['section']=='hujaj']
order=hj+[n for n in top if n not in hj]+[n for n in mahdi if n not in top]
rest={s:[n for n in sorted(E) if E[n]['section']==s and n not in order] for s in O}
while any(rest.values()):
    for s in O:
        if rest[s]: order.append(rest[s].pop(0))
assert len(order)==len(E)==len(set(order))
DAYS=['الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت','الأحد']
start=datetime.date(2026,10,10); ndays=(len(order)+1)//2; end=start+datetime.timedelta(days=ndays-1)
L=['# جدول النشر على فيسبوك — البطاقات المختصرة (النمط أ)','',
 f'منشوران يوميا بتوقيت القاهرة: الساعة 1:00 ظهرا والساعة 9:00 مساء، من السبت {start} إلى {end} ({ndays} يوما، {len(order)} منشورا).','',
 '- الأيام الأولى: قسم «الأدلة المتضافرة» كله، ثم البطاقات الخمسون الأقوى بترتيب قوتها، ثم قسم فتاوى الأزهر ودار الإفتاء المصرية كله.',
 '- بعدها: بقية البطاقات موزعة على الأقسام بالتناوب.',
 '- لكل منشور: صورة واحدة من ملفات «البطاقات_المختصرة»، ومعها التعليق الجاهز للصق كما هو.',
 '- من أراد النص الكامل والمصدر والرابط يجده في البطاقة نفسها برقمها في الطبعة الكاملة وفي «الطبعة النصية للبطاقات بالروابط».','',
 '## الجدول المختصر','','| اليوم | التاريخ | الوقت | رقم البطاقة | عنوانها | الصورة |','|---|---|---|---|---|---|']
rows=[]
for i,n in enumerate(order):
    day=i//2; dt=start+datetime.timedelta(days=day); t='1:00 ظهرا' if i%2==0 else '9:00 مساء'
    rows.append((day+1,DAYS[dt.weekday()],dt,t,n))
    L.append(f"| {day+1} — {DAYS[dt.weekday()]} | {dt} | {t} | {n} | {E[n]['title']} | {img(n)} |")
L+=['','## التعليقات الجاهزة للصق بترتيب النشر','']
for day,dn,dt,t,n in rows:
    c=cap[n]
    L+=[f"### اليوم {day} — {dn} {dt} — {t} — بطاقة {n}",'',f"الصورة: {img(n)}",'','```',c['caption'],'',c['hashtags'],'```','']
open(T+'جدول_النشر.md','w',encoding='utf8').write('\n'.join(L)); print(len(order),ndays,end)
