# -*- coding: utf-8 -*-
"""Batch 7 (v1.20.0): cards from verified research agents (Egypt fatwas, Muslim-law courts, fiqh al-ithghar,
father-absence harm, Spain INE statistics) + Piaget/Malaysia corrections."""
import json, re
V='/home/claude/work/verify/'
def load(f): return {x['key']:x for x in json.load(open(V+f)) if x['key']!='_rejected'}
EG=load('new_eg.json'); CO=load('new_courts.json'); FQ=load('new_fiqh.json'); HA=load('new_harm.json'); ST=load('new_stats.json')
TASH=re.compile('[ً-ْٰـ]')
AD=str.maketrans('٠١٢٣٤٥٦٧٨٩','0123456789')
def clean_ar(s): return TASH.sub('',s).translate(AD)
SITE={'shamela.ws':'المكتبة الشاملة','indiankanoon.org':'قاعدة الأحكام الهندية','www.ine.es':'المعهد الوطني للإحصاء في إسبانيا','ine.es':'المعهد الوطني للإحصاء في إسبانيا','sunnah.com':'موقع السنة','dorar.net':'الدرر السنية','archive.org':'أرشيف الإنترنت','link.springer.com':'دار سبرينغر','journals.sagepub.com':'دار سيج','doi.org':'صفحة الدراسة','api.openalex.org':'سجل OpenAlex','openalex.org':'سجل OpenAlex'}
def link(u,label):
    d=u.split('/')[2]
    return dict(url=u,label=label,site=SITE.get(d,d),domain=d)
C=[]
def card(x,id,sec,icon,title,supports,strength,label,label2='المصدر الثاني',latin=True,arabic=False,ltr=True):
    q=clean_ar(x['quote']) if arabic else x['quote']
    ot=('«'+q+'»') if arabic else ('"'+q+'"')
    links=[link(x['url'],label)]
    if x.get('url2'): links.append(link(x['url2'],label2))
    sup_names={'7':'سن السابعة','9':'سن التاسعة','childhood_ends_at_puberty':'انتهاء الطفولة بالبلوغ','shared_parenting':'الرعاية المشتركة','silat_al_rahim':'صلة الرحم'}
    str_names={'explicit_7':'نص في السابعة','explicit_9':'نص في التاسعة','explicit':'دلالة صريحة','indirect':'دلالة بالاستنباط'}
    chips=[['str',str_names[strength]]]+[['sup',sup_names[s]] for s in supports]
    C.append(dict(id=id,sec=sec,icon=icon,supports=supports,strength=strength,jurisdiction=clean_ar(x['jurisdiction']),title=title,
        ot=ot,ltr=(not arabic) and ltr,tt=('' if arabic else '«'+clean_ar(x['quote_ar'])+'»'),
        src=dict(author=clean_ar(x['author']) if arabic else x['author'],year=str(x['year'])[:40] if not arabic else '',jur=clean_ar(x['jurisdiction']),
                 title_latin=('' if arabic else x['title_latin']),sw=(clean_ar(x['title_latin'])+' · '+clean_ar(x['location'])) if arabic else '',
                 where=('' if arabic else x['where'][:160]),latin=not arabic),
        about=clean_ar(x['about']),level=clean_ar(x['level']),links=links,arg=clean_ar(x['argument']),chips=chips,fam=('fiqh' if arabic else 'west')))
