# -*- coding: utf-8 -*-
# v1.26.0: stepfather risk, psychological maltreatment, denigration, ECHR diligence, net-income maintenance, Quran on no-harm and capacity
import json,copy
P='/home/claude/work/new_cards.json'
N=json.load(open(P,encoding='utf8')); N=[x for x in N if not x.get('v126')]
tw=[x for x in N if x['id']=='A4-071'][0]; tf=[x for x in N if x['id']=='A1-065'][0]
def mk(cid,sec,icon,sup,strength,title,author,year,title_latin,where,jur,level,about,ot,tt,arg,links,chips):
    e=copy.deepcopy(tw)
    e.update(id=cid,sec=sec,icon=icon,supports=sup,strength=strength,jurisdiction=jur,title=title,ot=ot,ltr=True,tt=tt,about=about,level=level,arg=arg,chips=chips,v126=True,fam='west')
    e['src']=dict(author=author,year=str(year),jur=jur,title_latin=title_latin,sw='',where=where,latin=True)
    e['links']=[dict(url=u,label=l,site=s,domain=u.split('/')[2]) for u,l,s in links]
    return e
def fq(cid,sec,icon,sup,strength,title,author,sw,jur,level,about,ot,arg,links,chips):
    e=copy.deepcopy(tf); e.pop('mahdi',None)
    e.update(id=cid,sec=sec,icon=icon,supports=sup,strength=strength,jurisdiction=jur,title=title,ot=ot,ltr=False,tt='',about=about,level=level,arg=arg,chips=chips,v126=True,fam='fiqh')
    e['src']=dict(author=author,year='',jur=jur,title_latin='',sw=sw,where='',latin=False)
    e['links']=[dict(url=u,label=l,site=s,domain=u.split('/')[2]) for u,l,s in links]
    return e
