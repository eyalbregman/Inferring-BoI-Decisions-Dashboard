"""Phase 1 (full history): all BoI rate decisions Nov 2018 -> today.
raw/, blinded/, ground_truth.json for the complete set."""
import json, os, re, glob, base64, zipfile, io
from lib_extract import parse_title, blind

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR = r'C:\Users\eyalb\.claude\projects\C--Users-eyalb-Desktop-Claude-Code-Projects-Hawkish-Dovish\93d1ff52-d996-4611-b36a-b47b4ad7bd80\tool-results'


def _unwrap(blob):
    """tool-results file -> the JS return value (a dict id->{...})."""
    try:
        d = json.loads(blob)
    except Exception:
        d = None
    if isinstance(d, list) and d and isinstance(d[0], dict) and 'text' in d[0]:
        blob = ''.join(x.get('text', '') for x in d)
    # blob is now a JSON string (possibly with trailing "(captured at origin ...)")
    s, _ = json.JSONDecoder().raw_decode(blob.lstrip())
    if isinstance(s, str):
        s = json.loads(s)
    return s


DOCS = {}   # id -> {title, text, url?}

# --- batch fetch files (full history)
BATCH_FILES = [
    'toolu_018YQXkaHsgt3Vji7bKDFdwn.json',
    'mcp-Claude_Browser-javascript_tool-1788350455468.txt',
    'mcp-Claude_Browser-javascript_tool-1788350612030.txt',
    'mcp-Claude_Browser-javascript_tool-1788350632156.txt',
    'mcp-Claude_Browser-javascript_tool-1788350649764.txt',
    'mcp-Claude_Browser-javascript_tool-1788350670521.txt',
]
for fn in BATCH_FILES:
    p = os.path.join(TR, fn)
    obj = _unwrap(open(p, encoding='utf-8').read())
    for _id, v in obj.items():
        if v.get('text'):
            DOCS[_id] = v

# 2023-11-27: the a27-11-23 slug is the Staff Forecast; c27-11-23 is the real decision
_nov27 = _unwrap(open(os.path.join(TR, 'mcp-Claude_Browser-javascript_tool-1788351649003.txt'), encoding='utf-8').read())
if _nov27.get('c27-11-23', {}).get('text'):
    v = _nov27['c27-11-23']
    v['url'] = "https://www.boi.org.il/en/communication-and-publications/press-releases/c27-11-23/ (via Wayback)"
    DOCS['2023-11-27'] = v

# --- smoke-test fetch (10 most recent) already parsed to clean innerText
recent = json.load(open(os.path.join(ROOT, 'scripts', 'raw_fetch_recent.json'), encoding='utf-8'))
for _id, v in recent.items():
    if _id != '2026-01-05' and v.get('text'):
        DOCS.setdefault(_id, v)

# --- 2026-01-05 from the .docx
docx_blob = _unwrap(open(os.path.join(TR, 'mcp-Claude_Browser-javascript_tool-1788267494231.txt'), encoding='utf-8').read())
docx_b64 = next(r['b64'] for r in docx_blob if r.get('b64'))
zf = zipfile.ZipFile(io.BytesIO(base64.b64decode(docx_b64)))
xml = zf.read('word/document.xml').decode('utf-8', 'ignore')
jan5_lines = []
for para in re.split(r'</w:p>', xml):
    line = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', para)).strip()
    if line:
        jan5_lines.append(line)
DOCS['2026-01-05'] = {
    "title": "The Monetary Committee decides on January 5, 2026 to lower the interest to 4 percent",
    "text": "\n".join(jan5_lines),
    "url": "https://www.boi.org.il/media/5v1anpil/january-5-2026-intrest-rate.docx (via Wayback)",
}

# ---------------------------------------------------------------- assemble
# November 2018 -> today (task scope). Rate before 2018-11-26 was 0.10 (unchanged since Feb 2015).
EXPECTED = [
 "2018-11-26",
 "2019-01-07","2019-02-25","2019-04-08","2019-05-20","2019-07-08","2019-08-28","2019-10-07","2019-11-25",
 "2020-01-09","2020-02-24","2020-04-06","2020-05-25","2020-07-06","2020-08-24","2020-10-22","2020-11-30",
 "2021-01-04","2021-02-22","2021-04-19","2021-05-31","2021-07-05","2021-08-23","2021-10-07","2021-11-22",
 "2022-01-03","2022-02-21","2022-04-11","2022-05-23","2022-07-04","2022-08-22","2022-10-03","2022-11-21",
 "2023-01-02","2023-02-20","2023-04-03","2023-05-22","2023-07-10","2023-09-04","2023-10-23","2023-11-27",
 "2024-01-01","2024-02-26","2024-04-08","2024-05-27","2024-07-08","2024-08-28","2024-10-09","2024-11-25",
 "2025-01-06","2025-02-24","2025-04-07","2025-05-26","2025-07-07","2025-08-20","2025-09-29","2025-11-24",
 "2026-01-05","2026-02-23","2026-03-30","2026-05-25","2026-07-06",
]

missing = [i for i in EXPECTED if i not in DOCS]
if missing:
    print("!! MISSING DOCS:", missing)

for d in (os.path.join(ROOT, 'data', 'raw'), os.path.join(ROOT, 'data', 'blinded')):
    os.makedirs(d, exist_ok=True)
# wipe old blinded/raw so a stale smoke-test file can't linger
for f in glob.glob(os.path.join(ROOT, 'data', 'blinded', '*.txt')):
    os.remove(f)
for f in glob.glob(os.path.join(ROOT, 'data', 'raw', '*.txt')):
    os.remove(f)

ground = []
prev_rate = 0.10   # BoI rate immediately before the Jan 2018 decision (unchanged since Feb 2015)
problems = []
for _id in EXPECTED:
    if _id not in DOCS:
        continue
    v = DOCS[_id]
    title, text = v['title'], v['text']
    if 'monetary committee decides' not in title.lower():
        problems.append("%s: title not a decision -> %r" % (_id, title[:90]))
    pt = parse_title(title)
    if pt['date'] != _id:
        problems.append("%s: title date mismatch -> %s" % (_id, pt['date']))
    new_rate = pt['new_rate']
    decision = pt['decision']
    change = round(new_rate - prev_rate, 2)
    sign = (change > 0) - (change < 0)
    lbl_sign = {"raise": 1, "lower": -1, "maintain": 0}[decision]
    mismatch = sign != lbl_sign
    if mismatch:
        problems.append("%s: sign mismatch change=%s label=%s" % (_id, change, decision))

    open(os.path.join(ROOT, 'data', 'raw', _id + '.txt'), 'w', encoding='utf-8').write(text)
    open(os.path.join(ROOT, 'data', 'blinded', _id + '.txt'), 'w', encoding='utf-8').write(blind(text, title))

    ground.append({
        "id": _id, "date": _id,
        "new_rate": new_rate, "prev_rate": prev_rate,
        "change": change, "decision": decision,
        "source_url": v.get('url', ''),
        "title": re.sub(r'\s+', ' ', title.split('|')[0]).strip(),
        "sign_check": "MISMATCH" if mismatch else "ok",
    })
    prev_rate = new_rate

json.dump(ground, open(os.path.join(ROOT, 'data', 'ground_truth.json'), 'w'), indent=2)

print("wrote ground_truth.json:", len(ground), "decisions")
import collections
print("class counts:", collections.Counter(g['decision'] for g in ground))
print("\nproblems:" if problems else "no problems")
for p in problems:
    print("  ", p)
