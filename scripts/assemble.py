# -*- coding: utf-8 -*-
"""Rebuild both card editions from the previous HTML + patches + new cards.
Usage: python3 assemble.py
Inputs: out/NUQUL_7_9_CARDS_MOBILE.html, out/NUQUL_7_9_CARDS.html (base), out/nuqul_7_9.json,
        new_cards.json (new entries), links_fix.json (id -> {url,label,site,domain}), standing.py
Outputs: build/NUQUL_7_9_CARDS_MOBILE.html, build/NUQUL_7_9_CARDS.html
"""
import re, json, html as H, sys, os, collections, io
sys.path.insert(0,'/home/claude/work')
import flags, segno
from standing import S as STANDING
from plain import plain, leftovers

BASE_M='/home/claude/work/out/NUQUL_7_9_CARDS_MOBILE.html'
BASE_W='/home/claude/work/out/NUQUL_7_9_CARDS.html'
JSON='/home/claude/work/out/nuqul_7_9.json'
OUT='/home/claude/work/build'
os.makedirs(OUT,exist_ok=True)

TITLE_OLD='حول سن الحضانة والرعاية المشتركة'
MN='<span class="mn">بالمناصفة</span>'

# ---------------- sections ----------------
SECTIONS=[
 dict(key='med',  name='خبراء الطب', acc='#B00010', accd='#7E000B', g=('#FDEDEE','#F6CACE'),
      blurb='البلوغ يتبكر، والأب شريك في صحة ولده'),
 dict(key='body', name='جسد الطفل يشهد', acc='#00796B', accd='#004D40', g=('#E0F2F1','#B2DFDB'),
      blurb='السابعة علامة في الجسد: الأسنان والغدد والاستقلال بالنفس'),
 dict(key='psy',  name='خبراء علم النفس', acc='#5B4B9A', accd='#3F3370', g=('#F0ECFA','#D8CDF1'),
      blurb='سن العقل عند السابعة، والتعلق بالأب من السنة الأولى'),
 dict(key='school', name='المدرسة والتعليم', acc='#D81B60', accd='#9C1145', g=('#FCE4EC','#F8BBD0'),
      blurb='العالم يدخل الطفل المدرسة بين الخامسة والسابعة'),
 dict(key='soc',  name='خبراء علوم المجتمع والإنسان', acc='#B4541A', accd='#7E3A12', g=('#FDF0E6','#F6D3B8'),
      blurb='الطفولة تنتهي نحو السابعة، وغياب الأب يضر'),
 dict(key='harm', name='أضرار حرمان الطفل من أبيه', acc='#5C4033', accd='#3E2B22', g=('#F7F0EB','#E6D3C6'),
      blurb='الحرمان من الأب: مرض وانحراف وسجن'),
 dict(key='military', name='غياب الأب في الجندية: شهادة الأسر العسكرية', acc='#37474F', accd='#263238', g=('#ECEFF1','#CFD8DC'),
      blurb='الأب بطل غائب لا متهم، والطفل يتأذى بغيابه على قدر طوله'),
 dict(key='fear', name='تخويف الطفل وتلقينه يضران نفسه', acc='#6A1B9A', accd='#4A148C', g=('#F3E5F5','#E1BEE7'),
      blurb='الكلام المخيف يزرع الخوف، والترويع يورث القلق والاكتئاب'),
 dict(key='study',name='الدراسات العلمية في الرعاية المشتركة بالمناصفة', acc='#1F5FA8', accd='#16457A', g=('#E8F1FC','#C6DCF6'),
      blurb='أطفال الرعاية المشتركة بالمناصفة أحسن حالا'),
 dict(key='intl', name='المواثيق والهيئات الدولية', acc='#2E4A9A', accd='#20346D', g=('#EAEEFA','#CCD4F2'),
      blurb='حق الطفل في والديه معا'),
 dict(key='law',  name='التشريعات المقارنة', acc='#8A6418', accd='#5F4510', g=('#FBF3E2','#EEDDB4'),
      blurb='من لندن إلى بوينس آيرس: الأصل مشاركة الوالدين'),
 dict(key='enforce', name='حماية لقاء الطفل بوالديه وتنفيذه', acc='#0E6E55', accd='#094D3B', g=('#E2F4EE','#BDE5D7'),
      blurb='ألمانيا وفرنسا: من يعطل لقاء الطفل بأبيه يحاسب'),
 dict(key='tamyiz', name='سن التمييز في قوانين العالم', acc='#1A237E', accd='#0D1452', g=('#E8EAF6','#C5CAE9'),
      blurb='قوانين الشرق والغرب تجعل السابعة حد التمييز والمسؤولية'),
 dict(key='court',name='القضاء', acc='#17697A', accd='#0F4A56', g=('#E3F4F7','#BFE1E8'),
      blurb='صحبة الوالد وولده من صميم الحياة الأسرية'),
 dict(key='azhar', name='فتاوى الأزهر ودار الإفتاء المصرية', acc='#7B2D26', accd='#561F1A', g=('#F8EDEB','#EBCFCA'),
      blurb='شيوخ الأزهر ومفتو الديار المصرية: سبع وتسع، ثم الضم إلى الأب'),
 dict(key='eg',   name='فقه علماء مصر', acc='#3A4B52', accd='#26333A', g=('#EEF1F2','#D5DCDF'),
      blurb='علماء مصر يشهدون: سبع للغلام وتسع للجارية'),
 dict(key='f1',   name='القرآن والسنة والآثار', acc='#0F5C3A', accd='#0A3F28', g=('#E6F3EC','#C3E2D0'),
      blurb='النص المؤسس: الولد لأبويه، وقطع الرحم محرم'),
 dict(key='f2',   name='الفقه الحنفي', acc='#1F6B5C', accd='#154A40', g=('#E3F3EC','#BFE0D2'),
      blurb='الغلام إلى أبيه عند السابعة، والجارية عند التاسعة'),
 dict(key='f3',   name='الفقه المالكي', acc='#3E7A3A', accd='#2A5427', g=('#E9F3E6','#C9E2C3'),
      blurb='الأب أقوم على التعليم والتأديب'),
 dict(key='f4',   name='الفقه الشافعي', acc='#2A8A7A', accd='#1B5E53', g=('#E4F4F1','#BFE4DC'),
      blurb='الحضانة دون السبع، والكفالة على الأب'),
 dict(key='f5',   name='الفقه الحنبلي', acc='#4E6B2F', accd='#354A20', g=('#EDF2E4','#D3DEBF'),
      blurb='التمييز حد الحضانة، والجارية أسبق نضجا'),
 dict(key='f6',   name='الفقه المقارن والتربية الإسلامية', acc='#6B5E2A', accd='#4A411D', g=('#F3F0E3','#E1DABB'),
      blurb='التعليم والتأديب في السابعة عند علماء التربية واللغة'),
 dict(key='hujaj', name='الأدلة المتضافرة', acc='#8B1E5B', accd='#601440', g=('#FBEAF3','#F0CDE0'),
      blurb='أدلة من كل الأقسام تلتقي على حكم واحد'),
]

SEC={d['key']:d for d in SECTIONS}
ORDER=[d['key'] for d in SECTIONS]
AR_ORD=['الأول','الثاني','الثالث','الرابع','الخامس','السادس','السابع','الثامن','التاسع','العاشر','الحادي عشر','الثاني عشر','الثالث عشر','الرابع عشر','الخامس عشر','السادس عشر','السابع عشر','الثامن عشر','التاسع عشر','العشرون','الحادي والعشرون','الثاني والعشرون','الثالث والعشرون']

