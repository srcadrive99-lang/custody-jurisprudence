import json,re,glob
old=json.load(open('/tmp/claude-0/old_id2num.json'))
d=json.load(open('build/nuqul_7_9.json'))
new={x['id']:int(x['card_number']) for x in d['entries'] if x.get('card_number')}
M={str(v):new[k] for k,v in old.items() if k in new}
def mp(n): return M[str(n)]
T='build/tools/'
t=json.load(open(T+'top50.json'));[r.update(n=mp(r['n'])) for r in t];json.dump(t,open(T+'top50.json','w'),ensure_ascii=False,indent=1)
t=json.load(open(T+'top50_english.json'));[r.update(card=mp(r['card'])) for r in t];json.dump(t,open(T+'top50_english.json','w'),ensure_ascii=False,indent=1)
c=json.load(open(T+'fb_captions.json'));[r.update(n=mp(r['n'])) for r in c];json.dump(c,open(T+'fb_captions.json','w'),ensure_ascii=False,indent=1)
s=json.load(open(T+'short_ids.json'));s2={str(mp(k)):v for k,v in s.items()};json.dump(s2,open(T+'short_ids.json','w'),ensure_ascii=False,indent=1)
pat=re.compile(r'((?:بطاقة|البطاقة|بطاقتي|البطاقتين|البطاقتان|Card|card)\s*(?:رقم\s*)?)(\d{1,3}(?:\s*(?:،|,|و|-|–)\s*\d{1,3})*)')
def fix(m):
    return m.group(1)+re.sub(r'\d{1,3}',lambda x:str(mp(x.group())) if x.group() in M else x.group(),m.group(2))
for f in glob.glob(T+'*.md')+[T+'TOP50_EN.html']:
    if 'جدول_النشر' in f or 'تعليقات_فيسبوك' in f: continue
    s=open(f,encoding='utf8').read(); s2=pat.sub(fix,s); open(f,'w',encoding='utf8').write(s2); print(f, s!=s2)
print('mapped',len(M))
