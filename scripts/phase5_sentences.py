# -*- coding: utf-8 -*-
"""Split each blinded announcement into clean sentences for tone classification.

Writes data/sentences/<id>.json  = {"id","date","n","sentences":[...]}
The blinded text (data/blinded/*.txt) is used so the actual decision, rate figure
and dates are already gone; the sentence TONE is what we classify, not the outcome.
"""
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'data', 'blinded')
OUT = os.path.join(ROOT, 'data', 'sentences')
os.makedirs(OUT, exist_ok=True)

DROP_LINE = re.compile(
    r'^(For the file of data|Ecxel file|To view this file|Click here|'
    r'The minutes of the monetary discussions|The next decision regarding the interest rate)', re.I)

# procedural / non-analytical sentences to drop entirely
DROP_SENT = re.compile(
    r'(will be published|press briefing|click here|accompanying this notice|'
    r'for the file of data|governor will hold|minutes of the monetary)', re.I)

def clean(text):
    lines = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or DROP_LINE.match(ln):
            continue
        if re.fullmatch(r'[֐-׿\s%\d.,\-–]+', ln):   # hebrew / numeric-only
            continue
        lines.append(ln)
    t = " ".join(lines)
    t = t.replace('’', "'").replace('“', '"').replace('”', '"')
    t = re.sub(r'\s+\(Figures?\s*[^)]*\)', '', t)          # " (Figure 12a)"
    t = re.sub(r'\(Figures?\s*[^)]*\)', '', t)
    t = re.sub(r'\bFigures?\s*\d+[a-z\-]*\b', '', t)
    t = re.sub(r'\[DATE\]', 'a later date', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

REDACT = re.compile(r'\[(RATE|DECISION|LEVEL)[^\]]*\]')

# protect decimals / ranges / common abbreviations before splitting on . ; :
def split_sents(t):
    t = re.sub(r'(\d)\.(\d)', r'\1<DOT>\2', t)
    t = re.sub(r'\b([A-Z])\.([A-Z])\.', r'\1<DOT>\2<DOT>', t)   # U.S.
    t = re.sub(r'\bNo\.\s', 'No<DOT> ', t)
    parts = re.split(r'(?<=[.;:])\s+(?=[A-Z"\'‘(])', t)
    out = []
    for s in parts:
        s = s.replace('<DOT>', '.').strip()
        s = s.strip('"‘“ ').strip()
        if len(s) < 20:
            continue
        if DROP_SENT.search(s) or REDACT.search(s):   # drop decision-adjacent sentences
            continue
        # require at least a few real words
        if len(re.findall(r'[A-Za-z]{3,}', s)) < 4:
            continue
        out.append(s)
    return out

manifest = []
for f in sorted(glob.glob(os.path.join(SRC, '*.txt'))):
    dt = os.path.splitext(os.path.basename(f))[0]
    sents = split_sents(clean(open(f, encoding='utf-8', errors='replace').read()))
    rec = {"id": dt, "date": dt, "n": len(sents), "sentences": sents}
    json.dump(rec, open(os.path.join(OUT, dt + '.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    manifest.append((dt, len(sents)))

json.dump({"files": [m[0] for m in manifest],
           "counts": {m[0]: m[1] for m in manifest},
           "total_sentences": sum(m[1] for m in manifest)},
          open(os.path.join(OUT, '_manifest.json'), 'w', encoding='utf-8'), indent=1)

print("announcements:", len(manifest),
      "| total sentences:", sum(m[1] for m in manifest),
      "| mean:", round(sum(m[1] for m in manifest) / len(manifest), 1))
print("min/max per announcement:", min(m[1] for m in manifest), "/", max(m[1] for m in manifest))
