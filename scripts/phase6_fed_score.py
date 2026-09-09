# -*- coding: utf-8 -*-
"""Score every RAW Bank of Israel announcement on the Fed-anchored hawk/dove lexicon.

score = (H - D) / (H + D)      in [-1, +1]     (+1 = all hawkish hits, -1 = all dovish)
Also reports hawkish and dovish hits per 1,000 words.

RAW text: nav / date / file-link / minutes / Hebrew-only lines removed, exact-duplicate
lines collapsed (the headline is repeated ~4x in the source) -- but the decision
sentence, the rate figure and all stance / guidance language are KEPT, by design.

Writes results/fed_lexicon_scores.json  and  results/fed_lexicon_hits.json
"""
import os, re, glob, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'data', 'raw')

DROP = re.compile(
    r'^(Home Page|Communication and [Pp]ublications|Press Releases|Back|Share:?|'
    r'\d{1,2}/\d{1,2}/\d{2,4}|To view this|For the file of data|Ecxel file|Excel file|'
    r'This page was last updated|The minutes of the monetary discussions|'
    r'The next decision regarding the interest rate|click here)', re.I)

def raw_body(text):
    seen, out = set(), []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or DROP.match(ln):
            continue
        if re.fullmatch(r'[֐-׿\s%\d.,\-–]+', ln):          # hebrew / numeric-only
            continue
        key = re.sub(r'\s+', ' ', ln.lower())
        if key in seen:                                              # collapse repeated headline
            continue
        seen.add(key)
        out.append(ln)
    t = " ".join(out)
    t = t.replace('’', "'").replace('“', '"').replace('”', '"')
    t = re.sub(r'\(Figures?\s*[^)]*\)', ' ', t)
    t = re.sub(r'\bFigures?\s*\d+[a-z\-]*\b', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t

# ---- term matcher (same conventions as scripts/lexicon_build_xlsx.py) --------
_GAP = r"(?:'s|’s)?[\s\-]+"
def term_regex(term):
    def one(seg):
        words = re.split(r'[\s\-]+', seg.strip())
        p = _GAP.join(re.escape(w) for w in words)
        p = p.replace('percent', r'(?:[\d.,]+\s*)?percent')
        return r'\b' + p + r'\b'
    return re.compile(r'[^.;:]*?'.join(one(s) for s in term.split(' ... ')), re.I)

from lexicon_fed import LEXICON
LEX = [(t, cat, d, src, logic, term_regex(t)) for (t, cat, d, src, logic) in LEXICON]

gt = {r['id']: r for r in json.load(open(os.path.join(ROOT, 'data', 'ground_truth.json'), encoding='utf-8'))}

files = sorted(glob.glob(os.path.join(RAW, '*.txt')))
bodies = {os.path.splitext(os.path.basename(f))[0]: raw_body(open(f, encoding='utf-8', errors='replace').read())
          for f in files}
bodies = {k: v for k, v in bodies.items() if k in gt}          # in-scope 62

# per-term corpus coverage (for the lexicon sheet + verification)
cover = {}
for (t, cat, d, src, logic, rx) in LEX:
    tot = docf = 0
    ex = ""
    for k, b in bodies.items():
        c = len(rx.findall(b))
        if c:
            tot += c; docf += 1
            if not ex:
                m = rx.search(b)
                s0 = b.rfind('.', 0, m.start()) + 1
                s1 = b.find('.', m.end())
                ex = b[s0:s1 if s1 > 0 else m.end()+60].strip()[:200]
    cover[t] = (tot, docf, ex)

missing = [t for t, (tot, _, _) in cover.items() if tot == 0]

def score_body(b):
    """Count NON-OVERLAPPING matched spans. Where two lexicon terms match
    overlapping text, the longer match wins (its direction is credited once)."""
    spans = []                       # (start, end, direction, term)
    for (t, cat, d, src, logic, rx) in LEX:
        if d == 'C':
            continue
        for m in rx.finditer(b):
            spans.append((m.start(), m.end(), d, t))
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    taken = []                       # accepted (start, end)
    hh, dd = collections.Counter(), collections.Counter()
    for s, e, d, t in spans:
        if any(not (e <= ts or s >= te) for ts, te in taken):
            continue                 # overlaps an already-counted span
        taken.append((s, e))
        (hh if d == 'H' else dd)[t] += 1
    return hh, dd

rows, hits_detail = [], {}
for k in sorted(bodies):
    b = bodies[k]
    words = len(re.findall(r"[A-Za-z']+", b))
    hh, dd = score_body(b)
    H, D = sum(hh.values()), sum(dd.values())
    score = (H - D) / (H + D) if (H + D) else 0.0
    rows.append({"id": k, "date": k, "H": H, "D": D, "words": words,
                 "score": round(score, 4),
                 "hawk_per_1k": round(1000 * H / words, 2) if words else 0,
                 "dove_per_1k": round(1000 * D / words, 2) if words else 0,
                 "decision": gt[k].get('decision', '')})
    hits_detail[k] = {"hawk": hh.most_common(), "dove": dd.most_common()}

rows.sort(key=lambda r: r['date'])
json.dump(rows, open(os.path.join(ROOT, 'results', 'fed_lexicon_scores.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
json.dump({"coverage": {t: cover[t] for t in cover}, "hits": hits_detail},
          open(os.path.join(ROOT, 'results', 'fed_lexicon_hits.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

print(f"lexicon terms: {len(LEX)}  ({sum(1 for x in LEX if x[2]=='H')} H / {sum(1 for x in LEX if x[2]=='D')} D / {sum(1 for x in LEX if x[2]=='C')} C)")
print(f"scored {len(rows)} announcements")
if missing:
    print(f"\n{len(missing)} terms NOT found in the raw BoI corpus:")
    for t in missing:
        print("   -", t)
sc = [r['score'] for r in rows]
print(f"\nscore range {min(sc):+.3f} .. {max(sc):+.3f}   mean {sum(sc)/len(sc):+.3f}")
from collections import defaultdict
by = defaultdict(list)
for r in rows:
    by[r['decision']].append(r['score'])
for k in ('lower', 'maintain', 'raise'):
    if by[k]:
        print(f"  mean score | decision = {k:8s}: {sum(by[k])/len(by[k]):+.3f}  (n={len(by[k])})")
