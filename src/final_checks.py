import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
S = pd.read_csv("data/audit/sms_review.csv", encoding="utf-8-sig", dtype=str).fillna("")
D = pd.read_csv("data/audit/deepset_review.csv", encoding="utf-8-sig", dtype=str).fillna("")

# 1. How accurate was the pre-sort on the blind rows?
for name, d in [("SMS", S), ("deepset", D)]:
    b = d[d["presort"] != "uncertain"]
    print(f"{name}: {len(b)} blind rows | agreement with you: {(b['presort'] == b['decision']).mean():.0%}")
    if name == "SMS":
        for _, r in b[b["presort"] != b["decision"]].iterrows():
            print(f"   pre-sort {r['presort']}, you {r['decision']}: {r['text'][:120]}")


def sample(df, n, title):
    print(f"\n===== {title} =====")
    for t in df.sample(min(n, len(df)), random_state=11)["text"]:
        print("-", t[:140])


# 2. Are the SMS 'false_story' keeps real scams?
sample(S[S["reason"] == "false_story"], 12, "12 random SMS rows you kept as false_story")
# 3. Are the deepset keeps and drops consistent?
sample(D[D["decision"] == "keep"], 8, "8 random deepset keeps")
sample(D[D["decision"] == "drop"], 8, "8 random deepset drops")