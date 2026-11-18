import pandas as pd
from pathlib import Path

LABELS = ["safe", "scam", "prompt_injection"]
PROC = Path("data/processed")


def load_split(name):
    """Load train, val, test or hard as a DataFrame."""
    df = pd.read_csv(PROC / f"{name}.csv")
    df["text"] = df["text"].astype(str)
    return df
from sklearn.metrics import classification_report, confusion_matrix, f1_score


def report(name, y_true, y_pred):
    print(f"\n===== {name} =====")
    print("Macro F1:", round(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0), 3))
    print(classification_report(y_true, y_pred, labels=LABELS, digits=3, zero_division=0))
    cm = confusion_matrix(y_true, y_pred, labels=LABELS)
    print("Confusion matrix (rows = true, columns = predicted):")
    print("                  ", "  ".join(f"{l[:8]:>8}" for l in LABELS))
    for lab, row in zip(LABELS, cm):
        print(f"{lab:>18}", "  ".join(f"{v:>8}" for v in row))