TOC_BLURB={
 'med':'من ابن سينا إلى منظمة الصحة العالمية وكبريات مجلات طب الأطفال: السابعة سن الاستعداد للتأديب والتعليم، والتاسعة عتبة البلوغ، وانخراط الأب في رعاية ولده من صحته.',
 'psy':'أعلام علم نفس النمو يجعلون ما بين الخامسة والسابعة تحولا في العقل والسلوك، ويثبتون أن الطفل يتعلق بأبيه وأمه معا من سنيه الأولى، وأن اختيار الولد بعد سنين من الانفراد به اختيار مصنوع.',
 'soc':'علم الإنسان وعلم الاجتماع: الثقافات كلها تكلف الصغير في السابعة، والتعلم والمسؤولية يبدآن مع دخول المدرسة، وغياب الأب خسارة تتوارثها الأجيال.',
 'harm':'دراسات وطنية وسجلات رسمية: الحرمان من الأب يرفع خطر المرض النفسي والجريمة والانحراف، وزوج الأم خطر على الطفل.',
 'military':'مجلات طب الأطفال الأمريكية على مئات آلاف أطفال الجنود: غياب الأب في الخدمة العسكرية يرفع القلق والاكتئاب واضطراب السلوك على قدر طول الغياب، وهو غياب شريف مؤقت لا يتهم فيه الأب.',
 'military':'مجلات طب الأطفال الأمريكية على مئات آلاف أطفال الجنود: غياب الأب في الخدمة العسكرية يرفع القلق والاكتئاب واضطراب السلوك على قدر طول الغياب، وهو غياب شريف مؤقت لا يتهم فيه الأب.',
 'fear':'علم النفس والطب النفسي والأمم المتحدة: الطفل يكتسب الخوف من الكلام المخيف، وترويعه وتهديده وعزله يورث القلق والاكتئاب وأعراض الصدمة كالاعتداء الجسدي.',
 'study':'تحاليل بعدية ومراجعات منهجية ودراسات في عشرات الدول: أطفال الرعاية المشتركة بالمناصفة أحسن حالا من أطفال الانفراد، في كل الأعمار.',
 'intl':'اتفاقية حقوق الطفل وتفسيرها الرسمي وقرارات مجلس أوروبا: للطفل حق في والديه معا، والمسؤولية مشتركة، والمراهقة تبدأ في العاشرة.',
 'law':'تشريعات نافذة في أوروبا والأمريكتين وآسيا تجعل الأصل مشاركة الوالدين بالمناصفة أو تعظيم وقت كل والد، وتمنع تفضيل والد على الآخر بسبب جنسه.',
 'court':'محاكم عليا ودولية: صحبة الوالد وولده عنصر جوهري في الحياة الأسرية، وعلى الدولة أن تضمن تنفيذها فعلا، ولا تفضيل للأم لمجرد أنها أم.',
'azhar':'فتاوى رسمية لشيوخ الأزهر ومفتي الديار المصرية في قضايا المصريين الحقيقية، من القرن التاسع عشر إلى ما قبل سنة 2000: حضانة النساء تنتهي بسبع للغلام وتسع للبنت، ثم يضمه أبوه ولو لم ترض الحاضنة، ولا تخيير للصغير، ولا يمنع أحد الأبوين الآخر من رؤية ولده.',
 'eg':'شراح الفقه في مصر وتقنين قدري باشا والشيخ أبو زهرة: الغلام إلى أبيه في السابعة والجارية في التاسعة.',
 'f1':'آيات في وجوب صلة الرحم وتحريم قطعها، وأحاديث في حق الأب وإثم من يضيع من يعول، وآثار الصحابة في تخيير الغلام بعد التمييز لا قبله.',
 'f2':'فقهاء الحنفية: تنتهي حضانة النساء للغلام إذا استغنى بنفسه في السابعة، وللجارية إذا بلغت أو شارفت البلوغ في التاسعة، ويضم إلى أبيه للتعليم والتأديب.',
 'f3':'فقهاء المالكية: الأب أقوم على تعليم الولد وتأديبه، والحضانة حق للمحضون لا للحاضنة، ولا يمنع الأب من ولده.',
 'f4':'فقهاء الشافعية: الحضانة فيما دون السبع، وبعدها الكفالة على الأب، فالتعليم والتأديب مما يجب على الأب القيام به.',
 'f5':'فقهاء الحنابلة: التمييز حد الحضانة، والجارية تضم إلى أبيها في السابعة لأنها أسبق نضجا، وصيانة الولد وتعليمه إلى الأب.',
'hujaj':'أدلة متضافرة: كل بطاقة تجمع نصوصا منقولة بلفظها من أقسام مختلفة، القرآن والسنة والفقه وفتاوى الأزهر والطب وعلم النفس والدراسات والقضاء والتشريع والمواثيق الدولية، فتلتقي كلها على الحكم نفسه، ولكل نص رقم بطاقته الكاملة.',
 'body':'الطب الحيوي وطب الأسنان وعلم الأحياء التطوري: بين السادسة والثامنة تتبدل أسنان الطفل وتنضج غدته الكظرية ويستقل بطعامه وضبط نفسه، فالسابعة علامة في الجسد كما هي حد في الفقه.',
 'school':'اليونسكو والبيانات العالمية ووزارة التعليم الأمريكية: العالم كله يدخل الطفل المدرسة بين الخامسة والسابعة، ومشاركة الأب في التعليم ترفع تحصيل الولد.',
 'enforce':'قوانين ألمانيا وفرنسا: على الوالدين الامتناع عن كل ما يفسد علاقة الطفل بالآخر، وقضايا اللقاء تنظر أولا وبسرعة، ومن عطل اللقاء غرم أو سجن أو روجعت حضانته.',
 'tamyiz':'قوانين ألمانيا وباكستان ونيجيريا وبنغلاديش والهند وإنجلترا والقانون الكنسي: السابعة حد التمييز والأهلية والمسؤولية، وابن العاشرة يحاسب جنائيا.',
 'f6':'الموسوعات والفقه المقارن وعلماء التربية والطب واللغة في الإسلام: السابعة سن التعليم والتأديب، والتمييز هو مناط انتقال الولد إلى أبيه.',
}
OPEN_BLURB={
 'med':'أطباء الأطفال والغدد والمراجع الطبية الكبرى: البلوغ يبدأ عند البنات نحو التاسعة وعند البنين بعدها بسنتين، والأب شريك في صحة ولده ونموه من يومه الأول.',
 'psy':'أعلام علم نفس النمو يجعلون ما بين الخامسة والسابعة تحولا في العقل والسلوك، هو ما سماه الفقهاء التمييز، ويثبتون أن الطفل يتعلق بأبيه وأمه معا من سنيه الأولى.',
 'soc':'علماء الإنسان والاجتماع: الثقافات كلها تكلف الصغير في السابعة وتخرجه إلى المدرسة، والأب في كل المجتمعات شريك في التنشئة لا مجرد منفق.',
 'harm':'دراسات وطنية وسجلات رسمية في السويد وفنلندا والدنمارك وكندا وأمريكا: الحرمان من الأب يرفع خطر المرض النفسي والجريمة والانحراف، وزوج الأم خطر على الطفل.',
 'military':'مجلات طب الأطفال الأمريكية على مئات آلاف أطفال الجنود: غياب الأب في الخدمة العسكرية يرفع القلق والاكتئاب واضطراب السلوك على قدر طول الغياب، وهو غياب شريف مؤقت لا يتهم فيه الأب.',
 'fear':'الجمعية الأمريكية لعلم النفس ومجلات الطب النفسي ولجنة حقوق الطفل: تلقين الطفل الخوف من أبيه وترويعه وعزله إيذاء نفسي يضعف نفسه ويورثه القلق والاكتئاب.',
 'study':'تحاليل بعدية ومراجعات منهجية ودراسات في عشرات الدول: أطفال الرعاية المشتركة بالمناصفة أحسن حالا من أطفال الانفراد في الصحة والسلوك والدراسة، في كل الأعمار.',
 'intl':'اتفاقية حقوق الطفل وتفسيرها الرسمي وقرارات مجلس أوروبا: للطفل حق في والديه معا، والمسؤولية مشتركة، والمراهقة تبدأ في العاشرة لا في الخامسة عشرة.',
 'law':'تشريعات نافذة في أوروبا والأمريكتين وآسيا تجعل الأصل مشاركة الوالدين بالمناصفة أو تعظيم وقت كل والد، وتمنع تفضيل والد على الآخر بسبب جنسه.',
 'court':'محاكم عليا ودولية في أوروبا وأمريكا وكندا وألمانيا والبرازيل والهند: صحبة الوالد وولده عنصر جوهري في الحياة الأسرية، وعلى الدولة أن تضمن تنفيذها فعلا.',
'azhar':'فتاوى رسمية لشيوخ الأزهر ومفتي الديار المصرية في قضايا المصريين الحقيقية، من القرن التاسع عشر إلى ما قبل سنة 2000: حضانة النساء تنتهي بسبع للغلام وتسع للبنت، ثم يضمه أبوه ولو لم ترض الحاضنة، ولا تخيير للصغير، ولا يمنع أحد الأبوين الآخر من رؤية ولده.',
 'eg':'شراح الفقه في مصر وتقنين قدري باشا والشيخ أبو زهرة: الغلام إلى أبيه في السابعة والجارية في التاسعة.',
 'f1':'النص المؤسس: آيات صلة الرحم وتحريم قطعها، وأحاديث حق الأب وإثم من يضيع من يعول، وآثار الصحابة في تخيير الغلام بعد التمييز لا قبله.',
 'f2':'فقهاء الحنفية: تنتهي حضانة النساء للغلام إذا استغنى بنفسه في السابعة، وللجارية إذا بلغت أو شارفت البلوغ في التاسعة، ويضم إلى أبيه للتعليم والتأديب.',
 'f3':'فقهاء المالكية: الأب أقوم على تعليم الولد وتأديبه، والحضانة حق للمحضون لا للحاضنة، ولا يمنع الأب من ولده ولا يقطع عن رحمه.',
 'f4':'فقهاء الشافعية: الحضانة فيما دون السبع، وبعدها الكفالة على الأب سواء اختاره الولد أو اختار أمه، فالتعليم والتأديب مما يجب على الأب القيام به.',
 'f5':'فقهاء الحنابلة: التمييز حد الحضانة، والجارية تضم إلى أبيها في السابعة لأنها أسبق نضجا، وصيانة الولد وتعليمه إلى الأب لا إلى الحاضنة.',
'hujaj':'أدلة متضافرة: كل بطاقة تجمع نصوصا منقولة بلفظها من أقسام مختلفة، القرآن والسنة والفقه وفتاوى الأزهر والطب وعلم النفس والدراسات والقضاء والتشريع والمواثيق الدولية، فتلتقي كلها على الحكم نفسه، ولكل نص رقم بطاقته الكاملة.',
 'body':'الطب الحيوي وطب الأسنان وعلم الأحياء التطوري: بين السادسة والثامنة تتبدل أسنان الطفل وتنضج غدته الكظرية ويستقل بطعامه وضبط نفسه، فالسابعة علامة في الجسد كما هي حد في الفقه.',
 'school':'اليونسكو والبيانات العالمية ووزارة التعليم الأمريكية: العالم كله يدخل الطفل المدرسة بين الخامسة والسابعة، ومشاركة الأب في التعليم ترفع تحصيل الولد.',
 'enforce':'قوانين ألمانيا وفرنسا: على الوالدين الامتناع عن كل ما يفسد علاقة الطفل بالآخر، وقضايا اللقاء تنظر أولا وبسرعة، ومن عطل اللقاء غرم أو سجن أو روجعت حضانته.',
 'tamyiz':'قوانين ألمانيا وباكستان ونيجيريا وبنغلاديش والهند وإنجلترا والقانون الكنسي: السابعة حد التمييز والأهلية والمسؤولية، وابن العاشرة يحاسب جنائيا.',
 'f6':'الموسوعات الفقهية والفقه المقارن وعلماء التربية والطب واللغة في الإسلام: السابعة سن التعليم والتأديب، والتمييز هو مناط انتقال الولد إلى أبيه.',
}

