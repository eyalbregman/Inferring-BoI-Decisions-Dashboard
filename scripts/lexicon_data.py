# -*- coding: utf-8 -*-
"""Hawkish / dovish lexicon for Bank of Israel interest-rate announcements.

REFRAMED: this lexicon scores the STRENGTH AND CONFIDENCE OF THE LANGUAGE, not
the economic content and not the policy decision.

  H = strong / confident / emphatic  -- the sentence commits to a claim, amplifies
      it, or asserts it flatly ("rose sharply", "remains tight", "will", "significant").
  D = soft / hedged / tentative      -- the sentence qualifies, downplays or doubts
      the claim ("rose slightly", "may", "appears", "around", "uncertainty").
  N = neutral                        -- a plain factual verb or noun with no
      rhetorical charge on its own; listed only to mark it as deliberately unscored.

The label is subject-independent. "increased sharply" is strong language whether the
subject is inflation, unemployment, the shekel or bond yields, and whether that
month's decision was lower, maintain or raise. A plain "increased" is neutral; the
signal lives in the modifier, the modal and the framing, not in the noun.

Every term below occurs in the 62-announcement corpus (data/raw/*.txt, Nov 2018 -
today); counts are verified by scripts/lexicon_build_xlsx.py.

tuple: (term, category, direction, logic)
"""

