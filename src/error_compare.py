import sys
import pandas as pd
from explain import warning_signs

sys.stdout.reconfigure(encoding="utf-8")
P = pd.read_csv("data/processed/predictions_test_hard_v1.csv")
MODELS = [c for c in P.columns if c not in ["text", "label", "language", "source", "set"]]
ATT = {"scam", "prompt_injection"}


def kind(t, p):
    if t == p:
        return "correct"
    if t in ATT and p == "safe":
        return "missed_attack"
    if t == "safe" and p in ATT:
        return "false_alarm"
    return "wrong_type"


rows = []
for m in MODELS:
    P[f"k_{m}"] = [kind(t, p) for t, p in zip(P["label"], P[m])]
    for s, g in P.groupby("set"):
        vc = g[f"k_{m}"].value_counts()
        rows.append({"model": m, "set": s, "rows": len(g), "missed_attack": int(vc.get("missed_attack", 0)),
                     "false_alarm": int(vc.get("false_alarm", 0)), "wrong_type": int(vc.get("wrong_type", 0))})
print("MISTAKE KINDS")
print(pd.DataFrame(rows).to_string(index=False))

wrong = pd.DataFrame({m: P[m] != P["label"] for m in MODELS})
P["n_wrong"] = wrong.sum(axis=1)
print(f"\nRows wrong for ALL models: {(P['n_wrong'] == len(MODELS)).sum()} | for SOME: "
      f"{((P['n_wrong'] > 0) & (P['n_wrong'] < len(MODELS))).sum()} | for NONE: {(P['n_wrong'] == 0).sum()}")

T = P[P["set"] == "test"]
print("\nTEST accuracy by source")
for m in MODELS:
    print(f"  {m}: {(T[m] == T['label']).groupby(T['source']).mean().round(3).to_dict()}")

print("\nHARD set: every row any model got wrong")
for _, r in P[(P["set"] == "hard") & (P["n_wrong"] > 0)].iterrows():
    preds = " | ".join(f"{m}:{r[m]}" for m in MODELS)
    print(f"- true={r['label']} [{r['language']}]  {preds}\n    {r['text'][:130]}")

P["strong"] = P["text"].map(lambda t: any(s["strength"] == "strong" for s in warning_signs(t)))
print("\nRULES vs MODELS (strong warning sign present on the model's mistakes)")
for m in MODELS:
    ma = P[(P["label"].isin(ATT)) & (P[m] == "safe")]
    fa = P[(P["label"] == "safe") & (P[m].isin(ATT))]
    print(f"  {m}: {len(ma)} missed attacks (rules see a strong sign on {int(ma['strong'].sum())}); "
          f"{len(fa)} false alarms (rules fire on {int(fa['strong'].sum())})")

sheet = P[P["n_wrong"] > 0][["set", "text", "label", "language", "source"] + MODELS].copy()
sheet["cause"] = ""
sheet.to_csv("data/processed/error_review2.csv", index=False, encoding="utf-8-sig")
print(f"\nSaved {len(sheet)} mistaken rows to data/processed/error_review2.csv")