# ---------------- helpers ----------------
def txt(x): return H.unescape(re.sub(r'<[^>]+>',' ',x)).replace('  ',' ').strip()
def qr_svg(url):
    q=segno.make(url,error='m'); buf=io.BytesIO()
    q.save(buf,kind='svg',xmldecl=False,svgns=True,svgclass='segno',lineclass='qrline',dark='#000',light='#fff',border=4,scale=1)
    s=buf.getvalue().decode('utf8')
    m=re.search(r'width="(\d+)" height="(\d+)"',s); w,h=m.group(1),m.group(2)
    s=s.replace(f' width="{w}" height="{h}"',f' viewBox="0 0 {w} {h}"',1)
    return s

def ot_size(text,ltr,wide):
    L=len(text)
    if L<=90: return (30 if wide else 27)
    if L<=200: return (26 if wide else 24)
    if L<=320: return (23 if wide else 22)
    return (21 if wide else 20.5)

def add_mn(s):
    """append بالمناصفة after الرعاية المشتركة (any prefix) if not already followed by it."""
    return re.sub(r'(?<![ء-ي])((?:و|ف|ب|ل|ك|ول|وب|فب|فل|وك)?الرعاية المشتركة)(?!\s*(?:<span class="mn">)?بالمناصفة)', r'\1 '+MN, s)

def mn_plain(s):
    return re.sub(r'(?<![ء-ي])((?:و|ف|ب|ل|ك|ول|وب|فب|فل|وك)?الرعاية المشتركة)(?!\s*بالمناصفة)', r'\1 بالمناصفة', s)

def split_sections(h):
    i=h.find('<section class="page'); j=h.rfind('</section>')+len('</section>')
    head,body,tail=h[:i],h[i:j],h[j:]
    secs=[]
    for m in re.finditer(r'<section class="page[^"]*" id="([^"]+)".*?</section>',body,re.S):
        secs.append((m.group(1),m.group(0)))
    return head,secs,tail

# ---------------- card transforms ----------------

