# -*- coding: utf-8 -*-
"""Tiny inline-SVG icons: national flags (public symbols, simplified at icon size),
generic globe/book icons. viewBox 0 0 30 20."""
import math

def _wrap(inner, title):
    return (f'<svg class="ico" viewBox="0 0 30 20" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title}">'
            f'<clipPath id="fc"><rect width="30" height="20" rx="2"/></clipPath><g clip-path="url(#fc)">{inner}</g>'
            f'<rect x=".3" y=".3" width="29.4" height="19.4" rx="2" fill="none" stroke="rgba(0,0,0,.35)" stroke-width=".6"/></svg>')

def _h(colors):  # horizontal stripes equal
    n=len(colors); h=20/n
    return ''.join(f'<rect y="{i*h:.2f}" width="30" height="{h:.2f}" fill="{c}"/>' for i,c in enumerate(colors))
def _v(colors):
    n=len(colors); w=30/n
    return ''.join(f'<rect x="{i*w:.2f}" width="{w:.2f}" height="20" fill="{c}"/>' for i,c in enumerate(colors))
def _nordic(bg, cross, inner=None):
    s=f'<rect width="30" height="20" fill="{bg}"/><rect x="8" width="4" height="20" fill="{cross}"/><rect y="8" width="30" height="4" fill="{cross}"/>'
    if inner: s+=f'<rect x="9" width="2" height="20" fill="{inner}"/><rect y="9" width="30" height="2" fill="{inner}"/>'
    return s
