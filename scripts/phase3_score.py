"""Phase 3: join predictions to ground truth and score.
Usage: python phase3_score.py [variant]   (variant '' -> predictions.json/scores.json; 'rate' -> *_rate.json)"""
import json, os, collections, sys

VARIANT = sys.argv[1] if len(sys.argv) > 1 else ''
SUF = ('_' + VARIANT) if VARIANT else ''
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gt = {d['id']: d for d in json.load(open(os.path.join(ROOT, 'data', 'ground_truth.json')))}
preds = json.load(open(os.path.join(ROOT, 'results', 'predictions%s.json' % SUF)))

CLASSES = ["lower", "maintain", "raise"]
rows = []
for _id in sorted(gt):
    g = gt[_id]
    p = preds.get(_id, {})
    rows.append({
        "id": _id, "date": g['date'], "new_rate": g['new_rate'],
        "prev_rate": g['prev_rate'], "change": g['change'],
        "actual": g['decision'], "guess": p.get('decision'),
        "confidence": p.get('confidence'), "rationale": p.get('rationale'),
        "correct": p.get('decision') == g['decision'],
    })

n = len(rows)
correct = sum(r['correct'] for r in rows)
overall = correct / n if n else 0.0

per_class = {}
for c in CLASSES:
    sub = [r for r in rows if r['actual'] == c]
    per_class[c] = {
        "n": len(sub),
        "correct": sum(r['correct'] for r in sub),
        "accuracy": (sum(r['correct'] for r in sub) / len(sub)) if sub else None,
    }

actual_counts = collections.Counter(r['actual'] for r in rows)
majority_class, majority_n = actual_counts.most_common(1)[0]
baseline = majority_n / n if n else 0.0

# persistence baseline: predict each decision = the previous decision's actual outcome
# (a time-aware "you know what regime we're in" reference; first decision falls back to majority class)
persist_correct = 0
prev_actual = majority_class
for r in rows:
    if r['actual'] == prev_actual:
        persist_correct += 1
    prev_actual = r['actual']
persistence_baseline = persist_correct / n if n else 0.0

error_pairs = collections.Counter(
    (r['guess'], r['actual']) for r in rows if not r['correct'] and r['guess'])
error_pairs_named = [
    {"guessed": g, "actual": a, "count": c,
     "label": "Guessed %s -> was %s" % (g, a)}
    for (g, a), c in error_pairs.most_common()
]

summary = {
    "n_decisions": n,
    "overall_accuracy": overall,
    "correct": correct, "incorrect": n - correct,
    "per_class_accuracy": per_class,
    "actual_class_counts": dict(actual_counts),
    "majority_class": majority_class,
    "majority_class_baseline": baseline,
    "persistence_baseline": persistence_baseline,
    "error_pairs": error_pairs_named,
    "rows": rows,
}
summary["variant"] = VARIANT or "rate-blind"
json.dump(summary, open(os.path.join(ROOT, 'results', 'scores%s.json' % SUF), 'w'), indent=2)

print("N decisions          :", n)
print("Overall accuracy     : %.1f%% (%d/%d)" % (overall * 100, correct, n))
print("Majority-class baseline: %.1f%% (always predict '%s', %d/%d)" %
      (baseline * 100, majority_class, majority_n, n))
print("Persistence baseline   : %.1f%% (predict = previous decision's outcome)" %
      (persistence_baseline * 100))
print("Per-class accuracy:")
for c in CLASSES:
    pc = per_class[c]
    acc = "n/a" if pc['accuracy'] is None else "%.0f%%" % (pc['accuracy'] * 100)
    print("  %-9s %s (%d/%d)" % (c, acc, pc['correct'], pc['n']))
print("Error pairs (guessed -> actual), incorrect only:")
for e in error_pairs_named:
    print("  %-32s x%d" % (e['label'], e['count']))
if not error_pairs_named:
    print("  (none)")
