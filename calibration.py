"""
Stretch Tuesday — Calibration Analysis.

Reliability diagram + Expected Calibration Error (ECE).
"""

import numpy as np


def reliability_diagram(probs: np.ndarray, y_true: np.ndarray, n_bins: int = 10):
    """
    Bin predictions by max predicted probability; compute empirical accuracy per bin.

    Returns (bucket_centers, bucket_accuracies, bucket_counts), all length n_bins.
    """
    # TODO: bin edges via np.linspace(0, 1, n_bins + 1)
    # TODO: bucket_centers = midpoints of edges
    # TODO: for each prediction, take the max probability and the predicted class index
    # TODO: assign each prediction to a bucket by its max probability
    # TODO: bucket_accuracy = mean of (predicted == true) within the bucket; nan or 0 if empty
    # TODO: bucket_count = number of predictions in the bucket
    # TODO: return three numpy arrays
    edges = np.linspace(0, 1, n_bins + 1)
    centers = (edges[:-1] + edges[1:]) / 2

    max_probs = probs.max(axis=1)
    preds = probs.argmax(axis=1)
    correct = (preds == y_true).astype(float)

    bucket_accuracies = np.zeros(n_bins)
    bucket_counts = np.zeros(n_bins, dtype=int)

    for i in range(n_bins):
        if i < n_bins - 1:
            mask = (max_probs >= edges[i]) & (max_probs < edges[i + 1])
        else:
            mask = (max_probs >= edges[i]) & (max_probs <= edges[i + 1])
        bucket_counts[i] = mask.sum()
        bucket_accuracies[i] = correct[mask].mean() if bucket_counts[i] > 0 else 0.0

    return centers, bucket_accuracies, bucket_counts
    raise NotImplementedError


def expected_calibration_error(probs: np.ndarray, y_true: np.ndarray, n_bins: int = 10) -> float:
    """
    ECE = sum over bins of (bucket_count / N) * |bucket_accuracy - bucket_confidence|.

    A perfectly calibrated model has ECE = 0.
    """
    # TODO: bucket predictions as in reliability_diagram
    # TODO: for each bucket, compute confidence (mean max probability) and accuracy
    # TODO: weight |accuracy - confidence| by bucket fraction; sum
    # TODO: return float
    edges = np.linspace(0, 1, n_bins + 1)
    max_probs = probs.max(axis=1)
    preds = probs.argmax(axis=1)
    correct = (preds == y_true).astype(float)
    N = len(y_true)

    ece = 0.0
    for i in range(n_bins):
        if i < n_bins - 1:
            mask = (max_probs >= edges[i]) & (max_probs < edges[i + 1])
        else:
            mask = (max_probs >= edges[i]) & (max_probs <= edges[i + 1])
        count = mask.sum()
        if count > 0:
            acc = correct[mask].mean()
            conf = max_probs[mask].mean()
            ece += (count / N) * abs(acc - conf)

    return float(ece)
    raise NotImplementedError


def plot_reliability(centers: np.ndarray, accs: np.ndarray, counts: np.ndarray, output_path: str) -> None:
    """Save a reliability diagram. Provided helper — do not modify."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 5))
    width = 1.0 / max(len(centers), 1)
    ax.bar(centers, accs, width=width * 0.9, edgecolor="black", alpha=0.8, label="Empirical accuracy")
    ax.plot([0, 1], [0, 1], "--", color="grey", label="Perfect calibration")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Predicted probability (bucket center)")
    ax.set_ylabel("Empirical accuracy")
    ax.set_title("Reliability diagram")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    import json
    import os

    import pandas as pd
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    from manual_eval import compute_classification_report_from_arrays, manual_predict

    model = AutoModelForSequenceClassification.from_pretrained("model")
    tokenizer = AutoTokenizer.from_pretrained("model")

    df = pd.read_csv("predictions.csv")
    texts = df["text"].tolist()
    label_map = {"negative": 0, "neutral": 1, "positive": 2}
    y_true = df["label"].map(label_map).values

    preds, probs = manual_predict(model, tokenizer, texts)

    report = compute_classification_report_from_arrays(y_true, preds)
    print("\nManual classification report:")
    print(json.dumps(report, indent=2))

    centers, accs, counts = reliability_diagram(probs, y_true)
    ece = expected_calibration_error(probs, y_true)

    os.makedirs("figures", exist_ok=True)
    plot_reliability(centers, accs, counts, "figures/reliability-diagram.png")

    print(f"\nECE: {round(ece, 4)}")
    for c, a, n in zip(centers, accs, counts):
        if n > 0:
            print(f"  bin {c:.2f}: acc={a:.3f}, count={n}")