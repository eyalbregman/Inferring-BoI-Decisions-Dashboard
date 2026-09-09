# -*- coding: utf-8 -*-
"""Fed-anchored hawkish / dovish lexicon for scoring RAW Bank of Israel announcements.

Method (per the user's brief, after Doh, Song & Yang 2025):
  The Federal Reserve staff drafts, for every FOMC meeting, a DOVISH alternative
  statement (Alt A) and a HAWKISH one (Alt C / D). We pooled 75 meetings' worth of
  those drafts (2009-2020, from Bluebook / Tealbook-B, federalreserve.gov), measured
  which words and phrasings systematically separate the hawkish pole from the dovish
  pole (weighted log-odds, Monroe, Colaresi & Quinn 2008), and hand-read a spanning
  sample of Alt A vs Alt C pairs. This lexicon is that contrast vocabulary, curated
  with judgment, translated into the phrasings the Bank of Israel actually uses, and
  extended with the decision + forward-guidance language the user asked to include
  ("tightness is more hawkish"). Every term below occurs in the 62-announcement
  BoI corpus (verified by scripts/phase6_fed_score.py).

  H = hawkish pole   (Fed Alt C/D language: raising / restraining / "strong" / "tight"
                      / confidence that inflation is or will be a problem)
  D = dovish  pole   (Fed Alt A language: lowering / accommodation / "soft" / "weak"
                      / downside risks / global drag / low inflation / patience)
  C = context-set    (kept for transparency; contributes 0 to the score)

  source:  fed        - surfaced directly by the Fed Alt-A / Alt-C contrast
           fed+judg   - Fed contrast, generalised / re-expressed in BoI idiom
           judgment   - added by judgment (decision & guidance vocab, BoI idiom)

The policy decision is deliberately NOT hidden: on raw announcements the decision
sentence and the stance / guidance language are part of the score.

tuple: (term, category, direction, source, logic)
"""

