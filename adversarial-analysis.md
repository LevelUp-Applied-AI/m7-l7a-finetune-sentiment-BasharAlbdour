# Adversarial Evaluation Analysis

> **TODO** — fill each section after running `run_adversarial.py` against your fine-tuned model.

## Per-hypothesis accuracy

| Hypothesis category | Correct | Total | Accuracy |
|---|---|---|---|
| negation | 1 | 5 | 20% |
| lexical_trigger | 3 | 6 | 50% |
| domain_shift | 4 | 6 | 67% |
| length_extreme | 3 | 5 | 60% |
| sarcasm | 0 | 5 | 0% |
| other | 1 | 6 | 17% |

Overall accuracy: 12/33 = 36%

## Confirmed hypotheses

Which categories did the model fail on as you predicted? Cite specific row IDs and predictions.

The results confirmed most of what the integration task had already suggested, which made the adversarial set feel less like a surprise and more like a controlled replication of earlier observations.

**Sarcasm (0/5)** was the most striking failure. Every single sarcastic example was predicted positive with high confidence — rows 18 through 22 all landed between 0.84 and 0.90. The model read the opening word ("Amazing", "Great", "Nice", "Love", "Fantastic") and committed to positive before processing the rest of the sentence. Row 22 ("Fantastic, another update that fixes nothing I reported") is the clearest case: 0.8959 positive despite an unambiguous complaint. This was expected — the training data contains no sarcasm signal, so the model has no mechanism to detect polarity reversal.

**Negation (1/5)** confirmed the hypothesis that the model ignores negation structure and latches onto cue words. Row 9 ("I wouldn't call the new sync system reliable yet") predicted neutral at 0.7364 instead of negative — the word "reliable" pulled it away from the correct label. Row 12 ("I can't really say the redesign helped productivity") also predicted neutral, suggesting the model focused on "helped productivity" and discarded the negation entirely. Row 11 ("The backup feature never actually failed during testing") predicted neutral instead of positive — the word "failed" dominated even though the sentence means the opposite. The only correct negation prediction was row 1 ("did not improve battery life"), likely because "did not improve" combined with "battery life" is a pattern that appeared frequently enough in app reviews to be learned directly.

**Other (1/6)** confirmed that formal, third-person, and indirect language confuses the model. Row 29 ("Whoever redesigned the onboarding flow clearly spent time thinking about new users") was predicted negative at 0.6209 — a result that is difficult to explain except that the indirect phrasing and absence of direct product praise left the model without a clear signal. Row 31 ("One could argue that the interface introduces unnecessary complexity") was predicted neutral instead of negative — the hedged formal tone diluted what is clearly a criticism.

**Lexical triggers (3/6)** partially confirmed the hypothesis. Rows 4 and 5 showed the model ignoring conflict wording ("cat-and-mouse", "fighting the app") and predicting neutral — the opposite of what the integration task observed for news-style conflict language. Row 8 ("trench warfare") also predicted neutral despite the aggressive metaphor. This suggests the conflict-language effect from the integration task was stronger in news prose than in app-review framing, which is an interesting nuance.


## Refuted hypotheses

Which categories did the model handle better than you expected?

Two categories performed better than expected based on the integration task observations.

**Domain shift (4/6)** was the biggest surprise. In the integration task, the model struggled significantly with out-of-domain text — mean confidence was 0.577 and most predictions were uncertain. Here, rows 13, 14, 15, and 16 were all handled reasonably well. Row 15 ("The coach praised the rookie for staying calm under pressure") predicted positive at 0.7127, which is correct — in the integration task, NEWS_0135 (praise directed at a person) produced maximum uncertainty at 0.362. The adversarial version of the same hypothesis produced a confident correct prediction. The difference is likely that the adversarial sentence is shorter and more direct than the news article excerpt, which contained more complex framing. Row 14 ("Analysts called the rollout cautious but stable") predicted neutral at 0.8262 — also correct, and surprisingly confident for formal business language.

**Length extreme (3/5)** also held up better than expected. The two long sentences (rows 26 and 27) were both predicted correctly, suggesting that truncation to 128 tokens does not systematically destroy sentiment signal when the most important cues appear early. Row 26 is a long negative-leaning review that was labeled neutral — the model predicted neutral at 0.5683, which is technically correct but barely above chance. Row 27, a long formal sentence with mixed signals, was predicted neutral at 0.7079 — a reasonable and correct prediction.

## What the results reveal about the decision boundary

Articulate one or more specific things the adversarial results say about how the model decides.

The adversarial results, taken together with the integration task findings, point to a model that makes decisions based almost entirely on the presence of high-signal cue words in the first portion of the input, with very little sensitivity to the surrounding structure. The sarcasm results make this clearest: a single positive word at the start of a sentence ("Fantastic", "Amazing") is enough to produce a confident positive prediction regardless of what follows. The negation results confirm the same pattern from the other direction — "reliable", "helped productivity", and "failed" each pulled the prediction toward their literal polarity even when negated. The model appears to have learned a bag-of-words-style mapping from emotionally loaded terms to sentiment classes, rather than learning to compose meaning across a sentence. This is consistent with what the integration task revealed about high-confidence misfires on news articles: the model reacted to words like "attack" and "horrible" in isolation, without considering whether those words were describing a product experience or a geopolitical event. The decision boundary is essentially a weighted lexicon, not a syntactic or semantic reasoner, which explains why negation, sarcasm, and formal indirect criticism all fall outside what the model can handle reliably.