# targeted text fixes inside gists (.ot) and derived texts (not verbatim quotations of sources)
TEXT_FIX={
 'A4-027':[('فلا تنفرد الأم بالمميز.','فلا تنفرد الأم بالمميز. والتخيير عند من قال به إنما يكون بين أبوين صحبهما الصغير جميعا، ولا يكون مع تغييب أو إضرار أو حرمان.')],
 'A1-003':[('حين يعقل الصبي ما يختار.','حين يعقل الصبي ما يختار. والتخيير عند من قال به إنما يكون بين أبوين صحبهما الصغير جميعا، ولا يكون مع تغييب أو إضرار أو حرمان.')],
 'A1-015':[('فتنتهي عنده حضانة الأم المنفردة.','فتنتهي عنده حضانة الأم المنفردة. والتخيير عند من قال به إنما يكون بين أبوين صحبهما الصغير جميعا، ولا يكون مع تغييب أو إضرار أو حرمان.')],
 'A1-004':[('لم يعد في حكم من يكفله النساء وحدهن.','لم يعد في حكم من يكفله النساء وحدهن. والتخيير عند من قال به إنما يكون بين أبوين صحبهما الصغير جميعا، ولا يكون مع تغييب أو إضرار أو حرمان.')],
 'A1-005':[('لا تمتد بعد التمييز حتما.','لا تمتد بعد التمييز حتما. والتخيير عند من قال به إنما يكون بين أبوين صحبهما الصغير جميعا، ولا يكون مع تغييب أو إضرار أو حرمان.')],
 'A4-029':[('والرعاية المقسومة حكم.','والرعاية المقسومة حكم. والتخيير عند من قال به إنما يكون بين أبوين صحبهما الصغير جميعا، ولا يكون مع تغييب أو إضرار أو حرمان.')],
 'A1-013':[('فلا وجه لتأخيرها عن الغلام.','فلا وجه لتأخيرها عن الغلام. والتخيير عند من قال به إنما يكون بين أبوين صحبهما الصغير جميعا، ولا يكون مع تغييب أو إضرار أو حرمان.')],
 'A5-087':[('الأدلة تدل على أن الرعاية المشتركة بين الوالدين المنفصلين','الأدلة تدل على أن الرعاية المشتركة '+MN+' بين الوالدين المنفصلين')],
 'A5-101':[('تعرف الرعاية المشتركة بعد الطلاق بأنها','تعرف الوالدية المشتركة بعد الطلاق بأنها')],
 'A5-119':[('ويصرح بأن سلامة الطفل تتقدم على سائر الاعتبارات، ويستثني من الرعاية المشتركة والمتساوية الحالات التي ثبت فيها العنف الأسري أو إساءة معاملة الطفل وتقتضي حمايته من أحد الوالدين أو كليهما.','ويصرح بأن سلامة الطفل تتقدم على سائر الاعتبارات.'),
           ('أصلا قانونيا لا يعدل عنه إلا بثبوت العنف أو الإساءة؛','أصلا قانونيا؛')],
 'A5-134':[('<div class="rt">مراجعة 39 دراسة: المشاركة والموارد وحدود المقارنة</div>','<div class="rt">مراجعة 39 دراسة — أطفال الرعاية المشتركة '+MN+' كأطفال الأسرة المجتمعة</div>'),('شملت الرعاية المشتركة قضاء 30–70% من الوقت','شملت الرعاية المشتركة '+MN+' وما قاربها قضاء 30–70% من الوقت')],
 'A5-135':[('أو في الرعاية المشتركة عن شكاوى','أو في الرعاية المشتركة '+MN+' عن شكاوى')],
 'A5-051':[('(AFCC) في الرعاية المشتركة:','(AFCC) في الرعاية المشتركة '+MN+':')],
 'A5-064':[('لا يبطل نفع الرعاية المشتركة،','لا يبطل نفع الرعاية المشتركة '+MN+'،')],
 'A5-088':[('يرون الرعاية المشتركة نافعة','يرون الرعاية المشتركة '+MN+' نافعة')],
 'A5-098':[('وبإدخال الرعاية المشتركة وتمكين المحاكم من الحكم بالحضانة المشتركة مع خطط رعاية','وبإدخال مفهوم الحضانة المشتركة وتمكين المحاكم من الحكم بها مع خطط رعاية')],
 'A1-026':[('فدل ذلك على أن الرعاية المشتركة ثابتة قبل التخيير','فدل ذلك على أن الرعاية المشتركة '+MN+' ثابتة قبل التخيير'),
           ('Hence shared care is established before the choice','Hence equal shared care is established before the choice'),
           ('<div class="srcl"><b class="sa"><bdi>تحقيق مستنبط','<div class="srcl has-ico">'+flags.icon('heritage')+'<b class="sa"><bdi>تحقيق مستنبط')],
}
OV=json.load(open('/home/claude/work/verify/overlay.json',encoding='utf8')) if os.path.exists('/home/claude/work/verify/overlay.json') else {'ot':{},'links':{},'retire':{},'titles':{}}
def qrow_html(links):
    qcs=[]
    for l in links:
        u=H.escape(l['url'],quote=True)
        qcs.append(f'<div class="qc"><a class="qi" href="{u}" target="_blank" rel="noopener">{qr_svg(l["url"])}\n</a><div class="qt"><div class="ql">{l["label"]}</div><a class="qo" href="{u}" target="_blank" rel="noopener">فتح الدليل ↗</a><div class="qs">{l["site"]}</div><div class="qd">{l["domain"]}</div></div></div>')
    return f'<div class="qrow n{len(qcs)}">{"".join(qcs)}</div>'
def apply_overlay(cid,c):
    o=OV['ot'].get(cid)
    if o:
        t=o['text']; ltr=o['ltr']
        body=('"'+H.escape(t,quote=False)+'"') if ltr else ('«'+t+'»')
        fs=ot_size(t,ltr,False)
        new=f'<div class="sec orig"><div class="ot{" ltr" if ltr else ""}" style="font-size:{fs:g}px">{body}</div></div>'
        c,k=re.subn(r'<div class="sec orig"><div class="ot[^"]*" style="font-size:[\d.]+px">.*?</div></div>',lambda m:new,c,count=1,flags=re.S)
        if not k: print('OV ot miss',cid)
        if o['tt']:
            c=re.sub(r'<div class="sec trs"[^>]*><div class="tt[^"]*">.*?</div></div>',lambda m:f'<div class="sec trs"><div class="tt">{o["tt"]}</div></div>',c,count=1,flags=re.S)
        else:
            c=re.sub(r'(<div class="sec trs"[^>]*><div class="tt wt">)Gist:',r'\1Meaning:',c,count=1)
    for old,nl in OV.get('url_sub',{}).items():
        he=H.escape(old,quote=True)
        if he in c:
            c=re.sub(r'<div class="qc"><a class="qi" href="'+re.escape(he)+r'".*?<div class="qd">[^<]*</div></div></div>',lambda m:qrow_html([nl])[len('<div class="qrow n1">'):-len('</div>')],c,count=1,flags=re.S)
    if cid in OV['titles']:
        c=re.sub(r'<div class="rt">.*?</div>',lambda m:f'<div class="rt">{OV["titles"][cid]}</div>',c,count=1,flags=re.S)
    if cid in OV['links'] and 'class="qrow' not in c:
        c=c.replace('<div class="sec arg">',qrow_html([OV['links'][cid]])+'\n<div class="sec arg">',1)
    return c
def apply_text_fix(cid,c):
    for old,new in TEXT_FIX.get(cid,[]):
        if old not in c: print('TEXT_FIX miss',cid,old[:40])
        c=c.replace(old,new)
    return c

def transform_card(card, meta, links_fix, wide):
    """meta: dict with jurisdiction/category from JSON (may be None)."""
    c=card
    # 1. negative phrases
    c=c.replace(' (دون تاريخ نشر مبين)','').replace('(دون تاريخ نشر مبين)','')
    c=re.sub(r'<div class="note">رابط بحث مؤقت يستبدل برابط مباشر\.</div>','',c)
    # 2. temporary links -> direct
    cid=re.search(r'id="([^"]+)"',c).group(1)
    c=apply_text_fix(cid,c)
    c=apply_overlay(cid,c)
    if cid in links_fix:
        fx=links_fix[cid]
        def repl_qrow(m):
            q=m.group(0)
            q=re.sub(r'href="[^"]*"',f'href="{H.escape(fx["url"],quote=True)}"',q)
            q=re.sub(r'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 \d+ \d+" class="segno">.*?</svg>',qr_svg(fx['url']),q,count=1,flags=re.S)
            q=re.sub(r'<div class="ql">.*?</div>',f'<div class="ql">{fx["label"]}</div>',q,count=1)
            q=re.sub(r'<div class="qs">.*?</div>',f'<div class="qs">{fx["site"]}</div>',q,count=1)
            q=re.sub(r'<div class="qd">.*?</div>',f'<div class="qd">{fx["domain"]}</div>',q,count=1)
            return q
        c=re.sub(r'<div class="qrow n1">.*?</div></div></div>',repl_qrow,c,count=1,flags=re.S)
    # 3. المناصفة (outside .ot and outside QR/links)
    def mn_zone(m):
        return add_mn(m.group(0))
    c=re.sub(r'<div class="st1">.*?</div>',mn_zone,c,count=1,flags=re.S)
    c=re.sub(r'<div class="chips">.*?</div></div>',mn_zone,c,count=1,flags=re.S)
    c=re.sub(r'<div class="rt">.*?</div>',mn_zone,c,count=1,flags=re.S)
    c=re.sub(r'<div class="argt">.*?</div>',mn_zone,c,count=1,flags=re.S)
    c=re.sub(r'<div class="about st">.*?</span></div>',mn_zone,c,count=1,flags=re.S)
    c=re.sub(r'<div class="tt">.*?</div>',mn_zone,c,count=1,flags=re.S)
    # 4. icon into .srcl
    key=None
    if meta: key=flags.key_for(meta.get('jurisdiction',''),meta.get('category',''))
    if not key:
        sj=re.search(r'<span class="sj">(.*?)</span>',c,re.S)
        key=flags.key_for(txt(sj.group(1)) if sj else '')
    if key:
        c=c.replace('<div class="srcl">',f'<div class="srcl has-ico">{flags.icon(key)}',1)
    return c

