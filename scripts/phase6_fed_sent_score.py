# -*- coding: utf-8 -*-
"""Aggregate the Fed-anchored sentence labels into a per-announcement score.

Each sentence of every RAW BoI announcement is labelled H / D / N by whether its
wording belongs in the Fed's HAWKISH draft (Alt C/D) or DOVISH draft (Alt A).

  score = (H - D) / total sentences      in [-1, +1]

Writes results/fed_sentence_scores.json  and  results/fed_sentence_labels_full.json
"""
import os, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENT = os.path.join(ROOT, 'data', 'fed_sentences')
LAB = os.path.join(ROOT, 'data', 'fed_sent_labels')

gt = {r['id']: r for r in json.load(open(os.path.join(ROOT, 'data', 'ground_truth.json'), encoding='utf-8'))}

rows, full, missing = [], [], []
for sf in sorted(glob.glob(os.path.join(SENT, '20*.json'))):
    dt = os.path.splitext(os.path.basename(sf))[0]
    lf = os.path.join(LAB, dt + '.json')
    sents = json.load(open(sf, encoding='utf-8'))['sentences']
    if not os.path.exists(lf):
        missing.append(dt); continue
    labs = json.load(open(lf, encoding='utf-8'))['labels']
    if len(labs) != len(sents):
        print(f"  !! {dt}: {len(labs)} labels vs {len(sents)} sentences")
        n = min(len(labs), len(sents)); labs, sents = labs[:n], sents[:n]
    H, D, N = labs.count('H'), labs.count('D'), labs.count('N')
    tot = len(labs)
    score = (H - D) / tot if tot else 0.0
    rows.append({"id": dt, "date": dt, "n": tot, "H": H, "D": D, "N": N,
                 "score": round(score, 4),
                 "decision": gt.get(dt, {}).get('decision', '')})
    for i, (s, l) in enumerate(zip(sents, labs), 1):
        full.append({"id": dt, "i": i, "label": l, "sentence": s})

rows.sort(key=lambda r: r['date'])
json.dump(rows, open(os.path.join(ROOT, 'results', 'fed_sentence_scores.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
json.dump(full, open(os.path.join(ROOT, 'results', 'fed_sentence_labels_full.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

if missing:
    print("MISSING label files:", missing)
print(f"scored {len(rows)} announcements | {len(full)} sentences")
if rows:
    T = sum(r['n'] for r in rows)
    print("label mix:  H %.1f%%  D %.1f%%  N %.1f%%" % (
        100*sum(r['H'] for r in rows)/T, 100*sum(r['D'] for r in rows)/T, 100*sum(r['N'] for r in rows)/T))
    sc = [r['score'] for r in rows]
    print("score range %+.3f .. %+.3f  mean %+.3f" % (min(sc), max(sc), sum(sc)/len(sc)))
    from collections import defaultdict
    by = defaultdict(list)
    for r in rows:
        by[r['decision']].append(r['score'])
    for k in ('lower', 'maintain', 'raise'):
        if by[k]:
            print(f"  mean score | {k:8s}: {sum(by[k])/len(by[k]):+.3f}  (n={len(by[k])})")
