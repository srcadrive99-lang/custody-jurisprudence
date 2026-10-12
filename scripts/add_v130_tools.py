import json
T='/home/claude/work/build/tools/'
d=json.load(open('/home/claude/work/build/nuqul_7_9.json'));E={int(x['card_number']):x for x in d['entries'] if x.get('card_number')}
num={x['id']:n for n,x in E.items()}; SN=d['meta']['sections']
H='#سن_الحضانة #سبعة_وتسعة #الرعاية_المشتركة_بالمناصفة #حق_الطفل_في_أبويه'
CAP={
'A1-117':'الكاساني في بدائع الصنائع: ولاية الأب على ابنه سببها كمال شفقته وكمال رأيه.\nالأب أشفق الناس على ابنه، مش غريب يزوره ساعات.',
'A1-118':'القدوري: شفقة الأب لوحدها كفاية تحفظ ابنه، ومحدش غيره عنده الشفقة دي.\nعشان كده ربنا وصى باليتيم اللي فقد أبوه.\nحرمان الطفل من أبوه الحي بيخليه زي اليتيم.',
'A4-123':'ابن حجر في فتح الباري: من شفقة الأب إنه ينصح ابنه ويعرفه اللي ينفعه ويحذره من الغلط.\nإزاي يتمنع الأب من نصح ابنه وإرشاده؟',
'A1-119':'الشيخ عبد الوهاب خلاف من علماء مصر: شفقة الأب وحرصه على مصلحة أولاده ما يحتاجوش ضمان تاني.\nالأب مؤتمن على ولاده، مش متهم.',
'A1-120':'فتوى مفتي مصر الشيخ عبد المجيد سليم 1940: البنت الصغيرة يضمها أبوها، وشفقة غيره ما توصلش لشفقة الأب.',
'A1-121':'القاضي شريح، قاضي عمر بن الخطاب: «الأب أشفق والأم أرفق».\nالطفل محتاج شفقة الأب ورفق الأم مع بعض.',
'A1-122':'الفقها وشراح السنة وعلماء مصر على كلمة واحدة: الأب أكمل الناس شفقة على ابنه.\nحرمانه من ابنه ضد الشرع والعقل.',
}
IDS={'A1-117':'','A1-118':'','A4-123':'','A1-119':'','A1-120':'','A1-121':'','A1-122':''}
c=json.load(open(T+'fb_captions.json'))
c=[x for x in c if x['n'] not in [num[k] for k in CAP]]
for k,v in CAP.items(): c.append(dict(n=num[k],section=SN[E[num[k]]['section']],caption=v,hashtags=H))
for x in c: x['section']=SN[E[x['n']]['section']]
c.sort(key=lambda x:x['n']); json.dump(c,open(T+'fb_captions.json','w'),ensure_ascii=False,indent=1)
s=json.load(open(T+'short_ids.json'))
for k,v in IDS.items(): s[str(num[k])]=v
json.dump(dict(sorted(s.items(),key=lambda x:int(x[0]))),open(T+'short_ids.json','w'),ensure_ascii=False,indent=1)
L=['# تعليقات فيسبوك لكل البطاقات','',f'عدد البطاقات: {len(c)}. لكل بطاقة تعليق من سطرين أو ثلاثة بالعامية المصرية، ثم الوسوم.','']
sec=None
for x in sorted(c,key=lambda x:x['n']):
    if x['section']!=sec: sec=x['section']; L+=['',f'## {sec}','']
    L+=[f"### بطاقة {x['n']} — {E[x['n']]['title']}",'',x['caption'],'',x['hashtags'],'','---','']
open(T+'تعليقات_فيسبوك.md','w',encoding='utf8').write('\n'.join(L))
print(len(c),len(s),len(E), [n for n in E if n not in {x['n'] for x in c}][:10])