def set_number(card, n, total, page, pages, secname, wide):
    c=re.sub(r'<div class="num">\d+</div>',f'<div class="num">{n}</div>',card,count=1)
    c=re.sub(r'<span class="fid">.*?</span>',f'<span class="fid">{secname} · بطاقة {n} من {total} · صفحة {page} من {pages}</span>',c,count=1)
    return c

def set_wide(card):
    def f(m):
        cls=m.group(1); fs=float(m.group(2)); body=m.group(3)
        new={27:30,24:26,22:23,20.5:21}.get(fs,fs)
        return f'<div class="ot{cls}" style="font-size:{new:g}px">{body}</div></div>'
    return re.sub(r'<div class="ot([^"]*)" style="font-size:([\d.]+)px">(.*?)</div></div>',f,card,count=1,flags=re.S)

def set_section_class(card, key):
    fam='fiqh' if key in ('f1','f2','f3','f4','f5','f6') else ('west' if key not in ('eg','azhar') else 'fiqh')
    c=re.sub(r'<section class="page fam-\w+ sec-\w+"',f'<section class="page fam-{fam} sec-{key}"',card,count=1)
    return c

# ---------------- new card template ----------------
LOGO_FLAT=None; LOGO_IVORY='<div class="ivory" role="img" aria-label="7 · 9"></div>'
def logo_for(n):
    return LOGO_FLAT if n%2==1 else LOGO_IVORY

def build_card(e, n_hint, wide):
    """e: dict new entry (see new_cards.json)."""
    chips=''.join(f'<span class="chip {cls}">{t}</span>' for cls,t in e['chips'])
    ot_text=e['ot']; ltr=e.get('ltr',True)
    fs=ot_size(txt(ot_text),ltr,wide)
    ot=f'<div class="sec orig"><div class="ot{" ltr" if ltr else ""}" style="font-size:{fs:g}px">{ot_text}</div></div>'
    tt=f'<div class="sec trs"><div class="tt">{e["tt"]}</div></div>' if e.get('tt') else '<div class="sec trs" style="display:none"><div class="tt wt"></div></div>'
    src=e['src']  # dict: author, year, jur, title_latin, where
    sa=f'<b class="sa"><bdi dir="ltr">{H.escape(src["author"])}</bdi></b>' if src.get('latin',True) else f'<b class="sa"><bdi>{src["author"]}</bdi></b>'
    sd=f' <span class="sd">(<bdi>{src["year"]}</bdi>)</span>' if src.get('year') and not src.get('year_in_author') else ''
    parts=[sa+sd]
    if src.get('sw'): parts.append(f'<span class="sw"><bdi>{src["sw"]}</bdi></span>')
    if src.get('jur'): parts.append(f'<span class="sj">{src["jur"]}</span>')
    srcl=' <span class="dot">·</span> '.join(parts)
    if src.get('title_latin'): srcl+=f'<div class="swl" dir="ltr">{H.escape(src["title_latin"])}</div>'
    if src.get('where'): srcl+=f'<div class="sl2"><bdi>{src["where"]}</bdi></div>'
    ico=flags.icon(e['icon']) if e.get('icon') else ''
    srcl=f'<div class="srcl{" has-ico" if ico else ""}">{ico}{srcl}</div>'
    about=f'<div class="about st"><b>عن المصدر:</b> {e["about"]} <span class="lv">درجة الدليل: {e["level"]}</span></div>'
    links=e['links']  # list of dict url,label,site,domain
    qcs=[]
    for l in links:
        u=H.escape(l['url'],quote=True)
        qcs.append(f'<div class="qc"><a class="qi" href="{u}" target="_blank" rel="noopener">{qr_svg(l["url"])}\n</a><div class="qt"><div class="ql">{l["label"]}</div><a class="qo" href="{u}" target="_blank" rel="noopener">فتح الدليل ↗</a><div class="qs">{l["site"]}</div><div class="qd">{l["domain"]}</div></div></div>')
    qrow=f'<div class="qrow n{len(qcs)}">{"".join(qcs)}</div>'
    arg=f'<div class="sec arg"><span class="argl">المضمون: الاستدلال به</span><div class="argt">{e["arg"]}</div></div>'
    key=e['sec']; fam=e.get('fam','west')
    card=(f'<section class="page fam-{fam} sec-{key}" id="{e["id"]}" data-fam="{fam}" data-ax="5">\n'
          f'<div class="strip"><div class="num">0</div><div class="st"><div class="st1">{TITLE_OLD}</div><div class="chips">{chips}</div></div><div class="lgw">{logo_for(n_hint)}</div></div>\n'
          f'<div class="card"><div class="rt">{e["title"]}</div>\n{ot}\n{tt}\n{srcl}{about}\n{qrow}\n{arg}</div>\n'
          f'<div class="slog">لا للمظاهرات والثورات<i></i>لا لسيداو، ولا لتمييز المرأة على الرجل في الإجراءات والقرارات والقوانين<i></i>نعم لصلة الأرحام</div>\n'
          f'<div class="foot2"><span class="fid">x</span></div>\n</section>')
    return card

# ---------------- pages ----------------
def cover_page(base_cover, counts, total, wide, pages=0, njur=53):
    c=base_cover
    if wide:
        c=c.replace('<div style="font-weight: 700; font-size: 70px; line-height: 1.2; color: #1F5FA8">والرعاية المشتركة</div>',
                    '<div style="font-weight: 700; font-size: 70px; line-height: 1.2; color: #1F5FA8">والرعاية المشتركة <span class="mn" style="font-size:74px">بالمناصفة</span></div>')
        c=c.replace('height: 1460px;','min-height: 1460px;')
        i=c.find('<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));')
        j=c.find('<div style="display: flex; justify-content: space-between; align-items: center; padding: 16px 52px; background:')
    else:
        c=c.replace('<div style="font-weight:700;font-size:38px;line-height:1.25;color:#1F5FA8">والرعاية المشتركة</div>',
                    '<div style="font-weight:700;font-size:38px;line-height:1.25;color:#1F5FA8">والرعاية المشتركة <span class="mn" style="font-size:40px">بالمناصفة</span></div>')
        i=c.find('<div style="display:flex;flex-direction:column;gap:9px;padding:14px 18px 14px">')
        j=c.find('<div style="display:flex;gap:28px;padding:12px 18px;background:#EFE9DA')
    assert i>0 and j>i, 'cover tiles not found'
    c=re.sub(r'284 نصا ومصدرا',f'{total} نصا ومصدرا',c)
    c=re.sub(r'(color:\s*#C40000">)284(</div>)',rf'\g<1>{total}\2',c,count=1)
    c=re.sub(r'(line-height:\s*1\.1(?:;\s*color:\s*#182228)?">)53(</div>)',rf'\g<1>{njur}\2',c,count=1)
    c=c.replace('السجل العلمي · الإصدار الأول','السجل العلمي · الإصدار الثاني')
    tiles=[]
    for idx,key in enumerate(ORDER):
        d=SEC[key]; n=counts.get(key,0)
        if wide:
            tiles.append(f'<div style="position: relative; border-radius: 18px; padding: 12px 14px 10px; background: linear-gradient(180deg, rgba(255,255,255,0.85) 0%, rgba(255,255,255,0.15) 48%, rgba(255,255,255,0) 52%), linear-gradient(135deg, {d["g"][0]} 0%, {d["g"][1]} 100%); border: 1.5px solid {d["acc"]}33; box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 6px 16px {d["acc"]}1f; display: flex; gap: 12px; align-items: flex-start; min-height: 108px; box-sizing: border-box">\n'
                         f'<div style="flex: 0 0 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0) 45%), {d["acc"]}; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-family: \'CairoE\', Cairo, sans-serif; font-weight: 700; font-size: 20px; box-shadow: 0 3px 8px {d["acc"]}55">{idx+1:02d}</div>\n'
                         f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px">\n<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px"><div style="font-family: \'CairoE\', Cairo, sans-serif; font-weight: 700; font-size: 19px; line-height: 1.35; color: {d["acc"]}">{add_mn(d["name"])}</div><div style="font-family: \'CairoE\', Cairo, sans-serif; font-weight: 700; font-size: 14px; color: {d["acc"]}; white-space: nowrap; opacity: 0.85">{n} نصا</div></div>\n'
                         f'<div style="font-family: \'NotoArE\', \'Noto Sans Arabic\', sans-serif; font-size: 14px; line-height: 1.6; color: #34464F">{add_mn(d["blurb"])}</div></div></div>')
        else:
            tiles.append(f'<div style="border-radius:14px;padding:8px 10px;background:linear-gradient(180deg,rgba(255,255,255,.85) 0%,rgba(255,255,255,.15) 48%,rgba(255,255,255,0) 52%),linear-gradient(135deg,{d["g"][0]} 0%,{d["g"][1]} 100%);border:1.5px solid {d["acc"]}33;box-shadow:0 4px 10px {d["acc"]}1f;display:flex;gap:8px;align-items:center">\n'
                         f'<div style="flex:0 0 32px;height:32px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 45%),{d["acc"]};color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-family:\'CairoE\', sans-serif;font-weight:700;font-size:14px">{idx+1:02d}</div>\n'
                         f'<div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;gap:8px;align-items:baseline"><div style="font-family:\'CairoE\', sans-serif;font-weight:700;font-size:14.5px;line-height:1.3;color:{d["acc"]}">{add_mn(d["name"])}</div><div style="font-family:\'CairoE\', sans-serif;font-weight:700;font-size:11px;color:{d["acc"]};white-space:nowrap">{n} نصا</div></div>\n'
                         f'<div style="font-family:\'NotoArE\', sans-serif;font-size:11.5px;line-height:1.5;color:#34464F">{add_mn(d["blurb"])}</div></div></div>')
    if wide:
        grid=f'<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; padding: 18px 52px 18px; flex: 1; align-content: center">{"".join(tiles)}</div>\n'
    else:
        grid=f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:12px 18px 12px">{"".join(tiles)}</div>'
    c=c[:i]+grid+c[j:]
    c=re.sub(r'(color:\s*#1F5FA8">)10(</div>)',rf'\g<1>{len(ORDER)}\2',c,count=1)
    c=re.sub(r'الغلاف · صفحة 1 من \d+',f'الغلاف · صفحة 1 من {pages}',c)
    return c

