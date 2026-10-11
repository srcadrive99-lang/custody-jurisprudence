import json
T='/home/claude/work/build/tools/'
d=json.load(open('/home/claude/work/build/nuqul_7_9.json'));E={int(x['card_number']):x for x in d['entries'] if x.get('card_number')}
num={x['id']:n for n,x in E.items()}; SN=d['meta']['sections']
H='#سن_الحضانة #سبعة_وتسعة #الرعاية_المشتركة_بالمناصفة #حق_الطفل_في_أبويه'
CAP={
'A5-215':'القانون الألماني، المادة 1684: الأب والأم لازم يمتنعوا عن أي حاجة تبوظ علاقة الطفل بالتاني.\nولو حد أخل بده، المحكمة تعين حد ينفذ اللقاء بنفسه.\nفي ألمانيا الطفل بيشوف أبوه حق ليه، مش ساعات تحت الرقابة.',
'A5-216':'القانون الفرنسي، المادة 373-2: كل واحد من الأب والأم لازم يحترم علاقة الطفل بالتاني.\nقطع الطفل عن أبوه وتشويه صورته مخالفة للقانون هناك.',
'A5-217':'قانون العقوبات الفرنسي: اللي يمنع الطفل عن والده اللي له حق يشوفه يتسجن سنة ويدفع 15 ألف يورو.\nفي فرنسا بيعاقبوا اللي يقطع الطفل عن أبوه، مش الأب اللي بيطلب ابنه.',
}
IDS={'A5-215':'','A5-216':'','A5-217':''}
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
