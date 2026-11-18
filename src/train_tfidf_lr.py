from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score
import numpy as np

from common import load_split, LABELS, report

train = load_split("train")
val = load_split("val")
print(f"train rows: {len(train)} | val rows: {len(val)}")


def make_model(kind, C):
    if kind == "word":
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    else:
        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)
    clf = LogisticRegression(C=C, max_iter=2000, class_weight="balanced")
    return make_pipeline(vec, clf)


# ---------- 1. Try settings, judged on the validation set ----------
results = []
print("\nkind   C      macro F1 (val)")
for kind in ["word", "char"]:
    for C in [0.3, 1, 3, 10]:
        model = make_model(kind, C)
        model.fit(train["text"], train["label"])
        pred = model.predict(val["text"])
        f1 = f1_score(val["label"], pred, labels=LABELS, average="macro", zero_division=0)
        results.append((f1, kind, C))
        print(f"{kind:<6} {C:<6} {f1:.3f}")

best_f1, best_kind, best_C = max(results)
print(f"\nBest on validation: {best_kind}, C={best_C}, macro F1={best_f1:.3f}")

# ---------- 2. Full report for the best setting ----------
model = make_model(best_kind, best_C)
model.fit(train["text"], train["label"])
pred = model.predict(val["text"])
report(f"TF-IDF ({best_kind}) + Logistic Regression, C={best_C} (val)", val["label"], pred)

# ---------- 3. Which words push toward each label? ----------
vec = model.named_steps["tfidfvectorizer"]
clf = model.named_steps["logisticregression"]
names = np.array(vec.get_feature_names_out())
print("\nTop 12 features per label (higher weight = stronger signal):")
for i, label in enumerate(clf.classes_):
    top = np.argsort(clf.coef_[i])[::-1][:12]
    print(f"\n{label}:")
    print("  " + " | ".join(names[top]))