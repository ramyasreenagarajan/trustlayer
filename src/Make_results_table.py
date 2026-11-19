import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline, make_union
from sklearn.metrics import f1_score, recall_score
import pandas as pd

from common import load_split, LABELS
from baseline_rules import predict_one

# ----- EDIT THESE THREE LINES to match your Day 3 choice -----
ALGO = "svm"        # "lr" or "svm"
KIND = "word+char"  # "word", "char" or "word+char"
C = 0.3
# --------------------------------------------------------------
MODEL_NAME = f"TF-IDF ({KIND}) + {'Linear SVM' if ALGO == 'svm' else 'Logistic Regression'}, C={C}"


def word_vec():
    return TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)


def char_vec():
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)


def make_model():
    feats = word_vec() if KIND == "word" else char_vec() if KIND == "char" else make_union(word_vec(), char_vec())
    clf = LogisticRegression(C=C, max_iter=2000, class_weight="balanced") if ALGO == "lr" else LinearSVC(C=C, class_weight="balanced")
    return make_pipeline(feats, clf)


def macro_f1(y, p):
    return f1_score(y, p, labels=LABELS, average="macro", zero_division=0)


def ci(y, p, n=1000, seed=0):
    rng = np.random.default_rng(seed)
    y, p = np.array(y), np.array(p)
    s = [macro_f1(y[i], p[i]) for i in (rng.integers(0, len(y), len(y)) for _ in range(n))]
    return np.percentile(s, [2.5, 97.5])


train, val, test, hard = (load_split(n) for n in ["train", "val", "test", "hard"])
model = make_model()
model.fit(train["text"], train["label"])

for d in (val, test, hard):
    d["learned"] = model.predict(d["text"])
    d["rules"] = d["text"].map(predict_one)

both = pd.concat([test, hard], ignore_index=True)
own = both[both["source"].astype(str).str.startswith("own")]

sets = [("Validation", val), ("Test", test), ("Hard set", hard), ("Own rows (test + hard)", own)]


def recall_for(y, p, lab):
    return round(recall_score(y, p, labels=[lab], average=None, zero_division=0)[0], 2) if lab in set(y) else float("nan")


lines = ["| Model | Set | Rows | Macro F1 | 95% range | Recall scam | Recall injection |",
         "|---|---|---|---|---|---|---|"]
for mname, col in [("Keyword rules", "rules"), (MODEL_NAME, "learned")]:
    for sname, d in sets:
        y, p = d["label"], d[col]
        lo, hi = ci(y, p)
        lines.append(f"| {mname} | {sname} | {len(d)} | {macro_f1(y, p):.3f} | {lo:.2f} to {hi:.2f} | "
                     f"{recall_for(y, p, 'scam')} | {recall_for(y, p, 'prompt_injection')} |")

# per-language accuracy for the learned model (test + hard)
lang = ["", "| Language | Rows | Accuracy | Note |", "|---|---|---|---|"]
for g, d in both.groupby("language"):
    acc = (d["label"] == d["learned"]).mean()
    note = "too few rows to trust" if len(d) < 30 else ""
    lang.append(f"| {g} | {len(d)} | {acc:.2f} | {note} |")

out = "\n".join(lines + lang)
open("docs/results_table.md", "w", encoding="utf-8").write(out + "\n")
print(out)
print("\nSaved to docs/results_table.md")