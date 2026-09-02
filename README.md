# Can a language model read a Bank of Israel rate decision from the reasoning alone?

An experiment. Every Bank of Israel interest-rate announcement from **November 2018 to today**
(62 decisions) is stripped of everything that reveals the outcome — the headline, the decision
sentence, the stated policy-rate figure, the direction/stance language, and all dates. A language
model then reads only the remaining economic reasoning (inflation, growth, the shekel, the labour
market, geopolitics) and predicts the decision: **lower**, **maintain**, or **raise**.

Each announcement is classified by a fresh subagent in an isolated context, so the model never
sees another announcement, the dates, or the true decisions. Ground truth is parsed from the
press-release titles and kept in a file the interpreter never reads.

**[→ Live dashboard](https://eyalbregman.github.io/Inferring-BoI-Decisions-Dashboard/)**

## Headline results

| | Reasoning only | + prior rate level |
|---|---|---|
| Overall accuracy | 85.5% (53/62) | 91.9% (57/62) |
| Majority-class baseline ("always maintain") | 72.6% | 72.6% |
| Persistence baseline ("same as last meeting") | 82.3% | 82.3% |
| Hikes (raise) | 11/11 | 11/11 |
| Holds (maintain) | 42/45 | 44/45 |
| **Cuts (lower)** | **0/6** | **2/6** |

The model nails every hiking cycle and nearly every hold, but from the reasoning alone it caught
**none of the six rate cuts** — blinded BoI cut announcements read as balanced "holds". Telling
the model the interest-rate *level* in effect before the decision (but not the previous decision)
recovers two of the cuts: it can then see that a high rate leaves room to cut, and that a rate
already at the floor cannot be cut.

## Layout

```
data/raw/            full press releases (extracted text; HTML where available)
data/blinded/        rationale-only text the interpreter sees
data/ground_truth.json
results/predictions.json          predictions.json  (reasoning only)
results/predictions_rate.json     predictions      (prior rate level also given)
results/scores.json  results/scores_rate.json
docs/index.html      the dashboard (GitHub Pages entry)
.claude/agents/interpreter.md     the classifier subagent
scripts/             scrape / blind / score / dashboard pipeline
```

## Reproduce

```
python scripts/phase1_full.py        # parse titles -> ground_truth, blind the bodies
python scripts/audit_blind.py         # check nothing reveals the outcome
python scripts/collect_predictions_full.py   # assemble predictions.json
python scripts/collect_predictions_rate.py   # assemble predictions_rate.json
python scripts/phase3_score.py        # score (reasoning only)
python scripts/phase3_score.py rate   # score (prior rate level)
python scripts/phase4_dashboard.py    # build the dashboard
```

Source press releases are retrieved through the Wayback Machine (`boi.org.il` blocks automated
access). Two decisions (5 Jan 2026, 27 Nov 2023) were parsed from the BoI's `.docx` copies.

## Notes / limitations

- Ground truth is derived from press-release titles; all 62 pass a sign-of-change vs. label check.
- The interpreter is a general LLM: it carries a pretraining prior that central banks hold more
  often than they move. That prior — not leakage from this dataset — is likely why it defaults to
  "maintain" on the hedged cut announcements.
- With 62 decisions and two effective classes in most eras, small accuracy gaps are within noise;
  the baselines matter more than the headline number.
