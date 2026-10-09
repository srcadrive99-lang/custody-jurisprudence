# -*- coding: utf-8 -*-
"""Turn verification results (verify/result_*.json) into an overlay used by assemble.py and gen_data.py."""
import json, glob, re
TASH=re.compile('[ً-ْٰـ]'); AD=str.maketrans('٠١٢٣٤٥٦٧٨٩','0123456789')
def clean_ar(s): return TASH.sub('',s).translate(AD).strip()
B=json.load(open('build/nuqul_7_9.json')); E={e['id']:e for e in B['entries']}
R={}
for f in sorted(glob.glob('verify/result_*.json')):
    for x in json.load(open(f)): R[x['id']]=x
# found_text taken from secondary pages (reviews, lecture slides, encyclopaedias): do not put on the card as the author's words
SECONDARY={'A2-014','A5-060','A2-017','A5-068','A5-076','A5-077','A5-082','A5-066','A5-067','A2-006','A5-088','A5-079','A5-026','A1-046','A1-003','A4-012','A2-008'}
RETIRE={
 'A5-051':'المطابقة: فريق رابطة محاكم الأسرة رفض صراحة افتراض قانوني لتوزيع محدد للوقت بين الوالدين، فهو حجة على الرعاية المشتركة بالمناصفة.',
 'A5-050':'المطابقة: ملخص المراجعة يقرر أن مخاطر الإقامة المشتركة ومنافعها «لم تتضح بعد».',
 'A5-086':'المطابقة: الباحث يخلص إلى أن الإقامة المشتركة لا تنفع إلا حين يكون النزاع بين الوالدين منخفضا.',
 'A5-049':'المطابقة: التحليل وجد أن تكرار التواصل مع الأب غير المقيم لا يرتبط بنتائج الأطفال.',
 'A5-092':'المطابقة: المراهقون في الإقامة المشتركة كانوا كأقرانهم في أسر الأم المنفردة لا أحسن منهم.',
 'A5-094':'المطابقة: الملخص يجعل حال أطفال الإقامة المشتركة «مماثلا» لا أحسن، وقد يسوء مع النزاع.',
 'A5-084':'المطابقة: في مقدمة الكتاب أن الأدلة لا تكفي بعد لتقرير نفع الإقامة المشتركة على الحضانة المنفردة.',
 'A5-096':'المطابقة: التقرير يقدم الجودة على الكم ويقرر أن زيادة انخراط الأب ليست الأفضل في كل حال.',
}
TITLES={
 'A2-005':'الغزالي — لا يسامح الصبي في ترك الطهارة والصلاة إذا بلغ سن التمييز',
 'A5-014':'القانون الأرجنتيني — الحضانة المشتركة خيار أول يلزم به القاضي',
 'A5-087':'مايكل لامب 2018 — الأطفال ينتفعون حين تحفظ خطط الرعاية صلتهم بالوالدين معا',
 'A5-083':'وارشاك 2018 — مراجعة القيود العامة على مبيت الصغار عند آبائهم',
 'A5-085':'فرانسون وهيرن وبيرغستروم 2018 — حصيلة البحوث في الرعاية المشتركة بعد الانفصال',
 'A5-088':'برافر ولامب 2018 — آراء الخبراء في الرعاية المشتركة بعد الانفصال',
 'A4-007':'رد المحتار عن التتارخانية — لا يمنع أحد الأبوين من النظر إلى ولده وتعهده',
 'A5-036':'القانون الهولندي — حق الطفل في رعاية وتربية متكافئتين من الوالدين بعد الانفصال',
}
SITE={'shamela.ws':'المكتبة الشاملة','sunnah.com':'موقع السنة','dorar.net':'الدرر السنية','archive.org':'أرشيف الإنترنت'}
ov=dict(ot={},links={},retire=RETIRE,titles=TITLES,conf={},notes={})
for i,x in R.items():
    if i not in E: continue
    e=E[i]; st=x['status']
    if st in ('verified_verbatim','verified_gist','corrected') and i!='A1-046':
        ov['conf'][i]='verified'
    if x.get('notes'): ov['notes'][i]=(x.get('location','')+' — '+x['notes'])[:900]
    ft=x['found_text'].strip()
    gist=not e['original']['verbatim']
    if ft and i not in SECONDARY and i not in RETIRE and (gist or st=='corrected'):
        if re.search('[؀-ۿ]',ft[:40]):
            ov['ot'][i]=dict(text=clean_ar(ft),ltr=False,tt='',lang='ar')
        else:
            ar=clean_ar(x['proposed_ar'])
            if i!='A5-040': ar=ar.replace('الرعاية المشتركة بالمناصفة','الرعاية المشتركة').replace('الرعاية المشتركة','الحضانة المشتركة')
            ov['ot'][i]=dict(text=ft,ltr=True,tt=ar,lang=e['original']['lang'] if e['original']['lang']!='ar' else 'en')
    # heritage cards without any link: add the verified page
    su=x.get('source_url','')
    if su and not (e.get('links') or e.get('urls')) and len(su)<240:
        d=su.split('/')[2]
        ov['links'][i]=dict(url=su,label='النص في مصدره',site=SITE.get(d,d),domain=d)
json.dump(ov,open('verify/overlay.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print('ot',len(ov['ot']),'links',len(ov['links']),'conf',len(ov['conf']),'retire',len(RETIRE))
print(sorted(ov['ot']))
