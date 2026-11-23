import pandas as pd

for f in ["sms_review.csv", "deepset_review.csv"]:
    d = pd.read_csv(f"data/audit/{f}", encoding="utf-8-sig", dtype=str).fillna("")
    p = pd.read_csv(f"data/audit/{f.replace('.csv', '_pass1.csv')}", encoding="utf-8-sig", dtype=str).fillna("")
    print(f)
    print("  decisions:", d["decision"].value_counts().to_dict())
    print("  has reason column:", "reason" in d.columns)
    if "reason" in d.columns:
        print("  reasons given for keep rows:", d.loc[d["decision"] == "keep", "reason"].value_counts().to_dict())
    print("  share identical to first pass:", round((d["decision"] == p["decision"]).mean(), 2))
    