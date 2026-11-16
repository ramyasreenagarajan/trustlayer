import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

# From Day 1: which deepset label number means "injection"?
INJECTION_LABEL = 1


def clean_text(s):
    """Collapse tabs, newlines and repeated spaces into single spaces."""
    return " ".join(str(s).split())


# ---------- SMS Spam Collection ----------
sms = pd.read_csv(
    RAW / "SMSSpamCollection",
    sep="\t", header=None, names=["raw_label", "text"], quoting=3,
)
sms["text"] = sms["text"].map(clean_text)
sms["label"] = sms["raw_label"].map({"ham": "safe", "spam": "scam"})
sms["language"] = "english"
sms["source"] = "uci_sms_spam"
before = len(sms)
sms = sms[sms["text"].str.len() > 0].drop_duplicates(subset="text")
sms = sms[["text", "label", "language", "source"]]
sms.to_csv(OUT / "sms_clean.csv", index=False)
print(f"SMS: {before} rows -> {len(sms)} after removing empty rows and duplicates")
print(sms["label"].value_counts(), "\n")

# ---------- deepset prompt-injections ----------
parts = [
    pd.read_parquet(RAW / "deepset_train.parquet"),
    pd.read_parquet(RAW / "deepset_test.parquet"),
]
ds = pd.concat(parts, ignore_index=True)
ds["text"] = ds["text"].map(clean_text)
ds["label"] = ds["label"].map(
    lambda v: "prompt_injection" if v == INJECTION_LABEL else "safe"
)
ds["language"] = "english"  # check Part E: some rows may be another language
ds["source"] = "deepset_prompt_injections"
before = len(ds)
ds = ds[ds["text"].str.len() > 0].drop_duplicates(subset="text")
ds = ds[["text", "label", "language", "source"]]
ds.to_csv(OUT / "deepset_clean.csv", index=False)
print(f"deepset: {before} rows -> {len(ds)} after removing empty rows and duplicates")
print(ds["label"].value_counts())