import json
import datetime
import joblib
import pandas as pd
import sklearn
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import make_pipeline, make_union
from sklearn.metrics import f1_score

from common import load_split, LABELS

# ----- EDIT THESE THREE LINES to match your Day 3 choice -----
ALGO = "svm"        # "lr" or "svm"
KIND = "word+char"  # "word", "char" or "word+char"
C = 0.3
# --------------------------------------------------------------

MODELS = Path("models")
MODELS.mkdir(exist_ok=True)


def word_vec():
    return TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)


def char_vec():
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)


def make_pipe():
    feats = word_vec() if KIND == "word" else char_vec() if KIND == "char" else make_union(word_vec(), char_vec())
    if ALGO == "lr":
        clf = LogisticRegression(C=C, max_iter=2000, class_weight="balanced")
    else:
        clf = LinearSVC(C=C, class_weight="balanced")
    return make_pipeline(feats, clf)


train = load_split("train")
val = load_split("val")
test = load_split("test")

fit_df = pd.concat([train, val], ignore_index=True)
X, y = fit_df["text"], fit_df["label"]
print(f"Training on {len(fit_df)} rows (train + val). Config: {ALGO} | {KIND} | C={C}")

# Pipeline used to explain which words mattered
explainer = make_pipe()
explainer.fit(X, y)

# Model used to output probabilities
if ALGO == "lr":
    proba_model = explainer
else:
    proba_model = CalibratedClassifierCV(make_pipe(), method="sigmoid", cv=5)
    proba_model.fit(X, y)

# Sanity check only: do NOT change the model because of this number
pred = proba_model.predict(test["text"])
test_f1 = f1_score(test["label"], pred, labels=LABELS, average="macro", zero_division=0)
print("Sanity check, macro F1 on test:", round(test_f1, 3))

artifact = {
    "proba_model": proba_model,
    "explainer": explainer,
    "config": {"algo": ALGO, "kind": KIND, "C": C},
}
path = MODELS / "trustlayer_v0.joblib"
joblib.dump(artifact, path, compress=3)
print(f"Saved {path} ({path.stat().st_size / 1e6:.1f} MB)")

card = {
    "name": "trustlayer_v0",
    "date": datetime.date.today().isoformat(),
    "algo": ALGO, "features": KIND, "C": C,
    "classes": list(proba_model.classes_),
    "trained_on_rows": int(len(fit_df)),
    "trained_on_splits": ["train", "val"],
    "sklearn_version": sklearn.__version__,
    "sanity_test_macro_f1": round(float(test_f1), 3),
    "note": "Baseline. Scores per set are in docs/results.md. Thresholds in predict.py are provisional.",
}
(MODELS / "model_card.json").write_text(json.dumps(card, indent=2), encoding="utf-8")
print("Saved models/model_card.json")