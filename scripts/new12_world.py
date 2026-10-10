# -*- coding: utf-8 -*-
# v1.25.0: new sections (tamyiz, school, body) + soc/study/intl additions
import json,copy
P='/home/claude/work/new_cards.json'
N=json.load(open(P,encoding='utf8')); N=[x for x in N if not x.get('v125')]
tpl=[x for x in N if x['id']=='A4-071'][0]
def mk(cid,sec,icon,sup,strength,title,author,year,title_latin,where,jur,level,about,ot,tt,arg,links,chips):
    e=copy.deepcopy(tpl)
    e.update(id=cid,sec=sec,icon=icon,supports=sup,strength=strength,jurisdiction=jur,title=title,ot=ot,ltr=True,tt=tt,about=about,level=level,arg=arg,chips=chips,v125=True,fam='west')
    e['src']=dict(author=author,year=str(year),jur=jur,title_latin=title_latin,sw='',where=where,latin=True)
    e['links']=[dict(url=u,label=l,site=s,domain=u.split('/')[2]) for u,l,s in links]
    return e
S7=[['str hot','نص في السابعة'],['sup','سن السابعة']]
SR=[['str','دلالة صريحة'],['sup','صلة الرحم']]
SP=[['str','دلالة صريحة'],['sup','الرعاية المشتركة']]
C=[
# ---- tamyiz
mk('A1-110','tamyiz','de',['7'],'explicit_7','القانون المدني الألماني، المادة 104 — من لم يتم سبع سنين عديم الأهلية',
 'Bürgerliches Gesetzbuch (BGB)','1896/2002','§ 104 Geschäftsunfähigkeit','BGB § 104 Nr. 1','ألمانيا — القانون المدني الاتحادي','تشريع اتحادي نافذ',
 'القانون المدني الألماني نافذ منذ سنة 1900، وهو من أعمدة القوانين المدنية في العالم، وينشر نصه الرسمي على موقع وزارة العدل الاتحادية.',
 '"Geschäftsunfähig ist: 1. wer nicht das siebente Lebensjahr vollendet hat, ..."','«عديم الأهلية: 1. من لم يتم السنة السابعة من عمره ...»',
 'أكبر دول أوروبا تجعل تمام السابعة حدا قانونيا يبدأ عنده اعتبار تصرفات الطفل؛ فالسابعة ليست «فقها قديما»، بل حد يعمل به القانون الحديث.',
 [('https://www.gesetze-im-internet.de/bgb/__104.html','النص الرسمي للمادة','وزارة العدل الألمانية'),('https://bgb.kommentar.de/Geschaeftsunfaehigkeit','نص المادة وشرحها','شرح القانون المدني الألماني')],S7),
mk('A1-111','tamyiz','de',['7'],'explicit_7','القانون المدني الألماني، المادة 828 — من لم يتم سبع سنين لا يسأل عن ضرر يحدثه',
 'Bürgerliches Gesetzbuch (BGB)','1896/2002','§ 828 Minderjährige','BGB § 828 Abs. 1','ألمانيا — القانون المدني الاتحادي','تشريع اتحادي نافذ',
 'القانون المدني الألماني نافذ منذ سنة 1900، وينشر نصه الرسمي على موقع وزارة العدل الاتحادية.',
 '"Wer nicht das siebente Lebensjahr vollendet hat, ist für einen Schaden, den er einem anderen zufügt, nicht verantwortlich."',
 '«من لم يتم السنة السابعة من عمره لا يسأل عن ضرر يحدثه بغيره.»',
 'القانون الألماني يجعل تمام السابعة بداية مسؤولية الطفل عن أفعاله؛ وهو ما سماه الفقهاء التمييز، وعنده تنتهي حضانة النساء ويبدأ التأديب والتعليم.',
 [('https://www.gesetze-im-internet.de/bgb/__828.html','النص الرسمي للمادة','وزارة العدل الألمانية'),('https://gesetze.legal/bund/bgb/828','نص المادة','gesetze.legal')],S7),
mk('A1-112','tamyiz','pk',['7'],'explicit_7','قانون العقوبات الباكستاني، المادة 82 — لا جريمة على طفل دون السابعة',
 'Pakistan Penal Code (Act XLV of 1860)','1860','Section 82 — Act of a child under seven years of age','PPC s. 82','باكستان — قانون العقوبات النافذ','تشريع نافذ',
 'قانون العقوبات الباكستاني نافذ في أكبر بلد إسلامي في جنوب آسيا، والمادة 82 منه في باب الاستثناءات العامة.',
 '"Nothing is an offence, which is done by a child under seven years of age."','«لا يعد جريمة ما يفعله طفل دون السابعة من عمره.»',
 'دولة إسلامية كبرى تجعل السابعة حد التمييز في أخطر باب، وهو باب الجرائم؛ فالسابعة حد معتبر في قوانين المسلمين اليوم.',
 [('https://policehumanrightsresources.org/content/uploads/2016/07/Penal-Code-Pakistan-1860.pdf?x19059','نص القانون','مكتبة قوانين الشرطة وحقوق الإنسان')],S7),
mk('A1-113','tamyiz','ng',['7'],'explicit_7','القانون الجنائي النيجيري، المادة 30 — من لم يبلغ السابعة لا يسأل جنائيا',
 'Criminal Code Act (Nigeria)','1916/1990','Criminal Code, Part I, Chapter 5, section 30','s. 30','نيجيريا — القانون الجنائي النافذ','تشريع نافذ',
 'القانون الجنائي النيجيري نافذ في أكبر دولة إفريقية سكانا؛ والنص منقول في قاعدة بيانات جامعة نوتنغهام البريطانية لقوانين الدول.',
 '"A person under the age of seven years is not criminally responsible for any act or omission."','«من لم يبلغ السابعة من عمره لا يسأل جنائيا عن أي فعل أو امتناع.»',
 'أكبر دولة إفريقية تجعل السابعة حد المسؤولية الجنائية؛ فالسابعة حد يتفق عليه الفقه والقوانين في قارات العالم.',
 [('https://cjad.nottingham.ac.uk/en/state/100/keyword/566/','نص المادة','قاعدة بيانات جامعة نوتنغهام')],S7),
mk('A1-114','tamyiz','bd',['9'],'explicit_9','قانون العقوبات في بنغلاديش، المادة 82 — لا جريمة على طفل دون التاسعة',
 'The Penal Code, 1860 (Bangladesh)','1860','Section 82 — Act of a child under nine years of age','s. 82','بنغلاديش — قانون العقوبات النافذ','تشريع نافذ',
 'قانون العقوبات النافذ في بنغلاديش، وهي من أكبر الدول الإسلامية سكانا؛ والنص في قاعدة بيانات جامعة نوتنغهام.',
 '"Nothing is an offence which is done by a child under nine years of age."','«لا يعد جريمة ما يفعله طفل دون التاسعة من عمره.»',
 'دولة إسلامية كبرى تجعل التاسعة حدا للمسؤولية؛ والتاسعة هي الحد الذي جعله الفقهاء لانتهاء حضانة النساء للبنت.',
 [('https://cjad.nottingham.ac.uk/documents/implementations/pdf/Bangladesh-Penal_Code.pdf','نص القانون','قاعدة بيانات جامعة نوتنغهام')],[['str hot','نص في التاسعة'],['sup','سن التاسعة']]),
mk('A1-115','tamyiz','uk',['childhood_ends_at_puberty'],'explicit','قانون الأطفال والشباب في إنجلترا وويلز، المادة 50 — المسؤولية الجنائية تبدأ من العاشرة',
 'Children and Young Persons Act 1933','1933/1963','Section 50 — Age of criminal responsibility','s. 50','المملكة المتحدة — إنجلترا وويلز','تشريع نافذ',
 'قانون نافذ في إنجلترا وويلز منذ 1933، ونصه الرسمي على موقع التشريعات الحكومي البريطاني.',
 '"It shall be conclusively presumed that no child under the age of ten years can be guilty of any offence."',
 '«يفترض قطعا أن الطفل الذي لم يبلغ العاشرة لا يمكن أن يكون مذنبا بأي جريمة.»',
 'بريطانيا تحاسب ابن العاشرة جنائيا، فهو عندها ليس طفلا عاجزا يحتاج حضانة النساء؛ فمن يمد الحضانة سنين بعد ذلك يخالف حتى القوانين الغربية.',
 [('https://legislation.gov.uk/ukpga/Geo5/23-24/12/section/50','النص الرسمي','التشريعات البريطانية الرسمية')],[['str','دلالة صريحة'],['sup','انتهاء الطفولة بالبلوغ']]),
# ---- school
mk('A2-110','school','un',['7'],'explicit_7','اليونسكو — التصنيف الدولي للتعليم: سن دخول المدرسة الابتدائية بين 5 و7',
 'UNESCO Institute for Statistics','2011','International Standard Classification of Education: ISCED 2011','paragraph 122','الأمم المتحدة — اليونسكو','تعريف رسمي لهيئة أممية',
 'التصنيف الدولي للتعليم هو المعيار الرسمي الذي تعتمده اليونسكو ودول العالم في إحصاءات التعليم.',
 '"The customary or legal age of entry is usually not below 5 years old nor above 7 years old."',
 '«سن الالتحاق [بالتعليم الابتدائي] المعتاد أو القانوني لا يقل عادة عن 5 سنين ولا يزيد على 7 سنين.»',
 'العالم كله يخرج الطفل من البيت إلى المدرسة والتكليف بين الخامسة والسابعة؛ وهي سن التمييز التي جعلها الفقهاء حد انتقال الولد إلى أبيه للتعليم والتأديب.',
 [('https://unesdoc.unesco.org/ark:/48223/pf0000219109','النص الرسمي للتصنيف','المكتبة الرقمية لليونسكو')],S7),
mk('A2-111','school','us',['shared_parenting'],'explicit','وزارة التعليم الأمريكية 1997 — مشاركة الأب في المدرسة ترفع درجات الأولاد',
 'U.S. Department of Education, National Center for Education Statistics','1997','Fathers\' Involvement in Their Children\'s Schools — press release, October 2, 1997','NHES 1996 — 16,910 students','الولايات المتحدة — وزارة التعليم، المركز الوطني لإحصاءات التعليم','إحصاء رسمي للدولة',
 'دراسة رسمية للمركز الوطني لإحصاءات التعليم في وزارة التعليم الأمريكية، على مسح وطني لآباء نحو 17 ألف تلميذ.',
 '"... children in two-parent families where the father is are highly involved get better grades ... enjoy school more ... less likely to repeat a grade ... [in father-headed families children are] twice as likely to get mostly A\'s ..."',
 '«... الأطفال في الأسر ذات الوالدين الذين يشارك آباؤهم مشاركة عالية [في مدرستهم] يحصلون على درجات أفضل ... ويستمتعون بالمدرسة أكثر ... وأقل رسوبا ... [وفي الأسر التي يرعاها الأب] أكثر حصولا على أعلى الدرجات بمثلين ...»',
 'مشاركة الأب في تعليم ولده ترفع تحصيله؛ والتعليم هو العلة التي من أجلها جعل الفقهاء الولد عند أبيه بعد السابعة.',
 [('https://nces.ed.gov/pressrelease/father.asp','البيان الرسمي','وزارة التعليم الأمريكية'),('https://nces.ed.gov/pubs98/web/98121.asp','ملخص الدراسة','وزارة التعليم الأمريكية')],SP),
# ---- body
mk('A2-112','body','it',['7'],'explicit_7','ديل جوديتشي وزملاؤه — في السادسة إلى الثامنة يبدأ طور جديد في جسد الطفل',
 'Del Giudice M, Angeleri R, Manera V','2009/2011','The juvenile transition: A developmental switch point in human life history','Developmental Review 29 (2009): 1–31','إيطاليا — جامعة تورينو، مركز العلوم المعرفية','مراجعة علمية محكمة',
 'ماركو ديل جوديتشي من أبرز علماء تاريخ الحياة البشرية في علم النفس التطوري، والبحث من مركز العلوم المعرفية بجامعة تورينو، ومنشور في مجلة المراجعة النمائية ومراجع دار سبرينغر.',
 '"From the biological standpoint human juvenility begins with the endocrine events of adrenarche ... At about 6–8 years, with little difference between the sexes but substantial individual variation in timing, the cortex of the adrenal glands begins to secrete increasing quantities of androgens ..."',
 '«من الناحية الحيوية يبدأ طور اليفاعة عند الإنسان بأحداث غددية [هي نضج الغدة الكظرية] ... ففي نحو السادسة إلى الثامنة، بفارق قليل بين الذكور والإناث، تبدأ قشرة الغدة الكظرية إفراز كميات متزايدة من الهرمونات ...»',
 'جسد الطفل نفسه يعلن نهاية الطفولة الأولى بين السادسة والثامنة؛ فالسابعة حد في الأحياء كما هي حد في الفقه.',
 [('https://iris.unito.it/bitstream/2318/126112/1/DelGiudice_etal_JT.pdf','نص البحث','مستودع جامعة تورينو'),('https://iris.unito.it/bitstream/2318/132069/1/dev_rev.pdf','البحث الأصلي 2009','مستودع جامعة تورينو')],S7),
mk('A2-113','body','it',['7'],'explicit_7','ديل جوديتشي وزملاؤه — في السادسة والسابعة يستقل الطفل بطعامه، ويقفز ضبطه لنفسه',
 'Del Giudice M, Angeleri R, Manera V','2011','Juvenility and the Juvenile Transition','Springer reference entry, p. 1533','إيطاليا — جامعة تورينو، مركز العلوم المعرفية','مراجعة علمية محكمة',
 'ماركو ديل جوديتشي من أبرز علماء تاريخ الحياة البشرية في علم النفس التطوري، والبحث من مركز العلوم المعرفية بجامعة تورينو.',
 '"In humans, children become relatively able to feed themselves ... at about 6–7 years of age. ... In the psychological domain, the beginning of juvenility witnesses dramatic increases in self-control, emotional and attentional regulation, and executive functions in general, which collectively go under the label of “the 5- to 7-years shift”."',
 '«يصير الأطفال قادرين نسبيا على إطعام أنفسهم ... في نحو السادسة والسابعة من العمر. ... وفي الجانب النفسي يشهد أول طور اليفاعة زيادات كبيرة في ضبط النفس وتنظيم الانفعال والانتباه والوظائف التنفيذية عموما، وهو ما يسمى مجتمعا «تحول الخامسة إلى السابعة».»',
 'الاستغناء الذي جعله الفقهاء علة انتهاء حضانة النساء يثبته العلم في السادسة والسابعة: يأكل الطفل وحده، ويضبط نفسه وانتباهه.',
 [('https://iris.unito.it/bitstream/2318/126112/1/DelGiudice_etal_JT.pdf','نص البحث','مستودع جامعة تورينو')],S7),
# ---- soc
mk('A4-110','soc','us',['shared_parenting'],'explicit','راج تشيتي وزملاؤه، هارفارد وبيركلي 2014 — بنية الأسرة أقوى ما يتنبأ بارتقاء الأبناء',
 'Chetty R, Hendren N, Kline P, Saez E','2014','Where is the Land of Opportunity? The Geography of Intergenerational Mobility in the United States','Quarterly Journal of Economics 129(4) — Executive Summary, January 2014','الولايات المتحدة — جامعة هارفارد وجامعة كاليفورنيا في بيركلي','دراسة سجلات وطنية',
 'راج تشيتي أستاذ الاقتصاد بجامعة هارفارد ومن أشهر اقتصاديي العالم، والدراسة على سجلات ضرائب أكثر من 40 مليون أمريكي ومنشورة في المجلة الفصلية للاقتصاد.',
 '"Finally, the strongest predictors of upward mobility are measures of family structure such as the fraction of single parents in the area. ... Children of married parents also have higher rates of upward mobility if they live in communities with fewer single parents."',
 '«وأخيرا فإن أقوى ما يتنبأ بارتقاء الأبناء [في السلم الاجتماعي] مقاييس بنية الأسرة، مثل نسبة الأسر ذات الوالد الواحد في المنطقة ... وحتى أبناء الوالدين المتزوجين يرتقون أكثر إذا عاشوا في مجتمعات فيها أسر ذات والد واحد أقل.»',
 'أكبر دراسة اقتصادية في عصرها تجعل حضور الوالدين معا أقوى عامل في مستقبل الأبناء؛ فإقصاء الأب يضر الطفل والمجتمع كله.',
 [('https://eml.berkeley.edu/%7Esaez/geosummary.pdf','الملخص التنفيذي للدراسة','جامعة كاليفورنيا في بيركلي'),('https://cepr.org/voxeu/columns/where-land-opportunity-intergenerational-mobility-us','عرض الدراسة','مركز أبحاث السياسات الاقتصادية الأوروبي')],SP),
mk('A4-111','soc','us',['silat_al_rahim'],'explicit','راج تشيتي وزملاؤه 2018 — كثرة الآباء الحاضرين في الحي ترفع مستقبل الأولاد ولو غاب أبوهم',
 'Chetty R, Hendren N, Jones MR, Porter SR','2018/2020','Race and Economic Opportunity in the United States: An Intergenerational Perspective','Quarterly Journal of Economics 135(2), 2020 — abstract and introduction','الولايات المتحدة — جامعة هارفارد ومكتب الإحصاء الأمريكي','دراسة سجلات وطنية',
 'دراسة لفريق راج تشيتي بجامعة هارفارد مع مكتب الإحصاء الأمريكي على بيانات 20 مليون طفل، منشورة في المجلة الفصلية للاقتصاد.',
 '"The few areas with small black-white gaps tend to be low-poverty neighborhoods with low levels of racial bias among whites and high rates of father presence among blacks. ... Black father presence at the neighborhood level strongly predicts black boys\' outcomes irrespective of whether their own father is present or not ..."',
 '«المناطق القليلة التي تصغر فيها الفجوة [بين السود والبيض] هي في الغالب أحياء قليلة الفقر، قليلة التحيز العنصري، عالية في نسبة حضور الآباء ... وحضور الآباء في الحي يتنبأ بقوة بمستقبل الأولاد، سواء أكان أبو الولد نفسه حاضرا أم لا ...»',
 'حضور الأب لا ينفع ولده وحده، بل ينفع أولاد الحي كله؛ فإقصاء الآباء عن أولادهم يضر جيلا كاملا.',
 [('https://opportunityinsights.org/paper/race/','صفحة الدراسة','جامعة هارفارد — مختبر فرص التنمية'),('https://opportunityinsights.org/wp-content/uploads/2018/04/race_paper.pdf','نص الدراسة','جامعة هارفارد')],SR),
mk('A4-112','soc','uk',['silat_al_rahim'],'explicit','عطار شوارتز وزملاؤها 2009 — انخراط الأجداد يقلل مشكلات المراهقين، وأقوى أثره في الأسر المنفصلة',
 'Attar-Schwartz S, Tan JP, Buchanan A, Flouri E, Griggs J','2009','Grandparenting and Adolescent Adjustment in Two-Parent Biological, Lone-Parent, and Step-Families','Journal of Family Psychology 23(1): 67–75','المملكة المتحدة — جامعة أكسفورد','دراسة مسحية وطنية',
 'دراسة من مركز أبحاث الأسرة في جامعة أكسفورد على عينة بريطانية واسعة من المراهقين، في مجلة علم نفس الأسرة التي تصدرها الجمعية الأمريكية لعلم النفس.',
 '"... greater grandparent involvement was associated with fewer emotional problems (p < .01) and with more prosocial behavior (p < .001). ... grandparent involvement was more strongly associated with reduced adjustment difficulties among adolescents from lone-parent and step- families than those from two-parent biological families."',
 '«... ارتبط انخراط الأجداد الأكبر بمشكلات انفعالية أقل وبسلوك اجتماعي أحسن ... وكان ارتباط انخراط الأجداد بقلة صعوبات التوافق أقوى عند المراهقين من الأسر ذات الوالد الواحد والأسر المعاد تكوينها منه عند أبناء الأسر التي فيها الوالدان.»',
 'الأجداد رحم للطفل، وأحوج الأولاد إليهم أبناء الأسر المنفصلة؛ فقطع الطفل عن أبيه يقطعه عن أجداده وأعمامه أيضا.',
 [('https://cris.huji.ac.il/en/publications/grandparenting-and-adolescent-adjustment-in-two-parent-biological/','ملخص الدراسة','الجامعة العبرية — سجل أبحاث المؤلفة')],SR),
# ---- study
mk('A5-210','study','us',['shared_parenting'],'explicit','فابريشيوس — الأبناء أنفسهم بعد أن كبروا: العيش مع كل والد وقتا متساويا هو الأصلح',
 'Fabricius WV — Arizona State University','1990s/2020','Young adults\' perspectives on living arrangements after divorce — reported by ASU News, March 2, 2020','ASU News','الولايات المتحدة — جامعة ولاية أريزونا','دراسة ميدانية',
 'وليم فابريشيوس أستاذ علم النفس بجامعة ولاية أريزونا ومن أبرز الباحثين في الرعاية المشتركة بالمناصفة، والخبر من الموقع الرسمي للجامعة.',
 '"... the students overwhelmingly thought that living with each of their parents for equal amounts of time was best."',
 '«... رأى الطلاب [من أبناء المطلقين] بأغلبية ساحقة أن العيش مع كل واحد من الوالدين وقتا متساويا هو الأفضل.»',
 'هذا صوت الأبناء بعد أن كبروا وتحرروا من ضغط النزاع: يريدون أباهم وأمهم بالمناصفة. فلا تخيير مع تغييب، والجواب الصحيح يعرف من الأبناء بعد النضج.',
 [('https://news.asu.edu/20200302-asu-psychology-research-leads-international-conversation-about-custody-laws','خبر الجامعة','جامعة ولاية أريزونا')],SP),
# ---- intl
mk('A5-211','intl','world',['shared_parenting'],'explicit','المؤتمر الدولي السادس للرعاية المشتركة بالمناصفة 2023 — المناصفة هي الأمثل لنمو الطفل',
 'International Council on Shared Parenting (ICSP)','2023','Conclusions of the 6th International Conference on Shared Parenting, Athens, May 5–7, 2023','Conclusions 1 and 7','دولي — المجلس الدولي للرعاية المشتركة بالمناصفة (34 دولة)','خلاصة مؤتمر علمي دولي',
 'المجلس الدولي للرعاية المشتركة بالمناصفة يجمع الباحثين والقضاة والمختصين في قانون الأسرة؛ وحضر مؤتمره السادس في أثينا نحو 200 مندوب من 34 دولة.',
 '"... shared parenting is a viable post-divorce parenting arrangement that is optimal to child development and well-being ..."',
 '«... الرعاية المشتركة ترتيب ناجح بعد الطلاق، وهو الأمثل لنمو الطفل وحسن حاله ...»',
 'خلاصة مؤتمر دولي من 34 دولة: الرعاية المشتركة بالمناصفة هي الأمثل للطفل بعد الطلاق.',
 [('https://www.twohomes.org/?p=1196','خلاصات المؤتمر','المجلس الدولي للرعاية المشتركة بالمناصفة')],SP),
mk('A4-113','intl','world',['silat_al_rahim'],'explicit','منظمة التعاون الإسلامي — عهد حقوق الطفل في الإسلام 2005: لا يحرم الطفل من صلته بوالديه',
 'Organisation of Islamic Cooperation (OIC)','2005','Covenant on the Rights of the Child in Islam','Articles 8(2), 8(3), 11(1)','دولي — منظمة التعاون الإسلامي (57 دولة)','معاهدة دولية',
 'عهد اعتمده مؤتمر وزراء خارجية الدول الإسلامية في صنعاء سنة 2005، وهو وثيقة حقوق الطفل الرسمية لمنظمة التعاون الإسلامي التي تضم 57 دولة.',
 '"No child shall be separated from his/her parents against their will ... no child shall be deprived of maintaining relations with them. ... A sound upbringing is a right of the child and shall be the responsibility of his / her parents or legal guardian."',
 '«لا يفصل طفل عن والديه رغما عنهما ... ولا يحرم طفل من الحفاظ على صلته بهما ... والتربية السليمة حق للطفل، وهي مسؤولية والديه أو وليه الشرعي.»',
 'الدول الإسلامية كلها تعهدت ألا يحرم الطفل من صلته بوالديه، وأن تربيته مسؤولية الوالدين معا؛ فقطع الطفل عن أبيه مخالف لعهد المسلمين أنفسهم.',
 [('https://bdrive.oic-oci.org/index.php/s/8Czb8kFGRJJydgT/download','نص العهد','منظمة التعاون الإسلامي'),('https://www.refworld.org/docid/44eaf0e4a.html','سجل العهد','قاعدة بيانات المفوضية السامية لشؤون اللاجئين')],SR),
]
N+=C
json.dump(N,open(P,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('added',len(C))
