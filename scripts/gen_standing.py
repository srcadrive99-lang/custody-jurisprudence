# -*- coding: utf-8 -*-
import json,re,sys
sys.path.insert(0,'/home/claude/work')
from assemble import SEC, ORDER, mn_plain
j=json.load(open('/home/claude/work/build/nuqul_7_9.json',encoding='utf8'))
old=open('/home/claude/work/build/منزلة_المصادر_ودرجة_الأدلة.md',encoding='utf8').read()
head=old.split('## خبراء الطب')[0].rstrip()
md=[head,'']
for k in ORDER:
    rows=[e for e in j['entries'] if e.get('section')==k and e.get('source_standing')]
    if not rows: continue
    md+=[f'## {mn_plain(SEC[k]["name"])}','','| البطاقة | العنوان | عن المصدر | درجة الدليل |','|---|---|---|---|']
    for e in sorted(rows,key=lambda x:x['card_number']):
        t=(e.get('title') or e['author']['name']).replace('|','／')
        md.append(f'| {e["card_number"]} | {t} | {e["source_standing"].replace("|","／")} | {e.get("evidence_level","")} |')
    md.append('')
open('/home/claude/work/build/منزلة_المصادر_ودرجة_الأدلة.md','w',encoding='utf8').write('\n'.join(md))
print('rows',sum(1 for e in j['entries'] if e.get('source_standing') and e.get('section')))