LEXICON = [

# ============================================================ MAGNITUDE - AMPLIFIERS  (strong)
("sharp", "Magnitude - amplifier", "H", "Maximal-size word; asserts a large move."),
("sharply", "Magnitude - amplifier", "H", "Maximal-size adverb; asserts a large move."),
("sharp increase", "Magnitude - amplifier", "H", "Amplified rise - emphatic."),
("sharp decline", "Magnitude - amplifier", "H", "Amplified fall - emphatic."),
("sharp rise", "Magnitude - amplifier", "H", "Amplified rise - emphatic."),
("significant", "Magnitude - amplifier", "H", "Claims the move matters; confident framing."),
("significantly", "Magnitude - amplifier", "H", "Claims the move matters; confident framing."),
("considerable", "Magnitude - amplifier", "H", "Large-size word; emphatic."),
("marked", "Magnitude - amplifier", "H", "'Marked increase / decline' - emphatic, definite."),
("markedly", "Magnitude - amplifier", "H", "Emphatic adverb of size."),
("marked increase", "Magnitude - amplifier", "H", "Amplified rise - emphatic."),
("marked decline", "Magnitude - amplifier", "H", "Amplified fall - emphatic."),
("rapid", "Magnitude - amplifier", "H", "Maximal-speed word; asserts a fast move."),
("rapidly", "Magnitude - amplifier", "H", "Maximal-speed adverb."),
("rapid pace", "Magnitude - amplifier", "H", "'at a rapid pace' - emphatic speed."),
("at a rapid pace", "Magnitude - amplifier", "H", "Emphatic speed framing."),
("strong", "Magnitude - amplifier", "H", "Emphatic strength word."),
("strongly", "Magnitude - amplifier", "H", "Emphatic adverb."),
("robust", "Magnitude - amplifier", "H", "Emphatic strength word."),
("solid", "Magnitude - amplifier", "H", "Emphatic strength word."),
("steep", "Magnitude - amplifier", "H", "Emphatic-size word for a move."),
("severe", "Magnitude - amplifier", "H", "Maximal-severity word."),
("broad-based", "Magnitude - amplifier", "H", "Claims the move is widespread, not a one-off - confident."),
("jumped", "Magnitude - amplifier", "H", "Forceful motion verb."),
("accelerated", "Magnitude - amplifier", "H", "Asserts the pace itself is rising - emphatic."),
("acceleration", "Magnitude - amplifier", "H", "Asserts the pace itself is rising - emphatic."),
("renewed acceleration", "Magnitude - amplifier", "H", "Emphatic - a trend reasserting itself."),
("intensified", "Magnitude - amplifier", "H", "Asserts something is getting stronger."),
("record", "Magnitude - amplifier", "H", "'record high / record level' - maximal, emphatic."),
("record high", "Magnitude - amplifier", "H", "Maximal, emphatic."),
("notable", "Magnitude - amplifier", "H", "Flags the move as worth attention - confident."),
("notably", "Magnitude - amplifier", "H", "Emphasis adverb."),

# ============================================================ MAGNITUDE - DAMPENERS  (soft)
("slight", "Magnitude - dampener", "D", "Minimises the move - 'nothing much happened'."),
("slightly", "Magnitude - dampener", "D", "Minimises the move."),
("slight increase", "Magnitude - dampener", "D", "Downplayed rise."),
("slight decline", "Magnitude - dampener", "D", "Downplayed fall."),
("increased slightly", "Magnitude - dampener", "D", "Downplayed rise."),
("declined slightly", "Magnitude - dampener", "D", "Downplayed fall."),
("moderate", "Magnitude - dampener", "D", "Tempering word - 'not extreme'."),
("moderately", "Magnitude - dampener", "D", "Tempering adverb."),
("moderate pace", "Magnitude - dampener", "D", "'at a moderate pace' - tempered speed."),
("at a moderate pace", "Magnitude - dampener", "D", "Tempered speed framing."),
("relatively moderate", "Magnitude - dampener", "D", "Double-hedged - tempered and comparative."),
("somewhat", "Magnitude - dampener", "D", "Vague partial quantifier."),
("relatively", "Magnitude - dampener", "D", "Comparative hedge - avoids an absolute claim."),
("limited", "Magnitude - dampener", "D", "Caps the size of the move."),
("gradual", "Magnitude - dampener", "D", "Stresses slowness / smallness of steps."),
("gradually", "Magnitude - dampener", "D", "Stresses slowness."),
("partial", "Magnitude - dampener", "D", "Claims the move is incomplete."),
("partially", "Magnitude - dampener", "D", "Claims the move is incomplete."),
("some increase", "Magnitude - dampener", "D", "Vague, non-committal quantity."),

# ============================================================ FIRMNESS / PERSISTENCE  (strong)
("remains tight", "Firmness / persistence", "H", "Flat present-tense assertion of an ongoing state."),
("remains strong", "Firmness / persistence", "H", "Flat assertion of an ongoing state."),
("remains high", "Firmness / persistence", "H", "Flat assertion of an ongoing state."),
("remains elevated", "Firmness / persistence", "H", "Flat assertion of an ongoing state."),
("remained high", "Firmness / persistence", "H", "Flat assertion of an ongoing state."),
("remains very low", "Firmness / persistence", "H", "Flat, emphatic assertion of an ongoing state."),
("persistent", "Firmness / persistence", "H", "Asserts the condition will not go away."),
("persists", "Firmness / persistence", "H", "Asserts the condition will not go away."),
("persist", "Firmness / persistence", "H", "Asserts the condition will not go away."),
("entrenched", "Firmness / persistence", "H", "Asserts a condition is dug in - strong."),
("sticky", "Firmness / persistence", "H", "Asserts inflation is resisting decline - strong."),
("prolonged", "Firmness / persistence", "H", "Asserts a long, definite duration."),
("continued to increase", "Firmness / persistence", "H", "Asserts an established, still-running trend."),
("continued to decline", "Firmness / persistence", "H", "Asserts an established, still-running trend."),
("continued to rise", "Firmness / persistence", "H", "Asserts an established, still-running trend."),
("rapid upward trend", "Firmness / persistence", "H", "Emphatic + persistent."),

# ============================================================ ASSERTION / COMMITMENT  (strong)
("will", "Assertion / commitment", "H", "Categorical future - a promise, not a possibility."),
("must", "Assertion / commitment", "H", "Categorical necessity."),
("determined", "Assertion / commitment", "H", "'the Committee is determined to' - commitment language."),
("emphasized", "Assertion / commitment", "H", "The Bank foregrounds a point deliberately."),
("emphasizes", "Assertion / commitment", "H", "The Bank foregrounds a point deliberately."),
("stressed", "Assertion / commitment", "H", "The Bank foregrounds a point deliberately."),
("as necessary", "Assertion / commitment", "H", "'will act as necessary' - commitment to act."),
("required", "Assertion / commitment", "H", "Necessity framing."),

# ============================================================ EMPHASIS MARKERS  (strong)
("in particular", "Emphasis marker", "H", "Singles a point out for weight."),
("particularly", "Emphasis marker", "H", "Adds weight to the attached claim."),
("especially", "Emphasis marker", "H", "Adds weight to the attached claim."),

# ============================================================ LEVEL / STATE ADJECTIVES  (emphatic flat assertion)
("high", "Level / state", "H", "Bare, unqualified level word - a flat assertion."),
("higher", "Level / state", "H", "Comparative level word, stated flatly."),
("very high", "Level / state", "H", "Intensified flat assertion."),
("very low", "Level / state", "H", "Intensified flat assertion."),
("elevated", "Level / state", "H", "Flat assertion that a level is above normal."),
("tight", "Level / state", "H", "Flat assertion (labour market) - definite."),
("very tight", "Level / state", "H", "Intensified flat assertion."),
("full employment", "Level / state", "H", "Absolute-state phrase - no hedge."),
("excess demand", "Level / state", "H", "Absolute-state phrase - definite."),
("shortage", "Level / state", "H", "Absolute-state word - definite."),

# ============================================================ HEDGES / QUALIFIERS  (soft)
("expected to", "Hedge / qualifier", "D", "Forecast framing - a projection, not a fact."),
("is expected to", "Hedge / qualifier", "D", "Forecast framing."),
("are expected to", "Hedge / qualifier", "D", "Forecast framing."),
("projected", "Hedge / qualifier", "D", "Forecast framing."),
("projected to", "Hedge / qualifier", "D", "Forecast framing."),
("assessed", "Hedge / qualifier", "D", "'it is assessed that' - attributes the claim to judgement, not fact."),
("estimated", "Hedge / qualifier", "D", "Attributes the claim to an estimate."),
("estimate", "Hedge / qualifier", "D", "Attributes the claim to an estimate."),
("forecast", "Hedge / qualifier", "D", "Attributes the claim to a forecast."),
("broadly", "Hedge / qualifier", "D", "Approximating hedge."),
("largely", "Hedge / qualifier", "D", "Approximating hedge - 'mostly but not wholly'."),
("generally", "Hedge / qualifier", "D", "Approximating hedge."),

# ============================================================ TENTATIVENESS - MODALS  (soft)
("may", "Tentativeness - modal", "D", "Possibility, not commitment."),
("could", "Tentativeness - modal", "D", "Possibility, not commitment."),
("possible", "Tentativeness - modal", "D", "Names something as merely possible."),
("possibly", "Tentativeness - modal", "D", "Names something as merely possible."),
("it is possible that", "Tentativeness - modal", "D", "Explicit possibility framing."),
("may lead", "Tentativeness - modal", "D", "Possible consequence, not a stated one."),
("appears", "Tentativeness - modal", "D", "Evidential hedge - 'looks like' not 'is'."),
("appear", "Tentativeness - modal", "D", "Evidential hedge."),
("seems", "Tentativeness - modal", "D", "Evidential hedge."),
("likely", "Tentativeness - modal", "D", "Probability word - stops short of a claim."),

# ============================================================ APPROXIMATION  (soft)
("around", "Approximation", "D", "'around X percent' - avoids a precise figure."),
("approximately", "Approximation", "D", "Explicitly imprecise."),
("close to", "Approximation", "D", "Avoids stating the level is reached."),
("in the range of", "Approximation", "D", "Gives a band, not a number."),
("about", "Approximation", "D", "Imprecise quantifier ('about X percent')."),

# ============================================================ UNCERTAINTY  (soft)
("uncertainty", "Uncertainty", "D", "Names the limits of what the Bank knows."),
("uncertain", "Uncertainty", "D", "Names the limits of what the Bank knows."),
("high level of uncertainty", "Uncertainty", "D", "Foregrounds how little is settled."),
("great amount of uncertainty", "Uncertainty", "D", "Foregrounds how little is settled."),
("significant uncertainty", "Uncertainty", "D", "Foregrounds how little is settled."),
("difficult to assess", "Uncertainty", "D", "Admits the Bank cannot judge."),
("volatility", "Uncertainty", "D", "Names instability - no firm direction."),
("volatile", "Uncertainty", "D", "Names instability - no firm direction."),
("mixed", "Uncertainty", "D", "'mixed trend' - refuses a single direction."),
("mixed trend", "Uncertainty", "D", "Refuses a single direction."),
("in opposite directions", "Uncertainty", "D", "Explicitly balanced - no tilt."),
("so far", "Uncertainty", "D", "Marks the claim as provisional."),
("thus far", "Uncertainty", "D", "Marks the claim as provisional."),
("at this stage", "Uncertainty", "D", "Marks the claim as provisional."),

# ============================================================ CAUTION / PATIENCE  (soft - wait-and-see)
("cautious", "Caution / patience", "D", "Wait-and-see framing - avoids commitment."),
("gradual and cautious", "Caution / patience", "D", "Doubly hedged path language."),
("monitor", "Caution / patience", "D", "'will monitor' - defers judgement."),
("closely monitor", "Caution / patience", "D", "Defers judgement."),
("closely", "Caution / patience", "D", "'watching closely' - defers judgement."),

# ============================================================ NEUTRAL  (present in the corpus, deliberately NOT scored)
("increase", "Neutral (not scored)", "N", "Plain factual verb - the signal is in the modifier, not here."),
("increased", "Neutral (not scored)", "N", "Plain factual verb."),
("rose", "Neutral (not scored)", "N", "Plain factual verb."),
("decline", "Neutral (not scored)", "N", "Plain factual verb."),
("declined", "Neutral (not scored)", "N", "Plain factual verb."),
("decreased", "Neutral (not scored)", "N", "Plain factual verb."),
("fell", "Neutral (not scored)", "N", "Plain factual verb."),
("grew", "Neutral (not scored)", "N", "Plain factual verb."),
("expanded", "Neutral (not scored)", "N", "Plain factual verb."),
("contracted", "Neutral (not scored)", "N", "Plain factual verb."),
("moderated", "Neutral (not scored)", "N", "Plain factual verb (pace fell) - no rhetorical charge alone."),
("stable", "Neutral (not scored)", "N", "States that nothing moved - neither emphatic nor hedged."),
("unchanged", "Neutral (not scored)", "N", "States that nothing moved."),
("remained stable", "Neutral (not scored)", "N", "States that nothing moved."),
("remains", "Neutral (not scored)", "N", "Too frequent / structural to carry signal on its own."),
("remained", "Neutral (not scored)", "N", "Too frequent / structural."),
("continued", "Neutral (not scored)", "N", "Too frequent / structural."),
("continues", "Neutral (not scored)", "N", "Too frequent / structural."),
("low", "Neutral (not scored)", "N", "Bare level word - scored only when intensified ('very low')."),
("expected", "Neutral (not scored)", "N", "Scored only in the phrase 'expected to' (forecast framing)."),
]
