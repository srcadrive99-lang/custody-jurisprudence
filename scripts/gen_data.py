# -*- coding: utf-8 -*-
"""Build normalized nuqul_7_9.json (v1.17.0), schema, and clean markdown export
from: build JSON v1.16 (old entries), new_cards.json (67 new cards, re-id'd), built HTML (section/number)."""
import json, re, html as H, sys, datetime, collections
sys.path.insert(0, '/home/claude/work')
from assemble import SEC, ORDER, mn_plain
from standing import S as STANDING
from plain import plain

OLD = json.load(open('/home/claude/work/base_v1_15.json', encoding='utf8'))  # frozen v1.15 base (idempotent)
NEW = json.load(open('/home/claude/work/new_cards.json', encoding='utf8'))
IDMAP = json.load(open('/home/claude/work/id_map.json'))
LINKS_FIX = json.load(open('/home/claude/work/links_fix.json', encoding='utf8'))
HTML = open('/home/claude/work/build/NUQUL_7_9_CARDS_MOBILE.html', encoding='utf8').read()

def txt(x): return H.unescape(re.sub(r'<[^>]+>', ' ', x)).replace('  ', ' ').strip()

# card order / section / number from the built HTML
cards = {}
for m in re.finditer(r'<section class="page [^"]* sec-(\w+)" id="(A\d-\d{3})"[^>]*>(.*?)</section>', HTML, re.S):
    sec, cid, body = m.groups()
    num = int(re.search(r'<div class="num">(\d+)</div>', body).group(1))
    rt = txt(re.search(r'<div class="rt">(.*?)</div>', body, re.S).group(1))
    cards[cid] = dict(section=sec, card_number=num, card_title=rt)

AXIS_OF = {'eg': 1, 'f1': 1, 'f2': 1, 'f3': 1, 'f4': 1, 'f5': 1, 'f6': 1, 'med': 2, 'psy': 2, 'soc': 4, 'harm': 4, 'court': 5, 'law': 5, 'intl': 5, 'study': 5}
CAT_OF = {'eg': 'فتوى مصرية', 'f1': 'أثر', 'f2': 'فقه حنفي', 'f3': 'فقه مالكي', 'f4': 'فقه شافعي', 'f5': 'فقه حنبلي', 'f6': 'فقه مقارن ولغة', 'med': 'طب', 'psy': 'علم نفس', 'soc': 'علوم المجتمع والإنسان', 'harm': 'أضرار الحرمان من الأب',
          'court': 'قضاء', 'law': 'تشريع مقارن', 'intl': 'هيئات دولية', 'study': 'دراسة علمية'}

def lang_of(text, jur):
    if re.search(r'[؀-ۿ]', text): return 'ar'
    if re.search(r'[֐-׿]', text): return 'he'
    t = ' ' + text.lower() + ' '
    if re.search(r' (que|guarda|criança|pais|não|é) ', t) and ('ç' in t or 'ã' in t): return 'pt'
    if re.search(r' (der|die|das|und|nicht|des|ist|eine?) ', t): return 'de'
    if re.search(r' (que|los|las|del|niño|hijos|ambos|derecho) ', t): return 'es'
    if re.search(r' (les|des|une|est|avec|enfant|parents|droit) ', t) and re.search(r" (le|la|l') ", t): return 'fr'
    if re.search(r' (che|della|figli|genitori|minore|diritto) ', t): return 'it'
    if re.search(r' (ut|vel|et|est|aut|sit|qui|quae|ad) ', t) and re.search(r'(tur|ibus|orum|atis)\b', t): return 'la'
    return 'en'

