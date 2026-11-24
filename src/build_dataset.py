import pandas as pd
from pathlib import Path

PROC = Path("data/processed")
OWN = Path("data/own")
SMS_SAFE_CAP = 600      # how many SMS 'safe' rows to keep
SEED = 42
COLS = ["text", "label", "language", "source"]
ALLOWED = {"safe", "scam", "prompt_injection"}


def norm(s):
    """Lower-case, single-spaced version of a text, used only to spot duplicates."""
    return " ".join(str(s).lower().split())


# ---------- 1. Load ----------
own_files = sorted(OWN.glob("*_own.csv"))
print("Own files found:", [p.name for p in own_files])

def load_own(p):
    d = pd.read_csv(p)
    d["source"] = d["source"].fillna("own_hard" if p.name == "hard_own.csv" else "own")
    return d

own = pd.concat([load_own(p) for p in own_files], ignore_index=True)

sms = pd.read_csv(PROC / "sms_audited.csv")
ds = pd.read_csv(PROC / "deepset_audited.csv")
for _d in (sms, ds):
    _d["language"] = _d["language"].where(_d["language"].isin({"english", "german"}), "other_or_unknown")
# ---------- 2. Downsample SMS 'safe' ----------
sms_safe = sms[sms["label"] == "safe"]
sms_safe = sms_safe.sample(n=min(SMS_SAFE_CAP, len(sms_safe)), random_state=SEED)
sms = pd.concat([sms_safe, sms[sms["label"] == "scam"]])

# ---------- 3. Combine (own first, so own rows win when a duplicate exists) ----------
df = pd.concat([own, ds, sms], ignore_index=True)[COLS]

# ---------- 4. Clean ----------
df["text"] = df["text"].astype(str).map(lambda s: " ".join(s.split()))
df["label"] = df["label"].astype(str).str.strip().str.lower()

bad = df[~df["label"].isin(ALLOWED)]
if len(bad):
    print(f"\nWARNING: {len(bad)} rows have an unknown label and will be dropped:")
    print(bad[["text", "label", "source"]].head(10).to_string(max_colwidth=60))
    df = df[df["label"].isin(ALLOWED)]

missing_lang = df["language"].isna().sum()
if missing_lang:
    print(f"\nNote: {missing_lang} rows have no language; setting them to 'unknown'.")
    df["language"] = df["language"].fillna("unknown")

df = df[df["text"].str.len() >= 5]
df["key"] = df["text"].map(norm)

# conflicting labels for the same text
conf = df.groupby("key")["label"].nunique()
conf_keys = conf[conf > 1].index
if len(conf_keys):
    print(f"\nWARNING: {len(conf_keys)} texts appear with different labels and will be dropped:")
    print(df[df["key"].isin(conf_keys)][["text", "label", "source"]].head(10).to_string(max_colwidth=60))
    df = df[~df["key"].isin(conf_keys)]

before = len(df)
df = df.drop_duplicates(subset="key", keep="first").drop(columns="key")
print(f"\nDuplicates removed: {before - len(df)}")

# ---------- 5. Shuffle and save ----------
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
df.to_csv(PROC / "combined.csv", index=False)

# ---------- 6. Report ----------
print(f"\nFinal rows: {len(df)}")
print("\nBy label:\n", df["label"].value_counts())
print("\nBy source:\n", df["source"].value_counts())
print("\nLabel x language:\n", pd.crosstab(df["label"], df["language"]))
print("\nLabel x source:\n", pd.crosstab(df["label"], df["source"]))
print("\nAverage length in characters, by label:")
print(df.groupby("label")["text"].apply(lambda s: round(s.str.len().mean())))