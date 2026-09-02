"""Flag any blinded file that may still reveal the BoI decision or its policy rate."""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gt = {d['id']: d for d in json.load(open(os.path.join(ROOT, 'data', 'ground_truth.json')))}

FOREIGN = re.compile(r'Federal Reserve|\bECB\b|European Central Bank|central banks?|'
                     r'\bFed\b|eurozone|United States|\bUS\b|China', re.I)
DEC = re.compile(r'\b(unchanged|lower|lowered|reduce|reduced|cut|raise|raised|increase|increased|'
                 r'leave|left|keep|kept|maintain|hold)\b', re.I)

problems = 0
for _id, d in sorted(gt.items()):
    txt = open(os.path.join(ROOT, 'data', 'blinded', _id + '.txt'), encoding='utf-8').read()
    for sent in re.split(r'(?<=\.)\s+', txt):
        s = sent.strip()
        low = s.lower()
        if 'interest' not in low and 'policy rate' not in low and 'the rate' not in low:
            continue
        if FOREIGN.search(s):
            continue  # foreign-CB context is allowed
        if DEC.search(s) and re.search(r'\d', s):
            print("[%s] SUSPECT: %s" % (_id, s[:200])); problems += 1
    # explicit new_rate figure next to 'interest'
    nr = ('%g' % d['new_rate'])
    for m in re.finditer(re.escape(nr) + r'\s*percent', txt):
        ctx = txt[max(0, m.start()-70):m.start()]
        if re.search(r'interest|policy rate', ctx, re.I) and not FOREIGN.search(ctx):
            print("[%s] RATE NEAR INTEREST: ...%s%s..." % (_id, ctx[-60:], m.group(0))); problems += 1
    # leftover explicit dates
    for m in re.finditer(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', txt):
        print("[%s] DATE LEFT: %s" % (_id, m.group(0))); problems += 1

print("\n%d potential problems" % problems)