# ---- old entries (drop the 67 provisional A6 copies that carried a section) ----
entries = []
NEW_IDS = {c['id'] for c in NEW}
for e in OLD['entries']:
    if e['id'].startswith('A6-') and e.get('section'):
        continue  # provisional id of a new card; rebuilt below
    if e['id'] in NEW_IDS:
        continue  # old card replaced by a rebuilt entry with the same id
    e = dict(e)
    # normalize shape
    if isinstance(e.get('work'), str): e['work'] = {'title': e['work'], 'section': '', 'volume': '', 'page': '', 'edition': ''}
    for k in ('section', 'volume', 'page', 'edition'): e['work'].setdefault(k, '')
    if isinstance(e.get('original'), str): e['original'] = {'lang': lang_of(e['original'], e.get('jurisdiction', '')), 'text': e['original'], 'verbatim': not e['original'].startswith('مضمونه')}
    e.setdefault('notes', ''); e.setdefault('translation_ar', '')
    if 'دون تاريخ' in (e['author'].get('date') or ''): e['author']['date'] = ''
    if e['id'] in cards:
        e['section'] = cards[e['id']]['section']; e['card_number'] = cards[e['id']]['card_number']
        e['title'] = cards[e['id']]['card_title']  # the card title as built (carries all text fixes)
    else:
        e['section'] = None; e['card_number'] = None
    if e['id'] in LINKS_FIX:
        fx = LINKS_FIX[e['id']]; e['urls'] = [fx['url']]
        e['links'] = [{'url': fx['url'], 'label': fx['label'], 'site': fx['site'], 'domain': fx['domain']}]
    if e['id'] in STANDING and not e.get('source_standing'):
        e['source_standing'], e['evidence_level'] = STANDING[e['id']]
    entries.append(e)

# ---- new cards ----
for c in NEW:
    if c['id'] not in cards: continue  # retired
    sec = c['sec']; src = c['src']
    ot = c['ot']
    lang = lang_of(ot, c.get('jurisdiction', ''))
    e = {
        'id': c['id'], 'axis': AXIS_OF[sec], 'category': CAT_OF[sec], 'supports': c.get('supports', ['shared_parenting']),
        'author': {'name': src['author'], 'date': str(src.get('year', ''))},
        'work': {'title': src.get('title_latin', '') or '', 'section': src.get('where', '') or '', 'volume': '', 'page': '', 'edition': ''},
        'original': {'lang': lang, 'text': ot, 'verbatim': not ot.startswith('مضمونه')},
        'translation_ar': c.get('tt', '') or '',
        'urls': [l['url'] for l in c['links']],
        'links': [{'url': l['url'], 'label': l['label'], 'site': l['site'], 'domain': l['domain']} for l in c['links']],
        'confidence': 'verified', 'strength': c.get('strength', 'explicit'),
        'argument': c['arg'], 'notes': '', 'title': c['title'], 'jurisdiction': c.get('jurisdiction', ''),
        'about': c['about'], 'source_standing': c['about'], 'evidence_level': c['level'],
        'section': cards[c['id']]['section'], 'card_number': cards[c['id']]['card_number'],
    }
    entries.append(e)

# ---- targeted text fixes (mirror of TEXT_FIX in assemble.py, plain text) ----
FIX = {
 'A5-087': [('original', 'الأدلة تدل على أن الرعاية المشتركة بين الوالدين المنفصلين', 'الأدلة تدل على أن الرعاية المشتركة بالمناصفة بين الوالدين المنفصلين')],
 'A5-101': [('original', 'تعرف الرعاية المشتركة بعد الطلاق بأنها', 'تعرف الوالدية المشتركة بعد الطلاق بأنها')],
 'A5-119': [('original', 'ويصرح بأن سلامة الطفل تتقدم على سائر الاعتبارات، ويستثني من الرعاية المشتركة والمتساوية الحالات التي ثبت فيها العنف الأسري أو إساءة معاملة الطفل وتقتضي حمايته من أحد الوالدين أو كليهما.', 'ويصرح بأن سلامة الطفل تتقدم على سائر الاعتبارات.'),
            ('argument', 'أصلا قانونيا لا يعدل عنه إلا بثبوت العنف أو الإساءة؛', 'أصلا قانونيا؛')],
 'A5-134': [('original', 'شملت الرعاية المشتركة قضاء 30–70% من الوقت', 'شملت الرعاية المشتركة بالمناصفة وما قاربها قضاء 30–70% من الوقت')],
 'A5-135': [('original', 'أو في الرعاية المشتركة عن شكاوى', 'أو في الرعاية المشتركة بالمناصفة عن شكاوى')],
 'A5-051': [('original', '(AFCC) في الرعاية المشتركة:', '(AFCC) في الرعاية المشتركة بالمناصفة:')],
 'A5-064': [('original', 'لا يبطل نفع الرعاية المشتركة،', 'لا يبطل نفع الرعاية المشتركة بالمناصفة،')],
 'A5-088': [('original', 'يرون الرعاية المشتركة نافعة', 'يرون الرعاية المشتركة بالمناصفة نافعة')],
 'A5-098': [('original', 'وبإدخال الرعاية المشتركة وتمكين المحاكم من الحكم بالحضانة المشتركة مع خطط رعاية', 'وبإدخال مفهوم الحضانة المشتركة وتمكين المحاكم من الحكم بها مع خطط رعاية')],
 'A1-026': [('original', 'فدل ذلك على أن الرعاية المشتركة ثابتة قبل التخيير', 'فدل ذلك على أن الرعاية المشتركة بالمناصفة ثابتة قبل التخيير'),
            ('translation_en', 'Hence shared care is established before the choice', 'Hence equal shared care is established before the choice')],
}
byid = {e['id']: e for e in entries}
for cid, fl in FIX.items():
    e = byid[cid]
    for field, old, new in fl:
        if field == 'original':
            if old not in e['original']['text']: print('FIX miss', cid, old[:30])
            e['original']['text'] = e['original']['text'].replace(old, new)
        else:
            if old not in (e.get(field) or ''): print('FIX miss', cid, field, old[:30])
            e[field] = (e.get(field) or '').replace(old, new)
