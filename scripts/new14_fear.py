# -*- coding: utf-8 -*-
# v1.27.0: section «fear»: frightening and indoctrinating the child harms its mental health
import json,copy
P='/home/claude/work/new_cards.json'
N=json.load(open(P,encoding='utf8')); N=[x for x in N if not x.get('v127')]
tw=[x for x in N if x['id']=='A4-071'][0]
def mk(cid,icon,sup,title,author,year,title_latin,where,jur,level,about,ot,tt,arg,links):
    e=copy.deepcopy(tw)
    e.update(id=cid,sec='fear',icon=icon,supports=sup,strength='explicit',jurisdiction=jur,title=title,ot=ot,ltr=True,tt=tt,about=about,level=level,arg=arg,chips=[['str','دلالة صريحة'],['sup','صلة الرحم']],v127=True,fam='west')
    e['src']=dict(author=author,year=str(year),jur=jur,title_latin=title_latin,sw='',where=where,latin=True)
    e['links']=[dict(url=u,label=l,site=s,domain=u.split('/')[2]) for u,l,s in links]
    return e
C=[
mk('A2-115','us',['silat_al_rahim'],'الجمعية الأمريكية لعلم النفس 2014 — ترويع الطفل وتهديده وعزله يضره كالاعتداء الجسدي والجنسي أو أشد',
 'Spinazzola J, Hodgdon H, Liang L-J, Ford JD, Layne CM, Pynoos R, Briggs EC, Stolbach B','2014',
 'Unseen Wounds: The Contribution of Psychological Maltreatment to Child and Adolescent Mental Health and Risk Outcomes',
 'Psychological Trauma: Theory, Research, Practice, and Policy (American Psychological Association), 8 October 2014',
 'الولايات المتحدة — الشبكة الوطنية لصدمات الأطفال','دراسة محكمة على 5616 طفلا ومراهقا في مجلة الجمعية الأمريكية لعلم النفس',
 'دراسة على 5616 طفلا ومراهقا من قاعدة بيانات الشبكة الوطنية الأمريكية لصدمات الأطفال، نشرتها الجمعية الأمريكية لعلم النفس في مجلتها المحكمة.',
 '"... [children who are psychologically abused] face similar and sometimes worse mental health problems as children who are physically or sexually abused ... [they] suffered from anxiety, depression, low self-esteem, symptoms of post-traumatic stress and suicidality ... [psychological maltreatment includes] care-giver inflicted bullying, terrorizing, coercive control, severe insults, debasement ... threats, overwhelming demands, shunning and/or isolation."',
 '«... [الأطفال الذين يقع عليهم الإيذاء النفسي] يواجهون مشكلات نفسية مماثلة، وأحيانا أسوأ، من الأطفال الذين يقع عليهم الاعتداء الجسدي أو الجنسي ... [فقد] عانوا القلق والاكتئاب وتدني تقدير الذات وأعراض اضطراب ما بعد الصدمة والميل إلى الانتحار ... [والإيذاء النفسي يشمل] ما يوقعه القائم على رعاية الطفل من تنمر وترويع وسيطرة قسرية وإهانات شديدة وإذلال ... وتهديد ومطالب ساحقة ونبذ أو عزل.»',
 'ترويع الطفل وتهديده وعزله على يد من يرعاه ليس أمرا هينا: إنه يورث القلق والاكتئاب وأعراض الصدمة كالاعتداء الجسدي والجنسي أو أشد. فالطفل الذي يخوف من أبيه ويلقن أن أباه يريد قتله يقع عليه أخطر أنواع الأذى.',
 [('https://www.newswise.com/articles/childhood-psychological-abuse-as-harmful-as-sexual-or-physical-abuse','بيان الجمعية الأمريكية لعلم النفس عن الدراسة','Newswise')]),
mk('A2-116','ca',['silat_al_rahim'],'مجلة الطب النفسي الأمريكية 2015 — الإيذاء العاطفي للطفل يضره كالإيذاء الجسدي: قلق واكتئاب وعدوان',
 'Vachon DD, Krueger RF, Rogosch FA, Cicchetti D','2015','Assessment of the Harmful Psychiatric and Behavioral Effects of Different Forms of Child Maltreatment',
 'JAMA Psychiatry 72(11), 2015; doi:10.1001/jamapsychiatry.2015.1792',
 'كندا والولايات المتحدة — جامعة ماكغيل وجامعة مينيسوتا','دراسة محكمة على نحو 2300 طفل في مجلة الجمعية الطبية الأمريكية للطب النفسي',
 'دراسة لجامعات ماكغيل الكندية وروتشستر ومينيسوتا الأمريكيتين، على نحو 2300 طفل بين الخامسة والثالثة عشرة، نشرت في مجلة الجمعية الطبية الأمريكية للطب النفسي.',
 '"Emotional abuse may be as harmful as physical abuse and neglect. ... different types of child abuse have equivalent, broad, and universal effects ... These consequences are wide-ranging and include everything from anxiety and depression to rule-breaking and aggression."',
 '«الإيذاء العاطفي قد يكون في ضرره كالاعتداء الجسدي والإهمال ... فأنواع إيذاء الطفل المختلفة آثارها متكافئة وواسعة وعامة ... وهذه العواقب واسعة المدى، تشمل كل شيء من القلق والاكتئاب إلى مخالفة القواعد والعدوان.»',
 'تسميم عقل الطفل بالكلام المخيف إيذاء عاطفي، وآثاره كآثار الضرب: قلق واكتئاب وعدوان وخروج على القواعد.',
 [('https://www.mcgill.ca/newsroom/node/24532','بيان جامعة ماكغيل عن الدراسة','جامعة ماكغيل')]),
mk('A2-117','au',['silat_al_rahim'],'مجلة بلوس للطب 2012 — الإيذاء العاطفي في الطفولة يضاعف الاكتئاب ومحاولات الانتحار ثلاث مرات',
 'Norman RE, Byambaa M, De R, Butchart A, Scott J, Vos T','2012',
 'The Long-Term Health Consequences of Child Physical Abuse, Emotional Abuse, and Neglect: A Systematic Review and Meta-Analysis',
 'PLOS Medicine 9(11): e1001349; doi:10.1371/journal.pmed.1001349',
 'أستراليا — جامعة كوينزلاند، بمشاركة منظمة الصحة العالمية','تحليل جامع لعدة دراسات: أعلى درجات الدليل',
 'تحليل جامع من جامعة كوينزلاند الأسترالية، شارك فيه ألكسندر بوتشارت من منظمة الصحة العالمية، ونشر في مجلة بلوس للطب المحكمة.',
 '"... emotional abuse [OR = 3.06; 95% CI 2.43–3.85] ... [for depressive disorders] ... emotional abuse [OR = 3.37; 95% CI 2.44–4.67] ... [for suicide attempts] ... This overview of the evidence suggests a causal relationship between non-sexual child maltreatment ... [and a range of mental disorders] ..."',
 '«... الإيذاء العاطفي [نسبة الأرجحية 3.06] ... [في اضطرابات الاكتئاب] ... الإيذاء العاطفي [نسبة الأرجحية 3.37] ... [في محاولات الانتحار] ... وهذه الخلاصة للأدلة تدل على علاقة سببية بين إيذاء الطفل غير الجنسي ... [وطائفة من الاضطرابات النفسية] ...»',
 'أعلى درجات الدليل: الطفل الذي يؤذى عاطفيا يضاعف خطر إصابته بالاكتئاب ثلاث مرات، وخطر محاولته الانتحار أكثر من ثلاث مرات، والعلاقة سببية.',
 [('https://ideas.repec.org/a/plo/pmed00/1001349.html','ملخص البحث','IDEAS / RePEc'),('https://doi.org/10.1371/journal.pmed.1001349','البحث في المجلة','PLOS Medicine')]),
mk('A2-118','nl',['silat_al_rahim'],'موريس وفيلد 2010 — الطفل يكتسب الخوف من الكلام المخيف الذي يسمعه، دون أن يقع له شيء',
 'Peter Muris & Andy P. Field','2010','The role of verbal threat information in the development of childhood fear. "Beware the Jabberwock!"',
 'Clinical Child and Family Psychology Review 13(2): 129–150; doi:10.1007/s10567-010-0064-1',
 'هولندا والمملكة المتحدة — جامعة إيراسموس روتردام وجامعة ساسكس','مراجعة علمية محكمة لثلاثين سنة من البحوث',
 'بيتر موريس أستاذ علم نفس الطفل في جامعة إيراسموس الهولندية، وآندي فيلد أستاذ علم النفس في جامعة ساسكس البريطانية، وهما من أبرز من درس نشأة مخاوف الأطفال.',
 '"... childhood fears ... can also be elicited by means of threat information transmission ..."',
 '«... مخاوف الطفولة ... يمكن أن تنشأ أيضا بنقل معلومات مخيفة [إلى الطفل] ...»',
 'العلم يقرر أن الخوف يزرع في الطفل بالكلام وحده؛ فالطفل الذي يقال له إن أباه يسممه ويريد خطفه وقتله يتعلم الخوف من أبيه دون أن يقع عليه منه شيء.',
 [('https://repub.eur.nl/pub/18548','سجل البحث','مستودع جامعة إيراسموس'),('https://doi.org/10.1007/s10567-010-0064-1','البحث في المجلة','Springer')]),
mk('A2-119','uk',['silat_al_rahim'],'فيلد ولوسون وبانيرجي 2008 — الكلام المخيف يغير معتقدات الطفل ستة أشهر ويجعله يتجنب ما خوف منه',
 'Andy Field, Joanne Lawson, Robin Banerjee','2008',
 'The verbal threat information pathway to fear in children: the longitudinal effects on fear cognitions and the immediate effects on avoidance behavior',
 'Journal of Abnormal Psychology 117(1): 214–224',
 'المملكة المتحدة — جامعة ساسكس','تجربة محكمة في مجلة الجمعية الأمريكية لعلم النفس',
 'دراسة تجريبية من جامعة ساسكس البريطانية، نشرت في مجلة علم النفس المرضي التي تصدرها الجمعية الأمريكية لعلم النفس.',
 '"Verbal information has long been assumed to be an indirect pathway to fear. ... the changes persisted up to 6 months later ... Verbal threat information also induced behavioral avoidance ..."',
 '«طالما افترض أن الكلام طريق غير مباشر إلى الخوف ... [وقد] استمرت التغيرات [في معتقدات الأطفال] حتى ستة أشهر بعد ذلك ... كما أحدثت المعلومات المخيفة المنطوقة سلوك التجنب ...»',
 'كلمة مخيفة تقال للطفل تبقى في معتقده شهورا وتجعله يتجنب ما خوف منه؛ فكيف بطفل يلقن سنين أن أباه وأجداده يريدون أذاه؟ يتجنب طعامهم وهداياهم ولقاءهم، كما يقول العلم تماما.',
 [('https://sussex.figshare.com/articles/journal_contribution/The_verbal_threat_information_pathway_to_fear_in_children_the_longitudinal_effects_on_fear_cognitions_and_the_immediate_effects_on_avoidance_behavior/23327288','سجل البحث','مستودع جامعة ساسكس')]),
]
N+=C
json.dump(N,open(P,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('added',len(C))