def toc_page(base_toc, counts, pages_start, pages, wide):
    t=base_toc
    i=t.find('<a href="#sec-'); i=t.rfind('<div style=',0,i); j=t.find('<div class="foot2">')
    items=[]
    for idx,key in enumerate(ORDER):
        d=SEC[key]; name=add_mn(d['name']); bl=add_mn(TOC_BLURB[key])
        if wide:
            items.append(f'<a href="#sec-{key}" style="display: grid; grid-template-columns: 90px 1fr 120px; gap: 18px; align-items: start; padding: 12px 0; border-bottom: 1px solid #E3DDD0; text-decoration: none; color: inherit">\n'
                         f'<div style="font-family: \'CairoE\', sans-serif; font-weight: 700; font-size: 44px; line-height: 1; color: {d["acc"]}">{idx+1:02d}</div>\n'
                         f'<div><div style="font-family: \'CairoE\', sans-serif; font-weight: 700; font-size: 24px; line-height: 1.4; color: {d["acc"]}">{name}</div>\n'
                         f'<div style="font-family: \'NotoArE\', sans-serif; font-size: 16px; line-height: 1.7; color: #4A5A61">{bl}</div></div>\n'
                         f'<div style="text-align: left; font-family: \'NotoArE\', sans-serif; font-size: 15px; color: #4A5A61; line-height: 1.8"><div><b style="font-family: \'CairoE\', sans-serif; font-size: 22px; color: {d["acc"]}">{counts[key]}</b> نصا</div><div>من صفحة {pages_start[key]}</div></div></a>')
        else:
            items.append(f'<a href="#sec-{key}" style="display:grid;grid-template-columns:44px 1fr;gap:10px;padding:8px 0;border-bottom:1px solid #E3DDD0;text-decoration:none;color:inherit">\n'
                         f'<div style="font-family:\'CairoE\', sans-serif;font-weight:700;font-size:26px;line-height:1;color:{d["acc"]}">{idx+1:02d}</div>\n'
                         f'<div><div style="font-family:\'CairoE\', sans-serif;font-weight:700;font-size:17px;line-height:1.4;color:{d["acc"]}">{name} <span style="font-size:12px;color:#4A5A61;font-weight:400">· {counts[key]} نصا · من صفحة {pages_start[key]}</span></div>\n'
                         f'<div style="font-family:\'NotoArE\', sans-serif;font-size:12.5px;line-height:1.7;color:#4A5A61">{bl}</div></div></a>')
    wrap_open='<div style="margin-top: 18px">' if wide else '<div style="margin-top:8px">'
    t=t[:i]+wrap_open+''.join(items)+'</div>'+t[j:]
    t=t.replace(TITLE_OLD,TITLE_OLD+' '+MN)
    t=re.sub(r'<span class="fid">.*?</span>',f'<span class="fid">الفهرس · صفحة 2 من {pages}</span>',t)
    return t

def opener_page(base_opener, key, idx, count, page, pages, logo_svg, wide=False):
    d=SEC[key]; name=add_mn(d['name']); blurb=add_mn(OPEN_BLURB[key])
    if not wide:
        return (f'<section class="page opener" id="sec-{key}"><div style="min-height:700px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;border-top:10px solid {d["acc"]};padding:22px 16px 14px;border-radius:0 0 18px 18px;background:linear-gradient(180deg,rgba(255,255,255,.75) 0%,rgba(255,255,255,0) 40%),linear-gradient(160deg,{d["g"][0]} 0%,{d["g"][1]} 100%)">\n'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div style="font-family:\'NotoArE\', sans-serif;font-size:14px;letter-spacing:1px;color:#4A5A61">القسم {AR_ORD[idx]}</div>\n'
            f'<div style="font-family:\'CairoE\', sans-serif;font-weight:700;font-size:120px;line-height:1;color:{d["acc"]}">{idx+1:02d}</div></div><div>{logo_svg.replace("width:132px;height:132px","width:130px;height:130px")}</div></div>\n'
            f'<div><div style="font-family:\'CairoE\', sans-serif;font-weight:700;font-size:38px;line-height:1.3;color:{d["acc"]}">{name}</div>\n'
            f'<div style="height:4px;width:110px;background:{d["acc"]};margin:10px 0 12px"></div>\n'
            f'<div style="font-family:\'NotoArE\', sans-serif;font-size:16px;line-height:1.9;color:#34464F">{blurb}</div>\n'
            f'<div style="font-family:\'CairoE\', sans-serif;font-weight:700;font-size:19px;color:{d["acc"]};margin-top:10px">{count} {"حجة جامعة" if key=="hujaj" else "نصا ومصدرا"}</div></div></div>\n'
            f'<div class="foot2"><span class="fid">{name} · صفحة {page} من {pages}</span></div></section>')
    return (f'<section class="page opener" id="sec-{key}"><div style="min-height: 640px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; border-top: 14px solid {d["acc"]}; padding: 40px 24px 16px; border-radius: 0 0 22px 22px; background: linear-gradient(180deg, rgba(255,255,255,0.75) 0%, rgba(255,255,255,0) 40%), linear-gradient(160deg, {d["g"][0]} 0%, {d["g"][1]} 100%)">\n'
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start">\n<div><div style="font-family: \'NotoArE\', sans-serif; font-size: 18px; letter-spacing: 2px; color: #4A5A61">القسم {AR_ORD[idx]}</div>\n'
            f'<div style="font-family: \'CairoE\', sans-serif; font-weight: 700; font-size: 200px; line-height: 1; color: {d["acc"]}">{idx+1:02d}</div></div>\n<div style="opacity: 1">{logo_svg.replace("width:132px;height:132px","width:220px;height:220px")}</div></div>\n'
            f'<div><div style="font-family: \'CairoE\', sans-serif; font-weight: 700; font-size: 66px; line-height: 1.3; color: {d["acc"]}">{name}</div>\n'
            f'<div style="height: 5px; width: 160px; background: {d["acc"]}; margin: 14px 0 18px"></div>\n'
            f'<div style="font-family: \'NotoArE\', sans-serif; font-size: 22px; line-height: 1.9; color: #34464F; max-width: 820px">{blurb}</div>\n'
            f'<div style="font-family: \'CairoE\', sans-serif; font-weight: 700; font-size: 26px; color: {d["acc"]}; margin-top: 14px">{count} {"حجة جامعة" if key=="hujaj" else "نصا ومصدرا"}</div></div></div>\n'
            f'<div class="foot2"><span class="fid">{name} · صفحة {page} من {pages}</span></div></section>')