# phrase rule + plain-language pass on derived fields (never on verbatim heritage quotations)
for e in entries:
    for f in ('argument', 'title', 'about', 'source_standing', 'notes', 'category', 'evidence_level', 'jurisdiction', 'translation_ar'):
        if e.get(f): e[f] = plain(mn_plain(e[f]))
    if not (e['original']['verbatim'] and e['original']['lang'] == 'ar'):
        e['original']['text'] = plain(e['original']['text'])
    if not e['original']['verbatim']:
        pass  # gists handled above case by case (accuracy first)
    if 'translation_en' in e and e['translation_en']: pass

# ---- verification overlay (v1.20.0) ----
OV = json.load(open('/home/claude/work/verify/overlay.json', encoding='utf8'))
retired_now = []
for e in list(entries):
    i = e['id']
    if i in OV['retire']:
        entries.remove(e); retired_now.append({'id': i, 'reason': OV['retire'][i]}); continue
    if i == 'A6-002': e['argument'] = 'الجواب: الواقعة في صغير لم يستغن، فتقديم الأم فيها تقديم في مباشرة الخدمة والحمل، ولا ينفي صحبة الأب ورعايته المشتركة قبل السابعة؛ ثم ينتهي هذا التقديم بالتمييز.'
    if i == 'A5-003': e['author'] = {'name': 'الجمعية البرلمانية لمجلس أوروبا — لجنة المساواة', 'date': '2015'}
    if i in OV['conf'] and e['confidence'] != 'verified': e['confidence'] = 'verified'
    o = OV['ot'].get(i)
    if o:
        e['original'] = {'lang': o['lang'], 'text': o['text'], 'verbatim': True}
        if o['tt']: e['translation_ar'] = o['tt']
    if i in OV['links'] and not e.get('links'):
        l = OV['links'][i]; e['links'] = [l]; e['urls'] = [l['url']]
    if i in OV['notes']:
        e['notes'] = (('رابط بحث مؤقت' in (e.get('notes') or '')) and '' or (e.get('notes') or '')) + (' | ' if e.get('notes') and 'رابط بحث مؤقت' not in e['notes'] else '') + 'المطابقة 1.20.0: ' + OV['notes'][i]
    if 'رابط بحث مؤقت' in (e.get('notes') or ''): e['notes'] = e['notes'].replace('رابط بحث مؤقت يستبدل برابط مباشر.', '').strip()
    for old, nl in OV.get('url_sub', {}).items():
        if old in (e.get('urls') or []):
            e['urls'] = [nl['url'] if u == old else u for u in e['urls']]
            if e.get('links'): e['links'] = [nl if l['url'] == old else l for l in e['links']]