LEXICON = [

# --- Policy action ---
('raise the interest rate', 'Policy action', 'H', 'fed', "Alt C: 'decided to raise the target range'."),
('raise the interest', 'Policy action', 'H', 'fed', 'Rate hike -> hawkish.'),
('increase the interest rate', 'Policy action', 'H', 'fed', 'Rate hike -> hawkish.'),
('to increase the interest', 'Policy action', 'H', 'fed', 'Rate hike -> hawkish.'),
('increased the interest rate', 'Policy action', 'H', 'fed', 'Rate hike -> hawkish.'),
('increase the interest rate by', 'Policy action', 'H', 'fed', 'Rate hike -> hawkish.'),
('raising the interest rate', 'Policy action', 'H', 'fed+judg', 'Hiking cycle -> hawkish.'),
('the process of raising the interest', 'Policy action', 'H', 'fed+judg', 'Explicit hiking process -> hawkish.'),
('process of increasing the interest', 'Policy action', 'H', 'fed+judg', 'Explicit hiking process -> hawkish.'),
('increasing the interest rate', 'Policy action', 'H', 'fed+judg', 'Hiking -> hawkish.'),
('further increase', 'Policy action', 'H', 'fed+judg', 'More hikes flagged -> hawkish.'),
('lower the interest rate', 'Policy action', 'D', 'fed', "Alt A: 'decided to lower the target range'."),
('lower the interest', 'Policy action', 'D', 'fed', 'Rate cut -> dovish.'),
('to lower the interest', 'Policy action', 'D', 'fed', 'Rate cut -> dovish.'),
('reduce the interest rate', 'Policy action', 'D', 'fed', 'Rate cut -> dovish.'),
('to reduce the interest', 'Policy action', 'D', 'fed', 'Rate cut -> dovish.'),
('reduce the interest', 'Policy action', 'D', 'fed', 'Rate cut -> dovish.'),
('reducing the interest rate', 'Policy action', 'D', 'fed+judg', 'Cutting -> dovish.'),
('lowering the interest rate', 'Policy action', 'D', 'fed+judg', 'Cutting cycle -> dovish.'),

# --- Forward guidance & stance ---
('monetary restraint', 'Forward guidance & stance', 'H', 'fed+judg', 'Restrictive stance -> hawkish.'),
('restrictive', 'Forward guidance & stance', 'H', 'fed', 'Alt C stance word -> hawkish.'),
('monetary tightening', 'Forward guidance & stance', 'H', 'fed+judg', 'Tightening -> hawkish.'),
('the process of monetary tightening', 'Forward guidance & stance', 'H', 'fed+judg', 'Tightening cycle -> hawkish.'),
('tightening', 'Forward guidance & stance', 'H', 'fed', "Alt C: 'tighten' -> hawkish."),
('tighten', 'Forward guidance & stance', 'H', 'fed', "Alt C: 'labor market ... tighten' -> hawkish."),
('rising path of the interest rate', 'Forward guidance & stance', 'H', 'fed+judg', 'Explicit upward path -> hawkish.'),
('interest rate path', 'Forward guidance & stance', 'C', 'judgment', "Direction set by 'rising' / 'declining'."),
('gradual and cautious', 'Forward guidance & stance', 'H', 'judgment', 'In BoI, describes a *rising* rate path -> hawkish.'),
('accommodative', 'Forward guidance & stance', 'D', 'fed', 'Alt A stance word -> dovish.'),
('accommodation', 'Forward guidance & stance', 'D', 'fed', "Alt A: 'policy accommodation' -> dovish."),
('policy accommodation', 'Forward guidance & stance', 'D', 'fed', 'Alt A -> dovish.'),
('monetary accommodation', 'Forward guidance & stance', 'D', 'fed', 'Alt A -> dovish.'),
('expand the use', 'Forward guidance & stance', 'D', 'judgment', "BoI: 'expand the use of the tools' -> dovish."),
('range of tools', 'Forward guidance & stance', 'D', 'fed+judg', 'Emphasising the easing toolkit -> dovish lean.'),
('will act to', 'Forward guidance & stance', 'C', 'judgment', 'BoI boilerplate close; weak signal.'),
('support economic activity', 'Forward guidance & stance', 'D', 'fed+judg', 'Growth-support objective foregrounded -> dovish.'),
('supporting economic activity', 'Forward guidance & stance', 'D', 'fed+judg', 'Growth-support objective -> dovish.'),
('for an extended period', 'Forward guidance & stance', 'D', 'fed', 'Alt A: low-for-long guidance -> dovish.'),
('extended period', 'Forward guidance & stance', 'D', 'fed', 'Alt A: low-for-long -> dovish.'),
('considerable time', 'Forward guidance & stance', 'D', 'fed', 'Alt A: low-for-long guidance -> dovish.'),
('for some time', 'Forward guidance & stance', 'D', 'fed', "Alt A: 'below levels ... for some time' -> dovish (low-for-long)."),
('for a prolonged', 'Forward guidance & stance', 'D', 'fed+judg', 'Low-for-long guidance -> dovish.'),
('prolonged period', 'Forward guidance & stance', 'D', 'fed+judg', 'Low-for-long guidance -> dovish.'),
('stabilizing the markets', 'Forward guidance & stance', 'D', 'judgment', 'BoI crisis-support objective -> dovish.'),
('reducing uncertainty', 'Forward guidance & stance', 'D', 'judgment', 'BoI crisis-support objective -> dovish.'),

# --- Inflation ---
('high inflation', 'Inflation', 'H', 'fed+judg', 'High inflation -> hawkish.'),
('inflation increased', 'Inflation', 'H', 'fed+judg', 'Rising inflation -> hawkish.'),
('increase in inflation', 'Inflation', 'H', 'fed+judg', 'Rising inflation -> hawkish.'),
('acceleration of inflation', 'Inflation', 'H', 'fed+judg', 'Faster price growth -> hawkish.'),
('renewed acceleration', 'Inflation', 'H', 'judgment', 'Disinflation reversing -> hawkish.'),
('above the upper bound', 'Inflation', 'H', 'fed+judg', 'Inflation above the band -> hawkish.'),
('above the target', 'Inflation', 'H', 'fed+judg', 'Inflation above target -> hawkish.'),
('remains above the', 'Inflation', 'H', 'fed+judg', "'inflation remains above the target' -> hawkish."),
('price increases', 'Inflation', 'H', 'fed+judg', 'Rising prices -> hawkish.'),
('broad-based', 'Inflation', 'H', 'judgment', "BoI: 'broad-based increase in inflation' -> hawkish."),
('sticky', 'Inflation', 'H', 'judgment', 'Inflation resisting decline -> hawkish.'),
('risks of renewed acceleration of inflation', 'Inflation', 'H', 'judgment', 'Explicit upside inflation risk -> hawkish.'),
('below the lower bound', 'Inflation', 'D', 'fed+judg', 'Inflation below the band -> dovish.'),
('below the target', 'Inflation', 'D', 'fed+judg', 'Inflation below target -> dovish.'),
('inflation remains low', 'Inflation', 'D', 'fed+judg', 'Persistently low inflation -> dovish.'),
('inflation moderated', 'Inflation', 'D', 'fed+judg', 'Slower price growth -> dovish.'),
('moderation of inflation', 'Inflation', 'D', 'fed+judg', 'Slower price growth -> dovish.'),
('moderation in inflation', 'Inflation', 'D', 'fed+judg', 'Slower price growth -> dovish.'),
('decline in inflation', 'Inflation', 'D', 'fed+judg', 'Falling inflation -> dovish.'),
('convergence of inflation', 'Inflation', 'D', 'judgment', 'Inflation heading back to target -> dovish.'),
('converging to the target', 'Inflation', 'D', 'judgment', 'Inflation heading to target -> dovish.'),
('negative inflation', 'Inflation', 'D', 'judgment', 'Deflation -> strongly dovish.'),

# --- Labor market ---
('labor market remains tight', 'Labor market', 'H', 'fed+judg', 'Excess labour demand -> hawkish.'),
('the labor market remains tight', 'Labor market', 'H', 'fed+judg', 'Excess labour demand -> hawkish.'),
('tight labor market', 'Labor market', 'H', 'fed+judg', 'Excess labour demand -> hawkish.'),
('labor market ... tight', 'Labor market', 'H', 'fed', "Alt C: 'strengthen tighten' -> hawkish."),
('full employment', 'Labor market', 'H', 'fed+judg', 'No labour slack -> hawkish.'),
('high level of demand', 'Labor market', 'H', 'judgment', 'BoI: tight-labour phrase -> hawkish.'),
('excess demand', 'Labor market', 'H', 'fed+judg', 'Demand above supply -> hawkish.'),
('shortage of workers', 'Labor market', 'H', 'judgment', 'Excess labour demand -> hawkish.'),
('supply constraints', 'Labor market', 'H', 'judgment', 'Constrained supply -> price pressure -> hawkish.'),
('wages are increasing rapidly', 'Labor market', 'H', 'judgment', 'Fast wage growth -> hawkish.'),
('labor market weakness', 'Labor market', 'D', 'fed+judg', 'Weak labour demand -> dovish.'),
('unemployment rate increased', 'Labor market', 'D', 'fed+judg', 'Rising joblessness -> dovish.'),
('easing of the supply', 'Labor market', 'D', 'judgment', 'Labour supply improving -> dovish.'),
('decline in the pace of wage increases', 'Labor market', 'D', 'judgment', 'Slower wages -> dovish.'),

# --- Activity & demand ---
('economic activity remains strong', 'Activity & demand', 'H', 'fed+judg', 'Strong demand -> hawkish.'),
('activity remains strong', 'Activity & demand', 'H', 'fed+judg', 'Strong demand -> hawkish.'),
('strong economic activity', 'Activity & demand', 'H', 'fed+judg', 'Strong demand -> hawkish.'),
('robust', 'Activity & demand', 'H', 'fed+judg', "Alt C: 'job gains ... robust' -> hawkish."),
('lively economic activity', 'Activity & demand', 'H', 'judgment', 'BoI phrase -> hawkish.'),
('grew significantly', 'Activity & demand', 'H', 'fed+judg', 'Strong GDP -> hawkish.'),
('expanded sharply', 'Activity & demand', 'H', 'fed+judg', 'Strong GDP -> hawkish.'),
('above the ... trend', 'Activity & demand', 'H', 'judgment', 'Positive output gap -> hawkish.'),
('soft', 'Activity & demand', 'D', 'fed', "Alt A: 'business investment ... soft' -> dovish."),
('weak', 'Activity & demand', 'D', 'fed+judg', 'Weak activity -> dovish.'),
('weakness', 'Activity & demand', 'D', 'fed+judg', 'Weak activity -> dovish.'),
('weakened', 'Activity & demand', 'D', 'fed', "Alt A: 'exports have weakened' -> dovish."),
('has weakened', 'Activity & demand', 'D', 'fed', 'Alt A -> dovish.'),
('moderated', 'Activity & demand', 'D', 'fed', "Alt A: 'spending moderated from its strong pace' -> dovish."),
('slowdown', 'Activity & demand', 'D', 'fed+judg', 'Growth decelerating -> dovish.'),
('slowdown in economic activity', 'Activity & demand', 'D', 'fed+judg', 'Growth decelerating -> dovish.'),
('moderation of activity', 'Activity & demand', 'D', 'fed+judg', 'Growth decelerating -> dovish.'),
('moderation in economic activity', 'Activity & demand', 'D', 'fed+judg', 'Growth decelerating -> dovish.'),
('contraction', 'Activity & demand', 'D', 'fed+judg', 'Output falling -> dovish.'),
('contracted', 'Activity & demand', 'D', 'fed+judg', 'Output falling -> dovish.'),
('recession', 'Activity & demand', 'D', 'fed+judg', 'Downturn -> strongly dovish.'),
('below the ... trend', 'Activity & demand', 'D', 'judgment', 'Negative output gap -> dovish.'),
('deterioration', 'Activity & demand', 'D', 'fed+judg', 'Conditions deteriorating -> dovish.'),
('worsening', 'Activity & demand', 'D', 'fed+judg', 'Conditions deteriorating -> dovish.'),

# --- Financial conditions & risk ---
('risk premium increased', 'Financial conditions & risk', 'H', 'judgment', 'Higher risk premium / weaker shekel -> hawkish.'),
('spreads widened', 'Financial conditions & risk', 'H', 'judgment', 'Higher risk pricing -> hawkish.'),
('shekel weakened', 'Financial conditions & risk', 'H', 'judgment', 'Weaker shekel -> imported inflation -> hawkish.'),
('shekel depreciated', 'Financial conditions & risk', 'H', 'judgment', 'Weaker shekel -> hawkish.'),
('depreciation', 'Financial conditions & risk', 'H', 'judgment', 'Currency weakening -> hawkish for inflation.'),
('downside', 'Financial conditions & risk', 'D', 'fed', "Alt A: 'risks ... tilted to the downside' -> dovish."),
('global developments', 'Financial conditions & risk', 'D', 'fed', "Alt A: 'implications of global developments' -> dovish."),
('shekel strengthened', 'Financial conditions & risk', 'D', 'judgment', 'Stronger shekel -> disinflationary -> dovish.'),
('shekel appreciated', 'Financial conditions & risk', 'D', 'judgment', 'Stronger shekel -> dovish.'),
('appreciation', 'Financial conditions & risk', 'D', 'judgment', 'Currency strengthening -> dovish.'),
('risk premium ... declined', 'Financial conditions & risk', 'D', 'judgment', 'Lower risk premium -> dovish.'),
('financing constraints', 'Financial conditions & risk', 'D', 'judgment', 'Tighter credit access -> demand drag -> dovish.'),
('uncertainty', 'Financial conditions & risk', 'D', 'fed+judg', 'Caution signal -> dovish lean.'),
('geopolitical uncertainty', 'Financial conditions & risk', 'D', 'judgment', 'Caution signal -> dovish lean.'),

# --- Rhetorical intensity ---
# NB the generic Fed-contrast hedges (slight / moderate / somewhat / relatively) are
# dropped for the BoI application: they are Fed-discriminating but far too common as
# neutral descriptors in the (much longer) BoI announcements, where they swamp the
# stance signal. Only intensity words with real directional content are kept.
('rapid', 'Rhetorical intensity', 'H', 'fed+judg', 'Amplifier (rapid growth / credit / wages) -> hawkish lean.'),
('rapidly', 'Rhetorical intensity', 'H', 'fed+judg', 'Amplifier -> hawkish lean.'),
('strongly', 'Rhetorical intensity', 'H', 'fed', "Alt C: 'grow strongly' -> hawkish lean."),
('continued to strengthen', 'Rhetorical intensity', 'H', 'fed', 'Alt C persistence-of-strength -> hawkish.'),
('temporary', 'Rhetorical intensity', 'D', 'fed', "Alt A: price rises are 'temporary / transitory' -> dovish."),
('transitory', 'Rhetorical intensity', 'D', 'fed', "Alt A: inflation drivers 'transitory' -> dovish."),
]
