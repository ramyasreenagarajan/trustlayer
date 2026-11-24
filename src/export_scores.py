import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import make_pipeline, make_union

from common import load_split, PROC

ALGO, KIND, C = "svm", "word+char", 0.3   # same three values as in train_final.py


def vec(kind):
    w = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    c = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)
    return w if kind == "word" else c if kind == "char" else make_union(w, c)


def pipe():
    clf = LogisticRegression(C=C, max_iter=2000, class_weight="balanced") if ALGO == "lr" \
        else LinearSVC(C=C, class_weight="balanced")
    return make_pipeline(vec(KIND), clf)


train = load_split("train")
model = pipe() if ALGO == "lr" else CalibratedClassifierCV(pipe(), method="sigmoid", cv=5)
model.fit(train["text"], train["label"])

out = []
for name in ["val", "test", "hard"]:
    d = load_split(name)
    p = model.predict_proba(d["text"])
    s = d[["text", "label", "language", "source"]].copy()
    s["set"] = name
    for i, cl in enumerate(model.classes_):
        s[f"p_{cl}"] = p[:, i].round(4)
    out.append(s)
pd.concat(out).to_csv(PROC / "scores_trainonly.csv", index=False)
print("saved data/processed/scores_trainonly.csv (model trained on the train split only)")