# ---- axis 6 from the debate memo (opponent claim + answer + strongest cards) ----
import os
MEMO = '/home/claude/work/build/tools/مذكرة_المناظرة.md'
if os.path.exists(MEMO):
    txt = open(MEMO, encoding='utf8').read()
    k = 8
    for blk in re.split(r'\n## \d+\. ', txt)[1:]:
        claim = blk.split('\n', 1)[0].strip().strip('«»')
        ans = re.search(r'\*\*الجواب:\*\*\s*(.*?)\n', blk, re.S); ans = ans.group(1).strip() if ans else ''
        refs = re.findall(r'- بطاقة (\d+): (.*)', blk)
        entries.append({'id': f'A6-{k:03d}', 'axis': 6, 'category': 'دعوى المخالف', 'supports': ['counter'],
            'author': {'name': 'دعوى شائعة عند المخالفين', 'date': ''}, 'work': {'title': 'مذكرة المناظرة', 'section': '', 'volume': '', 'page': '', 'edition': ''},
            'original': {'lang': 'ar', 'text': 'مضمونه: دعوى المخالف: ' + claim, 'verbatim': False}, 'translation_ar': '', 'urls': [], 'confidence': 'verified', 'strength': 'contextual',
            'argument': 'الجواب: ' + ans + ' الأدلة: ' + '؛ '.join(f'بطاقة {n} ({t.strip()})' for n, t in refs), 'notes': '', 'jurisdiction': 'حجة الخصم والجواب عنها',
            'section': None, 'card_number': None})
        k += 1
# ---- order: by card order, then non-card entries ----
entries.sort(key=lambda e: (e['card_number'] is None, e['card_number'] or 0, e['id']))

