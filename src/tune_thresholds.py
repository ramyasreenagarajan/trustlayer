import json
import sys
import numpy as np
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
S = pd.read_csv("data/processed/scores_trainonly.csv")
S["risk"] = 1 - S["p_safe"]
S["attack"] = S["label"] != "safe"


def stats(d, t):
    flagged = d["risk"] >= t
    n_att, n_safe = int(d["attack"].sum()), int((~d["attack"]).sum())
    caught = int((flagged & d["attack"]).sum())
    fa = int((flagged & ~d["attack"]).sum())
    return {"t": t, "recall": caught / max(n_att, 1), "false_alarm_rate": fa / max(n_safe, 1),
            "precision": caught / max(caught + fa, 1), "caught": caught, "attacks": n_att,
            "false_alarms": fa, "safe": n_safe}


val = S[S["set"] == "val"]
grid = [round(x, 3) for x in np.arange(0.05, 0.951, 0.025)]
table = pd.DataFrame([stats(val, t) for t in grid])
print("VALIDATION: what each threshold does")
print(table[["t", "recall", "false_alarm_rate", "precision"]].round(3).to_string(index=False))

ok = table[table["recall"] >= 0.95]
t_susp = float(ok["t"].max()) if len(ok) else float(table["t"].min())
ok = table[table["precision"] >= 0.95]
t_att = float(ok["t"].min()) if len(ok) else 0.95
t_att = min(max(t_att, t_susp + 0.2), 0.95)
print(f"\nChosen by the rule: T_SUSPICIOUS = {t_susp}, T_ATTACK = {t_att}")

out = {"t_suspicious": t_susp, "t_attack": t_att,
       "tuned_on": "validation rows, scores from a model trained on the train split only"}
Path("models/deploy").mkdir(parents=True, exist_ok=True)
Path("models/deploy/thresholds.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

print("\nREPORTED ONCE, not used for tuning")
for name in ["test", "hard"]:
    d = S[S["set"] == name]
    for label, t in [("chosen", t_susp), ("default 0.25", 0.25)]:
        r = stats(d, t)
        print(f"{name:<5} threshold {label:<13} attacks caught {r['caught']}/{r['attacks']} "
              f"| safe rows flagged {r['false_alarms']}/{r['safe']}")