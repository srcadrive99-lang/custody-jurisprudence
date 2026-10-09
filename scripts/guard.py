# -*- coding: utf-8 -*-
"""«حجة لنا لا علينا» gate: blocks the build if any card text carries what the opponent can use."""
import json, re, sys
BAD = [
 (r'(?:الحيض|حيض|menarche|الطمث)[^.؛]{0,60}?\b1[0-6](?:[.,]\d+)?', 'سن حيض فوق التاسعة'),
 (r'\b1[0-6](?:[.,]\d+)?\s*(?:سنة|years)[^.؛]{0,40}(?:الحيض|حيض|menarche)', 'سن حيض فوق التاسعة'),
 (r'(?:البلوغ|بلوغ|puberty|الاحتلام)[^.؛]{0,50}(?:1[1-6](?:[.,]\d+)?\s*(?:سنة|years)|الرابعة عشرة|الخامسة عشرة|خمس عشرة|أربع عشرة)', 'بلوغ فوق العاشرة'),
 (r'حتى تحيض|حتى تتزوج|إلى أن تتزوج|حتى يبلغ الغلام', 'بقاء الصغير عند أمه إلى البلوغ أو الزواج'),
 (r'not clear|insufficient evidence|no difference|not related to child outcomes|لم تتضح', 'نتيجة مشككة'),
]
ALLOW = set(json.load(open('/home/claude/work/guard_allow.json'))) if __import__('os').path.exists('/home/claude/work/guard_allow.json') else set()
def check(path='/home/claude/work/build/nuqul_7_9.json'):
    J = json.load(open(path, encoding='utf8')); hits = []
    for e in J['entries']:
        if not e.get('card_number') or e['id'] in ALLOW: continue
        t = ' '.join([e['original']['text'], e.get('translation_ar') or '', e.get('title') or '', e.get('argument') or ''])
        for pat, why in BAD:
            m = re.search(pat, t, re.I)
            if m: hits.append((e['card_number'], e['id'], why, t[max(0, m.start()-40):m.end()+30])); break
    return hits
if __name__ == '__main__':
    h = check()
    for x in h: print(x)
    print('HITS', len(h)); sys.exit(1 if h else 0)