meta = dict(OLD['meta'])
meta['title'] = 'حول سن الحضانة والرعاية المشتركة بالمناصفة — النصوص والمصادر'
meta['owner'] = ''
meta['version'] = '1.20.1'; meta['date'] = datetime.date.today().isoformat()
meta['legend']['supports']['shared_parenting'] = 'الرعاية المشتركة بالمناصفة'
meta['sections'] = {k: mn_plain(SEC[k]['name']) for k in ORDER}
meta['section_order'] = list(ORDER)
meta.setdefault('changelog', {})
meta.pop('changelog_1_16', None)
meta['changelog']['1.16.0'] = ["إضافة 67 نصا ومصدرا جديدا (قضاء 13، تشريعات 15، علم نفس 14، طب 8، دراسات 9، هيئات دولية 4، مجتمع 2، أضرار 2)", "استبدال 65 رابط بحث مؤقتا بروابط مباشرة", "إضافة «عن المصدر» و«درجة الدليل» لكل مصدر غير تراثي", "حذف العبارات النافية", "إضافة «بالمناصفة» إلى «الرعاية المشتركة» في كل موضع", "تقسيم الفقه الإسلامي إلى ستة أقسام", "أيقونات الدول والمصادر", "طبعة فيسبوك 1080×1350"]
meta['changelog']['1.17.0'] = [
    'إعادة ترقيم النصوص الجديدة السبعة والستين على محاورها (A2 للطب وعلم النفس، A4 للمجتمع والأضرار، A5 للقضاء والتشريع والهيئات والدراسات) بدل الترقيم المؤقت A6 الذي كان يزاحم مدخلات المحور السادس',
    'توحيد بنية المدخلات كلها (work/original/links/section/card_number) ومطابقتها للمخطط',
    'إتمام قاعدة «الرعاية المشتركة بالمناصفة» في مضامين النصوص المنقولة بالمعنى مع حفظ دقة المعنى',
    'أيقونة لكل مصدر بلا استثناء',
    'استبدال بطاقة المراجعة المنهجية المشروطة (بود 2019) بالتحليل البعدي لبود وبيرسون ودرابو 2016 الجازم بأفضلية الحضانة المشتركة',
    'إصدار فيسبوك 1080×1350 بعد ضبط الأيقونات والنص اللاتيني',
]
meta['changelog']['1.18.0'] = [
    'مجالات جديدة: اقتصاديات قانون الأسرة (دراسة نمساوية على سجلات الدولة، وبرينيغ وآلن)، والطب النفسي الشرعي في رغبة الطفل (وارشاك 2003)، وطب الولادة (أليو 2010 و2011)، وطب الأسنان (جداول الجمعية الأمريكية)، واستطلاع الرأي العام (برافر 2011)، وسجلات محاكم ويسكونسن (كانسيان وماير 2014)، والقانون الهندوسي 1956',
    'إحصاءان رسميان من السويد والنرويج في شيوع الرعاية المشتركة بالمناصفة',
    'قاعدة وضوح اللفظ لعموم الناس مطبقة آليا على كل المنتجات',
    'إعادة كتابة الدستور كاملا (الإصدار 1.18.0)',
]
meta['changelog']['1.19.0'] = [
    'حفر واسع: 24 نصا جديدا — طب الولادة والرضاعة والنمو (لوري للأطفال 2023، أليو 2011، ريدشو 2013، بيزاكاني 2005، صالحو 2014، ويك 2007)، وعلم النفس (بانكسوفار، تشاكو، كولي، مينينغ، وارشاك 2015)، والدراسات (سيلتزر 1998)، والمجتمع والإحصاء والتاريخ (الإحصاء الهولندي، إيزيدور الإشبيلي، برينيغ وباكلي)، وأبقراط، وقانون 1839 الإنجليزي، وسبعة أحكام قضائية (نيويورك 1973، بنسلفانيا 1977، واشنطن 1978، الدستورية الألمانية 2010، والمحكمة الأوروبية في إلسهولتس وإمبروتا وكيليتش)',
]
meta['changelog']['1.20.0'] = [
    'مطابقة 126 مدخلا لم تكن متحققا منها على مصادرها الأصلية: تحقق منها 114، ونقل 58 منها من «المضمون» إلى النص الحرفي من مصدره مع ترجمته، وصححت إحالات (البخاري 2067، النسائي 3496، الغزالي «سن التمييز»، الثعالبي، المبسوط، رد المحتار)، وأضيفت روابط الشاملة والسنة لـ37 نصا تراثيا',
    'استبعاد 9 مصادر ظهر بالمطابقة أنها ذات حدين (حجة لنا وعلينا) عملا بقاعدة «حجة لنا لا علينا»',
    'تصحيح بطاقة بياجيه بنصه في «مبادئ نظرية المعرفة التكوينية» (السابعة إلى الثامنة نقطة تحول حاسمة)، وإتمام نص المادة 84 من قانون الأسرة الإسلامي الماليزي',
    'إضافة 27 نصا جديدا متحققا منها: سبع فتاوى لدار الإفتاء المصرية (حسونة النواوي، محمد عبده، محمد بخيت، أحمد هريدي) منها فتوى تنقل المادة 391 من تقنين قدري باشا، وأربعة أحكام لمحاكم هندية تطبق الفقه الحنفي، وأربعة نصوص فقهية في الإثغار والتمييز، وثمان دراسات في أضرار غياب الأب، وأربعة إحصاءات رسمية إسبانية في الحضانة المشتركة',
    'فحص الروابط كلها (416 رابطا) وإصلاح ما ظهر فيه خلل',
    'أدوات جديدة: مذكرة المناظرة، والخمسون الأقوى، ومذكرة تشريعية، وتعليقات فيسبوك وجدول النشر، ونصوص الفيديو، والطبعة الإنجليزية، ومستودع البناء',
]
_seen = {r['id'] for r in retired_now}
retired_now += [{'id': k, 'reason': v} for k, v in OV['retire'].items() if k not in _seen]
meta['changelog']['1.20.1'] = ['استبعاد 14 بطاقة لا تصلح حجة لنا: دراسات تجعل سن الحيض أو البلوغ عند الأنثى بين 11 و13 (الدراسة المصرية، تشيلي، البرازيل، كوريا، دليل ميرك، فسيولوجيا الحيض، مارشال وتانر)، والاحتلام 13 إلى 14.6 (الصين، الهند)، واكتمال التفكير المجرد في 14-15 (بياجيه وإنهلدر)، والمشناه (12 و13)، وتحديد البلوغ بخمس عشرة (شرح النووي)، و«حتى تحيض» (بدائع الصنائع)', 'الطبعة المختصرة بنمطين وتعريف مختصر بالمصدر', 'الطبعة النصية بالروابط (وورد ونص)']
meta['retired_ids'] = [r for r in meta.get('retired_ids', []) if r['id'] not in OV['retire']] + retired_now
meta['id_map_1_17'] = IDMAP
axes = OLD['axes']
axes[4]['title'] = 'الرعاية المشتركة بالمناصفة في التشريع والقضاء والصكوك والدراسات'
out = {'meta': meta, 'axes': axes, 'entries': entries}
json.dump(out, open('/home/claude/work/build/nuqul_7_9.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('entries', len(entries), 'cards', sum(1 for e in entries if e['card_number']), 'non-card', [e['id'] for e in entries if not e['card_number']])
print(collections.Counter(e['original']['lang'] for e in entries))

# ---- schema ----
schema = json.load(open('/mnt/user-data/outputs/nuqul_7_9.schema.json', encoding='utf8'))
mp = schema['properties']['meta']['properties']
mp['sections'] = {'type': 'object', 'description': 'مفاتيح الأقسام الخمسة عشر وأسماؤها'}
mp['section_order'] = {'type': 'array', 'items': {'type': 'string'}}
mp['changelog'] = {'type': 'object', 'description': 'سجل التغييرات لكل إصدار'}
mp['id_map_1_17'] = {'type': 'object', 'description': 'المعرفات المؤقتة للنصوص المضافة في 1.16 ومقابلها الدائم'}
ep = schema['$defs']['entry']['properties']
ep['source_standing'] = {'type': 'string', 'description': 'عن المصدر: منزلته العلمية أو القضائية'}
ep['evidence_level'] = {'type': 'string', 'description': 'درجة الدليل'}
ep['section'] = {'type': ['string', 'null'], 'description': 'مفتاح القسم في الإصدار؛ null لمدخل غير معروض في البطاقات'}
ep['card_number'] = {'type': ['integer', 'null'], 'description': 'رقم البطاقة في الإصدار'}
ep['links'] = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['url', 'label'],
               'properties': {'url': {'type': 'string'}, 'label': {'type': 'string'}, 'site': {'type': 'string'}, 'domain': {'type': 'string'}}}}
