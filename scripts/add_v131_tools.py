import json
T='/home/claude/work/build/tools/'
d=json.load(open('/home/claude/work/build/nuqul_7_9.json'));E={int(x['card_number']):x for x in d['entries'] if x.get('card_number')}
num={x['id']:n for n,x in E.items()}; SN=d['meta']['sections']
H='#سن_الحضانة #سبعة_وتسعة #الرعاية_المشتركة_بالمناصفة #حق_الطفل_في_أبويه'
CAP={
'A4-124':'مؤسسة راند ومجلة طب الأطفال الأمريكية: أطفال الجنود اللي أبوهم غايب في الحرب أكتر اضطرابا، وكل ما طال الغياب زادت مشاكلهم.\nالأب هنا بطل مش متهم.. والطفل اتأذى من الغياب نفسه.',
'A4-125':'دراسة على 642 ألف طفل من أولاد العسكريين: غياب الأب في الخدمة زود زياراتهم للطبيب النفسي 11%.\nغياب شريف ومؤقت.. أمال الغياب اللي القانون بيفرضه 15 سنة؟',
'A4-126':'دراسة على 300 ألف طفل من أولاد الجنود: كل ما طال غياب الأب زادت تشخيصات القلق والاكتئاب واضطراب السلوك.\nالغياب بيتقاس بالشهور، وأثره بيتقاس في الأطفال.',
'A2-124':'تحليل لعشر دراسات على 1611 مريض بالوسواس القهري: الإيذاء العاطفي في الطفولة مرتبط بشدة الوسواس.\nاللي بيلقن الطفل الخوف من أبوه بيزرع فيه هشاشة نفسية تعيش معاه.',
'A2-125':'تجربة في جامعة ساسكس: الطفل بيخاف بكلام البالغ اللي بيثق فيه، مش بكلام أصحابه ولا بالصور.\nكلمة من الحاضنة «أبوك هيسممك» بتزرع خوف يفضل.',
}
IDS={'A4-124':'مؤسسة راند: أكبر مؤسسة بحوث سياسات في أمريكا','A4-125':'الجامعة العسكرية الأمريكية للعلوم الصحية','A4-126':'جامعة نورث كارولينا','A2-124':'جامعة سنترال ساوث الصينية','A2-125':'آندي فيلد: أستاذ علم النفس بجامعة ساسكس البريطانية'}
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
