"""Phase 1 (smoke test): 10 most recent BoI rate decisions -> raw, blinded, ground_truth."""
import json, os, re, base64, zipfile, io
from lib_extract import parse_title, blind

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR = r'C:\Users\eyalb\.claude\projects\C--Users-eyalb-Desktop-Claude-Code-Projects-Hawkish-Dovish\93d1ff52-d996-4611-b36a-b47b4ad7bd80\tool-results'

def raw_decode(path):
    d = json.load(open(path, encoding='utf-8'))
    blob = ''.join(x['text'] for x in d) if isinstance(d, list) else d
    s, _ = json.JSONDecoder().raw_decode(blob)
    return json.loads(s)

# --- text + title for the 10 HTML-derived decisions (clean innerText captured earlier)
recent = json.load(open(os.path.join(ROOT, 'scripts', 'raw_fetch_recent.json'), encoding='utf-8'))

# --- raw HTML (to archive a .html copy per decision)
html_map = raw_decode(os.path.join(TR, 'mcp-Claude_Browser-javascript_tool-1788267526144.txt'))

# --- Jan 5 2026 from the .docx (no clean HTML archived)
docx_blob = raw_decode(os.path.join(TR, 'mcp-Claude_Browser-javascript_tool-1788267494231.txt'))
docx_b64 = next(r['b64'] for r in docx_blob if r.get('b64'))
zf = zipfile.ZipFile(io.BytesIO(base64.b64decode(docx_b64)))
xml = zf.read('word/document.xml').decode('utf-8', 'ignore')
paras = re.split(r'</w:p>', xml)
jan5_lines = []
for p in paras:
    chunks = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)
    line = ''.join(chunks).strip()
    if line:
        jan5_lines.append(line)
jan5_text = "\n".join(jan5_lines)
jan5_title = "The Monetary Committee decides on January 5, 2026 to lower the interest to 4 percent"

# ---------------------------------------------------------------- assemble
# id -> (title, raw_text, raw_html_or_None)
DOCS = {}
for _id, v in recent.items():
    if _id == '2026-01-05':
        continue  # earlier fetch grabbed the wrong page
    DOCS[_id] = (v['title'], v['text'], html_map.get(_id, {}).get('html'))
DOCS['2026-01-05'] = (jan5_title, jan5_text, None)

# the 10 test decisions, chronological; plus the prior decision (for prev_rate chaining only)
TEST_IDS = ["2025-05-26", "2025-07-07", "2025-08-20", "2025-09-29", "2025-11-24",
            "2026-01-05", "2026-02-23", "2026-03-30", "2026-05-25", "2026-07-06"]
PRIOR_ID = "2025-04-07"   # not scored; supplies prev_rate for the earliest test decision

for d in (os.path.join(ROOT, 'data', 'raw'), os.path.join(ROOT, 'data', 'blinded')):
    os.makedirs(d, exist_ok=True)

# prior decision rate
prior_title, _, _ = DOCS[PRIOR_ID]
prev_rate = parse_title(prior_title)['new_rate']
assert prev_rate is not None

ground = []
for _id in TEST_IDS:
    title, text, html = DOCS[_id]
    pt = parse_title(title)
    assert pt['date'] == _id, (pt['date'], _id)
    new_rate = pt['new_rate']
    change = round(new_rate - prev_rate, 2)
    decision = pt['decision']
    # cross-check sign of change vs label
    sign = (change > 0) - (change < 0)
    lbl_sign = {"raise": 1, "lower": -1, "maintain": 0}[decision]
    mismatch = sign != lbl_sign
    if mismatch:
        print("!! MISMATCH %s: change=%s label=%s" % (_id, change, decision))

    # write raw
    open(os.path.join(ROOT, 'data', 'raw', _id + '.txt'), 'w', encoding='utf-8').write(text)
    if html:
        open(os.path.join(ROOT, 'data', 'raw', _id + '.html'), 'w', encoding='utf-8').write(html)

    # blinded
    b = blind(text, title)
    open(os.path.join(ROOT, 'data', 'blinded', _id + '.txt'), 'w', encoding='utf-8').write(b)

    ground.append({
        "id": _id, "date": _id,
        "new_rate": new_rate, "prev_rate": prev_rate,
        "change": change, "decision": decision,
        "source_url": html_map.get(_id, {}).get('url') if _id != '2026-01-05'
                      else "https://www.boi.org.il/media/5v1anpil/january-5-2026-intrest-rate.docx (via Wayback)",
        "title": re.sub(r'\s+', ' ', title.split('|')[0]).strip(),
        "sign_check": "ok" if not mismatch else "MISMATCH",
    })
    prev_rate = new_rate

json.dump(ground, open(os.path.join(ROOT, 'data', 'ground_truth.json'), 'w'), indent=2)
print("wrote ground_truth.json with", len(ground), "decisions")
for g in ground:
    print("  %s  %-8s new=%-5s prev=%-5s chg=%+.2f  %s" %
          (g['id'], g['decision'], g['new_rate'], g['prev_rate'], g['change'], g['sign_check']))
