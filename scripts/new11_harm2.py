# -*- coding: utf-8 -*-
# v1.24.0: criminology, juvenile justice, prisons, homelessness, child psychiatry — father absence harms (harm section)
import json,copy
P='/home/claude/work/new_cards.json'; V='/home/claude/work/verify/'
N=json.load(open(P,encoding='utf8')); N=[x for x in N if not x.get('harm2')]
A={a['key']:a for f in ['new_crime.json','new_prison_home.json','new_psych.json'] for a in json.load(open(V+f,encoding='utf8')) if a.get('key')!='_rejected'}
tpl=[x for x in N if x['id']=='A4-071'][0]
CH=[['str','دلالة صريحة'],['sup','صلة الرحم']]
def mk(cid,key,icon,title,author,year,where,jur,level,about,arg,ot=None,tt=None,links=None,sup=('silat_al_rahim',)):
    a=A[key]; e=copy.deepcopy(tpl)
    e.update(id=cid,icon=icon,supports=list(sup),strength='explicit',jurisdiction=jur,title=title,
             ot='"'+(ot or a['quote'])+'"',ltr=True,tt='«'+(tt or a['quote_ar'])+'»',about=about or a['about'],level=level or a['level'],arg=arg or a['argument'],chips=CH,harm2=True)
    e['src']=dict(author=author,year=str(year),jur=jur,title_latin=a['title_latin'],sw='',where=where,latin=True)
    L=links or [(a['url'],'النص في مصدره'),(a.get('url2') or '','المصدر الثاني')]
    e['links']=[dict(url=u,label=l,site=s,domain=u.split('/')[2]) for u,l,s in [(x[0],x[1],x[2] if len(x)>2 else '') for x in L] if u]
    return e
