import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

PROC = Path("data/processed")
OWN = Path("data/own")
SEED = 42
COLS = ["text", "label", "language", "source"]


def norm(s):
    return " ".join(str(s).lower().split())


df = pd.read_csv(PROC / "combined.csv")
df["key"] = df["text"].map(norm)

# ---------- 1. Hard set ----------
hard_path = OWN / "hard_own.csv"
if hard_path.exists():
    hard = pd.read_csv(hard_path)
    hard["key"] = hard["text"].map(norm)
    hard["label"] = hard["label"].astype(str).str.strip().str.lower()
    hard["source"] = hard["source"].fillna("own_hard")
    hard = hard.drop_duplicates(subset="key")
    df = df[~df["key"].isin(hard["key"])]          # keep hard rows out of training data
    print(f"Hard set from {hard_path.name}: {len(hard)} rows")
else:
    own = df[df["source"] == "own"]
    _, hard = train_test_split(own, test_size=0.25, stratify=own["label"], random_state=SEED)
    df = df.drop(index=hard.index)
    print("No hard_own.csv found: using 25% of own rows as the hard set (weaker option).")

# ---------- 2. Train / validation / test (70 / 15 / 15) ----------
is_own = df["source"].astype(str).str.startswith("own")
own_df, pub_df = df[is_own], df[~is_own]

# public rows: normal stratified split
train, temp = train_test_split(pub_df, test_size=0.30, stratify=pub_df["label"], random_state=SEED)
val, test = train_test_split(temp, test_size=0.50, stratify=temp["label"], random_state=SEED)

# own rows: split per (label, language) group so each group appears in val and test
own_val, own_test, own_train = [], [], []
for _, g in own_df.groupby(["label", "language"]):
    g = g.sample(frac=1, random_state=SEED)
    k = max(1, round(0.15 * len(g))) if len(g) >= 3 else 0
    own_val.append(g.iloc[:k])
    own_test.append(g.iloc[k:2 * k])
    own_train.append(g.iloc[2 * k:])

train = pd.concat([train] + own_train)
val = pd.concat([val] + own_val)
test = pd.concat([test] + own_test)

# ---------- 3. Safety check: no overlap between sets ----------
sets = {"train": train, "val": val, "test": test, "hard": hard}
names = list(sets)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        overlap = set(sets[names[i]]["key"]) & set(sets[names[j]]["key"])
        assert not overlap, f"Overlap between {names[i]} and {names[j]}: {len(overlap)} texts"
print("Overlap check passed: no text appears in more than one set.\n")

# ---------- 4. Save ----------
for name, part in sets.items():
    part = part.sample(frac=1, random_state=SEED)
    part[COLS].to_csv(PROC / f"{name}.csv", index=False)

# ---------- 5. Report ----------
print(pd.DataFrame({k: v["label"].value_counts() for k, v in sets.items()}).fillna(0).astype(int))
print("\nTotals:", {k: len(v) for k, v in sets.items()})
print("\nOwn rows per set:", {k: int(v["source"].astype(str).str.startswith("own").sum()) for k, v in sets.items()})
print("\nLanguages per set:\n", pd.DataFrame({k: v["language"].value_counts() for k, v in sets.items()}).fillna(0).astype(int))