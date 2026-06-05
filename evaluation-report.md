# Module 7 Week A — Lab Evaluation Report
 
## Dataset
 
The AARSynth app reviews dataset contains 7,472 reviews across 9 apps with 3 sentiment classes: negative (0), neutral (1), and positive (2). The dataset was split 80/20 into 5,977 training examples and 1,495 test examples using seed=42.
 
## Model and Hyperparameters
 
- Backbone: `distilbert-base-uncased`
- Number of labels: 3
- Learning rate: 5e-5
- Epochs: 2
- Batch size: 8
- Max length: 128
- Seed: 42
- Training time: ~31 minutes (CPU, Windows, no GPU)
## Metrics on the Test Split
 
Aggregate:
 
| Metric | Value |
|---|---|
| Accuracy | 0.6428 |
| Macro-F1 | 0.6412 |
 
Per class:
 
| Class | F1 | Precision | Recall |
|---|---|---|---|
| Negative | 0.7101 | 0.7211 | 0.6994 |
| Neutral | 0.4990 | 0.4755 | 0.5248 |
| Positive | 0.7144 | 0.7380 | 0.6923 |
 
## Confusion Matrix
 
|  | negative | neutral | positive |
|---|---|---|---|
| **negative** | 349 | 133 | 17 |
| **neutral** | 106 | 243 | 114 |
| **positive** | 29 | 135 | 369 |
 
## Three Qualitative Error Examples
 
**Example 1 — Neutral misclassified as Negative**
 
- Text: `used to be great. now lots of issues with network. i keep getting no network errors, as failed to update errors even when signal is great, or i'm connected to my wi-fi at home.`
- Gold label: neutral
- Predicted label: negative
- Gold-class probability: 0.1905
The review is factually reporting problems but was likely rated neutral by the annotator because it is descriptive rather than emotionally charged. However words like "errors", "failed", and "no network" are strong negative signal words that triggered the model's negative prediction. This is a classic cue-word trigger failure where surface-level vocabulary overrides the overall tone.
 
**Example 2 — Neutral misclassified as Positive**
 
- Text: `nice app to use with friends`
- Gold label: neutral
- Predicted label: positive
- Gold-class probability: 0.0997
This is a genuinely ambiguous case that is hard even for a human annotator. The word "nice" strongly pulls toward positive, and the model assigned it confidently (gold probability only 0.10). The annotator likely rated it neutral because it lacks enthusiasm or specifics, but the surface-level language reads as positive. This calibrates expectations for production use — the model will confidently misclassify short, mildly positive neutral reviews.
 
**Example 3 — Positive misclassified as Neutral**
 
- Text: `good, but slow workflow.`
- Gold label: positive
- Predicted label: neutral
- Gold-class probability: 0.3196
The conjunction "but" followed by a complaint ("slow workflow") created mixed sentiment that the model could not resolve. Despite the overall positive rating from the annotator, the criticism dominated the model's prediction. This highlights a known weakness of single-label classifiers on mixed-sentiment text — the model overweighted the negative phrase and missed the overall positive intent.

## Hugging Face Hub Model URL
 
https://huggingface.co/Balbdour/m7-app-review-sentiment