HARM=[['str','دلالة صريحة'],['sup','صلة الرحم']]
C=[
fq('A1-116','f2','hanafi',['silat_al_rahim'],'explicit','الهداية — زوج الأم الأجنبي «يعطيه نزرا وينظر إليه شزرا»: تسقط حضانتها',
 'برهان الدين المرغيناني (ت 593هـ) — الفقه الحنفي','الهداية في شرح بداية المبتدي، كتاب الطلاق، باب حضانة الولد ومن أحق به، ج2 ص283 (دار إحياء التراث العربي، بيروت)',
 'المذهب الحنفي','متن معتمد في المذهب الحنفي',
 'الهداية للمرغيناني أعمدة كتب الفقه الحنفي، وعليها شروح المذهب الكبرى كفتح القدير والعناية والبناية، وهي المرجع الأول لقضاء الأحوال الشخصية في مصر منذ قرون.',
 '«ومن نكحت غير محرم [للصغير] سقط حقها [في الحضانة] لما روينا، ولأن زوج الأم إذا كان أجنبيا [عن الصغير] يعطيه نزرا [أي قليلا] وينظر إليه شزرا [أي بعين البغض] فلا نظر [أي لا مصلحة للصغير في بقائه عنده]»',
 'الفقه الحنفي يسقط حضانة الأم إذا تزوجت أجنبيا عن الطفل، وعلته خطر زوج الأم على الصغير: يقلل عطاءه وينظر إليه ببغض. وقد صدقت هذا التعليل دراسات القرن العشرين في خطر زوج الأم على الأطفال.',
 [('https://shamela.ws/book/11820/377','النص في مصدره','المكتبة الشاملة')],[['str','دلالة صريحة'],['sup','مصلحة الطفل']]),
mk('A4-114','harm','ca',['silat_al_rahim'],'explicit','دالي وويلسون — زوج الأم يقتل الأطفال الصغار ضربا بمعدل يزيد على 100 ضعف الأب',
 'Martin Daly & Margo Wilson','2001','The "Cinderella effect": Elevated mistreatment of stepchildren in comparison to those living with genetic parents','Annales Zoologici Fennici 38: 287–296; Center for Evolutionary Psychology, UC Santa Barbara',
 'كندا — جامعة ماكماستر','بحوث محكمة على سجلات رسمية في عدة دول',
 'مارتن دالي ومارغو ويلسون من جامعة ماكماستر الكندية، أشهر من درس خطر زوج الأم على الطفل، على سجلات الشرطة والوفيات الرسمية في كندا وإنجلترا وأستراليا والولايات المتحدة.',
 '"... more than 100 times higher than the corresponding rates for genetic parents ... the corresponding rate for stepfathers was over 120 times greater ..."',
 '«... [معدل قتل الأطفال الصغار ضربا على أيدي أزواج الأمهات وزوجات الآباء] أعلى بأكثر من 100 ضعف من المعدلات المقابلة عند الآباء والأمهات الحقيقيين ... [وفي كندا] كان المعدل المقابل عند أزواج الأمهات أكبر بأكثر من 120 ضعفا ...»',
 'الطفل الذي يقطع عن أبيه ويعيش مع زوج أمه في خطر يزيد على مئة ضعف؛ وهذا ما قاله فقهاء الحنفية قبل ثمانية قرون: زوج الأم «يعطيه نزرا وينظر إليه شزرا».',
 [('https://cep.ucsb.edu/wp-content/uploads/2023/05/cinderella-effect-facts.pdf','نص البحث','مركز علم النفس التطوري، جامعة كاليفورنيا')],HARM),
mk('A4-115','harm','us',['silat_al_rahim'],'explicit','مجلة طب الأطفال الأمريكية 2002 — وجود رجل غريب في بيت الطفل يضاعف خطر موته بالإيذاء 8 مرات',
 'Stiffman MN, Schnitzer PG, Adam P, Kruse RL, Ewigman BG','2002','Household composition and risk of fatal child maltreatment','Pediatrics 109(4): 615',
 'الولايات المتحدة — جامعة ميزوري','دراسة محكمة في مجلة الأكاديمية الأمريكية لطب الأطفال',
 'مجلة «طب الأطفال» هي المجلة الرسمية للأكاديمية الأمريكية لطب الأطفال، وأعلى مجلات طب الأطفال في العالم.',
 '"Children residing in households with adults unrelated to them were 8 times more likely to die of maltreatment than children in households with 2 biological parents ... Children living in households with 1 or more male adults that are not related to them are at increased risk for maltreatment injury death."',
 '«الأطفال الذين يقيمون في بيوت فيها بالغون لا قرابة لهم بهم أكثر عرضة للموت بالإيذاء 8 مرات من الأطفال في بيوت فيها الأبوان الحقيقيان ... والأطفال الذين يعيشون في بيوت فيها رجل بالغ أو أكثر لا قرابة له بهم في خطر أكبر من الموت بإصابات الإيذاء.»',
 'أعلى مجلة لطب الأطفال في العالم: وجود رجل غريب عن الطفل في بيته، كزوج الأم، يرفع خطر موته بالإيذاء ثمانية أضعاف. فإبعاد الطفل عن أبيه وتركه مع زوج أمه تعريض له للخطر.',
 [('https://doi.org/10.1542/peds.109.4.615','البحث في المجلة','مجلة طب الأطفال'),('https://www.healthpartners.com/knowledgeexchange/display/document-rn18442','ملخص البحث','HealthPartners')],HARM),
mk('A4-116','harm','us',['silat_al_rahim'],'explicit','راسل 1984 — البنات اللاتي ربين مع زوج الأم تعرض 17% منهن للاعتداء منه، مقابل 2% مع الأب',
 'Diana E. H. Russell','1984','The prevalence and seriousness of incestuous abuse: Stepfathers vs. biological fathers','Child Abuse & Neglect 8(1): 15–22',
 'الولايات المتحدة — عينة احتمالية من 930 امرأة في سان فرانسيسكو','دراسة محكمة على عينة احتمالية',
 'ديانا راسل باحثة اجتماعية أمريكية، ودراستها منشورة في مجلة «إيذاء الأطفال وإهمالهم» المحكمة، ومسجلة في المكتبة الوطنية للعدالة الجنائية الأمريكية.',
 '"Seventeen percent of the women who had stepfathers in their childhoods had been sexually abused ..."',
 '«17% من النساء اللاتي كان لهن زوج أم في طفولتهن تعرضن للاعتداء الجنسي ...»',
 'والنسبة عند من ربين مع آبائهن 2% كما في ملخص البحث؛ فخطر زوج الأم على البنت أضعاف خطر الأب عليها؛ فإبعاد البنت عن أبيها وتركها في بيت زوج أمها ترك لها في أخطر المواضع، وهو ما احتاط له الفقهاء بإسقاط حضانة الأم إذا تزوجت أجنبيا.',
 [('https://ojp.gov/ncjrs/virtual-library/abstracts/prevalence-and-seriousness-incestuous-abuse-stepfathers-vs','ملخص البحث','المكتبة الوطنية للعدالة الجنائية الأمريكية')],HARM),
mk('A5-212','intl','un',['silat_al_rahim'],'explicit','لجنة حقوق الطفل الأممية، التعليق العام 13 — تخويف الطفل وترويعه وعزله عنف نفسي',
 'UN Committee on the Rights of the Child','2011','General Comment No. 13: The right of the child to freedom from all forms of violence','CRC/C/GC/13, paragraph 21',
 'الأمم المتحدة — لجنة حقوق الطفل','تفسير رسمي لهيئة أممية',
 'لجنة حقوق الطفل هي الهيئة الأممية المختصة بتفسير اتفاقية حقوق الطفل ومتابعة تطبيقها في الدول الأعضاء.',
 '"Mental violence ... is often described as psychological maltreatment ... and may include: (a) All forms of persistent harmful interactions with the child ... (b) Scaring, terrorizing and threatening; exploiting and corrupting; spurning and rejecting; isolating, ignoring and favouritism ..."',
 '«العنف النفسي ... كثيرا ما يوصف بالإيذاء النفسي ... وقد يشمل: (أ) كل صور التعامل المؤذي المستمر مع الطفل ... (ب) تخويفه وترويعه وتهديده، واستغلاله وإفساده، وصده ونبذه، وعزله وتجاهله والتمييز بينه وبين غيره ...»',
 'الأمم المتحدة نفسها تعد تخويف الطفل وترويعه وعزله عنفا نفسيا؛ فمن يخوف الطفل من أبيه ويوهمه أنه يريد أذاه، ويعزله عنه، يقع في العنف النفسي الذي تحظره الاتفاقية.',
 [('https://hrlibrary.umn.edu/crc/gencom13.html','نص التعليق العام','مكتبة حقوق الإنسان، جامعة مينيسوتا')],HARM),
mk('A2-114','psy','us',['silat_al_rahim','shared_parenting'],'explicit','روين وإيمري 2014 — تشويه الوالد صورة الآخر عند الولد يضر الولد ويرتد على المشوه',
 'Jenna Rowen & Robert E. Emery','2014','Examining parental denigration behaviors of co-parents as reported by young adults and their association with parent–child closeness','Couple and Family Psychology: Research and Practice, 2014',
 'الولايات المتحدة — جامعة فرجينيا','دراسة محكمة في مجلة الجمعية الأمريكية لعلم النفس',
 'روبرت إيمري أستاذ علم النفس ومدير مركز الأطفال والأسر والقانون في جامعة فرجينيا، ومن أشهر الباحثين في الطلاق والأطفال.',
 '"... denigration clearly is more strongly related to emotional distance in children\'s relationship with the parent who does the denigrating ..."',
 '«... تشويه أحد الوالدين صورة الآخر يرتبط ارتباطا أقوى بالبعد العاطفي في علاقة الأولاد بالوالد الذي يشوه ...»',
 'تحريض الطفل على أبيه وسبه أمامه يفسد علاقة الطفل بوالديه كليهما، ويرتد على من يحرض؛ فالخاسر الأول هو الطفل.',
 [('https://www.family-institute.org/sites/default/files/pdfs/csi_rowan_talking_badly_about_your_coparent.pdf','عرض البحث','معهد الأسرة بجامعة نورث وسترن')],HARM),
mk('A5-213','court','eu',['silat_al_rahim'],'explicit','المحكمة الأوروبية لحقوق الإنسان 2019 — الدولة ملزمة باليقظة الاستثنائية لحفظ صلة الطفل بوالده',
 'European Court of Human Rights','2019','Pisică v. the Republic of Moldova, no. 23641/17, 29 October 2019','§§ 63, 66',
 'أوروبا — المحكمة الأوروبية لحقوق الإنسان','حكم قضائي نهائي',
 'المحكمة الأوروبية لحقوق الإنسان تفصل في التزام 46 دولة بالاتفاقية الأوروبية، وأحكامها ملزمة لها.',
 '"... the State has in principle an obligation to take measures with a view to reuniting parents with their children ... there is a duty to exercise exceptional diligence, in view of the risk that the passage of time may result in a de facto determination of the matter ..."',
 '«... على الدولة من حيث المبدأ التزام باتخاذ التدابير لجمع الوالدين بأولادهم ... وعليها واجب اليقظة الاستثنائية، لخطر أن يحسم مرور الوقت المسألة بالأمر الواقع ...»',
 'القضاء الأوروبي يلزم الدولة بالعمل الجاد السريع لجمع الطفل بالوالد الذي لا يعيش معه، لأن مرور الوقت مع القطيعة يحسم الأمر بالأمر الواقع ضد الطفل.',
 [('https://www.iri.edu.ar/wp-content/uploads/2019/12/ri57SGJurisprudencia7lCASO-DE-PISIC%C4%82-v.-LA-REPUBLICA-DE-MOLDOVA.pdf','نص الحكم','معهد العلاقات الدولية، جامعة لا بلاتا')],[['str','دلالة صريحة'],['sup','صلة الرحم']]),
mk('A5-214','law','de',['shared_parenting'],'explicit','جدول دوسلدورف الألماني 2025 — النفقة تحسب على صافي دخل الأب، ويحفظ له ما يعيش به',
 'Oberlandesgericht Düsseldorf','2025','Düsseldorfer Tabelle (Stand: 1. Januar 2025)','Tabelle; Anmerkung A. VII',
 'ألمانيا — محكمة الاستئناف العليا في دوسلدورف','معيار قضائي معتمد في كل محاكم ألمانيا',
 'جدول دوسلدورف تصدره محكمة الاستئناف العليا في دوسلدورف، وتعمل به محاكم ألمانيا كلها في تقدير نفقة الأولاد، وينشره موقع وزارة العدل في ولاية شمال الراين.',
 '"Nettoeinkommen des/der Barunterhaltspflichtigen ... [Notwendiger Eigenbedarf] für den erwerbstätigen Unterhaltspflichtigen monatlich 1.450 EUR."',
 '«صافي دخل الملزم بالنفقة ... [والحد الأدنى المحفوظ له] للملزم الذي يعمل: 1450 يورو في الشهر.»',
 'ألمانيا تقدر نفقة الأولاد على صافي دخل الأب لا على مجموع ما يقبضه، وتحفظ له ما يعيش به لا يمس؛ وهو معنى قوله تعالى: ﴿لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا مَا آتَاهَا﴾.',
 [('https://www.justiz.nrw/BS/broschueren_hilfen/dtabelle/duesseldorfer-tabelle-2025','الجدول الرسمي','وزارة العدل في شمال الراين'),('https://familienportal.nrw/sites/default/files/2024-12/Duesseldorfer-Tabelle-01_01_2025.pdf','الجدول بصيغة PDF','بوابة الأسرة في شمال الراين')],[['str','دلالة صريحة'],['sup','العدل في النفقة']]),
fq('A4-117','f1','quran',['silat_al_rahim'],'explicit','سورة البقرة 233 — لا يضار الأب بولده ولا الأم بولدها',
 'القرآن الكريم','سورة البقرة، الآية 233','القرآن الكريم','نص قطعي',
 'آية الرضاعة في سورة البقرة، وفيها أحكام الولد بعد الفرقة: الرضاع والنفقة والتشاور بين الأبوين.',
 '﴿لَا تُضَارَّ وَالِدَةٌ بِوَلَدِهَا وَلَا مَوْلُودٌ لَهُ بِوَلَدِهِ﴾',
 'القرآن يحرم أن يتخذ الولد وسيلة للإضرار بأحد أبويه؛ و«المولود له» هو الأب. فقطع الولد عن أبيه، وتحريضه عليه، وحرمانه من رعايته، إضرار بالأب بولده نهى الله عنه نصا.',
 [('https://quran.com/2/233','الآية في المصحف','القرآن الكريم')],[['str','دلالة صريحة'],['sup','صلة الرحم']]),
fq('A4-118','f1','quran',['shared_parenting'],'explicit','سورة الطلاق 7 — النفقة على قدر الطاقة',
 'القرآن الكريم','سورة الطلاق، الآية 7','القرآن الكريم','نص قطعي',
 'الآية في سورة الطلاق، وهي أصل تقدير النفقة بعد الفرقة.',
 '﴿لِيُنفِقْ ذُو سَعَةٍ مِّن سَعَتِهِ ۖ وَمَن قُدِرَ عَلَيْهِ رِزْقُهُ فَلْيُنفِقْ مِمَّا آتَاهُ اللَّهُ ۚ لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا مَا آتَاهَا﴾',
 'النفقة على قدر ما في يد الأب فعلا، لا على ما يكتب في كشف راتبه قبل الاستقطاع؛ ولا يكلف فوق طاقته.',
 [('https://quran.com/65/7','الآية في المصحف','القرآن الكريم')],[['str','دلالة صريحة'],['sup','العدل في النفقة']]),
]
N+=C
json.dump(N,open(P,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('added',len(C))
