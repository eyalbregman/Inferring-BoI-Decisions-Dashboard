# -*- coding: utf-8 -*-
"""Extract Alt A / B / C / D FOMC statement drafts from Bluebook / Tealbook-B PDFs.

Handles the 'separate statement' format (~2009+): each alternative is its own
section starting with a header line containing 'ALTERNATIVE X'. Writes one txt per
(meeting, alt) to data/fed_alts/<meeting>__<ALT>.txt and a manifest.

INPUT: the 136 Bluebook / Tealbook-B PDFs (2004-2020) are NOT committed (206 MB).
Filenames are in data/fed_bookb_files.txt; fetch them from
https://www.federalreserve.gov/monetarypolicy/files/<name> into ./fed_pdf/ first.
The extracted drafts (data/fed_alts/) and the contrast table (data/fed_contrast.csv)
ARE committed, so lexicon_fed.py is reproducible without re-downloading.
"""
import pdfplumber, re, glob, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFS = sorted(glob.glob(os.path.join(ROOT, 'fed_pdf', '*.pdf')))
OUT = os.path.join(ROOT, 'data', 'fed_alts')
os.makedirs(OUT, exist_ok=True)

# header that opens an alternative's own draft-statement section
HDR = re.compile(
    r'^(?:'
    r'(?:FOMC\s+STATEMENT\s*[—\-]\s*)?[A-Z]+\s+\d{4}\s+ALTERNATIVE\s+([ABCD])'      # "JULY 2016 ALTERNATIVE A"
    r'|FOMC\s+STATEMENT\s*[—\-]\s*[A-Z]+\s+\d{4}\s+ALTERNATIVE\s+([ABCD])'          # "FOMC STATEMENT—JUNE 2013 ALTERNATIVE A"
    r'|[A-Z]+\s+FOMC\s+STATEMENT\s*[—\-]\s*ALTERNATIVE\s+([ABCD])'                  # "NOVEMBER FOMC STATEMENT—ALTERNATIVE A"
    r'|ALTERNATIVE\s+([ABCD])\s+FOR\s+[A-Z]+\s+\d{4}'                                    # "ALTERNATIVE A FOR DECEMBER 2019"
    r'|Alternative\s+([ABCD])\s*$'                                                       # bare "Alternative A"
    r')', re.M)

STOP = re.compile(r'^(THE CASE FOR|The Case for|IMPLEMENTATION NOTE|DIRECTIVE|Directive|'
                   r'ECONOMIC CONDITIONS AND OUTLOOK|Implementation Note|LONG-RUN|Projections|'
                   r'[A-Z]+ \d{4} FOMC STATEMENT\s*$|[A-Z]+ FOMC STATEMENT\s*$)', re.M)

def clean_page(t):
    t = re.sub(r'(Authorized for Public Release|Class I+ FOMC[^\n]*|Restricted[^\n]*|'
               r'Page \d+ of \d+|\d+ of \d+|sevitanretlA|seigetartS|snoitcejorP)', ' ', t)
    return t

def pages_text(pdf):
    return [clean_page(p.extract_text() or '') for p in pdf.pages]

manifest = []
for f in PDFS:
    base = os.path.basename(f)[:-4]
    meeting = base[4:12]                        # FOMC20130619...
    with pdfplumber.open(f) as pdf:
        pt = pages_text(pdf)
    full = "\n".join(pt)
    # find every alternative header with position
    hits = []
    for m in HDR.finditer(full):
        alt = next(g for g in m.groups() if g)
        hits.append((m.start(), alt, m.group(0).strip()))
    # keep only the FIRST block per alt that is followed by a numbered paragraph "1."
    seen = {}
    for idx, (pos, alt, hdr) in enumerate(hits):
        end = hits[idx + 1][0] if idx + 1 < len(hits) else len(full)
        body = full[pos:end]
        sm = STOP.search(body, len(hdr))
        if sm:
            body = body[:sm.start()]
        if not re.search(r'\n\s*1\.\s', body):        # must contain a numbered para 1.
            continue
        if alt in seen:
            continue
        seen[alt] = body
    for alt, body in seen.items():
        body = re.sub(r'[ \t]+', ' ', body)
        body = re.sub(r'\n{2,}', '\n', body).strip()
        fn = os.path.join(OUT, f'{meeting}__{alt}.txt')
        open(fn, 'w', encoding='utf-8').write(body)
        manifest.append({'meeting': meeting, 'alt': alt, 'file': os.path.basename(fn),
                         'chars': len(body), 'src': base})

json.dump(manifest, open(os.path.join(OUT, '_manifest.json'), 'w'), indent=1)
from collections import Counter
byalt = Counter(m['alt'] for m in manifest)
bymtg = Counter(m['meeting'] for m in manifest)
print('files:', len(manifest), '| by alt:', dict(byalt))
print('meetings with >=1 alt:', len(bymtg))
print('meetings with A and (C or D):',
      sum(1 for mt in bymtg if any(m['alt']=='A' for m in manifest if m['meeting']==mt)
          and any(m['alt'] in 'CD' for m in manifest if m['meeting']==mt)))
missing = []
allmtg = sorted(set(os.path.basename(f)[4:12] for f in PDFS))
for mt in allmtg:
    alts = sorted(m['alt'] for m in manifest if m['meeting']==mt)
    if not alts:
        missing.append(mt)
print('meetings with NO extracted alts:', len(missing))
print(missing)
