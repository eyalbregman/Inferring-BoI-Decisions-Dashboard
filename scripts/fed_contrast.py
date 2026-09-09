# -*- coding: utf-8 -*-
"""Weighted log-odds (Monroe, Colaresi & Quinn 2008) contrast between the Fed's
DOVISH alternative drafts (Alt A) and HAWKISH alternative drafts (Alt C/D).

Positive z  -> term is characteristically HAWKISH-draft language
Negative z  -> term is characteristically DOVISH-draft language
"""
import glob, os, re, collections, math, csv

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALTS = os.path.join(HERE, 'data', 'fed_alts')

def load(pat):
    txt = []
    for f in glob.glob(os.path.join(ALTS, pat)):
        txt.append(open(f, encoding='utf-8').read())
    return "\n".join(txt)

DOVE = load('*__A.txt')
HAWK = load('*__C.txt') + "\n" + load('*__D.txt')

STOPW = set("""a an the and or but if then of to in on at by for with from into over under as is are was
were be been being this that these those it its it's they them their there we our us will would can
could may might must should shall not no nor than so such very more most much many few some any all
each both other into out up down off then once here when where why how which who whom whose what
committee federal open market reserve percent point points rate rates funds target range meeting
information received since met indicates data statement alternative b's b i ii iii iv""".split())

def toks(t):
    t = t.lower()
    t = re.sub(r"[^a-z\s'-]", " ", t)
    return [w.strip("'-") for w in t.split() if w.strip("'-") and len(w) > 1]

def grams(ws):
    g = list(ws)
    g += [" ".join(ws[i:i+2]) for i in range(len(ws)-1)]
    g += [" ".join(ws[i:i+3]) for i in range(len(ws)-2)]
    return g

def count(t):
    ws = toks(t)
    c = collections.Counter()
    for g in grams(ws):
        parts = g.split()
        if len(parts) == 1 and g in STOPW:
            continue
        if len(parts) > 1 and (parts[0] in STOPW or parts[-1] in STOPW):
            continue
        c[g] += 1
    return c

ch = count(HAWK)
cd = count(DOVE)
vocab = set(ch) | set(cd)

# informative Dirichlet prior = overall frequency, alpha0 scale
a0 = 1000.0
tot = collections.Counter()
for g in vocab:
    tot[g] = ch[g] + cd[g]
Stot = sum(tot.values())
nh = sum(ch.values()); nd = sum(cd.values())

rows = []
for g in vocab:
    if tot[g] < 6:            # need a few occurrences to be meaningful
        continue
    aw = a0 * tot[g] / Stot
    l_h = math.log((ch[g] + aw) / (nh + a0 - ch[g] - aw))
    l_d = math.log((cd[g] + aw) / (nd + a0 - cd[g] - aw))
    delta = l_h - l_d
    var = 1.0/(ch[g] + aw) + 1.0/(cd[g] + aw)
    z = delta / math.sqrt(var)
    rows.append((g, len(g.split()), ch[g], cd[g], round(z, 2)))

rows.sort(key=lambda r: r[4])
with open(os.path.join(HERE, 'data', 'fed_contrast.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f); w.writerow(['term', 'n', 'hawk_ct', 'dove_ct', 'z'])
    w.writerows(rows)

print(f"DOVE tokens {nd} | HAWK tokens {nh} | vocab kept {len(rows)}")
print("\n===== MOST HAWKISH-DRAFT TERMS (top z) =====")
for r in rows[-45:][::-1]:
    print(f"  {r[4]:+6.2f}  h{r[2]:<3} d{r[3]:<3}  {r[0]}")
print("\n===== MOST DOVISH-DRAFT TERMS (bottom z) =====")
for r in rows[:45]:
    print(f"  {r[4]:+6.2f}  h{r[2]:<3} d{r[3]:<3}  {r[0]}")
