# -*- coding: utf-8 -*-
# v1.31.0: military deployment (father absence without blame), OCD meta-analysis, Field 2001 verbatim
import json,copy
P='/home/claude/work/new_cards.json'
N=json.load(open(P,encoding='utf8')); N=[x for x in N if not x.get('v131')]
tw=[x for x in N if x['id']=='A4-071'][0]
def mk(cid,sec,icon,title,author,year,tl,where,jur,level,about,ot,tt,arg,links):
    e=copy.deepcopy(tw)
    e.update(id=cid,sec=sec,icon=icon,supports=['silat_al_rahim'],strength='explicit',jurisdiction=jur,title=title,ot=ot,ltr=True,tt=tt,about=about,level=level,arg=arg,chips=[['str','دلالة صريحة'],['sup','صلة الرحم']],v131=True,fam='west')
    e['src']=dict(author=author,year=str(year),jur=jur,title_latin=tl,sw='',where=where,latin=True)
    e['links']=[dict(url=u,label=l,site=s,domain=u.split('/')[2]) for u,l,s in links]
    return e
C=[
mk('A4-124','military','us','مجلة طب الأطفال الأمريكية 2010 — أطفال الجنود الغائبين في الحرب أكثر اضطرابا، وكلما طال غياب الأب زادت مشكلاتهم',
 'Chandra A, Lara-Cinisomo S, Jaycox LH, Tanielian T, Burns RM, Ruder T, Han B','2010','Children on the Homefront: The Experience of Children From Military Families','Pediatrics 125(1): 16–25',
 'الولايات المتحدة — مؤسسة راند','دراسة محكمة في مجلة الأكاديمية الأمريكية لطب الأطفال',
 'دراسة لمؤسسة راند الأمريكية على 1507 أطفال من أسر الجنود، نشرت في مجلة «طب الأطفال»، المجلة الرسمية للأكاديمية الأمريكية لطب الأطفال.',
 '"... children in this study had more emotional difficulties compared with national samples. Length of parental deployment and poorer nondeployed caregiver mental health were significantly associated with a greater number of challenges for children both during deployment and deployment reintegration."',
 '«... كان أطفال هذه الدراسة أكثر صعوبات انفعالية من العينات الوطنية. وارتبط طول غياب الوالد في الخدمة وسوء الصحة النفسية للوالد الباقي ارتباطا واضحا بكثرة المشكلات عند الأطفال، أثناء الغياب وبعد العودة.»',
 'هنا الأب بطل غائب في خدمة وطنه لا متهم؛ ومع ذلك يتأذى الطفل من غيابه، ويزداد أذاه بطول الغياب. فالضرر من الغياب نفسه، لا من صفة الأب. فكيف بغياب يفرضه القانون سنين؟',
 [('https://www.centreforevidence.org/article/20200322-children-on-the-homefront-the-experience-of-children-from-military-families','ملخص الدراسة','مركز الأدلة لأسر العسكريين'),('https://doi.org/10.1542/peds.2009-1180','البحث في المجلة','Pediatrics')]),
mk('A4-125','military','us','مجلة طب الأطفال الأمريكية 2010 — أكثر من 640 ألف طفل: غياب الوالد الجندي يزيد زياراتهم للطب النفسي 11%',
 'Gorman GH, Eide M, Hisle-Gorman E','2010','Wartime Military Deployment and Increased Pediatric Mental and Behavioral Health Complaints','Pediatrics 126(6): 1058–1066',
 'الولايات المتحدة — الجامعة العسكرية للعلوم الصحية','دراسة محكمة على سجلات طبية وطنية',
 'دراسة على السجلات الطبية لنحو 642 ألف طفل بين الثالثة والثامنة من أبناء العسكريين الأمريكيين، نشرت في مجلة الأكاديمية الأمريكية لطب الأطفال.',
 '"The sample comprised 642,397 children aged three to eight years and 442,722 military parents ... [children with a deployed parent] increased their outpatient mental and behavioral health visits by 11% ..."',
 '«شملت العينة 642397 طفلا بين الثالثة والثامنة و442722 والدا عسكريا ... [وزاد الأطفال الذين غاب والدهم في الخدمة] زياراتهم للعيادات النفسية والسلوكية بنسبة 11% ...»',
 'في أكبر سجل طبي لأطفال الجنود: غياب الوالد وحده يرفع حاجة الطفل إلى الطبيب النفسي، وهو غياب شريف مؤقت. فما بال غياب تفرضه المحاكم سنين؟',
 [('https://reachfamilies.umn.edu/node/5077','ملخص الدراسة','جامعة مينيسوتا'),('https://doi.org/10.1542/peds.2009-2856','البحث في المجلة','Pediatrics')]),
mk('A4-126','military','us','مجلة الجمعية الطبية الأمريكية لطب الأطفال 2011 — 300 ألف طفل: كلما طال غياب الوالد في الجيش زادت تشخيصات القلق والاكتئاب والاضطراب السلوكي',
 'Mansfield AJ, Kaufman JS, Engel CC, Gaynes BN','2011','Deployment and Mental Health Diagnoses Among Children of US Army Personnel','Archives of Pediatrics & Adolescent Medicine 165(11): 999–1005',
 'الولايات المتحدة — جامعة نورث كارولينا','دراسة محكمة على سجلات طبية وطنية',
 'دراسة على السجلات الطبية لأكثر من 300 ألف طفل من أبناء جنود الجيش الأمريكي بين الخامسة والسابعة عشرة، نشرت في مجلة الجمعية الطبية الأمريكية لطب الأطفال والمراهقين.',
 '"... the risk of a mental health diagnosis was higher for those youth who had a parent deployed for a longer period of time ... the largest effects among all children were observed for acute stress reaction and adjustment disorders, pediatric behavioral disorders, and depression."',
 '«... كان خطر التشخيص النفسي أعلى عند الأطفال الذين غاب والدهم في الخدمة مدة أطول ... وأكبر الآثار عند الأطفال جميعا كانت في اضطراب الكرب الحاد واضطرابات التكيف، والاضطرابات السلوكية، والاكتئاب.»',
 'الغياب يقاس بالشهور ويقاس أثره في الأطفال: كرب وقلق واكتئاب واضطراب سلوك، على قدر طول الغياب. والقانون الذي يغيب الأب عن ولده خمس عشرة سنة إلا ساعات يصنع هذا الأثر مضاعفا.',
 [('https://www.sciencedaily.com/releases/2011/07/110704174610.htm','عرض الدراسة','ScienceDaily'),('https://doi.org/10.1001/archpediatrics.2011.123','البحث في المجلة','JAMA Network')]),
mk('A2-124','fear','cn','تحليل جامع 2021 — الإيذاء العاطفي في الطفولة يرتبط بشدة الوسواس القهري',
 'Ou W, Li Z, Zheng Q, Chen W, Liu J, Liu B, Zhang Y','2021','Association Between Childhood Maltreatment and Symptoms of Obsessive-Compulsive Disorder: A Meta-Analysis','Frontiers in Psychiatry 11: 612586',
 'الصين — جامعة سنترال ساوث','تحليل جامع لعشر دراسات على 1611 مريضا',
 'تحليل جامع لعشر دراسات شملت 1611 مريضا بالوسواس القهري، نشر في مجلة «الحدود في الطب النفسي» المحكمة.',
 '"... childhood emotional abuse (CEA) and childhood sexual abuse (CSA) was related with the severity of OCS ... Our meta-analysis indicates that OCD patients who suffered more CM may exhibit more severe OCS and depressive symptoms."',
 '«... ارتبط الإيذاء العاطفي في الطفولة والاعتداء الجنسي في الطفولة بشدة أعراض الوسواس القهري ... ويدل تحليلنا الجامع على أن مرضى الوسواس القهري الذين تعرضوا لإيذاء أكثر في طفولتهم قد تظهر عليهم أعراض وسواسية واكتئابية أشد.»',
 'الطفل الذي يلقن الخوف والخرافة عن أبيه يؤذى عاطفيا، والإيذاء العاطفي في الطفولة يرتبط بشدة الوسواس القهري في الكبر؛ فهذا التلقين يصنع هشاشة نفسية تلازم الطفل.',
 [('https://www.frontiersin.org/articles/10.3389/fpsyt.2020.612586/full','البحث في المجلة','Frontiers in Psychiatry')]),
mk('A2-125','fear','uk','فيلد وأرجيريس ونولز 2001 — الطفل يغير معتقده ويخاف بكلام البالغ وحده',
 'Field AP, Argyris NG, Knowles KA','2001','Who\'s afraid of the big bad wolf: a prospective paradigm to test Rachman\'s indirect pathways in children','Behaviour Research and Therapy 39(11): 1259–1276',
 'المملكة المتحدة — جامعة ساسكس','تجربة محكمة على أطفال بين السابعة والتاسعة',
 'تجربة من جامعة ساسكس البريطانية على أطفال بين السابعة والتاسعة، نشرت في مجلة «بحوث السلوك والعلاج» المحكمة.',
 '"Fear-related beliefs about the monsters changed significantly as a result of verbal information but not video information. ... verbal information significantly changed fear-beliefs, but only when the information came from an adult."',
 '«تغيرت معتقدات الأطفال المتصلة بالخوف تغيرا واضحا بالمعلومات المنطوقة لا بالمعلومات المصورة ... وغيرت المعلومات المنطوقة معتقدات الخوف تغيرا واضحا، ولكن فقط حين جاءت من بالغ.»',
 'كلمة من بالغ يثق به الطفل تكفي لتزرع الخوف فيه، ولا يفعل ذلك كلام الأقران ولا الصور. فالحاضنة حين تقول للطفل إن أباه يسممه تزرع فيه خوفا يبقى، والعلم يقول إن كلامها هو الطريق الأقوى إلى خوفه.',
 [('https://sro.sussex.ac.uk/id/eprint/712/','سجل البحث','مستودع جامعة ساسكس')]),
]
N+=C
json.dump(N,open(P,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('added',len(C))
