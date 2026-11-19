import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline, make_union
from sklearn.metrics import f1_score, accuracy_score, recall_score

from common import load_split, LABELS, report, PROC

# ----- EDIT THESE THREE LINES to match your Day 3 choice -----
ALGO = "svm"        # "lr" or "svm"
KIND = "word+char"  # "word", "char" or "word+char"
C = 0.3
# --------------------------------------------------------------


def word_vec():
    return TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)


def char_vec():
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)


def make_model():
    feats = word_vec() if KIND == "word" else char_vec() if KIND == "char" else make_union(word_vec(), char_vec())
    if ALGO == "lr":
        clf = LogisticRegression(C=C, max_iter=2000, class_weight="balanced")
    else:
        clf = LinearSVC(C=C, class_weight="balanced")
    return make_pipeline(feats, clf)


def macro_f1(y_true, y_pred):
    return f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)


def bootstrap_ci(y_true, y_pred, n=1000, seed=0):
    rng = np.random.default_rng(seed)
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    scores = []
    for _ in range(n):
        idx = rng.integers(0, len(y_true), len(y_true))
        scores.append(macro_f1(y_true[idx], y_pred[idx]))
    return np.percentile(scores, [2.5, 97.5])


def group_table(df, col):
    rows = []
    for g, d in df.groupby(col):
        rec = recall_score(d["label"], d["pred"], labels=LABELS, average=None, zero_division=0)
        present = set(d["label"])
        row = {col: g, "n": len(d), "accuracy": round(accuracy_score(d["label"], d["pred"]), 3)}
        for lab, r in zip(LABELS, rec):
            row[f"rec_{lab}"] = round(r, 3) if lab in present else np.nan
        rows.append(row)
    return pd.DataFrame(rows).to_string(index=False)


train = load_split("train")
val = load_split("val")
test = load_split("test")
hard = load_split("hard")

model = make_model()
model.fit(train["text"], train["label"])
print(f"Model: {ALGO} | {KIND} | C={C}")
print(f"train rows: {len(train)} | test rows: {len(test)} | hard rows: {len(hard)}")

val_pred = model.predict(val["text"])
print("\nValidation macro F1 (for comparison):", round(macro_f1(val["label"], val_pred), 3))

test["pred"] = model.predict(test["text"])
hard["pred"] = model.predict(hard["text"])

# ---------- 1. Test set ----------
report("TEST set", test["label"], test["pred"])
lo, hi = bootstrap_ci(test["label"], test["pred"])
print(f"Macro F1 95% range (bootstrap): {lo:.3f} to {hi:.3f}")

# ---------- 2. Hard set ----------
report("HARD set", hard["label"], hard["pred"])
lo, hi = bootstrap_ci(hard["label"], hard["pred"])
print(f"Macro F1 95% range (bootstrap): {lo:.3f} to {hi:.3f}  (n={len(hard)}: treat with caution)")

# ---------- 3. Own rows only (test + hard) ----------
both = pd.concat([test, hard], ignore_index=True)
own = both[both["source"].astype(str).str.startswith("own")]
print(f"\n===== OWN rows only (test + hard), n={len(own)} =====")
print("Macro F1:", round(macro_f1(own["label"], own["pred"]), 3))
lo, hi = bootstrap_ci(own["label"], own["pred"])
print(f"95% range: {lo:.3f} to {hi:.3f}")

# ---------- 4. Breakdowns ----------
print("\n===== TEST set by source =====")
print(group_table(test, "source"))
print("\n===== TEST + HARD by language =====")
print(group_table(both, "language"))
print("\n===== TEST + HARD by true label (accuracy = recall of that label) =====")
print(group_table(both, "label"))

# ---------- 5. Save the mistakes for Day 5 (these files stay on your computer) ----------
for name, d in [("test", test), ("hard", hard)]:
    err = d[d["label"] != d["pred"]]
    err.to_csv(PROC / f"errors_{name}.csv", index=False)
    print(f"Saved {len(err)} mistakes to data/processed/errors_{name}.csv")