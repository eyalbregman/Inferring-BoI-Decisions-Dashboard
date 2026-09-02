"""Shared helpers: parse BoI press-release title -> ground truth; blind the body."""
import re, calendar

MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}

def parse_title(title):
    """Return dict(date, new_rate, decision) from a 'The Monetary Committee decides on ...' title."""
    t = re.sub(r'\s+', ' ', title).strip()
    t = t.split('|')[0].strip()
    m = re.search(r'decides on ([A-Za-z]+) (\d{1,2}),? (\d{4})\s+to (.*)', t, re.I)
    if not m:
        raise ValueError("unparseable title: %r" % title)
    mon, day, year, rest = m.groups()
    date = "%s-%02d-%02d" % (year, MONTHS[mon.lower()], int(day))
    rest = rest.strip().rstrip('.').lower()

    # decision class
    if re.search(r'\b(leave|keep|left|kept|unchanged)\b', rest):
        decision = "maintain"
    elif re.search(r'\b(lower|reduce|reduces|reduced|cut|decrease)\b', rest):
        decision = "lower"
    elif re.search(r'\b(raise|raises|increase|increases|increased|hike)\b', rest):
        decision = "raise"
    else:
        decision = None

    # new rate: last "<x> percent" / "<x>%" in the title tail (handles "... to 4.5%" and "at 4.75 percent")
    rates = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', rest)
    new_rate = float(rates[-1]) if rates else None
    return {"date": date, "new_rate": new_rate, "decision": decision, "title_tail": rest}


# ---------------------------------------------------------------- blinding

BOILERPLATE = [
    r'^Home Page$', r'^Communication and [Pp]ublications$', r'^Press Releases$',
    r'^Back$', r'^Press Release$', r'^Share:?$', r'^Figures?$', r'^Data$',
    r'To view this (press release|message|notice)[^\n]*', r'^\s*click here\s*$',
    r'For the file of figures[^\n]*', r'^\s*This page was last updated[^\n]*',
    r'^\d{1,2}/\d{1,2}/\d{2,4}$',
    r'(full )?press release as a file', r'for this message as a file',
    r'as a file,?\s*click here', r'^\s*figure of figures',
]

HEBREW = re.compile(r'[֐-׿]')

# sentence-body char that does NOT break on a decimal point ("0.15")
_S = r'(?:[^.]|\.(?=\d))'
_PCT = r'-?\d+(?:\.\d+)?\s*(?:percentage\s+points?|percent|%)'

# explicit decision sentence(s) — the outcome is stated here
DECISION_SENT = re.compile(
    _S + r'*\b(?:Monetary )?Committee\b' + _S + r'*\bdecid' + _S + r'*?\b(lower|raise|raises|increase|'
    r'increases|reduce|reduces|left|leave|keep|kept|maintain|unchanged|'
    r'interest(?:\s+rate)?\s+(?:to|at|by))' + _S + r'*\.', re.I)

# "the Committee decided ..." — the whole sentence describes a policy action; drop it
COMMITTEE_DECIDED = re.compile(_S + r'*\b(?:Monetary )?Committee\b' + _S + r'*\bdecided\b' + _S + r'*\.', re.I)

# restatement of the decision that also names the policy-rate figure
_DECISION_WORD = (r'unchanged|lower|lowers|lowered|reduce|reduces|reduced|cut|raise|raises|'
                  r'raised|increase|increases|increased|leave|leaves|left|keep|keeps|kept|'
                  r'maintain|maintains|hold|holds')
POLICY_RATE_SENT = re.compile(
    r'\b(?:' + _DECISION_WORD + r')\b' + _S + r'{0,30}?\binterest(?:\s+rate)?\b' + _S + r'{0,60}?\b' + _PCT, re.I)

# sentence that reveals the *direction* of the rate cycle
DIRECTION_SENT = re.compile(
    _S + r'*\binterest\s+rate\b' + _S + r'*?\b(raising|lowering|reducing|increasing|cutting|'
    r'hiking|tightening|easing|rais\w*\s+the\s+interest|the\s+process\s+of\s+(?:raising|reducing))' + _S + r'*\.',
    re.I)
DIRECTION_SENT2 = re.compile(
    _S + r'*\b(?:pace|process|path|continuation)\s+of\s+' + _S + r'*?\b(raising|increases?|hikes?|'
    r'reduc\w+|cuts?|lowering)\b' + _S + r'*?\binterest' + _S + r'*\.', re.I)

