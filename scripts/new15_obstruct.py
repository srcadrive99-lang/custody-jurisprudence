# -*- coding: utf-8 -*-
# v1.28.0: laws obliging each parent to protect the child's bond with the other parent
import json,copy
P='/home/claude/work/new_cards.json'
N=json.load(open(P,encoding='utf8')); N=[x for x in N if not x.get('v128')]
tw=[x for x in N if x['id']=='A4-071'][0]
def mk(cid,icon,title,author,year,tl,where,jur,level,about,ot,tt,arg,links):
    e=copy.deepcopy(tw)
    e.update(id=cid,sec='law',icon=icon,supports=['silat_al_rahim'],strength='explicit',jurisdiction=jur,title=title,ot=ot,ltr=True,tt=tt,about=about,level=level,arg=arg,chips=[['str','دلالة صريحة'],['sup','صلة الرحم']],v128=True,fam='west')
    e['src']=dict(author=author,year=str(year),jur=jur,title_latin=tl,sw='',where=where,latin=True)
    e['links']=[dict(url=u,label=l,site=s,domain=u.split('/')[2]) for u,l,s in links]
    return e
C=[
mk('A5-215','de','القانون المدني الألماني، المادة 1684 — على كل والد أن يمتنع عن كل ما يفسد علاقة الطفل بالوالد الآخر',
 'Bürgerliches Gesetzbuch (BGB)','1998','§ 1684 Umgang des Kindes mit den Eltern','BGB § 1684 Abs. 1, Abs. 2 Satz 1, Abs. 3 Sätze 2–3',
 'ألمانيا — القانون المدني الاتحادي','تشريع اتحادي نافذ',
 'القانون المدني الألماني نافذ في كل ألمانيا، والمادة 1684 هي أصل حق الطفل في لقاء والديه بعد الفرقة.',
 '"Das Kind hat das Recht auf Umgang mit jedem Elternteil; jeder Elternteil ist zum Umgang mit dem Kind verpflichtet und berechtigt. ... Die Eltern haben alles zu unterlassen, was das Verhältnis des Kindes zum jeweils anderen Elternteil beeinträchtigt oder die Erziehung erschwert. ... Es kann die Beteiligten durch Anordnungen zur Erfüllung der in Absatz 2 geregelten Pflicht anhalten. Wird die Pflicht nach Absatz 2 dauerhaft oder wiederholt erheblich verletzt, kann das Familiengericht auch eine Pflegschaft für die Durchführung des Umgangs anordnen (Umgangspflegschaft)."',
 '«للطفل حق اللقاء بكل واحد من والديه، وكل واحد من الوالدين ملزم بلقاء الطفل وله الحق فيه ... وعلى الوالدين أن يمتنعا عن كل ما يضر بعلاقة الطفل بالوالد الآخر أو يعسر تربيته ... وللمحكمة أن تلزم الأطراف بأوامر تحملهم على أداء هذا الواجب. فإذا أخل به إخلالا جسيما دائما أو متكررا، جاز لمحكمة الأسرة أن تعين وصيا يتولى تنفيذ اللقاء.»',
 'ألمانيا تلزم الحاضن بالامتناع عن كل ما يفسد علاقة الطفل بأبيه، وتعين المحكمة من ينفذ اللقاء إذا أخل به. فتحريض الطفل على أبيه وتخويفه منه مخالفة يحاسب عليها القانون هناك، والطفل يلقى أباه حقا له، لا ساعات تحت الرقابة.',
 [('https://gesetze.legal/bund/bgb/1684','نص المادة','gesetze.legal')]),
mk('A5-216','fr','القانون المدني الفرنسي، المادة 373-2 — على كل والد أن يحفظ صلته بالطفل ويحترم صلة الطفل بالوالد الآخر',
 'Code civil (France), loi n° 2002-305 du 4 mars 2002 relative à l\'autorité parentale','2002','Article 373-2 du Code civil','art. 373-2, alinéa 2',
 'فرنسا — القانون المدني','تشريع نافذ',
 'المادة 373-2 من القانون المدني الفرنسي أدخلها قانون السلطة الأبوية سنة 2002، وهي نافذة في فرنسا كلها.',
 '"Chacun des père et mère doit maintenir des relations personnelles avec l\'enfant et respecter les liens de celui-ci avec l\'autre parent."',
 '«على كل واحد من الأب والأم أن يحفظ صلته الشخصية بالطفل، وأن يحترم صلة الطفل بالوالد الآخر.»',
 'القانون الفرنسي يجعل احترام صلة الطفل بأبيه واجبا على الأم، كما يجعل احترام صلته بأمه واجبا على الأب. فقطع الطفل عن أبيه وتشويه صورته عنده إخلال بواجب قانوني.',
 [('https://www.senat.fr/leg/tas01-023.html','نص القانون كما أقره مجلس الشيوخ الفرنسي','مجلس الشيوخ الفرنسي')]),
mk('A5-217','fr','قانون العقوبات الفرنسي، المادة 227-5 — منع الطفل عمن له حق لقائه جريمة: سنة سجنا وغرامة 15 ألف يورو',
 'Code pénal (France)','1994','Article 227-5 du Code pénal (non-représentation d\'enfant)','art. 227-5',
 'فرنسا — قانون العقوبات','تشريع نافذ',
 'المادة 227-5 من قانون العقوبات الفرنسي في باب الاعتداء على القصر والأسرة، وتسمى جريمة «عدم تسليم الطفل».',
 '"Le fait de refuser indûment de représenter un enfant mineur à la personne qui a le droit de le réclamer est puni d\'un an d\'emprisonnement et de 15 000 euros d\'amende."',
 '«رفض تسليم الطفل القاصر بغير حق إلى من له حق المطالبة به يعاقب عليه بالسجن سنة وبغرامة 15 ألف يورو.»',
 'فرنسا تعاقب بالسجن من يمنع الطفل عمن له حق لقائه، أبا كان أو أما. فالعقوبة هناك على من يقطع الطفل عن والده، لا على الوالد الذي يطلب ولده.',
 [('https://www.cabinetaci.com/non-representation-denfant-cadre-juridique-et-defense-penale/','نص المادة وشرحها','مكتب محاماة فرنسي'),('https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006165319/2009-05-05/','باب المادة في الجريدة الرسمية الفرنسية','Légifrance')]),
]
N+=C
json.dump(N,open(P,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('added',len(C))
