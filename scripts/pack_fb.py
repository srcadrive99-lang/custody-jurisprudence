import json,os,zipfile,collections
NAMES=json.load(open('secnames.json'))
seq=json.load(open('fb_seq.json'))
groups=collections.OrderedDict(); groups['00_الغلاف_والفهرس_والإحصاءات']=[]
cur='00_الغلاف_والفهرس_والإحصاءات'
for id_,f in seq:
    if id_ in ('cover','toc','stats'):
        groups['00_الغلاف_والفهرس_والإحصاءات'].append((id_,f)); continue
    if id_.startswith('sec-'): cur=NAMES[id_[4:]]; groups.setdefault(cur,[])
    groups[cur].append((id_,f))
os.makedirs('build/صور_فيسبوك',exist_ok=True)
for g,items in groups.items():
    with zipfile.ZipFile(f'build/صور_فيسبوك/{g}.zip','w',zipfile.ZIP_STORED) as z:
        n=0; cnt=collections.Counter()
        for id_,f in items:
            n+=1
            if id_ in ('cover','toc','stats'):
                lab={'cover':'الغلاف','toc':'الفهرس','stats':'الإحصاءات'}[id_]; cnt[id_]+=1; nm=f'{n:03d}_{lab}_{cnt[id_]}.png'
            elif id_.startswith('sec-'): nm=f'{n:03d}_افتتاح.png'
            else: nm=f'{n:03d}_بطاقة.png'
            z.write(f,nm)
    print(g,len(items))
