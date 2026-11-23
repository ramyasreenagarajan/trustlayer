import pandas as pd

PATH = "data/audit/audit_sample.csv"
d = pd.read_csv(PATH, encoding="utf-8-sig", dtype=str).fillna("")

# edit this list if you disagree with any change
CHANGES = {"9": "drop", "13": "drop", "14": "drop", "43": "drop",
           "61": "drop", "90": "drop", "92": "drop", "103": "drop",
           "110": "drop", "117": "drop"}

for row_id, decision in CHANGES.items():
    d.loc[d["id"] == row_id, "decision"] = decision

d.to_csv(PATH, index=False, encoding="utf-8-sig")
print(d.groupby(["source", "label", "decision"]).size())