# Calibration Analysis

> **TODO** — fill each section after running your manual evaluation and reliability diagram.

## Reliability diagram interpretation

What does your saved diagram (`figures/reliability-diagram.png`) look like? Where is the model over-confident vs. under-confident? Cite specific bucket values.

Looking at the diagram, the model behaves pretty differently depending on how confident it is. In the middle confidence range — roughly 0.55 to 0.75 — the bars consistently fall below the diagonal, which means the model is over-confident there. The clearest example is the 0.65 bucket: the model was right only 47.8% of the time, but it was assigning confidence scores around 0.65. That's a gap of about 0.17, which is significant. The 0.75 bucket is similar — accuracy of 0.590 against confidence of 0.75, a gap of 0.16.
 
The 0.55 bucket is actually the most honest — accuracy of 0.532 sits almost exactly on the diagonal. At the high end, the model flips to slight under-confidence: the 0.85 bucket shows accuracy of 0.732 against confidence of 0.85 (gap of 0.12), and the 0.95 bucket shows accuracy of 0.861 against confidence of 0.95 (gap of 0.09). These gaps are smaller than in the mid-range, and the model is at least being conservative rather than over-confident at high confidence levels.

## Expected Calibration Error

Report your ECE. Interpret what it says about model trustworthiness for production use.

**ECE = 0.1065**
 
An ECE of about 0.11 means the model's confidence is off by around 11 percentage points on average. In practice this means you can't take the probability outputs at face value — when the model says 65% confident, it's actually only right about 48% of the time in that range. For anything where the probability matters (setting confidence thresholds, flagging uncertain predictions for human review, risk scoring), this model needs calibration work before going into production.

## A specific calibration pattern

Identify one specific pattern (over-confidence on majority class, under-confidence near boundaries, etc.) and reason about why it arose given how the model was trained.

The over-confidence is concentrated in the 0.55–0.75 range, which also happens to be where most predictions land (247 and 273 samples in those two buckets). This isn't a coincidence — this is where neutral class predictions pile up. Neutral is the hardest class by far (F1=0.499), and the model often confuses it with negative or positive. So what's happening is the model learned strong, clear signal for obviously positive or negative reviews, but when it encounters something ambiguous it still commits to a moderately high confidence score rather than hedging. The result is a cluster of over-confident wrong predictions right in the middle of the diagram

## A proposed engineering action

What would you change in production based on these findings? (Threshold-based abstention, temperature scaling, bucket-specific data collection, etc.)

The most practical fix here is temperature scaling. It's a post-hoc calibration method that divides the logits by a single scalar T before the softmax — no retraining needed, just one parameter fit on a small validation set by minimizing log-loss. Setting T > 1 softens the probability distribution, which directly pulls those over-confident mid-range predictions back toward the diagonal. It's cheap, reversible, and easy to deploy. After applying it I'd re-run the ECE calculation — for a model like this, a well-tuned temperature typically brings ECE down to around 0.03–0.05
