import pandas as pd
from pathlib import Path

LABELS = ["safe", "scam", "prompt_injection"]
PROC = Path("data/processed")


def load_split(name):
    """Load train, val, test or hard as a DataFrame."""
    df = pd.read_csv(PROC / f"{name}.csv")
    df["text"] = df["text"].astype(str)
    return df