def _star(cx,cy,r,fill):
    pts=[]
    for k in range(10):
        a=-math.pi/2+k*math.pi/5; rr=r if k%2==0 else r*0.4
        pts.append(f'{cx+rr*math.cos(a):.2f},{cy+rr*math.sin(a):.2f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'
def _uk(scale=1.0, ox=0, oy=0):
    g=(f'<rect width="30" height="20" fill="#012169"/>'
       f'<path d="M0,0 L30,20 M30,0 L0,20" stroke="#fff" stroke-width="4"/>'
       f'<path d="M0,0 L30,20 M30,0 L0,20" stroke="#C8102E" stroke-width="1.6"/>'
       f'<rect x="12" width="6" height="20" fill="#fff"/><rect y="7" width="30" height="6" fill="#fff"/>'
       f'<rect x="13.3" width="3.4" height="20" fill="#C8102E"/><rect y="8.3" width="30" height="3.4" fill="#C8102E"/>')
    return f'<g transform="translate({ox},{oy}) scale({scale})">{g}</g>'
def _globe(bg='#DCEBF7', ink='#2A5D8F'):
    return (f'<rect width="30" height="20" fill="{bg}"/><circle cx="15" cy="10" r="7.5" fill="#fff" stroke="{ink}" stroke-width="1"/>'
            f'<ellipse cx="15" cy="10" rx="3.2" ry="7.5" fill="none" stroke="{ink}" stroke-width=".8"/>'
            f'<path d="M7.5,10 H22.5 M9,6 H21 M9,14 H21" stroke="{ink}" stroke-width=".8" fill="none"/>')
def _book(c1, c2, letter=''):
    s=(f'<rect width="30" height="20" fill="#FBF8F1"/>'
       f'<path d="M4,4 Q10,2.5 15,4.5 V17 Q10,15 4,16.5 Z" fill="{c1}"/><path d="M26,4 Q20,2.5 15,4.5 V17 Q20,15 26,16.5 Z" fill="{c2}"/>'
       f'<path d="M15,4.5 V17" stroke="#fff" stroke-width=".8"/>'
       f'<path d="M6,7 Q10,6 13,7 M6,9.5 Q10,8.5 13,9.5 M6,12 Q10,11 13,12 M17,7 Q20,6 24,7 M17,9.5 Q20,8.5 24,9.5 M17,12 Q20,11 24,12" stroke="rgba(255,255,255,.75)" stroke-width=".7" fill="none"/>')
    return s

F = {}
F['us'] = _h(['#B22234','#fff']*6+['#B22234']) + '<rect width="12" height="10.8" fill="#3C3B6E"/>' + ''.join(f'<circle cx="{1+c*2}" cy="{1+r*1.2}" r=".45" fill="#fff"/>' for r in range(9) for c in range(6 if r%2==0 else 5)).replace('cx="1','cx="1')  # dot field
F['uk'] = _uk()
F['se'] = _nordic('#006AA7','#FECC02')
F['dk'] = _nordic('#C8102E','#fff')
F['no'] = _nordic('#BA0C2F','#fff','#00205B')
F['fi'] = _nordic('#fff','#002F6C')
F['is'] = _nordic('#02529C','#fff','#DC1E35')
F['de'] = _h(['#000','#DD0000','#FFCE00'])
F['at'] = _h(['#ED2939','#fff','#ED2939'])
F['nl'] = _h(['#AE1C28','#fff','#21468B'])
F['ru'] = _h(['#fff','#0039A6','#D52B1E'])
F['fr'] = _v(['#0055A4','#fff','#EF4135'])
F['it'] = _v(['#009246','#fff','#CE2B37'])
F['be'] = _v(['#000','#FDDA24','#EF3340'])
F['ie'] = _v(['#169B62','#fff','#FF883E'])
F['ch'] = '<rect width="30" height="20" fill="#D52B1E"/><rect x="13" y="4" width="4" height="12" fill="#fff"/><rect x="9" y="8" width="12" height="4" fill="#fff"/>'
F['es'] = '<rect width="30" height="20" fill="#AA151B"/><rect y="5" width="30" height="10" fill="#F1BF00"/>'
F['pt'] = '<rect width="30" height="20" fill="#FF0000"/><rect width="12" height="20" fill="#006600"/><circle cx="12" cy="10" r="4" fill="#FFE600"/><circle cx="12" cy="10" r="2.2" fill="#fff" stroke="#FF0000" stroke-width="1"/>'
F['ca'] = '<rect width="30" height="20" fill="#fff"/><rect width="7.5" height="20" fill="#D80621"/><rect x="22.5" width="7.5" height="20" fill="#D80621"/><path d="M15,3.5 L16.2,6 L18,5.2 L17.3,8 L19.5,8.3 L17.5,10.2 L18.8,12.5 L15.8,12 L15,15.5 L14.2,12 L11.2,12.5 L12.5,10.2 L10.5,8.3 L12.7,8 L12,5.2 L13.8,6 Z" fill="#D80621"/>'
F['au'] = '<rect width="30" height="20" fill="#00008B"/>' + _uk(0.5) + _star(22.5,5,2.2,'#fff') + _star(7.5,15,2.4,'#fff') + ''.join(_star(x,y,1,'#fff') for x,y in [(21,12),(26,9),(25,16),(19,9)])
F['nz'] = '<rect width="30" height="20" fill="#00247D"/>' + _uk(0.5) + ''.join(_star(x,y,1.4,'#CC142B') for x,y in [(22,7),(25,10.5),(21,13),(23,16.5)])
F['br'] = '<rect width="30" height="20" fill="#009C3B"/><polygon points="15,2 27,10 15,18 3,10" fill="#FFDF00"/><circle cx="15" cy="10" r="4.5" fill="#002776"/><path d="M11,9.2 Q15,8 19,10.2" stroke="#fff" stroke-width=".9" fill="none"/>'
F['ar'] = _h(['#74ACDF','#fff','#74ACDF']) + '<circle cx="15" cy="10" r="2" fill="#F6B40E"/>'
F['cl'] = '<rect width="30" height="20" fill="#fff"/><rect y="10" width="30" height="10" fill="#D52B1E"/><rect width="10" height="10" fill="#0039A6"/>' + _star(5,5,2.5,'#fff')
F['jp'] = '<rect width="30" height="20" fill="#fff"/><circle cx="15" cy="10" r="5.5" fill="#BC002D"/>'
F['in'] = _h(['#FF9933','#fff','#138808']) + '<circle cx="15" cy="10" r="2.6" fill="none" stroke="#000080" stroke-width=".9"/><circle cx="15" cy="10" r=".6" fill="#000080"/>'
F['il'] = '<rect width="30" height="20" fill="#fff"/><rect y="2.5" width="30" height="2.5" fill="#0038B8"/><rect y="15" width="30" height="2.5" fill="#0038B8"/><polygon points="15,5.8 18.4,11.6 11.6,11.6" fill="none" stroke="#0038B8" stroke-width=".9"/><polygon points="15,14.2 18.4,8.4 11.6,8.4" fill="none" stroke="#0038B8" stroke-width=".9"/>'
F['kr'] = '<rect width="30" height="20" fill="#fff"/><path d="M11,10 A4,4 0 0 1 19,10 Z" fill="#C60C30"/><path d="M19,10 A4,4 0 0 1 11,10 Z" fill="#003478"/><circle cx="13" cy="10" r="2" fill="#C60C30"/><circle cx="17" cy="10" r="2" fill="#003478"/><path d="M4,5 L7,3 M4,6.5 L7,4.5 M4,8 L7,6 M23,14 L26,12 M23,15.5 L26,13.5 M23,17 L26,15" stroke="#000" stroke-width=".9"/>'
F['cn'] = '<rect width="30" height="20" fill="#DE2910"/>' + _star(5,5,3,'#FFDE00') + ''.join(_star(x,y,1,'#FFDE00') for x,y in [(10,2.5),(12,5),(12,8),(10,10.5)])
F['hk'] = '<rect width="30" height="20" fill="#DE2910"/>' + ''.join(f'<ellipse cx="15" cy="7.2" rx="1.6" ry="3.2" fill="#fff" transform="rotate({k*72} 15 10)"/>' for k in range(5))
F['eg'] = _h(['#CE1126','#fff','#000']) + '<path d="M15,7 L17.4,9 L16.6,12.2 L13.4,12.2 L12.6,9 Z" fill="#C09300"/>'
F['ae'] = _h(['#00732F','#fff','#000']) + '<rect width="8" height="20" fill="#FF0000"/>'
F['kw'] = _h(['#007A3D','#fff','#CE1126']) + '<polygon points="0,0 8,5 8,15 0,20" fill="#000"/>'
F['sa'] = '<rect width="30" height="20" fill="#006C35"/><rect x="9" y="12.5" width="12" height="1.4" fill="#fff"/><path d="M9,6 Q12,4 15,7 Q18,4 21,7" stroke="#fff" stroke-width="1.2" fill="none"/>'
F['sd'] = _h(['#D21034','#fff','#000']) + '<polygon points="0,0 10,10 0,20" fill="#007229"/>'
F['om'] = _h(['#fff','#DB161B','#008000']) + '<rect width="8" height="20" fill="#DB161B"/>'
F['ye'] = _h(['#CE1126','#fff','#000'])
F['my'] = ''.join(f'<rect y="{i*20/14:.2f}" width="30" height="{20/14:.2f}" fill="{"#CC0001" if i%2==0 else "#fff"}"/>' for i in range(14)) + '<rect width="15" height="11.4" fill="#010066"/><circle cx="6" cy="5.7" r="3.2" fill="#FFCC00"/><circle cx="7" cy="5.7" r="2.8" fill="#010066"/>' + _star(10.5,5.7,2,'#FFCC00')
F['cz'] = _h(['#fff','#D7141A']) + '<polygon points="0,0 15,10 0,20" fill="#11457E"/>'
F['pl'] = _h(['#fff','#DC143C'])
F['ph'] = _h(['#0038A8','#CE1126']) + '<polygon points="0,0 13,10 0,20" fill="#fff"/><circle cx="4.5" cy="10" r="2" fill="#FCD116"/>'
F['za'] = '<rect width="30" height="20" fill="#fff"/><rect width="30" height="6.5" fill="#E03C31"/><rect y="13.5" width="30" height="6.5" fill="#001489"/><path d="M0,0 L12,10 L0,20 Z" fill="#000"/><path d="M0,2 L10,10 L0,18 M12,10 H30" stroke="#007749" stroke-width="4" fill="none"/>'
F['mx'] = _v(['#006847','#fff','#CE1126'])
F['tr'] = '<rect width="30" height="20" fill="#E30A17"/><circle cx="11" cy="10" r="5" fill="#fff"/><circle cx="12.3" cy="10" r="4" fill="#E30A17"/>' + _star(17.5,10,2,'#fff')
F['va'] = '<rect width="30" height="20" fill="#fff"/><rect width="15" height="20" fill="#FFE000"/><path d="M19,6 L26,13 M26,6 L19,13" stroke="#B8860B" stroke-width="1.6"/><circle cx="19" cy="6" r="1.6" fill="#B8860B"/><circle cx="26" cy="6" r="1.6" fill="#B8860B"/>'
F['eu'] = '<rect width="30" height="20" fill="#003399"/>' + ''.join(_star(15+6.5*math.cos(k*math.pi/6),10+6.5*math.sin(k*math.pi/6),1,'#FFCC00') for k in range(12))
F['un'] = _globe('#5B92E5','#fff').replace('fill="#fff" stroke="#fff"','fill="#5B92E5" stroke="#fff"')
F['afr'] = _globe('#1B8A3E','#fff').replace('fill="#fff" stroke="#fff"','fill="#1B8A3E" stroke="#fff"')
F['world'] = _globe()
F['americas'] = _globe('#EAF2F8','#1F5FA8')
# books
F['quran'] = _book('#8C6A1E','#B8923C')
F['sunnah'] = _book('#1F6B5C','#2E8B73')
F['hanafi'] = _book('#1F5FA8','#3E7BC4')
F['maliki'] = _book('#7E3A12','#B4541A')
F['shafii'] = _book('#17697A','#2A8A9E')
F['hanbali'] = _book('#154A40','#1F6B5C')
F['heritage'] = _book('#4A5A61','#6B7C84')
F['egbook'] = _book('#26333A','#3A4B52')
F['book'] = _book('#3F3370','#5B4B9A')

NAMES = {'us':'الولايات المتحدة','uk':'المملكة المتحدة','se':'السويد','dk':'الدنمارك','no':'النرويج','fi':'فنلندا','is':'آيسلندا','de':'ألمانيا','at':'النمسا','nl':'هولندا','ru':'روسيا','fr':'فرنسا','it':'إيطاليا','be':'بلجيكا','ie':'أيرلندا','ch':'سويسرا','es':'إسبانيا','pt':'البرتغال','ca':'كندا','au':'أستراليا','nz':'نيوزيلندا','br':'البرازيل','ar':'الأرجنتين','cl':'تشيلي','jp':'اليابان','in':'الهند','il':'إسرائيل','kr':'كوريا الجنوبية','cn':'الصين','hk':'هونغ كونغ','eg':'مصر','ae':'الإمارات','kw':'الكويت','sa':'السعودية','sd':'السودان','om':'عمان','ye':'اليمن','my':'ماليزيا','cz':'التشيك','pl':'بولندا','ph':'الفلبين','za':'جنوب إفريقيا','mx':'المكسيك','tr':'تركيا','va':'الفاتيكان','eu':'أوروبا','un':'الأمم المتحدة','afr':'إفريقيا','world':'عالمي','americas':'الأمريكتان','quran':'القرآن الكريم','sunnah':'السنة النبوية','hanafi':'المذهب الحنفي','maliki':'المذهب المالكي','shafii':'المذهب الشافعي','hanbali':'المذهب الحنبلي','heritage':'التراث الإسلامي','egbook':'مصر','book':'كتاب'}

def icon(key):
    return _wrap(F[key], NAMES.get(key,key))

KW = [  # order matters: more specific first
 ('المذهب الحنفي','hanafi'),('فقه حنفي','hanafi'),('المذهب المالكي','maliki'),('المذهب الشافعي','shafii'),('المذهب الحنبلي','hanbali'),
 ('القرآن','quran'),('التفسير','quran'),('السنة','sunnah'),('شروح الحديث','sunnah'),('آثار الصحابة','sunnah'),('حديث','sunnah'),
 ('التراث التربوي','heritage'),('معاجم','heritage'),('الفقه المقارن','heritage'),('المذهب المقارن','heritage'),('الطب الإسلامي','heritage'),('الكويت','kw'),
 ('المحكمة الأوروبية','eu'),('مجلس أوروبا','eu'),('الاتحاد الأوروبي','eu'),('الاتحاد الإفريقي','afr'),('منظمة الصحة','un'),('الأمم المتحدة','un'),('اليونيسف','un'),('يونيسف','un'),('اليونسكو','un'),
 ('الولايات المتحدة ونيوزيلندا','us'),('الولايات المتحدة','us'),('أمريك','us'),('المملكة المتحدة','uk'),('إنجلترا','uk'),('بريطاني','uk'),('غلاسكو','uk'),('اسكتلندا','uk'),('ويلز','uk'),
 ('السويد','se'),('الدنمارك','dk'),('النرويج','no'),('فنلندا','fi'),('آيسلندا','is'),('ألمانيا','de'),('النمسا','at'),('هولندا','nl'),('روسيا','ru'),('فرنسا','fr'),('إيطاليا','it'),('بلجيكا','be'),('أيرلندا','ie'),
 ('سويسرا','ch'),('إسبانيا','es'),('البرتغال','pt'),('كندا','ca'),('كيبيك','ca'),('أستراليا','au'),('نيوزيلندا','nz'),('البرازيل','br'),('الأرجنتين','ar'),('تشيلي','cl'),('اليابان','jp'),('الهند','in'),('إسرائيل','il'),
 ('كوريا','kr'),('هونغ كونغ','hk'),('الصين','cn'),('مصر','eg'),('الإمارات','ae'),('أبوظبي','ae'),('السعودية','sa'),('السودان','sd'),('عمان','om'),('اليمن','ye'),('ماليزيا','my'),('التشيك','cz'),('بولندا','pl'),('الفلبين','ph'),('جنوب إفريقيا','za'),('المكسيك','mx'),('تركيا','tr'),('الفاتيكان','va'),('الكنيسة','va'),
 ('عالمي','world'),('دولة','world'),('بلدان','world'),('دولي','world'),('إفريقيا','afr'),('أكا','afr'),
]
FIQH_KEYS={'hanafi','maliki','shafii','hanbali','quran','sunnah','heritage'}
def key_for(jur, cat=''):
    j=(jur or '')
    best=None
    for k,v in KW:
        i=j.find(k)
        if i>=0 and (best is None or i<best[0]): best=(i,v)
    if best: return best[1]
    c=(cat or '')
    for k,v in KW:
        if k in c: return v
    return None
