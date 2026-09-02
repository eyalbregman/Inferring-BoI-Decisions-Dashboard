"""Assemble results/predictions_rate.json (interpreter also knew the prior rate LEVEL)."""
import json, os, collections
from predictions_raw_rate import CASES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rcase_map = json.load(open(os.path.join(ROOT, 'scripts', 'rcase_map.json')))
in_scope = {d['id'] for d in json.load(open(os.path.join(ROOT, 'data', 'ground_truth.json')))}

preds, missing = {}, []
for case, _id in rcase_map.items():
    if _id not in in_scope:
        continue
    if case in CASES:
        preds[_id] = {**CASES[case], "blinded_file": "data/blinded/%s.txt" % _id,
                      "given_prior_rate": True}
    else:
        missing.append((case, _id))

json.dump(preds, open(os.path.join(ROOT, 'results', 'predictions_rate.json'), 'w'), indent=2)
print("collected", len(preds), "/", len(in_scope))
if missing:
    print("MISSING:", missing)
print("pred class counts:", dict(collections.Counter(p['decision'] for p in preds.values())))
