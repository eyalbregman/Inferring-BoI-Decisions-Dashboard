# -*- coding: utf-8 -*-
"""Split each RAW Bank of Israel announcement into clean sentences for Fed-anchored
hawkish / dovish classification.

RAW text (data/raw/*.txt): the headline, the decision sentence and all stance /
guidance language are KEPT (this measure is decision-inclusive, like the paper).
Navigation, dates, figure captions, Hebrew-only lines, the procedural closing and
the ~4x-repeated headline are removed.

Writes data/fed_sentences/<id>.json = {"id","date","n","sentences":[...]}
"""
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'data', 'raw')
OUT = os.path.join(ROOT, 'data', 'fed_sentences')
os.makedirs(OUT, exist_ok=True)

DROP_LINE = re.compile(
    r'^(Home Page|Communication and [Pp]ublications|Press Releases|Back|Share:?|'
    r'\d{1,2}/\d{1,2}/\d{2,4}|To view this|For the file of data|Ecxel file|Excel file|'
    r'This page was last updated|The minutes of the monetary discussions|'
    r'The next decision regarding the interest rate|click here)', re.I)

DROP_SENT = re.compile(
    r'(will be published|press briefing|click here|accompanying this notice|'
    r'for the file of data|governor will hold|minutes of the monetary discussions)', re.I)

HEADLINE = re.compile(
    r'The Monetary Committee (?:decides|decided) on [A-Z][a-z]+ \d{1,2},? \d{4},? '
    r'to (?:increase|raise|reduce|lower|decrease|keep|leave) the interest rate'
    r'(?:(?: by [\d.]+ percentage points?)?(?: to| unchanged at| at)? [\d.]+\s*percent'
    r'|\s+unchanged)\b\.?', re.I)

def clean(text):
    text = text.replace('​', ' ').replace('﻿', ' ')
    seen, lines = set(), []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or DROP_LINE.match(ln):
            continue
        if re.fullmatch(r'[֐-׿\s%\d.,\-–]+', ln):
            continue
        key = re.sub(r'\s+', ' ', ln.lower())
        if key in seen:                          # collapse exact repeated lines
            continue
        seen.add(key)
        lines.append(ln)
    t = " ".join(lines)
    t = t.replace('’', "'").replace('“', '"').replace('”', '"')
    t = re.sub(r'[֐-׿]+', ' ', t)                        # strip embedded Hebrew
    t = re.sub(r'[-–\d/.\s%]*Full press release(?: as a file)?', ' ', t, flags=re.I)
    t = re.sub(r'\bFull (?:file|article)\b.*?(?=[A-Z][a-z])', ' ', t)
    t = re.sub(r'\s[-–]\d{1,2}/\d{1,2}/\d{2,4}\s+[\d.]+%?\s', ' ', t)
    t = re.sub(r'\s*\(Figures?\s*[^)]*\)', '', t)
    t = re.sub(r'\bFigures?\s*\d+[a-z\-]*\b', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    # keep only the FIRST occurrence of the (usually 2-4x repeated) headline, as its own sentence
    heads = HEADLINE.findall(t)
    if heads:
        first = heads[0].rstrip('.') + '.'
        t = HEADLINE.sub(' ', t)
        t = first + ' ' + re.sub(r'\s+', ' ', t).strip()
    return t

def split_sents(t):
    t = re.sub(r'(\d)\.(\d)', r'\1<DOT>\2', t)
    t = re.sub(r'\b([A-Z])\.([A-Z])\.', r'\1<DOT>\2<DOT>', t)
    t = re.sub(r'\bNo\.\s', 'No<DOT> ', t)
    parts = re.split(r'(?<=[.;:])\s+(?=[A-Z"\'‘(])', t)
    out = []
    for s in parts:
        s = s.replace('<DOT>', '.').strip().strip('"‘“ ').strip()
        if len(s) < 20 or DROP_SENT.search(s):
            continue
        if len(re.findall(r'[A-Za-z]{3,}', s)) < 4:
            continue
        out.append(s)
    return out

manifest = []
for f in sorted(glob.glob(os.path.join(SRC, '*.txt'))):
    dt = os.path.splitext(os.path.basename(f))[0]
    sents = split_sents(clean(open(f, encoding='utf-8', errors='replace').read()))
    json.dump({"id": dt, "date": dt, "n": len(sents), "sentences": sents},
              open(os.path.join(OUT, dt + '.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    manifest.append((dt, len(sents)))

json.dump({"files": [m[0] for m in manifest],
           "counts": {m[0]: m[1] for m in manifest},
           "total_sentences": sum(m[1] for m in manifest)},
          open(os.path.join(OUT, '_manifest.json'), 'w', encoding='utf-8'), indent=1)

print("announcements:", len(manifest),
      "| total sentences:", sum(m[1] for m in manifest),
      "| mean:", round(sum(m[1] for m in manifest) / len(manifest), 1),
      "| min/max:", min(m[1] for m in manifest), "/", max(m[1] for m in manifest))
