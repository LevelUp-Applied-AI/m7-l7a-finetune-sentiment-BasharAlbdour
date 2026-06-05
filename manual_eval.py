"""
Stretch Tuesday — Manual Evaluation Harness.

Implement these without using Trainer.predict, sklearn metrics helpers, or
Hugging Face evaluate. The goal is to make the math explicit.
"""

import numpy as np
import torch


def manual_predict(model, tokenizer, texts: list, batch_size: int = 8):
    """
    Run manual PyTorch inference over a list of texts.

    Returns (preds, probs):
      preds: shape (N,), int class indices
      probs: shape (N, num_classes), probabilities (post-softmax)
    """
    # TODO: iterate texts in batches
    # TODO: tokenize each batch with truncation, max_length=128, padding=True, return_tensors='pt'
    # TODO: forward pass under torch.no_grad()
    # TODO: softmax over the last dim
    # TODO: argmax to get class indices
    # TODO: collect into numpy arrays of shape (N,) and (N, num_classes); return both
    model.eval()
    all_prob=[]
    all_pred=[]
    for i in range(0,len(texts),batch_size):
      batch_texts=texts[i:i+batch_size]
      inputs=tokenizer(
        batch_texts,
        truncation=True,
        max_length=128,
        padding=True,
        return_tensors="pt"
      )
      with torch.no_grad():
        outputs=model(**inputs)
      probs=torch.softmax(outputs.logits,dim=-1).numpy()
      preds=np.argmax(probs,axis=1)
      all_pred.append(preds)
      all_prob.append(probs)
    return np.concatenate(all_pred), np.concatenate(all_prob)
    raise NotImplementedError


def compute_classification_report_from_arrays(y_true, y_pred) -> dict:
    """
    Compute accuracy, per-class precision/recall/F1, and macro-F1 from numpy
    primitives only — no sklearn, no Hugging Face evaluate.

    Returns:
      {
        "accuracy": float,
        "macro_f1": float,
        "per_class": {label_index: {"precision": ..., "recall": ..., "f1": ...}, ...},
      }
    """
    # TODO: compute true positives / false positives / false negatives per class
    # TODO: precision = TP / (TP + FP); guard divide-by-zero
    # TODO: recall = TP / (TP + FN)
    # TODO: f1 = 2 * P * R / (P + R)
    # TODO: accuracy = sum(y_pred == y_true) / N
    # TODO: macro-F1 = mean of per-class f1 scores
    # TODO: assemble and return the dict
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    classes = np.unique(y_true)
    
    per_class = {}
    f1_scores = []
    
    for c in classes:
        tp = np.sum((y_pred == c) & (y_true == c))
        fp = np.sum((y_pred == c) & (y_true != c))
        fn = np.sum((y_pred != c) & (y_true == c))
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        per_class[int(c)] = {
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
        }
        f1_scores.append(f1)
    
    accuracy = float(np.sum(y_pred == y_true) / len(y_true))
    macro_f1 = float(np.mean(f1_scores))
    
    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "per_class": per_class,
    }
    raise NotImplementedError