def stats_page(base_stats, cards_meta, counts, page, pages):
    """cards_meta: list of dicts with sec,supports,strength,jurisdiction."""
    def table(title, counter):
        items=counter.most_common(); mx=items[0][1] if items else 1
        rows=''.join(f'<tr><td>{k}</td><td class="n">{v}</td><td><div class="bar" style="width:{max(2,round(v*100/mx))}%"></div></td></tr>' for k,v in items)
        return f'<div class="tb"><h3>{title}</h3><table>{rows}</table></div>'
    c1=collections.Counter();
    for key in ORDER: c1[add_mn(SEC[key]['name'])]=counts[key]
    c1=collections.Counter(dict(c1))
    SUP={'7':'سن السابعة','9':'سن التاسعة','childhood_ends_at_puberty':'انتهاء الطفولة بالبلوغ','shared_parenting':'الرعاية المشتركة بالمناصفة','silat_al_rahim':'صلة الرحم','counter':'حجة الخصم'}
    STR={'explicit_7':'نص في السابعة','explicit_9':'نص في التاسعة','explicit':'دلالة صريحة','indirect':'دلالة بالاستنباط','contextual':'دلالة سياقية'}
    c2=collections.Counter(); c3=collections.Counter(); c4=collections.Counter()
    for m in cards_meta:
        for s_ in m.get('supports',[]): c2[SUP.get(s_,s_)]+=1
        c3[STR.get(m.get('strength',''),m.get('strength',''))]+=1
        j=(m.get('jurisdiction') or '').split('—')[0].split('؛')[0].strip()
        if j: c4[j]+=1
    s=base_stats
    i=s.find('<div class="tb">'); j=s.find('<div class="foot2">')
    body=table('بحسب القسم',c1)+table('بحسب ما يدل عليه النص',c2)+table('بحسب قوة الدلالة',c3)+table('بحسب الدولة أو الهيئة أو المذهب',collections.Counter(dict(c4.most_common(28))))
    s=s[:i]+body+s[j:]
    s=re.sub(r'<span class="fid">.*?</span>',f'<span class="fid">الإحصاءات · صفحة {page} من {pages}</span>',s)
    return s

EXTRA_CSS=('.sec-military{--acc:#37474F;--accd:#263238;--tint:#ECEFF1;--tint2:#F5F7F8}.sec-enforce{--acc:#0E6E55;--accd:#094D3B;--tint:#E2F4EE;--tint2:#F1FAF6}.sec-fear{--acc:#6A1B9A;--accd:#4A148C;--tint:#F3E5F5;--tint2:#FAF2FB}.sec-azhar{--acc:#7B2D26;--accd:#561F1A;--tint:#F8EDEB;--tint2:#FCF6F5}.sec-body{--acc:#00796B;--accd:#004D40;--tint:#E0F2F1;--tint2:#F2FAF9}.sec-school{--acc:#D81B60;--accd:#9C1145;--tint:#FCE4EC;--tint2:#FEF4F7}.sec-tamyiz{--acc:#1A237E;--accd:#0D1452;--tint:#E8EAF6;--tint2:#F5F6FC}.sec-hujaj{--acc:#8B1E5B;--accd:#601440;--tint:#FBEAF3;--tint2:#FDF5F9}.sec-hujaj .hq{margin:0 0 .55em;padding:0 0 .45em;border-bottom:1px dashed #E2C3D4}.sec-hujaj .hq:last-child{border-bottom:0;margin-bottom:0}.sec-hujaj .hs{display:block;font-family:CairoE,sans-serif;font-weight:700;font-size:.62em;color:var(--accd);margin-top:.15em}.sec-hujaj .hsep{display:none}.sec-hujaj .hs .ico{display:inline-block;width:22px;height:15px;vertical-align:-3px;margin-left:5px;filter:drop-shadow(0 1px 1px rgba(0,0,0,.18))}'
           '.srcl.has-ico{position:relative;padding-left:40px}.srcl .ico{position:absolute;left:9px;top:50%;transform:translateY(-50%);width:26px;height:17.3px;display:block;filter:drop-shadow(0 1px 1px rgba(0,0,0,.18))}'
           '.mn{font-family:\'AmiriE\',\'CairoE\',serif;font-weight:700;font-size:1.12em;line-height:1;color:#C40000}'
           '.chip .mn{font-size:1.05em;color:inherit}.st1 .mn{color:inherit}.fid .mn{font-size:1em;color:inherit}.argt .mn,.about .mn,.tt .mn{color:#9A0000}'
           '.sec-f1{--acc:#0F5C3A;--accd:#0A3F28;--tint:#E6F3EC;--tint2:#F3FAF6}.sec-f2{--acc:#1F6B5C;--accd:#154A40;--tint:#E3F3EC;--tint2:#F3FAF6}'
           '.sec-f3{--acc:#3E7A3A;--accd:#2A5427;--tint:#E9F3E6;--tint2:#F5FAF3}.sec-f4{--acc:#2A8A7A;--accd:#1B5E53;--tint:#E4F4F1;--tint2:#F3FAF8}'
           '.sec-f5{--acc:#4E6B2F;--accd:#354A20;--tint:#EDF2E4;--tint2:#F7FAF2}.sec-f6{--acc:#6B5E2A;--accd:#4A411D;--tint:#F3F0E3;--tint2:#FAF8F1}')

def fiqh_subkey(meta):
    j=(meta or {}).get('jurisdiction','') ; cat=(meta or {}).get('category','')
    if 'الحنفي' in j: return 'f2'
    if 'المالكي' in j: return 'f3'
    if 'الشافعي' in j: return 'f4'
    if 'الحنبلي' in j: return 'f5'
    if any(k in j for k in ['القرآن','السنة','آثار','شروح الحديث','التفسير']) or cat in ('قرآن','حديث','أثر','حديث وشرح','تفسير'): return 'f1'
    return 'f6'


MOVE={'A5-215':'enforce','A5-216':'enforce','A5-217':'enforce','A5-212':'fear','A2-114':'fear','A5-157':'tamyiz','A5-158':'tamyiz','A5-161':'tamyiz','A4-058':'school','A2-072':'body','A2-042':'body','A2-043':'body'}
def _top_rank():
    try:
        D=json.load(open('/home/claude/work/build/nuqul_7_9.json',encoding='utf8'))
        num2id={x['card_number']:x['id'] for x in D['entries'] if x.get('card_number')}
        T=json.load(open('/home/claude/work/build/tools/top50.json',encoding='utf8'))
        return {(r.get('id') or num2id.get(r['n'])):r['rank'] for r in T}
    except Exception: return {}