# BoI policy-stance / rate-cycle language -> redact the sentence when it is about the BoI
_STANCE = re.compile(
    r'accommodat\w*\s+(?:monetary|policy|stance|measure)|'
    r'\bmonetary\s+policy\b[\w\s,]{0,22}?\baccommodat\w*|'
    r'\bpolicy\s+(?:remains?|is|stays?)\s+(?:very\s+|highly\s+)?accommodat\w*|'
    r'monetary\s+(?:tightening|easing|contraction|expansion|restraint|accommodation)|'
    r'(?:tighter|looser|more\s+restrictive|less\s+accommodative|degree\s+of)\s+(?:monetary|accommodat)|'
    r'restrictive\s+(?:monetary\s+)?(?:policy|stance|territory|level)|'
    r'removal\s+of\s+(?:the\s+)?(?:monetary\s+)?accommodation', re.I)
_DOMESTIC = re.compile(r'\bIsrael\b|\bthe\s+(?:Monetary\s+)?Committee\b|the Bank of Israel|'
                       r'\bthe\s+Governor\b|\bdomestic\b', re.I)

# rate-level fragments that sit close to the policy rate in the ZIRP era
RATE_LEVEL_FRAGS = [
    re.compile(r'\binterest\s+rate\s+of\s+' + _PCT, re.I),
    re.compile(_PCT + r'\s+interest\s+rate', re.I),
    re.compile(r'\bloans?\b([^.]{0,40}?)\bat\s+(?:a\s+)?' + _PCT, re.I),
]

MONTH_DATE = re.compile(
    r'\b(January|February|March|April|May|June|July|August|September|October|'
    r'November|December)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b', re.I)
NUM_DATE = re.compile(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b')


def blind(text, title):
    lines = [ln.strip() for ln in text.splitlines()]
    title_norm = re.sub(r'\s+', ' ', title.split('|')[0]).strip().lower()
    # also match the leading half of a two-line title ("... decides on January 5, 2026")
    title_head = title_norm.split(' to ')[0]

    kept = []
    for ln in lines:
        if not ln:
            continue
        low = re.sub(r'\s+', ' ', ln).strip().lower().rstrip('.')
        if low == title_norm.rstrip('.') or (len(low) > 25 and low == title_head):
            continue
        if low.startswith('the monetary committee decides on'):
            continue
        # orphaned second half of a split headline, e.g. "to lower the interest to 4 percent."
        if re.match(r'^to\s+(lower|raise|increase|reduce|reduc|leave|keep|maintain|hold)\b', low):
            continue
        if any(re.search(p, ln, re.I) for p in BOILERPLATE):
            continue
        if HEBREW.search(ln):          # embedded Hebrew snippet often restates the decision
            continue
        if title_norm and title_norm[:60] in low:
            continue
        kept.append(ln)

    body = "\n".join(kept)

    body = DECISION_SENT.sub(' [DECISION REDACTED] ', body)
    body = COMMITTEE_DECIDED.sub(' [DECISION REDACTED] ', body)
    body = DIRECTION_SENT.sub(' [DECISION REDACTED] ', body)
    body = DIRECTION_SENT2.sub(' [DECISION REDACTED] ', body)

    # stance/cycle sentences: redact when the sentence is about the BoI's own policy
    def _stance(m):
        s = m.group(0)
        if _STANCE.search(s) and _DOMESTIC.search(s):
            return ' [DECISION REDACTED] '
        return s
    body = re.sub(_S + r'*\.', _stance, body)
    body = POLICY_RATE_SENT.sub(' [RATE REDACTED] ', body)
    body = RATE_LEVEL_FRAGS[0].sub('interest rate of [RATE]', body)
    body = RATE_LEVEL_FRAGS[1].sub('[RATE] interest rate', body)
    body = RATE_LEVEL_FRAGS[2].sub(lambda m: 'loans' + m.group(1) + 'at [RATE]', body)

    body = MONTH_DATE.sub('[DATE]', body)
    body = NUM_DATE.sub('[DATE]', body)

    body = re.sub(r'[ \t]+', ' ', body)
    body = re.sub(r'\n\s*\n+', '\n\n', body).strip()
    return body
