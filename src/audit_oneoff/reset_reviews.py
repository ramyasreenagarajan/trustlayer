import pandas as pd

for f in ["sms_review.csv", "deepset_review.csv"]:
    p = f"data/audit/{f}"
    d = pd.read_csv(p, encoding="utf-8-sig", dtype=str).fillna("")
    d["decision"] = ""
    if "reason" in d.columns:
        d["reason"] = ""
    d.to_csv(p, index=False, encoding="utf-8-sig")
    print("emptied", f, len(d), "rows")