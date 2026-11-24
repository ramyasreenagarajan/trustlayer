import sys
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, recall_score

sys.stdout.reconfigure(encoding="utf-8")
LABELS = ["safe", "scam", "prompt_injection"]
ATT = {"scam", "prompt_injection"}
NAMES = {"tfidf_svm": "TF-IDF + Linear SVM",
         "distilbert_mbert_v1": "DistilBERT (multilingual)",
         "muril_v1": "MuRIL"}

P = pd.read_csv("data/processed/predictions_test_hard_v1.csv")
MODELS = [c for c in P.columns if c not in ["text", "label", "language", "source", "set"]]
own = P["source"].astype(str).str.startswith("own")
SUBSETS = [("Test", P[P["set"] == "test"]), ("Hard set", P[P["set"] == "hard"]), ("Own rows (test + hard)", P[own])]


def mf1(y, p):
    return f1_score(y, p, labels=LABELS, average="macro", zero_division=0)


def ci(y, p, n=1000, seed=0):
    rng = np.random.default_rng(seed)
    y, p = np.array(y), np.array(p)
    s = [mf1(y[i], p[i]) for i in (rng.integers(0, len(y), len(y)) for _ in range(n))]
    return np.percentile(s, [2.5, 97.5])


def rec(y, p, lab):
    if lab not in set(y):
        return "n/a"
    return f"{recall_score(y, p, labels=[lab], average=None, zero_division=0)[0]:.2f}"


lines = ["| Model | Set | Rows | Macro F1 | 95% range | Recall scam | Recall injection | Missed attacks | False alarms |",
         "|---|---|---|---|---|---|---|---|---|"]
for m in MODELS:
    for sname, d in SUBSETS:
        y, p = d["label"], d[m]
        lo, hi = ci(y, p)
        missed = int(((y.isin(ATT)) & (p == "safe")).sum())
        false_alarm = int(((y == "safe") & (p.isin(ATT))).sum())
        lines.append(f"| {NAMES.get(m, m)} | {sname} | {len(d)} | {mf1(y, p):.3f} | {lo:.2f} to {hi:.2f} | "
                     f"{rec(y, p, 'scam')} | {rec(y, p, 'prompt_injection')} | {missed} | {false_alarm} |")

both = P.copy()
lang = ["", "| Language | Rows | " + " | ".join(NAMES.get(m, m) for m in MODELS) + " | Note |",
        "|---|---|" + "---|" * len(MODELS) + "---|"]
for g, d in both.groupby("language"):
    accs = " | ".join(f"{(d['label'] == d[m]).mean():.2f}" for m in MODELS)
    note = "too few rows to trust" if len(d) < 30 else ""
    lang.append(f"| {g} | {len(d)} | {accs} | {note} |")

out = "\n".join(lines + lang)
open("docs/results_table.md", "w", encoding="utf-8").write(out + "\n")
print(out)
print("\nSaved to docs/results_table.md")