TOPRANK=_top_rank()
LVT=[('القرآن',0),('قرآن',0),('حديث',1),('فتوى رسمية',2),('محكمة عليا',3),('قضاء دولي',3),('معاهدة',4),('تشريع',4),('نص قانوني',4),('تعريف رسمي',5),('إحصاء رسمي',5),('تحليل جامع',6),('مراجعة منهجية',6),('مراجعة منظمة',6),('سجلات',7),('متابعة وطنية',7),('قرار برلماني',8),('تقرير رسمي',8),('بيان طبي',8),('إرشاد رسمي',8)]
# manual strength boost: placed right after the top-50 cards of their section, in this order
BOOST={k:n for n,k in enumerate(dict.fromkeys(['A4-125','A4-126','A4-124','A2-124','A2-125','A5-215','A5-220','A5-217','A5-221','A5-218','A5-222','A5-219','A5-216','A2-115','A2-117','A2-116','A5-212','A2-119','A2-118','A4-115','A4-114','A4-116','A4-117','A5-212','A5-213','A1-116','A2-114','A4-118','A5-214']))}
def strength_key(i, m, pos):
    m=m or {}
    lv=(m.get('evidence_level') or m.get('level') or '')
    tier=next((t for k,t in LVT if k in lv),9)
    st=m.get('strength','')
    return (0 if i in TOPRANK else (1 if i in BOOST else 2), TOPRANK.get(i,BOOST.get(i,999)), 0 if st in ('explicit_7','explicit_9') else 1, tier, pos)

def main():
    hm,secs_m,tail_m=split_sections(open(BASE_M,encoding='utf8').read())
    hw,secs_w,tail_w=split_sections(open(BASE_W,encoding='utf8').read())
    global LOGO_FLAT
    data=json.load(open(JSON)); META={e['id']:e for e in data['entries']}
    links_fix=json.load(open('/home/claude/work/links_fix.json')) if os.path.exists('/home/claude/work/links_fix.json') else {}
    new=json.load(open('/home/claude/work/new_cards.json')) if os.path.exists('/home/claude/work/new_cards.json') else []
    new=[e for e in new if e['id'] not in OV['retire']]
    # base pages
    base={i:h for i,h in secs_m}
    LOGO_FLAT=re.search(r'<div class="lgw">(<svg.*?</svg>)</div>',base['A5-113'],re.S).group(1)
    # group existing cards
    groups=collections.OrderedDict((k,[]) for k in ORDER)
    replaced={e['id']:e for e in new}
    for i,h in secs_m:
        if not re.match(r'A\d-\d{3}',i): continue
        if i in OV['retire']: continue
        key=re.search(r'sec-(\w+)',h).group(1)
        if key=='fiqh': key=fiqh_subkey(META.get(i))
        key=MOVE.get(i,key)
        if i in replaced: groups[key].append(('new',i,replaced.pop(i)))  # old card replaced in place
        else: groups[key].append(('old',i,h))
    for e in new:
        if e['id'] in replaced: groups[MOVE.get(e['id'],e['sec'])].append(('new',e['id'],e))
    # strongest first inside every section (the knockout section keeps its composed order)
    for k in groups:
        if k=='hujaj': continue
        idx={i:n for n,(kind,i,h) in enumerate(groups[k])}
        groups[k].sort(key=lambda t: strength_key(t[1], META.get(t[1]) if t[0]=='old' else t[2], idx[t[1]]))
    # ordering of new within section: append at end (keeps old order)
    counts={k:len(v) for k,v in groups.items()}; total=sum(counts.values())
    # page numbering: cover=1, toc=2, then per section opener + cards, stats last
    pages=2+sum(1+counts[k] for k in ORDER)+1
    out_m=[]; out_w=[]; n=0; page=2; pages_start={}; cards_meta=[]; NUMOF={}
    opener_tpl=base['sec-psy']
    for idx,key in enumerate(ORDER):
        page+=1; pages_start[key]=page
        out_m.append(opener_page(opener_tpl,key,idx,counts[key],page,pages,LOGO_FLAT,False)); out_w.append(opener_page(opener_tpl,key,idx,counts[key],page,pages,LOGO_FLAT,True))
        for kind,i,h in groups[key]:
            n+=1; page+=1; NUMOF[i]=n
            if kind=='old':
                cm=transform_card(h,META.get(i),links_fix,False)
                cm=set_section_class(cm,key)
                cm=set_number(cm,n,total,page,pages,add_mn(SEC[key]['name']),False)
                cw=set_wide(cm)
                meta=META.get(i,{}); cards_meta.append(dict(sec=key,supports=meta.get('supports',[]),strength=meta.get('strength',''),jurisdiction=meta.get('jurisdiction','')))
            else:
                def _rn(o):
                    if isinstance(o,str): return re.sub(r'\{N:(A\d-\d{3})\}',lambda m:str(NUMOF[m.group(1)]),o)
                    if isinstance(o,list): return [_rn(x) for x in o]
                    if isinstance(o,dict): return {k:_rn(v) for k,v in o.items()}
                    return o
                e=_rn(h); e=dict(e); e['sec']=key; cm=build_card(e,n,False)
                cm=set_number(cm,n,total,page,pages,add_mn(SEC[key]['name']),False)
                cm=re.sub(r'<div class="st1">.*?</div>',lambda m:add_mn(m.group(0)),cm,count=1)
                cm=re.sub(r'<div class="chips">.*?</div></div>',lambda m:add_mn(m.group(0)),cm,count=1,flags=re.S)
                cm=re.sub(r'<div class="rt">.*?</div>',lambda m:add_mn(m.group(0)),cm,count=1,flags=re.S)
                cm=re.sub(r'<div class="argt">.*?</div>',lambda m:add_mn(m.group(0)),cm,count=1,flags=re.S)
                cm=re.sub(r'<div class="about st">.*?</span></div>',lambda m:add_mn(m.group(0)),cm,count=1,flags=re.S)
                cw=set_wide(cm)
                cards_meta.append(dict(sec=key,supports=e.get('supports',['shared_parenting']),strength=e.get('strength','explicit'),jurisdiction=e.get('jurisdiction','')))
            out_m.append(cm); out_w.append(cw)
    page+=1
    st=stats_page(base['stats'],cards_meta,counts,page,pages)
    njur=len(set((m.get('jurisdiction') or '').split('—')[0].split('؛')[0].strip() for m in cards_meta if m.get('jurisdiction')))
    cov=cover_page(base['cover'],counts,total,False,pages,njur)
    toc=toc_page(base['toc'],counts,pages_start,pages,False)
    # wide cover/toc: base wide versions
    basew={i:h for i,h in secs_w}
    covw=cover_page(basew['cover'],counts,total,True,pages,njur); tocw=toc_page(basew['toc'],counts,pages_start,pages,True)
    css_extra='<style>'+EXTRA_CSS+'</style>'
    htm=hm.replace('</head>',css_extra+'</head>',1)+cov+toc+''.join(out_m)+st+tail_m
    htw=hw.replace('</head>',css_extra+'</head>',1)+covw+tocw+''.join(out_w)+st+tail_w
    htm=htm.replace(f'<title>{TITLE_OLD}',f'<title>{TITLE_OLD} بالمناصفة')
    htw=htw.replace(f'<title>{TITLE_OLD}',f'<title>{TITLE_OLD} بالمناصفة')
    # plain-language pass (jargon -> clear wording); verify heritage quotations untouched
    def fiqh_ots(h): return re.findall(r'<section class="page fam-fiqh[^"]*"[^>]*>.*?<div class="ot[^"]*"[^>]*>(.*?)</div></div>',h,re.S)
    before=fiqh_ots(htm); htm=plain(htm); htw=plain(htw); after=fiqh_ots(htm)
    assert before==after, 'plain() altered a heritage quotation'
    print('jargon leftovers:', leftovers(re.sub(r'<[^>]+>',' ',htm)))
    open(f'{OUT}/NUQUL_7_9_CARDS_MOBILE.html','w',encoding='utf8').write(htm)
    open(f'{OUT}/NUQUL_7_9_CARDS.html','w',encoding='utf8').write(htw)
    json.dump(dict(counts=counts,total=total,pages=pages,pages_start=pages_start,order=ORDER),open(f'{OUT}/layout.json','w'),ensure_ascii=False,indent=1)
    print('total cards',total,'pages',pages,counts)

if __name__=='__main__': main()