# ---------- Egypt: Dar al-Ifta fatwas ----------
card(EG['eg_bakhit_1917_art391'],'A1-056','eg','eg','فتوى مفتي الديار المصرية محمد بخيت 1917 — المادة 391: الغلام إلى أبيه في السابعة والصبية في التاسعة',['7','9'],'explicit_7','الفتوى في مصدرها',arabic=True)
card(EG['eg_bakhit_1918_reasoning'],'A1-057','eg','eg','فتوى محمد بخيت 1918 — علة انتهاء الحضانة: الغلام يحتاج الإعداد والتعليم، والصبية الحفظ والصيانة، والأب أقدر',['7','9'],'explicit_7','الفتوى في مصدرها',arabic=True)
card(EG['eg_bakhit_1915_boy9_to_father'],'A1-058','eg','eg','فتوى محمد بخيت 1915 — من بلغ تسعا انتهت حضانته فيضمه أبوه، ولا تنقل الحاضنة المحضون إلا بإذن أبيه',['7'],'explicit','الفتوى في مصدرها',arabic=True)
card(EG['eg_nawawi_1896_girl9'],'A1-059','eg','eg','فتوى مفتي الديار المصرية حسونة النواوي 1896 — حضانة البنت تستمر حتى تكمل تسع سنين',['9'],'explicit_9','الفتوى في مصدرها',arabic=True)
card(EG['eg_abduh_1900_father_daily_sight'],'A4-070','eg','eg','فتوى الإمام محمد عبده 1900 — تجبر الحاضنة على العودة بالولد حيث يطالعه أبوه، حفظا لحق الأب',['silat_al_rahim'],'explicit','الفتوى في مصدرها',arabic=True)
card(EG['eg_bakhit_1916_boy7_agnates'],'A1-060','eg','eg','فتوى محمد بخيت 1916 — إذا بلغ الغلام سبعا سلم إلى العصبة ويقدم الأب',['7'],'explicit_7','الفتوى في مصدرها',arabic=True)
card(EG['eg_haridi_1967_7_9'],'A1-061','eg','eg','فتوى مفتي الجمهورية أحمد هريدي 1967 — حق النساء في الحضانة محدد بسبع للصغير وتسع للصغيرة',['7','9'],'explicit_7','الفتوى في مصدرها',arabic=True)
# ---------- Muslim-law courts (India) ----------
card(CO['in_ap_hc_1983_jameel_ahmed_ansari_boy_after_7_to_father'],'A5-189','court','in','محكمة أندرا براديش العليا 1982 — في الشريعة الإسلامية: بعد السابعة الأب هو المستحق لحضانة الولد',['7'],'explicit_7','نص الحكم')
card(CO['in_bombay_hc_2007_sabdarali_boy_over_7_to_father_younger_to_mother'],'A5-190','court','in','محكمة بومباي العليا 2007 — حضانة الذكر فوق السابعة تعطى للأب، ورغبة الصغير ليست حاسمة',['7'],'explicit_7','نص الحكم')
card(CO['in_telangana_hc_2024_khusro_father_natural_guardian_rule_after_7'],'A5-191','court','in','محكمة تلنكانا العليا 2024 — تقرير القاعدة: الأب مستحق الحضانة بعد السابعة وهو الولي الطبيعي',['7'],'explicit_7','نص الحكم')
card(CO['in_madras_hc_1951_zynab_bi_hedaya_rationale_seven'],'A5-192','court','in','محكمة مدراس العليا 1951 — حضانة الأم للذكر تنتهي بتمام السابعة لاستغنائه، ثم يحتاج التعليم',['7'],'explicit_7','نص الحكم')
# ---------- fiqh: al-ithghar / tamyiz ----------
card(FQ['mughni_malik_hatta_yuthghir'],'A1-062','f5','hanbali','المغني — إذا بلغ الغلام سبعا خير، والأب أحق به عند أبي حنيفة إذا استقل، والأم حتى يثغر في رواية عن مالك',['7'],'explicit_7','النص في مصدره',arabic=True)
card(FQ['kashshaf_sab_awwal_hal_salah'],'A1-063','f5','hanbali','كشاف القناع — قيد بالسبع لأنها أول حال أمر الشرع فيها بمخاطبته بالصلاة',['7'],'explicit_7','النص في مصدره',arabic=True)
card(FQ['tuhfa_sab_sinn_tamyiz_salah'],'A1-064','f6','heritage','تحفة المودود — إذا صار له سبع سنين دخل في سن التمييز وأمر بالصلاة',['7'],'explicit_7','النص في مصدره',arabic=True)
card(FQ['lisan_ithghar_salah_nakhai'],'A3-009','f6','heritage','لسان العرب — كانوا يحبون أن يعلموا الصبي الصلاة إذا اثغر: الإثغار سقوط الأسنان ونباتها',['7'],'explicit','النص في مصدره','النهاية لابن الأثير',arabic=True)
# ---------- harm ----------
card(HA['comanor-phillips-2002-father-presence-delinquency'],'A4-071','harm','us','كومانور وفيليبس 2002 — وجود الأب في البيت أهم عامل في وقاية الولد من الجنوح، والدخل أقل أثرا',['silat_al_rahim'],'explicit','صفحة الدراسة')
card(HA['antecol-bedard-2007-years-with-father'],'A4-072','harm','us','أنتيكول وبيدار 2007 — كل خمس سنين إضافية مع الأب تخفض التدخين والمخدرات والإدانات',['silat_al_rahim'],'explicit','صفحة الدراسة')
card(HA['bramlett-blumberg-2007-nsch-family-structure-health'],'A4-073','harm','us','دراسة المسح الوطني لصحة الأطفال 2007 — أطفال الأسر بلا أب أسوأ صحة، وأسر الآباء المنفردين كالأسر المجتمعة',['silat_al_rahim','shared_parenting'],'explicit','صفحة الدراسة')
card(HA['makikyro-1998-finland-1966-psychiatric-single-parent'],'A4-074','harm','fi','دراسة مواليد شمال فنلندا 1998 — الحرمان من الأب قبل الرابعة عشرة يضاعف اضطرابات الشخصية في الرشد',['silat_al_rahim'],'explicit','صفحة الدراسة')
card(HA['sauvola-2001-finland-1966-mortality-single-parent'],'A4-075','harm','fi','دراسة مواليد شمال فنلندا 2001 — النشأة بلا أحد الوالدين ترفع وفيات الرجال وانتحارهم',['silat_al_rahim'],'explicit','صفحة الدراسة')
card(HA['carlson-2006-father-involvement-mediates-absence'],'A4-076','harm','us','كارلسون 2006 — انخراط الأب يفسر جانبا كبيرا من ضرر غيابه، وأنفعه حين يعيش مع ولده',['silat_al_rahim','shared_parenting'],'explicit','صفحة الدراسة')
card(HA['flouri-buchanan-2002-father-involvement-police'],'A4-077','harm','uk','فلوري وبوكانان 2002 — انخراط الأب في سن السابعة يقي الأولاد من مشاكل الشرطة في المراهقة',['7','silat_al_rahim'],'explicit','صفحة الدراسة')
card(HA['webster-2014-meta-analysis-father-absence-menarche'],'A4-078','harm','world','تحليل جامع لـ33 دراسة 2014 — غياب الأب يبكر حيض البنات',['childhood_ends_at_puberty','silat_al_rahim'],'explicit','صفحة الدراسة')
# ---------- statistics (Spain INE) ----------
card(ST['ine_spain_ensd2025_shared_custody_majority'],'A5-193','soc','es','الإحصاء الإسباني الرسمي 2025 — الحضانة المشتركة في أكثر من نصف حالات الطلاق: 50.8%',['shared_parenting'],'explicit','البيان الرسمي')
card(ST['ine_spain_ensd2023_shared_overtakes_mother'],'A5-194','soc','es','الإحصاء الإسباني الرسمي 2023 — لأول مرة تتقدم الحضانة المشتركة على حضانة الأم',['shared_parenting'],'explicit','البيان الرسمي','بيان 2024')
card(ST['ine_spain_2010_baseline_to_2025'],'A5-195','soc','es','الإحصاء الإسباني الرسمي 2010 — الحضانة المشتركة 10.5% فقط، فتضاعفت خمس مرات في خمس عشرة سنة',['shared_parenting'],'explicit','البيان الرسمي','بيان 2014')
card(ST['ine_spain_regional_2025_shared_majority'],'A5-196','soc','es','الإحصاء الإسباني الرسمي 2025 — الحضانة المشتركة أغلبية في تسعة أقاليم: كتالونيا 63%',['shared_parenting'],'explicit','جدول الإحصاء الرسمي')
# ---------- corrections ----------
PIAGET=dict(id='A2-008',sec='psy',icon='ch',supports=['7'],strength='explicit_7',jurisdiction='سويسرا — جامعة جنيف',
 title='بياجيه — سن السابعة إلى الثامنة نقطة تحول حاسمة في نمو العقل',
 ot='"The age of seven to eight years, on average, marks a decisive turning point in the development …"',
 tt='«سن السابعة إلى الثامنة، في المتوسط، يمثل نقطة تحول حاسمة في النمو …» [بدء مرحلة العمليات المحسوسة: التفكير المنطقي المنظم].',
 src=dict(author='Piaget J',year='1972',jur='سويسرا — جامعة جنيف',title_latin='The Principles of Genetic Epistemology (trans. W. Mays; L\'épistémologie génétique, 1970)',where='London: Routledge & Kegan Paul, 1972 — ch. 1: «The stage of concrete operations»'),
 about='جان بياجيه (1896–1980) عالم النفس السويسري في جامعة جنيف، مؤسس نظرية النمو المعرفي وأكثر علماء النفس أثرا في فهم عقل الطفل؛ والكتاب خلاصة نظريته كتبها بنفسه في آخر عمره.',level='نظرية علمية مؤسسة',
 links=[dict(url='https://archive.org/details/principlesofgene0000piag',label='الكتاب في مصدره',site='أرشيف الإنترنت',domain='archive.org')],
 arg='بياجيه نفسه يجعل السابعة «نقطة تحول حاسمة» في نمو العقل: فيها يبدأ التفكير المنطقي المنظم ويخرج الطفل من التمركز حول ذاته؛ وهذا هو التمييز الذي علق عليه الفقهاء انتهاء حضانة النساء.',
 chips=[['str','نص في السابعة'],['sup','سن السابعة']])
C.append(PIAGET)
json.dump(C,open('/home/claude/work/new7.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print(len(C))
