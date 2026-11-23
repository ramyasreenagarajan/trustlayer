import pandas as pd

for f in ["sms_review.csv", "deepset_review.csv"]:
    p = f"data/audit/{f}"
    d = pd.read_csv(p, encoding="utf-8-sig", dtype=str).fillna("")
    d.to_csv(p.replace(".csv", "_pass1.csv"), index=False, encoding="utf-8-sig")
    d["decision"] = ""
    d.to_csv(p, index=False, encoding="utf-8-sig")
    print("cleared", f, len(d), "rows (old answers kept in a _pass1 file)")