C=[
mk('A4-079','bjs-1988-survey-youth-custody-70pct-without-both-parents','us',
 'مكتب إحصاءات العدالة الأمريكي 1988 — 7 من كل 10 أحداث محتجزين نشؤوا بلا والديهم معا، وأكثرهم مع الأم وحدها',
 'Beck AJ, Kline SA, Greenfeld LA — Bureau of Justice Statistics',1988,'BJS Special Report NCJ-113365, September 1988 — Table 2',
 'الولايات المتحدة — وزارة العدل، مكتب إحصاءات العدالة','إحصاء رسمي للدولة',
 'تقرير رسمي من مكتب إحصاءات العدالة في وزارة العدل الأمريكية، مبني على مسح وطني لكل نزلاء مؤسسات احتجاز الأحداث الحكومية الطويلة الأمد.',
 'ثلاثة أرباع أطفال أمريكا كانوا يعيشون مع والديهم معا، أما في سجون الأحداث فأقل من الثلث، ونحو نصف المحتجزين نشؤوا مع الأم وحدها؛ فغياب الأب عن نشأة الولد يلازمه دخول السجن، والوقاية بقاء الأب في حياة ولده بعد الفراق.',
 links=[('https://bjs.ojp.gov/content/pub/pdf/syc87.pdf','نص التقرير الرسمي','مكتب إحصاءات العدالة الأمريكي'),('https://bjs.ojp.gov/library/publications/survey-youth-custody-1987-0','صفحة التقرير','مكتب إحصاءات العدالة الأمريكي')]),
mk('A4-080','sedlak_bruce_syrp_2010','us',
 'مكتب قضاء الأحداث الأمريكي 2010 — خطر احتجاز الحدث الذي يعيش مع والد واحد 3.6 أضعاف خطره مع والديه',
 'Sedlak AJ, Bruce C — OJJDP',2010,'OJJDP Juvenile Justice Bulletin NCJ 227730, December 2010, p. 6 and Table 4',
 'الولايات المتحدة — وزارة العدل، مكتب قضاء الأحداث ومنع الجنوح','إحصاء رسمي للدولة',None,
 'الحدث الذي يعيش مع والد واحد يتعرض لخطر الاحتجاز بنحو 3.6 أضعاف من يعيش مع والديه معا؛ فبقاء الوالدين كليهما في حياة الولد حماية له من السجن، وهذا أصل الرعاية المشتركة.',
 links=[('https://www.ojp.gov/pdffiles1/ojjdp/227730.pdf','نص النشرة الرسمية','وزارة العدل الأمريكية'),('https://ojjdp.ojp.gov/library/publications/survey-youth-residential-placement-youth-characteristics-and-backgrounds','صفحة النشرة','مكتب قضاء الأحداث الأمريكي')],sup=('silat_al_rahim','shared_parenting')),
mk('A4-081','ojjdp-2006-national-report-both-biological-parents-lower-offending','us',
 'التقرير الوطني الأمريكي عن الأحداث 2006 — من عاشوا مع أبيهم وأمهم معا أقل مخالفة للقانون',
 'Snyder HN, Sickmund M — OJJDP',2006,'Juvenile Offenders and Victims: 2006 National Report (NCJ 212906), Chapter 3, p. 72',
 'الولايات المتحدة — وزارة العدل، مكتب قضاء الأحداث ومنع الجنوح','إحصاء رسمي للدولة',None,None,
 links=[('https://ojjdp.ojp.gov/ojstatbb/nr2006/downloads/nr2006_hl.pdf','خلاصة التقرير الرسمي','مكتب قضاء الأحداث الأمريكي'),('https://ojp.gov/index%2ephp/node/1146836','صفحة التقرير','وزارة العدل الأمريكية')]),
mk('A4-082','sampson_1987_ajs','us',
 'سامبسون 1987 — تفكك الأسرة يرفع القتل والسرقة بالإكراه عند الأحداث مهما كان الدخل',
 'Sampson RJ',1987,'American Journal of Sociology 93(2): 348–383',
 'الولايات المتحدة — مجلة علم الاجتماع الأمريكية (جامعة شيكاغو)','دراسة محكمة في مجلة كبرى',None,None,
 ot='The study examines race-specific rates of robbery and homicide by juveniles and adults in over 150 U.S. cities in 1980. ... family disruption substantially increases the rates of ... murder and robbery, especially by juveniles. These effects are independent of income, region, race and age composition, density, city size, and welfare benefits ...',
 tt='تدرس الدراسة معدلات السرقة بالإكراه والقتل التي يرتكبها الأحداث والبالغون في أكثر من 150 مدينة أمريكية سنة 1980 ... وتفكك الأسرة [غياب الآباء عن البيوت] يرفع معدلات ... القتل والسرقة بالإكراه رفعا كبيرا، ولا سيما عند الأحداث. وهذه الآثار قائمة مهما كان الدخل والإقليم والتركيب العمري والعرقي وكثافة السكان وحجم المدينة وإعانات الرعاية الاجتماعية ...',
 links=[('https://dash.harvard.edu/handle/1/3226953','نص البحث في مستودع جامعة هارفارد','جامعة هارفارد'),('https://ojp.gov/ncjrs/virtual-library/abstracts/urban-black-violence-effect-male-joblessness-and-family-disruption','ملخص البحث','المكتبة الرقمية لوزارة العدل الأمريكية')]),
mk('A4-083','kroese_2021_systematic_review','nl',
 'مراجعة 48 دراسة 2021 — النشأة مع والد واحد ترفع خطر جريمة المراهقين',
 'Kroese J, Bernasco W, Liefbroer AC, Rouwendal J',2021,'Psychology, Crime & Law 27(1): 61–75',
 'هولندا — المعهد الهولندي لدراسة الجريمة وإنفاذ القانون','مراجعة منظمة للدراسات',None,None,
 links=[('https://pure.knaw.nl/portal/nl/publications/growing-up-in-single-parent-families-and-the-criminal-involvement/','ملخص المراجعة','الأكاديمية الملكية الهولندية للعلوم')]),
mk('A4-084','kroese_2022_thesis_mother_only','nl',
 'سجلات هولندا الوطنية 2022 — النشأة مع الأم وحدها أخطر في الجريمة من النشأة مع الأب وحده',
 'Kroese J — Vrije Universiteit Amsterdam',2022,'PhD thesis, Vrije Universiteit Amsterdam, 19 May 2022 — Statistics Netherlands register data',
 'هولندا — جامعة فريه أمستردام، السجلات الوطنية لهيئة الإحصاء الهولندية','دراسة سجلات وطنية',None,None,
 links=[('https://research.vu.nl/en/publications/broken-homes-and-crime-differential-effects-of-parental-separatio/','ملخص الرسالة','جامعة فريه أمستردام'),('https://nscr.nl/en/higher-risk-of-criminal-behaviour-with-children-growing-up-in-a-single-parent-family/','خبر المعهد الهولندي لدراسة الجريمة','المعهد الهولندي لدراسة الجريمة')],sup=('silat_al_rahim','shared_parenting')),
mk('A4-085','teneyck_2023_absent_father_timing','us',
 'تين إيك وزملاؤه 2023 — غياب الأب في أي مرحلة يلازمه الإجرام والقبض لاحقا',
 'TenEyck MF, Knox KN, El Sayed SA',2023,'American Journal of Criminal Justice 48: 193–217',
 'الولايات المتحدة — المجلة الأمريكية للعدالة الجنائية','دراسة محكمة على عينة وطنية',None,None,
 links=[('https://link.springer.com/doi/10.1007/s12103-021-09640-x','صفحة الدراسة','دار سبرينغر')]),
mk('A4-086','mackenzie-chamberlain-2008-homeless-students-single-parent-blended','au',
 'التعداد الوطني للطلاب المشردين في أستراليا 2008 — أبناء الوالد الواحد أكثر بين المشردين',
 'MacKenzie D, Chamberlain C',2008,'Youth Studies Australia 27(1): 17–25',
 'أستراليا — التعداد الوطني للطلاب المشردين','تعداد وطني',None,
 'تعداد وطني للطلاب المشردين في أستراليا يبين أن أبناء الأسر ذات الوالد الواحد أكثر تعرضا للتشرد من غيرهم؛ فانقطاع الولد عن أحد والديه عامل خطر، وهذا يدعو إلى حفظ صلته بوالديه كليهما بعد الفرقة.',
 links=[('https://ojp.gov/ncjrs/virtual-library/abstracts/youth-homelessness-2006','ملخص البحث','المكتبة الرقمية لوزارة العدل الأمريكية')]),
mk('A4-087','esbjorn-2008-denmark-child-psychiatry-family-status','dk',
 'السجل الوطني للطب النفسي للأطفال في الدنمارك 2008 — نصف المرضى فقط يعيشون مع والديهم مقابل ثلاثة أرباع عامة الأطفال',
 'Esbjørn BH, Levin E, Høyer M, Dyrborg J',2008,'European Child & Adolescent Psychiatry 17(8): 484–490',
 'الدنمارك — السجل الوطني لأطفال الطب النفسي','دراسة سجلات وطنية',None,
 'نحو نصف أطفال الطب النفسي في الدنمارك كلها لا يعيشون مع الأب والأم معا، مقابل ربع الأطفال فقط في عامة السكان؛ فقطع الطفل عن أحد والديه يرتبط بحاجته إلى الطب النفسي، وهذا حجة لإبقاء الأب حاضرا في حياة ولده.',
 links=[('https://research.regionh.dk/en/publications/child-and-adolescent-psychiatry-and-family-status-a-nationwide-re/','ملخص الدراسة','مستشفيات منطقة العاصمة الدنماركية')]),
mk('A4-088','sourander-2009-finland-1981-boys-suicide','fi',
 'جماعة مواليد فنلندا 1981 — الصبي الذي لا يعيش مع أبيه وأمه في الثامنة أكثر عرضة لخطر الانتحار في شبابه',
 'Sourander A, Klomek AB, et al.',2009,'Archives of General Psychiatry 66(4): 398–406 — reported in Psychiatric News (American Psychiatric Association)',
 'فنلندا — جماعة مواليد 1981 الوطنية','دراسة متابعة لجماعة مواليد وطنية',None,None,
 links=[('https://psychnews.psychiatryonline.org/doi/10.1176/pn.44.11.0019','خبر الجمعية الأمريكية للطب النفسي','الجمعية الأمريكية للطب النفسي')]),
mk('A4-089','hjern-2010-sweden-adhd-single-parent','se',
 'سجل الأدوية الوطني السويدي 2010 — أطفال الوالد الواحد أكثر علاجا من نقص الانتباه وفرط الحركة بنسبة 54%',
 'Hjern A, Weitoft GR, Lindblad F',2010,'Acta Paediatrica 99(6): 920 — reported by ScienceDaily',
 'السويد — سجل الأدوية الوطني','دراسة سجلات وطنية',None,None,
 links=[('https://www.sciencedaily.com/releases/2010/06/100601072634.htm','خبر الدراسة','ScienceDaily')]),
mk('A4-090','ons-2019-england-lone-parent-mental-disorder','uk',
 'مكتب الإحصاء الوطني البريطاني 2019 — أطفال الوالد الواحد أكثر إصابة بالاضطرابات النفسية',
 'Office for National Statistics',2019,'ONS article, 26 March 2019 — Mental Health of Children and Young People in England, 2017',
 'المملكة المتحدة — مكتب الإحصاء الوطني','إحصاء رسمي للدولة',None,None,
 links=[('https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/childhealth/articles/childrenwhosefamiliesstruggletogetonaremorelikelytohavementaldisorders/2019-03-26','نص التقرير الرسمي','مكتب الإحصاء الوطني البريطاني')]),
]
# place right after the last existing harm card in the list (section order is by list order)
N+=C
json.dump(N,open(P,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('added',len(C))
