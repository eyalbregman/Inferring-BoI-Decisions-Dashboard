"""Assemble results/predictions.json from the interpreter subagent outputs (keyed by decision id)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
case_map = json.load(open(os.path.join(ROOT, 'scripts', 'case_map.json')))

# raw interpreter JSON outputs, keyed by the neutral case name it was given
CASES = {
 "case_01.txt": {"decision":"maintain","confidence":0.82,"rationale":"Inflation sits at the 2% target midpoint with expectations anchored, but war-driven activity contraction, extreme geopolitical uncertainty, upside inflation risks from energy/housing/wages, and major central banks holding steady all point to a wait-and-see hold."},
 "case_02.txt": {"decision":"maintain","confidence":0.83,"rationale":"Inflation in the upper target range with upside risks and a tight labor market, offset by fragile growth, shekel appreciation, and heavy emphasis on geopolitical uncertainty — a wait-and-see hold."},
 "case_03.txt": {"decision":"maintain","confidence":0.88,"rationale":"Despite inflation slightly above target, shekel depreciation, and a tight labor market, the pervasive geopolitical uncertainty, still-recovering activity, contracting Q2 GDP, anchored inflation expectations, and explicit wait-and-see framing point to holding the rate steady."},
 "case_04.txt": {"decision":"maintain","confidence":0.82,"rationale":"Inflation at target midpoint, growth contracting but recovering, rising global inflation risks offset by sharp shekel appreciation, high geopolitical uncertainty, peer central banks on hold — a balanced wait-and-see hold."},
 "case_05.txt": {"decision":"lower","confidence":0.58,"rationale":"Inflation has moderated to 2.4% and is projected to fall to 1.7%, the shekel appreciated sharply, wage growth and home prices are decelerating, and labor supply constraints are easing, outweighing noted upside risks and a strong growth outlook."},
 "case_06.txt": {"decision":"maintain","confidence":0.72,"rationale":"Inflation sits at the target midpoint (1.8%) with anchored expectations and a stronger shekel, but robust above-trend growth, a tight labor market, re-accelerating housing costs, elevated geopolitical/oil risks and explicit upside inflation risks argue against easing, leaving a wait-and-see hold."},
 "case_07.txt": {"decision":"maintain","confidence":0.72,"rationale":"Inflation near target midpoint and lower energy prices are offset by a tight labor market, rapid wage growth, shekel depreciation and high geopolitical uncertainty, with the committee using balanced, data-dependent wait-and-see framing."},
 "case_08.txt": {"decision":"maintain","confidence":0.70,"rationale":"Inflation has moderated into the target range with expectations anchored near the midpoint, but a sharp activity rebound, a tight labor market with accelerating wages, and explicit upside inflation risks offset the disinflationary shekel appreciation, pointing to a wait-and-see hold."},
 "case_09.txt": {"decision":"maintain","confidence":0.90,"rationale":"Despite above-target inflation of 3.6%, weak growth below trend, wartime uncertainty, shekel appreciation, and a wait-and-see framing focused on market stabilization point to holding the rate unchanged."},
 "case_10.txt": {"decision":"maintain","confidence":0.72,"rationale":"Inflation at 3.1% is still above the target upper bound and the labor market remains tight with strong wage growth, but sharp shekel appreciation, a falling risk premium, moderate below-trend activity, well-anchored expectations, and explicit conditional forward guidance amid high geopolitical uncertainty point to a wait-and-see hold."},
}

preds = {}
for case, obj in CASES.items():
    _id = case_map[case]
    preds[_id] = {**obj, "blinded_file": "data/blinded/%s.txt" % _id}

os.makedirs(os.path.join(ROOT, 'results'), exist_ok=True)
json.dump(preds, open(os.path.join(ROOT, 'results', 'predictions.json'), 'w'), indent=2)
print("wrote", len(preds), "predictions")
