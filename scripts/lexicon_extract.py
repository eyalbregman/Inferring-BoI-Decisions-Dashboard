"""Extract candidate hawkish/dovish vocabulary from the 62 BoI announcements (raw text).
Outputs scratchpad/ngram_freq.csv : term, ngram, total_freq, doc_freq (of 62), example_sentence."""
import os, re, glob, json, collections, csv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.join(ROOT, 'data')

DROP_LINE = re.compile(
    r'^(Home Page|Communication and [Pp]ublications|Press Releases|Back|Share:?|'
    r'The Monetary Committee decides on|to (lower|raise|increase|reduce|leave|keep) the interest|'
    r'\d{1,2}/\d{1,2}/\d{2,4}|To view this|For the file|This page was last updated|'
    r'The minutes of the monetary discussions|The next decision regarding the interest rate)', re.I)

STOP = set("""a an the and or but if then than so as of to in on at by for with from into over under
between within without about above below up down out off again further this that these those
it its it's they them their there here what which who whom whose when where why how all any both
each few more most other some such no nor not only own same too very can will just should now
is are was were be been being do does did doing have has had having would could may might must
shall i we you he she his her our your my me us also across during since after before while
whether against per among toward towards vis regarding according due despite along amid onto""".split())

MONTHS = set("january february march april may june july august september october november december".split())
NOISE = set("""figure figures percent percentage points point israel israeli committee monetary
cpi gdp nis usd eur mr ms dr prof press release notice today year quarter month week day
first second third fourth q1 q2 q3 q4 h1 h2 pp bps""".split())

def body(text):
    out = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or DROP_LINE.match(ln):
            continue
        if re.fullmatch(r'[\u0590-\u05FF\s%\d.,-]+', ln):   # hebrew-only line
            continue
        out.append(ln)
    t = " ".join(out)
    t = re.sub(r'\(Figures?\s*[^)]*\)', ' ', t)             # (Figure 12a)
    t = re.sub(r'\bFigures?\s*\d+[a-z-]*\b', ' ', t)
    return t

def sentences(t):
    return [s.strip() for s in re.split(r'(?<=[.;:])\s+(?=[A-Z“"])', t) if len(s.strip()) > 20]

def toks(s):
    s = s.lower()
    s = re.sub(r"[^a-z\s'-]", " ", s)
    w = [x.strip("'-") for x in s.split()]
    return [x for x in w if x and len(x) > 1]

docs = sorted(glob.glob(os.path.join(ROOT, 'data', 'raw', '*.txt')))
total = collections.Counter()
docfreq = collections.Counter()
example = {}

for d in docs:
    raw = open(d, encoding='utf-8', errors='replace').read()
    t = body(raw)
    seen = set()
    for sent in sentences(t):
        w = toks(sent)
        grams = []
        grams += w
        grams += [" ".join(w[i:i+2]) for i in range(len(w)-1)]
        grams += [" ".join(w[i:i+3]) for i in range(len(w)-2)]
        for g in grams:
            parts = g.split()
            if any(p in MONTHS for p in parts):
                continue
            if len(parts) == 1 and (g in STOP or g in NOISE or g.isdigit()):
                continue
            if len(parts) > 1 and (parts[0] in STOP or parts[-1] in STOP):
                continue
            total[g] += 1
            if g not in seen:
                docfreq[g] += 1
                seen.add(g)
            if g not in example and 25 < len(sent) < 320:
                example[g] = sent

rows = []
for g, c in total.items():
    n = len(g.split())
    # keep: unigrams seen >=4 times; bigrams >=4; trigrams >=4
    if c >= 4 and docfreq[g] >= 3:
        rows.append((g, n, c, docfreq[g], example.get(g, "")))

rows.sort(key=lambda r: (-r[2], -r[3]))
with open(os.path.join(SP, 'ngram_freq.csv'), 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(['term', 'ngram_len', 'total_freq', 'doc_freq_of_62', 'example_sentence'])
    wr.writerows(rows)

print("candidate terms:", len(rows))
print("unigrams:", sum(1 for r in rows if r[1] == 1),
      " bigrams:", sum(1 for r in rows if r[1] == 2),
      " trigrams:", sum(1 for r in rows if r[1] == 3))
