import pandas as pd

PATH = "data/audit/audit_sample.csv"
d = pd.read_csv(PATH, encoding="utf-8-sig", dtype=str).fillna("")

# edit this list if you disagree with any change
CHANGES = {"27": "drop", "28": "drop", "31": "drop", "32": "drop", "34": "drop",
           "38": "drop", "40": "drop", "41": "drop", "42": "drop", "45": "drop",
           "50": "drop", "51": "drop", "54": "drop", "55": "drop", "57": "drop",
           "58": "drop", "60": "drop"}

for row_id, decision in CHANGES.items():
    d.loc[d["id"] == row_id, "decision"] = decision

d.to_csv(PATH, index=False, encoding="utf-8-sig")
print(f"Applied {len(CHANGES)} changes")
