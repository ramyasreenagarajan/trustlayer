import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline, make_union
from sklearn.metrics import f1_score, recall_score, precision_score

from common import load_split, LABELS, report
from baseline_rules import predict_one

train = load_split("train")
val = load_split("val")
print(f"train rows: {len(train)} | val rows: {len(val)}\n")


def word_vec():
    return TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)


def char_vec():
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)


def features(kind):
    if kind == "word":
        return word_vec()
    if kind == "char":
        return char_vec()
    return make_union(word_vec(), char_vec())


def make_model(algo, kind, C):
    if algo == "lr":
        clf = LogisticRegression(C=C, max_iter=2000, class_weight="balanced")
    else:
        clf = LinearSVC(C=C, class_weight="balanced")
    return make_pipeline(features(kind), clf)


def score_row(name, y_true, y_pred):
    f1s = f1_score(y_true, y_pred, labels=LABELS, average=None, zero_division=0)
    recs = recall_score(y_true, y_pred, labels=LABELS, average=None, zero_division=0)
    precs = precision_score(y_true, y_pred, labels=LABELS, average=None, zero_division=0)
    return {
        "model": name,
        "macro_f1": f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0),
        "f1_safe": f1s[0], "f1_scam": f1s[1], "f1_inj": f1s[2],
        "rec_scam": recs[1], "rec_inj": recs[2],
        "prec_scam": precs[1], "prec_inj": precs[2],
    }


rows = []
fitted = {}

# ---------- 1. Keyword rules (Day 1 baseline) ----------
rows.append(score_row("rules", val["label"], val["text"].map(predict_one)))

# ---------- 2. Learned models, judged on the validation set ----------
configs = []
for kind in ["word", "char", "word+char"]:
    for C in [1, 3]:
        configs.append(("lr", kind, C))
    for C in [0.1, 0.3, 1]:
        configs.append(("svm", kind, C))

for algo, kind, C in configs:
    name = f"{algo} | {kind} | C={C}"
    model = make_model(algo, kind, C)
    model.fit(train["text"], train["label"])
    pred = model.predict(val["text"])
    rows.append(score_row(name, val["label"], pred))
    fitted[name] = pred
    print("done:", name)

table = pd.DataFrame(rows).sort_values("macro_f1", ascending=False).reset_index(drop=True)
print("\n===== All models on the validation set (sorted by macro F1) =====")
print(table.round(3).to_string())

# ---------- 3. Full report for the top model ----------
best = table.iloc[0]["model"]
print(f"\nTop model by macro F1: {best}")
if best in fitted:
    report(f"{best} (val)", val["label"], fitted[best])
else:
    print("The keyword rules came out on top. Check your learned models for problems.")