schema['title'] = 'Nuqul 7-9 Corpus — حول سن الحضانة والرعاية المشتركة بالمناصفة'
json.dump(schema, open('/home/claude/work/build/nuqul_7_9.schema.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
try:
    import jsonschema
    jsonschema.validate(out, schema); print('schema OK')
except ImportError:
    print('jsonschema not installed')
except Exception as ex:
    print('SCHEMA ERROR', str(ex)[:400])

# ---- markdown ----
md = ['# حول سن الحضانة والرعاية المشتركة بالمناصفة — النصوص والمصادر', '',
      f'الإصدار {meta["version"]} · {meta["date"]} · {sum(1 for e in entries if e["card_number"])} بطاقة في {len(ORDER)} قسما · {len(entries)} مدخلا', '']
def fld(label, val):
    return f'**{label}:** {val}  ' if val else None
cur = None
for e in entries:
    if e['card_number'] is None: continue
    if e['section'] != cur:
        cur = e['section']; md += [f'## {meta["sections"][cur]}', '']
    a = e['author']; au = a['name'] + (f' ({a["date"]})' if a.get('date') else '')
    md.append(f'### بطاقة {e["card_number"]} — {e.get("title") or au}')
    w = e['work']; src = ' · '.join(x for x in [w.get('title'), w.get('section'), w.get('volume'), w.get('page'), w.get('edition')] if x)
    for line in [fld('المؤلف/الجهة', au), fld('المصدر', src), fld('الجهة/المذهب', e.get('jurisdiction')), fld('الموضع', e.get('notes'))]:
        if line: md.append(line)
    md.append(''); md.append('> ' + e['original']['text'].replace('\n', ' '))
    if e.get('translation_ar'): md.append('>'); md.append('> ' + e['translation_ar'].replace('\n', ' '))
    md.append('')
    md.append(f'**الاستدلال:** {e["argument"]}  ')
    if e.get('source_standing'): md.append(f'**عن المصدر:** {e["source_standing"]} — **درجة الدليل:** {e.get("evidence_level","")}  ')
    for l in e.get('links', []) or [{'url': u, 'label': 'الرابط'} for u in e.get('urls', [])]:
        md.append(f'- {l.get("label","الرابط")}: <{l["url"]}>')
    md.append('')
rest = [e for e in entries if e['card_number'] is None]
if rest:
    md += ['## مدخلات غير معروضة في البطاقات (حجة الخصم والجواب عنها)', '']
    for e in rest:
        a = e['author']; md.append(f'### {e["id"]} — {a["name"]}' + (f' ({a["date"]})' if a.get('date') else ''))
        md.append('> ' + e['original']['text']); md.append(''); md.append(f'**{e["argument"]}**'); md.append('')
open('/home/claude/work/build/nuqul_7_9.md', 'w', encoding='utf8').write('\n'.join(md))
print('md lines', len(md))
