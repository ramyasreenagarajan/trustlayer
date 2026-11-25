import json
import sys
import datetime
import platform
import joblib
import numpy as np
import pandas as pd
import sklearn
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import make_pipeline, make_union
from sklearn.metrics import f1_score

from common import load_split, LABELS

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path("models/deploy")
OUT.mkdir(parents=True, exist_ok=True)

C = 0.3  # same value as in train_final.py


def features():
    w = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    c = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)
    return make_union(w, c)


train, val, test = load_split("train"), load_split("val"), load_split("test")
fit = pd.concat([train, val], ignore_index=True)

model = make_pipeline(features(), CalibratedClassifierCV(
    LinearSVC(C=C, class_weight="balanced"), method="sigmoid", cv=5))
model.fit(fit["text"], fit["label"])

pred = model.predict(test["text"])
f1 = f1_score(test["label"], pred, labels=LABELS, average="macro", zero_division=0)
print("Sanity check only (do not tune on it): macro F1 on test =", round(f1, 3))

path = OUT / "model.joblib"
joblib.dump(model, path, compress=3)
size = path.stat().st_size / 1e6
print(f"Saved {path} ({size:.1f} MB)")

card = {
    "name": "trustlayer-tfidf-svm",
    "date": datetime.date.today().isoformat(),
    "trained_on_rows": int(len(fit)),
    "trained_on_splits": ["train", "val"],
    "classes": list(model.classes_),
    "features": "word 1-2 grams + character 2-5 grams, TF-IDF",
    "classifier": f"LinearSVC C={C}, class_weight=balanced, sigmoid calibration (5-fold)",
    "file_size_mb": round(size, 1),
    "python": platform.python_version(),
    "scikit_learn": sklearn.__version__,
    "numpy": np.__version__,
    "data_credits": "SMS Spam Collection (CC BY 4.0), deepset/prompt-injections (Apache 2.0), own examples (CC BY 4.0)",
    "note": "Scores are in docs/results.md. Thresholds are in thresholds.json.",
}
(OUT / "model_card.json").write_text(json.dumps(card, indent=2), encoding="utf-8")
print("Saved models/deploy/model_card.json")