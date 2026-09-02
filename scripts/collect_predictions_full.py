"""Assemble results/predictions.json (keyed by decision id) from the transcribed interpreter outputs."""
import json, os, collections
from predictions_raw import CASES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
case_map = json.load(open(os.path.join(ROOT, 'scripts', 'case_map.json')))
in_scope = {d['id'] for d in json.load(open(os.path.join(ROOT, 'data', 'ground_truth.json')))}

preds = {}
missing = []
for case, _id in case_map.items():
    if _id not in in_scope:
        continue
    if case in CASES:
        preds[_id] = {**CASES[case], "blinded_file": "data/blinded/%s.txt" % _id}
    else:
        missing.append((case, _id))

json.dump(preds, open(os.path.join(ROOT, 'results', 'predictions.json'), 'w'), indent=2)
print("collected", len(preds), "/", len(in_scope))
if missing:
    print("MISSING:", missing)
print("pred class counts:", dict(collections.Counter(p['decision'] for p in preds.values())))
