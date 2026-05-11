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
 
**Example 1 — Negative misclassified as Neutral**
 
- Text: `i m fed of this <url> has posted it add every where`
- Gold label: negative
- Predicted label: neutral
- Gold-class probability: 0.2565
The review expresses frustration ("fed of this") but the truncated phrasing and URL placeholder likely obscured the sentiment signal. Without clear negative keywords like "terrible" or "broken", the model defaulted to neutral.
 
**Example 2 — Neutral misclassified as Positive**
 
- Text: `nice app to use with friends`
- Gold label: neutral
- Predicted label: positive
- Gold-class probability: 0.0997
This is a genuinely ambiguous case. The word "nice" strongly pulls toward positive, and the model assigned it confidently (gold probability only 0.10). A human annotator likely rated it neutral because it lacks enthusiasm, but the surface-level language reads as positive — a reasonable model failure.
 
**Example 3 — Positive misclassified as Neutral**
 
- Text: `good, but slow workflow.`
- Gold label: positive
- Predicted label: neutral
- Gold-class probability: 0.3196
The conjunction "but" followed by a complaint ("slow workflow") created mixed sentiment that confused the model. Despite the overall positive rating, the criticism dominated the model's prediction. This highlights a known weakness of single-label classifiers on mixed-sentiment text.
 
## Hugging Face Hub Model URL
 
https://huggingface.co/Balbdour/m7-app-review-sentiment