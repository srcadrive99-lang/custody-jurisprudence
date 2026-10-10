import json
T='build/tools/'
d=json.load(open('build/nuqul_7_9.json'));E={int(x['card_number']):x for x in d['entries'] if x.get('card_number')}
num={x['id']:n for n,x in E.items()}; SN=d['meta']['sections']
H='#سن_الحضانة #سبعة_وتسعة #الرعاية_المشتركة_بالمناصفة #حق_الطفل_في_أبويه #فتاوى_الأزهر'
I='الشيخ المهدي العباسي، مفتي الديار المصرية وشيخ الأزهر في القرن الـ19، وفتاواه متسجلة بتاريخها في «الفتاوى المهدية».'
CAP={
'A1-078':I+'\nالحاضنة، أم أو غيرها، أحق بالولد لحد ما يستغنى، واتقدر بـ 7 سنين، وبعدها ما لهاش حق في حضانته.\nالسابعة حد قديم.. شاركها.',
'A1-079':I+'\nالبنت لما تكمل 9 حضانة أمها بتخلص، والأم ما ينفعش تمتنع عن تسليمها بأي حجة.\nانشرها.',
'A1-080':I+'\nفي فتوى واحدة: الولد اللي كمل 7 يروح لأبوه، وإخواته الصغيرين يفضلوا مع أمهم والأب يصرف عليهم ويدفع أجرة حضانتهم.\nده العدل.. شاركها.',
'A1-081':I+'\n«لا حضانة للأم إذا بلغ سن البنت تسع سنين على ما به الفتوى».\nكلمة واضحة من مفتي مصر.. انشرها.',
'A1-082':'فتوى رسمية من دار الإفتاء المصرية سنة 1920، بتوقيع الشيخ محمد بخيت مفتي الديار المصرية.\n«الولد متى كان عند أحد الأبوين لا يمنع الآخر عن النظر إليه وعن تعهده».\nالطفل لأبوه وأمه الاتنين.. ده أصل الرعاية المشتركة.',
'A1-083':'فتوى رسمية من دار الإفتاء المصرية سنة 1964، بتوقيع الشيخ أحمد هريدي مفتي الجمهورية.\nبعد ما حضانة الستات تخلص الأولاد بيبقوا مع أبوهم، والأب ما يمنعش الأم إنها تشوفهم.\nصلة الرحم محفوظة للاتنين.. شاركها.',
}
c=json.load(open(T+'fb_captions.json'))
c=[x for x in c if x['n'] not in [num[k] for k in CAP]]
for k,v in CAP.items(): c.append(dict(n=num[k],section=SN['azhar'],caption=v,hashtags=H))
for x in c: x['section']=SN[E[x['n']]['section']]
c.sort(key=lambda x:x['n']); json.dump(c,open(T+'fb_captions.json','w'),ensure_ascii=False,indent=1)
s=json.load(open(T+'short_ids.json'))
for k in CAP: s[str(num[k])]=''
for k,v in list(s.items()):
    if v.startswith('المهدي العباسي'): s[k]=''
json.dump(dict(sorted(s.items(),key=lambda x:int(x[0]))),open(T+'short_ids.json','w'),ensure_ascii=False,indent=1)
L=['# تعليقات فيسبوك لكل البطاقات','',f'عدد البطاقات: {len(c)}. لكل بطاقة تعليق من سطرين أو ثلاثة بالعامية المصرية، ثم الوسوم.','']
sec=None
for x in c:
    if x['section']!=sec: sec=x['section']; L+=['',f'## {sec}','']
    L+=[f"### بطاقة {x['n']} — {E[x['n']]['title']}",'',x['caption'],'',x['hashtags'],'','---','']
open(T+'تعليقات_فيسبوك.md','w',encoding='utf8').write('\n'.join(L))
print(len(c),len(s),len(E))
