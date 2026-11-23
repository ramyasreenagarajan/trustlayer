import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
d = pd.read_csv("data/audit/deepset_review.csv", encoding="utf-8-sig", dtype=str).fillna("")
for name in ["keep", "drop"]:
    print(f"\n===== 10 random '{name}' rows =====")
    for t in d[d["decision"] == name].sample(10, random_state=5)["text"]:
        print("-", t[:140])